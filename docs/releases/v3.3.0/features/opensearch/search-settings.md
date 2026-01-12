---
tags:
  - search
  - security
---

# Search Settings

## Summary

OpenSearch v3.3.0 introduces a new cluster-wide setting `search.query.max_query_string_length` that limits the maximum length of query strings in `query_string` and `simple_query_string` queries. This provides a simple but robust mechanism to control inputs from potentially untrusted sources and prevent resource exhaustion from excessively long query strings.

## Details

### What's New in v3.3.0

A new dynamic cluster setting has been added to limit the maximum allowed length of query strings used in Lucene-style query string queries.

### Technical Changes

#### New Configuration

| Setting | Description | Default | Min | Max |
|---------|-------------|---------|-----|-----|
| `search.query.max_query_string_length` | Maximum allowed length for query strings in `query_string` and `simple_query_string` queries | 32,000 | 1 | Integer.MAX_VALUE |

#### Setting Properties

- **Scope**: Node-level (applies cluster-wide)
- **Dynamic**: Yes (can be updated without restart)
- **Type**: Integer

#### Implementation Details

The setting is enforced in `QueryStringQueryParser.parse()` method. When a query string exceeds the configured limit, a `ParseException` is thrown with a descriptive error message:

```
Query string length exceeds max allowed length {limit} (search.query.max_query_string_length); actual length: {actual}
```

### Usage Example

Update the setting dynamically via the Cluster Settings API:

```json
PUT _cluster/settings
{
  "transient": {
    "search.query.max_query_string_length": 10000
  }
}
```

Or configure in `opensearch.yml`:

```yaml
search.query.max_query_string_length: 10000
```

### Use Cases

- **Security hardening**: Prevent denial-of-service attacks via extremely long query strings
- **Resource protection**: Limit memory and CPU usage from parsing complex queries
- **Input validation**: Enforce reasonable limits on user-provided search queries

### Migration Notes

No migration required. The default value of 32,000 characters is generous enough for most use cases. Adjust only if you need stricter limits or have legitimate use cases requiring longer query strings.

## Limitations

- Only applies to `query_string` and `simple_query_string` query types
- Does not limit other query types or the overall request body size
- The check occurs at parse time, so invalid queries may still consume some resources before being rejected

## References

### Documentation
- [Query String Query Documentation](https://docs.opensearch.org/latest/query-dsl/full-text/query-string/): Official query string query docs
- [Search Settings Documentation](https://docs.opensearch.org/latest/install-and-configure/configuring-opensearch/search-settings/): Search configuration reference
- [PR #19491](https://github.com/opensearch-project/OpenSearch/pull/19491): Main implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#19491](https://github.com/opensearch-project/OpenSearch/pull/19491) | Introduced new setting search.query.max_query_string_length |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-search-settings.md)
