---
tags:
  - domain/core
  - component/server
  - security
---
# Node Stats Bugfixes

## Summary

This release fixes a bug where the `_cat/nodes` and `_nodes/stats` APIs reported negative CPU usage values (-1) on certain Linux distributions. The issue occurred because OpenSearch lacked file permissions to read CPU-related cgroup paths on systems using the combined `cpu,cpuacct` cgroup controller.

## Details

### What's New in v3.4.0

The fix adds read permissions for additional cgroup paths in OpenSearch's security policy, enabling proper CPU statistics collection on Linux distributions that use combined cgroup controllers.

### Technical Changes

#### Root Cause

On certain Linux distributions (particularly RHEL 8.x and similar), the cgroup filesystem uses a combined `cpu,cpuacct` controller path instead of separate `cpu` and `cpuacct` paths. OpenSearch's security policy only granted read permissions for the separate paths, causing CPU stat collection to fail silently and return -1.

#### Security Policy Changes

| Path | Permission | Purpose |
|------|------------|---------|
| `/sys/fs/cgroup/cpu,cpuacct` | read | Combined CPU accounting cgroup directory |
| `/sys/fs/cgroup/cpu,cpuacct/-` | read | Files within combined cgroup |
| `/sys/fs/cgroup/cpuset/-` | read | CPU set files |

#### Affected APIs

- `GET /_cat/nodes` - CPU column showed -1
- `GET /_nodes/stats` - `os.cpu.percent` returned -1
- `GET /_cluster/stats` - CPU statistics were incorrect

### Usage Example

After the fix, CPU statistics are correctly reported:

```bash
# Before fix (on affected systems)
$ curl "/_cat/nodes?v&h=name,cpu"
name                              cpu
opensearch-node-1                 -1
opensearch-node-2                 -1

# After fix
$ curl "/_cat/nodes?v&h=name,cpu"
name                              cpu
opensearch-node-1                 12
opensearch-node-2                 8
```

### Migration Notes

No migration required. The fix is automatically applied when upgrading to v3.4.0.

## Limitations

- This fix specifically addresses Linux systems using cgroups v1 with combined controllers
- Systems using cgroups v2 may have different path structures

## References

### Documentation
- [Nodes Stats API Documentation](https://docs.opensearch.org/3.0/api-reference/nodes-apis/nodes-stats/): Official API documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#20108](https://github.com/opensearch-project/OpenSearch/pull/20108) | Add file permissions for 'cpu,cpuacct' cgroup |

### Issues (Design / RFC)
- [Issue #19120](https://github.com/opensearch-project/OpenSearch/issues/19120): Original bug report for negative CPU usage values

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-node-stats.md)
