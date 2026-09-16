"""
Configuration for DaVinci Resolve MCP server.
"""

from dataclasses import dataclass
from typing import Optional
import os


@dataclass(frozen=True)
class BridgeConfig:
    """Configuration for the HTTP bridge connection."""
    host: str = "127.0.0.1"
    port: int = 9876
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


@dataclass(frozen=True)
class ServerConfig:
    """Configuration for the MCP server."""
    name: str = "davinci-resolve"
    version: str = "1.0.0"
    description: str = "DaVinci Resolve MCP server for structured automation"


DEFAULT_BRIDGE_CONFIG = BridgeConfig()
DEFAULT_SERVER_CONFIG = ServerConfig()


def get_bridge_config() -> BridgeConfig:
    """Get bridge config from environment or defaults."""
    return BridgeConfig(
        host=os.getenv("DAVINCI_BRIDGE_HOST", "127.0.0.1"),
        port=int(os.getenv("DAVINCI_BRIDGE_PORT", "9876")),
        timeout=float(os.getenv("DAVINCI_BRIDGE_TIMEOUT", "30.0")),
        max_retries=int(os.getenv("DAVINCI_BRIDGE_MAX_RETRIES", "3")),
        retry_delay=float(os.getenv("DAVINCI_BRIDGE_RETRY_DELAY", "1.0")),
    )


def get_server_config() -> ServerConfig:
    """Get server config from environment or defaults."""
    return ServerConfig(
        name=os.getenv("DAVINCI_MCP_NAME", "davinci-resolve"),
        version=os.getenv("DAVINCI_MCP_VERSION", "1.0.0"),
        description=os.getenv("DAVINCI_MCP_DESCRIPTION", "DaVinci Resolve MCP server for structured automation"),
    )