# 1.0.0 — first public release candidate (unpublished)

**Status: BLOCKED.** Review [validation and remaining work](RELEASE_VALIDATION.md)
before approving a tag or release.

This candidate secures the local HTTP bridge with mandatory bearer authentication,
removes browser/CORS access and internal trace disclosure, and prevents automatic
replay of mutations. Communication failures after POST report an unknown outcome.

The project now installs as a Python package with a console entry point and module
launch. MCP stdio publishes real schemas for 162 declared tools. Route mappings,
JSON validation, context selection and several core write contracts are corrected.
Seven unimplemented ML tools return an explicit unavailable error. Unsupported
mutation options are rejected before execution.

The Windows helper preserves existing server options and unrelated configuration,
backs up installations and restores previous files/configuration on failure.
Core dependencies are hash-locked for multiple platforms; MCP is updated to 1.30.0.

Install from the reviewed checkout using the commands in [README](README.md).
Configure the same private `DAVINCI_BRIDGE_TOKEN` in Resolve and the MCP client.
Stop the old unauthenticated bridge before upgrading. Do not put credentials in
source control. After a mutation timeout inspect Resolve before manually retrying.

Real Resolve, Free/Studio compatibility, the real Claude CLI and several argument
adapters remain pending. No packages, tags, releases or installer binaries were
published. MIT license retained.
