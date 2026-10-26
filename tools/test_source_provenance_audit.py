#!/usr/bin/env python3
"""Regression tests for source provenance audit output."""
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/audit_source_provenance.py"
PATCH = ROOT / "patches/save-flow-3.4.1/ReflexAiClient.java"
REL = "src/main/java/com/example/reflexai/client/ReflexAiClient.java"

def make_project(root: Path, client: bytes) -> Path:
    project = root / "project"
    for rel in ("src/main/resources", "src/main/java/com/example/reflexai/client"):
        (project / rel).mkdir(parents=True, exist_ok=True)
    for rel in ("settings.gradle", "build.gradle"):
        (project / rel).write_text("// test fixture\n", encoding="utf-8")
    (project / "gradle.properties").write_text("minecraft_version=1.21.11\nmod_version=3.4.0\n", encoding="utf-8")
    (project / "src/main/resources/fabric.mod.json").write_text("{}\n", encoding="utf-8")
    (project / REL).write_bytes(client)
    return project

def main() -> int:
    tests = 0
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        patch = PATCH.read_bytes()
        project = make_project(root, patch)
        archive = root / "source.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("sample/" + REL, patch)
        p = subprocess.run([sys.executable, str(SCRIPT), str(project), str(archive)], text=True, capture_output=True)
        assert p.returncode == 0, p.stdout + p.stderr
        assert "archive client matches extracted project: True" in p.stdout
        assert "patch and extracted project source match byte-for-byte" in p.stdout
        tests += 1
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("sample/" + REL, patch + b"\n// archive-only change\n")
        p = subprocess.run([sys.executable, str(SCRIPT), str(project), str(archive)], text=True, capture_output=True)
        assert p.returncode == 0, p.stdout + p.stderr
        assert "archive client matches extracted project: False" in p.stdout
        assert "different snapshots" in p.stdout
        tests += 1
        p = subprocess.run([sys.executable, str(SCRIPT), str(root / "missing-project")], text=True, capture_output=True)
        assert p.returncode == 2
        assert "project directory not found" in p.stdout
        tests += 1
    print(f"PASS: {tests}/3 source provenance audit tests")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
