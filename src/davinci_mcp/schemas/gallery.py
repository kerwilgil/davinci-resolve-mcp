"""
Gallery tool schemas.
"""

from .common import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    CommonParams,
    create_tool_schema,
)


GET_GALLERY_ALBUMS = create_tool_schema(
    name="get_gallery_albums",
    description="Get all gallery albums",
    category=ToolCategory.GALLERY,
    mode=ToolMode.READ,
    properties={},
    returns={"type": "array", "items": {"type": "object"}},
)

GET_ALBUM_STILLS = create_tool_schema(
    name="get_album_stills",
    description="Get stills in a gallery album",
    category=ToolCategory.GALLERY,
    mode=ToolMode.READ,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
    },
    required=["album_name"],
    returns={"type": "array", "items": {"type": "object"}},
)

SET_CURRENT_ALBUM = create_tool_schema(
    name="set_current_album",
    description="Set the current gallery album",
    category=ToolCategory.GALLERY,
    mode=ToolMode.WRITE,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
    },
    required=["album_name"],
)

CREATE_GALLERY_ALBUM = create_tool_schema(
    name="create_gallery_album",
    description="Create a new gallery album",
    category=ToolCategory.GALLERY,
    mode=ToolMode.WRITE,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
    },
    required=["album_name"],
)

GRAB_STILL = create_tool_schema(
    name="grab_still",
    description="Grab a still from the current frame",
    category=ToolCategory.GALLERY,
    mode=ToolMode.WRITE,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
        "label": CommonParams.STILL_LABEL,
    },
    required=["album_name"],
)

GRAB_ALL_STILLS = create_tool_schema(
    name="grab_all_stills",
    description="Grab stills from all clips in timeline",
    category=ToolCategory.GALLERY,
    mode=ToolMode.WRITE,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
    },
    required=["album_name"],
)

EXPORT_STILLS = create_tool_schema(
    name="export_stills",
    description="Export stills from gallery",
    category=ToolCategory.GALLERY,
    mode=ToolMode.WRITE,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
        "output_folder": {"type": "string", "description": "Output folder path"},
        "format": {"type": "string", "description": "Image format", "enum": ["png", "jpg", "tiff", "exr"]},
    },
    required=["album_name", "output_folder"],
)

IMPORT_STILLS = create_tool_schema(
    name="import_stills",
    description="Import stills into gallery",
    category=ToolCategory.GALLERY,
    mode=ToolMode.WRITE,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
        "file_paths": {"type": "array", "items": {"type": "string"}, "description": "Still file paths"},
    },
    required=["album_name", "file_paths"],
)

DELETE_STILLS = create_tool_schema(
    name="delete_stills",
    description="Delete stills from gallery",
    category=ToolCategory.GALLERY,
    mode=ToolMode.WRITE,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
        "still_labels": {"type": "array", "items": {"type": "string"}, "description": "Still labels to delete"},
    },
    required=["album_name", "still_labels"],
)

SET_STILL_LABEL = create_tool_schema(
    name="set_still_label",
    description="Set label on a still",
    category=ToolCategory.GALLERY,
    mode=ToolMode.WRITE,
    properties={
        "album_name": CommonParams.GALLERY_ALBUM,
        "still_label": CommonParams.STILL_LABEL,
        "new_label": {"type": "string", "description": "New label"},
    },
    required=["album_name", "still_label", "new_label"],
)

GALLERY_SCHEMAS = {
    "get_gallery_albums": GET_GALLERY_ALBUMS,
    "get_album_stills": GET_ALBUM_STILLS,
    "set_current_album": SET_CURRENT_ALBUM,
    "create_gallery_album": CREATE_GALLERY_ALBUM,
    "grab_still": GRAB_STILL,
    "grab_all_stills": GRAB_ALL_STILLS,
    "export_stills": EXPORT_STILLS,
    "import_stills": IMPORT_STILLS,
    "delete_stills": DELETE_STILLS,
    "set_still_label": SET_STILL_LABEL,
}