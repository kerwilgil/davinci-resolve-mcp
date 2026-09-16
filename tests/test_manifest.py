"""Validates manifests/tool-manifest.json against the new schema registry.

This validates that `verified_tools` in the manifest matches tools that have
schemas defined in the new architecture. A tool can only be marked verified
once it has been exercised against a real DaVinci Resolve project; having a
schema is a necessary but not sufficient condition.
"""

import json
import unittest
from pathlib import Path

from src.davinci_mcp.schemas import ALL_SCHEMAS, VERIFIED_TOOLS


MANIFEST = Path(__file__).resolve().parents[1] / "manifests" / "tool-manifest.json"


def registered_tools() -> set:
    """Get tools that have schemas defined."""
    return set(ALL_SCHEMAS.keys())


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
        self.assertFalse(missing, f"verified_tools references tools not found in schemas: {missing}")

    def test_core_status_tool_is_verified(self):
        self.assertIn("get_resolve_status", self.manifest["verified_tools"])

    def test_timeline_construction_tools_are_verified(self):
        # Regression guard for the bug that triggered this extraction: a skill
        # documented create_timeline/insert_to_timeline before they were
        # registered as verified, breaking manifest/doc consistency checks.
        for tool in ("create_timeline", "insert_to_timeline"):
            self.assertIn(tool, self.registered, f"{tool} missing from schemas")
            self.assertIn(tool, self.manifest["verified_tools"], f"{tool} missing from verified_tools")

    def test_manifest_has_verified_tools_array(self):
        self.assertIn("verified_tools", self.manifest)
        self.assertIsInstance(self.manifest["verified_tools"], list)
        self.assertGreater(len(self.manifest["verified_tools"]), 0)

    def test_manifest_has_tool_categories(self):
        self.assertIn("tool_categories", self.manifest)

    def test_verified_tools_match_verified_list(self):
        """Manifest verified_tools should match the VERIFIED_TOOLS list."""
        manifest_verified = set(self.manifest["verified_tools"])
        schema_verified = set(VERIFIED_TOOLS)
        self.assertEqual(manifest_verified, schema_verified,
                         f"Mismatch: manifest={manifest_verified - schema_verified}, schemas={schema_verified - manifest_verified}")


if __name__ == "__main__":
    unittest.main()