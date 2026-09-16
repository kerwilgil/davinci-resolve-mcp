"""
Main MCP server for DaVinci Resolve.

This is the entry point for the MCP server that exposes DaVinci Resolve
tools through the Model Context Protocol.
"""

import asyncio
import logging
import sys
from typing import Any

from mcp.server.fastmcp import FastMCP

from .config import ServerConfig, get_server_config, get_bridge_config
from .bridge import BridgeClient
from .tools import ToolRegistry
from .schemas import VERIFIED_TOOLS, get_write_tools, get_read_tools, ToolCategory

logger = logging.getLogger(__name__)


class DaVinciMCPServer:
    """DaVinci Resolve MCP Server."""

    def __init__(
        self,
        server_config: ServerConfig | None = None,
        bridge_config: Any | None = None,
        read_only: bool = False,
    ):
        self.server_config = server_config or get_server_config()
        self.bridge_config = bridge_config or get_bridge_config()
        self.read_only = read_only

        self.mcp = FastMCP(self.server_config.name)
        self.bridge_client = BridgeClient(self.bridge_config)
        self.tool_registry = ToolRegistry(self.bridge_client, read_only=read_only)

        self._register_mcp_tools()

    def _register_mcp_tools(self) -> None:
        """Register all tools with the MCP server."""
        for tool_name in self.tool_registry.list_tools():
            schema = self.tool_registry._handlers.get(tool_name)
            if schema:
                self._register_tool(tool_name)

    def _register_tool(self, name: str) -> None:
        """Register a single tool with the MCP server."""
        handler = self.tool_registry.get_handler(name)

        @self.mcp.tool(name=name)
        async def tool_wrapper(**kwargs) -> dict:
            # Add registry reference for handler
            kwargs["_registry"] = self.tool_registry
            result = await self.tool_registry.execute(name, kwargs)
            if result.success:
                return result.data
            else:
                # Return structured error for MCP
                return result.error.to_dict() if result.error else {"error": "Unknown error"}

    def get_tool_list(self) -> list[str]:
        """Get list of all registered tools."""
        return self.tool_registry.list_tools()

    def get_verified_tools(self) -> list[str]:
        """Get list of verified tools."""
        return self.tool_registry.list_verified_tools()

    def get_write_tools(self) -> list[str]:
        """Get list of write tools."""
        return [name for name in self.tool_registry.list_tools()
                if name in get_write_tools()]

    def get_read_tools(self) -> list[str]:
        """Get list of read tools."""
        return [name for name in self.tool_registry.list_tools()
                if name in get_read_tools()]

    def get_tools_by_category(self, category: ToolCategory) -> list[str]:
        """Get tools by category."""
        from .schemas import get_tools_by_category
        return [name for name in get_tools_by_category(category)
                if self.tool_registry.has_tool(name)]

    async def connect(self) -> bool:
        """Connect to the bridge."""
        return self.bridge_client.connect()

    async def close(self) -> None:
        """Close connections."""
        self.bridge_client.close()

    async def __aenter__(self) -> "DaVinciMCPServer":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


def create_server(
    server_config: ServerConfig | None = None,
    bridge_config: Any | None = None,
    read_only: bool = False,
) -> DaVinciMCPServer:
    """Create a DaVinci MCP server instance."""
    return DaVinciMCPServer(server_config, bridge_config, read_only)


def main() -> None:
    """Main entry point for the MCP server."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )

    logger.info("Starting DaVinci Resolve MCP Server")

    # Create server
    server = create_server()

    # Run the MCP server (this blocks)
    server.mcp.run()


if __name__ == "__main__":
    main()