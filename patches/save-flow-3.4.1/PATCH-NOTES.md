# Reflex AI save-flow patch 3.4.1

This folder contains a **source patch only**, not a complete Minecraft mod project and not a compiled JAR.

## What changed

- The first-launch marker is not written merely because the Create World screen opened.
- The marker is written only after the client enters a world created through this flow.
- Returning to the title screen without entering a world clears the pending state; the marker remains absent.
- The title-screen button remains available to reopen the Create World screen.
- The proposed save name is `Reflex AI Training`; cheats are enabled for that new save only after the user confirms world creation.

## Apply

Run `apply-save-flow-patch.ps1 -ProjectRoot "C:\path\to\full\project"` from this folder. The patched `ReflexAiClient.java` is beside the script in this repository. The helper checks that both source files exist, makes a timestamped backup of the target client file, and then copies the patched file into place. It does not run Gradle or install a JAR.

## Verify

- Static checks: run `python3 tools/check_save_flow_patch.py` from the repository root.
- Manual test plan: see [SAVE-FLOW-TEST-PLAN.md](../../SAVE-FLOW-TEST-PLAN.md).
- CI: the GitHub Actions workflow runs the static checker for relevant changes.

## Status

Static source checks are not a Gradle build or an in-game test. No Gradle build or Minecraft 1.21.11 runtime test has been completed here. Do not treat this patch as a verified JAR or as proof that the repository contains all source files.
