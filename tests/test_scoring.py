from datetime import datetime, timedelta, timezone

from crawler.utils import scoring


def test_priority_weight_affects_score():
    today = datetime.now(timezone.utc).isoformat()
    high = scoring.compute_attention_score(["deep_rl"], "deepmind", today)
    low = scoring.compute_attention_score(["deep_rl"], "misc_personal", today)
    assert high > low


def test_recency_boost():
    today = datetime.now(timezone.utc).isoformat()
    old = (datetime.now(timezone.utc) - timedelta(days=6)).isoformat()
    recent_score = scoring.compute_attention_score(["deep_rl"], "arxiv", today)
    old_score = scoring.compute_attention_score(["deep_rl"], "arxiv", old)
    assert recent_score >= old_score
