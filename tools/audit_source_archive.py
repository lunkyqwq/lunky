#!/usr/bin/env python3
"""Read-only comparison of a source ZIP against an extracted source directory."""
from hashlib import sha256
from pathlib import Path, PurePosixPath
import argparse
import zipfile

IGNORED_PARTS = {".git", ".gradle", "build", "out", "__pycache__", ".idea"}


def safe_name(name: str) -> str | None:
    p = PurePosixPath(name.replace("\\", "/"))
    if p.is_absolute() or any(part in ("..", "") for part in p.parts):
        return None
    clean = str(p)
    if not clean or clean == "." or any(part in IGNORED_PARTS for part in p.parts):
        return None
    return clean


def archive_files(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as zf:
        files = {}
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = safe_name(info.filename)
            if name is None:
                if ".." in PurePosixPath(info.filename.replace("\\", "/")).parts or info.filename.startswith(("/", "\\")):
                    raise ValueError(f"unsafe ZIP entry path: {info.filename}")
                continue
            if name in files:
                raise ValueError(f"duplicate ZIP entry path: {name}")
            files[name] = zf.read(info)
    all_parts = [PurePosixPath(n).parts for n in files]
    if all_parts and all(len(p) > 1 for p in all_parts) and len({p[0] for p in all_parts}) == 1:
        prefix = all_parts[0][0]
        files = {str(PurePosixPath(n).relative_to(prefix)): data for n, data in files.items()}
    return files


def directory_files(path: Path) -> dict[str, bytes]:
    files = {}
    for item in path.rglob("*"):
        if item.is_symlink() or not item.is_file():
            continue
        rel = item.relative_to(path)
        if any(part in IGNORED_PARTS for part in rel.parts):
            continue
        name = safe_name(rel.as_posix())
        if name is not None:
            files[name] = item.read_bytes()
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="source ZIP archive")
    parser.add_argument("directory", type=Path, help="extracted source directory")
    args = parser.parse_args()
    if not args.archive.is_file() or not zipfile.is_zipfile(args.archive):
        print(f"FAIL: not a readable ZIP archive: {args.archive}")
        return 2
    if not args.directory.is_dir():
        print(f"FAIL: source directory does not exist: {args.directory}")
        return 2
    try:
        zipped = archive_files(args.archive)
        extracted = directory_files(args.directory)
    except (OSError, zipfile.BadZipFile, ValueError) as exc:
        print(f"FAIL: could not audit source snapshot: {exc}")
        return 2
    zip_names, dir_names = set(zipped), set(extracted)
    missing = sorted(dir_names - zip_names)
    extra = sorted(zip_names - dir_names)
    changed = sorted(name for name in zip_names & dir_names if sha256(zipped[name]).digest() != sha256(extracted[name]).digest())
    for name in missing:
        print(f"DIRECTORY-ONLY: {name}")
    for name in extra:
        print(f"ZIP-ONLY: {name}")
    for name in changed:
        print(f"CONTENT-DIFFERS: {name}")
    if missing or extra or changed:
        print(f"FAIL: snapshots differ (ZIP={len(zipped)}, directory={len(extracted)}, directory-only={len(missing)}, ZIP-only={len(extra)}, changed={len(changed)})")
        return 1
    print(f"PASS: snapshots match ({len(zipped)} files; generated folders excluded)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
