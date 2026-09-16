"""
Audio tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


GET_FAIRLIGHT_PRESETS = create_tool_schema(
    name="get_fairlight_presets",
    description="Get available Fairlight presets",
    category=ToolCategory.AUDIO,
    mode=ToolMode.READ,
    properties={
        "preset_type": CommonParams.FAIRLIGHT_PRESET_TYPE,
    },
    returns={"type": "array", "items": {"type": "string"}},
)

APPLY_FAIRLIGHT_PRESET = create_tool_schema(
    name="apply_fairlight_preset",
    description="Apply a Fairlight preset to a track",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "track_index": CommonParams.TRACK_INDEX,
        "preset_name": CommonParams.FAIRLIGHT_PRESET,
        "preset_type": CommonParams.FAIRLIGHT_PRESET_TYPE,
    },
    required=["track_index", "preset_name", "preset_type"],
)

INSERT_AUDIO_AT_PLAYHEAD = create_tool_schema(
    name="insert_audio_at_playhead",
    description="Insert audio at the current playhead position",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "file_path": {"type": "string", "description": "Path to audio file"},
        "track_index": CommonParams.TRACK_INDEX,
    },
    required=["file_path"],
)

GET_VOICE_ISOLATION_STATE = create_tool_schema(
    name="get_voice_isolation_state",
    description="Get voice isolation state for a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "object"},
)

SET_VOICE_ISOLATION_STATE = create_tool_schema(
    name="set_voice_isolation_state",
    description="Set voice isolation state for a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "enabled": {"type": "boolean", "description": "Enable voice isolation"},
        "strength": CommonParams.VOICE_ISOLATION_STRENGTH,
    },
    required=["clip_name", "enabled"],
)

GET_TAKES = create_tool_schema(
    name="get_takes",
    description="Get takes for a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "array", "items": {"type": "object"}},
)

ADD_TAKE = create_tool_schema(
    name="add_take",
    description="Add a take to a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "take_name": {"type": "string", "description": "Take name"},
    },
    required=["clip_name", "take_name"],
)

SELECT_TAKE = create_tool_schema(
    name="select_take",
    description="Select a take for a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "take_number": CommonParams.TAKE_NUMBER,
    },
    required=["clip_name", "take_number"],
)

DELETE_TAKE = create_tool_schema(
    name="delete_take",
    description="Delete a take from a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "take_number": CommonParams.TAKE_NUMBER,
    },
    required=["clip_name", "take_number"],
)

FINALIZE_TAKE = create_tool_schema(
    name="finalize_take",
    description="Finalize a take (make it the active take)",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "take_number": CommonParams.TAKE_NUMBER,
    },
    required=["clip_name", "take_number"],
)

LINK_PROXY_MEDIA = create_tool_schema(
    name="link_proxy_media",
    description="Link proxy media to a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "proxy_path": {"type": "string", "description": "Path to proxy media file"},
    },
    required=["clip_name", "proxy_path"],
)

UNLINK_PROXY_MEDIA = create_tool_schema(
    name="unlink_proxy_media",
    description="Unlink proxy media from a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

REPLACE_CLIP = create_tool_schema(
    name="replace_clip",
    description="Replace a clip with new media",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "new_file_path": {"type": "string", "description": "Path to new media file"},
    },
    required=["clip_name", "new_file_path"],
)

SET_CLIP_CACHE = create_tool_schema(
    name="set_clip_cache",
    description="Set clip cache settings",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "cache_mode": {"type": "string", "description": "Cache mode", "enum": ["none", "proxy", "optimized"]},
    },
    required=["clip_name", "cache_mode"],
)

UPDATE_SIDECAR = create_tool_schema(
    name="update_sidecar",
    description="Update sidecar file for a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

GET_LINKED_ITEMS = create_tool_schema(
    name="get_linked_items",
    description="Get linked items for a clip",
    category=ToolCategory.AUDIO,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "array", "items": {"type": "object"}},
)

AUDIO_SCHEMAS = {
    "get_fairlight_presets": GET_FAIRLIGHT_PRESETS,
    "apply_fairlight_preset": APPLY_FAIRLIGHT_PRESET,
    "insert_audio_at_playhead": INSERT_AUDIO_AT_PLAYHEAD,
    "get_voice_isolation_state": GET_VOICE_ISOLATION_STATE,
    "set_voice_isolation_state": SET_VOICE_ISOLATION_STATE,
    "get_takes": GET_TAKES,
    "add_take": ADD_TAKE,
    "select_take": SELECT_TAKE,
    "delete_take": DELETE_TAKE,
    "finalize_take": FINALIZE_TAKE,
    "link_proxy_media": LINK_PROXY_MEDIA,
    "unlink_proxy_media": UNLINK_PROXY_MEDIA,
    "replace_clip": REPLACE_CLIP,
    "set_clip_cache": SET_CLIP_CACHE,
    "update_sidecar": UPDATE_SIDECAR,
    "get_linked_items": GET_LINKED_ITEMS,
}