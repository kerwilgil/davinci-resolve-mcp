"""
Main MCP server for DaVinci Resolve.

This is the entry point for the MCP server that exposes DaVinci Resolve
tools through the Model Context Protocol.
"""

import asyncio
import logging
import sys
from typing import Any

import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, TextContent, Tool

from .availability import EXPERIMENTAL_TOOLS, SUPPORTED_TOOLS, UNAVAILABLE_TOOLS
from .config import ServerConfig, get_server_config, get_bridge_config
from .bridge import BridgeClient
from .errors import DaVinciMCPError
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

        self.mcp = Server(self.server_config.name, version=self.server_config.version)
        self.bridge_client = BridgeClient(self.bridge_config)
        self.tool_registry = ToolRegistry(self.bridge_client, read_only=read_only)

        self.exposed_tools = SUPPORTED_TOOLS
        if self.server_config.enable_experimental:
            self.exposed_tools = self.exposed_tools | EXPERIMENTAL_TOOLS
        self._register_mcp_tools()

    def _register_mcp_tools(self) -> None:
        """Register all tools with the MCP server."""
        from .schemas import get_schema

        @self.mcp.list_tools()
        async def list_tools():
            return [
                Tool(name=name, description=(
                    "EXPERIMENTAL: " if name in EXPERIMENTAL_TOOLS else ""
                ) + get_schema(name).description,
                     inputSchema={**get_schema(name).parameters,
                                  "required": get_schema(name).required})
                for name in self.get_tool_list()
            ]

        @self.mcp.call_tool(validate_input=False)
        async def call_tool(name, arguments):
            if name in UNAVAILABLE_TOOLS:
                error = DaVinciMCPError("This tool has no bridge implementation", "TOOL_UNAVAILABLE")
            elif name in EXPERIMENTAL_TOOLS and name not in self.exposed_tools:
                error = DaVinciMCPError("Experimental tool is disabled", "TOOL_EXPERIMENTAL_DISABLED")
            else:
                error = None
            if error is not None:
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(error.to_dict()))],
                    isError=True,
                )
            result = await self.tool_registry.execute(name, arguments or {})
            data = result.data if result.success else result.error.to_dict()
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(data))],
                isError=not result.success,
            )

    def get_tool_list(self) -> list[str]:
        """Get list of all registered tools."""
        return [name for name in self.tool_registry.list_tools() if name in self.exposed_tools]

    def get_verified_tools(self) -> list[str]:
        """Get list of verified tools."""
        return [name for name in self.get_tool_list() if name in SUPPORTED_TOOLS]

    def get_write_tools(self) -> list[str]:
        """Get list of write tools."""
        return [name for name in self.get_tool_list()
                if name in get_write_tools()]

    def get_read_tools(self) -> list[str]:
        """Get list of read tools."""
        return [name for name in self.get_tool_list()
                if name in get_read_tools()]

    def get_tools_by_category(self, category: ToolCategory) -> list[str]:
        """Get tools by category."""
        from .schemas import get_tools_by_category
        return [name for name in get_tools_by_category(category)
                if name in self.exposed_tools and self.tool_registry.has_tool(name)]

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
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            try:
                await server.mcp.run(read_stream, write_stream, server.mcp.create_initialization_options())
            finally:
                await server.close()

    asyncio.run(run())


if __name__ == "__main__":
    main()