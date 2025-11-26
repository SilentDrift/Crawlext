import json
from datetime import datetime, timezone
from pathlib import Path

from scrapy.exceptions import DropItem

from crawler.items import ArxivRawItem, PaperItem
from crawler.utils import rl_classification, scoring, text_cleaning, time_utils
from crawler.utils.config import load_yaml


class NormalizeArxivItemPipeline:
    def __init__(self):
        cfg = load_yaml("crawler.yaml")
        self.window_days = int((cfg.get("window") or {}).get("date_window_days", 7))

    def process_item(self, item, spider):
        if not isinstance(item, ArxivRawItem):
            return item

        submitted_at = item.get("submitted_at")
        if not time_utils.is_within_last_n_days(submitted_at, self.window_days):
            raise DropItem(f"Arxiv item outside window: {submitted_at}")

        title = item.get("title") or ""
        abstract = item.get("abstract") or ""
        clean_blob = f"{text_cleaning.clean_text(title)} {text_cleaning.clean_text(abstract)}"
        rl_tags = rl_classification.classify_rl(clean_blob)
        if not rl_tags:
            rl_tags = ["general_dl"]

        paper = PaperItem()
        paper["source"] = "arxiv"
        paper["arxiv_id"] = item.get("arxiv_id")
        paper["url"] = item.get("url")
        paper["title"] = title.strip()
        paper["authors"] = item.get("authors") or []
        paper["abstract"] = abstract.strip()
        paper["categories"] = item.get("categories") or []
        paper["submitted_at"] = submitted_at
        paper["updated_at"] = item.get("updated_at")
        paper["rl_tags"] = rl_tags
        paper["attention_score"] = scoring.compute_attention_score(rl_tags, "arxiv", submitted_at)
        paper["collected_at"] = time_utils.format_iso(datetime.now(timezone.utc))
        return paper


class JsonWriterPipeline:
    def __init__(self):
        cfg = load_yaml("crawler.yaml")
        out_cfg = cfg.get("output") or {}
        self.normalized_dir = Path(out_cfg.get("normalized_dir", "data/normalized"))
        self.normalized_dir.mkdir(parents=True, exist_ok=True)
        self.date_str = datetime.now(timezone.utc).date().isoformat()
        self.paper_file = None
        self.post_file = None

    def open_spider(self, spider):
        self.paper_file = (self.normalized_dir / f"papers_{self.date_str}.jsonl").open(
            "a", encoding="utf-8"
        )
        self.post_file = None

    def close_spider(self, spider):
        for handle in (self.paper_file, self.post_file):
            if handle and not handle.closed:
                handle.close()

    def process_item(self, item, spider):
        if isinstance(item, PaperItem):
            self._write(self.paper_file, item)
            return item
        return item

    def _write(self, handle, item):
        if not handle:
            return
        handle.write(json.dumps(dict(item), ensure_ascii=False) + "\n")
