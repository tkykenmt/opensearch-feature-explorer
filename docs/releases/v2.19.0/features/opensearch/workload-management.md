---
tags:
  - opensearch
---
# Workload Management

## Summary

This release adds Integration Tests for Workload Management (WLM), providing comprehensive test coverage for the WLM feature's core functionality including query group resource enforcement, task cancellation, and resiliency modes.

## Details

### What's New in v2.19.0

This release introduces a new integration test suite (`WorkloadManagementIT`) that validates the end-to-end behavior of Workload Management. The tests cover:

- **High CPU enforcement**: Verifies that tasks are canceled when CPU limits are exceeded in enforced mode
- **High memory enforcement**: Verifies that tasks are canceled when memory limits are exceeded in enforced mode
- **Monitor-only mode**: Confirms that tasks are not canceled when WLM is in monitor-only mode
- **No cancellation scenarios**: Validates that tasks within resource limits complete successfully

### Technical Changes

The PR adds the following test infrastructure:

| Component | Description |
|-----------|-------------|
| `WorkloadManagementIT` | Main integration test class with parameterized tests for concurrent segment search |
| `TestClusterUpdatePlugin` | Plugin for testing cluster state updates with query groups |
| `TestClusterUpdateTransportAction` | Transport action for creating/deleting query groups in tests |
| `TestQueryGroupTaskTransportAction` | Transport action for executing test tasks with query group assignment |
| `TestQueryGroupTaskRequest` | Request class for test tasks with resource type and query group ID |

The tests also expose helper classes from `SearchBackpressureIT`:
- `ExceptionCatchingListener` - Made public for reuse
- `TaskFactory` interface - Made public for reuse

### Test Scenarios

| Test | Mode | Resource | Expected Behavior |
|------|------|----------|-------------------|
| `testHighCPUInEnforcedMode` | enabled | CPU | Task canceled with `TaskCancelledException` |
| `testHighCPUInMonitorMode` | monitor_only | CPU | Task completes without cancellation |
| `testHighMemoryInEnforcedMode` | enabled | Memory | Task canceled with `TaskCancelledException` |
| `testHighMemoryInMonitorMode` | monitor_only | Memory | Task completes without cancellation |
| `testNoCancellation` | enabled | CPU/Memory | Task completes when within limits (80%) |

### Running the Tests

```bash
./gradlew :server:internalClusterTest --tests org.opensearch.wlm.WorkloadManagementIT
```

## Limitations

- Tests require the workload-management plugin to be installed
- Tests use low resource thresholds (1%) to trigger cancellation quickly
- Tests are parameterized for both concurrent and non-concurrent segment search modes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16359](https://github.com/opensearch-project/OpenSearch/pull/16359) | Add Workload Management IT | [#12342](https://github.com/opensearch-project/OpenSearch/issues/12342) |

### Documentation
- [Workload Management Documentation](https://docs.opensearch.org/2.19/tuning-your-cluster/availability-and-recovery/workload-management/wlm-feature-overview/)
- [RFC #12342](https://github.com/opensearch-project/OpenSearch/issues/12342): Search Query Sandboxing: User Experience
