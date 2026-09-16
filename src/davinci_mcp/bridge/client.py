"""
High-level client for the DaVinci Resolve bridge.
"""

from typing import Any, Optional, Dict
from dataclasses import dataclass

from ..config import BridgeConfig, get_bridge_config
from ..errors import (
    BridgeConnectionError,
    BridgeResponseError,
    ToolExecutionError,
    DaVinciMCPError,
)
from .protocol import BridgeMethod, BridgeRequest, get_endpoint_for_tool, is_write_tool
from .transport import HTTPTransport, TransportStats


@dataclass
class ToolCall:
    """A tool call request."""
    name: str
    arguments: Dict[str, Any]
    request_id: Optional[str] = None


@dataclass
class ToolResult:
    """A tool call result."""
    success: bool
    data: Any = None
    error: Optional[DaVinciMCPError] = None
    request_id: Optional[str] = None

    @classmethod
    def success_result(cls, data: Any, request_id: Optional[str] = None) -> "ToolResult":
        return cls(success=True, data=data, request_id=request_id)

    @classmethod
    def error_result(cls, error: DaVinciMCPError, request_id: Optional[str] = None) -> "ToolResult":
        return cls(success=False, error=error, request_id=request_id)


class BridgeClient:
    """Client for communicating with the DaVinci Resolve HTTP bridge."""

    def __init__(self, config: Optional[BridgeConfig] = None, transport: Optional[HTTPTransport] = None):
        self.config = config or get_bridge_config()
        self.transport = transport or HTTPTransport(self.config)
        self._connected = False

    def connect(self) -> bool:
        """Establish connection to the bridge."""
        self._connected = self.transport.health_check()
        return self._connected

    @property
    def is_connected(self) -> bool:
        return self._connected

    def call_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call via the bridge."""
        if not self._connected:
            if not self.connect():
                return ToolResult.error_result(
                    BridgeConnectionError(
                        "Bridge not connected",
                        host=self.config.host,
                        port=self.config.port,
                    ),
                    request_id=tool_call.request_id,
                )

        try:
            method, endpoint = get_endpoint_for_tool(tool_call.name)
        except ValueError as e:
            return ToolResult.error_result(
                ToolExecutionError(
                    f"Unknown tool: {tool_call.name}",
                    tool_name=tool_call.name,
                    original_error=str(e),
                ),
                request_id=tool_call.request_id,
            )

        # Build request
        bridge_request = BridgeRequest(
            method=method,
            path=endpoint,
            params={},
            body=tool_call.arguments if method == BridgeMethod.POST else None,
            request_id=tool_call.request_id,
        )

        # For GET requests, put arguments in query params
        if method == BridgeMethod.GET:
            bridge_request.params = tool_call.arguments
            bridge_request.body = None

        try:
            response = self.transport.send(bridge_request)

            if response.is_success:
                return ToolResult.success_result(response.data, tool_call.request_id)
            else:
                error_data = response.data if isinstance(response.data, dict) else {"message": str(response.data)}
                return ToolResult.error_result(
                    BridgeResponseError(
                        error_data.get("message", f"Bridge error: HTTP {response.status_code}"),
                        status_code=response.status_code,
                        response_data=error_data,
                    ),
                    tool_call.request_id,
                )

        except DaVinciMCPError as e:
            return ToolResult.error_result(e, tool_call.request_id)

    def call_tool_simple(self, name: str, **kwargs) -> ToolResult:
        """Convenience method for simple tool calls."""
        return self.call_tool(ToolCall(name=name, arguments=kwargs))

    def get_stats(self) -> TransportStats:
        """Get transport statistics."""
        return self.transport.stats

    def close(self) -> None:
        """Close the client connection."""
        self.transport.close()
        self._connected = False

    def __enter__(self) -> "BridgeClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()