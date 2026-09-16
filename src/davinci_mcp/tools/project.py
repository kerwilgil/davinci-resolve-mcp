"""
Project tool implementations.
"""

from ..schemas import ToolCategory, ToolMode
from ..tools import ToolRegistry
from ..bridge import ToolResult


async def get_resolve_status(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get DaVinci Resolve connection status."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_resolve_status")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_project_info(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get current project information."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_project_info")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_current_page(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get current page."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_current_page")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def open_page(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Open a specific page."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("open_page", page=arguments["page"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def save_project(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Save the current project."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("save_project")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_project_setting(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set a project setting."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_project_setting", setting=arguments["setting"], value=arguments["value"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_timeline_setting(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set a timeline setting."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {"setting": arguments["setting"], "value": arguments["value"]}
    if "timeline_name" in arguments:
        kwargs["timeline_name"] = arguments["timeline_name"]
    result = client.call_tool_simple("set_timeline_setting", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def export_current_frame(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Export current frame as image."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("export_current_frame", file_path=arguments["file_path"], format=arguments.get("format", "png"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def create_subtitles_from_audio(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Create subtitles from audio."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("create_subtitles_from_audio", timeline_name=arguments.get("timeline_name"), language=arguments.get("language", "en"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def detect_scene_cuts(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Detect scene cuts in timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("detect_scene_cuts", timeline_name=arguments.get("timeline_name"), threshold=arguments.get("threshold", 0.3))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_project_list(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get list of projects."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_project_list")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_database_list(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get list of databases."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_database_list")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def load_project(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Load a project."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("load_project", project_name=arguments["project_name"], database_name=arguments.get("database_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def create_project(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Create a new project."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("create_project", project_name=arguments["project_name"], database_name=arguments.get("database_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_project(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete a project."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_project", project_name=arguments["project_name"], database_name=arguments.get("database_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def archive_project(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Archive a project."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("archive_project", project_name=arguments["project_name"], archive_path=arguments["archive_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def export_project(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Export a project."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("export_project", project_name=arguments["project_name"], file_path=arguments["file_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def import_project(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Import a project."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("import_project", file_path=arguments["file_path"], database_name=arguments.get("database_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def navigate_project_folder(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Navigate to project folder."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("navigate_project_folder", folder_path=arguments["folder_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_database(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set active database."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_database", database_name=arguments["database_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def layout_preset(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Apply layout preset."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("layout_preset", preset_name=arguments["preset_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def render_preset(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Apply render preset."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("render_preset", preset_name=arguments["preset_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def burnin_preset(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Apply burn-in preset."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("burnin_preset", preset_name=arguments["preset_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_keyframe_mode(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get keyframe mode."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_keyframe_mode")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_keyframe_mode(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set keyframe mode."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_keyframe_mode", mode=arguments["mode"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def refresh_lut_list(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Refresh LUT list."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("refresh_lut_list")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_media_storage(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get media storage volumes."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_media_storage")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def reveal_in_storage(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Reveal clip in storage."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("reveal_in_storage", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


# Voice isolation and background removal (AI tools)
async def voice_isolate(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Voice isolation on clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("voice_isolate", clip_name=arguments.get("clip_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def voice_isolate_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Voice isolation on timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("voice_isolate_timeline", timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def remove_background(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Remove background from clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("remove_background", clip_name=arguments.get("clip_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def remove_background_video(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Remove background from video."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("remove_background_video", clip_name=arguments.get("clip_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def remove_background_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Remove background from clip (alias)."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("remove_background_clip", clip_name=arguments.get("clip_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def transcribe_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Transcribe timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("transcribe_timeline", timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def transcribe_file(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Transcribe file."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("transcribe_file", file_path=arguments["file_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_project_tools(registry: ToolRegistry) -> None:
    """Register all project tools."""
    tools = {
        "get_resolve_status": get_resolve_status,
        "get_project_info": get_project_info,
        "get_current_page": get_current_page,
        "open_page": open_page,
        "save_project": save_project,
        "set_project_setting": set_project_setting,
        "set_timeline_setting": set_timeline_setting,
        "export_current_frame": export_current_frame,
        "create_subtitles_from_audio": create_subtitles_from_audio,
        "detect_scene_cuts": detect_scene_cuts,
        "get_project_list": get_project_list,
        "get_database_list": get_database_list,
        "load_project": load_project,
        "create_project": create_project,
        "delete_project": delete_project,
        "archive_project": archive_project,
        "export_project": export_project,
        "import_project": import_project,
        "navigate_project_folder": navigate_project_folder,
        "set_database": set_database,
        "layout_preset": layout_preset,
        "render_preset": render_preset,
        "burnin_preset": burnin_preset,
        "get_keyframe_mode": get_keyframe_mode,
        "set_keyframe_mode": set_keyframe_mode,
        "refresh_lut_list": refresh_lut_list,
        "get_media_storage": get_media_storage,
        "reveal_in_storage": reveal_in_storage,
        "voice_isolate": voice_isolate,
        "voice_isolate_timeline": voice_isolate_timeline,
        "remove_background": remove_background,
        "remove_background_video": remove_background_video,
        "remove_background_clip": remove_background_clip,
        "transcribe_timeline": transcribe_timeline,
        "transcribe_file": transcribe_file,
    }

    for name, handler in tools.items():
        registry.register(name, handler)