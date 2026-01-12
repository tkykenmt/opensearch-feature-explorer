---
tags:
  - indexing
  - search
---

# Derived Fields

## Summary

This release fixes a bug in derived field query rewriting that caused range queries to incorrectly return no results. The fix implements selective query rewriting based on query type, preventing `PointRangeQuery` and related queries from being rewritten in a way that breaks derived field functionality.

## Details

### What's New in v3.3.0

The `DerivedFieldQuery.rewrite()` method has been restored with intelligent query-type detection. Previously, the rewrite logic was commented out due to issues with range queries at the Lucene layer. This fix introduces a `needsRewrite()` method that selectively skips rewriting for query types that would break when rewritten against non-indexed derived fields.

### Technical Changes

#### Problem Background

Derived fields are computed dynamically from `_source` or doc values and are not indexed. When Lucene's `PointRangeQuery` is rewritten, it checks for point values in the index. Since derived fields have no indexed point values, the rewrite incorrectly returns a `MatchNoDocsQuery`, causing range queries on derived fields to return zero results.

#### Solution: Selective Rewrite

The fix adds a `needsRewrite()` method that checks the query type before attempting rewrite:

```java
private boolean needsRewrite() {
    if (query instanceof PointRangeQuery) {
        return false;
    }

    if (query instanceof ApproximateScoreQuery approximateQuery) {
        Query originalQuery = approximateQuery.getOriginalQuery();
        if (originalQuery instanceof IndexOrDocValuesQuery indexOrDocValuesQuery) {
            Query indexQuery = indexOrDocValuesQuery.getIndexQuery();
            return !(indexQuery instanceof PointRangeQuery);
        }
    }

    if (query instanceof IndexOrDocValuesQuery indexOrDocValuesQuery) {
        Query indexQuery = indexOrDocValuesQuery.getIndexQuery();
        return !(indexQuery instanceof PointRangeQuery);
    }

    return true;
}
```

#### Query Types Handled

| Query Type | Rewrite Behavior |
|------------|------------------|
| `PointRangeQuery` | Skip rewrite (return `this`) |
| `ApproximateScoreQuery` wrapping `IndexOrDocValuesQuery` with `PointRangeQuery` | Skip rewrite |
| `IndexOrDocValuesQuery` with `PointRangeQuery` | Skip rewrite |
| All other queries | Proceed with normal rewrite |

### Usage Example

Range queries on derived fields now work correctly:

```json
POST /logs/_search
{
  "query": {
    "range": {
      "derived_timestamp": {
        "gte": "2024-01-01",
        "lte": "2024-12-31"
      }
    }
  }
}
```

Where `derived_timestamp` is defined as:

```json
PUT /logs/_mapping
{
  "derived": {
    "derived_timestamp": {
      "type": "date",
      "script": {
        "source": "emit(Long.parseLong(doc['raw_timestamp'].value))"
      }
    }
  }
}
```

## Limitations

- Derived fields are still computed at query time, which may impact performance for large datasets
- Scoring and sorting on derived fields are not yet supported
- Chained derived fields (one derived field referencing another) are not supported

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/field-types/supported-field-types/derived/): Derived field type documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#19496](https://github.com/opensearch-project/OpenSearch/pull/19496) | Fix derived field rewrite to handle range queries |

### Issues (Design / RFC)
- [Issue #19337](https://github.com/opensearch-project/OpenSearch/issues/19337): Bug report for derived field rewrite issues

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/derived-fields.md)
