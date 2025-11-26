from datetime import datetime, timezone
from typing import Optional

from dateutil import parser


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        dt = parser.parse(date_str)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError, parser.ParserError):
        return None


def format_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def is_within_last_n_days(date_str: str, n: int) -> bool:
    dt = parse_date(date_str)
    if not dt:
        return False
    now = datetime.now(timezone.utc)
    delta = now - dt
    return 0 <= delta.days <= n
