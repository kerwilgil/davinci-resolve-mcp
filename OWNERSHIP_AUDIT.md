# OWNERSHIP AUDIT - davinci-resolve-mcp (FINAL STATE)

## Classification of Current Files

### EXACT_UPSTREAM (byte-for-byte identical to hiteshK03/davinci-resolve-mcp@f812df7)
- **REMOVED**: `src/CursorBridge.py` — was SHA: 10f5870ccebfb9c18e67beeff1c8261c59c9055c
- **REMOVED**: `src/resolve_mcp_bridge.py` — was SHA: a3beddab78541510f172d462726b09fe4a8c0c84

### DERIVED (modified from upstream)
- None

### ORIGINAL (written for this repo, not derived from upstream)
- `src/davinci_mcp/` — complete new modular implementation
  - `server.py` — MCP server entry point
  - `config.py` — configuration
  - `errors.py` — structured error types
  - `bridge/` — HTTP bridge client (protocol.py, transport.py, client.py)
  - `schemas/` — tool schemas (9 category modules + common + registry)
  - `tools/` — tool implementations (9 category modules + registry)
- `manifests/tool-manifest.json` — derived from new registry
- `tests/` — comprehensive test suite (78 tests passing)
- `scripts/install.ps1` — installer for new architecture
- `scripts/autostart.py` — autostart for DaVinci Resolve
- `.github/workflows/ci.yml` — CI configuration
- `examples/mcp.json` — example MCP configuration
- `requirements.in` / `requirements.lock` — dependency specifications
- `README.md` — standalone project documentation
- `CHANGELOG.md` — project changelog
- `LICENSE` — MIT License, Copyright Kerwil Gil
- `pyproject.toml` — package metadata, author Kerwil Gil

### GENERATED
- `requirements.lock` — generated from requirements.in via uv

### DEPENDENCY_METADATA
- `requirements.in`
- `requirements.lock`
- `pyproject.toml`

## Files Requiring Rewrite (REWRITE_REQUIRED) - ALL COMPLETED

### Core Implementation Files (replaced with original implementations) ✅
1. `src/CursorBridge.py` — **REMOVED** (was EXACT_UPSTREAM)
2. `src/resolve_mcp_bridge.py` — **REMOVED** (was EXACT_UPSTREAM)
3. **NEW**: `src/davinci_mcp/` — complete modular implementation

### Legal/Attribution Files (updated after rewrite) ✅
1. `LICENSE` — **UPDATED**: Copyright Kerwil Gil
2. `NOTICE.md` — **REMOVED** (no third-party code remains)
3. `pyproject.toml` — **UPDATED**: author Kerwil Gil, no upstream URL
4. `README.md` — **REWRITTEN**: independent project documentation
5. `CHANGELOG.md` — **REWRITTEN**: independent project history
6. `MIGRATION_FROM_MARTE.md` — **REMOVED**

### Documentation/Config Files (upstream/MARTE references removed) ✅
1. `README.md` — no mentions of MARTE, hiteshK03, upstream, vendoring
2. `scripts/install.ps1` — updated for new architecture
3. `manifests/tool-manifest.json` — derived from new registry, no upstream fields

## Summary

| Category | Count | Status |
|---|---|---|
| EXACT_UPSTREAM | 0 | **REMOVED** |
| DERIVED | 0 | — |
| ORIGINAL | 50+ | **NEW ARCHITECTURE** |
| GENERATED | 1 | requirements.lock |
| DEPENDENCY_METADATA | 3 | requirements.in, requirements.lock, pyproject.toml |
| REWRITE_REQUIRED (core) | 2 | **COMPLETED** |
| REWRITE_REQUIRED (legal) | 6 | **COMPLETED** |

## Target State - ACHIEVED

- ✅ EXACT_UPSTREAM_SOURCE_FILES: 0
- ✅ DERIVED_UPSTREAM_SOURCE_FILES: 0
- ✅ THIRD_PARTY_SOURCE_FILES_REMAINING: 0
- ✅ DERIVED_SOURCE_FILES_REMAINING: 0
- ✅ All tests passing (78/78)
- ✅ License: Kerwil Gil
- ✅ pyproject.toml author: Kerwil Gil
- ✅ No upstream/MARTE/IA references in code
- ✅ Vendor-neutral documentation

## Architecture Verification

The new implementation provides:
- Modular architecture: server / bridge / tools / schemas separation
- 162 typed tools across 9 categories
- Structured tool registry with read/write classification
- Local-first HTTP bridge (127.0.0.1:9876) with timeouts and retries
- Structured error handling with deterministic error codes
- Comprehensive schema definitions with validation
- Test suite: registry consistency, manifest validation, bridge protocol, schema validation
- GitHub Actions CI with pinned actions
- Locked dependencies via uv with hash verification
- Windows install script with SHA-256 verification
- Optional autostart for DaVinci Resolve