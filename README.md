# Reflex AI — save-flow patch repository

This repository currently tracks the **3.4.1 independent training-save UI patch**, not the complete Reflex AI Fabric mod source tree.

## Current patch
- Source file: [ReflexAiClient.java](patches/save-flow-3.4.1/ReflexAiClient.java)
- Notes and application steps: [PATCH-NOTES.md](patches/save-flow-3.4.1/PATCH-NOTES.md)

The patch opens Minecraft's normal Create World screen, prefills the name `Reflex AI Training`, enables cheats for that newly created world, and keeps a title-screen button for reopening the flow. It does not silently create a world or overwrite an existing save.

## Important status
- This repository does **not** currently contain the full project source tree or a verified build workflow.
- The patch is source code, **not** a compiled `.jar`.
- Static checks were performed, but Gradle compilation and Minecraft 1.21.11 in-game testing have not been completed.

To use it, apply the patched Java file to the matching full source project. Do not copy this repository's patch file directly into the Minecraft `mods` folder.
