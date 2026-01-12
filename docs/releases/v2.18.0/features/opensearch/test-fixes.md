# Test Fixes

## Summary

This release item fixes a flaky test in `ApproximatePointRangeQueryTests.testApproximateRangeWithSizeOverDefault` that was causing intermittent CI failures. The fix adjusts the totalHits assertion logic to properly handle Lucene's behavior when returning hit counts beyond the default threshold.

## Details

### What's New in v2.18.0

The `testApproximateRangeWithSizeOverDefault` test was failing intermittently due to how Lucene's `IndexSearcher` handles total hit counts. By default, Lucene provides an accurate count for up to 1000 hits. Beyond this threshold, Lucene may return a lower bound using `GREATER_THAN_OR_EQUAL_TO` for performance optimization.

### Technical Changes

#### Root Cause

The test searches for documents in a range that includes 12,001 documents with a requested size of 11,000. When Lucene's `search()` method returns results:
- Sometimes it returns `TotalHits.Relation.EQUAL_TO` with an exact count
- Sometimes it returns `TotalHits.Relation.GREATER_THAN_OR_EQUAL_TO` with a lower bound estimate

The original test only checked for exact equality, causing failures when Lucene used the lower bound relation.

#### Fix Implementation

The fix modifies the assertion logic to handle both cases:

```java
if (topDocs.totalHits.relation == Relation.EQUAL_TO) {
    assertEquals(topDocs.totalHits.value, 11000);
} else {
    assertTrue(11000 <= topDocs.totalHits.value);
    assertTrue(maxHits >= topDocs.totalHits.value);
}
```

This approach:
- Checks for exact count (11000) when relation is `EQUAL_TO`
- Validates the count is within expected bounds (11000 to 12001) when relation is `GREATER_THAN_OR_EQUAL_TO`

#### Code Cleanup

The PR also includes minor code cleanup:
- Removed redundant semicolons
- Removed unnecessary blank lines
- Added import for `TotalHits.Relation`

### Usage Example

No user-facing changes. This is an internal test fix.

## Limitations

- This fix addresses only the `testApproximateRangeWithSizeOverDefault` test
- Other flaky tests in `ApproximatePointRangeQueryTests` may require similar fixes

## References

### Documentation
- [Lucene IndexSearcher Documentation](https://lucene.apache.org/core/9_11_0/core/org/apache/lucene/search/IndexSearcher.html): Explains totalHits behavior
- [PR #4270](https://github.com/opensearch-project/OpenSearch/pull/4270): Similar fix for related flaky test issue

### Pull Requests
| PR | Description |
|----|-------------|
| [#16434](https://github.com/opensearch-project/OpenSearch/pull/16434) | Fix flaky test by adjusting totalHits assertion logic |

### Issues (Design / RFC)
- [Issue #15807](https://github.com/opensearch-project/OpenSearch/issues/15807): AUTOCUT Gradle Check Flaky Test Report for ApproximatePointRangeQueryTests

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/test-fixes.md)
