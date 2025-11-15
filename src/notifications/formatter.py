from typing import Dict
from src.utils.date_utils import format_expiry_label


def format_api_result(api_result: Dict) -> str:
    """
    API 검사 결과를 Slack/이메일 등에서 공통으로 사용할 문자열로 포맷팅.
    """
    name = api_result["name"]
    url = api_result["url"]
    status = api_result["status"]   # ok, warning, expired, error
    expires_on = api_result.get("expires_on")
    response_ms = api_result.get("response_ms")

    expiry_info = format_expiry_label(expires_on, warning_days=7)
    expiry_label = expiry_info["label"]

    # 상태 이모지
    emoji = {
        "ok": "🟢",
        "warning": "🟡",
        "expired": "🔴",
        "error": "❌",
        "none": "⚪"
    }.get(status, "⚪")

    result = (
        f"{emoji} *{name}*\n"
        f"- URL: {url}\n"
        f"- 상태: {status.upper()}\n"
        f"- {expiry_label}\n"
        f"- 응답시간: {response_ms}ms\n"
    )

    return result
