import datetime as dt
from typing import Optional, Literal, Dict


ExpiryStatus = Literal["none", "ok", "warning", "expired"]


def _parse_date(date_str: Optional[str]) -> Optional[dt.date]:
    """YYYY-MM-DD 문자열을 date 객체로 변환. 없거나 빈 값이면 None."""
    if not date_str:
        return None
    return dt.date.fromisoformat(date_str)


def compute_days_left(expires_on: Optional[str]) -> Optional[int]:
    """
    만료일까지 남은 일수 계산.
    - expires_on 이 없으면 None
    - 오늘 기준 (만료일 - 오늘).days
    """
    expiry_date = _parse_date(expires_on)
    if expiry_date is None:
        return None

    today = dt.date.today()
    return (expiry_date - today).days


def determine_expiry_status(
    days_left: Optional[int],
    warning_days: int = 7,
) -> ExpiryStatus:
    """
    남은 일수에 따라 상태 분류:
    - None       -> "none"       (만료일 없음)
    - < 0        -> "expired"    (이미 만료)
    - 0 ~ N일    -> "warning"    (만료 임박)
    - 그 외      -> "ok"
    """
    if days_left is None:
        return "none"
    if days_left < 0:
        return "expired"
    if days_left <= warning_days:
        return "warning"
    return "ok"


def format_expiry_label(
    expires_on: Optional[str],
    warning_days: int = 7,
) -> Dict[str, object]:
    """
    화면/로그에 쓸 만료일 문자열과 상태를 함께 반환.

    반환 예시:
    - {"label": "만료일 : 2026-11-11 · 73일 남음", "status": "ok", "days_left": 73}
    - {"label": "만료일 : 2026-11-11 · 3일 남음 (만료 임박)", "status": "warning", ...}
    - {"label": "만료일 : 2026-11-11 · 2일 지남 (만료됨)", "status": "expired", ...}
    - {"label": "만료일 : (설정 없음)", "status": "none", "days_left": None}
    """
    days_left = compute_days_left(expires_on)
    status = determine_expiry_status(days_left, warning_days)

    if expires_on is None:
        return {
            "label": "만료일 : (설정 없음)",
            "status": status,
            "days_left": None,
        }

    # days_left 는 여기서 None 이 아님 (expires_on 이 있으니까)
    assert days_left is not None

    base_date = expires_on  # "YYYY-MM-DD" 형식 그대로 사용

    if status == "expired":
        label = f"만료일 : {base_date} · {abs(days_left)}일 지남 (만료됨)"
    elif status == "warning":
        label = f"만료일 : {base_date} · {days_left}일 남음 (만료 임박)"
    elif status == "ok":
        label = f"만료일 : {base_date} · {days_left}일 남음"
    else:  # "none" 이지만 여기로 올 일은 거의 없음 (예비용)
        label = "만료일 : (설정 없음)"

    return {
        "label": label,
        "status": status,
        "days_left": days_left,
    }