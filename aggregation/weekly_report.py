from collections import defaultdict
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List

from crawler.utils.config import load_yaml
from crawler.utils import time_utils


def _recent_files(directory: Path, pattern: str, window_days: int) -> Iterable[Path]:
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=window_days)
    for path in sorted(directory.glob(pattern)):
        try:
            date_part = path.stem.split("_")[-1]
            file_date = datetime.fromisoformat(date_part).date()
            if file_date >= cutoff:
                yield path
        except ValueError:
            continue


def _load_jsonl(paths: Iterable[Path]) -> List[dict]:
    items: List[dict] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return items


def _group_by_tag(papers: List[dict], posts: List[dict]) -> Dict[str, dict]:
    grouped: Dict[str, dict] = defaultdict(lambda: {"papers": [], "posts": []})
    for paper in papers:
        for tag in paper.get("rl_tags", []):
            grouped[tag]["papers"].append(paper)
    for post in posts:
        for tag in post.get("rl_tags", []):
            grouped[tag]["posts"].append(post)
    for tag in grouped:
        grouped[tag]["papers"].sort(key=lambda x: x.get("attention_score", 0), reverse=True)
        grouped[tag]["posts"].sort(key=lambda x: x.get("attention_score", 0), reverse=True)
    return grouped


def generate(window_days: int | None = None) -> Path:
    crawler_cfg = load_yaml("crawler.yaml")
    out_cfg = crawler_cfg.get("output") or {}
    normalized_dir = Path(out_cfg.get("normalized_dir", "data/normalized"))
    reports_dir = Path(out_cfg.get("reports_dir", "data/reports"))
    reports_dir.mkdir(parents=True, exist_ok=True)

    taxonomy = load_yaml("rl_taxonomy.yaml").get("categories") or []
    window = window_days or int((crawler_cfg.get("window") or {}).get("date_window_days", 7))

    paper_files = list(_recent_files(normalized_dir, "papers_*.jsonl", window))
    post_files = list(_recent_files(normalized_dir, "posts_*.jsonl", window))
    papers = [p for p in _load_jsonl(paper_files) if time_utils.is_within_last_n_days(p.get("submitted_at"), window)]
    posts = [p for p in _load_jsonl(post_files) if time_utils.is_within_last_n_days(p.get("published_at"), window)]
    grouped = _group_by_tag(papers, posts)

    today = datetime.now(timezone.utc).date().isoformat()
    lines: List[str] = [f"# RL / DL Weekly Digest — {today}", ""]

    for category in taxonomy:
        cat_id = category.get("id")
        cat_name = category.get("name", cat_id)
        bucket = grouped.get(cat_id, {"papers": [], "posts": []})
        if not bucket["papers"] and not bucket["posts"]:
            continue
        lines.append(f"## {cat_name}")

        if bucket["papers"]:
            lines.append("")
            lines.append("### Top arXiv papers")
            for idx, paper in enumerate(bucket["papers"], 1):
                lines.append(f"{idx}. **{paper.get('title','').strip()}** (arXiv:{paper.get('arxiv_id')}) — {', '.join(paper.get('authors', []))}")
                lines.append(f"   - Score: {paper.get('attention_score')}")
                abstract = (paper.get("abstract") or "").strip()
                if abstract:
                    lines.append(f"   - Abstract: {abstract}")
                lines.append(f"   - URL: {paper.get('url')}")
                lines.append("")

        if bucket["posts"]:
            lines.append("### Top blog posts")
            for idx, post in enumerate(bucket["posts"], 1):
                lines.append(f"{idx}. **{post.get('title','').strip()}**")
                lines.append(f"   - Source: {post.get('source')} | Score: {post.get('attention_score')}")
                snippet = (post.get("text") or "").strip()
                if snippet:
                    lines.append(f"   - Summary: {snippet[:500]}")
                lines.append(f"   - URL: {post.get('url')}")
                lines.append("")

        lines.append("---")

    if len(lines) == 2:
        lines.append("No items found for this window.")

    report_path = reports_dir / f"weekly_report_{today}.md"
    report_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return report_path


if __name__ == "__main__":
    path = generate()
    print(f"Wrote report to {path}")
