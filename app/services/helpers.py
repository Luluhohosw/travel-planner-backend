"""通用工具函数"""
import json


def parse_preferences(pref_str: str) -> list:
    if not pref_str:
        return []
    try:
        result = json.loads(pref_str)
        if isinstance(result, list):
            return result
    except (json.JSONDecodeError, TypeError):
        pass
    return [p.strip() for p in pref_str.replace("，", ",").split(",") if p.strip()]


def parse_destination(dest_str: str) -> list:
    if not dest_str:
        return []
    try:
        result = json.loads(dest_str)
        if isinstance(result, list):
            return result
    except (json.JSONDecodeError, TypeError):
        pass
    for sep in ["→", "->", "-", "—"]:
        if sep in dest_str:
            return [d.strip() for d in dest_str.split(sep) if d.strip()]
    return [dest_str.strip()]


def safe_json_loads(text: str, default=None):
    if not text:
        return default
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default
