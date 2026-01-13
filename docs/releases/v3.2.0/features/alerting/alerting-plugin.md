---
tags:
  - domain/observability
  - component/server
  - indexing
  - observability
  - search
---
# Alerting Plugin

## Summary

This release includes three bug fixes for the Alerting plugin: a fix for the MGet operation with randomized fan-out distribution, improved API responses when the alerting config index doesn't exist, and updated Maven snapshot publishing infrastructure.

## Details

### What's New in v3.2.0

Three bug fixes improve the reliability and user experience of the Alerting plugin:

1. **MGet Bug Fix & Fan-out Randomization**: Fixes a bug in the `getDocSources` method and refactors fan-out distribution to randomize node selection across monitor runs
2. **Consistent API Responses**: Returns meaningful error messages or empty responses when the alerting config index doesn't exist
3. **Maven Snapshot Publishing**: Updates the Maven snapshot publish endpoint and credentials following Sonatype migration

### Technical Changes

#### MGet Bug Fix & Fan-out Distribution (PR #1885)

The `getDocSources` method had a bug where the `findingId` to document mapping was incorrect during batch MGet operations. The fix:

- Moves the MGet request creation inside the batch loop
- Creates a proper `docIdToFindingId` mapping to correctly associate documents with findings
- Adds logging for MGet operation duration

Additionally, the fan-out distribution logic was refactored:

- Extracted to a new `MonitorFanOutUtils.kt` utility file
- Randomizes node selection using `shuffled()` to distribute load evenly across runs
- Simplified shard distribution algorithm using round-robin assignment

```kotlin
// New randomized node selection
val shuffledNodes = allNodes.shuffled()
val nodes = shuffledNodes.subList(0, totalNodes)

// Round-robin shard assignment
shardIdList.forEachIndexed { idx, shardId ->
    val nodeIdx = idx % nodes.size
    nodeShardAssignments[nodes[nodeIdx]]!!.add(shardId)
}
```

#### Consistent API Responses (PR #1818)

When no monitors exist, the alerting config index (`.opendistro-alerting-config`) is not created. Previously, GET and SEARCH API calls would return confusing `IndexNotFoundException` errors.

**Before:**
```json
{
  "error": {
    "type": "alerting_exception",
    "reason": "Configured indices are not found: [.opendistro-alerting-config]"
  },
  "status": 404
}
```

**After (GET):**
```json
{
  "error": {
    "type": "alerting_exception",
    "reason": "Monitor not found. Backing index is missing."
  },
  "status": 404
}
```

**After (SEARCH):**
```json
{
  "hits": {
    "total": { "value": 0, "relation": "eq" },
    "hits": []
  }
}
```

#### Maven Snapshot Publishing (PR #1869)

Updates the Maven snapshot publishing infrastructure following Sonatype migration:

- Changed snapshot URL from `https://aws.oss.sonatype.org/content/repositories/snapshots` to `https://central.sonatype.com/repository/maven-snapshots/`
- Migrated from AWS Secrets Manager to 1Password for credential management
- Updated GitHub Actions workflow to use `1password/load-secrets-action@v2`

### Usage Example

The API behavior changes are transparent to users. The improved error messages help diagnose issues:

```bash
# GET request when no monitors exist
GET _plugins/_alerting/monitors/nonexistent-id
# Returns: "Monitor not found. Backing index is missing." (404)

# SEARCH request when no monitors exist
GET _plugins/_alerting/monitors/_search
{
  "query": { "match_all": {} }
}
# Returns: Empty search response with 0 hits (200)
```

## Limitations

- The fan-out randomization may result in different nodes being selected on each monitor run, which could affect debugging if issues are node-specific
- The empty response behavior for SEARCH only applies when the index doesn't exist; other errors are still propagated

## References

### Documentation
- [Alerting Documentation](https://docs.opensearch.org/3.0/observing-your-data/alerting/index/): Official alerting documentation
- [Monitors Documentation](https://docs.opensearch.org/3.0/observing-your-data/alerting/monitors/): Monitor types and configuration

### Pull Requests
| PR | Description |
|----|-------------|
| [#1885](https://github.com/opensearch-project/alerting/pull/1885) | Fix MGet bug, randomize fan out distribution |
| [#1818](https://github.com/opensearch-project/alerting/pull/1818) | Refactored consistent responses and fixed unrelated exceptions |
| [#1869](https://github.com/opensearch-project/alerting/pull/1869) | Update the maven snapshot publish endpoint and credential |

### Issues (Design / RFC)
- [Issue #1057](https://github.com/opensearch-project/alerting/issues/1057): Return empty responses if there is no alerting config index created
- [Issue #5551](https://github.com/opensearch-project/opensearch-build/issues/5551): Sonatype migration campaign

## Related Feature Report

- [Full feature documentation](../../../../features/alerting/alerting.md)
