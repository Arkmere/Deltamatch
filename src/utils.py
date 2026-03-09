from __future__ import annotations

import hashlib
import json
from typing import Any


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def config_fingerprint(config: dict[str, Any]) -> str:
    return sha256_text(json.dumps(config, sort_keys=True, default=str))


def make_exact_group_id(row_hash: str) -> str:
    return f"EXACT_{sha256_text(row_hash)[:8]}"
