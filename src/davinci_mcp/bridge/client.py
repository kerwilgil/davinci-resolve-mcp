"""
High-level client for the DaVinci Resolve bridge.
"""

import time

from typing import Any, Optional, Dict
from dataclasses import dataclass

from ..config import BridgeConfig, get_bridge_config
from ..errors import (
    BridgeConnectionError,
    BridgeOutcomeUnknownError,
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
        from .protocol import UNAVAILABLE_TOOLS
        if tool_call.name in UNAVAILABLE_TOOLS:
            return ToolResult.error_result(
                DaVinciMCPError("This tool has no bridge implementation", "TOOL_UNAVAILABLE"),
                tool_call.request_id,
            )
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

        arguments = {key: value for key, value in tool_call.arguments.items() if value is not None}
        wait_timeout = None
        if tool_call.name == "start_rendering":
            wait = arguments.pop("wait_for_completion", False)
            timeout = arguments.pop("completion_timeout", None)
            if type(wait) is not bool or (timeout is not None and (
                    not wait or type(timeout) not in (int, float) or not 0.1 <= timeout <= 600)):
                return ToolResult.error_result(
                    DaVinciMCPError("completion_timeout requires waiting and must be 0.1–600 seconds",
                                    "TOOL_VALIDATION_ERROR"), tool_call.request_id)
            if wait:
                wait_timeout = 30 if timeout is None else timeout
        if method == BridgeMethod.POST:
            # Resolve's bridge uses camelCase for mutation bodies.
            arguments = {
                key.split("_")[0] + "".join(part.title() for part in key.split("_")[1:]): value
                for key, value in arguments.items()
            }
            aliases = {
                "rename_timeline": {"newName": "name"},
                "duplicate_timeline": {"newName": "name"},
                "set_track_name": {"trackName": "name"},
                "import_media": {"paths": "filePaths"},
                "import_media_from_storage": {"paths": "filePaths"},
                "add_marker": {"frame": "frameId"},
                "delete_markers": {"frame": "frameId"},
                "insert_to_timeline": {"frame": "recordFrame"},
                "add_clip_marker": {"frame": "frameId"},
                "delete_clip_markers": {"frame": "frameId"},
                "add_clip_flag": {"flag": "color"},
                "create_gallery_album": {"albumName": "name"},
                "export_stills": {"outputFolder": "folderPath"},
                "archive_project": {"archivePath": "filePath"},
                "import_fusion_comp_to_clip": {"filePath": "path"},
                "export_fusion_comp_from_clip": {"filePath": "path"},
                "add_take": {"takeName": "mediaPoolClipName"},
                "select_take": {"takeNumber": "takeIndex"},
                "delete_take": {"takeNumber": "takeIndex"},
                "finalize_take": {"takeNumber": "takeIndex"},
                "export_timeline": {"filePath": "fileName", "format": "exportType"},
            }
            for source, target in aliases.get(tool_call.name, {}).items():
                if source in arguments:
                    arguments[target] = arguments.pop(source)

        if tool_call.name == "export_timeline":
            formats = {"aaf": "AAF", "xml": "FCP_7_XML", "fcp": "FCPXML_1_10",
                       "drt": "DRT", "edl": "EDL", "otio": "OTIO"}
            arguments["exportType"] = formats.get(arguments.get("exportType"), arguments.get("exportType"))
        if tool_call.name == "set_clip_cache" and "cacheMode" in arguments:
            modes = {"enabled": 1, "disabled": 0, "auto": -1}
            mode = arguments.pop("cacheMode")
            if mode not in modes:
                return ToolResult.error_result(
                    DaVinciMCPError("Proxy and optimized media are separate from Resolve output cache",
                                    "TOOL_VALIDATION_ERROR"), tool_call.request_id)
            arguments["cacheValue"] = modes[mode]

        if tool_call.name == "insert_to_timeline":
            track_type = arguments.pop("trackType", "video")
            if track_type not in ("video", "audio"):
                return ToolResult.error_result(DaVinciMCPError("Unsupported insertion track type", "TOOL_VALIDATION_ERROR"))
            arguments["mediaType"] = 1 if track_type == "video" else 2

        # Build request
        bridge_request = BridgeRequest(
            method=method,
            path=endpoint,
            params=arguments if method == BridgeMethod.GET else {},
            body=arguments if method == BridgeMethod.POST else None,
            request_id=tool_call.request_id,
        )

        try:
            response = self.transport.send(bridge_request)

            if (method == BridgeMethod.POST and response.is_server_error
                    and isinstance(response.data, dict) and response.data.get("error") == "Bridge operation failed"):
                raise BridgeOutcomeUnknownError()
            if response.is_success and not (isinstance(response.data, dict) and
                    (response.data.get("error") or response.data.get("success") is False)):
                data = response.data
                if wait_timeout is not None:
                    data = self._wait_for_render_jobs(data, wait_timeout)
                return ToolResult.success_result(data, tool_call.request_id)
            else:
                error_data = response.data if isinstance(response.data, dict) else {"message": str(response.data)}
                return ToolResult.error_result(
                    BridgeResponseError(
                        "Bridge operation failed",
                        status_code=response.status_code,
                        response_data=error_data,
                    ),
                    tool_call.request_id,
                )

        except DaVinciMCPError as e:
            return ToolResult.error_result(e, tool_call.request_id)

    def _wait_for_render_jobs(self, start_result, timeout):
        """Poll the accepted job IDs without issuing another mutation."""
        job_ids = start_result.get("jobIds") if isinstance(start_result, dict) else None
        if not isinstance(job_ids, list) or not job_ids or not all(isinstance(job_id, str) for job_id in job_ids):
            raise BridgeOutcomeUnknownError()
        deadline = time.monotonic() + timeout
        remaining = set(job_ids)
        statuses = {}
        status_path = get_endpoint_for_tool("get_render_job_status")[1]
        while remaining:
            for job_id in list(remaining):
                budget = deadline - time.monotonic()
                if budget <= 0:
                    raise BridgeOutcomeUnknownError(job_ids=job_ids)
                try:
                    response = self.transport.send(
                        BridgeRequest(BridgeMethod.GET, status_path, {"job_id": job_id}),
                        timeout=budget,
                    )
                    status = response.data["status"]["JobStatus"] if response.is_success else None
                except (DaVinciMCPError, TypeError, KeyError):
                    status = None
                if not isinstance(status, str):
                    raise BridgeOutcomeUnknownError(job_ids=job_ids)
                normalized = status.strip().lower()
                if normalized in {"complete", "completed", "failed", "cancelled", "canceled"}:
                    statuses[job_id] = normalized
                    remaining.remove(job_id)
            if remaining:
                time.sleep(max(0, min(0.25, deadline - time.monotonic())))
        failed = {job_id: status for job_id, status in statuses.items() if status not in {"complete", "completed"}}
        if failed:
            raise DaVinciMCPError("One or more render jobs failed or were cancelled",
                                  "RENDER_JOB_FAILED", {"jobStatus": statuses})
        return {**start_result, "jobStatus": statuses, "completed": True}

    def call_tool_simple(self, name: str, /, **kwargs) -> ToolResult:
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