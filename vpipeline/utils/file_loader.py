
from pathlib import Path
import json, tomlkit
from typing import Any

def load_json(path) -> dict[str, Any]:
    with path.open(encoding='utf-8') as fp:
        return json.load(fp)

def save_json(path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as fp:
        json.dump(obj, fp, indent=2)

def load_toml(path):
    with path.open(encoding='utf-8') as fp:
        return tomlkit.parse(fp.read())

def save_toml(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as fp:
        fp.write(tomlkit.dumps(doc).replace('"encoding.codec"','encoding.codec'))
