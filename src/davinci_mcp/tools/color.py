"""
Color tool implementations.
"""

from ..tools import ToolRegistry
from ..bridge import ToolResult


async def get_node_graph(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get node graph."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_node_graph", clip_name=arguments.get("clip_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_lut(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set LUT."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_lut", clip_name=arguments["clip_name"], node_index=arguments["node_index"], lut_path=arguments["lut_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_lut(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get LUT."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_lut", clip_name=arguments["clip_name"], node_index=arguments["node_index"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_node_enabled(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set node enabled."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_node_enabled", clip_name=arguments["clip_name"], node_index=arguments["node_index"], enabled=arguments["enabled"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def apply_grade_from_drx(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Apply grade from DRX."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("apply_grade_from_drx", clip_name=arguments["clip_name"], drx_path=arguments["drx_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def reset_all_grades(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Reset all grades."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("reset_all_grades", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def apply_arri_cdl_lut(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Apply ARRI CDL LUT."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("apply_arri_cdl_lut", clip_name=arguments["clip_name"], slope=arguments["slope"], offset=arguments["offset"], power=arguments["power"], saturation=arguments["saturation"], lut_path=arguments.get("lut_path"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_cdl(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set CDL."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_cdl", clip_name=arguments["clip_name"], node_index=arguments["node_index"], slope=arguments["slope"], offset=arguments["offset"], power=arguments["power"], saturation=arguments["saturation"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def export_lut(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Export LUT."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("export_lut", clip_name=arguments["clip_name"], output_path=arguments["output_path"], format=arguments.get("format", "cube"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def copy_grades(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Copy grades."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("copy_grades", source_clip=arguments["source_clip"], target_clips=arguments["target_clips"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def reset_node_colors(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Reset node colors."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("reset_node_colors", clip_name=arguments["clip_name"], node_index=arguments["node_index"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_color_versions(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get color versions."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_color_versions", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def add_color_version(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add color version."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("add_color_version", clip_name=arguments["clip_name"], name=arguments["name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def load_color_version(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Load color version."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("load_color_version", clip_name=arguments["clip_name"], version_name=arguments["version_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_color_version(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete color version."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_color_version", clip_name=arguments["clip_name"], version_name=arguments["version_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def rename_color_version(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Rename color version."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("rename_color_version", clip_name=arguments["clip_name"], old_name=arguments["old_name"], new_name=arguments["new_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_color_groups(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get color groups."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_color_groups")
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def add_color_group(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add color group."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("add_color_group", name=arguments["name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_color_group(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete color group."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_color_group", group_name=arguments["group_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def assign_to_color_group(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Assign to color group."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("assign_to_color_group", group_name=arguments["group_name"], clip_names=arguments["clip_names"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def remove_from_color_group(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Remove from color group."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("remove_from_color_group", group_name=arguments["group_name"], clip_names=arguments["clip_names"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_color_tools(registry: ToolRegistry) -> None:
    """Register all color tools."""
    tools = {
        "get_node_graph": get_node_graph,
        "set_lut": set_lut,
        "get_lut": get_lut,
        "set_node_enabled": set_node_enabled,
        "apply_grade_from_drx": apply_grade_from_drx,
        "reset_all_grades": reset_all_grades,
        "apply_arri_cdl_lut": apply_arri_cdl_lut,
        "set_cdl": set_cdl,
        "export_lut": export_lut,
        "copy_grades": copy_grades,
        "reset_node_colors": reset_node_colors,
        "get_color_versions": get_color_versions,
        "add_color_version": add_color_version,
        "load_color_version": load_color_version,
        "delete_color_version": delete_color_version,
        "rename_color_version": rename_color_version,
        "get_color_groups": get_color_groups,
        "add_color_group": add_color_group,
        "delete_color_group": delete_color_group,
        "assign_to_color_group": assign_to_color_group,
        "remove_from_color_group": remove_from_color_group,
    }

    for name, handler in tools.items():
        registry.register(name, handler)