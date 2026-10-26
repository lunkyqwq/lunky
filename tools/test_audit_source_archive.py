#!/usr/bin/env python3
"""Regression tests for ZIP-versus-directory source snapshot audit."""
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

SCRIPT = Path(__file__).with_name("audit_source_archive.py")


def run(archive: Path, directory: Path):
    return subprocess.run([sys.executable, str(SCRIPT), str(archive), str(directory)], capture_output=True, text=True)


def main() -> int:
    count = 0
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        src = base / "src"
        (src / "src/main").mkdir(parents=True)
        (src / "src/main/A.java").write_text("class A {}\n", encoding="utf-8")
        (src / "README.md").write_text("same\n", encoding="utf-8")
        archive = base / "source.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            for file in src.rglob("*"):
                if file.is_file():
                    zf.write(file, Path("project-root") / file.relative_to(src))
        result = run(archive, src)
        assert result.returncode == 0 and "snapshots match (2 files" in result.stdout, result.stdout + result.stderr
        count += 1
        (src / "README.md").write_text("changed\n", encoding="utf-8")
        result = run(archive, src)
        assert result.returncode == 1 and "CONTENT-DIFFERS: README.md" in result.stdout, result.stdout + result.stderr
        count += 1
        (src / "README.md").unlink()
        (src / "extra.txt").write_text("extra\n", encoding="utf-8")
        result = run(archive, src)
        assert result.returncode == 1 and "ZIP-ONLY: README.md" in result.stdout and "DIRECTORY-ONLY: extra.txt" in result.stdout, result.stdout + result.stderr
        count += 1
        bad = base / "unsafe.zip"
        with zipfile.ZipFile(bad, "w") as zf:
            zf.writestr("../outside.txt", "nope")
        result = run(bad, src)
        assert result.returncode == 2 and "unsafe ZIP entry path" in result.stdout, result.stdout + result.stderr
        count += 1
    print(f"PASS: {count}/4 source archive audit tests")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
