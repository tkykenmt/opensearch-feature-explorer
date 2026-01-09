# Replication

## Summary

This release fixes a bug in the `ResyncReplicationRequest` class where the `hashCode()` method incorrectly calculated hash codes for array fields. The fix ensures proper contract compliance between `equals()` and `hashCode()` methods, which is essential for correct behavior when these objects are used in hash-based collections.

## Details

### What's New in v2.18.0

The `ResyncReplicationRequest` class is used during primary-replica resync operations to batch translog operations from the primary shard to replica shards. The fix corrects the `hashCode()` implementation to properly handle the `operations` array field.

### Technical Changes

#### Bug Fix

The issue was in the `hashCode()` method of `ResyncReplicationRequest`:

**Before (incorrect):**
```java
@Override
public int hashCode() {
    return Objects.hash(trimAboveSeqNo, maxSeenAutoIdTimestampOnPrimary, operations);
}
```

**After (correct):**
```java
@Override
public int hashCode() {
    return Objects.hash(trimAboveSeqNo, maxSeenAutoIdTimestampOnPrimary, Arrays.hashCode(operations));
}
```

#### Problem Explanation

When passing an array directly to `Objects.hash()`, Java uses the array's identity hash code (based on memory address) rather than the content-based hash code. This violates the contract between `equals()` and `hashCode()`:

- `equals()` was correctly using `Arrays.equals(operations, that.operations)` to compare array contents
- `hashCode()` was incorrectly using the array's identity hash code

This mismatch means two `ResyncReplicationRequest` objects with identical content could have different hash codes, causing issues when used in hash-based collections like `HashMap` or `HashSet`.

#### Components Affected

| Component | Description |
|-----------|-------------|
| `ResyncReplicationRequest` | Request class for primary-replica resync operations |

### Usage Example

The fix ensures correct behavior in scenarios like:

```java
// Two requests with identical content
ResyncReplicationRequest request1 = new ResyncReplicationRequest(shardId, 42L, 100, operations);
ResyncReplicationRequest request2 = new ResyncReplicationRequest(shardId, 42L, 100, operations);

// Contract: if equals() returns true, hashCode() must return same value
assert request1.equals(request2);
assert request1.hashCode() == request2.hashCode(); // Now works correctly
```

## Limitations

- This is an internal bug fix with no user-facing API changes
- No migration steps required

## Related PRs

| PR | Description |
|----|-------------|
| [#16378](https://github.com/opensearch-project/OpenSearch/pull/16378) | Fix array hashCode calculation in ResyncReplicationRequest |
| [#15383](https://github.com/opensearch-project/OpenSearch/pull/15383) | Previous attempt (closed without merge) |

## References

- [Segment replication documentation](https://docs.opensearch.org/2.18/tuning-your-cluster/availability-and-recovery/segment-replication/index/): Related replication concepts

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/replication.md)
