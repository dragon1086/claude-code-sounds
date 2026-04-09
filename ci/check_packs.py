#!/usr/bin/env python3
"""
CI check: each folder under packs/ must have a valid pack.json
with required fields: name, description, license.
"""
import json
import sys
from pathlib import Path

packs_dir = Path(__file__).parent.parent / "packs"
errors = []

for pack_dir in sorted(packs_dir.iterdir()):
    if not pack_dir.is_dir():
        continue
    pack_json = pack_dir / "pack.json"
    if not pack_json.exists():
        errors.append(f"{pack_dir.name}: missing pack.json")
        continue
    try:
        data = json.loads(pack_json.read_text())
        for field in ("name", "description", "license"):
            if field not in data:
                errors.append(f"{pack_dir.name}/pack.json: missing field '{field}'")
    except json.JSONDecodeError as e:
        errors.append(f"{pack_dir.name}/pack.json: invalid JSON — {e}")

if errors:
    print("FAIL: pack validation errors:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print("OK: all packs have valid pack.json")
