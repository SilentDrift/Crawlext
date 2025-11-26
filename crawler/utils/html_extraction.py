from typing import Optional

from bs4 import BeautifulSoup
from crawler.utils.time_utils import parse_date, format_iso


def extract_main_text(html: Optional[str]) -> str:
    if not html:
        return ""

    soup = BeautifulSoup(html, "lxml")

    # Prefer article-like containers when present.
    article = soup.find("article")
    if article:
        return article.get_text(" ", strip=True)

    main = soup.find("main")
    if main:
        return main.get_text(" ", strip=True)

    # Fallback to body text.
    body = soup.find("body")
    if body:
        return body.get_text(" ", strip=True)

    return soup.get_text(" ", strip=True)


def extract_published_at(html: Optional[str]) -> Optional[str]:
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")

    meta_props = [
        ("meta", {"property": "article:published_time"}),
        ("meta", {"property": "og:published_time"}),
        ("meta", {"name": "pubdate"}),
        ("meta", {"name": "date"}),
        ("meta", {"name": "dc.date"}),
        ("meta", {"name": "dc.date.issued"}),
        ("meta", {"name": "dcterms.date"}),
        ("meta", {"name": "dcterms.created"}),
    ]
    for tag, attrs in meta_props:
        node = soup.find(tag, attrs=attrs)
        if node and node.get("content"):
            dt = parse_date(node.get("content"))
            if dt:
                return format_iso(dt)

    time_tag = soup.find("time")
    if time_tag:
        dt_val = time_tag.get("datetime") or time_tag.get_text(strip=True)
        dt = parse_date(dt_val)
        if dt:
            return format_iso(dt)

    return None
