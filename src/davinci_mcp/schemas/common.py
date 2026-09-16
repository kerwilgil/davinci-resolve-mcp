"""
Common schema definitions for DaVinci Resolve MCP tools.
"""

from typing import Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum


class ToolCategory(str, Enum):
    """Categories of tools."""
    PROJECT = "project"
    TIMELINE = "timeline"
    MEDIA = "media"
    CLIPS = "clips"
    COLOR = "color"
    FUSION = "fusion"
    AUDIO = "audio"
    RENDER = "render"
    GALLERY = "gallery"


class ToolMode(str, Enum):
    """Tool execution mode."""
    READ = "read"
    WRITE = "write"


@dataclass(frozen=True)
class ToolSchema:
    """Schema definition for a tool."""
    name: str
    description: str
    category: ToolCategory
    mode: ToolMode
    parameters: dict
    required: list[str] = field(default_factory=list)
    returns: Optional[dict] = None
    examples: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class ToolMetadata:
    """Metadata about a registered tool."""
    name: str
    category: ToolCategory
    mode: ToolMode
    handler: str  # Module path to handler function
    schema: ToolSchema
    status: str = "verified"  # verified, experimental, deprecated
    deprecated: bool = False
    replacement: Optional[str] = None


# Common parameter types
class CommonParams:
    """Common parameter definitions reused across tools."""

    PROJECT_NAME = {
        "type": "string",
        "description": "Name of the project (uses current if omitted)",
    }

    TIMELINE_NAME = {
        "type": "string",
        "description": "Name of the timeline (uses current if omitted)",
    }

    CLIP_NAME = {
        "type": "string",
        "description": "Name of the clip",
    }

    MARKER_FRAME = {
        "type": "integer",
        "description": "Frame number for the marker",
        "minimum": 0,
    }

    MARKER_COLOR = {
        "type": "string",
        "description": "Marker color",
        "enum": ["Red", "Green", "Blue", "Cyan", "Magenta", "Yellow", "Black", "White"],
    }

    MARKER_NAME = {
        "type": "string",
        "description": "Marker name/label",
    }

    MARKER_NOTE = {
        "type": "string",
        "description": "Marker note/description",
    }

    TRACK_TYPE = {
        "type": "string",
        "description": "Track type",
        "enum": ["video", "audio", "subtitle"],
    }

    TRACK_INDEX = {
        "type": "integer",
        "description": "Track index (1-based)",
        "minimum": 1,
    }

    RENDER_FORMAT = {
        "type": "string",
        "description": "Render format preset name",
    }

    RENDER_PRESET = {
        "type": "string",
        "description": "Render preset name",
    }

    MEDIA_PATH = {
        "type": "string",
        "description": "File system path to media",
    }

    FOLDER_NAME = {
        "type": "string",
        "description": "Folder name in media pool",
    }

    PAGE_NAME = {
        "type": "string",
        "description": "Page name (media, cut, edit, fusion, color, fairlight, deliver)",
        "enum": ["media", "cut", "edit", "fusion", "color", "fairlight", "deliver"],
    }

    PLAYHEAD_FRAME = {
        "type": "integer",
        "description": "Playhead position in frames",
        "minimum": 0,
    }

    TIMECODE = {
        "type": "string",
        "description": "Timecode in HH:MM:SS:FF format",
        "pattern": r"^\d{2}:\d{2}:\d{2}:\d{2}$",
    }

    NODE_INDEX = {
        "type": "integer",
        "description": "Node index (1-based)",
        "minimum": 1,
    }

    LUT_PATH = {
        "type": "string",
        "description": "Path to LUT file",
    }

    GALLERY_ALBUM = {
        "type": "string",
        "description": "Gallery album name",
    }

    STILL_LABEL = {
        "type": "string",
        "description": "Still label",
    }

    VOICE_ISOLATION_STRENGTH = {
        "type": "number",
        "description": "Voice isolation strength (0.0 to 1.0)",
        "minimum": 0.0,
        "maximum": 1.0,
    }

    FAIRLIGHT_PRESET = {
        "type": "string",
        "description": "Fairlight preset name",
    }

    FAIRLIGHT_PRESET_TYPE = {
        "type": "string",
        "description": "Fairlight preset type",
        "enum": ["track", "bus", "master"],
    }

    TAKE_NUMBER = {
        "type": "integer",
        "description": "Take number",
        "minimum": 1,
    }

    DATABASE_NAME = {
        "type": "string",
        "description": "Database name",
    }

    PROJECT_INDEX = {
        "type": "integer",
        "description": "Project index in database",
        "minimum": 0,
    }


def create_tool_schema(
    name: str,
    description: str,
    category: ToolCategory,
    mode: ToolMode,
    properties: dict,
    required: list[str] = None,
    returns: dict = None,
    examples: list[dict] = None,
) -> ToolSchema:
    """Factory function to create a tool schema."""
    return ToolSchema(
        name=name,
        description=description,
        category=category,
        mode=mode,
        parameters={"type": "object", "properties": properties, "additionalProperties": False},
        required=required or [],
        returns=returns,
        examples=examples or [],
    )