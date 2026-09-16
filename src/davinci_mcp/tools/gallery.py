"""
Gallery tool implementations.
"""

from ..tools import ToolRegistry
from ..bridge import ToolResult


async def get_gallery_albums(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get gallery albums."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_gallery_albums")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_album_stills(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get album stills."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_album_stills", album_name=arguments["album_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_current_album(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set current album."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_current_album", album_name=arguments["album_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def create_gallery_album(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Create gallery album."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("create_gallery_album", album_name=arguments["album_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def grab_still(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Grab still."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("grab_still", album_name=arguments["album_name"], label=arguments.get("label"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def grab_all_stills(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Grab all stills."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("grab_all_stills", album_name=arguments["album_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def export_stills(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Export stills."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("export_stills", album_name=arguments["album_name"], output_folder=arguments["output_folder"], format=arguments.get("format", "png"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def import_stills(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Import stills."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("import_stills", album_name=arguments["album_name"], file_paths=arguments["file_paths"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_stills(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete stills."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_stills", album_name=arguments["album_name"], still_labels=arguments["still_labels"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_still_label(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set still label."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_still_label", album_name=arguments["album_name"], still_label=arguments["still_label"], new_label=arguments["new_label"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_gallery_tools(registry: ToolRegistry) -> None:
    """Register all gallery tools."""
    tools = {
        "get_gallery_albums": get_gallery_albums,
        "get_album_stills": get_album_stills,
        "set_current_album": set_current_album,
        "create_gallery_album": create_gallery_album,
        "grab_still": grab_still,
        "grab_all_stills": grab_all_stills,
        "export_stills": export_stills,
        "import_stills": import_stills,
        "delete_stills": delete_stills,
        "set_still_label": set_still_label,
    }

    for name, handler in tools.items():
        registry.register(name, handler)