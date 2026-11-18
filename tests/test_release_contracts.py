"""Documented Resolve API contracts exercised via registry, client and loopback HTTP."""
import asyncio
import json
import tempfile
import threading
import unittest
from http.server import HTTPServer
from pathlib import Path
from unittest.mock import Mock, call

from src.davinci_mcp.availability import EXPERIMENTAL_TOOLS, SUPPORTED_TOOLS, UNAVAILABLE_TOOLS
from src.davinci_mcp.bridge import BridgeClient
from src.davinci_mcp.config import BridgeConfig
from src.davinci_mcp.schemas import ALL_SCHEMAS
from src.davinci_mcp.tools import ToolRegistry
from test_release_regressions import ROOT, TOKEN, load_bridge


class ResolveContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bridge = load_bridge()
        cls.server = HTTPServer(("127.0.0.1", 0), cls.bridge.BridgeHandler)
        cls.server.bridge_token = TOKEN
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.resolve = self.bridge.resolve_obj = Mock()
        self.manager = self.resolve.GetProjectManager.return_value
        self.project = self.manager.GetCurrentProject.return_value
        self.project.GetName.return_value = "Disposal"
        self.timeline = self.project.GetCurrentTimeline.return_value
        self.timeline.GetName.return_value = "Sequence"
        self.timeline.GetStartFrame.return_value = 86400
        self.timeline.GetEndFrame.return_value = 120000
        self.timeline.GetStartTimecode.return_value = "01:00:00:00"
        self.timeline.GetSetting.side_effect = {"timelineFrameRate": "24", "timelineDropFrameTimecode": "0"}.get
        self.timeline.GetTrackCount.side_effect = lambda kind: 1 if kind == "video" else 0
        self.timeline.GetItemListInTrack.return_value = []
        self.project.IsRenderingInProgress.return_value = False
        self.client = BridgeClient(BridgeConfig(port=self.server.server_port, max_retries=0, token=TOKEN))
        self.registry = ToolRegistry(self.client)

    def tool(self, tool_name, **args):
        return asyncio.run(self.registry.execute(tool_name, args))

    def with_named_clips(self, *names):
        clips = [Mock() for _ in names]
        for clip, name in zip(clips, names):
            clip.GetName.return_value = name
        self.timeline.GetItemListInTrack.return_value = clips
        return clips

    def set_gallery(self):
        gallery = self.project.GetGallery.return_value
        album = Mock()
        stills = [Mock(), Mock()]
        album.GetStills.return_value = stills
        album.GetLabel.side_effect = {stills[0]: "first", stills[1]: "second"}.get
        gallery.GetCurrentStillAlbum.return_value = Mock()
        gallery.GetGalleryStillAlbums.return_value = [album]
        gallery.GetGalleryPowerGradeAlbums.return_value = []
        gallery.GetAlbumName.return_value = "targets"
        return gallery, album, stills

    def test_scope_matches_manifest(self):
        manifest = json.loads((ROOT / "manifests/tool-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["tool_availability"]["SUPPORTED"]), SUPPORTED_TOOLS)
        self.assertEqual(set(manifest["tool_availability"]["EXPERIMENTAL"]), EXPERIMENTAL_TOOLS)
        self.assertEqual(set(manifest["tool_availability"]["UNAVAILABLE"]), UNAVAILABLE_TOOLS)
        self.assertEqual(SUPPORTED_TOOLS | EXPERIMENTAL_TOOLS | UNAVAILABLE_TOOLS, set(ALL_SCHEMAS))
        self.assertFalse(SUPPORTED_TOOLS & (EXPERIMENTAL_TOOLS | UNAVAILABLE_TOOLS))

    def test_read_project_page_timeline_and_selected_track(self):
        self.resolve.GetCurrentPage.return_value = "edit"
        self.project.GetTimelineCount.return_value = 1
        self.project.GetSetting.return_value = ""
        self.timeline.GetTrackName.return_value = "Video"
        self.timeline.GetCurrentTimecode.return_value = "01:00:00:00"
        self.timeline.GetMarkInOut.return_value = {}
        self.timeline.GetSetting.return_value = ""
        self.timeline.GetSetting.side_effect = None
        self.timeline.GetTrackCount.side_effect = lambda kind: 2 if kind == "audio" else 0
        self.with_named_clips()
        self.assertEqual(self.tool("get_project_info").data["name"], "Disposal")
        self.assertEqual(self.tool("get_current_page").data["page"], "edit")
        self.assertEqual(self.tool("get_timeline_info", timeline_name="Sequence").data["name"], "Sequence")
        result = self.tool("get_timeline_clips", track_type="audio", track_index=2)
        self.assertTrue(result.success, result.error)
        self.timeline.GetItemListInTrack.assert_called_once_with("audio", 2)

    def test_playhead_converts_offset_and_rejects_wrong_context_or_range(self):
        self.assertTrue(self.tool("set_playhead", frame=25, timeline_name="Sequence").success)
        self.timeline.SetCurrentTimecode.assert_called_once_with("01:00:01:01")
        for args in ({"frame": 0, "timeline_name": "Other"}, {"frame": 50000}, {"frame": True}):
            self.assertFalse(self.tool("set_playhead", **args).success)
        self.assertEqual(self.timeline.SetCurrentTimecode.call_count, 1)

    def test_drop_frame_minute_and_tenth_minute(self):
        self.timeline.GetEndFrame.return_value = 200000
        for rate, initial, minute, ten, skipped in (
                ("29.97", "01:00:00;00", 1800, 17982, 2),
                ("59.94", "01:00:00;00", 3600, 35964, 4)):
            self.timeline.GetSetting.side_effect = {"timelineFrameRate": rate}.get
            self.timeline.GetStartTimecode.return_value = initial
            self.assertEqual(self.bridge._timeline_timecode(self.timeline, minute - 1),
                             f"01:00:59;{minute // 60 - 1:02}")
            self.assertEqual(self.bridge._timeline_timecode(self.timeline, minute), f"01:01:00;{skipped:02}")
            self.assertEqual(self.bridge._timeline_timecode(self.timeline, ten), "01:10:00;00")
            self.timeline.GetStartTimecode.return_value = "01:01:00;00"
            with self.assertRaises(ValueError):
                self.bridge._timeline_timecode(self.timeline, 0)

    def test_windows_and_posix_file_import_use_the_selected_folder(self):
        pool = self.project.GetMediaPool.return_value
        folder, original, clip = Mock(), Mock(), Mock()
        pool.GetRootFolder.return_value = Mock()
        pool.GetRootFolder.return_value.GetSubFolderList.return_value = [folder]
        folder.GetName.return_value = "Test"
        pool.GetCurrentFolder.return_value = original
        pool.ImportMedia.return_value = [clip]
        clip.GetName.return_value = "synthetic.wav"
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "synthetic.wav"
            source.touch()
            self.assertTrue(self.tool("import_media", file_paths=[str(source)], folder_path="Test").success)
            pool.ImportMedia.assert_called_once_with([str(source)])
            self.assertEqual(pool.SetCurrentFolder.call_args_list, [call(folder), call(original)])
            self.assertFalse(self.tool("import_media", file_paths=[str(source)], folder_path="Missing").success)
            self.assertEqual(pool.ImportMedia.call_count, 1)

    def test_clip_list_mutations_resolve_every_target(self):
        first, second = self.with_named_clips("one", "two")
        invalid = (["one", "missing"], ["one", "one"])
        for names in invalid:
            self.assertFalse(self.tool("delete_timeline_clips", clip_names=names).success)
        for name in ("link_timeline_clips", "create_compound_clip", "create_fusion_clip"):
            opts = {"name": "Merged"} if name.startswith("create_") else {}
            self.assertFalse(self.tool(name, clip_names=["one", "missing"], **opts).success)
        self.timeline.DeleteClips.assert_not_called()
        self.timeline.SetClipsLinked.assert_not_called()
        self.timeline.CreateCompoundClip.assert_not_called()
        self.timeline.CreateFusionClip.assert_not_called()
        self.assertTrue(self.tool("delete_timeline_clips", clip_names=["one"]).success)
        self.assertTrue(self.tool("link_timeline_clips", clip_names=["one", "two"]).success)
        self.assertTrue(self.tool("create_compound_clip", clip_names=["one", "two"], name="Compound").success)
        self.assertTrue(self.tool("create_fusion_clip", clip_names=["one", "two"], name="Fusion").success)
        self.timeline.DeleteClips.assert_called_once_with([first], False)
        self.timeline.SetClipsLinked.assert_called_once_with([first, second], True)
        self.timeline.CreateCompoundClip.assert_called_once_with([first, second], {"name": "Compound"})
        self.timeline.CreateFusionClip.assert_called_once_with([first, second])
        self.timeline.CreateFusionClip.return_value.SetName.assert_called_once_with("Fusion")

    def test_render_index_and_stable_id_use_exact_job(self):
        self.project.GetRenderJobList.return_value = [{"JobId": "A"}, {"JobId": "B"}]
        self.project.GetRenderJobStatus.return_value = {"JobStatus": "Complete"}
        self.assertEqual(self.tool("get_render_settings").data["renderJobList"], [{"JobId": "A"}, {"JobId": "B"}])
        self.assertTrue(self.tool("get_render_job_status", job_index=1).success)
        self.project.GetRenderJobStatus.assert_called_once_with("B")
        for selectors in ({}, {"job_index": 4}, {"job_index": 1, "job_id": "A"}):
            self.assertFalse(self.tool("delete_render_job", **selectors).success)
        self.project.DeleteRenderJob.assert_not_called()
        self.assertTrue(self.tool("delete_render_job", job_id="A").success)
        self.assertTrue(self.tool("delete_render_job", job_index=1).success)
        self.assertEqual(self.project.DeleteRenderJob.call_args_list, [call("A"), call("B")])

    def test_render_mode_uses_documented_numeric_mapping(self):
        self.assertTrue(self.tool("set_render_mode", mode="single").success)
        self.assertTrue(self.tool("set_render_mode", mode="individual_clips").success)
        self.assertFalse(self.tool("set_render_mode", mode="unknown").success)
        self.assertEqual(self.project.SetCurrentRenderMode.call_args_list, [call(1), call(0)])

    def test_render_wait_success_uses_single_mutation(self):
        self.project.GetRenderJobList.return_value = [{"JobId": "A"}]
        self.project.GetRenderJobStatus.side_effect = [{"JobStatus": "Rendering"}, {"JobStatus": "Complete"}]
        result = self.tool("start_rendering", wait_for_completion=True, completion_timeout=3)
        self.assertTrue(result.success, result.error)
        self.assertEqual(result.data["jobStatus"], {"A": "complete"})
        self.project.StartRendering.assert_called_once_with(["A"])
        self.assertEqual(self.project.GetRenderJobStatus.call_args_list, [call("A"), call("A")])

    def test_render_wait_timeout_reports_ids_without_replay(self):
        self.project.GetRenderJobList.return_value = [{"JobId": "A"}, {"JobId": "B"}]
        self.project.GetRenderJobStatus.return_value = {"JobStatus": "Rendering"}
        result = self.tool("start_rendering", wait_for_completion=True, completion_timeout=0.1)
        self.assertEqual(result.error.code, "BRIDGE_OUTCOME_UNKNOWN")
        self.assertEqual(result.error.details["jobIds"], ["A", "B"])
        self.assertFalse(result.error.details["retry_safe"])
        self.project.StartRendering.assert_called_once_with(["A", "B"])

    def test_render_failure_and_invalid_wait_options(self):
        self.project.GetRenderJobList.return_value = [{"JobId": "A"}]
        self.project.GetRenderJobStatus.return_value = {"JobStatus": "Failed"}
        self.assertFalse(self.tool("start_rendering", completion_timeout=1).success)
        self.project.StartRendering.assert_not_called()
        result = self.tool("start_rendering", wait_for_completion=True)
        self.assertEqual(result.error.code, "RENDER_JOB_FAILED")
        self.project.StartRendering.assert_called_once_with(["A"])

    def test_gallery_read_and_mutation_never_fall_back_to_current_album(self):
        gallery, album, stills = self.set_gallery()
        listed = self.tool("get_gallery_albums")
        self.assertTrue(listed.success, listed.error)
        found = self.tool("get_album_stills", album_name="targets")
        self.assertTrue(found.success, found.error)
        self.assertEqual([s["label"] for s in found.data["stills"]], ["first", "second"])
        self.assertTrue(self.tool("set_current_album", album_name="targets").success)
        gallery.SetCurrentStillAlbum.assert_called_once_with(album)
        self.assertTrue(self.tool("set_still_label", album_name="targets", still_label="first", new_label="renamed").success)
        album.SetLabel.assert_called_once_with(stills[0], "renamed")
        self.assertTrue(self.tool("delete_stills", album_name="targets", still_labels=["second"]).success)
        album.DeleteStills.assert_called_once_with([stills[1]])
        self.assertFalse(self.tool("delete_stills", album_name="targets", still_labels=["first", "missing"]).success)
        album.GetLabel.side_effect = lambda still: "duplicate"
        self.assertFalse(self.tool("delete_stills", album_name="targets", still_labels=["duplicate"]).success)
        gallery.GetGalleryPowerGradeAlbums.return_value = [Mock()]
        self.assertFalse(self.tool("delete_stills", album_name="targets", still_labels=["first"]).success)
        self.assertEqual(album.DeleteStills.call_count, 1)
        gallery.GetCurrentStillAlbum.return_value.DeleteStills.assert_not_called()

    def test_project_database_mismatch_and_ambiguity_prevent_mutation(self):
        local = {"DbName": "Temporary", "DbType": "Disk"}
        remote = {"DbName": "Remote", "DbType": "PostgreSQL", "IpAddress": "127.0.0.1"}
        self.manager.GetDatabaseList.return_value = [local, remote]
        self.manager.GetCurrentDatabase.return_value = local
        self.assertEqual(self.tool("get_database_list").data["currentDatabase"], local)
        for name in ("create_project", "load_project", "delete_project"):
            self.assertFalse(self.tool(name, project_name="Fixture", database_name="Remote").success)
        self.manager.CreateProject.assert_not_called()
        self.manager.LoadProject.assert_not_called()
        self.manager.DeleteProject.assert_not_called()
        self.assertTrue(self.tool("create_project", project_name="Fixture", database_name="Temporary").success)
        self.assertTrue(self.tool("load_project", project_name="Fixture", database_name="Temporary").success)
        self.assertTrue(self.tool("delete_project", project_name="Fixture", database_name="Temporary").success)
        self.assertTrue(self.tool("set_database", database_name="Remote").success)
        self.manager.SetCurrentDatabase.assert_called_once_with(remote)
        self.manager.GetDatabaseList.return_value = [local, {**remote, "DbName": "Temporary"}]
        self.assertFalse(self.tool("set_database", database_name="Temporary").success)
        self.assertEqual(self.manager.SetCurrentDatabase.call_count, 1)

    def test_template_placement_options_reject_before_any_edit(self):
        for tool, selector in (("insert_title", "title_name"), ("insert_generator", "generator_name"),
                               ("insert_fusion_composition", "composition_name")):
            result = self.tool(tool, **{selector: "template", "track_type": "video", "track_index": 1, "frame": 0})
            self.assertFalse(result.success)
        self.timeline.InsertTitleIntoTimeline.assert_not_called()
        self.timeline.InsertGeneratorIntoTimeline.assert_not_called()
        self.timeline.InsertFusionCompositionIntoTimeline.assert_not_called()
        self.timeline.SetCurrentTimecode.assert_not_called()

    def test_fusion_export_selects_name_and_rejects_overwrite(self):
        [clip] = self.with_named_clips("item")
        clip.GetFusionCompNameList.return_value = ["first", "second"]
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "disposable.comp"
            args = {"clip_name": "item", "comp_name": "second", "file_path": str(destination)}
            self.assertTrue(self.tool("export_fusion_comp_from_clip", **args).success)
            destination.touch()
            self.assertFalse(self.tool("export_fusion_comp_from_clip", **args).success)
            clip.ExportFusionComp.assert_called_once_with(str(destination), 2)

    def test_cache_and_take_options_match_resolve_contract(self):
        [clip] = self.with_named_clips("item")
        clip.GetTakesCount.return_value = 3
        clip.GetSelectedTakeIndex.return_value = 2
        self.assertTrue(self.tool("set_clip_cache", clip_name="item", cache_type="fusion", cache_mode="auto").success)
        self.assertFalse(self.tool("set_clip_cache", clip_name="item", cache_type="color", cache_mode="auto").success)
        self.assertTrue(self.tool("set_clip_cache", clip_name="item", cache_mode="disabled").success)
        clip.SetFusionOutputCache.assert_called_once_with(-1)
        clip.SetColorOutputCache.assert_called_once_with(0)
        self.assertTrue(self.tool("select_take", clip_name="item", take_number=2).success)
        self.assertTrue(self.tool("delete_take", clip_name="item", take_number=3).success)
        self.assertFalse(self.tool("delete_take", clip_name="item", take_number=4).success)
        self.assertFalse(self.tool("finalize_take", clip_name="item", take_number=1).success)
        self.assertTrue(self.tool("finalize_take", clip_name="item", take_number=2).success)
        clip.SelectTakeByIndex.assert_called_once_with(2)
        clip.DeleteTakeByIndex.assert_called_once_with(3)
        clip.FinalizeTake.assert_called_once_with()

    def test_timeline_and_frame_export_use_explicit_format_and_new_path(self):
        self.resolve.EXPORT_AAF = 10
        self.resolve.EXPORT_AAF_NEW = 20
        with tempfile.TemporaryDirectory() as directory:
            aaf = str(Path(directory) / "disposable.aaf")
            png = str(Path(directory) / "disposable.png")
            self.assertTrue(self.tool("export_timeline", file_path=aaf, format="aaf").success)
            self.timeline.Export.assert_called_once_with(aaf, 10, 20)
            self.assertFalse(self.tool("export_timeline", file_path=aaf, format="drx").success)
            self.assertFalse(self.tool("export_current_frame", file_path=png, format="jpg").success)
            self.assertTrue(self.tool("export_current_frame", file_path=png).success)
            self.project.ExportCurrentFrameAsStill.assert_called_once_with(png)
