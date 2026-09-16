"""
Structured error types for DaVinci Resolve MCP.
"""

from typing import Any, Optional
from dataclasses import dataclass


class DaVinciMCPError(Exception):
    """Base exception for DaVinci MCP errors."""

    def __init__(
        self,
        message: str,
        code: str = "DAVINCI_MCP_ERROR",
        details: Optional[dict] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def to_dict(self) -> dict:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            }
        }


class BridgeConnectionError(DaVinciMCPError):
    """Raised when the bridge cannot be reached."""

    def __init__(
        self,
        message: str = "Cannot connect to DaVinci Resolve bridge",
        host: str = "127.0.0.1",
        port: int = 9876,
        original_error: Optional[Exception] = None,
    ):
        details = {"host": host, "port": port}
        if original_error:
            details["original_error"] = str(original_error)
        super().__init__(message, "BRIDGE_CONNECTION_ERROR", details)


class BridgeTimeoutError(DaVinciMCPError):
    """Raised when a bridge request times out."""

    def __init__(
        self,
        message: str = "Bridge request timed out",
        timeout: float = 30.0,
        endpoint: str = "",
    ):
        super().__init__(message, "BRIDGE_TIMEOUT_ERROR", {"timeout": timeout, "endpoint": endpoint})


class BridgeResponseError(DaVinciMCPError):
    """Raised when the bridge returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        response_data: Optional[dict] = None,
    ):
        super().__init__(
            message,
            "BRIDGE_RESPONSE_ERROR",
            {"status_code": status_code, "response": response_data},
        )


class ToolValidationError(DaVinciMCPError):
    """Raised when tool arguments fail validation."""

    def __init__(
        self,
        message: str,
        tool_name: str,
        field: Optional[str] = None,
        value: Any = None,
    ):
        details = {"tool": tool_name}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = str(value)
        super().__init__(message, "TOOL_VALIDATION_ERROR", details)


class ToolExecutionError(DaVinciMCPError):
    """Raised when a tool execution fails in DaVinci Resolve."""

    def __init__(
        self,
        message: str,
        tool_name: str,
        original_error: Optional[str] = None,
    ):
        details = {"tool": tool_name}
        if original_error:
            details["original_error"] = original_error
        super().__init__(message, "TOOL_EXECUTION_ERROR", details)


class ReadOnlyViolationError(DaVinciMCPError):
    """Raised when a write operation is attempted in read-only mode."""

    def __init__(self, tool_name: str):
        super().__init__(
            f"Tool '{tool_name}' is a write operation but server is in read-only mode",
            "READ_ONLY_VIOLATION",
            {"tool": tool_name},
        )


@dataclass(frozen=True)
class ErrorResponse:
    """Standardized error response structure."""
    code: str
    message: str
    details: dict

    @classmethod
    def from_exception(cls, exc: DaVinciMCPError) -> "ErrorResponse":
        return cls(exc.code, exc.message, exc.details)

    def to_dict(self) -> dict:
        return {"error": {"code": self.code, "message": self.message, "details": self.details}}