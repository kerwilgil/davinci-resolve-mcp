"""Tests for schema definitions and validation."""

import unittest
from src.davinci_mcp.schemas import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
    ALL_SCHEMAS,
    VERIFIED_TOOLS,
    get_schema,
    is_verified,
    get_tools_by_category,
    get_write_tools,
    get_read_tools,
)


class TestCommonParams(unittest.TestCase):
    """Test common parameter definitions."""

    def test_common_params_exist(self):
        """Common parameters should be defined."""
        self.assertIn("type", CommonParams.PROJECT_NAME)
        self.assertIn("type", CommonParams.TIMELINE_NAME)
        self.assertIn("type", CommonParams.CLIP_NAME)
        self.assertIn("type", CommonParams.MARKER_FRAME)
        self.assertIn("enum", CommonParams.MARKER_COLOR)
        self.assertIn("type", CommonParams.TRACK_TYPE)
        self.assertIn("enum", CommonParams.TRACK_TYPE)
        self.assertIn("type", CommonParams.RENDER_FORMAT)
        self.assertIn("type", CommonParams.MEDIA_PATH)
        self.assertIn("type", CommonParams.FOLDER_NAME)
        self.assertIn("enum", CommonParams.PAGE_NAME)
        self.assertIn("type", CommonParams.PLAYHEAD_FRAME)
        self.assertIn("pattern", CommonParams.TIMECODE)
        self.assertIn("type", CommonParams.NODE_INDEX)
        self.assertIn("type", CommonParams.LUT_PATH)
        self.assertIn("type", CommonParams.GALLERY_ALBUM)
        self.assertIn("type", CommonParams.STILL_LABEL)
        self.assertIn("type", CommonParams.VOICE_ISOLATION_STRENGTH)
        self.assertIn("type", CommonParams.FAIRLIGHT_PRESET)
        self.assertIn("enum", CommonParams.FAIRLIGHT_PRESET_TYPE)
        self.assertIn("type", CommonParams.TAKE_NUMBER)
        self.assertIn("type", CommonParams.DATABASE_NAME)
        self.assertIn("type", CommonParams.PROJECT_INDEX)


class TestCreateToolSchema(unittest.TestCase):
    """Test schema factory function."""

    def test_create_basic_schema(self):
        """Test creating a basic schema."""
        schema = create_tool_schema(
            name="test_tool",
            description="A test tool",
            category=ToolCategory.PROJECT,
            mode=ToolMode.READ,
            properties={
                "param1": {"type": "string", "description": "First param"},
            },
            required=["param1"],
        )

        self.assertEqual(schema.name, "test_tool")
        self.assertEqual(schema.description, "A test tool")
        self.assertEqual(schema.category, ToolCategory.PROJECT)
        self.assertEqual(schema.mode, ToolMode.READ)
        self.assertEqual(schema.required, ["param1"])
        self.assertIn("param1", schema.parameters["properties"])

    def test_create_schema_with_returns(self):
        """Test creating schema with returns."""
        schema = create_tool_schema(
            name="test_tool",
            description="A test tool",
            category=ToolCategory.PROJECT,
            mode=ToolMode.READ,
            properties={},
            returns={"type": "object", "properties": {"result": {"type": "string"}}},
        )

        self.assertIsNotNone(schema.returns)
        self.assertEqual(schema.returns["type"], "object")

    def test_create_schema_with_examples(self):
        """Test creating schema with examples."""
        schema = create_tool_schema(
            name="test_tool",
            description="A test tool",
            category=ToolCategory.PROJECT,
            mode=ToolMode.READ,
            properties={},
            examples=[{"param1": "value1"}],
        )

        self.assertEqual(len(schema.examples), 1)
        self.assertEqual(schema.examples[0], {"param1": "value1"})


class TestSchemaRegistry(unittest.TestCase):
    """Test the combined schema registry."""

    def test_all_schemas_populated(self):
        """ALL_SCHEMAS should contain all categories."""
        self.assertGreater(len(ALL_SCHEMAS), 100)

    def test_all_categories_represented(self):
        """All tool categories should be represented."""
        categories = set(s.category for s in ALL_SCHEMAS.values())
        self.assertEqual(categories, set(ToolCategory))

    def test_all_modes_represented(self):
        """Both read and write modes should be represented."""
        modes = set(s.mode for s in ALL_SCHEMAS.values())
        self.assertEqual(modes, {ToolMode.READ, ToolMode.WRITE})

    def test_verified_tools_list(self):
        """VERIFIED_TOOLS should be a list of strings."""
        self.assertIsInstance(VERIFIED_TOOLS, list)
        self.assertGreater(len(VERIFIED_TOOLS), 30)
        for tool in VERIFIED_TOOLS:
            self.assertIsInstance(tool, str)

    def test_get_schema_returns_schema(self):
        """get_schema should return schema for known tools."""
        schema = get_schema("get_resolve_status")
        self.assertIsNotNone(schema)
        self.assertEqual(schema.name, "get_resolve_status")

    def test_get_schema_returns_none_for_unknown(self):
        """get_schema should return None for unknown tools."""
        schema = get_schema("unknown_tool_xyz")
        self.assertIsNone(schema)

    def test_is_verified(self):
        """is_verified should work correctly."""
        self.assertTrue(is_verified("get_resolve_status"))
        self.assertTrue(is_verified("create_timeline"))
        self.assertFalse(is_verified("unknown_tool_xyz"))

    def test_get_tools_by_category(self):
        """get_tools_by_category should return correct tools."""
        project_tools = get_tools_by_category(ToolCategory.PROJECT)
        self.assertGreater(len(project_tools), 5)
        for tool in project_tools:
            schema = get_schema(tool)
            self.assertEqual(schema.category, ToolCategory.PROJECT)

    def test_get_write_tools(self):
        """get_write_tools should return only write tools."""
        write_tools = get_write_tools()
        self.assertGreater(len(write_tools), 30)
        for tool in write_tools:
            schema = get_schema(tool)
            self.assertEqual(schema.mode, ToolMode.WRITE)

    def test_get_read_tools(self):
        """get_read_tools should return only read tools."""
        read_tools = get_read_tools()
        self.assertGreater(len(read_tools), 30)
        for tool in read_tools:
            schema = get_schema(tool)
            self.assertEqual(schema.mode, ToolMode.READ)


