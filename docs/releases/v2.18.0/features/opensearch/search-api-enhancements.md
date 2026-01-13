---
tags:
  - domain/core
  - component/server
  - indexing
  - search
---
# Search API Enhancements

## Summary

OpenSearch 2.18.0 introduces internal API enhancements to support the Query Insights plugin's query shape feature. These changes add the `WithFieldName` interface to aggregation and sort builders, and expose successful search shard indices in the search request context.

## Details

### What's New in v2.18.0

Two key enhancements improve the internal search API infrastructure:

1. **WithFieldName Interface Implementation**: `ValuesSourceAggregationBuilder` and `FieldSortBuilder` now implement the `WithFieldName` interface, providing a uniform way to retrieve field names from these builders.

2. **Successful Search Shard Indices**: The `SearchRequestContext` now tracks which indices were successfully queried at the shard level, enabling better query analysis and insights.

### Technical Changes

#### New Interface Implementation

The `WithFieldName` interface provides a standardized method to retrieve field names from query components:

```java
public interface WithFieldName {
    String fieldName();
}
```

Classes implementing this interface in v2.18.0:
- `ValuesSourceAggregationBuilder` - Base class for all values-source aggregations
- `FieldSortBuilder` - Builder for field-based sorting

#### New Components

| Component | Description |
|-----------|-------------|
| `WithFieldName` interface | Standardized interface for retrieving field names from builders |
| `successfulSearchShardIndices` | New field in `SearchRequestContext` tracking successful shard indices |

#### API Changes

**SearchRequestContext**:
```java
// New method to get indices that were successfully queried
public Set<String> getSuccessfulSearchShardIndices()
```

**ValuesSourceAggregationBuilder**:
```java
// New method implementing WithFieldName interface
@Override
public String fieldName() {
    return field();
}
```

**FieldSortBuilder**:
```java
// New method implementing WithFieldName interface
@Override
public String fieldName() {
    return getFieldName();
}
```

### Usage Example

These changes are primarily internal APIs used by the Query Insights plugin for query shape generation:

```java
// Query Insights can now uniformly check for field names
if (builder instanceof WithFieldName) {
    String fieldName = ((WithFieldName) builder).fieldName();
    // Use fieldName for query shape construction
}

// Access successful shard indices from search context
Set<String> successfulIndices = searchRequestContext.getSuccessfulSearchShardIndices();
```

### Migration Notes

These are internal API changes. No migration is required for end users. Plugin developers using these classes may benefit from the new `WithFieldName` interface for uniform field name access.

## Limitations

- The `WithFieldName` interface only provides access to a single field name; queries operating on multiple fields are not covered
- `successfulSearchShardIndices` is populated only after search completion

## References

### Documentation
- [Query Insights Documentation](https://docs.opensearch.org/2.18/observing-your-data/query-insights/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#15916](https://github.com/opensearch-project/OpenSearch/pull/15916) | Implement WithFieldName interface in ValuesSourceAggregationBuilder & FieldSortBuilder |
| [#15967](https://github.com/opensearch-project/OpenSearch/pull/15967) | Add successfulSearchShardIndices in searchRequestContext |
| [#15705](https://github.com/opensearch-project/OpenSearch/pull/15705) | Adding WithFieldName interface for QueryBuilders with fieldName (prerequisite) |

### Issues (Design / RFC)
- [Issue #69](https://github.com/opensearch-project/query-insights/issues/69): Query Shape Field Data Type RFC

## Related Feature Report

- Full feature documentation
