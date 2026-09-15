# Notice

`src/resolve_mcp_bridge.py` and `src/CursorBridge.py` are vendored, unmodified,
from [hiteshK03/davinci-resolve-mcp](https://github.com/hiteshK03/davinci-resolve-mcp),
commit `f812df7ab5d376592a24fb94611473fdf3a1acb2`, Copyright (c) 2026 Hitesh
Kandala, MIT License. See `LICENSE`.

Everything else in this repository (`manifests/`, `tests/`, `scripts/`,
`.github/workflows/`, and this documentation) is original tooling written to
install, verify, and operate that vendored server, published by Kerwil Gil.

## Why this project exists

This repository packages the upstream MCP server with an install script,
a pinned dependency lockfile, and a test suite that checks the server's
tool manifest against what is actually implemented in the vendored source
-- so the list of "verified" tools never silently drifts from the code
that backs it.

## Updating the vendored commit

1. Review the upstream diff and its dependency changes.
2. Update `manifests/tool-manifest.json` (`vendored_commit`) and copy the new
   `src/resolve_mcp_bridge.py` / `src/CursorBridge.py`.
3. Regenerate `requirements.lock` with hashes (`uv pip compile requirements.in
   --generate-hashes --output-file requirements.lock`).
4. Re-run `python -m unittest discover -s tests -v` and confirm every
   `verified_tools` entry is still implemented.
5. Manually re-verify each `verified_tools` entry against a real DaVinci
   Resolve project before shipping -- this repo's tests confirm a tool
   *exists*, not that it behaves correctly.
