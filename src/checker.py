import time
import requests
from typing import Dict, Any, Optional

from src.utils.date_utils import format_expiry_label


def apply_auth(headers: Dict[str, str], auth_cfg: Dict[str, Any]) -> Dict[str, str]:
    """config의 auth 설정에 따라 headers를 완성."""
    auth_type = auth_cfg.get("type")

    if auth_type == "none":
        return headers

    elif auth_type == "bearer":
        token_key = auth_cfg.get("token_env_key")
        from os import getenv
        token = getenv(token_key)
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    elif auth_type == "apikey_header":
        header_name = auth_cfg.get("header_name")
        token_key = auth_cfg.get("token_env_key")
        from os import getenv
        token = getenv(token_key)
        if header_name and token:
            headers[header_name] = token
        return headers

    else:
        # 알 수 없는 auth 타입
        return headers


def check_single_api(api_cfg: Dict[str, Any], warning_days: int = 7) -> Dict[str, Any]:
    """단일 API를 검사하고 결과를 딕셔너리 형태로 반환."""
    url = api_cfg["url"]
    method = api_cfg["method"].upper()
    timeout = api_cfg.get("timeout", 5)
    headers = api_cfg.get("headers", {}).copy()
    body = api_cfg.get("body", None)

    # 인증 적용
    headers = apply_auth(headers, api_cfg.get("auth", {}))

    # 요청 시간 측정
    start = time.time()
    status = "error"
    response_ms: Optional[int] = None

    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=timeout)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=body, timeout=timeout)
        else:
            return {
                "name": api_cfg["name"],
                "url": url,
                "status": "error",
                "error": f"Unsupported method: {method}",
                "response_ms": None,
                "expires_on": api_cfg.get("expires_on"),
            }

        response_ms = int((time.time() - start) * 1000)

        # HTTP 응답 상태 코드 기반 초기 상태
        if 200 <= resp.status_code < 300:
            status = "ok"
        elif 300 <= resp.status_code < 500:
            status = "warning"
        else:
            status = "error"

    except Exception as e:
        return {
            "name": api_cfg["name"],
            "url": url,
            "status": "error",
            "error": str(e),
            "response_ms": None,
            "expires_on": api_cfg.get("expires_on"),
        }

    # 만료일 계산
    expiry_info = format_expiry_label(api_cfg.get("expires_on"), warning_days=warning_days)

    # 만료 상태가 더 심각하면 만료 상태로 override
    if expiry_info["status"] in ["warning", "expired"]:
        status = expiry_info["status"]

    return {
        "name": api_cfg["name"],
        "url": url,
        "status": status,               # ok/warning/expired/error
        "response_ms": response_ms,
        "expires_on": api_cfg.get("expires_on"),
        "expiry_label": expiry_info["label"],
        "days_left": expiry_info["days_left"],
    }
