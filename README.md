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

- The static regression checker covers **16 source, ordering, helper, documentation, and delimiter checks**.
- The GitHub Actions workflow runs the reusable static checker on relevant changes.
- **Gradle compilation and Minecraft 1.21.11 in-game testing have not been completed here.**
- This repository does **not** currently contain the full project source tree and the patch is **not** a compiled `.jar`.

Use [SAVE-FLOW-TEST-PLAN.md](SAVE-FLOW-TEST-PLAN.md) to test first launch, cancellation, manual re-entry, and protection of existing saves in a backed-up test instance. A successful static check is not proof of a successful game build.
