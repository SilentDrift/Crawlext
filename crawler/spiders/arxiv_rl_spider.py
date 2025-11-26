from datetime import datetime, timedelta, timezone

import scrapy

from crawler.items import ArxivRawItem
from crawler.utils import arxiv_client, time_utils
from crawler.utils.config import load_yaml


class ArxivRlSpider(scrapy.Spider):
    name = "arxiv_rl_spider"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cfg = load_yaml("arxiv_queries.yaml").get("arxiv") or {}
        self.date_window_days = int(cfg.get("date_window_days", 7))
        self.max_results = int(cfg.get("max_results_per_query", 200))
        self.queries = cfg.get("queries") or []

    def start_requests(self):
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=self.date_window_days)
        for query in self.queries:
            search_query = query.get("search_query")
            query_id = query.get("id")
            if not search_query:
                continue
            url = arxiv_client.build_query_url(search_query, start_date, end_date, self.max_results)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"query_id": query_id, "search_query": search_query},
            )

    def parse(self, response):
        query_id = response.meta.get("query_id")
        entries = arxiv_client.parse_arxiv_response(response.text)
        for entry in entries:
            submitted_at = entry.get("submitted_at")
            if submitted_at and not time_utils.is_within_last_n_days(submitted_at, self.date_window_days):
                continue
            yield ArxivRawItem(
                source="arxiv",
                query_id=query_id,
                arxiv_id=entry.get("arxiv_id"),
                url=entry.get("url"),
                title=entry.get("title"),
                authors=entry.get("authors"),
                abstract=entry.get("abstract"),
                categories=entry.get("categories"),
                submitted_at=submitted_at,
                updated_at=entry.get("updated_at"),
                raw_meta={"search_query": response.meta.get("search_query")},
            )
