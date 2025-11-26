from datetime import datetime

from crawler.utils import arxiv_client


def test_parse_arxiv_response_parses_entry():
    xml = """
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <id>http://arxiv.org/abs/1234.5678v1</id>
        <updated>2025-11-20T00:00:00Z</updated>
        <published>2025-11-20T00:00:00Z</published>
        <title>Reinforcement Learning Test</title>
        <summary>Some abstract about reinforcement learning.</summary>
        <author><name>A. Researcher</name></author>
        <category term="cs.LG" />
      </entry>
    </feed>
    """
    entries = arxiv_client.parse_arxiv_response(xml)
    assert len(entries) == 1
    entry = entries[0]
    assert entry["arxiv_id"] == "1234.5678v1"
    assert "Reinforcement Learning" in entry["title"]
    assert entry["categories"] == ["cs.LG"]


def test_build_query_url_includes_dates():
    start = datetime(2025, 11, 19)
    end = datetime(2025, 11, 26)
    url = arxiv_client.build_query_url("cat:cs.LG", start, end, 10)
    assert "submittedDate:[2025-11-19+TO+2025-11-26]" in url
