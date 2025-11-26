from typing import Optional

from bs4 import BeautifulSoup


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
