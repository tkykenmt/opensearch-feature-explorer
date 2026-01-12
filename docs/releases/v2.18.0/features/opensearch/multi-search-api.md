---
tags:
  - indexing
  - search
---

# Multi-Search API

## Summary

This release fixes a bug where the Multi-Search Template API (`_msearch/template`) did not return a `status` field in each search response, unlike the regular Multi-Search API (`_msearch`). This fix ensures response consistency between the two similar APIs, making it easier for clients to handle responses uniformly.

## Details

### What's New in v2.18.0

The Multi-Search Template API now includes a `status` field in each response item, matching the behavior of the Multi-Search API. This applies to both successful responses and error responses.

### Technical Changes

#### Response Format Change

Before v2.18.0, the `_msearch/template` response did not include status codes:

```json
{
  "took": 5,
  "responses": [
    {
      "took": 3,
      "timed_out": false,
      "_shards": { ... },
      "hits": { ... }
    }
  ]
}
```

After v2.18.0, each response includes a `status` field:

```json
{
  "took": 5,
  "responses": [
    {
      "took": 3,
      "timed_out": false,
      "_shards": { ... },
      "hits": { ... },
      "status": 200
    }
  ]
}
```

#### Modified Components

| Component | Description |
|-----------|-------------|
| `MultiSearchTemplateResponse.java` | Added `status` field to failure responses using `ExceptionsHelper.status()` |
| `SearchTemplateResponse.java` | Added `status` field to successful responses using `response.status().getStatus()` |

#### Status Codes

The `status` field returns standard HTTP status codes:

| Status | Meaning |
|--------|---------|
| 200 | Successful search |
| 400 | Bad request (e.g., invalid query, malformed template) |
| 404 | Index not found |

### Usage Example

```json
GET _msearch/template
{"index":"my-index"}
{"id":"my_template","params":{"query_text":"search term"}}
{"index":"unknown_index"}
{"id":"my_template","params":{"query_text":"another term"}}
```

Response:

```json
{
  "took": 10,
  "responses": [
    {
      "took": 5,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": { "value": 10, "relation": "eq" },
        "max_score": 1.0,
        "hits": [...]
      },
      "status": 200
    },
    {
      "error": {
        "type": "index_not_found_exception",
        "reason": "no such index [unknown_index]",
        "root_cause": [...]
      },
      "status": 404
    }
  ]
}
```

### Migration Notes

This is a backward-compatible change. Existing clients will continue to work, but can now optionally use the `status` field for more consistent error handling across `_msearch` and `_msearch/template` APIs.

## Limitations

- The fix only affects the Multi-Search Template API response format
- No changes to request format or query behavior

## References

### Documentation
- [Multi-Search Template Documentation](https://docs.opensearch.org/2.18/api-reference/msearch-template/): Official API documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#16265](https://github.com/opensearch-project/OpenSearch/pull/16265) | Fix multi-search with template doesn't return status code |

### Issues (Design / RFC)
- [Issue #11133](https://github.com/opensearch-project/OpenSearch/issues/11133): Bug report - MultiSearchTemplateResponse does not return a status field
- [Issue #708](https://github.com/opensearch-project/opensearch-java/issues/708): Related Java client issue

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/multi-search-api.md)
