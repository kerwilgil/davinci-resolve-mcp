"""Network and installed-package regression tests; no Resolve projects are accessed."""
import asyncio
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import sys
import sysconfig
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.client import HTTPConnection
from http.server import HTTPServer
from unittest.mock import MagicMock, Mock, patch
from urllib.error import HTTPError, URLError

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.davinci_mcp.bridge import BridgeClient, BridgeMethod, BridgeRequest, HTTPTransport, ToolCall
from src.davinci_mcp.bridge.protocol import TOOL_TO_ENDPOINT, UNAVAILABLE_TOOLS
from src.davinci_mcp.config import BridgeConfig
from src.davinci_mcp.errors import BridgeOutcomeUnknownError, BridgeTimeoutError
from src.davinci_mcp.schemas import ALL_SCHEMAS
from src.davinci_mcp.tools import ToolRegistry

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "test-only-credential-" + "x" * 32


def load_bridge():
    spec = importlib.util.spec_from_file_location("controlled_bridge", ROOT / "src/CursorBridge.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


class BridgeHTTPTests(unittest.TestCase):
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

    def request(self, method="GET", path="/status", body=None, headers=None):
        conn = HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        conn.request(method, path, body, headers or {})
        response = conn.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        conn.close()
        return result

    def test_every_route_rejects_missing_and_wrong_auth_before_dispatch(self):
        for method, routes in [("GET", self.bridge.GET_ROUTES), ("POST", self.bridge.POST_ROUTES)]:
            for path in routes:
                for headers in ({}, {"Authorization": "Bearer incorrect"}):
                    with self.subTest(method=method, path=path, headers=headers):
                        self.assertEqual(self.request(method, path, headers=headers)[0], 401)

    def test_authorized_read_has_no_cors(self):
        status, headers, data = self.request(headers={"Authorization": "Bearer " + TOKEN})
        self.assertEqual(status, 200)
        self.assertFalse(json.loads(data)["connected"])
        self.assertNotIn("Access-Control-Allow-Origin", headers)

    def test_origin_and_rebinding_are_rejected_with_valid_token(self):
        for extra in ({"Origin": "https://untrusted.example"}, {"Origin": "null"}, {"Host": "untrusted.example"}):
            self.assertEqual(self.request(headers={"Authorization": "Bearer " + TOKEN, **extra})[0], 403)
        self.assertEqual(self.request("OPTIONS")[0], 403)

    def test_json_bounds_types_and_content_type(self):
        headers = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}
        for body in ("[]", "null", "broken", '"string"'):
            self.assertEqual(self.request("POST", "/project/save", body, headers)[0], 400)
        self.assertEqual(self.request("POST", "/project/save", "{}", {**headers, "Content-Length": "-1"})[0], 413)
        self.assertEqual(self.request("POST", "/project/save", "{}", {**headers, "Content-Length": "1048577"})[0], 413)
        self.assertEqual(self.request("POST", "/project/save", "{}", {**headers, "Content-Type": "text/plain"})[0], 415)

    def test_errors_do_not_disclose_trace_or_paths(self):
        with patch.dict(self.bridge.GET_ROUTES, {"/test-error": Mock(side_effect=RuntimeError("/private/sensitive"))}):
            status, _, data = self.request(path="/test-error", headers={"Authorization": "Bearer " + TOKEN})
        self.assertEqual(status, 500)
        self.assertNotIn(b"sensitive", data)
        self.assertNotIn(b"Traceback", data)

    def test_authorized_read_and_write_use_real_client(self):
        resolve = Mock()
        resolve.GetProductName.return_value = "Controlled Resolve"
        resolve.GetVersionString.return_value = "test"
        resolve.OpenPage.return_value = True
        with patch.object(self.bridge, "resolve_obj", resolve):
            client = BridgeClient(BridgeConfig(port=self.server.server_port, token=TOKEN, max_retries=0))
            read = client.call_tool(ToolCall("get_resolve_status", {}))
            write = client.call_tool(ToolCall("open_page", {"page": "edit"}))
            self.assertTrue(read.success)
            self.assertEqual(read.data["product"], "Controlled Resolve")
            self.assertTrue(write.success)
            resolve.OpenPage.assert_called_once_with("edit")

    def test_unknown_mutation_selector_cannot_fall_back_to_default_target(self):
        resolve = Mock()
        with patch.object(self.bridge, "resolve_obj", resolve):
            status, _, _ = self.request("POST", "/projects/delete", json.dumps({"projectName": "disposable", "databaseName": "other"}),
                {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
        self.assertEqual(status, 422)
        resolve.GetProjectManager.assert_not_called()

    def test_start_without_token_fails_closed(self):
        with patch.dict(os.environ, {"DAVINCI_BRIDGE_TOKEN": ""}):
            with self.assertRaises(RuntimeError):
                self.bridge.serve()

    def test_routes_cover_all_implemented_tools(self):
        for name in ALL_SCHEMAS.keys() - UNAVAILABLE_TOOLS:
            method, route = TOOL_TO_ENDPOINT[name]
            routes = self.bridge.GET_ROUTES if method == BridgeMethod.GET else self.bridge.POST_ROUTES
            self.assertIn(route, routes, name)

    def test_named_clip_resolution_rejects_missing_and_ambiguous_targets(self):
        timeline = Mock()
        clip = Mock()
        clip.GetName.return_value = "target"
        timeline.GetTrackCount.side_effect = lambda kind: 1 if kind == "video" else 0
        timeline.GetItemListInTrack.return_value = [clip]
        self.assertEqual(self.bridge._named_clip_reference(timeline, "target")["clipIndex"], 0)
        for items in ([], [clip, clip]):
            timeline.GetItemListInTrack.return_value = items
            with self.assertRaises(ValueError):
                self.bridge._named_clip_reference(timeline, "target")

    def test_mismatched_project_context_rejects_before_mutation(self):
        project = Mock()
        project.GetName.return_value = "current"
        resolve = Mock()
        resolve.GetProjectManager.return_value.GetCurrentProject.return_value = project
        with patch.object(self.bridge, "resolve_obj", resolve):
            status, _, _ = self.request("POST", "/project/save", json.dumps({"projectName": "other"}),
                {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
        self.assertEqual(status, 400)
        resolve.GetProjectManager.return_value.SaveProject.assert_not_called()

    def test_insert_preserves_target_track_and_record_frame(self):
        project, pool, clip = Mock(), Mock(), Mock()
        project.GetMediaPool.return_value = pool
        clip.GetName.return_value = "source.mov"
        pool.GetRootFolder.return_value.GetClipList.return_value = [clip]
        pool.AppendToTimeline.return_value = [Mock()]
        resolve = Mock()
        resolve.GetProjectManager.return_value.GetCurrentProject.return_value = project
        with patch.object(self.bridge, "resolve_obj", resolve):
            result = BridgeClient(BridgeConfig(port=self.server.server_port, token=TOKEN, max_retries=0)).call_tool(
                ToolCall("insert_to_timeline", {"clip_name": "source.mov", "track_type": "audio", "track_index": 2, "frame": 120}))
        self.assertTrue(result.success)
        pool.AppendToTimeline.assert_called_once_with([{"mediaPoolItem": clip, "trackIndex": 2, "recordFrame": 120, "mediaType": 2}])

    def test_create_timeline_applies_explicit_settings(self):
        project, pool, timeline, resolve = Mock(), Mock(), Mock(), Mock()
        project.GetMediaPool.return_value = pool
        pool.CreateEmptyTimeline.return_value = timeline
        timeline.GetTrackCount.return_value = 1
        resolve.GetProjectManager.return_value.GetCurrentProject.return_value = project
        with patch.object(self.bridge, "resolve_obj", resolve):
            result = self.bridge.action_create_timeline({"name": "disposable-mock", "frameRate": 25,
                "startTimecode": "01:00:00:00", "videoTracks": 2})
        self.assertTrue(result["success"])
        timeline.SetSetting.assert_any_call("timelineFrameRate", "25")
        timeline.SetStartTimecode.assert_called_once_with("01:00:00:00")
        timeline.AddTrack.assert_called_once_with("video")


class RetryTests(unittest.TestCase):
    def setUp(self):
        self.transport = HTTPTransport(BridgeConfig(max_retries=2, retry_delay=0, token=TOKEN))

    def test_post_communication_failures_are_unknown_and_never_repeated(self):
        for failure in (TimeoutError(), URLError(socket.timeout()), URLError("refused"), ConnectionResetError()):
            with self.subTest(failure=type(failure)), patch.object(self.transport._opener, "open", side_effect=failure) as opened:
                with self.assertRaises(BridgeOutcomeUnknownError) as caught:
                    self.transport.send(BridgeRequest(BridgeMethod.POST, "/project/create", {}, {"projectName": "temporary"}))
                self.assertEqual(opened.call_count, 1)
                self.assertEqual(caught.exception.to_dict()["error"]["details"]["outcome"], "unknown")

    def test_http_errors_do_not_repeat_posts(self):
        for code in (400, 401, 403, 404, 500, 503):
            with self.subTest(code=code), patch.object(self.transport._opener, "open", side_effect=HTTPError("local", code, "failure", {}, io.BytesIO(b'{}'))) as opened:
                response = self.transport.send(BridgeRequest(BridgeMethod.POST, "/project/create", {}, {}))
                self.assertEqual(response.status_code, code)
                self.assertEqual(opened.call_count, 1)

    def test_wrapped_get_timeout_retries_safely(self):
        with patch.object(self.transport._opener, "open", side_effect=URLError(socket.timeout())) as opened:
            with self.assertRaises(BridgeTimeoutError):
                self.transport.send(BridgeRequest(BridgeMethod.GET, "/status", {}))
            self.assertEqual(opened.call_count, 3)

    def test_query_encoding_and_auth_header(self):
        response = MagicMock(status=200)
        response.read.return_value = b'{}'
        response.__enter__.return_value = response
        with patch.object(self.transport._opener, "open", return_value=response) as opened:
            self.transport.send(BridgeRequest(BridgeMethod.GET, "/mediapool/clip/info", {"clip_name": "a & b+#.mov"}))
        req = opened.call_args.args[0]
        self.assertIn("a+%26+b%2B%23.mov", req.full_url)
        self.assertEqual(req.get_header("Authorization"), "Bearer " + TOKEN)

    def test_non_loopback_config_is_rejected(self):
        with self.assertRaises(ValueError):
            BridgeConfig(host="example.com")
        self.assertNotIn(TOKEN, repr(BridgeConfig(token=TOKEN)))


class RegistryRegressionTests(unittest.IsolatedAsyncioTestCase):
    async def test_validation_is_strict_and_no_internal_registry_is_accepted(self):
        client = Mock()
        registry = ToolRegistry(client)
        for args in ({"track_index": True}, {"track_index": 0}, {"track_index": 1, "unexpected": 1}, {"_registry": {}}, {"track_index": 1, "track_type": "invalid"}):
            result = await registry.execute("get_timeline_clips", args)
            self.assertFalse(result.success)
        client.call_tool_simple.assert_not_called()

    async def test_registry_injects_context_after_validation(self):
        client = Mock()
        client.call_tool_simple.return_value = Mock(success=True, data={"saved": True})
        result = await ToolRegistry(client).execute("save_project", {})
        self.assertTrue(result.success)
        client.call_tool_simple.assert_called_once_with("save_project")

    async def test_read_only_rejects_mutation_before_network(self):
        client = Mock()
        result = await ToolRegistry(client, read_only=True).execute("save_project", {})
        self.assertFalse(result.success)
        client.call_tool_simple.assert_not_called()

    async def test_unavailable_tools_fail_without_connection(self):
        client = BridgeClient()
        with patch.object(client, "connect") as connected:
            for name in UNAVAILABLE_TOOLS:
                result = client.call_tool(ToolCall(name, {}))
                self.assertFalse(result.success)
                self.assertEqual(result.error.code, "TOOL_UNAVAILABLE")
            connected.assert_not_called()


class InstalledStdioTests(unittest.IsolatedAsyncioTestCase):
    async def test_installed_stdio_reads_and_mutates_controlled_bridge(self):
        bridge = load_bridge()
        resolve = Mock()
        resolve.GetProductName.return_value = "Controlled Resolve"
        resolve.GetVersionString.return_value = "test"
        resolve.OpenPage.return_value = True
        bridge.resolve_obj = resolve
        server = HTTPServer(("127.0.0.1", 0), bridge.BridgeHandler)
        server.bridge_token = TOKEN
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                params = StdioServerParameters(command=sys.executable, args=["-m", "davinci_mcp.server"], cwd=directory,
                    env={"DAVINCI_BRIDGE_TOKEN": TOKEN, "DAVINCI_BRIDGE_PORT": str(server.server_port), "DAVINCI_BRIDGE_MAX_RETRIES": "0"})
                async with asyncio.timeout(20):
                    async with stdio_client(params) as (read, write):
                        async with ClientSession(read, write) as session:
                            await session.initialize()
                            status = await session.call_tool("get_resolve_status", {})
                            self.assertFalse(status.isError)
                            self.assertEqual(json.loads(status.content[0].text)["product"], "Controlled Resolve")
                            result = await session.call_tool("open_page", {"page": "edit"})
                            self.assertFalse(result.isError)
                            resolve.OpenPage.assert_called_once_with("edit")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    async def test_installed_module_and_entrypoint_publish_real_schemas(self):
        # No source path is passed to the subprocess: this must use an installed wheel.
        for command, args in ((sys.executable, ["-m", "davinci_mcp.server"]),
                              (str(Path(sysconfig.get_path("scripts")) / ("davinci-resolve-mcp.exe" if os.name == "nt" else "davinci-resolve-mcp")), [])):
            with tempfile.TemporaryDirectory() as directory:
                params = StdioServerParameters(command=command, args=args, cwd=directory, env={"DAVINCI_BRIDGE_MAX_RETRIES": "0", "DAVINCI_BRIDGE_TIMEOUT": "0.1"})
                async with asyncio.timeout(20):
                    async with stdio_client(params) as (read, write):
                        async with ClientSession(read, write) as session:
                            await session.initialize()
                            tools = (await session.list_tools()).tools
                            self.assertEqual({tool.name for tool in tools}, set(ALL_SCHEMAS))
                            for tool in tools:
                                schema = ALL_SCHEMAS[tool.name]
                                self.assertEqual(tool.inputSchema, {**schema.parameters, "required": schema.required})
                            bad = await session.call_tool("create_timeline", {"name": "test"})
                            self.assertTrue(bad.isError)
                            disconnected = await session.call_tool("get_resolve_status", {})
                            self.assertTrue(disconnected.isError)
