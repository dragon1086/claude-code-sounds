#!/usr/bin/env bash
# claude-sounds — sound pack manager for claude-code-sounds
#
# Usage:
#   claude-sounds list                              # List installed packs
#   claude-sounds use <pack-name>                   # Switch to a built-in pack
#   claude-sounds use https://github.com/...        # Switch to an external pack
#   claude-sounds preview <pack-name>               # Show what sounds a pack contains
#   claude-sounds current                           # Show active pack
#
# The active pack is tracked in hooks/config/hooks-config.json ("activePack" key).
# Switching a pack copies the pack's sounds/ tree into hooks/sounds/.
# Missing slots in partial packs fall back to the default pack.

set -euo pipefail

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKS_DIR="$SCRIPT_DIR/packs"
SOUNDS_DIR="$SCRIPT_DIR/hooks/sounds"
CONFIG_FILE="$SCRIPT_DIR/hooks/config/hooks-config.json"

# ── Helpers ───────────────────────────────────────────────────────────────────
die()  { echo "error: $*" >&2; exit 1; }
info() { echo "$*"; }

require_sounds_dir() {
    [[ -d "$SOUNDS_DIR" ]] || die "hooks/sounds/ not found — are you in the repo root?"
}

get_active_pack() {
    if [[ -f "$CONFIG_FILE" ]] && command -v python3 &>/dev/null; then
        python3 -c "
import json, sys
try:
    d = json.load(open('$CONFIG_FILE'))
    print(d.get('activePack', 'default'))
except Exception:
    print('default')
"
    else
        echo "default"
    fi
}

set_active_pack() {
    local pack_name="$1"
    if command -v python3 &>/dev/null && [[ -f "$CONFIG_FILE" ]]; then
        python3 -c "
import json
path = '$CONFIG_FILE'
d = json.load(open(path))
d['activePack'] = '$pack_name'
with open(path, 'w') as f:
    json.dump(d, f, indent=2)
    f.write('\n')
"
    fi
}

# Copy a pack's sounds/ tree into hooks/sounds/.
# Always starts from the default pack, then overlays the target pack on top.
# This guarantees partial packs fall back to default for missing slots —
# regardless of what the previous active pack was.
apply_pack_sounds() {
    local pack_sounds_dir="$1"
    require_sounds_dir

    _rsync_dir() {
        local src="$1" dst="$2"
        if command -v rsync &>/dev/null; then
            rsync -a --no-whole-file "$src/" "$dst/"
        else
            cp -r "$src/." "$dst/"
        fi
    }

    # ── Step 1: restore default as the base ───────────────────────────────
    local default_sounds
    default_sounds="$(python3 -c "import os; print(os.path.realpath('$PACKS_DIR/default/sounds'))" 2>/dev/null \
        || readlink "$PACKS_DIR/default/sounds" || echo "$PACKS_DIR/default/sounds")"

    if [[ -d "$default_sounds" ]]; then
        _rsync_dir "$default_sounds" "$SOUNDS_DIR"
    fi

    # ── Step 2: overlay the target pack (partial packs OK) ────────────────
    local resolved
    resolved="$(python3 -c "import os; print(os.path.realpath('$pack_sounds_dir'))" 2>/dev/null || echo "$pack_sounds_dir")"

    if [[ ! -d "$resolved" ]]; then
        die "Pack sounds directory not found: $resolved"
    fi

    # Skip overlay if the target IS the default (already done above)
    if [[ "$resolved" != "$default_sounds" ]]; then
        _rsync_dir "$resolved" "$SOUNDS_DIR"
    fi
}

# ── Commands ──────────────────────────────────────────────────────────────────

