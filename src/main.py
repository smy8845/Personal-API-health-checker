from src.config_loader import load_config
from src.checker import check_single_api


def print_api_result(result: dict) -> None:
    """한 개 API 결과를 보기 좋게 출력."""
    status = result["status"]
    emoji = {
        "ok": "🟢",
        "warning": "🟡",
        "expired": "🔴",
        "error": "❌",
        "none": "⚪",
    }.get(status, "⚪")

    print(f"{emoji} {result['name']}")
    print(f"- URL: {result['url']}")
    if result.get("response_ms") is not None:
        print(f"- 응답시간: {result['response_ms']}ms")
    if "expiry_label" in result:
        print(f"- {result['expiry_label']}")
    if status == "error" and "error" in result:
        print(f"- 오류: {result['error']}")
    print("-" * 40)


def main() -> None:
    cfg = load_config()
    settings = cfg["settings"]
    apis = cfg["apis"]

    print("=== API Health Check ===")
    print(f"총 {len(apis)}개 API 검사\n")

    for api_cfg in apis:
        result = check_single_api(api_cfg, warning_days=settings["expiry_warning_days"])
        print_api_result(result)


if __name__ == "__main__":
    main()
