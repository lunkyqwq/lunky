#!/usr/bin/env python3
"""Mutation tests proving the static checker rejects selected regressions."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REL = Path("patches/save-flow-3.4.1/ReflexAiClient.java")
HELPER_REL = Path("patches/save-flow-3.4.1/apply-save-flow-patch.ps1")
CHECKER_REL = Path("tools/check_save_flow_patch.py")

mutations = [
    ("missing title button", SOURCE_REL, 'Reflex AI 训练存档', 'Reflex AI 训练入口'),
    ("missing world-entry guard", SOURCE_REL, 'if (pendingTrainingWorldStart && client.world != null)', 'if (false && client.world != null)'),
    ("missing helper checksum verification", HELPER_REL, '$stagedHash -ne $sourceHash', '$stagedHash -eq $sourceHash'),
]

failed = False
with tempfile.TemporaryDirectory(prefix="save-flow-mutation-") as tmp:
    temp_root = Path(tmp)
    for label, rel, old, new in mutations:
        case_root = temp_root / label.replace(" ", "-")
        shutil.copytree(ROOT, case_root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        target = case_root / rel
        content = target.read_text(encoding="utf-8")
        if old not in content:
            print(f"FAIL: {label} (mutation anchor not found)")
            failed = True
            continue
        target.write_text(content.replace(old, new, 1), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(case_root / CHECKER_REL)],
            cwd=case_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        ok = result.returncode != 0
        print(f"{'PASS' if ok else 'FAIL'}: checker rejects {label}")
        if not ok:
            print(result.stdout)
            failed = True

sys.exit(1 if failed else 0)
