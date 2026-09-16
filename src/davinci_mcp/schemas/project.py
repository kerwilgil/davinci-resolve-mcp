"""
Project tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


GET_RESOLVE_STATUS = create_tool_schema(
    name="get_resolve_status",
    description="Get DaVinci Resolve connection status",
    category=ToolCategory.PROJECT,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "object"},
)

GET_PROJECT_INFO = create_tool_schema(
    name="get_project_info",
    description="Get information about the current project",
    category=ToolCategory.PROJECT,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "object"},
)

GET_CURRENT_PAGE = create_tool_schema(
    name="get_current_page",
    description="Get the current page in DaVinci Resolve",
    category=ToolCategory.PROJECT,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "object"},
)

OPEN_PAGE = create_tool_schema(
    name="open_page",
    description="Open a specific page in DaVinci Resolve",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "page": CommonParams.PAGE_NAME,
    },
    required=["page"],
)

SAVE_PROJECT = create_tool_schema(
    name="save_project",
    description="Save the current project",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={},
)

SET_PROJECT_SETTING = create_tool_schema(
    name="set_project_setting",
    description="Set a project setting",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "setting": {"type": "string", "description": "Setting name"},
        "value": {"type": "string", "description": "Setting value"},
    },
    required=["setting", "value"],
)

SET_TIMELINE_SETTING = create_tool_schema(
    name="set_timeline_setting",
    description="Set a timeline setting",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "setting": {"type": "string", "description": "Setting name"},
        "value": {"type": "string", "description": "Setting value"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["setting", "value"],
)

EXPORT_CURRENT_FRAME = create_tool_schema(
    name="export_current_frame",
    description="Export the current frame as an image",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "file_path": {"type": "string", "description": "Output file path"},
        "format": {"type": "string", "description": "Image format", "enum": ["png", "jpg", "tiff", "exr"]},
    },
    required=["file_path"],
)

CREATE_SUBTITLES_FROM_AUDIO = create_tool_schema(
    name="create_subtitles_from_audio",
    description="Create subtitles from audio using speech recognition",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "timeline_name": CommonParams.TIMELINE_NAME,
        "language": {"type": "string", "description": "Language code (e.g., 'en', 'es')"},
    },
    required=["timeline_name"],
)

DETECT_SCENE_CUTS = create_tool_schema(
    name="detect_scene_cuts",
    description="Detect scene cuts in the timeline",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "timeline_name": CommonParams.TIMELINE_NAME,
        "threshold": {"type": "number", "description": "Detection threshold (0.0-1.0)", "minimum": 0.0, "maximum": 1.0},
    },
    required=["timeline_name"],
)

GET_PROJECT_LIST = create_tool_schema(
    name="get_project_list",
    description="Get list of projects in current database",
    category=ToolCategory.PROJECT,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "array", "items": {"type": "string"}},
)

GET_DATABASE_LIST = create_tool_schema(
    name="get_database_list",
    description="Get list of available databases",
    category=ToolCategory.PROJECT,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "array", "items": {"type": "object"}},
)

LOAD_PROJECT = create_tool_schema(
    name="load_project",
    description="Load a project from the database",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "project_name": {"type": "string", "description": "Project name to load"},
        "database_name": CommonParams.DATABASE_NAME,
    },
    required=["project_name"],
)

CREATE_PROJECT = create_tool_schema(
    name="create_project",
    description="Create a new project",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "project_name": {"type": "string", "description": "New project name"},
        "database_name": CommonParams.DATABASE_NAME,
    },
    required=["project_name"],
)

DELETE_PROJECT = create_tool_schema(
    name="delete_project",
    description="Delete a project from the database",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "project_name": {"type": "string", "description": "Project name to delete"},
        "database_name": CommonParams.DATABASE_NAME,
    },
    required=["project_name"],
)

ARCHIVE_PROJECT = create_tool_schema(
    name="archive_project",
    description="Archive a project",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "project_name": {"type": "string", "description": "Project name to archive"},
        "archive_path": {"type": "string", "description": "Archive file path"},
    },
    required=["project_name", "archive_path"],
)

EXPORT_PROJECT = create_tool_schema(
    name="export_project",
    description="Export a project to .drp file",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "project_name": {"type": "string", "description": "Project name to export"},
        "file_path": {"type": "string", "description": "Output .drp file path"},
    },
    required=["project_name", "file_path"],
)

IMPORT_PROJECT = create_tool_schema(
    name="import_project",
    description="Import a project from .drp file",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "file_path": {"type": "string", "description": "Path to .drp file"},
        "database_name": CommonParams.DATABASE_NAME,
    },
    required=["file_path"],
)

NAVIGATE_PROJECT_FOLDER = create_tool_schema(
    name="navigate_project_folder",
    description="Navigate to a project folder in the project manager",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "folder_path": {"type": "string", "description": "Folder path"},
    },
    required=["folder_path"],
)

SET_DATABASE = create_tool_schema(
    name="set_database",
    description="Set the active database",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "database_name": CommonParams.DATABASE_NAME,
    },
    required=["database_name"],
)

LAYOUT_PRESET = create_tool_schema(
    name="layout_preset",
    description="Apply a layout preset",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "preset_name": {"type": "string", "description": "Layout preset name"},
    },
    required=["preset_name"],
)

RENDER_PRESET = create_tool_schema(
    name="render_preset",
    description="Apply a render preset",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "preset_name": {"type": "string", "description": "Render preset name"},
    },
    required=["preset_name"],
)

BURNIN_PRESET = create_tool_schema(
    name="burnin_preset",
    description="Apply a burn-in preset",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "preset_name": {"type": "string", "description": "Burn-in preset name"},
    },
    required=["preset_name"],
)

GET_KEYFRAME_MODE = create_tool_schema(
    name="get_keyframe_mode",
    description="Get current keyframe mode",
    category=ToolCategory.PROJECT,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "object"},
)

SET_KEYFRAME_MODE = create_tool_schema(
    name="set_keyframe_mode",
    description="Set keyframe mode",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "mode": {"type": "string", "description": "Keyframe mode", "enum": ["auto", "manual", "none"]},
    },
    required=["mode"],
)

REFRESH_LUT_LIST = create_tool_schema(
    name="refresh_lut_list",
    description="Refresh the LUT list",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={},
)

GET_MEDIA_STORAGE = create_tool_schema(
    name="get_media_storage",
    description="Get available media storage volumes",
    category=ToolCategory.PROJECT,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "array", "items": {"type": "object"}},
)

REVEAL_IN_STORAGE = create_tool_schema(
    name="reveal_in_storage",
    description="Reveal a clip in media storage",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

VOICE_ISOLATE = create_tool_schema(
    name="voice_isolate",
    description="Voice isolation on clip",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

VOICE_ISOLATE_TIMELINE = create_tool_schema(
    name="voice_isolate_timeline",
    description="Voice isolation on timeline",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["timeline_name"],
)

REMOVE_BACKGROUND = create_tool_schema(
    name="remove_background",
    description="Remove background from clip",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

REMOVE_BACKGROUND_VIDEO = create_tool_schema(
    name="remove_background_video",
    description="Remove background from video",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

REMOVE_BACKGROUND_CLIP = create_tool_schema(
    name="remove_background_clip",
    description="Remove background from clip (alias)",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

TRANSCRIBE_TIMELINE = create_tool_schema(
    name="transcribe_timeline",
    description="Transcribe timeline",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["timeline_name"],
)

TRANSCRIBE_FILE = create_tool_schema(
    name="transcribe_file",
    description="Transcribe file",
    category=ToolCategory.PROJECT,
    mode=ToolMode.WRITE,
    properties={
        "file_path": {"type": "string", "description": "Path to file to transcribe"},
    },
    required=["file_path"],
)

PROJECT_SCHEMAS = {
    "get_resolve_status": GET_RESOLVE_STATUS,
    "get_project_info": GET_PROJECT_INFO,
    "get_current_page": GET_CURRENT_PAGE,
    "open_page": OPEN_PAGE,
    "save_project": SAVE_PROJECT,
    "set_project_setting": SET_PROJECT_SETTING,
    "set_timeline_setting": SET_TIMELINE_SETTING,
    "export_current_frame": EXPORT_CURRENT_FRAME,
    "create_subtitles_from_audio": CREATE_SUBTITLES_FROM_AUDIO,
    "detect_scene_cuts": DETECT_SCENE_CUTS,
    "get_project_list": GET_PROJECT_LIST,
    "get_database_list": GET_DATABASE_LIST,
    "load_project": LOAD_PROJECT,
    "create_project": CREATE_PROJECT,
    "delete_project": DELETE_PROJECT,
    "archive_project": ARCHIVE_PROJECT,
    "export_project": EXPORT_PROJECT,
    "import_project": IMPORT_PROJECT,
    "navigate_project_folder": NAVIGATE_PROJECT_FOLDER,
    "set_database": SET_DATABASE,
    "layout_preset": LAYOUT_PRESET,
    "render_preset": RENDER_PRESET,
    "burnin_preset": BURNIN_PRESET,
    "get_keyframe_mode": GET_KEYFRAME_MODE,
    "set_keyframe_mode": SET_KEYFRAME_MODE,
    "refresh_lut_list": REFRESH_LUT_LIST,
    "get_media_storage": GET_MEDIA_STORAGE,
    "reveal_in_storage": REVEAL_IN_STORAGE,
    "voice_isolate": VOICE_ISOLATE,
    "voice_isolate_timeline": VOICE_ISOLATE_TIMELINE,
    "remove_background": REMOVE_BACKGROUND,
    "remove_background_video": REMOVE_BACKGROUND_VIDEO,
    "remove_background_clip": REMOVE_BACKGROUND_CLIP,
    "transcribe_timeline": TRANSCRIBE_TIMELINE,
    "transcribe_file": TRANSCRIBE_FILE,
}