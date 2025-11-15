# src/notifications/builder.py

from typing import List, Dict


def build_notifications(api_results: List[Dict[str, object]]) -> List[str]:
    """
    API 검사 결과(api_results)를 받아 Slack 등으로 보낼 메시지 배열을 생성한다.
    """
    messages = []
    for result in api_results:
        name = result["name"]
        status = result["status"]
        response_time = result.get("response_time_ms")
        expiry = result.get("expiry_label", "만료 정보 없음")

        # 상태별 아이콘
        if status == "ok":
            icon = "🟢"
        elif status == "warning":
            icon = "🟡"
        elif status == "expired":
            icon = "🔴"
        else:
            icon = "⚠️"

        # 실패 API는 응답시간 대신 오류 메시지 출력
        if status == "error":
            msg = (
                f"{icon} **{name}**\n"
                f"- 상태: ERROR\n"
                f"- 오류 메시지: {result.get('error', '알 수 없음')}\n"
            )
        else:
            msg = (
                f"{icon} **{name}**\n"
                f"- 상태: {status.upper()}\n"
                f"- 응답시간: {response_time}ms\n"
                f"- 만료일: {expiry}\n"
            )

        messages.append(msg)

    return messages
