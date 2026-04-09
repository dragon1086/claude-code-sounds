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

HOOKS = {
    "SessionStart":       [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"once":True,"statusMessage":"SessionStart"}],
    "SessionEnd":         [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"once":True,"statusMessage":"SessionEnd"}],
    "PreToolUse":         [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"PreToolUse"}],
    "PostToolUse":        [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"PostToolUse"}],
    "PostToolUseFailure": [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"PostToolUseFailure"}],
    "UserPromptSubmit":   [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"UserPromptSubmit"}],
    "Notification":       [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"Notification"}],
    "Stop":               [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"Stop"}],
    "StopFailure":        [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"StopFailure"}],
    "SubagentStart":      [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"SubagentStart"}],
    "SubagentStop":       [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"SubagentStop"}],
    "PermissionRequest":  [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"PermissionRequest"}],
    "PermissionDenied":   [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"PermissionDenied"}],
    "PreCompact":         [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"once":True,"statusMessage":"PreCompact"}],
    "PostCompact":        [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"PostCompact"}],
    "InstructionsLoaded": [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"InstructionsLoaded"}],
    "ConfigChange":       [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"ConfigChange"}],
    "Setup":              [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"Setup"}],
    "TeammateIdle":       [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"TeammateIdle"}],
    "TaskCreated":        [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"TaskCreated"}],
    "TaskCompleted":      [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"TaskCompleted"}],
    "WorktreeCreate":     [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"WorktreeCreate"}],
    "WorktreeRemove":     [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"WorktreeRemove"}],
    "CwdChanged":         [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"CwdChanged"}],
    "FileChanged":        [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"FileChanged"}],
    "Elicitation":        [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"Elicitation"}],
    "ElicitationResult":  [{"type":"command","command":HOOK_CMD,"async":True,"timeout":5000,"statusMessage":"ElicitationResult"}],
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
