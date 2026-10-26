#!/usr/bin/env python3
"""Verify SHA-256 entries in PATCH-BUNDLE-MANIFEST.sha256 without modifying files."""
from hashlib import sha256
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "PATCH-BUNDLE-MANIFEST.sha256"
REQUIRED = (
    "README.md", "README-zh-CN.md", "SAVE-FLOW-TEST-PLAN.md",
    "SOURCE-INTEGRATION-AUDIT.md", "BUILD-READINESS-REPORT.md",
    "patches/save-flow-3.4.1/ReflexAiClient.java",
    "patches/save-flow-3.4.1/PATCH-NOTES.md",
    "patches/save-flow-3.4.1/apply-save-flow-patch.ps1",
    "tools/check_save_flow_patch.py", "tools/test_save_flow_checker.py",
    "tools/audit_local_source.py", "tools/audit_source_provenance.py",
    "tools/test_source_provenance_audit.py", "tools/verify_patch_bundle.py",
    "tools/test_verify_patch_bundle.py", "tools/update_patch_bundle_manifest.py",
    ".github/workflows/verify-save-flow-patch.yml",
)

def main() -> int:
    if not MANIFEST.is_file():
        print("FAIL: PATCH-BUNDLE-MANIFEST.sha256 is missing")
        return 1
    expected = {}
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2 or len(parts[0]) != 64 or any(c not in "0123456789abcdef" for c in parts[0]):
            print(f"FAIL: malformed manifest line {number}")
            return 1
        digest, name = parts
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or name in expected:
            print(f"FAIL: unsafe or duplicate manifest path on line {number}: {name}")
            return 1
        expected[name] = digest
    missing_required = sorted(set(REQUIRED) - set(expected))
    if missing_required:
        print("FAIL: required path(s) absent from manifest: " + ", ".join(missing_required))
        return 1
    failed = False
    for name, digest in expected.items():
        path = ROOT.joinpath(*PurePosixPath(name).parts)
        if not path.is_file():
            print(f"FAIL: missing file: {name}")
            failed = True
            continue
        actual = sha256(path.read_bytes()).hexdigest()
        ok = actual == digest
        print(f"{'PASS' if ok else 'FAIL'}: {name}")
        failed |= not ok
    print(f"{'FAIL' if failed else 'PASS'}: {len(expected)} manifest entries checked")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
