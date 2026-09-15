# Changelog

All notable changes to this project are documented in this file.

## [0.1.0] - 2026-09-15

### Added

- Initial standalone release, extracted from a private monorepo's editor
  tooling. Vendors `hiteshK03/davinci-resolve-mcp` at commit
  `f812df7ab5d376592a24fb94611473fdf3a1acb2` (MIT).
- `manifests/tool-manifest.json`: the audited list of verified tools, now
  including `create_timeline` and `insert_to_timeline` (previously
  documented by a downstream skill but missing from the manifest -- the
  root cause this extraction resolved).
- Test suite validating the manifest against the vendored source
  (`tests/test_manifest.py`) and a server import/smoke test
  (`tests/test_server_load.py`).
- `scripts/install.ps1`: installs a locked Python 3.11 environment, copies
  and hash-verifies `CursorBridge.py` into DaVinci Resolve's Scripts/Utility
  folder, and registers the server with Claude Code.
- `scripts/autostart.py`: opt-in autostart script for DaVinci Resolve's
  Scripts/Start folder.
- GitHub Actions CI running the test suite on every push and pull request.
