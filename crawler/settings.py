import os
from typing import Any

from crawler.utils.config import load_yaml

_crawler_cfg = load_yaml("crawler.yaml")


def _scrapy_cfg(key: str, default: Any) -> Any:
    return (_crawler_cfg.get("scrapy") or {}).get(key, default)


BOT_NAME = "rl_research_crawler"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = int(_scrapy_cfg("concurrent_requests", 8))
DOWNLOAD_DELAY = float(_scrapy_cfg("download_delay", 0.25))

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent": "rl-research-crawler/0.1 (+https://example.com)",
}

DOWNLOADER_MIDDLEWARES = {}
SPIDER_MIDDLEWARES = {}

ITEM_PIPELINES = {
    "crawler.pipelines.NormalizeArxivItemPipeline": 200,
    "crawler.pipelines.JsonWriterPipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL = os.getenv("SCRAPY_LOG_LEVEL", "INFO")
