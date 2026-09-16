"""
Media pool tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


GET_MEDIA_POOL = create_tool_schema(
    name="get_media_pool",
    description="Get the root media pool folder structure",
    category=ToolCategory.MEDIA,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "object"},
)

GET_MEDIA_POOL_STRUCTURE = create_tool_schema(
    name="get_media_pool_structure",
    description="Get the full media pool folder structure",
    category=ToolCategory.MEDIA,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "object"},
)

NAVIGATE_MEDIA_POOL = create_tool_schema(
    name="navigate_media_pool",
    description="Navigate to a media pool folder",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "folder_path": {"type": "string", "description": "Path to folder (e.g., 'Root/Folder1/Subfolder')"},
    },
    required=["folder_path"],
)

CREATE_MEDIA_POOL_FOLDER = create_tool_schema(
    name="create_media_pool_folder",
    description="Create a new folder in the media pool",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "folder_name": CommonParams.FOLDER_NAME,
        "parent_path": {"type": "string", "description": "Parent folder path (empty for root)"},
    },
    required=["folder_name"],
)

IMPORT_MEDIA = create_tool_schema(
    name="import_media",
    description="Import media files into the media pool",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "file_paths": {"type": "array", "items": {"type": "string"}, "description": "Paths to media files"},
        "folder_path": {"type": "string", "description": "Destination folder path"},
    },
    required=["file_paths"],
)

GET_CLIP_METADATA = create_tool_schema(
    name="get_clip_metadata",
    description="Get metadata for a clip in the media pool",
    category=ToolCategory.MEDIA,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "object"},
)

SET_CLIP_METADATA = create_tool_schema(
    name="set_clip_metadata",
    description="Set metadata for a clip in the media pool",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "metadata": {"type": "object", "description": "Metadata key-value pairs to set"},
    },
    required=["clip_name", "metadata"],
)

GET_CLIP_INFO = create_tool_schema(
    name="get_clip_info",
    description="Get detailed info for a clip",
    category=ToolCategory.MEDIA,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
)

GET_CLIP_PROPERTIES = create_tool_schema(
    name="get_clip_properties",
    description="Get properties for a clip in the media pool",
    category=ToolCategory.MEDIA,
    mode=ToolMode.READ,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
    },
    required=["clip_name"],
    returns={"type": "object"},
)

SET_POOL_CLIP_PROPERTY = create_tool_schema(
    name="set_pool_clip_property",
    description="Set a property on a media pool clip",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "clip_name": CommonParams.CLIP_NAME,
        "property_name": {"type": "string", "description": "Property name"},
        "property_value": {"type": "string", "description": "Property value"},
    },
    required=["clip_name", "property_name", "property_value"],
)

DELETE_MEDIA_POOL_CLIPS = create_tool_schema(
    name="delete_media_pool_clips",
    description="Delete clips from the media pool",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Names of clips to delete"},
    },
    required=["clip_names"],
)

MOVE_MEDIA_POOL_CLIPS = create_tool_schema(
    name="move_media_pool_clips",
    description="Move clips to a different folder in the media pool",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Names of clips to move"},
        "destination_folder": {"type": "string", "description": "Destination folder path"},
    },
    required=["clip_names", "destination_folder"],
)

RELINK_MEDIA_POOL_CLIPS = create_tool_schema(
    name="relink_media_pool_clips",
    description="Relink offline clips to new media files",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Names of clips to relink"},
        "new_paths": {"type": "array", "items": {"type": "string"}, "description": "New file paths for each clip"},
    },
    required=["clip_names", "new_paths"],
)

UNLINK_MEDIA_POOL_CLIPS = create_tool_schema(
    name="unlink_media_pool_clips",
    description="Unlink clips from their media files (make offline)",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "clip_names": {"type": "array", "items": {"type": "string"}, "description": "Names of clips to unlink"},
    },
    required=["clip_names"],
)

AUTO_SYNC_AUDIO = create_tool_schema(
    name="auto_sync_audio",
    description="Auto-sync audio clips with video clips",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "video_clip": CommonParams.CLIP_NAME,
        "audio_clips": {"type": "array", "items": {"type": "string"}, "description": "Audio clips to sync"},
    },
    required=["video_clip", "audio_clips"],
)

IMPORT_TIMELINE_FROM_FILE = create_tool_schema(
    name="import_timeline_from_file",
    description="Import a timeline from a file (AAF, XML, etc.)",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "file_path": {"type": "string", "description": "Path to timeline file"},
        "format": {"type": "string", "description": "File format", "enum": ["aaf", "xml", "fcp"]},
    },
    required=["file_path", "format"],
)

EXPORT_METADATA = create_tool_schema(
    name="export_metadata",
    description="Export project/timeline metadata",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "file_path": {"type": "string", "description": "Output file path"},
        "format": {"type": "string", "description": "Export format", "enum": ["csv", "json", "xml"]},
        "scope": {"type": "string", "description": "What to export", "enum": ["project", "timeline", "clips"]},
    },
    required=["file_path", "format", "scope"],
)

IMPORT_MEDIA_FROM_STORAGE = create_tool_schema(
    name="import_media_from_storage",
    description="Import media from a storage location",
    category=ToolCategory.MEDIA,
    mode=ToolMode.WRITE,
    properties={
        "storage_path": {"type": "string", "description": "Storage volume path"},
        "file_patterns": {"type": "array", "items": {"type": "string"}, "description": "File patterns to match"},
    },
    required=["storage_path"],
)

MEDIA_SCHEMAS = {
    "get_media_pool": GET_MEDIA_POOL,
    "get_media_pool_structure": GET_MEDIA_POOL_STRUCTURE,
    "navigate_media_pool": NAVIGATE_MEDIA_POOL,
    "create_media_pool_folder": CREATE_MEDIA_POOL_FOLDER,
    "import_media": IMPORT_MEDIA,
    "get_clip_metadata": GET_CLIP_METADATA,
    "set_clip_metadata": SET_CLIP_METADATA,
    "get_clip_info": GET_CLIP_INFO,
    "get_clip_properties": GET_CLIP_PROPERTIES,
    "set_pool_clip_property": SET_POOL_CLIP_PROPERTY,
    "delete_media_pool_clips": DELETE_MEDIA_POOL_CLIPS,
    "move_media_pool_clips": MOVE_MEDIA_POOL_CLIPS,
    "relink_media_pool_clips": RELINK_MEDIA_POOL_CLIPS,
    "unlink_media_pool_clips": UNLINK_MEDIA_POOL_CLIPS,
    "auto_sync_audio": AUTO_SYNC_AUDIO,
    "import_timeline_from_file": IMPORT_TIMELINE_FROM_FILE,
    "export_metadata": EXPORT_METADATA,
    "import_media_from_storage": IMPORT_MEDIA_FROM_STORAGE,
}