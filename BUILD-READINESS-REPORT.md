# Build-readiness report (2026-10-26)

## Verified
- The extracted project contains `build.gradle`, `settings.gradle`, `gradle.properties`, and `src/main/resources/fabric.mod.json`.
- Metadata declares Minecraft 1.21.11, Yarn `1.21.11+build.6`, Fabric Loader `0.18.1`, Fabric API `0.141.1+1.21.11`, Java 21, and mod version `3.4.0`.
- The extracted project's client entrypoint is byte-identical to the save-flow patch.
- The source ZIP passes CRC validation, but its client entrypoint differs from the extracted directory. A full file-by-file comparison also finds a differing `README.md` and a Chinese-named text file whose decoded ZIP name differs from the directory name. See [SOURCE-SNAPSHOT-COMPARISON.md](SOURCE-SNAPSHOT-COMPARISON.md). These are not the same source snapshot.

## Blockers
1. No `gradle` command is installed in the current environment.
2. The extracted project has no `gradlew`, `gradlew.bat`, or `gradle/wrapper` files.
3. The full ZIP-versus-directory audit reports 15 files on each side, one directory-only path, one ZIP-only path, and two content differences; the Chinese filename may also reflect ZIP filename-encoding behavior.\n4. No Gradle build, Minecraft launch, or in-game test was run in this pass.

## Status
- Save-flow source integration: confirmed for the extracted directory.
- Archive consistency: not passed (full source snapshots differ; see [SOURCE-SNAPSHOT-COMPARISON.md](SOURCE-SNAPSHOT-COMPARISON.md)).
- Reproducible build: not verified.
- Installable JAR: not produced or verified.

Audit command:

```sh
python3 tools/audit_source_provenance.py /path/to/ReflexAI-Fabric-3.4.0 /path/to/ReflexAI-Fabric-3.4.0-source.zip\npython3 tools/audit_source_archive.py /path/to/ReflexAI-Fabric-3.4.0-source.zip /path/to/ReflexAI-Fabric-3.4.0
```
