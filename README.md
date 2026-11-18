# DaVinci Resolve MCP

A local MCP server for DaVinci Resolve automation. MIT licensed.

**Release candidate 1.0.0.** Automated contract tests cover the default tool set.
Validation in the Resolve application remains pending. See the
[validation evidence and disposable-project procedure](RELEASE_VALIDATION.md).

The MCP client communicates over stdio with the installed Python package, which
sends authenticated HTTP requests to `CursorBridge.py` inside Resolve. The bridge
binds only to `127.0.0.1:9876`. It never starts merely because it was imported.

## Installation

Python 3.11+ and an MCP client are required. The CI exercises Python 3.11 and 3.13
on Windows, macOS and Linux; this does not certify those platforms with Resolve.
Resolve's installed Python interpreter must support Python 3 syntax. Its exact
version and the Free/Studio feature matrix are still pending physical validation.

From a checkout, create an isolated environment and install the locked core:

```bash
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python --require-hashes -r requirements.lock
uv pip install --python .venv/bin/python --no-deps .
```

Those are the macOS/Linux package commands. On Windows the interpreter path is
`.venv\Scripts\python.exe`. Always install the package; executing the source file
`src/davinci_mcp/server.py` directly does not support its relative imports.

Launch either the installed `davinci-resolve-mcp` command or:

```bash
/path/to/.venv/bin/python -m davinci_mcp.server
```

The server uses stdio; its logs go to stderr. For Claude Code:

```bash
claude mcp add --scope user --transport stdio davinci-resolve -- /absolute/path/to/.venv/bin/python -m davinci_mcp.server
```

See [examples/mcp.json](examples/mcp.json) for a generic client configuration.
No PyPI package or validated installer binary has been published.

### Windows helper

From a checkout, with `uv` and `claude` on PATH:

```powershell
.\scripts\install.ps1
# Upgrade an existing installation, preserving backups:
.\scripts\install.ps1 -Force
# Preview without writing:
.\scripts\install.ps1 -WhatIf
```

The helper installs the package into `%LOCALAPPDATA%\davinci-resolve-mcp`, copies
and hash-verifies the bridge in Resolve's Scripts/Utility folder, and registers
`python -m davinci_mcp.server` in Claude's **user** scope. Existing server env and
other options are retained. Previous environments and bridges are backed up.
Failure restores the previous environment, bridge, startup files and the exact
user MCP configuration bytes. Do not edit Claude's configuration concurrently
with installation. Project/local Claude registrations are not overwritten; an
existing conflicting registration must be resolved by the user.

`-EnableAutostart` opts into a dedicated `davinci_mcp_autostart.py` startup file;
it does not overwrite an unrelated `autostart.py`. Without this flag an existing
startup opt-in is retained. Autostart and the real Claude CLI integration remain
pending physical verification; CI uses a controlled CLI stub.

## Configure authentication and start the bridge

Generate a fresh secret locally, without committing it:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Set `DAVINCI_BRIDGE_TOKEN` to this same value in **both** the Resolve process and
the MCP server process. It must be ASCII and at least 32 characters long. The
bridge fails closed without it. Prefer passing it through each application's
launch environment. A GUI application started from Finder or the Start menu may
not inherit a terminal's environment. Client configuration files containing a
token must remain private and must not be committed.

For a manual Resolve session, set `os.environ["DAVINCI_BRIDGE_TOKEN"]` to your
secret in Resolve's Python console, then run the copied `CursorBridge.py` from
Workspace > Scripts. This integration procedure is **PENDING** on real Resolve.
On Windows the helper copies the script. On macOS manually copy it to the
Scripts/Utility directory used by your Resolve installation; directory discovery
and GUI startup have not been validated here.

The bridge uses port 9876. Restarting it does not automatically shut down another
instance. Close Resolve or use an authorized `/bridge/shutdown` request to stop
an old authenticated instance. Do not leave the old unauthenticated bridge running
when upgrading; replace it and restart Resolve before using the new MCP client.

