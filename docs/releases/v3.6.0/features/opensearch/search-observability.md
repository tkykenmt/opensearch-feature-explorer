---
tags:
  - opensearch
---
# Search Observability

## Summary

In v3.6.0, the search request slow log now includes the `indices` field, showing which index names or patterns were targeted by a search request. Previously, slow log entries only contained the query source, shard stats, and timing information, making it difficult to identify which index a slow request was executed against.

## Details

### What's New in v3.6.0

The `SearchRequestSlowLog` class was updated to include the `indices` field in both the structured (JSON) and plaintext log output formats. The indices are extracted from `context.getRequest().indices()` and formatted using `Arrays.toString()`.

#### Slow Log Output Changes

Before v3.6.0:
```
took[80.8ms], took_millis[80], phase_took_millis[{...}], total_hits[4 hits], search_type[QUERY_THEN_FETCH], shards[{...}], source[{...}], id[]
```

After v3.6.0:
```
took[80.8ms], took_millis[80], phase_took_millis[{...}], total_hits[4 hits], search_type[QUERY_THEN_FETCH], shards[{...}], indices[index_1, index_2, my_index_*], source[{...}], id[]
```

The `indices` field appears between `shards` and `source` in the log output.

#### JSON Log Fields

The structured JSON log now includes an `indices` key:

| Field | Description | Example |
|-------|-------------|---------|
| `indices` | Target index names/patterns from the search request | `[index_1, index_2, my_index_*]` |

When no indices are specified (e.g., `/_search`), the field shows `[]`.

### Technical Changes

The change modifies `SearchRequestSlowLog.java` in the `server` module:

- Added `java.util.Arrays` import
- In `prepareMap()` (JSON output): added `messageFields.put("indices", Arrays.toString(context.getRequest().indices()))`
- In `message()` (plaintext output): added `sb.append("indices").append(Arrays.toString(context.getRequest().indices())).append(", ")`

### Example Slow Log Entries

Single index search (`/index_1,index_2,my_index_*/_search`):
```
[2026-02-10T07:58:07,922][WARN ][o.o.a.s.SearchRequestSlowLog] [runTask-0] took[32.1ms], took_millis[32], phase_took_millis[{expand=0, query=25, fetch=1}], total_hits[0 hits], search_type[QUERY_THEN_FETCH], shards[{total:2, successful:2, skipped:0, failed:0}], indices[index_1, index_2, my_index_*], source[{"query":{"match_all":{"boost":1.0}}}], id[], request_id[]
```

Wildcard search (`/*/_search`):
```
indices[*]
```

No index specified (`/_search`):
```
indices[]
```

## Limitations

- The `indices` field shows the raw index names/patterns as provided in the request, not the resolved concrete indices
- Wildcard patterns are logged as-is without expansion

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/OpenSearch/pull/20588` | Add indices to search request slowlog | `https://github.com/opensearch-project/OpenSearch/issues/20531` |

### Documentation
- https://docs.opensearch.org/latest/install-and-configure/configuring-opensearch/logs/
