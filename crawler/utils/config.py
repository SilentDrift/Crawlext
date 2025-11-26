from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=None)
def load_yaml(name: str) -> dict[str, Any]:
    path = PROJECT_ROOT / "configs" / name
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}
