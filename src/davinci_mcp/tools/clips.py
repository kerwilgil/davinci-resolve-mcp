"""
Clip tool implementations.
"""

from ..tools import ToolRegistry
from ..bridge import ToolResult


async def add_clip_marker(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add clip marker."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {"clip_name": arguments["clip_name"], "frame": arguments["frame"]}
    if "color" in arguments:
        kwargs["color"] = arguments["color"]
    if "name" in arguments:
        kwargs["name"] = arguments["name"]
    if "note" in arguments:
        kwargs["note"] = arguments["note"]
    if "duration" in arguments:
        kwargs["duration"] = arguments["duration"]
    result = client.call_tool_simple("add_clip_marker", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_clip_markers(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get clip markers."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_clip_markers", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_clip_markers(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete clip markers."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {"clip_name": arguments["clip_name"]}
    if "frame" in arguments:
        kwargs["frame"] = arguments["frame"]
    result = client.call_tool_simple("delete_clip_markers", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def add_clip_flag(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add clip flag."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("add_clip_flag", clip_name=arguments["clip_name"], flag=arguments["flag"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_clip_flags(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get clip flags."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_clip_flags", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def clear_clip_flags(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Clear clip flags."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("clear_clip_flags", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_clip_thumbnail(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get clip thumbnail."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_clip_thumbnail", clip_name=arguments["clip_name"], frame=arguments.get("frame", 0))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_current_video_item(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get current video item."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_current_video_item")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_clip_color(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set clip color."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_clip_color", clip_name=arguments["clip_name"], color=arguments["color"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_clip_enabled(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Enable or disable a clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_clip_enabled", clip_name=arguments["clip_name"], enabled=arguments["enabled"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_clip_properties(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set clip properties."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_clip_properties", clip_name=arguments["clip_name"], properties=arguments["properties"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_clips_tools(registry: ToolRegistry) -> None:
    """Register all clip tools."""
    tools = {
        "add_clip_marker": add_clip_marker,
        "get_clip_markers": get_clip_markers,
        "delete_clip_markers": delete_clip_markers,
        "add_clip_flag": add_clip_flag,
        "get_clip_flags": get_clip_flags,
        "clear_clip_flags": clear_clip_flags,
        "get_clip_thumbnail": get_clip_thumbnail,
        "get_current_video_item": get_current_video_item,
        "set_clip_color": set_clip_color,
        "set_clip_enabled": set_clip_enabled,
        "set_clip_properties": set_clip_properties,
    }

    for name, handler in tools.items():
        registry.register(name, handler)