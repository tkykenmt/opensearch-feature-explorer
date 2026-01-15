---
tags:
  - opensearch
---
# Query Improvements

## Summary

OpenSearch v2.16.0 introduces two query-related improvements: the `indices.query.bool.max_clause_count` setting is now dynamically updateable without requiring a cluster restart, and `unsignedLongRangeQuery` now returns `MatchNoDocsQuery` when lower bounds exceed upper bounds for better query optimization.

## Details

### Dynamic Max Clause Count Setting

The `indices.query.bool.max_clause_count` setting controls the maximum number of clauses allowed in boolean queries and affects wildcard/prefix query expansion. Previously, this was a static setting requiring a cluster restart to change.

#### Before v2.16.0
- Setting was static (`Setting.Property.NodeScope` only)
- Required cluster restart to modify
- Defined in `SearchModule` class

#### After v2.16.0
- Setting is now dynamic (`Setting.Property.Dynamic`)
- Can be updated at runtime via cluster settings API
- Moved to `SearchService` class
- Uses `IndexSearcher.setMaxClauseCount()` for runtime updates

#### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `indices.query.bool.max_clause_count` | Maximum clauses in boolean queries | 1024 |

#### Usage Example

Update the setting dynamically:

```json
PUT _cluster/settings
{
  "transient": {
    "indices.query.bool.max_clause_count": 2048
  }
}
```

### UnsignedLong Range Query Optimization

Range queries on `unsigned_long` fields now return `MatchNoDocsQuery` immediately when the lower bound exceeds the upper bound, avoiding unnecessary query execution.

#### Technical Change

In `NumberFieldMapper.unsignedLongRangeQuery()`:

```java
if (l.compareTo(u) > 0) {
    return new MatchNoDocsQuery();
}
```

This optimization aligns with similar behavior in Lucene for other numeric types (see [LUCENE-8811](https://issues.apache.org/jira/browse/LUCENE-8811)).

## Limitations

- The `max_clause_count` setting change takes effect immediately but does not affect queries already in progress
- Setting very high values for `max_clause_count` can lead to memory issues with complex queries

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#13568](https://github.com/opensearch-project/OpenSearch/pull/13568) | Set INDICES_MAX_CLAUSE_COUNT dynamically | [#12549](https://github.com/opensearch-project/OpenSearch/issues/12549), [#1526](https://github.com/opensearch-project/OpenSearch/issues/1526) |
| [#14416](https://github.com/opensearch-project/OpenSearch/pull/14416) | Optimize UnsignedLong range queries to convert to MatchNoDocsQuery when lower > upper bounds | [#14404](https://github.com/opensearch-project/OpenSearch/issues/14404) |

### Documentation
- [Index Settings](https://docs.opensearch.org/2.16/install-and-configure/configuring-opensearch/index-settings/): Configuration reference
- [Query String](https://docs.opensearch.org/2.16/query-dsl/full-text/query-string/): Query string query documentation
