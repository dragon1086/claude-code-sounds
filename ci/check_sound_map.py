#!/usr/bin/env python3
"""
CI check: HOOK_SOUND_MAP + AGENT_HOOK_SOUND_MAP values in hooks.py
must each have a corresponding folder under hooks/sounds/.
"""
import ast
import sys
from pathlib import Path

repo = Path(__file__).parent.parent
hooks_py = repo / "hooks" / "scripts" / "hooks.py"
sounds_dir = repo / "hooks" / "sounds"

source = hooks_py.read_text()
tree = ast.parse(source)

map_values = set()
for map_name in ("HOOK_SOUND_MAP", "AGENT_HOOK_SOUND_MAP"):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == map_name:
                    if isinstance(node.value, ast.Dict):
                        for v in node.value.values:
                            if isinstance(v, ast.Constant):
                                map_values.add(v.value)

print(f"Map values ({len(map_values)}):")
for v in sorted(map_values):
    print(f"  {v}")

folder_names = {p.name for p in sounds_dir.iterdir() if p.is_dir()}

print(f"\nsounds/ folders ({len(folder_names)}):")
for f in sorted(folder_names):
    print(f"  {f}")

missing = map_values - folder_names
extra   = folder_names - map_values

if extra:
    print(f"\nWARN: folders in sounds/ not referenced by any map:")
    for e in sorted(extra):
        print(f"  {e}")

if missing:
    print(f"\nFAIL: map values with no matching sounds/ folder:")
    for m in sorted(missing):
        print(f"  {m}")
    sys.exit(1)

print("\nOK: all map values have a corresponding sounds/ folder")
