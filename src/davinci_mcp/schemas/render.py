"""
Render tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


GET_RENDER_SETTINGS = create_tool_schema(
    name="get_render_settings",
    description="Get current render settings",
    category=ToolCategory.RENDER,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "object"},
)

SET_RENDER_SETTINGS = create_tool_schema(
    name="set_render_settings",
    description="Set render settings",
    category=ToolCategory.RENDER,
    mode=ToolMode.WRITE,
    properties={
        "settings": {"type": "object", "description": "Render settings key-value pairs"},
    },
    required=["settings"],
)

SET_RENDER_FORMAT = create_tool_schema(
    name="set_render_format",
    description="Set render format",
    category=ToolCategory.RENDER,
    mode=ToolMode.WRITE,
    properties={
        "format": CommonParams.RENDER_FORMAT,
    },
    required=["format"],
)

GET_RENDER_FORMATS = create_tool_schema(
    name="get_render_formats",
    description="Get available render formats",
    category=ToolCategory.RENDER,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "array", "items": {"type": "string"}},
)

ADD_RENDER_JOB = create_tool_schema(
    name="add_render_job",
    description="Add a render job to the queue",
    category=ToolCategory.RENDER,
    mode=ToolMode.WRITE,
    properties={
        "preset": CommonParams.RENDER_PRESET,
        "timeline_name": CommonParams.TIMELINE_NAME,
        "output_path": {"type": "string", "description": "Output file path"},
        "render_range": {"type": "string", "description": "Render range", "enum": ["full", "in_out", "selected"]},
    },
    required=["preset", "output_path"],
)

START_RENDERING = create_tool_schema(
    name="start_rendering",
    description="Start rendering queued jobs",
    category=ToolCategory.RENDER,
    mode=ToolMode.WRITE,
    properties={
        "wait_for_completion": {"type": "boolean", "description": "Poll accepted job IDs to completion", "default": False},
        "completion_timeout": {"type": "number", "description": "Seconds to wait after acceptance (default 30)", "minimum": 0.1, "maximum": 600},
    },
)

STOP_RENDERING = create_tool_schema(
    name="stop_rendering",
    description="Stop current rendering",
    category=ToolCategory.RENDER,
    mode=ToolMode.WRITE,
    properties={},
)

DELETE_RENDER_JOB = create_tool_schema(
    name="delete_render_job",
    description="Delete a render job from the queue",
    category=ToolCategory.RENDER,
    mode=ToolMode.WRITE,
    properties={
        "job_index": {"type": "integer", "description": "Zero-based index in the current queue", "minimum": 0},
        "job_id": {"type": "string", "description": "Stable Resolve job ID; prefer for deletion", "minLength": 1},
    },
    required=[],
)

GET_RENDER_JOB_STATUS = create_tool_schema(
    name="get_render_job_status",
    description="Get status of a render job",
    category=ToolCategory.RENDER,
    mode=ToolMode.READ,
    properties={
        "job_index": {"type": "integer", "description": "Zero-based index in the current queue", "minimum": 0},
        "job_id": {"type": "string", "description": "Stable Resolve job ID; prefer for deletion", "minLength": 1},
    },
    required=[],
    returns={"type": "object"},
)

GET_RENDER_RESOLUTIONS = create_tool_schema(
    name="get_render_resolutions",
    description="Get available render resolutions",
    category=ToolCategory.RENDER,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "array", "items": {"type": "string"}},
)

GET_QUICK_EXPORT_PRESETS = create_tool_schema(
    name="get_quick_export_presets",
    description="Get available quick export presets",
    category=ToolCategory.RENDER,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "array", "items": {"type": "string"}},
)

QUICK_EXPORT = create_tool_schema(
    name="quick_export",
    description="Quick export current timeline",
    category=ToolCategory.RENDER,
    mode=ToolMode.WRITE,
    properties={
        "preset": {"type": "string", "description": "Quick export preset name"},
        "output_path": {"type": "string", "description": "Output file path"},
    },
    required=["preset", "output_path"],
)

SET_RENDER_MODE = create_tool_schema(
    name="set_render_mode",
    description="Set render mode (single/individual clips)",
    category=ToolCategory.RENDER,
    mode=ToolMode.WRITE,
    properties={
        "mode": {"type": "string", "description": "Render mode", "enum": ["single", "individual_clips"]},
    },
    required=["mode"],
)

RENDER_SCHEMAS = {
    "get_render_settings": GET_RENDER_SETTINGS,
    "set_render_settings": SET_RENDER_SETTINGS,
    "set_render_format": SET_RENDER_FORMAT,
    "get_render_formats": GET_RENDER_FORMATS,
    "add_render_job": ADD_RENDER_JOB,
    "start_rendering": START_RENDERING,
    "stop_rendering": STOP_RENDERING,
    "delete_render_job": DELETE_RENDER_JOB,
    "get_render_job_status": GET_RENDER_JOB_STATUS,
    "get_render_resolutions": GET_RENDER_RESOLUTIONS,
    "get_quick_export_presets": GET_QUICK_EXPORT_PRESETS,
    "quick_export": QUICK_EXPORT,
    "set_render_mode": SET_RENDER_MODE,
}