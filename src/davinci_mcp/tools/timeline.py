"""
Timeline tool implementations.
"""

from ..tools import ToolRegistry
from ..bridge import ToolResult


async def get_timeline_info(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get timeline information."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_timeline_info", timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_timeline_clips(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get timeline clips."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_timeline_clips", timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def get_timeline_markers(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Get timeline markers."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("get_timeline_markers", timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_playhead(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set playhead position."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_playhead", frame=arguments["frame"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def add_marker(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add a marker."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {"frame": arguments["frame"]}
    if "color" in arguments:
        kwargs["color"] = arguments["color"]
    if "name" in arguments:
        kwargs["name"] = arguments["name"]
    if "note" in arguments:
        kwargs["note"] = arguments["note"]
    if "duration" in arguments:
        kwargs["duration"] = arguments["duration"]
    if "timeline_name" in arguments:
        kwargs["timeline_name"] = arguments["timeline_name"]
    result = client.call_tool_simple("add_marker", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_markers(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete markers."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {}
    if "frame" in arguments:
        kwargs["frame"] = arguments["frame"]
    if "timeline_name" in arguments:
        kwargs["timeline_name"] = arguments["timeline_name"]
    result = client.call_tool_simple("delete_markers", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def switch_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Switch timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("switch_timeline", timeline_name=arguments["timeline_name"])
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def create_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Create a new timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {"name": arguments["name"], "frame_rate": arguments["frame_rate"]}
    if "start_timecode" in arguments:
        kwargs["start_timecode"] = arguments["start_timecode"]
    if "video_tracks" in arguments:
        kwargs["video_tracks"] = arguments["video_tracks"]
    if "audio_tracks" in arguments:
        kwargs["audio_tracks"] = arguments["audio_tracks"]
    if "project_name" in arguments:
        kwargs["project_name"] = arguments["project_name"]
    result = client.call_tool_simple("create_timeline", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def rename_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Rename timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("rename_timeline", new_name=arguments["new_name"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def duplicate_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Duplicate timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("duplicate_timeline", new_name=arguments["new_name"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def export_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Export timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("export_timeline", file_path=arguments["file_path"], format=arguments["format"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def insert_to_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Insert a clip at a specific position in the timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {
        "clip_name": arguments["clip_name"],
        "track_type": arguments["track_type"],
        "track_index": arguments["track_index"],
        "frame": arguments["frame"],
    }
    if "timeline_name" in arguments:
        kwargs["timeline_name"] = arguments["timeline_name"]
    result = client.call_tool_simple("insert_to_timeline", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def append_to_timeline(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Append a clip to the end of a track in the timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {
        "clip_name": arguments["clip_name"],
        "track_type": arguments["track_type"],
        "track_index": arguments["track_index"],
    }
    if "timeline_name" in arguments:
        kwargs["timeline_name"] = arguments["timeline_name"]
    result = client.call_tool_simple("append_to_timeline", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def insert_title(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Insert a title into the timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {
        "title_name": arguments["title_name"],
        "track_type": arguments["track_type"],
        "track_index": arguments["track_index"],
        "frame": arguments["frame"],
    }
    if "timeline_name" in arguments:
        kwargs["timeline_name"] = arguments["timeline_name"]
    result = client.call_tool_simple("insert_title", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def insert_generator(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Insert a generator into the timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {
        "generator_name": arguments["generator_name"],
        "track_type": arguments["track_type"],
        "track_index": arguments["track_index"],
        "frame": arguments["frame"],
    }
    if "timeline_name" in arguments:
        kwargs["timeline_name"] = arguments["timeline_name"]
    result = client.call_tool_simple("insert_generator", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def insert_fusion_composition(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Insert a Fusion composition into the timeline."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    kwargs = {
        "composition_name": arguments["composition_name"],
        "track_type": arguments["track_type"],
        "track_index": arguments["track_index"],
        "frame": arguments["frame"],
    }
    if "timeline_name" in arguments:
        kwargs["timeline_name"] = arguments["timeline_name"]
    result = client.call_tool_simple("insert_fusion_composition", **kwargs)
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_timeline_mark_in_out(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set timeline mark in/out."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_timeline_mark_in_out", mark_in=arguments["mark_in"], mark_out=arguments["mark_out"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def clear_timeline_mark_in_out(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Clear timeline mark in/out."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("clear_timeline_mark_in_out", timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_timeline_clips(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete timeline clips."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_timeline_clips", clip_names=arguments["clip_names"], track_type=arguments.get("track_type"), track_index=arguments.get("track_index"), timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def link_timeline_clips(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Link timeline clips."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("link_timeline_clips", clip_names=arguments["clip_names"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def create_compound_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Create compound clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("create_compound_clip", clip_names=arguments["clip_names"], name=arguments["name"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def create_fusion_clip(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Create fusion clip."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("create_fusion_clip", clip_names=arguments["clip_names"], name=arguments["name"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def add_track(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Add track."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("add_track", track_type=arguments["track_type"], track_index=arguments.get("track_index"), timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def delete_track(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Delete track."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("delete_track", track_type=arguments["track_type"], track_index=arguments["track_index"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_track_enable(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set track enable."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_track_enable", track_type=arguments["track_type"], track_index=arguments["track_index"], enabled=arguments["enabled"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_track_lock(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set track lock."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_track_lock", track_type=arguments["track_type"], track_index=arguments["track_index"], locked=arguments["locked"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


async def set_track_name(arguments: dict, request_id: str | None = None) -> ToolResult:
    """Set track name."""
    registry: ToolRegistry = arguments.get("_registry")
    client = registry.client
    result = client.call_tool_simple("set_track_name", track_type=arguments["track_type"], track_index=arguments["track_index"], name=arguments["name"], timeline_name=arguments.get("timeline_name"))
    if result.success:
        return ToolResult.success_result(result.data, request_id)
    return result


def register_timeline_tools(registry: ToolRegistry) -> None:
    """Register all timeline tools."""
    tools = {
        "get_timeline_info": get_timeline_info,
        "get_timeline_clips": get_timeline_clips,
        "get_timeline_markers": get_timeline_markers,
        "set_playhead": set_playhead,
        "add_marker": add_marker,
        "delete_markers": delete_markers,
        "switch_timeline": switch_timeline,
        "create_timeline": create_timeline,
        "rename_timeline": rename_timeline,
        "duplicate_timeline": duplicate_timeline,
        "export_timeline": export_timeline,
        "set_timeline_mark_in_out": set_timeline_mark_in_out,
        "clear_timeline_mark_in_out": clear_timeline_mark_in_out,
        "delete_timeline_clips": delete_timeline_clips,
        "link_timeline_clips": link_timeline_clips,
        "create_compound_clip": create_compound_clip,
        "create_fusion_clip": create_fusion_clip,
        "add_track": add_track,
        "delete_track": delete_track,
        "set_track_enable": set_track_enable,
        "set_track_lock": set_track_lock,
        "set_track_name": set_track_name,
        "insert_to_timeline": insert_to_timeline,
        "append_to_timeline": append_to_timeline,
        "insert_title": insert_title,
        "insert_generator": insert_generator,
        "insert_fusion_composition": insert_fusion_composition,
    }

    for name, handler in tools.items():
        registry.register(name, handler)