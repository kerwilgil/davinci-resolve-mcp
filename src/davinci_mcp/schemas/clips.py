"""
Clip tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


ADD_CLIP_MARKER = create_tool_schema(
    name="add_clip_marker",
    description="Add a marker to a clip",
    category=ToolCategory.CLIPS,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "frame": CommonParams.MARKER_FRAME,
        "color": CommonParams.MARKER_COLOR,
        "name": CommonParams.MARKER_NAME,
        "note": CommonParams.MARKER_NOTE,
        "duration": {"type": "integer", "description": "Marker duration in frames", "minimum": 1},
    },
    required=["clip_name", "frame"],
)

GET_CLIP_MARKERS = create_tool_schema(
    name="get_clip_markers",
    description="Get markers on a clip",
    category=ToolCategory.CLIPS,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "array", "items": {"type": "object"}},
)

DELETE_CLIP_MARKERS = create_tool_schema(
    name="delete_clip_markers",
    description="Delete markers from a clip",
    category=ToolCategory.CLIPS,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "frame": {"type": "integer", "description": "Specific frame to delete (omits deletes all)", "minimum": 0},
    },
    required=["clip_name"],
)

ADD_CLIP_FLAG = create_tool_schema(
    name="add_clip_flag",
    description="Add a flag to a clip",
    category=ToolCategory.CLIPS,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "flag": {"type": "string", "description": "Flag name/color", "enum": ["Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Purple", "Pink"]},
    },
    required=["clip_name", "flag"],
)

GET_CLIP_FLAGS = create_tool_schema(
    name="get_clip_flags",
    description="Get flags on a clip",
    category=ToolCategory.CLIPS,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "array", "items": {"type": "string"}},
)

CLEAR_CLIP_FLAGS = create_tool_schema(
    name="clear_clip_flags",
    description="Clear all flags from a clip",
    category=ToolCategory.CLIPS,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

GET_CLIP_THUMBNAIL = create_tool_schema(
    name="get_clip_thumbnail",
    description="Get thumbnail for a clip",
    category=ToolCategory.CLIPS,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "frame": {"type": "integer", "description": "Frame to get thumbnail from", "minimum": 0},
    },
    required=["clip_name"],
    returns={"type": "object"},
)

GET_CURRENT_VIDEO_ITEM = create_tool_schema(
    name="get_current_video_item",
    description="Get the current video item at playhead",
    category=ToolCategory.CLIPS,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "object"},
)

SET_CLIP_COLOR = create_tool_schema(
    name="set_clip_color",
    description="Set clip color",
    category=ToolCategory.CLIPS,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "color": {"type": "string", "description": "Clip color", "enum": ["Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Purple", "Pink"]},
    },
    required=["clip_name", "color"],
)

SET_CLIP_ENABLED = create_tool_schema(
    name="set_clip_enabled",
    description="Enable or disable a clip",
    category=ToolCategory.CLIPS,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "enabled": {"type": "boolean", "description": "Whether to enable the clip"},
    },
    required=["clip_name", "enabled"],
)

SET_CLIP_PROPERTIES = create_tool_schema(
    name="set_clip_properties",
    description="Set clip properties",
    category=ToolCategory.CLIPS,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "properties": {"type": "object", "description": "Clip properties key-value pairs"},
    },
    required=["clip_name", "properties"],
)

CLIP_SCHEMAS = {
    "add_clip_marker": ADD_CLIP_MARKER,
    "get_clip_markers": GET_CLIP_MARKERS,
    "delete_clip_markers": DELETE_CLIP_MARKERS,
    "add_clip_flag": ADD_CLIP_FLAG,
    "get_clip_flags": GET_CLIP_FLAGS,
    "clear_clip_flags": CLEAR_CLIP_FLAGS,
    "get_clip_thumbnail": GET_CLIP_THUMBNAIL,
    "get_current_video_item": GET_CURRENT_VIDEO_ITEM,
    "set_clip_color": SET_CLIP_COLOR,
    "set_clip_enabled": SET_CLIP_ENABLED,
    "set_clip_properties": SET_CLIP_PROPERTIES,
}