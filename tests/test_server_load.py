"""Smoke tests: the MCP server module imports cleanly and registers its tools.

Heavy optional dependencies (faster-whisper, demucs, rembg, soundfile) are
imported lazily inside individual tool functions, so importing the module
only requires the `mcp` package -- no DaVinci Resolve installation and no
ML dependencies needed to run this file.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "src" / "resolve_mcp_bridge.py"


def _load_server_module():
    spec = importlib.util.spec_from_file_location("resolve_mcp_bridge", SERVER_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ServerLoadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = _load_server_module()

    def test_module_imports(self):
        self.assertTrue(hasattr(self.module, "mcp"))

    def test_host_and_port_are_localhost_only(self):
        # CursorBridge.py binds the HTTP bridge; resolve_mcp_bridge.py talks
        # to it. Both must stay on localhost -- this project is not designed
        # to be exposed on a network interface.
        bridge_text = (ROOT / "src" / "CursorBridge.py").read_text(encoding="utf-8")
        self.assertIn('HOST = "127.0.0.1"', bridge_text)

    def test_key_tools_are_present_as_attributes_or_functions(self):
        for name in ("get_resolve_status", "create_timeline", "insert_to_timeline"):
            self.assertTrue(hasattr(self.module, name), f"missing {name}")

    def test_get_resolve_status_handles_unreachable_bridge(self):
        # With no CursorBridge running, the tool must return a structured
        # error rather than raise, so an MCP client gets a usable response.
        result = self.module.get_resolve_status()
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main()
