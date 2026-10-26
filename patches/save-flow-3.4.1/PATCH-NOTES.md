# Reflex AI save-flow patch 3.4.1

This folder contains a **source patch only**, not a complete Minecraft mod project and not a compiled JAR.

## What changed
- The first-launch marker is not written merely because the Create World screen opened.
- The marker is written only after the client enters a world created through this flow.
- Returning to the title screen without entering a world clears the pending state; the marker remains absent.
- The title-screen button remains available to reopen the Create World screen.
- The proposed save name is `Reflex AI Training`; cheats are enabled for that new save only after the user confirms world creation.

## Apply
Replace `src/main/java/com/example/reflexai/client/ReflexAiClient.java` in the matching full source tree with this file.

## Verification status
ZIP/source integrity and static checks passed in the working environment. No Gradle build or in-game test has been completed. Do not treat this patch as a verified JAR or as proof that the repository contains all source files.
