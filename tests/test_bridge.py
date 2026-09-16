"""Tests for bridge communication layer."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from urllib.error import HTTPError, URLError

from src.davinci_mcp.bridge import (
    HTTPTransport,
    BridgeClient,
    BridgeMethod,
    BridgeRequest,
    BridgeResponse,
    ToolCall,
    ToolResult,
)
from src.davinci_mcp.config import BridgeConfig
from src.davinci_mcp.errors import (
    BridgeConnectionError,
    BridgeTimeoutError,
    BridgeResponseError,
)
from src.davinci_mcp.bridge.protocol import is_write_tool


class TestBridgeProtocol(unittest.TestCase):
    """Test bridge protocol definitions."""

    def test_bridge_method_enum(self):
        """BridgeMethod enum should have GET and POST."""
        self.assertEqual(BridgeMethod.GET.value, "GET")
        self.assertEqual(BridgeMethod.POST.value, "POST")

    def test_is_write_tool_classification(self):
        """Write tool classification should work."""
        # Test known write tools
        self.assertTrue(is_write_tool("create_timeline"))
        self.assertTrue(is_write_tool("insert_to_timeline"))
        self.assertTrue(is_write_tool("add_marker"))
        self.assertTrue(is_write_tool("set_playhead"))

        # Test known read tools
        self.assertFalse(is_write_tool("get_resolve_status"))
        self.assertFalse(is_write_tool("get_project_info"))
        self.assertFalse(is_write_tool("get_timeline_info"))

    def test_bridge_request_creation(self):
        """BridgeRequest should be creatable."""
        req = BridgeRequest(
            method=BridgeMethod.GET,
            path="/status",
            params={"foo": "bar"},
        )
        self.assertEqual(req.method, BridgeMethod.GET)
        self.assertEqual(req.path, "/status")
        self.assertEqual(req.params, {"foo": "bar"})

    def test_bridge_response_success(self):
        """BridgeResponse is_success property."""
        resp = BridgeResponse(status_code=200, data={"ok": True})
        self.assertTrue(resp.is_success)
        self.assertFalse(resp.is_client_error)
        self.assertFalse(resp.is_server_error)

    def test_bridge_response_client_error(self):
        """BridgeResponse client error property."""
        resp = BridgeResponse(status_code=404, data={"error": "not found"})
        self.assertFalse(resp.is_success)
        self.assertTrue(resp.is_client_error)
        self.assertFalse(resp.is_server_error)

    def test_bridge_response_server_error(self):
        """BridgeResponse server error property."""
        resp = BridgeResponse(status_code=500, data={"error": "server error"})
        self.assertFalse(resp.is_success)
        self.assertFalse(resp.is_client_error)
        self.assertTrue(resp.is_server_error)


class TestHTTPTransport(unittest.TestCase):
    """Test HTTP transport layer."""

    def setUp(self):
        self.config = BridgeConfig(host="127.0.0.1", port=9876, timeout=5.0)
        self.transport = HTTPTransport(self.config)

    @patch("urllib.request.OpenerDirector.open")
    def test_send_success(self, mock_open):
        """Test successful request."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"result": "ok"}'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_open.return_value = mock_response

        req = BridgeRequest(method=BridgeMethod.GET, path="/status", params={})
        resp = self.transport.send(req)

        self.assertTrue(resp.is_success)
        self.assertEqual(resp.data, {"result": "ok"})
        self.assertEqual(self.transport.stats.requests_made, 1)
        self.assertEqual(self.transport.stats.requests_failed, 0)

    @patch("urllib.request.OpenerDirector.open")
    def test_send_http_error_4xx(self, mock_open):
        """Test 4xx error handling (no retry)."""
        mock_response = MagicMock()
        mock_response.status = 404
        mock_response.read.return_value = b'{"message": "not found"}'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_open.side_effect = HTTPError("url", 404, "Not Found", {}, mock_response)

        req = BridgeRequest(method=BridgeMethod.GET, path="/missing", params={})
        resp = self.transport.send(req)

        self.assertFalse(resp.is_success)
        self.assertEqual(resp.status_code, 404)
        # Should not retry on 4xx
        self.assertEqual(mock_open.call_count, 1)

    @patch("urllib.request.OpenerDirector.open")
    def test_send_http_error_5xx_retry(self, mock_open):
        """Test 5xx error with retry and eventual exception."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.read.return_value = b'{"message": "server error"}'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_open.side_effect = HTTPError("url", 500, "Server Error", {}, mock_response)

        req = BridgeRequest(method=BridgeMethod.GET, path="/error", params={})

        with self.assertRaises(BridgeResponseError):
            self.transport.send(req)

        # Should retry max_retries times (3) + 1 initial = 4
        self.assertEqual(mock_open.call_count, 4)

    @patch("urllib.request.OpenerDirector.open")
    def test_send_connection_error(self, mock_open):
        """Test connection error."""
        mock_open.side_effect = URLError("Connection refused")

        req = BridgeRequest(method=BridgeMethod.GET, path="/status", params={})

        with self.assertRaises(BridgeConnectionError):
            self.transport.send(req)

    @patch("urllib.request.OpenerDirector.open")
    def test_send_timeout(self, mock_open):
        """Test timeout error."""
        import socket
        mock_open.side_effect = socket.timeout("timed out")

        req = BridgeRequest(method=BridgeMethod.GET, path="/status", params={})

        with self.assertRaises(BridgeTimeoutError):
            self.transport.send(req)


class TestBridgeClient(unittest.TestCase):
    """Test high-level bridge client."""

    def setUp(self):
        self.config = BridgeConfig()
        self.transport = Mock(spec=HTTPTransport)
        self.client = BridgeClient(self.config, self.transport)

    def test_tool_call_creation(self):
        """Test ToolCall creation."""
        call = ToolCall(name="get_resolve_status", arguments={})
        self.assertEqual(call.name, "get_resolve_status")
        self.assertEqual(call.arguments, {})

    def test_tool_result_success(self):
        """Test ToolResult success."""
        result = ToolResult.success_result({"status": "ok"}, "req-123")
        self.assertTrue(result.success)
        self.assertEqual(result.data, {"status": "ok"})
        self.assertEqual(result.request_id, "req-123")

    def test_tool_result_error(self):
        """Test ToolResult error."""
        error = BridgeConnectionError("test")
        result = ToolResult.error_result(error, "req-123")
        self.assertFalse(result.success)
        self.assertEqual(result.error, error)
        self.assertEqual(result.request_id, "req-123")

    def test_call_tool_unknown(self):
        """Test calling unknown tool."""
        self.transport.health_check.return_value = True
        self.client._connected = True

        call = ToolCall(name="unknown_tool", arguments={})
        result = self.client.call_tool(call)

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)

    def test_call_tool_not_connected(self):
        """Test calling tool when not connected."""
        self.client._connected = False
        self.transport.health_check.return_value = False

        call = ToolCall(name="get_resolve_status", arguments={})
        result = self.client.call_tool(call)

        self.assertFalse(result.success)
        self.assertIsInstance(result.error, BridgeConnectionError)


class TestReadWriteClassification(unittest.TestCase):
    """Test read/write tool classification."""

    def test_core_tools_classification(self):
        """Test core tools have correct classification."""
        # Read tools
        read_tools = [
            "get_resolve_status",
            "get_project_info",
            "get_timeline_info",
            "get_timeline_clips",
            "get_render_settings",
            "get_media_pool",
        ]
        for tool in read_tools:
            self.assertFalse(is_write_tool(tool), f"{tool} should be read")

        # Write tools
        write_tools = [
            "create_timeline",
            "insert_to_timeline",
            "add_marker",
            "set_playhead",
            "import_media",
            "delete_media_pool_clips",
        ]
        for tool in write_tools:
            self.assertTrue(is_write_tool(tool), f"{tool} should be write")

    def test_all_tools_classified(self):
        """All tools should have a classification."""
        from src.davinci_mcp.schemas import ALL_SCHEMAS
        for name in ALL_SCHEMAS:
            try:
                is_write = is_write_tool(name)
                self.assertIsInstance(is_write, bool)
            except ValueError:
                self.fail(f"Tool {name} not in TOOL_TO_ENDPOINT mapping")


if __name__ == "__main__":
    unittest.main()