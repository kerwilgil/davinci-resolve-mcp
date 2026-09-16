# DaVinci Resolve MCP

A local-first Model Context Protocol server for structured DaVinci Resolve
automation.

## Overview

This project provides a native MCP (Model Context Protocol) server that enables
structured automation of DaVinci Resolve through typed tools. Any MCP-compatible
client (Claude Code, Cursor, or custom clients) can drive DaVinci Resolve
programmatically: read project and timeline state, build and edit timelines,
manage the media pool, move clips, apply color operations, run renders, and
more — all through a typed tool interface instead of screen automation.

## Features

- **Native MCP interface** — structured tools for MCP-compatible clients.
- **Timeline automation** — create, inspect and modify timelines.
- **Media operations** — import and manage media and clips.
- **Project introspection** — structured project and timeline state.
- **Typed tool registry** — deterministic schemas and tool metadata.
- **Read/write separation** — explicit distinction between inspection and mutation.
- **Local-first bridge** — communication restricted to the local Resolve instance.
- **Structured errors** — predictable failures instead of opaque exceptions.
- **Automated validation** — registry, schemas and contracts covered by CI.
- **Extensible architecture** — tools grouped by Resolve domain instead of one monolithic bridge.

## Architecture

```
MCP client (Claude Code, Cursor, ...)
        | stdio, MCP tool calls
        v
src/davinci_mcp/server.py     (MCP server process; runs on your machine)
        | HTTP, localhost only
        v
src/CursorBridge.py           (runs inside DaVinci Resolve's Fusion console)
        |
        v
DaVinci Resolve project / timeline / media pool
```

The MCP server (`src/davinci_mcp/server.py`) never talks to DaVinci Resolve
directly — it only ever calls `http://127.0.0.1:9876`, where `CursorBridge.py`
is listening. If DaVinci Resolve is closed or the bridge script isn't running,
every tool call returns a structured connection error instead of hanging or
crashing.

## Requirements

- DaVinci Resolve 18 or later (Free or Studio; a handful of tools such as
  `smart_reframe_clip` and stabilization require Studio).