cmd_list() {
    info "Installed packs:"
    local active
    active="$(get_active_pack)"
    for pack_dir in "$PACKS_DIR"/*/; do
        local name
        name="$(basename "$pack_dir")"
        local marker=""
        [[ "$name" == "$active" ]] && marker=" (active)"
        local desc=""
        if [[ -f "$pack_dir/pack.json" ]] && command -v python3 &>/dev/null; then
            desc="$(python3 -c "
import json
try:
    d = json.load(open('$pack_dir/pack.json'))
    print(' — ' + d.get('description', ''))
except Exception:
    pass
" 2>/dev/null)"
        fi
        info "  $name$marker$desc"
    done
    info ""
    info "Use 'claude-sounds use <name>' to switch packs."
    info "Use 'claude-sounds use https://github.com/...' for external packs."
}

cmd_current() {
    info "Active pack: $(get_active_pack)"
}

cmd_preview() {
    local pack_name="${1:-}"
    [[ -n "$pack_name" ]] || die "Usage: claude-sounds preview <pack-name>"

    local pack_dir="$PACKS_DIR/$pack_name"
    [[ -d "$pack_dir" ]] || die "Pack '$pack_name' not found in $PACKS_DIR"

    local sounds_dir="$pack_dir/sounds"
    if [[ -L "$sounds_dir" ]]; then
        sounds_dir="$(python3 -c "import os; print(os.path.realpath('$sounds_dir'))" 2>/dev/null || readlink "$sounds_dir")"
    fi

    info "Pack: $pack_name"
    if [[ -f "$pack_dir/pack.json" ]] && command -v python3 &>/dev/null; then
        python3 -c "
import json
d = json.load(open('$pack_dir/pack.json'))
for k in ['author','description','license']:
    if k in d: print(f'  {k}: {d[k]}')
" 2>/dev/null
    fi
    info ""
    info "Sound slots:"
    if [[ -d "$sounds_dir" ]]; then
        find "$sounds_dir" -name "*.wav" -o -name "*.mp3" | sort | while read -r f; do
            info "  $(basename "$(dirname "$f")")/$(basename "$f")"
        done
    else
        info "  (no sounds directory found)"
    fi
}

cmd_use() {
    local target="${1:-}"
    [[ -n "$target" ]] || die "Usage: claude-sounds use <pack-name|url>"

    require_sounds_dir

    # ── External pack: GitHub URL ──────────────────────────────────────────
    if [[ "$target" == http* ]]; then
        command -v git &>/dev/null || die "git is required to install external packs"

        local repo_name
        repo_name="$(basename "$target" .git)"
        local dest="$PACKS_DIR/$repo_name"

        if [[ -d "$dest" ]]; then
            info "Updating existing pack '$repo_name'..."
            git -C "$dest" pull --ff-only
        else
            info "Cloning external pack from $target..."
            git clone --depth=1 "$target" "$dest"
        fi

        [[ -d "$dest/sounds" ]] || die "Cloned repo has no sounds/ directory — not a valid pack"

        info "Applying pack '$repo_name'..."
        apply_pack_sounds "$dest/sounds"
        set_active_pack "$repo_name"
        info "Done. Active pack: $repo_name"
        return
    fi

    # ── Silent pack: generate on-the-fly if needed ────────────────────────
    if [[ "$target" == "silent" ]]; then
        local silent_dir="$PACKS_DIR/silent"
        if [[ ! -d "$silent_dir/sounds" ]]; then
            info "Building silent pack (100ms silence for all slots)..."
            _build_silent_pack "$silent_dir"
        fi
        info "Applying silent pack..."
        apply_pack_sounds "$silent_dir/sounds"
        set_active_pack "silent"
        info "Done. Sounds are now silent. Use 'claude-sounds use default' to restore."
        return
    fi

    # ── Built-in pack ─────────────────────────────────────────────────────
    local pack_dir="$PACKS_DIR/$target"
    [[ -d "$pack_dir" ]] || die "Pack '$target' not found. Run 'claude-sounds list' to see available packs."

    local pack_sounds="$pack_dir/sounds"
    [[ -d "$pack_sounds" || -L "$pack_sounds" ]] || die "Pack '$target' has no sounds/ directory"

    info "Applying pack '$target'..."
    apply_pack_sounds "$pack_sounds"
    set_active_pack "$target"
    info "Done. Active pack: $target"
}

# Build a silent pack by copying the sounds structure and replacing files with silence
_build_silent_pack() {
    local dest="$1"
    mkdir -p "$dest/sounds"

    # Create a 100ms silent WAV (PCM 16-bit 44100Hz mono)
    local tmp_silent
    tmp_silent="$(mktemp /tmp/silence_XXXXXX.wav)"

    if command -v ffmpeg &>/dev/null; then
        ffmpeg -y -f lavfi -i "anullsrc=r=44100:cl=mono" -t 0.1 -q:a 9 "$tmp_silent" &>/dev/null
    elif command -v python3 &>/dev/null; then
        python3 -c "
import struct, wave
path = '$tmp_silent'
with wave.open(path, 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    f.writeframes(struct.pack('<4410h', *([0]*4410)))
"
    else
        die "ffmpeg or python3 required to generate silent WAV files"
    fi

    # Mirror the sounds/ directory structure with silent files
    for folder in "$SOUNDS_DIR"/*/; do
        local folder_name
        folder_name="$(basename "$folder")"
        mkdir -p "$dest/sounds/$folder_name"
        for audio_file in "$folder"*.wav "$folder"*.mp3; do
            [[ -f "$audio_file" ]] || continue
            cp "$tmp_silent" "$dest/sounds/$folder_name/$(basename "$audio_file")"
        done
    done

    # Add pack.json
    cat > "$dest/pack.json" << 'EOF'
{
  "name": "silent",
  "author": "claude-code-sounds",
  "description": "100ms silence for all slots — disables sounds without removing hooks",
  "license": "MIT"
}
EOF

    rm -f "$tmp_silent"
}

