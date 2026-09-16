"""
Media tool implementations.
"""

from ..tools import ToolRegistry
from ..bridge import ToolResult


async def get_media_pool(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get media pool root."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_media_pool")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_media_pool_structure(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get media pool structure."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_media_pool_structure")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def navigate_media_pool(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Navigate media pool."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("navigate_media_pool", folder_path=arguments["folder_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def create_media_pool_folder(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Create media pool folder."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("create_media_pool_folder", folder_name=arguments["folder_name"], parent_path=arguments.get("parent_path", ""))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def import_media(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Import media."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("import_media", file_paths=arguments["file_paths"], folder_path=arguments.get("folder_path"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_clip_metadata(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get clip metadata."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_clip_metadata", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_clip_metadata(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set clip metadata."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_clip_metadata", clip_name=arguments["clip_name"], metadata=arguments["metadata"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_clip_info(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get clip info."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_clip_info", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_clip_properties(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get clip properties."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_clip_properties", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_pool_clip_property(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set pool clip property."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_pool_clip_property", clip_name=arguments["clip_name"], property_name=arguments["property_name"], property_value=arguments["property_value"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_media_pool_clips(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete media pool clips."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_media_pool_clips", clip_names=arguments["clip_names"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def move_media_pool_clips(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Move media pool clips."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("move_media_pool_clips", clip_names=arguments["clip_names"], destination_folder=arguments["destination_folder"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def relink_media_pool_clips(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Relink media pool clips."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("relink_media_pool_clips", clip_names=arguments["clip_names"], new_paths=arguments["new_paths"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def unlink_media_pool_clips(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Unlink media pool clips."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("unlink_media_pool_clips", clip_names=arguments["clip_names"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def auto_sync_audio(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Auto sync audio."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("auto_sync_audio", video_clip=arguments["video_clip"], audio_clips=arguments["audio_clips"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def import_timeline_from_file(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Import timeline from file."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("import_timeline_from_file", file_path=arguments["file_path"], format=arguments["format"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def export_metadata(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Export metadata."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("export_metadata", file_path=arguments["file_path"], format=arguments["format"], scope=arguments["scope"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def import_media_from_storage(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Import media from storage."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("import_media_from_storage", storage_path=arguments["storage_path"], file_patterns=arguments.get("file_patterns"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_media_tools(registry: ToolRegistry) -> None:
    """Register all media tools."""
    tools = {
        "get_media_pool": get_media_pool,
        "get_media_pool_structure": get_media_pool_structure,
        "navigate_media_pool": navigate_media_pool,
        "create_media_pool_folder": create_media_pool_folder,
        "import_media": import_media,
        "get_clip_metadata": get_clip_metadata,
        "set_clip_metadata": set_clip_metadata,
        "get_clip_info": get_clip_info,
        "get_clip_properties": get_clip_properties,
        "set_pool_clip_property": set_pool_clip_property,
        "delete_media_pool_clips": delete_media_pool_clips,
        "move_media_pool_clips": move_media_pool_clips,
        "relink_media_pool_clips": relink_media_pool_clips,
        "unlink_media_pool_clips": unlink_media_pool_clips,
        "auto_sync_audio": auto_sync_audio,
        "import_timeline_from_file": import_timeline_from_file,
        "export_metadata": export_metadata,
        "import_media_from_storage": import_media_from_storage,
    }

    for name, handler in tools.items():
        registry.register(name, handler)