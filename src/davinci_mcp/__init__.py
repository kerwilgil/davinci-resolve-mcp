"""
DaVinci Resolve MCP - A local-first Model Context Protocol server
for structured DaVinci Resolve automation.
"""

from .server import DaVinciMCPServer, create_server, main
from .config import ServerConfig, BridgeConfig, get_server_config, get_bridge_config
from .schemas import (
    ToolSchema,
    ToolCategory,
    ToolMode,
    VERIFIED_TOOLS,
    get_schema,
    is_verified,
    get_tools_by_category,
    get_write_tools,
    get_read_tools,
)
from .bridge import BridgeClient, ToolCall, ToolResult
from .tools import ToolRegistry
from .errors import DaVinciMCPError, BridgeConnectionError, ToolExecutionError

__version__ = "1.0.0"
__author__ = "Kerwil Gil"
__email__ = "kerwil.gil@up.ac.pa"

__all__ = [
    "DaVinciMCPServer",
    "create_server",
    "main",
    "ServerConfig",
    "BridgeConfig",
    "get_server_config",
    "get_bridge_config",
    "ToolSchema",
    "ToolCategory",
    "ToolMode",
    "VERIFIED_TOOLS",
    "get_schema",
    "is_verified",
    "get_tools_by_category",
    "get_write_tools",
    "get_read_tools",
    "BridgeClient",
    "ToolCall",
    "ToolResult",
    "ToolRegistry",
    "DaVinciMCPError",
    "BridgeConnectionError",
    "ToolExecutionError",
]