# Configure a project to use claude-code-sounds hooks via settings.json.
# Works even when the plugin is installed as project-scope (not user-scope),
# by copying hooks/ into the project's .claude/hooks/ and patching settings.json.
cmd_setup_project() {
    # Locate project root: prefer CLAUDE_PROJECT_DIR, then walk up for .claude/
    local project_dir="${CLAUDE_PROJECT_DIR:-}"
    if [[ -z "$project_dir" ]]; then
        local dir="$PWD"
        while [[ "$dir" != "/" ]]; do
            [[ -d "$dir/.claude" ]] && { project_dir="$dir"; break; }
            dir="$(dirname "$dir")"
        done
    fi
    [[ -n "$project_dir" ]] || die "No Claude Code project found. Run from inside a project with a .claude/ directory, or set CLAUDE_PROJECT_DIR."

    local target="$project_dir/.claude/hooks"

    # Copy hooks/ from plugin source to project
    if [[ -d "$target" ]]; then
        info "Updating existing hooks at $target ..."
        cp -r "$SCRIPT_DIR/hooks/." "$target/"
    else
        info "Installing hooks to $target ..."
        cp -r "$SCRIPT_DIR/hooks" "$target"
    fi

    # Patch settings.json
    local settings="$project_dir/.claude/settings.json"
    [[ -f "$settings" ]] || echo "{}" > "$settings"

    python3 - "$settings" <<'PYEOF'
import json, sys

path = sys.argv[1]
with open(path) as f:
    settings = json.load(f)

CMD = "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py"

HOOKS = {
    "SessionStart":       [{"type":"command","command":CMD,"async":True,"timeout":5000,"once":True}],
    "SessionEnd":         [{"type":"command","command":CMD,"async":True,"timeout":5000,"once":True}],
    "PreToolUse":         [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "PostToolUse":        [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "PostToolUseFailure": [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "UserPromptSubmit":   [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "Notification":       [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "Stop":               [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "StopFailure":        [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "SubagentStart":      [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "SubagentStop":       [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "PermissionRequest":  [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "PermissionDenied":   [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "PreCompact":         [{"type":"command","command":CMD,"async":True,"timeout":5000,"once":True}],
    "PostCompact":        [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "InstructionsLoaded": [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "ConfigChange":       [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "Setup":              [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "TeammateIdle":       [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "TaskCreated":        [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "TaskCompleted":      [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "WorktreeCreate":     [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "WorktreeRemove":     [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "CwdChanged":         [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "FileChanged":        [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "Elicitation":        [{"type":"command","command":CMD,"async":True,"timeout":5000}],
    "ElicitationResult":  [{"type":"command","command":CMD,"async":True,"timeout":5000}],
}

existing = settings.get("hooks", {})
existing.update(HOOKS)
settings["hooks"] = existing

with open(path, "w") as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Patched {path} with {len(HOOKS)} hook events.")
PYEOF

    info ""
    info "Done. Hooks installed at: $target"
    info "Restart Claude Code session to activate."
}

# ── Entrypoint ────────────────────────────────────────────────────────────────
usage() {
    cat << 'EOF'
claude-sounds — sound pack manager for claude-code-sounds

Usage:
  claude-sounds list                      List installed packs
  claude-sounds current                   Show active pack
  claude-sounds use <pack>                Switch to a built-in pack (e.g. silent, default)
  claude-sounds use <url>                 Switch to an external pack (GitHub URL)
  claude-sounds preview <pack>            Show sounds in a pack
  claude-sounds setup-project             Register hooks in this project's .claude/settings.json
                                          (use when installed as project-scope via /plugin install)

Examples:
  claude-sounds use silent
  claude-sounds use default
  claude-sounds use https://github.com/someone/star-trek-sounds
  claude-sounds list
  claude-sounds setup-project
EOF
}

case "${1:-}" in
    list)           cmd_list ;;
    current)        cmd_current ;;
    use)            cmd_use "${2:-}" ;;
    preview)        cmd_preview "${2:-}" ;;
    setup-project)  cmd_setup_project ;;
    help|--help|-h|"") usage ;;
    *) die "Unknown command: $1. Run 'claude-sounds help' for usage." ;;
esac
