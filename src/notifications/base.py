from typing import Protocol, Dict, Any


class Notifier(Protocol):
    """모든 알림 클래스가 따라야 하는 인터페이스(약속)."""

    def send(self, message: str, data: Dict[str, Any]) -> None:
        """
        알림 전송 공통 인터페이스
        - message: 최종 사용자에게 보여줄 메시지(문자열)
        - data: 알림에 필요한 추가 데이터(딕셔너리)
        """
        ...
