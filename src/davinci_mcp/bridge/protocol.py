"""
Protocol definitions for the DaVinci Resolve HTTP bridge.
"""

from dataclasses import dataclass
from typing import Any, Optional
from enum import Enum


class BridgeMethod(str, Enum):
    """HTTP methods supported by the bridge."""
    GET = "GET"
    POST = "POST"


@dataclass(frozen=True)
class BridgeRequest:
    """A request to the bridge."""
    method: BridgeMethod
    path: str
    params: dict
    body: Optional[dict] = None
    request_id: Optional[str] = None


@dataclass(frozen=True)
class BridgeResponse:
    """A response from the bridge."""
    status_code: int
    data: Any
    request_id: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        return 500 <= self.status_code < 600


# Standard bridge endpoints
class BridgeEndpoints:
    """Known bridge endpoints."""

    # Read endpoints (GET)
    STATUS = "/status"
    PROJECT = "/project"
    PAGE = "/page"
    TIMELINE = "/timeline"
    TIMELINE_CLIPS = "/timeline/clips"
    TIMELINE_MARKERS = "/timeline/markers"
    TIMELINE_CURRENT_ITEM = "/timeline/current-item"
    TIMELINE_THUMBNAIL = "/timeline/thumbnail"
    RENDER = "/render"
    RENDER_RESOLUTIONS = "/render/resolutions"
    RENDER_QUICK_EXPORT_PRESETS = "/render/quick-export-presets"
    MEDIAPOOL = "/mediapool"
    MEDIAPOOL_STRUCTURE = "/mediapool/structure"
    MEDIAPOOL_CLIP_METADATA = "/mediapool/clip/metadata"
    MEDIAPOOL_CLIP_INFO = "/mediapool/clip/info"
    CLIP_MARKERS = "/clip/markers"
    CLIP_FLAGS = "/clip/flags"
    CLIP_NODE_GRAPH = "/clip/node-graph"
    CLIP_COLOR_VERSIONS = "/clip/color-versions"
    CLIP_FUSION_COMPS = "/clip/fusion-comps"
    CLIP_TAKES = "/clip/takes"
    CLIP_LINKED_ITEMS = "/clip/linked-items"
    COLOR_GROUPS = "/color/groups"
    AUDIO_VOICE_ISOLATION = "/audio/voice-isolation"
    FAIRLIGHT_PRESETS = "/fairlight/presets"
    GALLERY_ALBUMS = "/gallery/albums"
    GALLERY_STILLS = "/gallery/stills"
    KEYFRAME_MODE = "/keyframe-mode"
    PROJECTS = "/projects"
    DATABASES = "/databases"
    MEDIA_STORAGE = "/media-storage"

    # Write endpoints (POST)
    PAGE_WRITE = "/page"
    PLAYHEAD = "/playhead"
    MARKER_ADD = "/marker/add"
    MARKER_DELETE = "/marker/delete"
    TIMELINE_SWITCH = "/timeline/switch"
    TIMELINE_CREATE = "/timeline/create"
    TIMELINE_RENAME = "/timeline/rename"
    TIMELINE_DUPLICATE = "/timeline/duplicate"
    TIMELINE_EXPORT = "/timeline/export"
    TIMELINE_MARK_IN_OUT = "/timeline/mark-in-out"
    TIMELINE_CLEAR_MARK_IN_OUT = "/timeline/clear-mark-in-out"
    TIMELINE_CLIPS_DELETE = "/timeline/clips/delete"
    TIMELINE_CLIPS_LINK = "/timeline/clips/link"
    TIMELINE_COMPOUND_CLIP = "/timeline/compound-clip"
    TIMELINE_FUSION_CLIP = "/timeline/fusion-clip"
    TRACK_ADD = "/track/add"
    TRACK_DELETE = "/track/delete"
    TRACK_ENABLE = "/track/enable"
    TRACK_LOCK = "/track/lock"
    TRACK_NAME = "/track/name"
    IMPORT_MEDIA = "/mediapool/import"
    TIMELINE_APPEND = "/timeline/append"
    TIMELINE_INSERT = "/timeline/insert"
    CLIP_COLOR = "/clip/color"
    CLIP_ENABLED = "/clip/enabled"
    CLIP_PROPERTIES = "/clip/properties"
    TITLE_INSERT = "/title/insert"
    GENERATOR_INSERT = "/generator/insert"
    FUSION_COMP_INSERT = "/fusion/comp/insert"
    RENDER_SETTINGS = "/render/settings"
    RENDER_FORMAT = "/render/format"
    RENDER_ADD_JOB = "/render/job/add"
    RENDER_START = "/render/start"
    RENDER_STOP = "/render/stop"
    RENDER_DELETE_JOB = "/render/job/delete"
    PROJECT_SAVE = "/project/save"
    PROJECT_SETTING = "/project/setting"
    TIMELINE_SETTING = "/timeline/setting"
    EXPORT_FRAME = "/export/frame"
    SUBTITLES_CREATE = "/subtitles/create"
    SCENE_CUTS_DETECT = "/scene-cuts/detect"
    MEDIAPOOL_FOLDER_CREATE = "/mediapool/folder/create"
    MEDIAPOOL_NAVIGATE = "/mediapool/navigate"
    CLIP_METADATA_SET = "/clip/metadata/set"
    POOL_CLIP_PROPERTY = "/pool/clip/property"
    MEDIAPOOL_CLIPS_DELETE = "/mediapool/clips/delete"
    MEDIAPOOL_CLIPS_MOVE = "/mediapool/clips/move"
    MEDIAPOOL_CLIPS_RELINK = "/mediapool/clips/relink"
    MEDIAPOOL_CLIPS_UNLINK = "/mediapool/clips/unlink"
    AUTO_SYNC_AUDIO = "/auto-sync/audio"
    IMPORT_TIMELINE = "/timeline/import"
    EXPORT_METADATA = "/export/metadata"
    IMPORT_MEDIA_STORAGE = "/media-storage/import"
    CLIP_MARKER_ADD = "/clip/marker/add"
    CLIP_MARKER_GET = "/clip/marker/get"
    CLIP_MARKER_DELETE = "/clip/marker/delete"
    CLIP_FLAG_ADD = "/clip/flag/add"
    CLIP_FLAG_GET = "/clip/flag/get"
    CLIP_FLAG_CLEAR = "/clip/flag/clear"
    TIMELINE_CLIPS_DELETE_V2 = "/timeline/clips/delete-v2"
    TIMELINE_CLIPS_LINK_V2 = "/timeline/clips/link-v2"
    COMPOUND_CLIP_CREATE = "/compound-clip/create"
    FUSION_CLIP_CREATE = "/fusion-clip/create"
    CURRENT_VIDEO_ITEM = "/current-video-item"
    CLIP_THUMBNAIL = "/clip/thumbnail"
    TIMELINE_EXPORT_V2 = "/timeline/export-v2"
    GALLERY_ALBUMS_GET = "/gallery/albums/get"
    ALBUM_STILLS_GET = "/album/stills/get"
    ALBUM_CURRENT_SET = "/album/current/set"
    GALLERY_ALBUM_CREATE = "/gallery/album/create"
    GRAB_STILL = "/grab/still"
    GRAB_ALL_STILLS = "/grab/all-stills"
    EXPORT_STILLS = "/export/stills"
    IMPORT_STILLS = "/import/stills"
    STILLS_DELETE = "/stills/delete"
    STILL_LABEL_SET = "/still/label/set"
    NODE_GRAPH_GET = "/node-graph/get"
    LUT_SET = "/lut/set"
    LUT_GET = "/lut/get"
    NODE_ENABLE_SET = "/node/enable/set"
    GRADE_FROM_DRX = "/grade/from-drx"
    RESET_ALL_GRADES = "/reset/all-grades"
    ARRI_CDL_LUT = "/arri/cdl-lut"
    CDL_SET = "/cdl/set"
    LUT_EXPORT = "/lut/export"
    GRADES_COPY = "/grades/copy"
    NODE_COLORS_RESET = "/node/colors/reset"
    COLOR_VERSIONS_GET = "/color/versions/get"
    COLOR_VERSION_ADD = "/color/version/add"
    COLOR_VERSION_LOAD = "/color/version/load"
    COLOR_VERSION_DELETE = "/color/version/delete"
    COLOR_VERSION_RENAME = "/color/version/rename"
    COLOR_GROUPS_GET = "/color/groups/get"
    COLOR_GROUP_ADD = "/color/group/add"
    COLOR_GROUP_DELETE = "/color/group/delete"
    COLOR_GROUP_ASSIGN = "/color/group/assign"
    COLOR_GROUP_REMOVE = "/color/group/remove"
    FUSION_COMPS_GET = "/fusion/comps/get"
    FUSION_COMP_ADD = "/fusion/comp/add"
    FUSION_COMP_IMPORT = "/fusion/comp/import"
    FUSION_COMP_EXPORT = "/fusion/comp/export"
    FUSION_COMP_DELETE = "/fusion/comp/delete"
    FUSION_COMP_LOAD = "/fusion/comp/load"
    FUSION_COMP_RENAME = "/fusion/comp/rename"
    MAGIC_MASK_CREATE = "/magic-mask/create"
    MAGIC_MASK_REGENERATE = "/magic-mask/regenerate"
    STABILIZE_CLIP = "/stabilize/clip"
    SMART_REFRAME = "/smart-reframe/clip"
    FAIRLIGHT_PRESETS_GET = "/fairlight/presets/get"
    FAIRLIGHT_PRESET_APPLY = "/fairlight/preset/apply"
    AUDIO_INSERT = "/audio/insert"
    VOICE_ISOLATION_GET = "/voice-isolation/get"
    VOICE_ISOLATION_SET = "/voice-isolation/set"
    TAKES_GET = "/takes/get"
    TAKE_ADD = "/take/add"
    TAKE_SELECT = "/take/select"
    TAKE_DELETE = "/take/delete"
    TAKE_FINALIZE = "/take/finalize"
    PROXY_LINK = "/proxy/link"
    PROXY_UNLINK = "/proxy/unlink"
    CLIP_REPLACE = "/clip/replace"
    CLIP_CACHE = "/clip/cache"
    SIDECAR_UPDATE = "/sidecar/update"
    LINKED_ITEMS_GET = "/linked-items/get"
    TIMELINE_MARK_IN_OUT_SET = "/timeline/mark-in-out/set"
    TIMELINE_MARK_IN_OUT_CLEAR = "/timeline/mark-in-out/clear"
    PROJECT_LIST = "/projects/list"
    DATABASE_LIST = "/databases/list"
    PROJECT_LOAD = "/project/load"
    PROJECT_CREATE = "/project/create"
    PROJECT_DELETE = "/project/delete"
    PROJECT_ARCHIVE = "/project/archive"
    PROJECT_EXPORT = "/project/export"
    PROJECT_IMPORT = "/project/import"
    PROJECT_FOLDER_NAVIGATE = "/project/folder/navigate"
    DATABASE_SET = "/database/set"
    LAYOUT_PRESET = "/layout/preset"
    RENDER_PRESET = "/render/preset"
    BURNIN_PRESET = "/burnin/preset"
    KEYFRAME_MODE_GET = "/keyframe-mode/get"
    KEYFRAME_MODE_SET = "/keyframe-mode/set"
    RENDER_JOB_STATUS = "/render/job/status"
    RENDER_RESOLUTIONS_GET = "/render/resolutions/get"
    QUICK_EXPORT_PRESETS_GET = "/quick-export/presets/get"
    QUICK_EXPORT = "/quick-export"
    RENDER_MODE_SET = "/render/mode/set"
    LUT_LIST_REFRESH = "/lut/list/refresh"
    MEDIA_STORAGE_GET = "/media-storage/get"
    REVEAL_IN_STORAGE = "/reveal-in-storage"
    VOICE_ISOLATE = "/voice-isolate"
    VOICE_ISOLATE_TIMELINE = "/voice-isolate/timeline"
    REMOVE_BACKGROUND = "/remove-background"
    REMOVE_BACKGROUND_VIDEO = "/remove-background/video"
    REMOVE_BACKGROUND_CLIP = "/remove-background/clip"
    TIMELINE_TRANSCRIBE = "/timeline/transcribe"
    FILE_TRANSCRIBE = "/file/transcribe"
    BRIDGE_SHUTDOWN = "/bridge/shutdown"


