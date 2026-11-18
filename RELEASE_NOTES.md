# DaVinci Resolve MCP 1.0.0 candidate

The first public candidate installs as a Python package and exposes 36 supported
tools over MCP stdio. The default scope covers project and timeline inspection,
media import, selected edits and exports, render control, and validated gallery,
take and cache operations. The [manifest](manifests/tool-manifest.json) lists
119 opt-in experimental tools and seven unavailable ML tools.

The loopback bridge requires authentication and rejects browser-origin requests.
Mutations are submitted once. If render completion cannot be confirmed, the
server reports an unknown outcome and returns the accepted job IDs when known.
Named selectors and export destinations are checked before sensitive operations.

Use the [installation instructions](README.md) to install the locked core and
configure the bridge token. The Windows helper retains previous installation and
configuration state on failure. The source distribution includes the helper,
bridge script, manifest and release documentation. Build metadata declares MIT.

Physical Resolve testing is **PENDING**. Follow the disposable-project checklist
before claiming version or edition compatibility. [Validation](RELEASE_VALIDATION.md)
