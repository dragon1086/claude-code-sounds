#!/usr/bin/env bash
set -euo pipefail

# Find project root
find_project_root() {
  local dir="$PWD"
  while [[ "$dir" != "/" ]]; do
    [[ -d "$dir/.claude" ]] && echo "$dir" && return
    dir="$(dirname "$dir")"
  done
  echo ""
}

PROJECT_ROOT="$(find_project_root)"
if [[ -z "$PROJECT_ROOT" ]]; then
  echo "Error: no .claude/ directory found."
  exit 1
fi

TARGET="$PROJECT_ROOT/.claude/hooks"
SETTINGS="$PROJECT_ROOT/.claude/settings.json"

# Remove only the files/dirs that claude-code-sounds installs.
# We do NOT rm -rf the entire hooks/ dir — users may have other hooks there.
removed_any=0
for subpath in scripts sounds config; do
  full="$TARGET/$subpath"
  if [[ -e "$full" ]]; then
    rm -rf "$full"
    echo "Removed $full"
    removed_any=1
  fi
done

# Remove the hooks/ dir itself only if it's now empty
if [[ -d "$TARGET" ]] && [[ -z "$(ls -A "$TARGET")" ]]; then
  rmdir "$TARGET"
  echo "Removed $TARGET (empty)"
fi

if [[ "$removed_any" -eq 0 ]]; then
  echo "No claude-code-sounds files found in $TARGET"
fi

# Remove hook entries from settings.json
if [[ -f "$SETTINGS" ]]; then
  python3 - "$SETTINGS" <<'PYEOF'
import json, sys

path = sys.argv[1]
with open(path) as f:
    settings = json.load(f)

HOOK_EVENTS = [
    "SessionStart","SessionEnd","PreToolUse","PostToolUse","PostToolUseFailure",
    "UserPromptSubmit","Notification","Stop","StopFailure","SubagentStart",
    "SubagentStop","PermissionRequest","PermissionDenied","PreCompact","PostCompact",
    "InstructionsLoaded","ConfigChange","Setup","TeammateIdle","TaskCreated",
    "TaskCompleted","WorktreeCreate","WorktreeRemove","CwdChanged","FileChanged",
    "Elicitation","ElicitationResult"
]

hooks = settings.get("hooks", {})
removed = 0
for event in HOOK_EVENTS:
    if event in hooks:
        entries = hooks[event]
        hooks[event] = [
            e for e in entries
            if "hooks/scripts/hooks.py" not in e.get("command", "")
        ]
        if not hooks[event]:
            del hooks[event]
            removed += 1

settings["hooks"] = hooks
if not settings["hooks"]:
    del settings["hooks"]

with open(path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print(f"Removed {removed} hook entries from {path}")
PYEOF
fi

echo ""
echo "✓ claude-code-sounds uninstalled."
echo "Restart Claude Code to deactivate."
