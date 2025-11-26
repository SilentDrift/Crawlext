import os
from datetime import datetime
from typing import Dict, List, Optional
from xml.etree import ElementTree

ARXIV_API_URL = os.getenv("ARXIV_API_URL", "https://export.arxiv.org/api/query")


def build_query_url(search_query: str, start_date: datetime, end_date: datetime, max_results: int) -> str:
    date_clause = f"submittedDate:[{start_date.strftime('%Y%m%d')}0000+TO+{end_date.strftime('%Y%m%d')}2359]"
    query = f"({search_query})+AND+{date_clause}"
    return (
        f"{ARXIV_API_URL}?"
        f"search_query={query}"
        f"&sortBy=submittedDate&sortOrder=descending"
        f"&max_results={max_results}"
    )


def parse_arxiv_response(response_body: str) -> List[Dict[str, Optional[str]]]:
    entries: List[Dict[str, Optional[str]]] = []
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ElementTree.fromstring(response_body)
    except ElementTree.ParseError:
        return entries

    for entry in root.findall("atom:entry", ns):
        entry_id = (entry.findtext("atom:id", default="", namespaces=ns) or "").split("/abs/")[-1]
        title = entry.findtext("atom:title", default="", namespaces=ns)
        summary = entry.findtext("atom:summary", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)
        updated = entry.findtext("atom:updated", default="", namespaces=ns)
        authors = [a.findtext("atom:name", default="", namespaces=ns) for a in entry.findall("atom:author", ns)]
        categories = [c.attrib.get("term") for c in entry.findall("atom:category", ns) if c.attrib.get("term")]

        entries.append(
            {
                "arxiv_id": entry_id,
                "title": title,
                "abstract": summary,
                "authors": [a for a in authors if a],
                "categories": categories,
                "submitted_at": published,
                "updated_at": updated,
                "url": f"https://arxiv.org/abs/{entry_id}" if entry_id else None,
            }
        )
    return entries
