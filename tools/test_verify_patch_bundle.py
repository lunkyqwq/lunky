#!/usr/bin/env python3
"""Mutation tests for patch bundle manifest verification."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/verify_patch_bundle.py"

def main() -> int:
    count = 0
    with tempfile.TemporaryDirectory() as temp:
        copy = Path(temp) / "bundle"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        target = copy / "patches/save-flow-3.4.1/PATCH-NOTES.md"
        target.write_text(target.read_text(encoding="utf-8") + "\nmutation\n", encoding="utf-8")
        p = subprocess.run([sys.executable, str(copy / "tools/verify_patch_bundle.py")], capture_output=True, text=True)
        assert p.returncode != 0, p.stdout + p.stderr
        assert "FAIL: patches/save-flow-3.4.1/PATCH-NOTES.md" in p.stdout
        count += 1
        manifest = copy / "PATCH-BUNDLE-MANIFEST.sha256"
        lines = manifest.read_text(encoding="utf-8").splitlines()
        manifest.write_text("\n".join(line for line in lines if not line.endswith("  tools/verify_patch_bundle.py")) + "\n", encoding="utf-8")
        p = subprocess.run([sys.executable, str(copy / "tools/verify_patch_bundle.py")], capture_output=True, text=True)
        assert p.returncode != 0, p.stdout + p.stderr
        assert "tools/verify_patch_bundle.py" in p.stdout
        count += 1
    print(f"PASS: {count}/2 bundle verifier mutation tests")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
