# Index Management Bugfixes

## Summary

OpenSearch v3.4.0 includes four bug fixes for the Index Management plugin addressing issues in ISM policy rebinding, Snapshot Management deletion workflow, SM Explain API serialization, and rollup test stability.

## Details

### What's New in v3.4.0

This release fixes critical bugs affecting ISM policy management, Snapshot Management operations, and test reliability.

### Technical Changes

#### ISM Policy Rebinding After Removal (PR #1525)

**Problem**: After removing an ISM policy from an index using `POST _plugins/_ism/remove/{index}`, the coordinator sweep would incorrectly rebind the policy to the index.

**Root Cause**: The `ManagedIndexCoordinator.kt` had flawed logic when checking the `auto_manage` setting:
- When `index.plugins.index_state_management.auto_manage` was set to `false`, the code incorrectly fell through to check the legacy setting
- The legacy setting `index.opendistro.index_state_management.auto_manage` defaulted to `true`, causing the index to be picked up again

**Fix**: Changed the logic to first check if the new setting key exists (even if blank), and only fall back to the legacy setting when the new setting is not explicitly set.

```kotlin
// Before (incorrect)
if (AUTO_MANAGE.get(indexMetadata.settings)) {
    true
} else {
    LegacyOpenDistroManagedIndexSettings.AUTO_MANAGE.get(indexMetadata.settings)
}

// After (correct)
if (indexMetadata.settings.get(AUTO_MANAGE.key).isNullOrBlank()) {
    LegacyOpenDistroManagedIndexSettings.AUTO_MANAGE.get(indexMetadata.settings)
} else {
    AUTO_MANAGE.get(indexMetadata.settings)
}
```

#### Snapshot Pattern Parsing in SM Deletion (PR #1503)

**Problem**: Snapshot Management deletion-only policies with `snapshot_pattern` failed to find matching snapshots, throwing `SnapshotMissingException` even when snapshots existed.

**Root Cause**: Comma-separated snapshot patterns (e.g., `"policy-name*,snp*"`) were passed as a single string to `GetSnapshotsRequest.snapshots()`, causing the API to search for a literal snapshot name instead of matching multiple patterns.

**Fix**: Split comma-separated patterns into separate array elements before passing to the API.

```kotlin
// Before
.snapshots(arrayOf(name))  // Single element: ["policy-name*,snp*"]

// After
val patterns = name.split(",").map { it.trim() }.toTypedArray()
.snapshots(patterns)  // Multiple elements: ["policy-name*", "snp*"]
```

#### ExplainSMPolicy Serialization (PR #1507)

**Problem**: The `ExplainSMPolicy.toXContent()` method used `.field()` for the nullable `creation` field instead of `.optionalField()`, causing incorrect serialization when creation workflow metadata was null.

**Fix**: Use `.optionalField()` for the `creation` field with version-aware handling for backward compatibility.

```kotlin
if (Version.CURRENT.onOrAfter(Version.V_3_3_0)) {
    builder.optionalField(SMMetadata.CREATION_FIELD, it.creation)
} else {
    builder.field(SMMetadata.CREATION_FIELD, it.creation)
}
```

#### Rollup Start/Stop Test Race Condition (PR #1529)

**Problem**: Rollup start/stop tests with multiple shards experienced intermittent failures due to version conflicts (HTTP 409).

**Root Cause**: Race condition between test operations and active rollup runner:
1. Test reads rollup document (seqNo = N)
2. Active rollup runner updates the document (seqNo = N+1)
3. Test tries to update with seqNo = N → 409 Version Conflict

**Fix**: Move `_stop` and `_start` API calls inside the `waitFor` block to enable automatic retries on version conflicts.

### Files Changed

| File | Change |
|------|--------|
| `ManagedIndexCoordinator.kt` | Fix auto_manage setting check logic |
| `SMUtils.kt` | Split comma-separated snapshot patterns |
| `ExplainSMPolicy.kt` | Use optionalField for nullable creation |
| `RestStartRollupActionIT.kt` | Move _start call inside waitFor block |
| `RestStopRollupActionIT.kt` | Move _stop call inside waitFor block |

## Limitations

- The ISM policy rebinding fix only affects new policy removals; existing affected indexes may need manual intervention
- The snapshot pattern fix requires SM policies to be re-evaluated on next scheduled run

## References

### Documentation
- [Snapshot Management Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-management/)
- [Index State Management Documentation](https://docs.opensearch.org/3.0/im-plugin/ism/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1525](https://github.com/opensearch-project/index-management/pull/1525) | Fix ISM policy rebinding after removal |
| [#1503](https://github.com/opensearch-project/index-management/pull/1503) | Fix snapshot pattern parsing in SM deletion |
| [#1507](https://github.com/opensearch-project/index-management/pull/1507) | Fix ExplainSMPolicy serialization for null creation |
| [#1529](https://github.com/opensearch-project/index-management/pull/1529) | Fix race condition in rollup start/stop tests |

### Issues (Design / RFC)
- [Issue #1524](https://github.com/opensearch-project/index-management/issues/1524): ISM policy rebinding bug report
- [Issue #1502](https://github.com/opensearch-project/index-management/issues/1502): SM deletion snapshot pattern bug report
- [Issue #1506](https://github.com/opensearch-project/index-management/issues/1506): ExplainSMPolicy serialization bug report
- [Issue #90](https://github.com/opensearch-project/index-management/issues/90): Flaky tests tracking issue

## Related Feature Report

- [Full feature documentation](../../../features/index-management/index-management.md)
