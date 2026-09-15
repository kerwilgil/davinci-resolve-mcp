# DaVinci Resolve MCP

MCP server for controlling and automating DaVinci Resolve workflows through structured tools.

This project lets any MCP-compatible client (Claude Code, Cursor, or another
MCP client) drive DaVinci Resolve programmatically: read project and timeline
state, build and edit timelines, manage the media pool, move clips, apply
color operations, run renders, and more -- all through a typed tool
interface instead of screen automation. A local HTTP bridge (`CursorBridge.py`)
runs inside DaVinci Resolve's own scripting console; the MCP server
(`resolve_mcp_bridge.py`) is a thin stdio process that forwards structured
tool calls to that bridge and returns structured results.

## Overview

- **`src/CursorBridge.py`** runs inside DaVinci Resolve (via Workspace >
  Scripts, or autostart) and exposes a JSON HTTP API on `127.0.0.1:9876`.
- **`src/resolve_mcp_bridge.py`** is the MCP server: an external process,
  started by your MCP client, that exposes 162 tools over stdio and
  forwards each call to the bridge above.
- **`manifests/tool-manifest.json`** records which of those tools have
  actually been exercised against a real project (`verified_tools`), plus
  the exact upstream commit this repository vendors.

Both files are vendored, unmodified, from
[hiteshK03/davinci-resolve-mcp](https://github.com/hiteshK03/davinci-resolve-mcp)
(MIT License) -- see `NOTICE.md` for full attribution. This repository adds
the installation script, dependency lockfile, and manifest/test harness
around that server.

## Features

- 162 MCP tools covering project info, timeline construction and editing,
  media pool management, color (nodes, grades, CDL, LUTs, color groups),
  Fusion compositions, Fairlight audio, gallery/stills, rendering, and
  project/database management (see the full table below).
- Read tools return structured project/timeline/clip state without
  mutating anything.
- Write tools (timeline creation, clip insertion, render jobs, project
  settings, etc.) modify the currently open DaVinci Resolve project.
- Local Whisper-based transcription (`transcribe_timeline`,
  `transcribe_file`) and scene-cut detection, useful for transcript-driven
  editing workflows.
- Optional audio isolation (Demucs) and background removal (rembg) tools,
  each importing their (larger) dependencies lazily so the base install
  stays light.
- Structured error responses (`{"error": ...}`) when the bridge is
  unreachable or DaVinci Resolve returns an error, instead of raising.

## Architecture

```
MCP client (Claude Code, Cursor, ...)
        | stdio, MCP tool calls
        v
src/resolve_mcp_bridge.py   (this process; runs on your machine)
        | HTTP, localhost only
        v
src/CursorBridge.py         (runs inside DaVinci Resolve's Fusion console)
        |
        v
DaVinci Resolve project / timeline / media pool
```

`resolve_mcp_bridge.py` never talks to DaVinci Resolve directly -- it only
ever calls `http://127.0.0.1:9876`, where `CursorBridge.py` is listening.
If DaVinci Resolve is closed or the bridge script isn't running, every tool
call returns a structured connection error instead of hanging or crashing.

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
Resolve's `Scripts/Start` folder (off by default -- see Security). Use
`-Force` to back up and replace an existing installation. `-WhatIf` previews
the operation without applying it.

On macOS/Linux, install manually: create a virtual environment, `uv pip
install --require-hashes --requirements requirements.lock`, then register
`src/resolve_mcp_bridge.py` with your MCP client. `CursorBridge.py` still
needs to run inside DaVinci Resolve's own Scripts folder for your platform.

## Configuration

Point any MCP client at `src/resolve_mcp_bridge.py` with the environment's
Python interpreter, for example (`examples/mcp.json`):

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "python",
      "args": ["path/to/src/resolve_mcp_bridge.py"]
    }
  }
}
```

`scripts/install.ps1` does this automatically for Claude Code via
`claude mcp add --transport stdio davinci-resolve -- <python> <server>`.

## Running the MCP Server

1. Open DaVinci Resolve with a project.
2. Run **Workspace > Scripts > CursorBridge** (or enable autostart).
3. Confirm the console prints `Bridge is running (read + write)`.
4. From your MCP client, call `get_resolve_status()` first to confirm the
   bridge is reachable before running anything else.

## Available Tools

162 tools are registered in `src/resolve_mcp_bridge.py`. **Type** is
inferred from each tool's naming convention (`get_*`/`list_*` = Read,
everything else = Write); **Status: Verified** means the tool is listed in
`manifests/tool-manifest.json` as exercised against a real project --
every other tool is implemented and exposed but not yet manually verified
end-to-end.

| Tool | Description | Type | Status |
|---|---|---|---|
| `get_resolve_status` | Check whether the CursorBridge is running and DaVinci Resolve is connected. | Read | Verified |
| `get_project_info` | Get information about the currently open DaVinci Resolve project. | Read | Verified |
| `get_current_page` | Get which page the user is currently viewing in DaVinci Resolve. | Read | Available |
| `get_timeline_info` | Get detailed information about the current timeline. | Read | Verified |
| `get_timeline_clips` | Get the list of clips on a specific track in the current timeline. | Read | Verified |
| `get_timeline_markers` | Get all markers on the current timeline. | Read | Available |
| `get_render_settings` | Get the current render configuration for the project. | Read | Available |
| `get_media_pool` | List clips and subfolders in the current media pool folder. | Read | Available |
| `get_clip_properties` | Get the inspector/transform properties of a timeline clip (zoom, pan, tilt, opacity, crop, etc.). | Read | Available |
| `open_page` | Switch DaVinci Resolve to a different page. | Write | Verified |
| `set_playhead` | Move the playhead to a specific timecode in the current timeline. | Write | Verified |
| `add_marker` | Add a marker to the current timeline. | Write | Verified |
| `delete_markers` | Delete timeline markers by frame position or by color. | Write | Available |
| `switch_timeline` | Switch to a different timeline in the project. | Write | Available |
| `create_timeline` | Create a new empty timeline in the media pool. | Write | Verified |
| `rename_timeline` | Rename the current timeline. | Write | Available |
| `duplicate_timeline` | Duplicate the current timeline. | Write | Available |
| `add_track` | Add a new track to the current timeline. | Write | Available |
| `delete_track` | Delete a track from the current timeline. | Write | Available |
| `set_track_enable` | Enable or disable a track in the current timeline. | Write | Available |
| `set_track_lock` | Lock or unlock a track in the current timeline. | Write | Available |
| `set_track_name` | Rename a track in the current timeline. | Write | Available |
| `import_media` | Import media files into the current media pool folder. | Write | Available |
| `append_to_timeline` | Append a media pool clip to the end of the current timeline. | Write | Available |
| `insert_to_timeline` | Insert a media pool clip at a specific track and timeline position. | Write | Verified |
| `set_clip_color` | Set the color label of a clip on the timeline. | Write | Available |
| `set_clip_enabled` | Enable or disable a clip on the timeline. | Write | Available |
| `set_clip_properties` | Set transform and compositing properties on a timeline clip. | Write | Verified |
| `insert_title` | Insert a title at the playhead in the current timeline. | Write | Verified |
| `insert_generator` | Insert a generator at the playhead in the current timeline. | Write | Verified |
| `insert_fusion_composition` | Insert an empty Fusion composition at the playhead in the current timeline. | Write | Available |
| `set_render_settings` | Configure render settings for the project. | Write | Verified |
| `set_render_format` | Set the render output format and codec. | Write | Verified |
| `get_render_formats` | List available render formats, or codecs for a specific format. | Read | Available |
| `add_render_job` | Add a render job to the queue based on current render settings. | Write | Verified |
| `start_rendering` | Start rendering queued jobs. | Write | Verified |
| `stop_rendering` | Stop any currently active render process. | Write | Available |
| `delete_render_job` | Delete render job(s) from the queue. | Write | Available |
| `save_project` | Save the currently open DaVinci Resolve project. | Write | Available |
| `set_project_setting` | Set a project-level setting. | Write | Available |
| `set_timeline_setting` | Set a timeline-level setting on the current timeline. | Write | Verified |
| `export_current_frame` | Export the current frame (at playhead) as a still image. | Write | Verified |
| `create_subtitles_from_audio` | [STUDIO ONLY] Auto-generate subtitles from the audio in the current timeline using DaVinci Resolve's built-in speech-to-text (Neural Engine). | Write | Verified |
| `detect_scene_cuts` | Automatically detect and create scene cuts along the current timeline. | Write | Verified |
| `get_media_pool_structure` | Get the full media pool folder tree structure. | Read | Available |
| `navigate_media_pool` | Navigate to a specific folder in the media pool. | Write | Available |
| `create_media_pool_folder` | Create a new subfolder in the media pool. | Write | Available |
| `get_clip_metadata` | Get all metadata for a media pool clip. | Read | Verified |
| `set_clip_metadata` | Set metadata on a media pool clip. | Write | Available |
| `get_clip_info` | Get detailed properties for a media pool clip including flags, markers, and all clip attributes. | Read | Verified |
| `set_pool_clip_property` | Set a property on a media pool clip. | Write | Available |
| `delete_media_pool_clips` | Delete clips from the media pool. | Write | Available |
| `move_media_pool_clips` | Move clips to a different folder in the media pool. | Write | Available |
| `relink_media_pool_clips` | Relink media pool clips to a new filesystem folder. | Write | Available |
| `unlink_media_pool_clips` | Unlink media pool clips from their source files. | Write | Available |
| `auto_sync_audio` | Auto-sync audio to video clips in the media pool. | Write | Available |
| `import_timeline_from_file` | Import a timeline from an AAF, EDL, XML, FCPXML, DRT, ADL, or OTIO file. | Write | Available |
| `export_metadata` | Export clip metadata from the media pool to a CSV file. | Write | Available |
| `import_media_from_storage` | Import media files from Resolve's Media Storage into the current media pool folder. | Write | Available |
| `add_clip_marker` | Add a marker to a specific clip on the timeline (not a timeline marker). | Write | Available |
| `get_clip_markers` | Get all markers on a specific timeline clip. | Read | Available |
| `delete_clip_markers` | Delete markers from a specific timeline clip. | Write | Available |
| `add_clip_flag` | Add a flag to a timeline clip. Flags are colored labels visible in the timeline. | Write | Available |
| `get_clip_flags` | Get all flags on a specific timeline clip. | Read | Available |
| `clear_clip_flags` | Clear flags from a timeline clip. | Write | Available |
| `delete_timeline_clips` | Delete clips from the timeline. | Write | Available |
| `link_timeline_clips` | Link or unlink timeline clips. Linked clips move together when dragged. | Write | Available |
| `create_compound_clip` | Create a compound clip from selected timeline items. | Write | Available |
| `create_fusion_clip` | Create a Fusion clip from selected timeline items. | Write | Available |
| `get_current_video_item` | Get information about the clip currently under the playhead. | Read | Available |
| `get_clip_thumbnail` | Get a thumbnail image of the current clip at the playhead position. | Read | Verified |
| `export_timeline` | Export the current timeline to a file (AAF, EDL, FCPXML, OTIO, etc.). | Write | Available |
| `get_gallery_albums` | List all gallery still albums and PowerGrade albums. | Read | Available |
| `get_album_stills` | List stills in a gallery album. | Read | Available |
| `set_current_album` | Set the active gallery album. Stills will be grabbed into this album. | Write | Available |
| `create_gallery_album` | Create a new gallery album. | Write | Available |
| `grab_still` | Grab a still from the current clip at the playhead position. | Write | Verified |
| `grab_all_stills` | Grab stills from all clips on the timeline. | Write | Available |
| `export_stills` | Export stills from a gallery album to disk. | Write | Available |
| `import_stills` | Import stills (grade references) into the current gallery album. | Write | Available |
| `delete_stills` | Delete stills from a gallery album. | Write | Available |
| `set_still_label` | Set the label on a gallery still in the current album. | Write | Available |
| `get_node_graph` | Get the color node graph for a clip or the timeline. | Read | Verified |
| `set_lut` | Apply a LUT to a specific node in a clip's color graph. | Write | Available |
| `get_lut` | Get the LUT applied to a specific node. | Read | Available |
| `set_node_enabled` | Enable or disable a node in the color graph. | Write | Available |
| `apply_grade_from_drx` | Apply a color grade from a DRX still file to a clip. | Write | Available |
| `reset_all_grades` | Reset all color grades on a clip's node graph back to default. | Write | Available |
| `apply_arri_cdl_lut` | Apply ARRI CDL and LUT to a clip. | Write | Available |
| `set_cdl` | Set CDL (Color Decision List) values on a clip. | Write | Verified |
| `export_lut` | Export a LUT from a clip's color grading. | Write | Available |
| `copy_grades` | Copy color grades from one clip to others. | Write | Available |
| `reset_node_colors` | Reset node colors for all nodes in a clip's active color version. | Write | Available |
| `get_color_versions` | Get all color versions for a clip (local and remote). | Read | Available |
| `add_color_version` | Add a new color version to a clip. | Write | Available |
| `load_color_version` | Load/activate a named color version on a clip. | Write | Available |
| `delete_color_version` | Delete a color version from a clip. | Write | Available |
| `rename_color_version` | Rename a color version on a clip. | Write | Available |
| `get_color_groups` | List all color groups in the current project. | Read | Available |
| `add_color_group` | Create a new color group. Group name must be unique. | Write | Available |
| `delete_color_group` | Delete a color group. Clips in the group become ungrouped. | Write | Available |
| `assign_to_color_group` | Assign a timeline clip to a color group. | Write | Available |
| `remove_from_color_group` | Remove a clip from its color group. | Write | Available |
| `get_fusion_comps` | List Fusion compositions on a timeline clip. | Read | Available |
| `add_fusion_comp_to_clip` | Add a new blank Fusion composition to a timeline clip. | Write | Available |
| `import_fusion_comp_to_clip` | Import a Fusion composition from file into a timeline clip. | Write | Available |
| `export_fusion_comp_from_clip` | Export a Fusion composition from a timeline clip to a file. | Write | Available |
| `delete_fusion_comp_on_clip` | Delete a named Fusion composition from a timeline clip. | Write | Available |
| `load_fusion_comp_on_clip` | Load a named Fusion composition as the active one on a clip. | Write | Available |
| `rename_fusion_comp_on_clip` | Rename a Fusion composition on a timeline clip. | Write | Available |
| `create_magic_mask` | [STUDIO ONLY] Create a Magic Mask on a timeline clip using DaVinci Neural Engine. | Write | Available |
| `regenerate_magic_mask` | [STUDIO ONLY] Regenerate an existing Magic Mask on a clip using DaVinci Neural Engine. | Write | Available |
| `stabilize_clip` | [STUDIO ONLY] Stabilize a timeline clip using DaVinci Neural Engine enhanced stabilization. | Write | Available |
| `smart_reframe_clip` | [STUDIO ONLY] Apply Smart Reframe to a clip using DaVinci Neural Engine for automatic aspect ratio adjustment. | Write | Verified |
| `get_fairlight_presets` | List available Fairlight audio presets. | Read | Available |
| `apply_fairlight_preset` | Apply a Fairlight preset to the current timeline. | Write | Available |
| `insert_audio_at_playhead` | Insert audio at the playhead on a selected track in the Fairlight page. | Write | Available |
| `get_voice_isolation_state` | [STUDIO ONLY] Get Resolve's native voice isolation state for a clip or audio track. | Read | Available |
| `set_voice_isolation_state` | [STUDIO ONLY] Set Resolve's native voice isolation state on a clip or audio track. | Write | Available |
| `get_takes` | Get all takes for a clip (take selector). | Read | Available |
| `add_take` | Add a media pool clip as a new take to a timeline clip. | Write | Available |
| `select_take` | Select a take by index. | Write | Available |
| `delete_take` | Delete a take by index. | Write | Available |
| `finalize_take` | Finalize the take selection on a clip, committing the chosen take. | Write | Available |
| `link_proxy_media` | Link a proxy media file to a media pool clip. | Write | Available |
| `unlink_proxy_media` | Unlink proxy media from a media pool clip. | Write | Available |
| `replace_clip` | Replace a media pool clip's underlying source file. | Write | Available |
| `set_clip_cache` | Set render cache mode for a timeline clip. | Write | Available |
| `update_sidecar` | Update sidecar file for BRAW clips or RMD file for R3D clips. | Write | Available |
| `get_linked_items` | Get items linked to a timeline clip (e.g. audio linked to video). | Read | Available |
| `set_timeline_mark_in_out` | Set mark in/out points on the current timeline. | Write | Verified |
| `clear_timeline_mark_in_out` | Clear mark in/out points on the current timeline. | Write | Available |
| `get_project_list` | List projects and folders in the current database folder. | Read | Available |
| `get_database_list` | List all databases configured in Resolve (Disk and PostgreSQL). | Read | Available |
| `load_project` | Load/open a project by name. | Write | Available |
| `create_project` | Create a new project. | Write | Available |
| `delete_project` | Delete a project (cannot be the currently loaded project). | Write | Available |
| `archive_project` | Archive a project to a file. | Write | Available |
| `export_project` | Export a project to a .drp file. | Write | Available |
| `import_project` | Import a project from a .drp file. | Write | Available |
| `navigate_project_folder` | Navigate the project folder hierarchy. | Write | Available |
| `set_database` | Switch to a different database. | Write | Available |
| `layout_preset` | Manage UI layout presets. | Write | Available |
| `render_preset` | Manage render presets. | Write | Available |
| `burnin_preset` | Manage data burn-in presets. | Write | Available |
| `get_keyframe_mode` | Get the current keyframe mode (All, Color, or Sizing). | Read | Available |
| `set_keyframe_mode` | Set the keyframe mode. | Write | Available |
| `get_render_job_status` | Get the status and progress of a specific render job. | Read | Verified |
| `get_render_resolutions` | Get available render resolutions, optionally filtered by format and codec. | Read | Available |
| `get_quick_export_presets` | List available Quick Export render presets (YouTube, Vimeo, etc.). | Read | Available |
| `quick_export` | Quick Export the current timeline using a preset. | Write | Available |
| `set_render_mode` | Set the render mode. | Write | Available |
| `refresh_lut_list` | Refresh the LUT list so Resolve discovers newly added LUT files. | Write | Available |
| `get_media_storage` | Browse Resolve's Media Storage. | Read | Available |
| `reveal_in_storage` | Expand and reveal a file or folder in Resolve's Media Storage panel. | Write | Available |
| `voice_isolate` | [FREE + STUDIO · LOCAL AI] Separate vocals from background audio using Demucs (open-source replacement for Studio Voice Isolation). | Write | Available |
| `voice_isolate_timeline` | [FREE + STUDIO · LOCAL AI] Isolate vocals from the current timeline's audio track using Demucs. | Write | Available |
| `remove_background` | [FREE + STUDIO · LOCAL AI] Remove background from a single image (open-source replacement for Studio Magic Mask). | Write | Available |
| `remove_background_video` | [FREE + STUDIO · LOCAL AI] Remove background from every frame of a video file (open-source replacement for Studio Magic Mask). | Write | Available |
| `remove_background_clip` | [FREE + STUDIO · LOCAL AI] Remove background from a specific timeline clip's source video (open-source replacement for Studio Magic Mask). | Write | Available |
| `transcribe_timeline` | [FREE + STUDIO · LOCAL AI] Transcribe the audio from the current timeline using local Whisper (open-source replacement for Studio speech-to-text). | Write | Verified |
| `transcribe_file` | [FREE + STUDIO · LOCAL AI] Transcribe any audio or video file using local Whisper (open-source replacement for Studio speech-to-text). | Write | Available |

## Example Usage

```python
# From an MCP client session, after get_resolve_status() confirms connectivity:
get_project_info()
create_timeline(name="rough_cut")
insert_to_timeline(
    media_pool_item="clip_01.mp4",
    start_frame=0,
    end_frame=300,
    track_index=1,
)
set_timeline_mark_in_out(mark_in=0, mark_out=300)
add_render_job()
start_rendering()
```

## Development

```powershell
git clone https://github.com/kerwilgil/davinci-resolve-mcp.git
cd davinci-resolve-mcp
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe mcp==1.28.1
```

The heavier optional dependencies (`faster-whisper`, `demucs`, `rembg`,
`soundfile`) are imported lazily inside individual tool functions, so they
are only required to exercise transcription/audio/background-removal tools,
not to import or test the module.

## Testing

```powershell
python -m unittest discover -s tests -v
```

`tests/test_manifest.py` checks that every tool in `verified_tools` is
actually registered in `src/resolve_mcp_bridge.py`, that the manifest has
no duplicates, and that `create_timeline`/`insert_to_timeline` stay
verified (the regression this repository was extracted to fix).
`tests/test_server_load.py` imports the server module and confirms the
bridge stays bound to `127.0.0.1`.

## Security

- Runs entirely locally: `CursorBridge.py` binds only to `127.0.0.1:9876`
  and controls whatever project is currently open in DaVinci Resolve on
  that machine.
- Write tools modify the open project/timeline/media pool directly --
  confirm before running anything destructive (deleting clips, tracks,
  projects, or render jobs; rendering and saving both have persistent
  effects).
- Any local process able to reach port 9876 can call the bridge. Do not
  expose it via port forwarding, firewall rules, tunnels, or a
  `0.0.0.0` bind.
- Only connect MCP clients you trust -- the server grants full read/write
  control over the open project.
- Autostart is opt-in (`.davinci-mcp-autostart-enabled` marker); without it,
  `scripts/autostart.py` exits immediately. Starting the bridge manually and
  closing Resolve when done minimizes the exposure window.

## Roadmap

- Expand timeline-editing coverage in `verified_tools` as more tools are
  manually exercised against real projects.
- Add integration tests that spin up a fake `CursorBridge` HTTP server to
  exercise `resolve_mcp_bridge.py`'s request/response handling without
  requiring DaVinci Resolve itself.
- Richer project/media-pool introspection helpers.
- Transactional/safe-edit workflows (e.g. dry-run a timeline edit before
  applying it).
- Track compatibility across DaVinci Resolve versions as new releases ship.

## License

MIT, inherited from the vendored upstream project. See `LICENSE` and
`NOTICE.md` for attribution details.
