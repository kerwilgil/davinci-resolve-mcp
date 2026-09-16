"""
Audio tool implementations.
"""

from ..tools import ToolRegistry
from ..bridge import ToolResult


async def get_fairlight_presets(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get Fairlight presets."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_fairlight_presets", preset_type=arguments.get("preset_type"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def apply_fairlight_preset(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Apply Fairlight preset."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("apply_fairlight_preset", track_index=arguments["track_index"], preset_name=arguments["preset_name"], preset_type=arguments["preset_type"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def insert_audio_at_playhead(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Insert audio at playhead."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("insert_audio_at_playhead", file_path=arguments["file_path"], track_index=arguments.get("track_index"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_voice_isolation_state(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get voice isolation state."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_voice_isolation_state", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_voice_isolation_state(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set voice isolation state."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_voice_isolation_state", clip_name=arguments["clip_name"], enabled=arguments["enabled"], strength=arguments.get("strength", 0.5))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_takes(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get takes."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_takes", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def add_take(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add take."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("add_take", clip_name=arguments["clip_name"], take_name=arguments["take_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def select_take(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Select take."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("select_take", clip_name=arguments["clip_name"], take_number=arguments["take_number"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_take(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete take."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_take", clip_name=arguments["clip_name"], take_number=arguments["take_number"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def finalize_take(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Finalize take."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("finalize_take", clip_name=arguments["clip_name"], take_number=arguments["take_number"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def link_proxy_media(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Link proxy media."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("link_proxy_media", clip_name=arguments["clip_name"], proxy_path=arguments["proxy_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def unlink_proxy_media(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Unlink proxy media."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("unlink_proxy_media", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def replace_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Replace clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("replace_clip", clip_name=arguments["clip_name"], new_file_path=arguments["new_file_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_clip_cache(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set clip cache."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_clip_cache", clip_name=arguments["clip_name"], cache_mode=arguments["cache_mode"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def update_sidecar(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Update sidecar."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("update_sidecar", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_linked_items(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get linked items."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_linked_items", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_audio_tools(registry: ToolRegistry) -> None:
    """Register all audio tools."""
    tools = {
        "get_fairlight_presets": get_fairlight_presets,
        "apply_fairlight_preset": apply_fairlight_preset,
        "insert_audio_at_playhead": insert_audio_at_playhead,
        "get_voice_isolation_state": get_voice_isolation_state,
        "set_voice_isolation_state": set_voice_isolation_state,
        "get_takes": get_takes,
        "add_take": add_take,
        "select_take": select_take,
        "delete_take": delete_take,
        "finalize_take": finalize_take,
        "link_proxy_media": link_proxy_media,
        "unlink_proxy_media": unlink_proxy_media,
        "replace_clip": replace_clip,
        "set_clip_cache": set_clip_cache,
        "update_sidecar": update_sidecar,
        "get_linked_items": get_linked_items,
    }

    for name, handler in tools.items():
        registry.register(name, handler)