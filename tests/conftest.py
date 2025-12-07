import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG_ROOT = ROOT / "lb_unixbench_plugin"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(PKG_ROOT))
