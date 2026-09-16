"""
Color tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


GET_NODE_GRAPH = create_tool_schema(
    name="get_node_graph",
    description="Get the node graph for current clip",
    category=ToolCategory.COLOR,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    returns={"type": "object"},
)

SET_LUT = create_tool_schema(
    name="set_lut",
    description="Apply a LUT to a node",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "node_index": CommonParams.NODE_INDEX,
        "lut_path": CommonParams.LUT_PATH,
    },
    required=["clip_name", "node_index", "lut_path"],
)

GET_LUT = create_tool_schema(
    name="get_lut",
    description="Get LUT applied to a node",
    category=ToolCategory.COLOR,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "node_index": CommonParams.NODE_INDEX,
    },
    required=["clip_name", "node_index"],
    returns={"type": "object"},
)

SET_NODE_ENABLED = create_tool_schema(
    name="set_node_enabled",
    description="Enable or disable a node",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "node_index": CommonParams.NODE_INDEX,
        "enabled": {"type": "boolean", "description": "Whether to enable the node"},
    },
    required=["clip_name", "node_index", "enabled"],
)

APPLY_GRADE_FROM_DRX = create_tool_schema(
    name="apply_grade_from_drx",
    description="Apply a grade from a .drx file",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "drx_path": {"type": "string", "description": "Path to .drx file"},
    },
    required=["clip_name", "drx_path"],
)

RESET_ALL_GRADES = create_tool_schema(
    name="reset_all_grades",
    description="Reset all grades on a clip",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

APPLY_ARRI_CDL_LUT = create_tool_schema(
    name="apply_arri_cdl_lut",
    description="Apply ARRI CDL + LUT to a clip",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "slope": {"type": "array", "items": {"type": "number"}, "description": "RGB slope values", "minItems": 3, "maxItems": 3},
        "offset": {"type": "array", "items": {"type": "number"}, "description": "RGB offset values", "minItems": 3, "maxItems": 3},
        "power": {"type": "array", "items": {"type": "number"}, "description": "RGB power values", "minItems": 3, "maxItems": 3},
        "saturation": {"type": "number", "description": "Saturation value"},
        "lut_path": CommonParams.LUT_PATH,
    },
    required=["clip_name", "slope", "offset", "power", "saturation"],
)

SET_CDL = create_tool_schema(
    name="set_cdl",
    description="Set CDL values on a node",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "node_index": CommonParams.NODE_INDEX,
        "slope": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
        "offset": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
        "power": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
        "saturation": {"type": "number"},
    },
    required=["clip_name", "node_index", "slope", "offset", "power", "saturation"],
)

EXPORT_LUT = create_tool_schema(
    name="export_lut",
    description="Export current grade as LUT",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "output_path": {"type": "string", "description": "Output LUT file path"},
        "format": {"type": "string", "description": "LUT format", "enum": ["cube", "3dl"]},
    },
    required=["clip_name", "output_path"],
)

COPY_GRADES = create_tool_schema(
    name="copy_grades",
    description="Copy grades from one clip to another",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "source_clip": CommonParams.CLIP_NAME,
        "target_clips": {"type": "array", "items": {"type": "string"}, "description": "Target clip names"},
    },
    required=["source_clip", "target_clips"],
)

RESET_NODE_COLORS = create_tool_schema(
    name="reset_node_colors",
    description="Reset colors on a specific node",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "node_index": CommonParams.NODE_INDEX,
    },
    required=["clip_name", "node_index"],
)

GET_COLOR_VERSIONS = create_tool_schema(
    name="get_color_versions",
    description="Get color versions for a clip",
    category=ToolCategory.COLOR,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "array", "items": {"type": "object"}},
)

ADD_COLOR_VERSION = create_tool_schema(
    name="add_color_version",
    description="Add a new color version",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "name": {"type": "string", "description": "Version name"},
    },
    required=["clip_name", "name"],
)

LOAD_COLOR_VERSION = create_tool_schema(
    name="load_color_version",
    description="Load a color version",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "version_name": {"type": "string", "description": "Version name to load"},
    },
    required=["clip_name", "version_name"],
)

DELETE_COLOR_VERSION = create_tool_schema(
    name="delete_color_version",
    description="Delete a color version",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "version_name": {"type": "string", "description": "Version name to delete"},
    },
    required=["clip_name", "version_name"],
)

RENAME_COLOR_VERSION = create_tool_schema(
    name="rename_color_version",
    description="Rename a color version",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "old_name": {"type": "string", "description": "Current version name"},
        "new_name": {"type": "string", "description": "New version name"},
    },
    required=["clip_name", "old_name", "new_name"],
)

GET_COLOR_GROUPS = create_tool_schema(
    name="get_color_groups",
    description="Get color groups",
    category=ToolCategory.COLOR,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "array", "items": {"type": "object"}},
)

ADD_COLOR_GROUP = create_tool_schema(
    name="add_color_group",
    description="Add a color group",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "name": {"type": "string", "description": "Group name"},
    },
    required=["name"],
)

DELETE_COLOR_GROUP = create_tool_schema(
    name="delete_color_group",
    description="Delete a color group",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "group_name": {"type": "string", "description": "Group name to delete"},
    },
    required=["group_name"],
)

ASSIGN_TO_COLOR_GROUP = create_tool_schema(
    name="assign_to_color_group",
    description="Assign clips to a color group",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "group_name": CommonParams.GALLERY_ALBUM,
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Clip names to assign"},
    },
    required=["group_name", "clip_names"],
)

REMOVE_FROM_COLOR_GROUP = create_tool_schema(
    name="remove_from_color_group",
    description="Remove clips from a color group",
    category=ToolCategory.COLOR,
    mode=ToolMode.WRITE,
    properties={
        "group_name": CommonParams.GALLERY_ALBUM,
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Clip names to remove"},
    },
    required=["group_name", "clip_names"],
)

COLOR_SCHEMAS = {
    "get_node_graph": GET_NODE_GRAPH,
    "set_lut": SET_LUT,
    "get_lut": GET_LUT,
    "set_node_enabled": SET_NODE_ENABLED,
    "apply_grade_from_drx": APPLY_GRADE_FROM_DRX,
    "reset_all_grades": RESET_ALL_GRADES,
    "apply_arri_cdl_lut": APPLY_ARRI_CDL_LUT,
    "set_cdl": SET_CDL,
    "export_lut": EXPORT_LUT,
    "copy_grades": COPY_GRADES,
    "reset_node_colors": RESET_NODE_COLORS,
    "get_color_versions": GET_COLOR_VERSIONS,
    "add_color_version": ADD_COLOR_VERSION,
    "load_color_version": LOAD_COLOR_VERSION,
    "delete_color_version": DELETE_COLOR_VERSION,
    "rename_color_version": RENAME_COLOR_VERSION,
    "get_color_groups": GET_COLOR_GROUPS,
    "add_color_group": ADD_COLOR_GROUP,
    "delete_color_group": DELETE_COLOR_GROUP,
    "assign_to_color_group": ASSIGN_TO_COLOR_GROUP,
    "remove_from_color_group": REMOVE_FROM_COLOR_GROUP,
}