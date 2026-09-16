"""
Bridge package for DaVinci Resolve MCP.

Provides HTTP transport and client for communicating with the
CursorBridge running inside DaVinci Resolve.
"""

from .protocol import (
    BridgeMethod,
    BridgeRequest,
    BridgeResponse,
    BridgeEndpoints,
    TOOL_TO_ENDPOINT,
    get_endpoint_for_tool,
    is_write_tool,
)
from .transport import HTTPTransport, TransportStats
from .client import BridgeClient, ToolCall, ToolResult

__all__ = [
    "BridgeMethod",
    "BridgeRequest",
    "BridgeResponse",
    "BridgeEndpoints",
    "TOOL_TO_ENDPOINT",
    "get_endpoint_for_tool",
    "is_write_tool",
    "HTTPTransport",
    "TransportStats",
    "BridgeClient",
    "ToolCall",
    "ToolResult",
]