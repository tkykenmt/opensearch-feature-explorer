---
tags:
  - indexing
  - neural-search
  - search
---

# Neural Search Compatibility

## Summary

This release item updates the neural-search plugin for OpenSearch 3.0 compatibility. The changes include adapting to Lucene 10 API changes, updating to the latest OpenSearch core APIs, and improving CI/CD infrastructure for backward compatibility testing.

## Details

### What's New in v3.0.0

The neural-search plugin required significant updates to maintain compatibility with OpenSearch 3.0, which introduced breaking changes from Lucene 10 and JVM 21 requirements.

### Technical Changes

#### API Compatibility Updates

The following API changes were made to align with Lucene 10 and OpenSearch 3.0:

| Change | Description |
|--------|-------------|
| `TotalHits.value` → `TotalHits.value()` | Lucene 10 changed TotalHits from public fields to accessor methods |
| `TotalHits.relation` → `TotalHits.relation()` | Same accessor method pattern for relation field |
| `BooleanClause.getQuery()` → `BooleanClause.query()` | Simplified accessor method naming |
| `Scorer(Weight)` → `Scorer()` | Scorer constructor no longer requires Weight parameter |
| `DisiWrapper(Scorer)` → `DisiWrapper(Scorer, boolean)` | Additional parameter for DisiWrapper constructor |
| `Query.rewrite(IndexReader)` → `Query.rewrite(IndexSearcher)` | Rewrite method now takes IndexSearcher |
| `org.opensearch.client.Client` → `org.opensearch.transport.client.Client` | Client class relocated to transport package |
| `ChildScorable.child` → `ChildScorable.child()` | Accessor method pattern for child scorable |
| `LeafMetaData.getSort()` → `LeafMetaData.sort()` | Simplified accessor for index sort |

#### HybridQuery Changes

The `HybridQuery` class was updated to handle boolean clauses differently:

```java
// New constructor accepting BooleanClause list directly
public HybridQuery(
    final Collection<Query> subQueries,
    final HybridQueryContext hybridQueryContext,
    final List<BooleanClause> booleanClauses
)
```

This change improves handling of wrapped queries for index aliases where core OpenSearch rewrites queries into boolean queries with modified clause structures.

#### Infrastructure Updates

| Component | Change |
|-----------|--------|
| BWC Version | Updated from 2.19.0-SNAPSHOT to 2.20.0-SNAPSHOT |
| OpenSearch Version | Updated to 3.0.0-beta1-SNAPSHOT |
| Build Qualifier | Changed from alpha1 to beta1 |
| CI Windows Precommit | Removed redundant Windows precommit job |
| BWC Tests | Removed Windows from BWC test matrix |
| Aggregation Tests | Reduced JDK matrix for Windows aggregation tests |

#### Model State Handling

Improved model loading state detection for BWC tests:

```java
private static final Set<MLModelState> READY_FOR_INFERENCE_STATES = 
    Set.of(MLModelState.LOADED, MLModelState.DEPLOYED);

protected boolean isModelReadyForInference(final MLModelState mlModelState) {
    return READY_FOR_INFERENCE_STATES.contains(mlModelState);
}
```

### Migration Notes

For plugin developers extending neural-search:

1. Update all `TotalHits` field accesses to use accessor methods
2. Update `BooleanClause` query access to use `query()` method
3. Update `Scorer` subclasses to use parameterless constructor
4. Update `Query.rewrite()` implementations to accept `IndexSearcher`
5. Update Client imports to use `org.opensearch.transport.client.Client`

## Limitations

- BWC tests are now limited to Linux platforms only
- Rolling upgrade BWC tests require 2.20.0-SNAPSHOT as the minimum version

## References

### Documentation
- [Lucene 10 Changelog](https://lucene.apache.org/core/10_0_0/changes/Changes.html): Apache Lucene 10 changes

### Blog Posts
- [OpenSearch 3.0 Blog](https://opensearch.org/blog/opensearch-3-0-what-to-expect/): New features and breaking changes

### Pull Requests
| PR | Description |
|----|-------------|
| [#1141](https://github.com/opensearch-project/neural-search/pull/1141) | Update neural-search for OpenSearch 3.0 compatibility |
| [#1245](https://github.com/opensearch-project/neural-search/pull/1245) | Update neural-search for OpenSearch 3.0 beta compatibility |
| [#502](https://github.com/opensearch-project/neural-search/pull/502) | Adding code guidelines |

### Issues (Design / RFC)
- [Issue #225](https://github.com/opensearch-project/neural-search/issues/225): Release version 3.0.0
- [Issue #3747](https://github.com/opensearch-project/opensearch-build/issues/3747): OpenSearch 3.0.0 release tracking

## Related Feature Report

- [Full feature documentation](../../../features/neural-search/neural-search-compatibility.md)