- Python 3.11+.
- [`uv`](https://github.com/astral-sh/uv) for locked, hash-verified
  dependency installs.
- An MCP-compatible client (e.g. Claude Code: `claude mcp add`).
- FFmpeg on `PATH` for transcription/scene-detection tools.

## Installation

From a checkout of this repository, on Windows:

```powershell
.\scripts\install.ps1
```

This creates a locked Python 3.11 virtual environment, installs dependencies
from `requirements.lock` with hash verification, copies and SHA-256-verifies
`src/CursorBridge.py` into DaVinci Resolve's `Scripts/Utility` folder, and
registers the server with Claude Code via `claude mcp add`.

Add `-EnableAutostart` to also install `scripts/autostart.py` into DaVinci
Resolve's `Scripts/Start` folder (off by default — see Security). Use
`-Force` to back up and replace an existing installation. `-WhatIf` previews
the operation without applying it.

On macOS/Linux, install manually: create a virtual environment, `uv pip
install --require-hashes --requirements requirements.lock`, then register
`src/davinci_mcp/server.py` with your MCP client. `CursorBridge.py` still
needs to run inside DaVinci Resolve's own Scripts folder for your platform.

## Configuration

Point any MCP client at `src/davinci_mcp/server.py` with the environment's
Python interpreter. For Claude Code:

```bash
claude mcp add davinci-resolve -- python /path/to/src/davinci_mcp/server.py
```

Environment variables (all optional):

| Variable | Default | Description |
|---|---|---|
| `DAVINCI_BRIDGE_HOST` | `127.0.0.1` | Bridge host |
| `DAVINCI_BRIDGE_PORT` | `9876` | Bridge port |
| `DAVINCI_BRIDGE_TIMEOUT` | `30.0` | Request timeout (seconds) |
| `DAVINCI_BRIDGE_MAX_RETRIES` | `3` | Max retries for failed requests |
| `DAVINCI_BRIDGE_RETRY_DELAY` | `1.0` | Base retry delay (seconds) |
| `DAVINCI_MCP_NAME` | `davinci-resolve` | MCP server name |
| `DAVINCI_MCP_VERSION` | `1.0.0` | MCP server version |
| `DAVINCI_MCP_DESCRIPTION` | `DaVinci Resolve MCP server...` | Server description |

## Running the Bridge

Start `src/CursorBridge.py` inside DaVinci Resolve:

1. Open DaVinci Resolve
2. Go to **Workspace → Scripts → CursorBridge**
3. The bridge will start listening on `http://127.0.0.1:9876`

Or enable autostart during installation (`-EnableAutostart`) to have the bridge
start automatically when Resolve launches.

## Available Tools

The server exposes 162 tools across 9 categories. See `manifests/tool-manifest.json`
for the complete list of verified tools.

### Project (29 tools)
`get_resolve_status`, `get_project_info`, `get_current_page`, `open_page`,
`save_project`, `set_project_setting`, `set_timeline_setting`,
`export_current_frame`, `create_subtitles_from_audio`, `detect_scene_cuts`,
`get_project_list`, `get_database_list`, `load_project`, `create_project`,
`delete_project`, `archive_project`, `export_project`, `import_project`,
`navigate_project_folder`, `set_database`, `layout_preset`, `render_preset`,
`burnin_preset`, `get_keyframe_mode`, `set_keyframe_mode`, `refresh_lut_list`,
`get_media_storage`, `reveal_in_storage`, `voice_isolate`, `voice_isolate_timeline`,
`remove_background`, `remove_background_video`, `remove_background_clip`,
`transcribe_timeline`, `transcribe_file`

### Timeline (27 tools)
`get_timeline_info`, `get_timeline_clips`, `get_timeline_markers`,
`set_playhead`, `add_marker`, `delete_markers`, `switch_timeline`,
`create_timeline`, `rename_timeline`, `duplicate_timeline`, `export_timeline`,
`set_timeline_mark_in_out`, `clear_timeline_mark_in_out`,
`delete_timeline_clips`, `link_timeline_clips`, `create_compound_clip`,
`create_fusion_clip`, `add_track`, `delete_track`, `set_track_enable`,
`set_track_lock`, `set_track_name`

### Media (16 tools)
`get_media_pool`, `get_media_pool_structure`, `navigate_media_pool`,
`create_media_pool_folder`, `import_media`, `get_clip_metadata`,
`set_clip_metadata`, `get_clip_info`, `set_pool_clip_property`,
`delete_media_pool_clips`, `move_media_pool_clips`, `relink_media_pool_clips`,
`unlink_media_pool_clips`, `auto_sync_audio`, `import_timeline_from_file`,
`export_metadata`, `import_media_from_storage`

### Clips (8 tools)
`add_clip_marker`, `get_clip_markers`, `delete_clip_markers`,
`add_clip_flag`, `get_clip_flags`, `clear_clip_flags`,
`get_clip_thumbnail`, `get_current_video_item`

### Color (23 tools)
`get_node_graph`, `set_lut`, `get_lut`, `set_node_enabled`,
`apply_grade_from_drx`, `reset_all_grades`, `apply_arri_cdl_lut`,
`set_cdl`, `export_lut`, `copy_grades`, `reset_node_colors`,
`get_color_versions`, `add_color_version`, `load_color_version`,
`delete_color_version`, `rename_color_version`, `get_color_groups`,
`add_color_group`, `delete_color_group`, `assign_to_color_group`,
`remove_from_color_group`

### Fusion (10 tools)
`get_fusion_comps`, `add_fusion_comp_to_clip`, `import_fusion_comp_to_clip`,
`export_fusion_comp_from_clip`, `delete_fusion_comp_on_clip`,
`load_fusion_comp_on_clip`, `rename_fusion_comp_on_clip`,
`create_magic_mask`, `regenerate_magic_mask`, `stabilize_clip`,
`smart_reframe_clip`

### Audio (16 tools)
`get_fairlight_presets`, `apply_fairlight_preset`, `insert_audio_at_playhead`,
`get_voice_isolation_state`, `set_voice_isolation_state`, `get_takes`,
`add_take`, `select_take`, `delete_take`, `finalize_take`,
`link_proxy_media`, `unlink_proxy_media`, `replace_clip`, `set_clip_cache`,
`update_sidecar`, `get_linked_items`

### Render (11 tools)
`get_render_settings`, `set_render_settings`, `set_render_format`,
`get_render_formats`, `add_render_job`, `start_rendering`, `stop_rendering`,
`delete_render_job`, `get_render_job_status`, `get_render_resolutions`,
`get_quick_export_presets`, `quick_export`, `set_render_mode`

### Gallery (10 tools)
`get_gallery_albums`, `get_album_stills`, `set_current_album`,
`create_gallery_album`, `grab_still`, `grab_all_stills`, `export_stills`,
`import_stills`, `delete_stills`, `set_still_label`

## Examples

### Create a timeline and add clips

```python
# Via MCP tool calls
create_timeline(name="My Timeline", frame_rate=24)
insert_to_timeline(clip_name="clip1.mp4", track_type="video", track_index=1)
insert_to_timeline(clip_name="audio.wav", track_type="audio", track_index=1)
```

### Render a timeline

```python
add_render_job(preset="H.264 Master", output_path="/renders/out.mp4")
start_rendering(wait_for_completion=true)
```

### Color grading

```python
set_lut(clip_name="clip1", node_index=1, lut_path="/luts/film.cube")
set_cdl(clip_name="clip1", node_index=2,
        slope=[1.1, 1.0, 0.9],
        offset=[0.02, 0.0, -0.01],
        power=[0.95, 1.0, 1.05],
        saturation=1.1)
```

## Development

### Project Structure

```
src/davinci_mcp/
├── __init__.py          # Package exports
├── server.py            # MCP server entry point
├── config.py            # Configuration
├── errors.py            # Structured error types
├── bridge/
│   ├── __init__.py      # Bridge exports
│   ├── protocol.py      # HTTP protocol definitions
│   ├── transport.py     # HTTP transport layer
│   └── client.py        # High-level bridge client
├── schemas/
│   ├── __init__.py      # Schema registry
│   ├── common.py        # Common definitions
│   ├── timeline.py      # Timeline tool schemas
│   ├── media.py         # Media pool tool schemas
│   ├── clips.py         # Clip tool schemas
│   ├── color.py         # Color tool schemas
│   ├── fusion.py        # Fusion tool schemas
│   ├── audio.py         # Audio tool schemas
│   ├── render.py        # Render tool schemas
│   ├── gallery.py       # Gallery tool schemas
│   └── project.py       # Project tool schemas
└── tools/
    ├── __init__.py      # Tool registry & base
    ├── project.py       # Project tool implementations
    ├── timeline.py      # Timeline tool implementations
    ├── media.py         # Media tool implementations
    ├── clips.py         # Clips tool implementations
    ├── color.py         # Color tool implementations
    ├── fusion.py        # Fusion tool implementations
    ├── audio.py         # Audio tool implementations
    ├── render.py        # Render tool implementations
    └── gallery.py       # Gallery tool implementations
```

### Running Tests

```bash
# Install test dependencies
uv pip install -r requirements.lock

# Run all tests
python -m pytest tests/ -v

# Run specific test modules
python -m pytest tests/test_registry.py -v
python -m pytest tests/test_bridge.py -v
python -m pytest tests/test_schemas.py -v
```

Tests are pure Python and do not require DaVinci Resolve to be installed.

### Adding a New Tool

1. Add schema in appropriate `schemas/<category>.py`
2. Register in `schemas/__init__.py` (added to `ALL_SCHEMAS` automatically)
3. Add implementation in appropriate `tools/<category>.py`
4. Register in `tools/__init__.py` via the category's `register_*_tools()` function
5. Add to `manifests/tool-manifest.json` under `verified_tools` once tested
6. Run tests to verify registration and schema consistency

## Testing

The test suite covers:

- **Registry consistency** — all tools have schemas, no duplicates, verified tools subset
- **Manifest consistency** — manifest verified tools match registry
- **Schema validation** — all schemas well-formed, required fields present, enums valid
- **Bridge protocol** — request/response handling, error classification, retries
- **Read/write classification** — tools correctly categorized
- **Transport layer** — HTTP communication, timeouts, connection errors

## Security

- The bridge binds to `127.0.0.1` only — never exposed on network interfaces.
- Autostart is opt-in (`-EnableAutostart`) and creates a marker file.
- Structured error responses prevent information leakage.
- No authentication on the local bridge — ensure your machine is trusted.

## Roadmap

- [ ] WebSocket transport for lower latency
- [ ] Batch tool execution support
- [ ] Real-time timeline events via SSE
- [ ] Additional AI/ML tool integrations
- [ ] macOS/Linux install scripts
- [ ] Official PyPI release

## License

MIT License

Copyright (c) 2026 Kerwil Gil

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.