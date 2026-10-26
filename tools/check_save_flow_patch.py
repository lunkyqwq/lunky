#!/usr/bin/env python3
"""Static regression checks for the independent training-save UI source patch."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "patches/save-flow-3.4.1/ReflexAiClient.java"
HELPER_PATH = ROOT / "patches/save-flow-3.4.1/apply-save-flow-patch.ps1"
NOTES_PATH = ROOT / "patches/save-flow-3.4.1/PATCH-NOTES.md"
PLAN_PATH = ROOT / "SAVE-FLOW-TEST-PLAN.md"

required = [SOURCE_PATH, HELPER_PATH, NOTES_PATH, PLAN_PATH]
missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
if missing:
    print("FAIL: required file(s) missing: " + ", ".join(missing))
    sys.exit(1)

source = SOURCE_PATH.read_text(encoding="utf-8")
helper = HELPER_PATH.read_text(encoding="utf-8")
notes = NOTES_PATH.read_text(encoding="utf-8")
plan = PLAN_PATH.read_text(encoding="utf-8")

open_method_start = "private static void openTrainingWorldCreator"
open_method_index = source.find(open_method_start)
open_method = source[open_method_index:] if open_method_index >= 0 else ""
world_entered_guard = "if (pendingTrainingWorldStart && client.world != null)"
marker_write = "markFirstLaunchPrompted();"
guard_index = source.find(world_entered_guard)
marker_index = source.find(marker_write)

# Remove comments and string/character literals before checking balanced Java delimiters.
without_comments = re.sub(r"/\*.*?\*/|//[^\n]*", " ", source, flags=re.S)
without_literals = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', "LIT", without_comments)
stack = []
closing = {
")": "(", "]": "[", "}": "{"}
delimiters_balanced = True
for char in without_literals:
    if char in "([{":
        stack.append(char)
    elif char in ")]}":
        if not stack or stack.pop() != closing[char]:
            delimiters_balanced = False
            break
delimiters_balanced = delimiters_balanced and not stack

checks = {
    "title-screen button is present": 'Reflex AI 训练存档' in source,
    "training save name is prefilled": 'TRAINING_WORLD_NAME = "Reflex AI Training"' in source,
    "marker is stored in the mod config directory": 'getConfigDir().resolve("reflexai").resolve("training-world-prompted")' in source,
    "world-entry guard exists": guard_index >= 0,
    "marker write occurs after the world-entry guard": guard_index >= 0 and marker_index > guard_index and marker_index < open_method_index,
    "opening the creator does not directly write marker": bool(open_method) and marker_write not in open_method,
    "cancel path clears pending state": 'pendingTrainingWorldStart = false;' in source and 'client.currentScreen instanceof TitleScreen' in source,
    "create-world flow sets prefill and pending flags": 'prefillNextCreateWorld = true;' in open_method and 'pendingTrainingWorldStart = true;' in open_method,
    "Java braces, brackets and parentheses balance": delimiters_balanced,
    "helper source path matches bundle layout": "Join-Path $PSScriptRoot 'ReflexAiClient.java'" in helper,
    "helper targets the full project's client source": "src/main/java/com/example/reflexai/client/ReflexAiClient.java" in helper,
    "helper refuses source-target self-overwrite": 'Patch source and target resolve to the same file' in helper,
    "helper skips already-applied identical source": '$sourceHash -eq $targetHash' in helper,
    "helper verifies staged file checksum": '$stagedHash -ne $sourceHash' in helper,
    "helper makes a timestamped backup": 'Copy-Item -LiteralPath $target -Destination $backup' in helper and 'yyyyMMdd-HHmmss-fff' in helper,
    "helper says it does not build or install a JAR": 'does not build or install a JAR' in helper,
    "notes identify this as source-only": 'not a compiled JAR' in notes,
    "manual plan covers old-save protection": 'Existing-save protection' in plan,
    "manual plan covers cancellation": 'Cancel:' in plan,
}

failed = False
for label, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {label}")
    failed |= not ok

sys.exit(1 if failed else 0)