| MCP environment variable | Default | Meaning |
|---|---|---|
| `DAVINCI_BRIDGE_TOKEN` | none | Shared bearer credential; required by bridge |
| `DAVINCI_BRIDGE_HOST` | `127.0.0.1` | Only `127.0.0.1` or `localhost` accepted |
| `DAVINCI_BRIDGE_PORT` | `9876` | Client target port; bridge uses 9876 |
| `DAVINCI_BRIDGE_TIMEOUT` | `30.0` | Seconds per request |
| `DAVINCI_BRIDGE_MAX_RETRIES` | `3` | GET retries only; POST is sent once |
| `DAVINCI_BRIDGE_RETRY_DELAY` | `1.0` | GET retry backoff base, seconds |
| `DAVINCI_MCP_NAME` | `davinci-resolve` | Server name |
| `DAVINCI_MCP_VERSION` | `1.0.0` | MCP server version |
| `DAVINCI_MCP_DESCRIPTION` | package description | Server description |
| `DAVINCI_MCP_ENABLE_EXPERIMENTAL` | `0` | Set to `1` to expose explicitly labeled experimental tools |

Bridge version `2.0.0` identifies its existing HTTP API, independently of package
version `1.0.0`.

## Tool support and errors

MCP discovers **36 supported tools** by default. The manifest lists these tools,
119 experimental tools available by opt-in, and seven unavailable ML tools.
The supported label reflects automated testing against the documented Resolve
API. Edition and version compatibility remain pending physical validation.
The historical `verified_tools` manifest field remains for existing consumers.

- `set_playhead(frame)` uses a zero-based offset from timeline start. Media
  insertion uses the absolute Resolve record frame reported by the timeline.
- Render selectors accept an index in the current queue or a stable job ID.
  Prefer the ID for deletion. `start_rendering(wait_for_completion=true)`
  polls the accepted IDs and has an optional completion timeout in seconds.
- Named project and timeline contexts must match the active context. An
  explicitly named project database must already be active. The
  `set_database` tool switches to a uniquely named database.
- Clip, album and still selectors must resolve uniquely. The bridge validates
  entire selections before deleting, linking or merging clips or stills.
- Title, generator and standalone Fusion insertion at an explicit track and
  frame are experimental. The documented Resolve methods have no destination
  track argument. The bridge rejects these placement requests before editing.
- The seven unimplemented ML tools stay hidden in both discovery modes.
  Direct MCP calls return `TOOL_UNAVAILABLE`.

See the [tool manifest](manifests/tool-manifest.json) for the complete classification.

Every HTTP route requires authentication, including reads, exports, deletion and
shutdown. Browser origins and non-local Host headers are rejected; CORS is disabled.
Requests are bounded, proxy use and redirects are disabled, and internal failures
do not return paths or tracebacks. The token grants local read/write authority; it
does not protect against malicious software already running as your OS user.

POST communication failures return `BRIDGE_OUTCOME_UNKNOWN`: inspect Resolve
before trying again. The operation may already have executed. HTTP errors are
returned without replaying POST. Only read-only GET requests have bounded retries.

## Development and release checks

```bash
python -m pip install build==1.6.1 setuptools==84.2.1 wheel==0.48.0 ruff==0.15.7
export SOURCE_DATE_EPOCH="$(git log -1 --format=%ct)"
python scripts/build_release.py
python -m pip install --no-deps dist/davinci_resolve_mcp-1.0.0-py3-none-any.whl
python -m unittest discover -s tests -v
ruff check src tests scripts
```

Installed-package stdio tests must run after wheel installation. Tests launch a
controlled loopback bridge and simulate Resolve; they never access personal
projects. Lint currently checks syntax and correctness rules; repository-wide
style modernization is outside this release correction.

CI also exercises Windows installation/update/rollback with real Python installs
and a controlled Claude CLI, audits locked runtime dependencies, and scans Git
history and the publication tree with redacted Gitleaks output.

See [release notes](RELEASE_NOTES.md) and [validation](RELEASE_VALIDATION.md).


## License

[MIT](LICENSE). Copyright (c) 2026 Kerwil Gil.
