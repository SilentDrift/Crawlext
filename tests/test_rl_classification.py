from crawler.utils import rl_classification


def test_classify_rl_hits_deep_rl():
    text = "We study a reinforcement learning method with policy gradient and actor-critic updates."
    tags = rl_classification.classify_rl(text)
    assert "deep_rl" in tags


def test_classify_rl_respects_min_hits():
    text = "This paper uses transformers for representation learning."
    tags = rl_classification.classify_rl(text)
    assert "general_dl" in tags
