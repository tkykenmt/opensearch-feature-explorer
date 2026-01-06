#!/usr/bin/env python3
"""OpenSearch Documentation MCP Server."""

import json
import sys
import urllib.request
import urllib.parse


def search(query: str, version: str = "3.0", types: str = "docs,blogs", 
           limit: int = 10, offset: int = 0) -> dict:
    """Search OpenSearch docs and blogs."""
    encoded = urllib.parse.quote(query)
    url = f"https://search-api.opensearch.org/search?q={encoded}&v={version}&t={types}"
    
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    
    all_results = data.get("results", [])
    total = len(all_results)
    page_results = all_results[offset:offset + limit]
    
    results = []
    for r in page_results:
        item_url = r["url"]
        if r["type"] == "DOCS":
            item_url = f"https://docs.opensearch.org{item_url}"
        results.append({
            "title": r["title"],
            "url": item_url,
            "type": r["type"],
            "snippet": r.get("content", "")[:300]
        })
    
    return {
        "query": query,
        "version": version,
        "total": total,
        "offset": offset,
        "limit": limit,
        "hasMore": offset + limit < total,
        "results": results
    }


def handle_request(request: dict) -> dict:
    """Handle JSON-RPC request."""
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "opensearch-docs", "version": "1.0.0"}
            }
        }
    
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [{
                    "name": "search",
                    "description": "Search OpenSearch documentation and blogs. Use offset for pagination.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                            "version": {"type": "string", "description": "OpenSearch version (default: 3.0)"},
                            "types": {"type": "string", "description": "docs, blogs, or docs,blogs"},
                            "limit": {"type": "integer", "description": "Max results per page (default: 10)"},
                            "offset": {"type": "integer", "description": "Skip first N results for pagination (default: 0)"}
                        },
                        "required": ["query"]
                    }
                }]
            }
        }
    
    if method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "search":
            try:
                result = search(
                    query=args["query"],
                    version=args.get("version", "3.0"),
                    types=args.get("types", "docs,blogs"),
                    limit=args.get("limit", 10),
                    offset=args.get("offset", 0)
                )
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True}
                }
    
    if method == "notifications/initialized":
        return None
    
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    """Run MCP server over stdio."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response:
                print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    main()
