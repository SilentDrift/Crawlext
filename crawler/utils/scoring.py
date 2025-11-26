from datetime import datetime, timezone
from typing import List

from crawler.utils.config import load_yaml
from crawler.utils.time_utils import parse_date

_sources = {entry["id"]: entry for entry in load_yaml("sources.yaml").get("blogs", [])}


def compute_attention_score(
    rl_tags: List[str],
    source_id: str,
    published_at: str,
    is_featured: bool = False,
) -> float:
    weight = float((_sources.get(source_id) or {}).get("priority_weight", 1.0))
    base = 0.4 + 0.2 * min(len(rl_tags), 3)
    score = base * weight

    dt = parse_date(published_at)
    if dt:
        days_old = (datetime.now(timezone.utc) - dt).days
        recency_boost = max(0.0, 1 - min(days_old, 7) / 7) * 0.3
        score += recency_boost

    if is_featured:
        score += 0.2

    return round(score, 3)
