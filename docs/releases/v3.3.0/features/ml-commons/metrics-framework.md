---
tags:
  - ml
  - observability
---

# Metrics Framework Bug Fix

## Summary

This release fixes a critical bug in the ML Commons Metrics Framework where the version checking logic for starting the stats collector job was inverted. The bug prevented the stats collector job from starting on nodes running OpenSearch versions newer than 3.1.0.

## Details

### What's New in v3.3.0

Fixed the version comparison logic in `MLCommonsClusterEventListener` that determines whether to start the stats collector job when a data node joins the cluster.

### Technical Changes

#### Bug Description

The original code incorrectly checked:
```java
Version.V_3_1_0.onOrAfter(node.getVersion())
```

This condition evaluated to `true` only when the node version was 3.1.0 or **older**, which is the opposite of the intended behavior.

#### Fix Applied

The corrected code now properly checks:
```java
node.getVersion().onOrAfter(Version.V_3_1_0)
```

This ensures the stats collector job starts for nodes running version 3.1.0 or **newer**.

#### Impact

| Scenario | Before Fix | After Fix |
|----------|------------|-----------|
| Node v3.0.0 joins | Stats collector started ❌ | Stats collector NOT started ✓ |
| Node v3.1.0 joins | Stats collector started ✓ | Stats collector started ✓ |
| Node v3.2.0+ joins | Stats collector NOT started ❌ | Stats collector started ✓ |

### Code Change

```java
// File: MLCommonsClusterEventListener.java
// Before:
if (node.isDataNode() && Version.V_3_1_0.onOrAfter(node.getVersion())) {

// After:
if (node.isDataNode() && node.getVersion().onOrAfter(Version.V_3_1_0)) {
```

### Test Coverage

New test cases were added to `MLCommonsClusterEventListenerTests.java` to verify:
- Stats collector starts for v3.1.0 data nodes
- Stats collector starts for v3.2.0+ data nodes
- Stats collector does NOT start for pre-v3.1.0 data nodes

## Limitations

- This fix is backported to 3.1 and 3.2 branches
- Clusters that were affected by this bug may need to restart nodes to trigger the stats collector job

## References

### Documentation
- [Metrics Framework Documentation](https://docs.opensearch.org/3.0/monitoring-your-cluster/metrics/getting-started/)
- [ML Commons Cluster Settings](https://docs.opensearch.org/3.0/ml-commons-plugin/cluster-settings/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#4220](https://github.com/opensearch-project/ml-commons/pull/4220) | Fix version checking logic for starting the stats collector job |

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/metrics-framework.md)
