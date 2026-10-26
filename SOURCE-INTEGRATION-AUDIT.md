## Correction: source ZIP differs from extracted directory

The extracted `ReflexAI-Fabric-3.4.0/` client file is byte-identical to the patch (SHA-256 `1a4fbbcb6f927f7ad1d4d40b4379996cfeb3686ca56c112ac71e25121ab555dd`). However, `ReflexAI-Fabric-3.4.0-source.zip` passes CRC validation but its client file has SHA-256 `b7797a1688062232bfda6dc21555c6033597a41b87867cc640c1a869494d80a1` and differs from both. The ZIP and extracted directory must not be treated as the same snapshot.

Run `python3 tools/audit_source_provenance.py PROJECT_DIR SOURCE_ARCHIVE.zip` to check this locally. See `BUILD-READINESS-REPORT.md` for current build blockers. This audit is read-only and does not compile or launch Minecraft.
