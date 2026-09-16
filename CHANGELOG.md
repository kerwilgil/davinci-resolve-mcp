# Changelog

All notable changes to this project are documented in this file.

## [1.0.0] - 2026-09-15

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