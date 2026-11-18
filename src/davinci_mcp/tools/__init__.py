"""
Tools package for DaVinci Resolve MCP.

Provides tool implementations organized by Resolve domain.
"""

from collections.abc import Callable

from jsonschema import Draft202012Validator

from ..schemas import (
    ToolCategory,
    ToolSchema,
    ToolMode,
    VERIFIED_TOOLS,
    get_schema,
    is_verified,
    get_write_tools,
    get_read_tools,
)
from ..bridge import BridgeClient, ToolCall, ToolResult
from ..errors import ToolExecutionError, ToolValidationError, ReadOnlyViolationError


class ToolRegistry:
    """Registry of all available tools with metadata."""

    def __init__(self, client: BridgeClient, read_only: bool = False):
        self.client = client
        self.read_only = read_only
        self._handlers: dict[str, Callable[..., ToolResult]] = {}
        self._register_all_tools()

    def _register_all_tools(self) -> None:
        """Register all tool handlers."""
        # Import and register tools from each module
        from .project import register_project_tools
        from .timeline import register_timeline_tools
        from .media import register_media_tools
        from .clips import register_clips_tools
        from .color import register_color_tools
        from .fusion import register_fusion_tools
        from .audio import register_audio_tools
        from .render import register_render_tools
        from .gallery import register_gallery_tools

        register_project_tools(self)
        register_timeline_tools(self)
        register_media_tools(self)
        register_clips_tools(self)
        register_color_tools(self)
        register_fusion_tools(self)
        register_audio_tools(self)
        register_render_tools(self)
        register_gallery_tools(self)

    def register(self, name: str, handler: Callable[..., ToolResult]) -> None:
        """Register a tool handler."""
        self._handlers[name] = handler

    def get_handler(self, name: str) -> Callable[..., ToolResult] | None:
        """Get a tool handler by name."""
        return self._handlers.get(name)

    def has_tool(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self._handlers

    def list_tools(self) -> list[str]:
        """List all registered tool names."""
        return list(self._handlers.keys())

    def list_verified_tools(self) -> list[str]:
        """List all verified tool names."""
        return [name for name in self._handlers.keys() if is_verified(name)]

    async def execute(self, name: str, arguments: dict, request_id: str | None = None) -> ToolResult:
        """Execute a tool by name."""
        # Check read-only mode for write tools
        if self.read_only:
            from ..schemas import ALL_SCHEMAS
            schema = ALL_SCHEMAS.get(name)
            if schema and schema.mode == ToolMode.WRITE:
                return ToolResult.error_result(
                    ReadOnlyViolationError(name),
                    request_id=request_id,
                )

        handler = self.get_handler(name)
        if not handler:
            return ToolResult.error_result(
                ToolExecutionError(f"Tool not found: {name}", tool_name=name),
                request_id=request_id,
            )

        try:
            # Validate arguments against schema
            schema = get_schema(name)
            if schema:
                self._validate_arguments(name, arguments, schema)

            # Execute handler
            result = await handler({**arguments, "_registry": self}, request_id)
            return result

        except ToolValidationError as e:
            return ToolResult.error_result(e, request_id=request_id)
        except Exception as e:
            return ToolResult.error_result(
                ToolExecutionError("Tool execution failed", tool_name=name),
                request_id=request_id,
            )

    def _validate_arguments(self, name: str, arguments: dict, schema: "ToolSchema") -> None:
        """Validate tool arguments against schema."""
        validator = Draft202012Validator({**schema.parameters, "required": schema.required})
        error = next(validator.iter_errors(arguments), None)
        if error:
            raise ToolValidationError(
                "Arguments do not match the tool schema",
                tool_name=name,
                field=".".join(str(part) for part in error.absolute_path) or None,
            )


# Tool handler function signatures
# All handlers must be async functions with signature:
# async def handler(arguments: dict, request_id: str | None = None) -> ToolResult