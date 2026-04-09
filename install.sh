#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# claude-code-sounds installer
# Copies hooks/ into your project's .claude/hooks/
# and patches .claude/settings.json
# ─────────────────────────────────────────────

FORCE=0
for arg in "$@"; do
  [[ "$arg" == "--force" ]] && FORCE=1
done

# Find project root (walk up looking for .claude/)
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
  echo "Error: no .claude/ directory found. Run this from inside a Claude Code project."
  exit 1
fi

TARGET="$PROJECT_ROOT/.claude/hooks"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$SCRIPT_DIR/hooks"

# Copy hooks/
if [[ -d "$TARGET" && "$FORCE" -eq 0 ]]; then
  echo "Warning: $TARGET already exists. Use --force to overwrite."
  exit 1
fi

echo "Installing claude-code-sounds into $TARGET ..."
cp -r "$SOURCE" "$TARGET"

# Patch settings.json
SETTINGS="$PROJECT_ROOT/.claude/settings.json"
if [[ ! -f "$SETTINGS" ]]; then
  echo "{}" > "$SETTINGS"
fi

# Use Python to patch settings.json (avoids jq dependency)
python3 - "$SETTINGS" <<'PYEOF'
import json, sys

path = sys.argv[1]
with open(path) as f:
    settings = json.load(f)

HOOK_CMD = "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py"

def make_hook(cmd, once=False):
    h = {"type": "command", "command": cmd, "async": True, "timeout": 5000}
    if once:
        h["once"] = True
    return [{"matcher": "", "hooks": [h]}]

HOOKS = {
    "SessionStart":       make_hook(HOOK_CMD, once=True),
    "SessionEnd":         make_hook(HOOK_CMD, once=True),
    "PreToolUse":         make_hook(HOOK_CMD),
    "PostToolUse":        make_hook(HOOK_CMD),
    "PostToolUseFailure": make_hook(HOOK_CMD),
    "UserPromptSubmit":   make_hook(HOOK_CMD),
    "Notification":       make_hook(HOOK_CMD),
    "Stop":               make_hook(HOOK_CMD),
    "StopFailure":        make_hook(HOOK_CMD),
    "SubagentStart":      make_hook(HOOK_CMD),
    "SubagentStop":       make_hook(HOOK_CMD),
    "PermissionRequest":  make_hook(HOOK_CMD),
    "PermissionDenied":   make_hook(HOOK_CMD),
    "PreCompact":         make_hook(HOOK_CMD, once=True),
    "PostCompact":        make_hook(HOOK_CMD),
    "InstructionsLoaded": make_hook(HOOK_CMD),
    "ConfigChange":       make_hook(HOOK_CMD),
    "Setup":              make_hook(HOOK_CMD),
    "TeammateIdle":       make_hook(HOOK_CMD),
    "TaskCreated":        make_hook(HOOK_CMD),
    "TaskCompleted":      make_hook(HOOK_CMD),
    "WorktreeCreate":     make_hook(HOOK_CMD),
    "WorktreeRemove":     make_hook(HOOK_CMD),
    "CwdChanged":         make_hook(HOOK_CMD),
    "FileChanged":        make_hook(HOOK_CMD),
    "Elicitation":        make_hook(HOOK_CMD),
    "ElicitationResult":  make_hook(HOOK_CMD),
}

existing = settings.get("hooks", {})
existing.update(HOOKS)
settings["hooks"] = existing

with open(path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print(f"Patched {path} with {len(HOOKS)} hook events.")
PYEOF

echo ""
echo "✓ claude-code-sounds installed successfully."
echo ""
echo "Sounds are in: $TARGET/sounds/"
echo "To customize: replace any .wav or .mp3 file in a sounds/ subfolder."
echo "To disable a hook: edit $TARGET/config/hooks-config.local.json"
echo ""
echo "Restart Claude Code to activate."
