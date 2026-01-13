---
tags:
  - domain/data
  - component/server
  - indexing
  - ml
  - security
---
# Index Management Bugfixes

## Summary

OpenSearch v3.0.0 includes several bugfixes and improvements for the Index Management plugin, including a new ISM unfollow action for cross-cluster replication, rollup target index settings support, security vulnerability fixes, and build system updates for Java Agent migration.

## Details

### What's New in v3.0.0

#### ISM Unfollow Action for Cross-Cluster Replication

A new `unfollow` action has been added to Index State Management (ISM) policies. This action invokes the stop-replication utility from common-utils to stop cross-cluster replication on follower indexes.

**Use Case**: When managing follower indexes in a cross-cluster replication setup, you can now automate the process of stopping replication as part of your ISM policy lifecycle.

```json
{
  "policy": {
    "states": [
      {
        "name": "stop_replication",
        "actions": [
          {
            "unfollow": {}
          }
        ]
      }
    ]
  }
}
```

#### Rollup Target Index Settings

The rollup job now supports an optional `target_index_settings` field, allowing users to specify custom index settings when creating the target rollup index.

```json
PUT _plugins/_rollup/jobs/my_rollup_job
{
  "rollup": {
    "source_index": "my_source_index",
    "target_index": "my_rollup_index",
    "target_index_settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    },
    ...
  }
}
```

### Security Fixes

#### CVE Fix: logback-core Upgrade

Upgraded logback-core to version 1.5.13 to address:
- QOS.CH logback-core Expression Language Injection vulnerability
- Potential Arbitrary Code Execution (ACE) vulnerability through compromised logback configuration files or environment variables

### Build System Updates

#### Java Agent Migration

Fixed build issues related to the deprecation of SecurityManager in favor of Java Agent. This aligns with OpenSearch 3.0's migration to JDK 21 and the broader Java ecosystem's move away from SecurityManager.

#### CI/CD Updates

- Updated codecov/codecov-action from v1 to v5 for improved code coverage reporting

## Limitations

- The `unfollow` action requires the cross-cluster-replication plugin to be installed
- Target index settings for rollup only apply when creating a new target index

## References

### Documentation
- [Index State Management Documentation](https://docs.opensearch.org/3.0/im-plugin/ism/index/)
- [Index Rollups Documentation](https://docs.opensearch.org/3.0/im-plugin/index-rollups/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1198](https://github.com/opensearch-project/index-management/pull/1198) | Adding unfollow action in ISM to invoke stop replication for CCR |
| [#1377](https://github.com/opensearch-project/index-management/pull/1377) | Target Index Settings if create index during rollup |
| [#1388](https://github.com/opensearch-project/index-management/pull/1388) | Fixed CVE upgrade logback-core to 1.5.13 |
| [#1404](https://github.com/opensearch-project/index-management/pull/1404) | Fix build due to phasing off SecurityManager usage in favor of Java Agent |
| [#1308](https://github.com/opensearch-project/index-management/pull/1308) | Bump codecov/codecov-action from 1 to 5 |

### Issues (Design / RFC)
- [Issue #726](https://github.com/opensearch-project/index-management/issues/726): Original feature request for unfollow action
- [Issue #1376](https://github.com/opensearch-project/index-management/issues/1376): Target index settings feature request

## Related Feature Report

- [Full feature documentation](../../../features/index-management/index-management.md)
