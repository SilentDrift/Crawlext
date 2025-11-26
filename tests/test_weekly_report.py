import json
from datetime import datetime, timezone

from aggregation import weekly_report


def test_weekly_report_generates(monkeypatch, tmp_path):
    normalized = tmp_path / "normalized"
    reports = tmp_path / "reports"
    normalized.mkdir()
    reports.mkdir()

    today = datetime.now(timezone.utc).date().isoformat()
    paper = {
        "title": "Reinforcement Learning Sample",
        "arxiv_id": "1234.5678",
        "authors": ["A. Researcher"],
        "abstract": "policy gradient in RL",
        "submitted_at": f"{today}T00:00:00Z",
        "url": "https://arxiv.org/abs/1234.5678",
        "rl_tags": ["deep_rl"],
        "attention_score": 0.9,
    }
    post = {
        "title": "Blog RL Post",
        "source": "deepmind",
        "published_at": f"{today}T00:00:00Z",
        "url": "https://example.com/post",
        "text": "policy gradient explanation",
        "rl_tags": ["deep_rl"],
        "attention_score": 0.8,
    }

    (normalized / f"papers_{today}.jsonl").write_text(json.dumps(paper) + "\n", encoding="utf-8")
    (normalized / f"posts_{today}.jsonl").write_text(json.dumps(post) + "\n", encoding="utf-8")

    def fake_load_yaml(name: str):
        if name == "crawler.yaml":
            return {"output": {"normalized_dir": str(normalized), "reports_dir": str(reports)}, "window": {"date_window_days": 7}}
        if name == "rl_taxonomy.yaml":
            return {"categories": [{"id": "deep_rl", "name": "Deep RL"}]}
        return {}

    monkeypatch.setattr(weekly_report, "load_yaml", fake_load_yaml)
    path = weekly_report.generate()
    content = path.read_text(encoding="utf-8")
    assert "Deep RL" in content
    assert "Reinforcement Learning Sample" in content
