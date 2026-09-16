"""
Fusion tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


GET_FUSION_COMPS = create_tool_schema(
    name="get_fusion_comps",
    description="Get Fusion compositions on a clip",
    category=ToolCategory.FUSION,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "array", "items": {"type": "object"}},
)

ADD_FUSION_COMP_TO_CLIP = create_tool_schema(
    name="add_fusion_comp_to_clip",
    description="Add a Fusion composition to a clip",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "comp_name": {"type": "string", "description": "Composition name"},
    },
    required=["clip_name", "comp_name"],
)

IMPORT_FUSION_COMP_TO_CLIP = create_tool_schema(
    name="import_fusion_comp_to_clip",
    description="Import a Fusion composition from file to a clip",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "file_path": {"type": "string", "description": "Path to .setting or .comp file"},
    },
    required=["clip_name", "file_path"],
)

EXPORT_FUSION_COMP_FROM_CLIP = create_tool_schema(
    name="export_fusion_comp_from_clip",
    description="Export a Fusion composition from a clip to file",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "comp_name": {"type": "string", "description": "Composition name"},
        "file_path": {"type": "string", "description": "Output file path"},
    },
    required=["clip_name", "comp_name", "file_path"],
)

DELETE_FUSION_COMP_ON_CLIP = create_tool_schema(
    name="delete_fusion_comp_on_clip",
    description="Delete a Fusion composition from a clip",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "comp_name": {"type": "string", "description": "Composition name to delete"},
    },
    required=["clip_name", "comp_name"],
)

LOAD_FUSION_COMP_ON_CLIP = create_tool_schema(
    name="load_fusion_comp_on_clip",
    description="Load a Fusion composition on a clip",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "comp_name": {"type": "string", "description": "Composition name"},
    },
    required=["clip_name", "comp_name"],
)

RENAME_FUSION_COMP_ON_CLIP = create_tool_schema(
    name="rename_fusion_comp_on_clip",
    description="Rename a Fusion composition on a clip",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "old_name": {"type": "string", "description": "Current composition name"},
        "new_name": {"type": "string", "description": "New composition name"},
    },
    required=["clip_name", "old_name", "new_name"],
)

CREATE_MAGIC_MASK = create_tool_schema(
    name="create_magic_mask",
    description="Create a Magic Mask on a clip (Studio only)",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "strokes": {"type": "array", "items": {"type": "object"}, "description": "Stroke data for mask"},
    },
    required=["clip_name", "strokes"],
)

REGENERATE_MAGIC_MASK = create_tool_schema(
    name="regenerate_magic_mask",
    description="Regenerate an existing Magic Mask (Studio only)",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "mask_index": {"type": "integer", "description": "Mask index", "minimum": 0},
    },
    required=["clip_name", "mask_index"],
)

STABILIZE_CLIP = create_tool_schema(
    name="stabilize_clip",
    description="Stabilize a clip (Studio only)",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "mode": {"type": "string", "description": "Stabilization mode", "enum": ["perspective", "similarity", "translation"]},
    },
    required=["clip_name"],
)

SMART_REFRAME_CLIP = create_tool_schema(
    name="smart_reframe_clip",
    description="Smart reframe a clip for different aspect ratios (Studio only)",
    category=ToolCategory.FUSION,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "target_aspect": {"type": "string", "description": "Target aspect ratio", "enum": ["9:16", "1:1", "4:5", "16:9"]},
    },
    required=["clip_name", "target_aspect"],
)

FUSION_SCHEMAS = {
    "get_fusion_comps": GET_FUSION_COMPS,
    "add_fusion_comp_to_clip": ADD_FUSION_COMP_TO_CLIP,
    "import_fusion_comp_to_clip": IMPORT_FUSION_COMP_TO_CLIP,
    "export_fusion_comp_from_clip": EXPORT_FUSION_COMP_FROM_CLIP,
    "delete_fusion_comp_on_clip": DELETE_FUSION_COMP_ON_CLIP,
    "load_fusion_comp_on_clip": LOAD_FUSION_COMP_ON_CLIP,
    "rename_fusion_comp_on_clip": RENAME_FUSION_COMP_ON_CLIP,
    "create_magic_mask": CREATE_MAGIC_MASK,
    "regenerate_magic_mask": REGENERATE_MAGIC_MASK,
    "stabilize_clip": STABILIZE_CLIP,
    "smart_reframe_clip": SMART_REFRAME_CLIP,
}