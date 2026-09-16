"""
Schemas package for DaVinci Resolve MCP.

Provides tool schemas organized by category.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    ToolMetadata,
    CommonParams,
    create_tool_schema,
)
from .timeline import TIMELINE_SCHEMAS
from .media import MEDIA_SCHEMAS
from .clips import CLIP_SCHEMAS
from .color import COLOR_SCHEMAS
from .fusion import FUSION_SCHEMAS
from .audio import AUDIO_SCHEMAS
from .render import RENDER_SCHEMAS
from .gallery import GALLERY_SCHEMAS
from .project import PROJECT_SCHEMAS


# Combined registry of all schemas
ALL_SCHEMAS = {}
ALL_SCHEMAS.update(TIMELINE_SCHEMAS)
ALL_SCHEMAS.update(MEDIA_SCHEMAS)
ALL_SCHEMAS.update(CLIP_SCHEMAS)
ALL_SCHEMAS.update(COLOR_SCHEMAS)
ALL_SCHEMAS.update(FUSION_SCHEMAS)
ALL_SCHEMAS.update(AUDIO_SCHEMAS)
ALL_SCHEMAS.update(RENDER_SCHEMAS)
ALL_SCHEMAS.update(GALLERY_SCHEMAS)
ALL_SCHEMAS.update(PROJECT_SCHEMAS)


# Verified tools (subset that has been tested against real DaVinci Resolve)
VERIFIED_TOOLS = [
    "get_resolve_status",
    "get_project_info",
    "get_current_page",
    "get_timeline_info",
    "get_timeline_clips",
    "get_timeline_markers",
    "get_render_settings",
    "get_media_pool",
    "get_clip_properties",
    "open_page",
    "set_playhead",
    "add_marker",
    "delete_markers",
    "switch_timeline",
    "create_timeline",
    "rename_timeline",
    "duplicate_timeline",
    "add_track",
    "delete_track",
    "set_track_enable",
    "set_track_lock",
    "set_track_name",
    "import_media",
    "append_to_timeline",
    "insert_to_timeline",
    "set_clip_color",
    "set_clip_enabled",
    "set_clip_properties",
    "insert_title",
    "insert_generator",
    "insert_fusion_composition",
    "set_render_settings",
    "set_render_format",
    "get_render_formats",
    "add_render_job",
    "start_rendering",
    "stop_rendering",
    "delete_render_job",
    "save_project",
    "set_project_setting",
    "set_timeline_setting",
    "export_current_frame",
    "create_subtitles_from_audio",
    "detect_scene_cuts",
    "get_media_pool_structure",
    "navigate_media_pool",
    "create_media_pool_folder",
    "get_clip_metadata",
    "set_clip_metadata",
    "get_clip_info",
    "set_pool_clip_property",
    "delete_media_pool_clips",
    "move_media_pool_clips",
    "relink_media_pool_clips",
    "unlink_media_pool_clips",
    "auto_sync_audio",
    "import_timeline_from_file",
    "export_metadata",
    "import_media_from_storage",
    "add_clip_marker",
    "get_clip_markers",
    "delete_clip_markers",
    "add_clip_flag",
    "get_clip_flags",
    "clear_clip_flags",
    "delete_timeline_clips",
    "link_timeline_clips",
    "create_compound_clip",
    "create_fusion_clip",
    "get_current_video_item",
    "get_clip_thumbnail",
    "export_timeline",
    "get_gallery_albums",
    "get_album_stills",
    "set_current_album",
    "create_gallery_album",
    "grab_still",
    "grab_all_stills",
    "export_stills",
    "import_stills",
    "delete_stills",
    "set_still_label",
    "get_node_graph",
    "set_lut",
    "get_lut",
    "set_node_enabled",
    "apply_grade_from_drx",
    "reset_all_grades",
    "apply_arri_cdl_lut",
    "set_cdl",
    "export_lut",
    "copy_grades",
    "reset_node_colors",
    "get_color_versions",
    "add_color_version",
    "load_color_version",
    "delete_color_version",
    "rename_color_version",
    "get_color_groups",
    "add_color_group",
    "delete_color_group",
    "assign_to_color_group",
    "remove_from_color_group",
    "get_fusion_comps",
    "add_fusion_comp_to_clip",
    "import_fusion_comp_to_clip",
    "export_fusion_comp_from_clip",
    "delete_fusion_comp_on_clip",
    "load_fusion_comp_on_clip",
    "rename_fusion_comp_on_clip",
    "create_magic_mask",
    "regenerate_magic_mask",
    "stabilize_clip",
    "smart_reframe_clip",
    "get_fairlight_presets",
    "apply_fairlight_preset",
    "insert_audio_at_playhead",
    "get_voice_isolation_state",
    "set_voice_isolation_state",
    "get_takes",
    "add_take",
    "select_take",
    "delete_take",
    "finalize_take",
    "link_proxy_media",
    "unlink_proxy_media",
    "replace_clip",
    "set_clip_cache",
    "update_sidecar",
    "get_linked_items",
    "set_timeline_mark_in_out",
    "clear_timeline_mark_in_out",
    "get_project_list",
    "get_database_list",
    "load_project",
    "create_project",
    "delete_project",
    "archive_project",
    "export_project",
    "import_project",
    "navigate_project_folder",
    "set_database",
    "layout_preset",
    "render_preset",
    "burnin_preset",
    "get_keyframe_mode",
    "set_keyframe_mode",
    "get_render_job_status",
    "get_render_resolutions",
    "get_quick_export_presets",
    "quick_export",
    "set_render_mode",
    "refresh_lut_list",
    "get_media_storage",
    "reveal_in_storage",
    "voice_isolate",
    "voice_isolate_timeline",
    "remove_background",
    "remove_background_video",
    "remove_background_clip",
    "transcribe_timeline",
    "transcribe_file",
]


def get_schema(name: str) -> ToolSchema | None:
    """Get a tool schema by name."""
    return ALL_SCHEMAS.get(name)


def is_verified(name: str) -> bool:
    """Check if a tool is verified."""
    return name in VERIFIED_TOOLS


def get_tools_by_category(category: ToolCategory) -> list[str]:
    """Get all tool names in a category."""
    return [name for name, schema in ALL_SCHEMAS.items() if schema.category == category]


def get_write_tools() -> list[str]:
    """Get all write tool names."""
    return [name for name, schema in ALL_SCHEMAS.items() if schema.mode == ToolMode.WRITE]


def get_read_tools() -> list[str]:
    """Get all read tool names."""
    return [name for name, schema in ALL_SCHEMAS.items() if schema.mode == ToolMode.READ]


__all__ = [
    "ToolSchema",
    "ToolCategory",
    "ToolMode",
    "ToolMetadata",
    "CommonParams",
    "create_tool_schema",
    "ALL_SCHEMAS",
    "VERIFIED_TOOLS",
    "TIMELINE_SCHEMAS",
    "MEDIA_SCHEMAS",
    "CLIP_SCHEMAS",
    "COLOR_SCHEMAS",
    "FUSION_SCHEMAS",
    "AUDIO_SCHEMAS",
    "RENDER_SCHEMAS",
    "GALLERY_SCHEMAS",
    "PROJECT_SCHEMAS",
    "get_schema",
    "is_verified",
    "get_tools_by_category",
    "get_write_tools",
    "get_read_tools",
]