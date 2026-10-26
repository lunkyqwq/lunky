# Reflex AI — save-flow patch repository

This repository currently tracks the **3.4.1 independent training-save UI patch**, not the complete Reflex AI Fabric mod source tree.

**中文说明：** [README-zh-CN.md](README-zh-CN.md)

## Current patch

- Source file: [ReflexAiClient.java](patches/save-flow-3.4.1/ReflexAiClient.java)
- Notes and application steps: [PATCH-NOTES.md](patches/save-flow-3.4.1/PATCH-NOTES.md)
- Manual test and acceptance checklist: [SAVE-FLOW-TEST-PLAN.md](SAVE-FLOW-TEST-PLAN.md)
- Reusable static regression checker: [check_save_flow_patch.py](tools/check_save_flow_patch.py)
- GitHub Actions workflow: [Verify save-flow patch](.github/workflows/verify-save-flow-patch.yml)

The patch opens Minecraft's normal Create World screen, prefills the name `Reflex AI Training`, and keeps a title-screen button for reopening the flow. It does not silently create a world or overwrite an existing save. The first-launch marker should be written only after the client actually enters a world through this flow.

## How to apply

Apply the patched Java file to a matching full source project. The PowerShell helper makes a timestamped backup before replacing the target file. Read [PATCH-NOTES.md](patches/save-flow-3.4.1/PATCH-NOTES.md) first and pass the correct project root to the script. The helper does not compile or install anything.

## Verification status

- The static regression checker covers **21 source, ordering, helper-safety, documentation, and delimiter checks**.
- The GitHub Actions workflow runs the reusable static checker on relevant changes.
- **Gradle compilation and Minecraft 1.21.11 in-game testing have not been completed here.**
- This repository does **not** currently contain the full project source tree and the patch is **not** a compiled `.jar`.

Use [SAVE-FLOW-TEST-PLAN.md](SAVE-FLOW-TEST-PLAN.md) to test first launch, cancellation, manual re-entry, and protection of existing saves in a backed-up test instance. A successful static check is not proof of a successful game build.


Checker mutation tests: `python3 tools/test_save_flow_checker.py`.


Checker mutation tests: `python3 tools/test_save_flow_checker.py`.


## Source snapshot provenance audit

The extracted 3.4.0 source tree has a client file byte-identical to the patch, but the same-named `ReflexAI-Fabric-3.4.0-source.zip` contains a different client snapshot. Do not treat them as interchangeable. See [SOURCE-INTEGRATION-AUDIT.md](SOURCE-INTEGRATION-AUDIT.md) and [BUILD-READINESS-REPORT.md](BUILD-READINESS-REPORT.md); run `python3 tools/audit_source_provenance.py /path/to/ReflexAI-Fabric-3.4.0 /path/to/ReflexAI-Fabric-3.4.0-source.zip` for a read-only comparison. Run `python3 tools/test_source_provenance_audit.py` to test the audit tool. This does not compile or test the mod.

## Full source archive comparison

The focused provenance audit checks the client entrypoint; `tools/audit_source_archive.py` compares all source files in a ZIP with an extracted directory, including added, missing, and changed files. The observed 3.4.0 ZIP/directory mismatch is recorded in [SOURCE-SNAPSHOT-COMPARISON.md](SOURCE-SNAPSHOT-COMPARISON.md). Run `python3 tools/test_audit_source_archive.py` for regression tests. The tool does not extract or modify the archive.

## Patch bundle integrity

`PATCH-BUNDLE-MANIFEST.sha256` records hashes for the source-only patch bundle. Run `python3 tools/update_patch_bundle_manifest.py` to regenerate the manifest and `python3 tools/update_patch_bundle_manifest.py --check` to detect stale entries. Then run `python3 tools/verify_patch_bundle.py` and `python3 tools/test_verify_patch_bundle.py` to verify file hashes and test tampering/path-traversal detection. The manifest does not prove the mod compiles or runs in Minecraft.
