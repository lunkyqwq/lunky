#!/usr/bin/env python3
"""Audit whether the save-flow patch is already present in a local full source tree."""
from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PATCH_SOURCE = ROOT / "patches/save-flow-3.4.1/ReflexAiClient.java"
EXPECTED_SOURCE_REL = Path("src/main/java/com/example/reflexai/client/ReflexAiClient.java")
REQUIRED_PROJECT_FILES = [
    Path("settings.gradle"),
    Path("build.gradle"),
    Path("gradle.properties"),
    Path("src/main/resources/fabric.mod.json"),
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 tools/audit_local_source.py /path/to/ReflexAI-Fabric-project")
        return 2

    project = Path(sys.argv[1]).expanduser().resolve()
    if not project.is_dir():
        print(f"FAIL: project directory does not exist: {project}")
        return 2

    failed = False
    for relative in REQUIRED_PROJECT_FILES:
        ok = (project / relative).is_file()
        print(f"{'PASS' if ok else 'FAIL'}: project file {relative.as_posix()} exists")
        failed |= not ok

    patch_exists = PATCH_SOURCE.is_file()
    target = project / EXPECTED_SOURCE_REL
    target_exists = target.is_file()
    print(f"{'PASS' if patch_exists else 'FAIL'}: bundled patch source exists")
    print(f"{'PASS' if target_exists else 'FAIL'}: target client source exists")
    failed |= not patch_exists or not target_exists
    if failed:
        return 1

    patch_bytes = PATCH_SOURCE.read_bytes()
    target_bytes = target.read_bytes()
    patch_hash = sha256(patch_bytes).hexdigest()
    target_hash = sha256(target_bytes).hexdigest()
    print(f"Patch SHA-256:  {patch_hash}")
    print(f"Target SHA-256: {target_hash}")
    identical = patch_bytes == target_bytes
    print(f"{'PASS' if identical else 'INFO'}: source files {'are byte-identical' if identical else 'differ; review before applying anything'}")

    props = (project / "gradle.properties").read_text(encoding="utf-8")
    version_ok = "minecraft_version=1.21.11" in props and "mod_version=3.4.0" in props
    print(f"{'PASS' if version_ok else 'INFO'}: project metadata declares Minecraft 1.21.11 and mod version 3.4.0")
    if identical:
        print("RESULT: save-flow patch is already integrated; do not apply it again.")
        return 0
    print("RESULT: integration is not proven. This audit does not modify files or run Gradle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
