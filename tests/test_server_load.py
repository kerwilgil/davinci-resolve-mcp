"""Smoke tests for the new architecture."""

import unittest
from src.davinci_mcp.schemas import VERIFIED_TOOLS, get_write_tools, get_read_tools
from src.davinci_mcp.bridge.protocol import is_write_tool


class ArchitectureTests(unittest.TestCase):
    """Test the new architecture components."""

    def test_verified_tools_exist_in_schemas(self):
        from src.davinci_mcp.schemas import get_schema
        for tool in VERIFIED_TOOLS:
            schema = get_schema(tool)
            self.assertIsNotNone(schema, f"Verified tool {tool} missing from schemas")

    def test_get_resolve_status_is_read_tool(self):
        self.assertFalse(is_write_tool("get_resolve_status"))

    def test_create_timeline_is_write_tool(self):
        self.assertTrue(is_write_tool("create_timeline"))

    def test_insert_to_timeline_is_write_tool(self):
        self.assertTrue(is_write_tool("insert_to_timeline"))

    def test_key_tools_are_in_schemas(self):
        from src.davinci_mcp.schemas import get_schema
        for name in ("get_resolve_status", "create_timeline", "insert_to_timeline"):
            schema = get_schema(name)
            self.assertIsNotNone(schema, f"missing {name}")

    def test_read_write_classification_consistent(self):
        """Verify read/write classification matches schema mode."""
        from src.davinci_mcp.schemas import get_schema, ToolMode
        for tool in VERIFIED_TOOLS:
            schema = get_schema(tool)
            if schema:
                is_write_schema = schema.mode == ToolMode.WRITE
                is_write_protocol = is_write_tool(tool)
                self.assertEqual(is_write_schema, is_write_protocol,
                                 f"Tool {tool}: schema={is_write_schema}, protocol={is_write_protocol}")

    def test_bridge_host_is_localhost(self):
        """Verify bridge binds to localhost only."""
        import os
        bridge_path = os.path.join(os.path.dirname(__file__), "..", "src", "CursorBridge.py")
        if os.path.exists(bridge_path):
            # File may have UTF-16 BOM
            with open(bridge_path, "rb") as f:
                raw = f.read()
            if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
                bridge_text = raw.decode("utf-16")
            else:
                bridge_text = raw.decode("utf-8")
            self.assertIn('HOST = "127.0.0.1"', bridge_text)


if __name__ == "__main__":
    unittest.main()