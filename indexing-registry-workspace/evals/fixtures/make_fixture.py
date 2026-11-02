#!/usr/bin/env python3
"""Build the workspace an indexing-registry eval starts from, in this release's formats.

Usage: python3 make_fixture.py <fixture-name> <target-dir>
       python3 make_fixture.py --list

- stale-tools: Client Follow-Up at state 5 (its plan waits for approval, so Design owns it) from the
  shared routing-state library (framework-fixtures/states/s05-plan-to-approve/with-registry), with
  the registry tools and dashboard page of an earlier version laid over it: `tools/` copied before
  TOOLS_VERSION existed (each file carries a `stale-tools-9.1.0` or `stale-template-9.1.0` marker) and
  a `registry-dashboard.html` built from that template, both from framework-fixtures/seeds/sales-stale-tools.
  IR1 runs Design on it (the update offer in Design's closing maintenance pass) and a direct
  "update my registry".
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FF = ROOT / "framework-fixtures"


def fx_stale_tools(t):
    shutil.copytree(FF / "states" / "s05-plan-to-approve" / "with-registry", t, symlinks=True)
    seed = FF / "seeds" / "sales-stale-tools"
    shutil.copytree(seed / "tools", Path(t) / "tools")
    shutil.copy2(seed / "registry-dashboard.html", Path(t) / "registry-dashboard.html")


FIXTURES = {"stale-tools": fx_stale_tools}


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print("\n".join(FIXTURES))
        sys.exit(0)
    if len(sys.argv) != 3 or sys.argv[1] not in FIXTURES:
        sys.exit(__doc__)
    target = Path(sys.argv[2])
    if target.exists():
        sys.exit(f"{target} already exists; pass a new folder")
    target.parent.mkdir(parents=True, exist_ok=True)
    FIXTURES[sys.argv[1]](target)
    print(target)
