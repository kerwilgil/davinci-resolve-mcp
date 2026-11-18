# Changelog

All notable changes to this project are documented in this file.

## [Unreleased] — 1.0.0 release candidate

- Require bearer authentication on every bridge route; reject browser origins and
  non-local Host headers, bound JSON bodies, remove CORS and redact internal errors.
- Send mutations once. Report communication failures as `BRIDGE_OUTCOME_UNKNOWN`.
  Keep bounded GET retries, disable proxies/redirects and encode query parameters.
- Install a real Python package with a console entry point and module launch;
  publish actual tool schemas through MCP stdio and enforce JSON Schema validation.
- Correct bridge route mappings, mutation argument names, named clip/context guards,
  timeline creation settings and render destination handling.
- Return `TOOL_UNAVAILABLE` for seven declared ML tools without bridge implementations.
- Update MCP to 1.30.0 and regenerate a hash-locked, universal core dependency set.
- Preserve user MCP settings, previous installations and unrelated startup scripts;
  exercise installer upgrade and injected rollback on Windows CI.
- Add installed-wheel stdio, loopback authorization and mutation regression tests,
  multi-platform CI and publication/history secret scanning.
- Physical integration remains pending as recorded in RELEASE_VALIDATION.md.

- Resolve non-drop and 29.97/59.94 drop-frame playhead offsets, zero-based render
  queue indices, stable job IDs and render mode. Poll accepted jobs with a
  bounded timeout and report unknown completion without submitting another POST.
- Verify named database, timeline, clip, album and still selections before
  effects. Adapt Fusion exports, take operations and color/Fusion output cache.
- Expose 36 tools by default, with 119 experimental tools explicitly opt-in
  and seven unimplemented ML tools unavailable. Reject unsupported explicit
  title, generator and Fusion template placement before editing.
- Include installer, bridge, manifests and docs in the source distribution.
  Build repeatable wheel and sdist with pinned tools and a fixed source epoch.

## Initial implementation — 2026-09-15 (not a published release)

### Added

- Initial independent implementation of DaVinci Resolve MCP server
- Modular architecture: server / bridge / tools / schemas separation
- 162 typed tools across 9 categories (project, timeline, media, clips, color, fusion, audio, render, gallery)
- Structured tool registry with read/write classification
- Local-first HTTP bridge (127.0.0.1:9876) with timeouts and retries
- Structured error handling with deterministic error codes
- Comprehensive schema definitions with validation
- Test suite: registry consistency, manifest validation, bridge protocol, schema validation
- GitHub Actions CI with pinned actions
- Locked dependencies via uv with hash verification
- Windows install script with SHA-256 verification
- Optional autostart for DaVinci Resolve

### Changed

- Complete rewrite replacing vendored upstream implementation
- New tool registry as single source of truth
- Manifest derived from registry, not manually maintained
- Vendor-neutral documentation (no Claude/Anthropic references)
- Author metadata updated to Kerwil Gil

### Removed

- All upstream/vendor references (hiteshK03, MARTE)
- NOTICE.md (no third-party code remains)
- MIGRATION_FROM_MARTE.md