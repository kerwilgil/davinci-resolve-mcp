"""Tool exposure policy for the 1.0 release."""

from .bridge.protocol import UNAVAILABLE_TOOLS
from .schemas import ALL_SCHEMAS

# This scope has controlled contract coverage against the documented Resolve API.
SUPPORTED_TOOLS = frozenset({
    "get_resolve_status", "get_project_info", "get_current_page", "open_page",
    "get_timeline_info", "get_timeline_clips", "set_playhead", "create_timeline",
    "import_media", "insert_to_timeline", "delete_timeline_clips",
    "link_timeline_clips", "create_compound_clip", "create_fusion_clip",
    "export_timeline", "export_current_frame",
    "get_render_settings", "start_rendering", "delete_render_job",
    "get_render_job_status", "set_render_mode",
    "get_gallery_albums", "get_album_stills", "set_current_album", "delete_stills",
    "set_still_label", "get_database_list", "create_project", "load_project",
    "delete_project", "set_database", "select_take", "delete_take", "finalize_take",
    "export_fusion_comp_from_clip", "set_clip_cache",
})
EXPERIMENTAL_TOOLS = ALL_SCHEMAS.keys() - SUPPORTED_TOOLS - UNAVAILABLE_TOOLS
