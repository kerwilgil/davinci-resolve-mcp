"""
Tools package for DaVinci Resolve MCP.

Provides tool implementations organized by Resolve domain.
"""

from ..schemas import (
    ToolCategory,
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
        self._handlers: dict[str, callable] = {}
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

    def register(self, name: str, handler: callable) -> None:
        """Register a tool handler."""
        self._handlers[name] = handler

    def get_handler(self, name: str) -> callable | None:
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
            result = await handler(arguments, request_id)
            return result

        except ToolValidationError as e:
            return ToolResult.error_result(e, request_id=request_id)
        except Exception as e:
            return ToolResult.error_result(
                ToolExecutionError(f"Tool execution failed: {e}", tool_name=name, original_error=str(e)),
                request_id=request_id,
            )

    def _validate_arguments(self, name: str, arguments: dict, schema: "ToolSchema") -> None:
        """Validate tool arguments against schema."""
        # Check required fields
        for req in schema.required:
            if req not in arguments:
                raise ToolValidationError(
                    f"Missing required argument: {req}",
                    tool_name=name,
                    field=req,
                )

        # Basic type validation for properties
        props = schema.parameters.get("properties", {})
        for key, value in arguments.items():
            if key in props:
                prop_schema = props[key]
                expected_type = prop_schema.get("type")
                if expected_type and not self._check_type(value, expected_type):
                    raise ToolValidationError(
                        f"Argument '{key}' must be of type {expected_type}",
                        tool_name=name,
                        field=key,
                        value=value,
                    )

                # Check enum values
                if "enum" in prop_schema and value not in prop_schema["enum"]:
                    raise ToolValidationError(
                        f"Argument '{key}' must be one of: {prop_schema['enum']}",
                        tool_name=name,
                        field=key,
                        value=value,
                    )

                # Check minimum/maximum for numbers
                if expected_type in ("integer", "number"):
                    if "minimum" in prop_schema and value < prop_schema["minimum"]:
                        raise ToolValidationError(
                            f"Argument '{key}' must be >= {prop_schema['minimum']}",
                            tool_name=name,
                            field=key,
                            value=value,
                        )
                    if "maximum" in prop_schema and value > prop_schema["maximum"]:
                        raise ToolValidationError(
                            f"Argument '{key}' must be <= {prop_schema['maximum']}",
                            tool_name=name,
                            field=key,
                            value=value,
                        )

    def _check_type(self, value: any, expected_type: str) -> bool:
        """Check if value matches expected JSON schema type."""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        expected = type_map.get(expected_type)
        if expected is None:
            return True
        return isinstance(value, expected)


# Tool handler function signatures
# All handlers must be async functions with signature:
# async def handler(arguments: dict, request_id: str | None = None) -> ToolResult