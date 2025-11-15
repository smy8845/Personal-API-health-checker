# src/main.py

from src.config_loader import load_config
from src.checker import check_single_api
from src.notifications.builder import build_notifications
from src.notifications.slack_sender import send_slack_message


def main():
    config = load_config()

    apis = config["apis"]
    settings = config.get("settings", {})
    notif_settings = config.get("notification", {})

    slack_url = notif_settings.get("slack_webhook", "")

    results = []

    print("=== API Health Check ===")

    for api in apis:
        print(f"\n▶ {api['name']}")
        result = check_single_api(api, settings)
        results.append(result)

    # Slack 메시지 생성
    messages = build_notifications(results)

    # Slack 전송
    send_slack_message(slack_url, messages)


if __name__ == "__main__":
    main()
