# Source integration and provenance audit

## Verified source snapshots

In the extracted local directory `ReflexAI-Fabric-3.4.0/`, the client entrypoint:

`src/main/java/com/example/reflexai/client/ReflexAiClient.java`

is byte-identical to `patches/save-flow-3.4.1/ReflexAiClient.java`. Both SHA-256 hashes are:

`1a4fbbcb6f927f7ad1d4d40b4379996cfeb3686ca56c112ac71e25121ab555dd`

**Correction: the same-named `ReflexAI-Fabric-3.4.0-source.zip` is not the same snapshot as the extracted directory.** The ZIP passes CRC validation and contains 29 entries, but its client source SHA-256 is `b7797a1688062232bfda6dc21555c6033597a41b87867cc640c1a869494d80a1`, different from both the extracted directory and patch. The files differ in the create-world flow, including `pendingTrainingWorldStart`. Do not treat the ZIP and extracted tree as interchangeable.

## Reproduce the audit

```sh
python3 tools/audit_source_provenance.py /path/to/ReflexAI-Fabric-3.4.0 /path/to/ReflexAI-Fabric-3.4.0-source.zip
python3 tools/test_source_provenance_audit.py
```

The audit is read-only. It does not alter files, download dependencies, run Gradle, compile the mod, or launch Minecraft.

See [BUILD-READINESS-REPORT.md](BUILD-READINESS-REPORT.md) for the current build blockers.
