"""Validates manifests/tool-manifest.json against the vendored MCP server source.

`verified_tools` must always be a subset of the tools that are actually
registered with `@mcp.tool()` in src/resolve_mcp_bridge.py. A tool can only be
marked verified once it has been exercised against a real DaVinci Resolve
project; being present in the source is a necessary but not sufficient
condition.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "src" / "resolve_mcp_bridge.py"
MANIFEST = ROOT / "manifests" / "tool-manifest.json"

TOOL_DEF = re.compile(r"@mcp\.tool\(\)\s*\n(?:async )?def (\w+)\(")


def registered_tools() -> set:
    text = SERVER.read_text(encoding="utf-8")
    return set(TOOL_DEF.findall(text))


class ToolManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.registered = registered_tools()

    def test_server_exposes_tools(self):
        self.assertGreater(len(self.registered), 0)

    def test_manifest_has_no_duplicates(self):
        verified = self.manifest["verified_tools"]
        self.assertEqual(len(verified), len(set(verified)))

    def test_verified_tools_are_all_implemented(self):
        verified = set(self.manifest["verified_tools"])
        missing = verified - self.registered
        self.assertFalse(missing, f"verified_tools references tools not found in {SERVER.name}: {missing}")

    def test_core_status_tool_is_verified(self):
        self.assertIn("get_resolve_status", self.manifest["verified_tools"])

    def test_timeline_construction_tools_are_verified(self):
        # Regression guard: these timeline tools are both implemented and
        # explicitly tracked as verified in the standalone manifest.
        for tool in ("create_timeline", "insert_to_timeline"):
            self.assertIn(tool, self.registered, f"{tool} missing from vendored source")
            self.assertIn(tool, self.manifest["verified_tools"], f"{tool} missing from verified_tools")

    def test_manifest_commit_field_present(self):
        self.assertTrue(self.manifest["vendored_commit"])
        self.assertEqual(len(self.manifest["vendored_commit"]), 40)


if __name__ == "__main__":
    unittest.main()
