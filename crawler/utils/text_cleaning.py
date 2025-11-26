import re
from typing import Optional

from bs4 import BeautifulSoup

WHITESPACE_RE = re.compile(r"\s+")


def strip_html(raw: Optional[str]) -> str:
    if not raw:
        return ""
    soup = BeautifulSoup(raw, "lxml")
    return soup.get_text(" ", strip=True)


def clean_text(raw: Optional[str]) -> str:
    text = strip_html(raw)
    text = text.lower()
    text = WHITESPACE_RE.sub(" ", text)
    return text.strip()