class TestCategorySchemas(unittest.TestCase):
    """Test each category's schema module."""

    def test_timeline_schemas(self):
        """Timeline schemas should be valid."""
        from src.davinci_mcp.schemas.timeline import TIMELINE_SCHEMAS
        self.assertGreater(len(TIMELINE_SCHEMAS), 20)
        for name, schema in TIMELINE_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.TIMELINE)

    def test_media_schemas(self):
        """Media schemas should be valid."""
        from src.davinci_mcp.schemas.media import MEDIA_SCHEMAS
        self.assertGreater(len(MEDIA_SCHEMAS), 10)
        for name, schema in MEDIA_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.MEDIA)

    def test_clips_schemas(self):
        """Clips schemas should be valid."""
        from src.davinci_mcp.schemas.clips import CLIP_SCHEMAS
        self.assertGreater(len(CLIP_SCHEMAS), 5)
        for name, schema in CLIP_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.CLIPS)

    def test_color_schemas(self):
        """Color schemas should be valid."""
        from src.davinci_mcp.schemas.color import COLOR_SCHEMAS
        self.assertGreater(len(COLOR_SCHEMAS), 15)
        for name, schema in COLOR_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.COLOR)

    def test_fusion_schemas(self):
        """Fusion schemas should be valid."""
        from src.davinci_mcp.schemas.fusion import FUSION_SCHEMAS
        self.assertGreater(len(FUSION_SCHEMAS), 5)
        for name, schema in FUSION_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.FUSION)

    def test_audio_schemas(self):
        """Audio schemas should be valid."""
        from src.davinci_mcp.schemas.audio import AUDIO_SCHEMAS
        self.assertGreater(len(AUDIO_SCHEMAS), 10)
        for name, schema in AUDIO_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.AUDIO)

    def test_render_schemas(self):
        """Render schemas should be valid."""
        from src.davinci_mcp.schemas.render import RENDER_SCHEMAS
        self.assertGreater(len(RENDER_SCHEMAS), 8)
        for name, schema in RENDER_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.RENDER)

    def test_gallery_schemas(self):
        """Gallery schemas should be valid."""
        from src.davinci_mcp.schemas.gallery import GALLERY_SCHEMAS
        self.assertGreater(len(GALLERY_SCHEMAS), 5)
        for name, schema in GALLERY_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.GALLERY)

    def test_project_schemas(self):
        """Project schemas should be valid."""
        from src.davinci_mcp.schemas.project import PROJECT_SCHEMAS
        self.assertGreater(len(PROJECT_SCHEMAS), 20)
        for name, schema in PROJECT_SCHEMAS.items():
            self.assertEqual(schema.category, ToolCategory.PROJECT)


class TestSchemaValidation(unittest.TestCase):
    """Test schema parameter validation."""

    def test_no_duplicate_names(self):
        """No duplicate tool names across all schemas."""
        names = list(ALL_SCHEMAS.keys())
        self.assertEqual(len(names), len(set(names)))

    def test_all_schemas_have_parameters(self):
        """All schemas should have parameters defined."""
        for name, schema in ALL_SCHEMAS.items():
            self.assertIsInstance(schema.parameters, dict)
            self.assertEqual(schema.parameters.get("type"), "object")

    def test_schema_descriptions_not_empty(self):
        """All schemas should have non-empty descriptions."""
        for name, schema in ALL_SCHEMAS.items():
            self.assertGreater(len(schema.description), 5,
                               f"Schema {name} has empty or too short description")

    def test_required_fields_exist_in_properties(self):
        """Required fields should exist in properties."""
        for name, schema in ALL_SCHEMAS.items():
            props = schema.parameters.get("properties", {})
            for req in schema.required:
                self.assertIn(req, props,
                              f"Required field '{req}' not in properties for {name}")

    def test_enum_values_are_lists(self):
        """Enum values should be lists."""
        for name, schema in ALL_SCHEMAS.items():
            props = schema.parameters.get("properties", {})
            for prop_name, prop_schema in props.items():
                if "enum" in prop_schema:
                    self.assertIsInstance(prop_schema["enum"], list,
                                          f"Enum for {name}.{prop_name} should be list")


if __name__ == "__main__":
    unittest.main()