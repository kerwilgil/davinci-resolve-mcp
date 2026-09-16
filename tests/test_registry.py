"""Tests for tool registry consistency and validation."""

import json
import unittest
from pathlib import Path

from src.davinci_mcp.schemas import (
    ALL_SCHEMAS,
    VERIFIED_TOOLS,
    get_write_tools,
    get_read_tools,
    ToolCategory,
)
from src.davinci_mcp.tools import ToolRegistry
from src.davinci_mcp.bridge import BridgeClient
from src.davinci_mcp.config import BridgeConfig


class TestRegistryConsistency(unittest.TestCase):
    """Test tool registry consistency."""

    def setUp(self):
        self.config = BridgeConfig()
        self.client = BridgeClient(self.config)
        self.registry = ToolRegistry(self.client)

    def test_all_tools_have_schemas(self):
        """Every registered tool must have a schema."""
        for tool_name in self.registry.list_tools():
            from src.davinci_mcp.schemas import get_schema
            schema = get_schema(tool_name)
            self.assertIsNotNone(schema, f"Tool '{tool_name}' missing schema")

    def test_no_duplicate_tools(self):
        """No duplicate tool names in registry."""
        tools = self.registry.list_tools()
        self.assertEqual(len(tools), len(set(tools)), "Duplicate tool names found")

    def test_all_schemas_registered(self):
        """All defined schemas should be registered (or explicitly excluded)."""
        registered = set(self.registry.list_tools())
        schema_names = set(ALL_SCHEMAS.keys())
        missing = schema_names - registered
        # Allow some tools to not be implemented yet
        self.assertLessEqual(len(missing), len(schema_names) * 0.1,
                             f"Too many schemas not registered: {missing}")

    def test_verified_tools_subset_of_registered(self):
        """Verified tools must be a subset of registered tools."""
        registered = set(self.registry.list_tools())
        verified = set(VERIFIED_TOOLS)
        missing = verified - registered
        self.assertFalse(missing, f"Verified tools not registered: {missing}")

    def test_verified_tools_have_schemas(self):
        """All verified tools must have schemas."""
        for tool in VERIFIED_TOOLS:
            from src.davinci_mcp.schemas import get_schema
            schema = get_schema(tool)
            self.assertIsNotNone(schema, f"Verified tool '{tool}' missing schema")

    def test_write_tools_classification(self):
        """Write tools classification should match schema mode."""
        write_tools = set(get_write_tools())
        registered = set(self.registry.list_tools())
        for tool in write_tools:
            if tool in registered:
                from src.davinci_mcp.schemas import get_schema
                schema = get_schema(tool)
                self.assertEqual(schema.mode.value, "write",
                                 f"Tool '{tool}' classified as write but schema says {schema.mode}")

    def test_read_tools_classification(self):
        """Read tools classification should match schema mode."""
        read_tools = set(get_read_tools())
        registered = set(self.registry.list_tools())
        for tool in read_tools:
            if tool in registered:
                from src.davinci_mcp.schemas import get_schema
                schema = get_schema(tool)
                self.assertEqual(schema.mode.value, "read",
                                 f"Tool '{tool}' classified as read but schema says {schema.mode}")

    def test_category_coverage(self):
        """All categories should have at least some tools."""
        for category in ToolCategory:
            tools = [t for t in self.registry.list_tools()
                     if t in [n for n, s in ALL_SCHEMAS.items() if s.category == category]]
            self.assertGreater(len(tools), 0, f"Category {category} has no tools")

    def test_tool_metadata_completeness(self):
        """Each tool should have complete metadata."""
        for tool_name in self.registry.list_tools():
            from src.davinci_mcp.schemas import get_schema
            schema = get_schema(tool_name)
            if schema:
                self.assertIsNotNone(schema.description)
                self.assertGreater(len(schema.description), 10)
                self.assertIsNotNone(schema.category)
                self.assertIsNotNone(schema.mode)


class TestManifestConsistency(unittest.TestCase):
    """Test manifest consistency with registry."""

    def setUp(self):
        self.manifest_path = Path(__file__).parent.parent / "manifests" / "tool-manifest.json"
        with open(self.manifest_path) as f:
            self.manifest = json.load(f)

    def test_manifest_has_verified_tools(self):
        """Manifest must have verified_tools array."""
        self.assertIn("verified_tools", self.manifest)
        self.assertIsInstance(self.manifest["verified_tools"], list)
        self.assertGreater(len(self.manifest["verified_tools"]), 0)

    def test_manifest_verified_tools_no_duplicates(self):
        """Manifest verified_tools must not have duplicates."""
        verified = self.manifest["verified_tools"]
        self.assertEqual(len(verified), len(set(verified)))

    def test_manifest_verified_tools_in_registry(self):
        """Manifest verified tools must exist in registry."""
        config = BridgeConfig()
        client = BridgeClient(config)
        registry = ToolRegistry(client)
        registered = set(registry.list_tools())
        verified = set(self.manifest["verified_tools"])
        missing = verified - registered
        self.assertFalse(missing, f"Manifest verified tools not in registry: {missing}")

    def test_manifest_has_categories(self):
        """Manifest should have tool_categories."""
        self.assertIn("tool_categories", self.manifest)

    def test_manifest_categories_complete(self):
        """All categories in manifest should have tools."""
        for category, tools in self.manifest["tool_categories"].items():
            self.assertIsInstance(tools, list)
            self.assertGreater(len(tools), 0, f"Category {category} empty")


class TestSchemaValidation(unittest.TestCase):
    """Test schema validation."""

    def test_all_schemas_valid(self):
        """All schemas should have valid structure."""
        for name, schema in ALL_SCHEMAS.items():
            self.assertIsInstance(name, str)
            self.assertIsInstance(schema.description, str)
            self.assertGreater(len(schema.description), 0)
            self.assertIsInstance(schema.category, ToolCategory)
            self.assertIn(schema.mode.value, ["read", "write"])
            self.assertIsInstance(schema.parameters, dict)
            self.assertIn("type", schema.parameters)
            self.assertEqual(schema.parameters["type"], "object")

    def test_schema_required_fields_array(self):
        """Schema required fields should be array."""
        for schema in ALL_SCHEMAS.values():
            self.assertIsInstance(schema.required, list)

    def test_schema_properties_object(self):
        """Schema properties should be object."""
        for schema in ALL_SCHEMAS.values():
            props = schema.parameters.get("properties", {})
            self.assertIsInstance(props, dict)


if __name__ == "__main__":
    unittest.main()