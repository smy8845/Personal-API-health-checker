# src/notifications/slack_sender.py

import json
import urllib.request


def send_slack_message(webhook_url: str, messages: list):
    """
    Slack incoming webhook으로 메시지 리스트를 전송한다.
    """
    if not webhook_url:
        print("⚠️ Slack Webhook URL이 설정되지 않아 알림을 건너뜀")
        return

    text = "\n\n".join(messages)

    payload = {
        "text": text
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            print(f"Slack 응답 상태: {response.status}")
    except Exception as e:
        print(f"Slack 전송 실패: {e}")
