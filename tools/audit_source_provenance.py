#!/usr/bin/env python3
"""Read-only provenance/build-readiness audit for Reflex AI source snapshots."""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import sys

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "patches/save-flow-3.4.1/ReflexAiClient.java"
CLIENT_REL = Path("src/main/java/com/example/reflexai/client/ReflexAiClient.java")
REQUIRED = [
    Path("settings.gradle"), Path("build.gradle"), Path("gradle.properties"),
    Path("src/main/resources/fabric.mod.json"),
]

def digest(data: bytes) -> str:
    return sha256(data).hexdigest()

def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: python3 tools/audit_source_provenance.py PROJECT_DIR [SOURCE_ARCHIVE.zip]")
        return 2
    project = Path(sys.argv[1]).expanduser().resolve()
    archive = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) == 3 else None
    if not project.is_dir():
        print(f"FAIL: project directory not found: {project}")
        return 2
    failed = False
    for rel in REQUIRED:
        ok = (project / rel).is_file()
        print(f"{'PASS' if ok else 'FAIL'} project file: {rel.as_posix()}")
        failed |= not ok
    for rel in (Path("gradlew"), Path("gradlew.bat"), Path("gradle/wrapper/gradle-wrapper.jar"), Path("gradle/wrapper/gradle-wrapper.properties")):
        present = (project / rel).exists()
        print(f"{'PASS' if present else 'INFO'} wrapper component: {rel.as_posix()} {'present' if present else 'missing'}")
    if not PATCH.is_file() or not (project / CLIENT_REL).is_file():
        print("FAIL patch/client source missing; cannot compare")
        return 1
    patch_data = PATCH.read_bytes()
    project_data = (project / CLIENT_REL).read_bytes()
    print(f"Patch SHA-256:   {digest(patch_data)}")
    print(f"Project SHA-256: {digest(project_data)}")
    print(f"{'PASS' if patch_data == project_data else 'INFO'} patch and extracted project source {'match byte-for-byte' if patch_data == project_data else 'DIFFER'}")
    props = (project / "gradle.properties").read_text(encoding="utf-8")
    for needle in ("minecraft_version=1.21.11", "mod_version=3.4.0"):
        ok = needle in props
        print(f"{'PASS' if ok else 'INFO'} metadata: {needle}")
    if archive:
        if not archive.is_file():
            print(f"FAIL archive not found: {archive}")
            return 2
        try:
            with ZipFile(archive) as zf:
                bad = zf.testzip()
                names = zf.namelist()
                if bad:
                    print(f"FAIL archive CRC check: {bad}")
                    return 1
                print(f"PASS archive CRC check; entries={len(names)}")
                matching = next((n for n in names if n.endswith("/" + CLIENT_REL.as_posix())), None)
                if matching:
                    archived_data = zf.read(matching)
                    print(f"Archive SHA-256: {digest(archived_data)}")
                    same_project = archived_data == project_data
                    same_patch = archived_data == patch_data
                    print(f"{'PASS' if same_project else 'INFO'} archive client matches extracted project: {same_project}")
                    print(f"{'PASS' if same_patch else 'INFO'} archive client matches patch: {same_patch}")
                    if not same_project:
                        print("WARNING: source ZIP and extracted project are different snapshots; do not treat them as interchangeable.")
                else:
                    print("INFO archive does not contain the expected client source path")
        except BadZipFile:
            print("FAIL archive is not a valid ZIP")
            return 1
    print("NOTE: read-only audit; no dependency download, Gradle run, compilation, or game launch.")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
