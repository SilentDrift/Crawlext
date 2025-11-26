# Crawlext

Weekly Scrapy-based research radar that crawls arXiv and key RL/DL blogs, filters and scores papers and posts, and generates structured digests summarizing the most relevant recent work for reinforcement learning.

## What it does
- Hits arXiv with a set of ML/RL queries for the last `N` days (default 7).
- Crawls configured blogs (RSS or HTML list pages), extracts article text, filters for RL/DL relevance.
- Classifies content with keyword taxonomy, computes a heuristic attention score, and writes normalized JSONL.
- Builds a weekly Markdown report sorted by topic and score.

## Quickstart
1) Create and activate a virtualenv, then install deps:
```
pip install -r requirements.txt
```
2) Copy `.env.example` to `.env` and adjust if needed.
3) Run crawls (uses configs in `configs/`):
```
python scripts/run_arxiv_crawl.py
python scripts/run_blog_crawl.py
```
4) Generate a digest for the last 7 days:
```
python scripts/generate_weekly_report.py
```

## Layout
- `configs/`: arXiv queries, blog sources, RL taxonomy, crawler knobs.
- `crawler/`: Scrapy project (spiders, pipelines, utils).
- `aggregation/weekly_report.py`: turns JSONL into Markdown digest.
- `scripts/`: small entrypoints to run crawls and report.
- `data/`: raw/normalized JSONL plus reports (git-ignored in practice).
- `tests/`: lightweight unit tests for classification, scoring, report, client parsing.

## Notes
- Default window is 7 days; change via `configs/crawler.yaml`.
- Taxonomy/keywords are intentionally simple and easy to tweak in `configs/rl_taxonomy.yaml`.
- Attention score is heuristic: tag strength + source weight + recency.
- Spiders are conservative: RL/DL specialization lives in pipelines; spiders mostly fetch candidates.
