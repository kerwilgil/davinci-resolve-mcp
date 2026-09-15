r"""
autostart.py
=============
Place this file in DaVinci Resolve's Scripts/Start folder:

  %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Start\

DaVinci Resolve runs every script in that folder automatically on startup.
This script launches CursorBridge in a daemon thread so it does not block
Resolve's own startup.

Requires CursorBridge.py to already be present in Scripts/Utility/ (normal
install location -- see scripts/install.ps1).

Autostart is opt-in: this script only launches the bridge if a marker file
named ".davinci-mcp-autostart-enabled" exists next to it. Without the
marker it exits immediately and prints how to enable it. This keeps the
write-capable bridge from listening on every Resolve launch by default.
"""

import threading
import sys
import os
import builtins

_start_dir = os.path.dirname(os.path.abspath(__file__))
_enable_marker = os.path.join(_start_dir, ".davinci-mcp-autostart-enabled")
if not os.path.isfile(_enable_marker):
    print("[autostart] Disabled: missing .davinci-mcp-autostart-enabled")
    print("[autostart] Start the bridge manually (Workspace > Scripts > CursorBridge)")
    print("[autostart] or re-run scripts/install.ps1 -EnableAutostart to opt in.")
    raise SystemExit(0)

# ---------------------------------------------------------------------------
# Step 1: capture Fusion's globals while still on the main thread
# (fu, bmd, fusion are only available here -- not inside a background thread)
# ---------------------------------------------------------------------------
for _name, _getter in [
    ("fu",     lambda: fu),       # noqa: F821
    ("bmd",    lambda: bmd),      # noqa: F821
    ("fusion", lambda: fusion),   # noqa: F821
]:
    try:
        setattr(builtins, _name, _getter())
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Step 2: add the Utility folder to sys.path so CursorBridge is importable
# ---------------------------------------------------------------------------
_utility_dir = os.path.normpath(os.path.join(_start_dir, "..", "Utility"))

if _utility_dir not in sys.path:
    sys.path.insert(0, _utility_dir)

# ---------------------------------------------------------------------------
# Step 3: launch CursorBridge on a daemon thread
#
# Importing CursorBridge from the thread means:
#   - _init_resolve() finds fu/bmd on builtins -> resolve_obj gets set
#   - server.serve_forever() blocks this thread (daemon) but not Resolve
#   - the daemon thread dies automatically when Resolve closes
# ---------------------------------------------------------------------------
def _run_cursor_bridge():
    try:
        import CursorBridge  # noqa -- runs the whole module, including serve_forever()
    except ImportError:
        print("[autostart] CursorBridge.py not found in: %s" % _utility_dir)
        print("[autostart] Make sure CursorBridge.py is in Scripts/Utility/")
    except Exception as _e:
        print("[autostart] Error starting the bridge: %s" % _e)


_bridge_thread = threading.Thread(target=_run_cursor_bridge, name="CursorBridgeThread", daemon=True)
_bridge_thread.start()

print("[autostart] Bridge starting in background (port 9876)...")
print("[autostart] No need to run Workspace > Scripts > CursorBridge manually.")
