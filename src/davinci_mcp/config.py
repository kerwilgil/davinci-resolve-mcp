"""
Configuration for DaVinci Resolve MCP server.
"""

from dataclasses import dataclass, field
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

    token: str = field(default="", repr=False)

    def __post_init__(self):
        if self.host not in ("127.0.0.1", "localhost"):
            raise ValueError("Bridge host must be loopback (127.0.0.1 or localhost)")
        if not 1 <= self.port <= 65535 or self.timeout <= 0 or self.max_retries < 0 or self.retry_delay < 0:
            raise ValueError("Invalid bridge connection settings")

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


@dataclass(frozen=True)
class ServerConfig:
    """Configuration for the MCP server."""
    name: str = "davinci-resolve"
    version: str = "1.0.0"
    description: str = "DaVinci Resolve MCP server for structured automation"
    enable_experimental: bool = False


DEFAULT_BRIDGE_CONFIG = BridgeConfig()
DEFAULT_SERVER_CONFIG = ServerConfig()


def get_bridge_config() -> BridgeConfig:
    """Get bridge config from environment or defaults."""
    return BridgeConfig(
        token=os.getenv("DAVINCI_BRIDGE_TOKEN", ""),
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
        enable_experimental=os.getenv("DAVINCI_MCP_ENABLE_EXPERIMENTAL", "").lower() in ("1", "true"),
    )