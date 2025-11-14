import json
from pathlib import Path
from typing import Any, Dict

CONFIG_PATH = Path("config.json")
EXAMPLE_CONFIG_PATH = Path("config.example.json")


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    """config.json을 읽되, 없으면 config.example.json을 사용"""
    if not path.exists():
        # GitHub Actions 같은 환경에서는 config.json이 없으므로
        # 예시 설정 파일을 대신 사용
        path = EXAMPLE_CONFIG_PATH

    with path.open(encoding="utf-8") as f:
        raw = json.load(f)

    settings = raw.get("settings", {})
    default_timeout = settings.get("default_timeout", 5)
    expiry_warning_days = settings.get("expiry_warning_days", 7)

    apis = []
    for api in raw.get("apis", []):
        api = api.copy()

        # timeout 기본값 채우기
        api["timeout"] = api.get("timeout", default_timeout)

        # expires_on: 없거나 null이면 그대로 둠 (나중에 "설정 없음"으로 표시)
        api["expires_on"] = api.get("expires_on", None)

        # headers/body 기본값
        api["headers"] = api.get("headers") or {}
        api["body"] = api.get("body", None)

        apis.append(api)

    return {
        "settings": {
            "default_timeout": default_timeout,
            "expiry_warning_days": expiry_warning_days,
        },
        "apis": apis,
    }