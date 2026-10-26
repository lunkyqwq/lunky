# Source snapshot comparison report

## Scope

This report compares the local source directory `/mnt/data/ReflexAI-Fabric-3.4.0` with `/mnt/data/ReflexAI-Fabric-3.4.0-source.zip` as present in the working environment on 2026-10-26. It is a local audit record, not a claim that the archive is the canonical upstream release.

## Results

The ZIP passes its internal CRC test (29 entries), but the full file-by-file comparison does **not** match:

- `README.md` has different contents between the archive and extracted directory.
- `src/main/java/com/example/reflexai/client/ReflexAiClient.java` has different contents. The extracted directory's client is byte-identical to `patches/save-flow-3.4.1/ReflexAiClient.java` (SHA-256 `1a4fbbcb6f927f7ad1d4d40b4379996cfeb3686ca56c112ac71e25121ab555dd`). The archived client has SHA-256 `b7797a1688062232bfda6dc21555c6033597a41b87867cc640c1a869494d80a1`.
- One Chinese-named text file appears under different decoded names in the ZIP and extracted directory. The ZIP lists `Σ╕ÇΘö«µï┐σê░µêÉσôüJAR.txt`, while the directory has `一键拿到成品JAR.txt`. This may be a ZIP filename-encoding issue; do not assume they are the same file without inspecting the raw archive metadata.

The full comparison tool reports 15 files on each side, one directory-only path, one ZIP-only path, and two content differences. The existing targeted provenance audit independently confirms the client-source mismatch.

## Reproduce

```bash
python3 tools/audit_source_archive.py /path/to/ReflexAI-Fabric-3.4.0-source.zip /path/to/ReflexAI-Fabric-3.4.0
python3 tools/audit_source_provenance.py /path/to/ReflexAI-Fabric-3.4.0 /path/to/ReflexAI-Fabric-3.4.0-source.zip
python3 tools/test_audit_source_archive.py
```

The first command returns exit code `1` when snapshots differ. The audit is read-only and does not extract files, download dependencies, run Gradle, compile the mod, or launch Minecraft. Generated folders (`.git`, `.gradle`, `build`, `out`, `__pycache__`, `.idea`) are excluded.

## Decision

Do not treat the ZIP and extracted directory as interchangeable build inputs. Select and archive one canonical source snapshot, then rerun this comparison before any build attempt. The repository's patch remains source-only; this report does not establish successful compilation or in-game behavior.
