#!/usr/bin/env python3
"""Standalone OpenSearch documentation search script (no external dependencies)."""

import argparse
import json
import sys
import urllib.parse
import urllib.request


def _fetch_docs(query: str, version: str, types: str) -> list:
    encoded = urllib.parse.quote(query)
    url = f"https://search-api.opensearch.org/search?q={encoded}&v={version}&t={types}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read().decode()).get("results", [])


def _fetch_forum(query: str) -> tuple:
    encoded = urllib.parse.quote(query)
    url = f"https://forum.opensearch.org/search/query?term={encoded}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    posts = data.get("posts", [])
    topics = {t["id"]: t for t in data.get("topics", [])}
    has_more = data.get("grouped_search_result", {}).get("more_posts", False)
    return posts, topics, has_more


def search_docs(query: str, version: str = "latest", limit: int = 10, offset: int = 0) -> dict:
    all_results = _fetch_docs(query, version, "docs")
    page = all_results[offset : offset + limit]
    return {
        "query": query, "total": len(all_results), "hasMore": offset + limit < len(all_results),
        "results": [{"title": r["title"], "url": f"https://docs.opensearch.org{r['url']}", "snippet": r.get("content", "")[:300]} for r in page]
    }


def search_blogs(query: str, version: str = "latest", limit: int = 10, offset: int = 0) -> dict:
    all_results = _fetch_docs(query, version, "blogs")
    page = all_results[offset : offset + limit]
    return {
        "query": query, "total": len(all_results), "hasMore": offset + limit < len(all_results),
        "results": [{"title": r["title"], "url": r["url"], "snippet": r.get("content", "")[:300]} for r in page]
    }


def search_forum(query: str, limit: int = 10) -> dict:
    posts, topics, has_more = _fetch_forum(query)
    results = []
    for p in posts[:limit]:
        topic = topics.get(p.get("topic_id"), {})
        results.append({
            "title": topic.get("title", ""),
            "url": f"https://forum.opensearch.org/t/{topic.get('slug', '')}/{p.get('topic_id')}",
            "snippet": p.get("blurb", "")[:300],
        })
    return {"query": query, "total": len(results), "hasMore": has_more, "results": results}


def main():
    parser = argparse.ArgumentParser(description="Search OpenSearch docs/blogs/forum")
    sub = parser.add_subparsers(dest="cmd", required=True)

    for name, fn in [("docs", search_docs), ("blogs", search_blogs), ("forum", search_forum)]:
        p = sub.add_parser(name)
        p.add_argument("query")
        if name != "forum":
            p.add_argument("-v", "--version", default="latest")
            p.add_argument("-o", "--offset", type=int, default=0)
        p.add_argument("-l", "--limit", type=int, default=10)

    args = parser.parse_args()
    if args.cmd == "docs":
        result = search_docs(args.query, args.version, args.limit, args.offset)
    elif args.cmd == "blogs":
        result = search_blogs(args.query, args.version, args.limit, args.offset)
    else:
        result = search_forum(args.query, args.limit)

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
