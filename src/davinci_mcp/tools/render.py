"""
Render tool implementations.
"""

from ..tools import ToolRegistry
from ..bridge import ToolResult


async def get_render_settings(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get render settings."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_render_settings")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_render_settings(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set render settings."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_render_settings", settings=arguments["settings"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_render_format(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set render format."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_render_format", format=arguments["format"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_render_formats(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get render formats."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_render_formats")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def add_render_job(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add render job."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("add_render_job", preset=arguments["preset"], output_path=arguments["output_path"], timeline_name=arguments.get("timeline_name"), render_range=arguments.get("render_range", "full"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def start_rendering(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Start rendering."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("start_rendering", wait_for_completion=arguments.get("wait_for_completion", False))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def stop_rendering(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Stop rendering."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("stop_rendering")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_render_job(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete render job."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_render_job", job_index=arguments["job_index"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_render_job_status(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get render job status."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_render_job_status", job_index=arguments["job_index"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_render_resolutions(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get render resolutions."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_render_resolutions")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_quick_export_presets(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get quick export presets."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_quick_export_presets")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def quick_export(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Quick export."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("quick_export", preset=arguments["preset"], output_path=arguments["output_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_render_mode(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set render mode."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_render_mode", mode=arguments["mode"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_render_tools(registry: ToolRegistry) -> None:
    """Register all render tools."""
    tools = {
        "get_render_settings": get_render_settings,
        "set_render_settings": set_render_settings,
        "set_render_format": set_render_format,
        "get_render_formats": get_render_formats,
        "add_render_job": add_render_job,
        "start_rendering": start_rendering,
        "stop_rendering": stop_rendering,
        "delete_render_job": delete_render_job,
        "get_render_job_status": get_render_job_status,
        "get_render_resolutions": get_render_resolutions,
        "get_quick_export_presets": get_quick_export_presets,
        "quick_export": quick_export,
        "set_render_mode": set_render_mode,
    }

    for name, handler in tools.items():
        registry.register(name, handler)