# Mapping of tool names to bridge endpoints and methods
TOOL_TO_ENDPOINT = {
    # Project/Status tools
    "get_resolve_status": (BridgeMethod.GET, BridgeEndpoints.STATUS),
    "get_project_info": (BridgeMethod.GET, BridgeEndpoints.PROJECT),
    "get_current_page": (BridgeMethod.GET, BridgeEndpoints.PAGE),
    "open_page": (BridgeMethod.POST, BridgeEndpoints.PAGE_WRITE),

    # Timeline tools
    "get_timeline_info": (BridgeMethod.GET, BridgeEndpoints.TIMELINE),
    "get_timeline_clips": (BridgeMethod.GET, BridgeEndpoints.TIMELINE_CLIPS),
    "get_timeline_markers": (BridgeMethod.GET, BridgeEndpoints.TIMELINE_MARKERS),
    "set_playhead": (BridgeMethod.POST, BridgeEndpoints.PLAYHEAD),
    "add_marker": (BridgeMethod.POST, BridgeEndpoints.MARKER_ADD),
    "delete_markers": (BridgeMethod.POST, BridgeEndpoints.MARKER_DELETE),
    "switch_timeline": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_SWITCH),
    "create_timeline": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_CREATE),
    "rename_timeline": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_RENAME),
    "duplicate_timeline": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_DUPLICATE),
    "export_timeline": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_EXPORT),
    "set_timeline_mark_in_out": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_MARK_IN_OUT),
    "clear_timeline_mark_in_out": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_CLEAR_MARK_IN_OUT),
    "delete_timeline_clips": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_CLIPS_DELETE),
    "link_timeline_clips": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_CLIPS_LINK),
    "create_compound_clip": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_COMPOUND_CLIP),
    "create_fusion_clip": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_FUSION_CLIP),

    # Track tools
    "add_track": (BridgeMethod.POST, BridgeEndpoints.TRACK_ADD),
    "delete_track": (BridgeMethod.POST, BridgeEndpoints.TRACK_DELETE),
    "set_track_enable": (BridgeMethod.POST, BridgeEndpoints.TRACK_ENABLE),
    "set_track_lock": (BridgeMethod.POST, BridgeEndpoints.TRACK_LOCK),
    "set_track_name": (BridgeMethod.POST, BridgeEndpoints.TRACK_NAME),

    # Media pool tools
    "get_media_pool": (BridgeMethod.GET, BridgeEndpoints.MEDIAPOOL),
    "get_clip_properties": (BridgeMethod.GET, BridgeEndpoints.MEDIAPOOL_CLIP_INFO),
    "import_media": (BridgeMethod.POST, BridgeEndpoints.IMPORT_MEDIA),
    "append_to_timeline": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_APPEND),
    "insert_to_timeline": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_INSERT),
    "set_clip_color": (BridgeMethod.POST, BridgeEndpoints.CLIP_COLOR),
    "set_clip_enabled": (BridgeMethod.POST, BridgeEndpoints.CLIP_ENABLED),
    "set_clip_properties": (BridgeMethod.POST, BridgeEndpoints.CLIP_PROPERTIES),
    "insert_title": (BridgeMethod.POST, BridgeEndpoints.TITLE_INSERT),
    "insert_generator": (BridgeMethod.POST, BridgeEndpoints.GENERATOR_INSERT),
    "insert_fusion_composition": (BridgeMethod.POST, BridgeEndpoints.FUSION_COMP_INSERT),

    # Render tools
    "get_render_settings": (BridgeMethod.GET, BridgeEndpoints.RENDER),
    "set_render_settings": (BridgeMethod.POST, BridgeEndpoints.RENDER_SETTINGS),
    "set_render_format": (BridgeMethod.POST, BridgeEndpoints.RENDER_FORMAT),
    "get_render_formats": (BridgeMethod.GET, BridgeEndpoints.RENDER_RESOLUTIONS),
    "add_render_job": (BridgeMethod.POST, BridgeEndpoints.RENDER_ADD_JOB),
    "start_rendering": (BridgeMethod.POST, BridgeEndpoints.RENDER_START),
    "stop_rendering": (BridgeMethod.POST, BridgeEndpoints.RENDER_STOP),
    "delete_render_job": (BridgeMethod.POST, BridgeEndpoints.RENDER_DELETE_JOB),
    "get_render_job_status": (BridgeMethod.GET, BridgeEndpoints.RENDER_JOB_STATUS),
    "get_render_resolutions": (BridgeMethod.GET, BridgeEndpoints.RENDER_RESOLUTIONS_GET),
    "get_quick_export_presets": (BridgeMethod.GET, BridgeEndpoints.QUICK_EXPORT_PRESETS_GET),
    "quick_export": (BridgeMethod.POST, BridgeEndpoints.QUICK_EXPORT),
    "set_render_mode": (BridgeMethod.POST, BridgeEndpoints.RENDER_MODE_SET),

    # Project tools
    "save_project": (BridgeMethod.POST, BridgeEndpoints.PROJECT_SAVE),
    "set_project_setting": (BridgeMethod.POST, BridgeEndpoints.PROJECT_SETTING),
    "set_timeline_setting": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_SETTING),
    "export_current_frame": (BridgeMethod.POST, BridgeEndpoints.EXPORT_FRAME),
    "create_subtitles_from_audio": (BridgeMethod.POST, BridgeEndpoints.SUBTITLES_CREATE),
    "detect_scene_cuts": (BridgeMethod.POST, BridgeEndpoints.SCENE_CUTS_DETECT),
    "get_media_pool_structure": (BridgeMethod.GET, BridgeEndpoints.MEDIAPOOL_STRUCTURE),
    "navigate_media_pool": (BridgeMethod.POST, BridgeEndpoints.MEDIAPOOL_NAVIGATE),
    "create_media_pool_folder": (BridgeMethod.POST, BridgeEndpoints.MEDIAPOOL_FOLDER_CREATE),
    "get_clip_metadata": (BridgeMethod.GET, BridgeEndpoints.MEDIAPOOL_CLIP_METADATA),
    "set_clip_metadata": (BridgeMethod.POST, BridgeEndpoints.CLIP_METADATA_SET),
    "get_clip_info": (BridgeMethod.GET, BridgeEndpoints.MEDIAPOOL_CLIP_INFO),
    "set_pool_clip_property": (BridgeMethod.POST, BridgeEndpoints.POOL_CLIP_PROPERTY),
    "delete_media_pool_clips": (BridgeMethod.POST, BridgeEndpoints.MEDIAPOOL_CLIPS_DELETE),
    "move_media_pool_clips": (BridgeMethod.POST, BridgeEndpoints.MEDIAPOOL_CLIPS_MOVE),
    "relink_media_pool_clips": (BridgeMethod.POST, BridgeEndpoints.MEDIAPOOL_CLIPS_RELINK),
    "unlink_media_pool_clips": (BridgeMethod.POST, BridgeEndpoints.MEDIAPOOL_CLIPS_UNLINK),
    "auto_sync_audio": (BridgeMethod.POST, BridgeEndpoints.AUTO_SYNC_AUDIO),
    "import_timeline_from_file": (BridgeMethod.POST, BridgeEndpoints.IMPORT_TIMELINE),
    "export_metadata": (BridgeMethod.POST, BridgeEndpoints.EXPORT_METADATA),
    "import_media_from_storage": (BridgeMethod.POST, BridgeEndpoints.IMPORT_MEDIA_STORAGE),

    # Clip marker tools
    "add_clip_marker": (BridgeMethod.POST, BridgeEndpoints.CLIP_MARKER_ADD),
    "get_clip_markers": (BridgeMethod.GET, BridgeEndpoints.CLIP_MARKER_GET),
    "delete_clip_markers": (BridgeMethod.POST, BridgeEndpoints.CLIP_MARKER_DELETE),

    # Clip flag tools
    "add_clip_flag": (BridgeMethod.POST, BridgeEndpoints.CLIP_FLAG_ADD),
    "get_clip_flags": (BridgeMethod.GET, BridgeEndpoints.CLIP_FLAG_GET),
    "clear_clip_flags": (BridgeMethod.POST, BridgeEndpoints.CLIP_FLAG_CLEAR),

    # Advanced timeline tools
    "delete_timeline_clips_v2": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_CLIPS_DELETE_V2),
    "link_timeline_clips_v2": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_CLIPS_LINK_V2),
    "create_compound_clip_v2": (BridgeMethod.POST, BridgeEndpoints.COMPOUND_CLIP_CREATE),
    "create_fusion_clip_v2": (BridgeMethod.POST, BridgeEndpoints.FUSION_CLIP_CREATE),

    # Clip inspection tools
    "get_current_video_item": (BridgeMethod.GET, BridgeEndpoints.CURRENT_VIDEO_ITEM),
    "get_clip_thumbnail": (BridgeMethod.GET, BridgeEndpoints.CLIP_THUMBNAIL),
    "export_timeline_v2": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_EXPORT_V2),

    # Gallery tools
    "get_gallery_albums": (BridgeMethod.GET, BridgeEndpoints.GALLERY_ALBUMS_GET),
    "get_album_stills": (BridgeMethod.GET, BridgeEndpoints.ALBUM_STILLS_GET),
    "set_current_album": (BridgeMethod.POST, BridgeEndpoints.ALBUM_CURRENT_SET),
    "create_gallery_album": (BridgeMethod.POST, BridgeEndpoints.GALLERY_ALBUM_CREATE),
    "grab_still": (BridgeMethod.POST, BridgeEndpoints.GRAB_STILL),
    "grab_all_stills": (BridgeMethod.POST, BridgeEndpoints.GRAB_ALL_STILLS),
    "export_stills": (BridgeMethod.POST, BridgeEndpoints.EXPORT_STILLS),
    "import_stills": (BridgeMethod.POST, BridgeEndpoints.IMPORT_STILLS),
    "delete_stills": (BridgeMethod.POST, BridgeEndpoints.STILLS_DELETE),
    "set_still_label": (BridgeMethod.POST, BridgeEndpoints.STILL_LABEL_SET),

    # Color tools
    "get_node_graph": (BridgeMethod.GET, BridgeEndpoints.NODE_GRAPH_GET),
    "set_lut": (BridgeMethod.POST, BridgeEndpoints.LUT_SET),
    "get_lut": (BridgeMethod.GET, BridgeEndpoints.LUT_GET),
    "set_node_enabled": (BridgeMethod.POST, BridgeEndpoints.NODE_ENABLE_SET),
    "apply_grade_from_drx": (BridgeMethod.POST, BridgeEndpoints.GRADE_FROM_DRX),
    "reset_all_grades": (BridgeMethod.POST, BridgeEndpoints.RESET_ALL_GRADES),
    "apply_arri_cdl_lut": (BridgeMethod.POST, BridgeEndpoints.ARRI_CDL_LUT),
    "set_cdl": (BridgeMethod.POST, BridgeEndpoints.CDL_SET),
    "export_lut": (BridgeMethod.POST, BridgeEndpoints.LUT_EXPORT),
    "copy_grades": (BridgeMethod.POST, BridgeEndpoints.GRADES_COPY),
    "reset_node_colors": (BridgeMethod.POST, BridgeEndpoints.NODE_COLORS_RESET),
    "get_color_versions": (BridgeMethod.GET, BridgeEndpoints.COLOR_VERSIONS_GET),
    "add_color_version": (BridgeMethod.POST, BridgeEndpoints.COLOR_VERSION_ADD),
    "load_color_version": (BridgeMethod.POST, BridgeEndpoints.COLOR_VERSION_LOAD),
    "delete_color_version": (BridgeMethod.POST, BridgeEndpoints.COLOR_VERSION_DELETE),
    "rename_color_version": (BridgeMethod.POST, BridgeEndpoints.COLOR_VERSION_RENAME),
    "get_color_groups": (BridgeMethod.GET, BridgeEndpoints.COLOR_GROUPS_GET),
    "add_color_group": (BridgeMethod.POST, BridgeEndpoints.COLOR_GROUP_ADD),
    "delete_color_group": (BridgeMethod.POST, BridgeEndpoints.COLOR_GROUP_DELETE),
    "assign_to_color_group": (BridgeMethod.POST, BridgeEndpoints.COLOR_GROUP_ASSIGN),
    "remove_from_color_group": (BridgeMethod.POST, BridgeEndpoints.COLOR_GROUP_REMOVE),

    # Fusion tools
    "get_fusion_comps": (BridgeMethod.GET, BridgeEndpoints.FUSION_COMPS_GET),
    "add_fusion_comp_to_clip": (BridgeMethod.POST, BridgeEndpoints.FUSION_COMP_ADD),
    "import_fusion_comp_to_clip": (BridgeMethod.POST, BridgeEndpoints.FUSION_COMP_IMPORT),
    "export_fusion_comp_from_clip": (BridgeMethod.POST, BridgeEndpoints.FUSION_COMP_EXPORT),
    "delete_fusion_comp_on_clip": (BridgeMethod.POST, BridgeEndpoints.FUSION_COMP_DELETE),
    "load_fusion_comp_on_clip": (BridgeMethod.POST, BridgeEndpoints.FUSION_COMP_LOAD),
    "rename_fusion_comp_on_clip": (BridgeMethod.POST, BridgeEndpoints.FUSION_COMP_RENAME),
    "create_magic_mask": (BridgeMethod.POST, BridgeEndpoints.MAGIC_MASK_CREATE),
    "regenerate_magic_mask": (BridgeMethod.POST, BridgeEndpoints.MAGIC_MASK_REGENERATE),

    # Stabilization/Reframe
    "stabilize_clip": (BridgeMethod.POST, BridgeEndpoints.STABILIZE_CLIP),
    "smart_reframe_clip": (BridgeMethod.POST, BridgeEndpoints.SMART_REFRAME),

    # Audio tools
    "get_fairlight_presets": (BridgeMethod.GET, BridgeEndpoints.FAIRLIGHT_PRESETS_GET),
    "apply_fairlight_preset": (BridgeMethod.POST, BridgeEndpoints.FAIRLIGHT_PRESET_APPLY),
    "insert_audio_at_playhead": (BridgeMethod.POST, BridgeEndpoints.AUDIO_INSERT),
    "get_voice_isolation_state": (BridgeMethod.GET, BridgeEndpoints.VOICE_ISOLATION_GET),
    "set_voice_isolation_state": (BridgeMethod.POST, BridgeEndpoints.VOICE_ISOLATION_SET),

    # Takes tools
    "get_takes": (BridgeMethod.GET, BridgeEndpoints.TAKES_GET),
    "add_take": (BridgeMethod.POST, BridgeEndpoints.TAKE_ADD),
    "select_take": (BridgeMethod.POST, BridgeEndpoints.TAKE_SELECT),
    "delete_take": (BridgeMethod.POST, BridgeEndpoints.TAKE_DELETE),
    "finalize_take": (BridgeMethod.POST, BridgeEndpoints.TAKE_FINALIZE),

    # Proxy/Linked items
    "link_proxy_media": (BridgeMethod.POST, BridgeEndpoints.PROXY_LINK),
    "unlink_proxy_media": (BridgeMethod.POST, BridgeEndpoints.PROXY_UNLINK),
    "replace_clip": (BridgeMethod.POST, BridgeEndpoints.CLIP_REPLACE),
    "set_clip_cache": (BridgeMethod.POST, BridgeEndpoints.CLIP_CACHE),
    "update_sidecar": (BridgeMethod.POST, BridgeEndpoints.SIDECAR_UPDATE),
    "get_linked_items": (BridgeMethod.GET, BridgeEndpoints.LINKED_ITEMS_GET),

    # Project management
    "get_project_list": (BridgeMethod.GET, BridgeEndpoints.PROJECT_LIST),
    "get_database_list": (BridgeMethod.GET, BridgeEndpoints.DATABASE_LIST),
    "load_project": (BridgeMethod.POST, BridgeEndpoints.PROJECT_LOAD),
    "create_project": (BridgeMethod.POST, BridgeEndpoints.PROJECT_CREATE),
    "delete_project": (BridgeMethod.POST, BridgeEndpoints.PROJECT_DELETE),
    "archive_project": (BridgeMethod.POST, BridgeEndpoints.PROJECT_ARCHIVE),
    "export_project": (BridgeMethod.POST, BridgeEndpoints.PROJECT_EXPORT),
    "import_project": (BridgeMethod.POST, BridgeEndpoints.PROJECT_IMPORT),
    "navigate_project_folder": (BridgeMethod.POST, BridgeEndpoints.PROJECT_FOLDER_NAVIGATE),
    "set_database": (BridgeMethod.POST, BridgeEndpoints.DATABASE_SET),

    # Presets
    "layout_preset": (BridgeMethod.POST, BridgeEndpoints.LAYOUT_PRESET),
    "render_preset": (BridgeMethod.POST, BridgeEndpoints.RENDER_PRESET),
    "burnin_preset": (BridgeMethod.POST, BridgeEndpoints.BURNIN_PRESET),

    # Keyframe
    "get_keyframe_mode": (BridgeMethod.GET, BridgeEndpoints.KEYFRAME_MODE_GET),
    "set_keyframe_mode": (BridgeMethod.POST, BridgeEndpoints.KEYFRAME_MODE_SET),

    # LUT
    "refresh_lut_list": (BridgeMethod.POST, BridgeEndpoints.LUT_LIST_REFRESH),

    # Media storage
    "get_media_storage": (BridgeMethod.GET, BridgeEndpoints.MEDIA_STORAGE_GET),
    "reveal_in_storage": (BridgeMethod.POST, BridgeEndpoints.REVEAL_IN_STORAGE),

    # AI/ML tools
    "voice_isolate": (BridgeMethod.POST, BridgeEndpoints.VOICE_ISOLATE),
    "voice_isolate_timeline": (BridgeMethod.POST, BridgeEndpoints.VOICE_ISOLATE_TIMELINE),
    "remove_background": (BridgeMethod.POST, BridgeEndpoints.REMOVE_BACKGROUND),
    "remove_background_video": (BridgeMethod.POST, BridgeEndpoints.REMOVE_BACKGROUND_VIDEO),
    "remove_background_clip": (BridgeMethod.POST, BridgeEndpoints.REMOVE_BACKGROUND_CLIP),
    "transcribe_timeline": (BridgeMethod.POST, BridgeEndpoints.TIMELINE_TRANSCRIBE),
    "transcribe_file": (BridgeMethod.POST, BridgeEndpoints.FILE_TRANSCRIBE),

    # Bridge control
    "bridge_shutdown": (BridgeMethod.POST, BridgeEndpoints.BRIDGE_SHUTDOWN),
}


def get_endpoint_for_tool(tool_name: str) -> tuple[BridgeMethod, str]:
    """Get the HTTP method and endpoint for a tool."""
    if tool_name not in TOOL_TO_ENDPOINT:
        raise ValueError(f"Unknown tool: {tool_name}")
    return TOOL_TO_ENDPOINT[tool_name]


def is_write_tool(tool_name: str) -> bool:
    """Check if a tool is a write operation (POST)."""
    method, _ = get_endpoint_for_tool(tool_name)
    return method == BridgeMethod.POST