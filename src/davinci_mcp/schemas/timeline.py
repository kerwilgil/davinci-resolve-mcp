"""
Timeline tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


# Timeline inspection tools
GET_TIMELINE_INFO = create_tool_schema(
    name="get_timeline_info",
    description="Get information about the current timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.READ,
    properties={
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    returns={
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "frame_rate": {"type": "number"},
            "duration_frames": {"type": "integer"},
            "tracks": {"type": "object"},
            "markers": {"type": "array"},
        },
    },
)

GET_TIMELINE_CLIPS = create_tool_schema(
    name="get_timeline_clips",
    description="Get all clips in the current timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.READ,
    properties={
        "timeline_name": CommonParams.TIMELINE_NAME,
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
    },
    returns={"type": "array", "items": {"type": "object"}},
)

GET_TIMELINE_MARKERS = create_tool_schema(
    name="get_timeline_markers",
    description="Get all markers in the current timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.READ,
    properties={
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    returns={"type": "array", "items": {"type": "object"}},
)

# Timeline modification tools
SET_PLAYHEAD = create_tool_schema(
    name="set_playhead",
    description="Set the playhead position",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "frame": CommonParams.PLAYHEAD_FRAME,
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["frame"],
)

ADD_MARKER = create_tool_schema(
    name="add_marker",
    description="Add a marker to the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "frame": CommonParams.MARKER_FRAME,
        "color": CommonParams.MARKER_COLOR,
        "name": CommonParams.MARKER_NAME,
        "note": CommonParams.MARKER_NOTE,
        "duration": {"type": "integer", "description": "Marker duration in frames", "minimum": 1},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["frame"],
)

DELETE_MARKERS = create_tool_schema(
    name="delete_markers",
    description="Delete markers from the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "frame": {"type": "integer", "description": "Specific frame to delete (omits deletes all)", "minimum": 0},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
)

SWITCH_TIMELINE = create_tool_schema(
    name="switch_timeline",
    description="Switch to a different timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "timeline_name": {"type": "string", "description": "Name of the timeline to switch to"},
    },
    required=["timeline_name"],
)

CREATE_TIMELINE = create_tool_schema(
    name="create_timeline",
    description="Create a new timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "name": {"type": "string", "description": "Timeline name"},
        "frame_rate": {"type": "number", "description": "Frame rate (e.g., 24, 25, 30)"},
        "start_timecode": CommonParams.TIMECODE,
        "video_tracks": {"type": "integer", "description": "Number of video tracks", "minimum": 1, "default": 4},
        "audio_tracks": {"type": "integer", "description": "Number of audio tracks", "minimum": 1, "default": 4},
        "project_name": CommonParams.PROJECT_NAME,
    },
    required=["name", "frame_rate"],
)

RENAME_TIMELINE = create_tool_schema(
    name="rename_timeline",
    description="Rename the current timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "new_name": {"type": "string", "description": "New timeline name"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["new_name"],
)

DUPLICATE_TIMELINE = create_tool_schema(
    name="duplicate_timeline",
    description="Duplicate the current timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "new_name": {"type": "string", "description": "Name for the duplicate"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["new_name"],
)

EXPORT_TIMELINE = create_tool_schema(
    name="export_timeline",
    description="Export timeline to file (AAF, XML, etc.)",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "file_path": {"type": "string", "description": "Output file path"},
        "format": {"type": "string", "description": "Export format", "enum": ["aaf", "xml", "fcp", "drx"]},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["file_path", "format"],
)

SET_TIMELINE_MARK_IN_OUT = create_tool_schema(
    name="set_timeline_mark_in_out",
    description="Set mark in/out points on timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "mark_in": {"type": "integer", "description": "Mark in frame", "minimum": 0},
        "mark_out": {"type": "integer", "description": "Mark out frame", "minimum": 0},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["mark_in", "mark_out"],
)

CLEAR_TIMELINE_MARK_IN_OUT = create_tool_schema(
    name="clear_timeline_mark_in_out",
    description="Clear mark in/out points on timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
)

DELETE_TIMELINE_CLIPS = create_tool_schema(
    name="delete_timeline_clips",
    description="Delete clips from timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Names of clips to delete"},
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["clip_names"],
)

LINK_TIMELINE_CLIPS = create_tool_schema(
    name="link_timeline_clips",
    description="Link video and audio clips in timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Names of clips to link"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["clip_names"],
)

CREATE_COMPOUND_CLIP = create_tool_schema(
    name="create_compound_clip",
    description="Create a compound clip from selected clips",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Names of clips to compound"},
        "name": {"type": "string", "description": "Name for the compound clip"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["clip_names", "name"],
)

CREATE_FUSION_CLIP = create_tool_schema(
    name="create_fusion_clip",
    description="Create a Fusion clip from selected clips",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Names of clips"},
        "name": {"type": "string", "description": "Name for the Fusion clip"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["clip_names", "name"],
)

# Track tools
ADD_TRACK = create_tool_schema(
    name="add_track",
    description="Add a new track to the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["track_type"],
)

DELETE_TRACK = create_tool_schema(
    name="delete_track",
    description="Delete a track from the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["track_type", "track_index"],
)

SET_TRACK_ENABLE = create_tool_schema(
    name="set_track_enable",
    description="Enable or disable a track",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "enabled": {"type": "boolean", "description": "Whether to enable the track"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["track_type", "track_index", "enabled"],
)

SET_TRACK_LOCK = create_tool_schema(
    name="set_track_lock",
    description="Lock or unlock a track",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "locked": {"type": "boolean", "description": "Whether to lock the track"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["track_type", "track_index", "locked"],
)

SET_TRACK_NAME = create_tool_schema(
    name="set_track_name",
    description="Rename a track",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "name": {"type": "string", "description": "New track name"},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["track_type", "track_index", "name"],
)

INSERT_TO_TIMELINE = create_tool_schema(
    name="insert_to_timeline",
    description="Insert a clip at a specific position in the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "frame": {"type": "integer", "description": "Frame position to insert at", "minimum": 0},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["clip_name", "track_type", "track_index", "frame"],
)

APPEND_TO_TIMELINE = create_tool_schema(
    name="append_to_timeline",
    description="Append a clip to the end of a track in the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["clip_name", "track_type", "track_index"],
)

INSERT_TITLE = create_tool_schema(
    name="insert_title",
    description="Insert a title into the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "title_name": {"type": "string", "description": "Title template name"},
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "frame": {"type": "integer", "description": "Frame position", "minimum": 0},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["title_name", "track_type", "track_index", "frame"],
)

INSERT_GENERATOR = create_tool_schema(
    name="insert_generator",
    description="Insert a generator into the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "generator_name": {"type": "string", "description": "Generator name"},
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "frame": {"type": "integer", "description": "Frame position", "minimum": 0},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["generator_name", "track_type", "track_index", "frame"],
)

INSERT_FUSION_COMPOSITION = create_tool_schema(
    name="insert_fusion_composition",
    description="Insert a Fusion composition into the timeline",
    category=ToolCategory.TIMELINE,
    mode=ToolMode.WRITE,
    properties={
        "composition_name": {"type": "string", "description": "Fusion composition name"},
        "track_type": CommonParams.TRACK_TYPE,
        "track_index": CommonParams.TRACK_INDEX,
        "frame": {"type": "integer", "description": "Frame position", "minimum": 0},
        "timeline_name": CommonParams.TIMELINE_NAME,
    },
    required=["composition_name", "track_type", "track_index", "frame"],
)

# Export all schemas
TIMELINE_SCHEMAS = {
    "get_timeline_info": GET_TIMELINE_INFO,
    "get_timeline_clips": GET_TIMELINE_CLIPS,
    "get_timeline_markers": GET_TIMELINE_MARKERS,
    "set_playhead": SET_PLAYHEAD,
    "add_marker": ADD_MARKER,
    "delete_markers": DELETE_MARKERS,
    "switch_timeline": SWITCH_TIMELINE,
    "create_timeline": CREATE_TIMELINE,
    "rename_timeline": RENAME_TIMELINE,
    "duplicate_timeline": DUPLICATE_TIMELINE,
    "export_timeline": EXPORT_TIMELINE,
    "set_timeline_mark_in_out": SET_TIMELINE_MARK_IN_OUT,
    "clear_timeline_mark_in_out": CLEAR_TIMELINE_MARK_IN_OUT,
    "delete_timeline_clips": DELETE_TIMELINE_CLIPS,
    "link_timeline_clips": LINK_TIMELINE_CLIPS,
    "create_compound_clip": CREATE_COMPOUND_CLIP,
    "create_fusion_clip": CREATE_FUSION_CLIP,
    "add_track": ADD_TRACK,
    "delete_track": DELETE_TRACK,
    "set_track_enable": SET_TRACK_ENABLE,
    "set_track_lock": SET_TRACK_LOCK,
    "set_track_name": SET_TRACK_NAME,
    "insert_to_timeline": INSERT_TO_TIMELINE,
    "append_to_timeline": APPEND_TO_TIMELINE,
    "insert_title": INSERT_TITLE,
    "insert_generator": INSERT_GENERATOR,
    "insert_fusion_composition": INSERT_FUSION_COMPOSITION,
}