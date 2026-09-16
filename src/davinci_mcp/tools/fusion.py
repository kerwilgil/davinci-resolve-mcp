"""
Fusion tool implementations.
"""

from ..tools import ToolRegistry
from ..bridge import ToolResult


async def get_fusion_comps(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get fusion comps."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_fusion_comps", clip_name=arguments["clip_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def add_fusion_comp_to_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add fusion comp to clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("add_fusion_comp_to_clip", clip_name=arguments["clip_name"], comp_name=arguments["comp_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def import_fusion_comp_to_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Import fusion comp to clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("import_fusion_comp_to_clip", clip_name=arguments["clip_name"], file_path=arguments["file_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def export_fusion_comp_from_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Export fusion comp from clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("export_fusion_comp_from_clip", clip_name=arguments["clip_name"], comp_name=arguments["comp_name"], file_path=arguments["file_path"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_fusion_comp_on_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete fusion comp on clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_fusion_comp_on_clip", clip_name=arguments["clip_name"], comp_name=arguments["comp_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def load_fusion_comp_on_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Load fusion comp on clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("load_fusion_comp_on_clip", clip_name=arguments["clip_name"], comp_name=arguments["comp_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def rename_fusion_comp_on_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Rename fusion comp on clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("rename_fusion_comp_on_clip", clip_name=arguments["clip_name"], old_name=arguments["old_name"], new_name=arguments["new_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def create_magic_mask(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Create magic mask."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("create_magic_mask", clip_name=arguments["clip_name"], strokes=arguments["strokes"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def regenerate_magic_mask(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Regenerate magic mask."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("regenerate_magic_mask", clip_name=arguments["clip_name"], mask_index=arguments["mask_index"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def stabilize_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Stabilize clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("stabilize_clip", clip_name=arguments["clip_name"], mode=arguments.get("mode", "perspective"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def smart_reframe_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Smart reframe clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("smart_reframe_clip", clip_name=arguments["clip_name"], target_aspect=arguments["target_aspect"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_fusion_tools(registry: ToolRegistry) -> None:
    """Register all fusion tools."""
    tools = {
        "get_fusion_comps": get_fusion_comps,
        "add_fusion_comp_to_clip": add_fusion_comp_to_clip,
        "import_fusion_comp_to_clip": import_fusion_comp_to_clip,
        "export_fusion_comp_from_clip": export_fusion_comp_from_clip,
        "delete_fusion_comp_on_clip": delete_fusion_comp_on_clip,
        "load_fusion_comp_on_clip": load_fusion_comp_on_clip,
        "rename_fusion_comp_on_clip": rename_fusion_comp_on_clip,
        "create_magic_mask": create_magic_mask,
        "regenerate_magic_mask": regenerate_magic_mask,
        "stabilize_clip": stabilize_clip,
        "smart_reframe_clip": smart_reframe_clip,
    }

    for name, handler in tools.items():
        registry.register(name, handler)