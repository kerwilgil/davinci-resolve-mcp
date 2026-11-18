# Release validation — 1.0.0 candidate

Decision: **BLOCKED**. No release, tag, PyPI upload or automatic merge is authorized.

## Evidence

- Baseline: `main` at `8c5a7f96621e8ecd6fe3ce629e48a51940fa97b9`; clean checkout,
  last existing CI successful. No existing tags or releases found.
- Local host: macOS arm64, Python 3.11.15. **102 tests passed**, including successful installed stdio read/write and the
  unsupported-selector guard. Cross-platform results are recorded in PR checks.
- Built wheel and sdist; installed wheel in an isolated virtual environment.
  Real MCP SDK client initializes subprocesses from an unrelated temporary
  working directory via both module and console entry point. Discovers all 162
  declared tools with exact properties/required fields; checks invalid arguments,
  disconnected calls and successful read/write against a controlled HTTP bridge.
- Controlled HTTP tests cover authenticated reads/writes, missing/wrong tokens
  across every route, Host/Origin rejection, malformed/bounded JSON, trace
  redaction, context/clip selection and timeout/non-replayed mutation behavior.
- Runtime correctness lint and `git diff --check` pass. Style modernization was
  intentionally excluded from this correction.
- Gitleaks 8.30.1: full Git history scanned with redaction, zero findings.
  Publication content is rescanned before push and in CI; no secret values are logged.
- Original core lock: 26 advisory records across five packages (some duplicates).
  Updated lock: pip-audit reports **no known vulnerabilities** with MCP 1.30.0.
  This covers the core lock, not unimplemented optional ML extras.
- CI now runs Python 3.11/3.13 on Ubuntu, macOS and Windows. Native Windows
  installer test uses real uv/Python/package installs and a controlled Claude
  CLI to verify preview, upgrade, rollback and preservation of configuration.
  The real Claude CLI and Resolve GUI integration remain PENDING.
- MIT license preserved. Package version remains 1.0.0; bridge API version 2.0.0
  is independent. Manifest `verified_tools` is a legacy declaration, not evidence.

## Blocking functional gaps

The route mapping now covers all 155 tools with bridge implementations. Endpoint
presence does not establish argument semantics. Remaining concrete examples:

| Public tool/argument | Bridge contract / remaining work |
|---|---|
| `set_playhead(frame)` | Bridge requires timecode; frame/drop-frame conversion needs implementation and tests |
| `delete_render_job(job_index)` / `get_render_job_status(job_index)` | Bridge expects a stable job ID; resolve and validate index before using the ID |
| `set_render_mode(mode)` | Public string enum differs from numeric `renderMode`; adapter and validation needed |
| `start_rendering(wait_for_completion)` | Bridge has no completion wait contract |
| `get_album_stills(album_name)` and gallery writes | Bridge primarily selects albums/stills by index; unique name/label resolution needed |
| `clip_names` in compound/link/delete operations | Bridge expects track/clip references; resolve every requested clip or reject the whole call |
| `database_name` in project operations | Database identity must be validated before project mutation |
| title/generator insertion track/frame options | Bridge inserts at current playhead; explicit placement is not implemented |
| several Fusion, cache, take and export options | Further semantic adapters require focused regression tests |
| seven ML tools | No bridge implementation; explicitly return `TOOL_UNAVAILABLE` |

Mutation body allowlists now reject unrecognized selectors/options **before any
mutation**, instead of allowing ignored arguments to act on a default target.
Named timeline/project scopes must match the current context. Named timeline
clips must be unique. These are safeguards, not claims that remaining semantics
are implemented. Legacy direct HTTP bodies remain usable when they match the
actual bridge contract.

## Physical integration and compatibility

**PENDING**: DaVinci Resolve was not found in `/Applications`; no personal
projects were opened or modified. Resolve Free/Studio and version compatibility
have not been certified. Earlier README claims that Resolve 18+, Free operation,
or a particular Studio feature worked were removed because no evidence was found.

To unblock, use only a disposable project: validate status/project reads, create a
new timeline, import generated media, insert/delete only generated items, export
to a temporary directory and validate errors. Record Resolve version, edition,
OS, embedded Python and observed results per tool. Feature names or manifest
membership cannot certify Free/Studio support. Do not test against personal clips,
timelines, renders or project files.

## Correction cycles

1. Baseline and root causes: authentication, POST replay, frozen request mutation,
   package/entry point, MCP schema publication and registry validation.
2. Controlled regressions: HTTP authorization and errors, route mapping, argument
   normalization, clip/context safety and installed-wheel MCP subprocesses.
3. Focused final checks: vulnerable SDK/lock update, cross-platform CI, installer
   preservation/rollback and fail-closed handling of unsupported mutation fields.

The independent-review limitation is explicit: this audit was performed by one
agent. Remaining semantic work is recorded above rather than represented as PASS.
