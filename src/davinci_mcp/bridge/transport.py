"""
HTTP transport layer for communicating with the DaVinci Resolve bridge.
"""

import json
import time
import uuid
from typing import Any, Optional
from urllib import request, error
from dataclasses import dataclass

from ..config import BridgeConfig
from ..errors import (
    BridgeConnectionError,
    BridgeTimeoutError,
    BridgeResponseError,
    DaVinciMCPError,
)
from .protocol import BridgeMethod, BridgeRequest, BridgeResponse


@dataclass
class TransportStats:
    """Transport statistics."""
    requests_made: int = 0
    requests_failed: int = 0
    total_latency_ms: float = 0.0

    def record_request(self, latency_ms: float, success: bool) -> None:
        self.requests_made += 1
        if not success:
            self.requests_failed += 1
        self.total_latency_ms += latency_ms

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.requests_made if self.requests_made > 0 else 0.0


class HTTPTransport:
    """HTTP transport for bridge communication."""

    def __init__(self, config: Optional[BridgeConfig] = None):
        self.config = config or BridgeConfig()
        self.stats = TransportStats()
        self._opener = request.build_opener()

    def send(self, bridge_request: BridgeRequest) -> BridgeResponse:
        """Send a request to the bridge and return the response."""
        url = f"{self.config.base_url}{bridge_request.path}"
        request_id = bridge_request.request_id or str(uuid.uuid4())[:8]

        # Prepare request data
        if bridge_request.method == BridgeMethod.GET and bridge_request.params:
            query_string = "&".join(f"{k}={v}" for k, v in bridge_request.params.items())
            url = f"{url}?{query_string}"
            data = None
        else:
            data = None
            if bridge_request.body is not None:
                data = json.dumps(bridge_request.body).encode("utf-8")
            elif bridge_request.params:
                data = json.dumps(bridge_request.params).encode("utf-8")

        # Build the request
        req = request.Request(
            url,
            data=data,
            method=bridge_request.method.value,
            headers={
                "Content-Type": "application/json",
                "X-Request-ID": request_id,
                "User-Agent": "davinci-mcp/1.0.0",
            },
        )

        start_time = time.perf_counter()
        last_exception: Optional[Exception] = None

        for attempt in range(self.config.max_retries + 1):
            try:
                with self._opener.open(req, timeout=self.config.timeout) as resp:
                    response_data = resp.read()
                    latency_ms = (time.perf_counter() - start_time) * 1000

                    try:
                        parsed = json.loads(response_data.decode("utf-8"))
                    except json.JSONDecodeError:
                        parsed = {"raw": response_data.decode("utf-8", errors="replace")}

                    bridge_response = BridgeResponse(
                        status_code=resp.status,
                        data=parsed,
                        request_id=request_id,
                    )

                    self.stats.record_request(latency_ms, bridge_response.is_success)
                    return bridge_response

            except error.HTTPError as e:
                latency_ms = (time.perf_counter() - start_time) * 1000
                try:
                    error_data = json.loads(e.read().decode("utf-8"))
                except Exception:
                    error_data = {"message": str(e)}

                bridge_response = BridgeResponse(
                    status_code=e.code,
                    data=error_data,
                    request_id=request_id,
                )

                self.stats.record_request(latency_ms, False)

                # Don't retry client errors (4xx)
                if 400 <= e.code < 500:
                    return bridge_response

                last_exception = BridgeResponseError(
                    f"Bridge returned HTTP {e.code}",
                    status_code=e.code,
                    response_data=error_data,
                )

            except error.URLError as e:
                latency_ms = (time.perf_counter() - start_time) * 1000
                self.stats.record_request(latency_ms, False)
                last_exception = BridgeConnectionError(
                    f"Failed to connect to bridge: {e}",
                    host=self.config.host,
                    port=self.config.port,
                    original_error=e,
                )

            except TimeoutError as e:
                latency_ms = (time.perf_counter() - start_time) * 1000
                self.stats.record_request(latency_ms, False)
                last_exception = BridgeTimeoutError(
                    f"Request timed out after {self.config.timeout}s",
                    timeout=self.config.timeout,
                    endpoint=bridge_request.path,
                )

            # Wait before retry (except on last attempt)
            if attempt < self.config.max_retries:
                time.sleep(self.config.retry_delay * (attempt + 1))

        # All retries exhausted
        raise last_exception or BridgeConnectionError(
            "Request failed after all retries",
            host=self.config.host,
            port=self.config.port,
        )

    def health_check(self) -> bool:
        """Check if the bridge is reachable."""
        try:
            req = BridgeRequest(
                method=BridgeMethod.GET,
                path="/status",
                params={},
            )
            resp = self.send(req)
            return resp.is_success
        except DaVinciMCPError:
            return False

    def close(self) -> None:
        """Close the transport (no-op for urllib)."""
        pass