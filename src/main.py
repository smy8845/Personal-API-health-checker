from .config_loader import load_config


def format_api_summary(api: dict) -> str:
    """API 한 개에 대한 요약 문자열 (만료일 정보 제외)"""
    return f"- {api['name']} ({api['method']} {api['url']}, timeout={api['timeout']}초)"


def main() -> None:
    cfg = load_config()
    apis = cfg["apis"]

    print("=== API 설정 로드 결과 ===")
    print(f"총 {len(apis)}개 API")

    for api in apis:
        print(format_api_summary(api))


if __name__ == "__main__":
    # 모듈로 실행할 때는 거의 안 쓰겠지만, 로컬 테스트용으로 남겨둠
    main()