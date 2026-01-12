# Search Stats - Negative Value Handling

## Summary

This release fixes a critical bug where negative search statistics values caused exceptions when accessing the `/_nodes/stats` API. The fix ensures that negative `current` values in search request phase statistics are handled gracefully by writing `0` instead, preventing serialization failures.

## Details

### What's New in v3.3.0

This release addresses a bug where search statistics could become negative due to race conditions in phase tracking, causing the nodes stats API to fail with `IllegalStateException`.

### Technical Changes

#### Bug Description

The issue occurred in the `SearchStats.PhaseStatsLongHolder` class when serializing statistics:

1. The `current` counter tracks active search phases
2. Due to multiple exit paths from a phase, the counter could be decremented more than once
3. When `current` became negative, `StreamOutput.writeVLong()` threw an exception because VLong encoding doesn't support negative values

#### Error Example

```
java.lang.IllegalStateException: Negative longs unsupported, use writeLong or writeZLong for negative numbers [-3]
    at org.opensearch.common.io.stream.StreamOutput.writeVLong(StreamOutput.java:307)
    at org.opensearch.index.search.stats.SearchStats$PhaseStatsLongHolder.writeTo(SearchStats.java:88)
```

#### Solution

The fix adds defensive checks in the `writeTo()` method:

```java
@Override
public void writeTo(StreamOutput out) throws IOException {
    if (current < 0) {
        out.writeVLong(0);
    } else {
        out.writeVLong(current);
    }
    out.writeVLong(total);
    out.writeVLong(timeInMillis);
}
```

Additionally, warning logs are emitted when negative values are detected:

```java
requestStatsLongHolder.requestStatsHolder.forEach((phaseName, phaseStats) -> {
    if (phaseStats.current < 0) {
        PhaseStatsLongHolder.logger.warn(
            "SearchRequestStats 'current' is negative for phase '{}': {}",
            phaseName,
            phaseStats.current
        );
    }
});
```

#### Why Not Use ZLong?

The PR author considered using `ZLong` (which supports negative values) but rejected it due to potential serialization compatibility issues between different OpenSearch versions during rolling upgrades.

### Migration Notes

No migration required. The fix is backward compatible and automatically handles negative values.

## Limitations

- The fix treats the symptom (negative values) rather than the root cause (race condition in phase tracking)
- Negative values are logged as warnings for monitoring but the underlying race condition may still occur

## References

### Documentation
- [Nodes Stats API Documentation](https://docs.opensearch.org/3.0/api-reference/nodes-apis/nodes-stats/): Official API documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#19340](https://github.com/opensearch-project/OpenSearch/pull/19340) | Handle negative search request nodes stats |

### Issues (Design / RFC)
- [Issue #16598](https://github.com/opensearch-project/OpenSearch/issues/16598): Bug report - Negative Search Stats causing nodes/stats API failures

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/search-request-stats.md)
