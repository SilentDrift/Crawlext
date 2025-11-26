from typing import List

from crawler.utils.config import load_yaml

_taxonomy = load_yaml("rl_taxonomy.yaml").get("categories", [])


def classify_rl(text: str) -> List[str]:
    tags: List[str] = []
    text_l = (text or "").lower()
    for category in _taxonomy:
        keywords = category.get("keywords") or []
        min_hits = category.get("min_hits", 1)
        hits = sum(1 for kw in keywords if kw.lower() in text_l)
        if hits >= min_hits:
            tags.append(category.get("id"))
    return tags
