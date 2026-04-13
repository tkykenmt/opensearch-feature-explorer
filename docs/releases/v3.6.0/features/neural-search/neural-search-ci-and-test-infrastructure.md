---
tags:
  - neural-search
---
# Neural Search CI & Test Infrastructure

## Summary

Fixed integration test health check failures in remote clusters by replacing the hardcoded node count system property with dynamic discovery via the `_cluster/health` API, and using `>=` syntax for `wait_for_nodes` to tolerate clusters with more nodes than expected.

## Details

### What's New in v3.6.0

#### Dynamic Node Count Discovery

Previously, `BaseNeuralSearchIT` obtained the cluster node count from a system property (`cluster.number_of_nodes`) with a default of `"1"`. This worked for local test clusters but failed when running integration tests against remote clusters where the property was not set correctly.

The fix replaces the static system property with a runtime `_cluster/health` API call:

```java
// Before (static)
numOfNodes = System.getProperty("cluster.number_of_nodes", "1");

// After (dynamic)
numOfNodes = String.valueOf(getClusterNodeCount());
```

The new `getClusterNodeCount()` method queries `GET /_cluster/health` and reads the `number_of_nodes` field from the response.

#### Tolerant Health Check Syntax

The `waitForClusterHealthGreen()` method now uses `>=` prefix for the `wait_for_nodes` parameter instead of an exact match:

```java
// Before
waitForGreen.addParameter("wait_for_nodes", numOfNodes);

// After
waitForGreen.addParameter("wait_for_nodes", ">=" + numOfNodes);
```

This prevents timeout failures when the actual cluster has more nodes than expected.

### Technical Changes

| Change | File | Description |
|--------|------|-------------|
| Dynamic node count | `BaseNeuralSearchIT.java` | Replace `System.getProperty()` with `_cluster/health` API call |
| New method | `BaseNeuralSearchIT.java` | Add `getClusterNodeCount()` method |
| Health check syntax | `BaseNeuralSearchIT.java` | Use `>=` prefix in `wait_for_nodes` parameter |

## Limitations

- If the cluster is unreachable during test setup, the test fails immediately rather than falling back to a default value

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1776](https://github.com/opensearch-project/neural-search/pull/1776) | Fixed integ tests to read num of nodes dynamically | [#1774](https://github.com/opensearch-project/neural-search/issues/1774) |
