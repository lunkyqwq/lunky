#!/usr/bin/env python3
"""Static regression checks for the independent training-save UI source patch."""
from pathlib import Path
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
open_method = source[source.index(open_method_start):] if open_method_start in source else ""
world_entered_guard = "if (pendingTrainingWorldStart && client.world != null)"
marker_write = "markFirstLaunchPrompted();"

checks = {
    "title-screen button is present": 'Reflex AI 训练存档' in source,
    "training save name is prefilled": 'TRAINING_WORLD_NAME = "Reflex AI Training"' in source,
    "marker is stored in the mod config directory": 'getConfigDir().resolve("reflexai").resolve("training-world-prompted")' in source,
    "marker write follows world entry guard": world_entered_guard in source and marker_write in source[:source.index(open_method_start)] if open_method_start in source else False,
    "opening the creator does not directly write marker": bool(open_method) and marker_write not in open_method,
    "cancel path clears pending state": 'pendingTrainingWorldStart = false;' in source and 'client.currentScreen instanceof TitleScreen' in source,
    "helper source path matches repository layout": "Join-Path $PSScriptRoot 'ReflexAiClient.java'" in helper,
    "helper targets the full project's client source": "src/main/java/com/example/reflexai/client/ReflexAiClient.java" in helper,
    "helper makes a timestamped backup": 'Copy-Item -LiteralPath $target -Destination $backup' in helper and 'yyyyMMdd-HHmmss' in helper,
    "helper says it does not build or install a JAR": 'does not build or install a JAR' in helper,
    "notes identify this as source-only": 'not a compiled JAR' in notes,
    "manual plan covers old-save protection": '旧存档保护' in plan,
    "manual plan covers cancellation": '取消流程' in plan,
}

failed = False
for label, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {label}")
    failed |= not ok

sys.exit(1 if failed else 0)
