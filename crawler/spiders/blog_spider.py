from datetime import datetime, timezone
from typing import Iterable

import scrapy
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
import feedparser

from crawler.items import BlogRawItem
from crawler.utils.config import load_yaml


class BlogSpider(scrapy.Spider):
    name = "blog_spider"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cfg = load_yaml("sources.yaml")
        self.sources = cfg.get("blogs") or []

    def start_requests(self):
        for source in self.sources:
            source_id = source.get("id")
            stype = source.get("type")
            if stype == "rss" and source.get("rss_url"):
                yield scrapy.Request(
                    source["rss_url"],
                    callback=self.parse_rss,
                    meta={"source_id": source_id},
                )
            elif stype == "html" and source.get("base_url"):
                base = source.get("base_url").rstrip("/")
                list_path = source.get("list_path", "")
                if list_path.startswith("http"):
                    url = list_path
                elif list_path.startswith("/"):
                    url = f"{base}{list_path}"
                elif list_path:
                    url = f"{base}/{list_path}"
                else:
                    url = base
                yield scrapy.Request(
                    url,
                    callback=self.parse_html_index,
                    meta={"source_id": source_id},
                )

    def parse_rss(self, response):
        source_id = response.meta.get("source_id")
        feed = feedparser.parse(response.text)
        for entry in feed.entries:
            published = entry.get("published") or entry.get("updated")
            yield BlogRawItem(
                source=source_id,
                url=entry.get("link"),
                title=entry.get("title"),
                published_at=self._safe_iso(published),
                html=entry.get("summary") or entry.get("content", [{}])[0].get("value"),
            )

    def parse_html_index(self, response):
        source_id = response.meta.get("source_id")
        soup = BeautifulSoup(response.text, "lxml")
        links = self._extract_links(soup)
        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(
                url,
                callback=self.parse_article,
                meta={"source_id": source_id},
            )

    def parse_article(self, response):
        source_id = response.meta.get("source_id")
        soup = BeautifulSoup(response.text, "lxml")
        title_tag = soup.find("h1") or soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else response.url
        date_tag = soup.find("time")
        published = date_tag.get("datetime") if date_tag else None
        yield BlogRawItem(
            source=source_id,
            url=response.url,
            title=title,
            published_at=self._safe_iso(published),
            html=response.text,
        )

    def _extract_links(self, soup: BeautifulSoup) -> Iterable[str]:
        selectors = ["article a", "h2 a", "h3 a", "a"]
        seen = set()
        for selector in selectors:
            for tag in soup.select(selector):
                href = tag.get("href")
                if href and href not in seen and href.startswith(("/", "http")):
                    seen.add(href)
                    yield href

    def _safe_iso(self, date_str):
        if not date_str:
            return None
        try:
            return date_parser.parse(date_str).astimezone(timezone.utc).isoformat()
        except (ValueError, TypeError, OverflowError, date_parser.ParserError):
            return None
