# Release validation for v1.0.0

Integration in the Resolve application is **PENDING**. The PR checks record the
automated result for the proposed changes.

## Scope

| Classification | Tools | Exposure |
| --- | ---: | --- |
| SUPPORTED | 36 | Default MCP discovery. Documented contracts exercised with controlled Resolve objects. |
| EXPERIMENTAL | 119 | Enable `DAVINCI_MCP_ENABLE_EXPERIMENTAL=1` for discovery and calls. Descriptions are labeled. |
| UNAVAILABLE | 7 | No bridge implementation. Direct calls return `TOOL_UNAVAILABLE`. |

The full list is in [tool-manifest.json](manifests/tool-manifest.json). The
`verified_tools` field is retained for compatibility with previous consumers.
It records historical declarations. New consumers should read
`tool_availability` and `verification_status`.

## Contract validation

The API reference is Blackmagic Design's installed Developer/Scripting/README.txt,
dated 7 October 2025. The local machine has the developer support files and lacks
the Resolve application bundle. No personal project was loaded or changed.

| Area | Automated evidence |
| --- | --- |
| Playhead | Timeline-start offsets, 24 fps and 29.97/59.94 drop-frame minute boundaries, invalid labels, wrong timeline and out-of-range frames |
| Rendering | Zero-based indices mapped to stable IDs, explicit mode values, single start POST, terminal failure and bounded wait with unknown outcome |
| Gallery | Exact album and still label selection, ambiguous and missing labels, complete-set checks before deletion |
| Clip edits | Resolve every named item and reject duplicates before link, delete, compound or Fusion clip creation |
| Projects | Match an explicit database to the current connection before mutation. Resolve an explicit switch against the available database list. |
| Template placement | Reject explicit track/frame placement before moving the playhead or inserting. The documented API has no track parameter. Title, generator and standalone Fusion placement remain experimental. |
| Fusion, takes and cache | Resolve a named composition to its export index, validate take indices and selected take on finalize, map color/Fusion cache states |
| Export | Map documented timeline formats and AAF subtype. Reject mismatched still formats and existing output files. |
| Packaging and security | Clean wheel installs, installed stdio discovery and writes to a controlled bridge, bounded transport with no POST replay, Windows installer preview/update/rollback using a controlled Claude CLI, core dependency audit and redacted Gitleaks |

Advanced render ranges, Quick Export filename/extension behavior, noncanonical
legacy cache modes, and other partly implemented tools remain outside the default
scope. Optional ML dependencies are outside the core hash lock. The README
documents the opt-in and the manifest lists all experimental tools.

## Physical test that unlocks the release

Use a disposable local project and a new empty output directory. Record the OS,
Resolve version and edition, embedded Python version and observed results.

1. Start the bridge via Resolve's Workspace Scripts or Fusion Console and
   connect the installed MCP client with the shared token. Verify a rejected
   unauthenticated request, then query Resolve, the project and timeline.
2. Create a timeline. Import a short generated video and a generated audio file.
   Insert onto a known track, set the playhead, and read back the track contents
   and position. Exercise drop-frame playback at a minute boundary if supported
   by that timeline configuration.
3. Delete only items created in the test. Run a small render job in the
   disposable project and check completion by ID. Export a DRT and a still into
   the new output directory and verify the files are readable.
4. Use test-only gallery stills, takes and Fusion compositions for the
   corresponding supported selectors. Check each operation against the
   selected test object. Record skipped features and edition limitations.
5. On Windows, also exercise registration using the real Claude CLI profile
   created for QA. CI covers the installer transaction with a controlled CLI.
6. Close the temporary project and bridge. Restrict compatibility claims to
   the edition and operating system actually exercised.

The license is MIT. Package version is 1.0.0 and bridge version 2.0.0 identifies
the existing HTTP family. Wheel and sdist can be rebuilt using the pinned tools
and source epoch documented in the README.
