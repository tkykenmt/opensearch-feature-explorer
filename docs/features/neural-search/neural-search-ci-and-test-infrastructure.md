---
tags:
  - neural-search
---
# Neural Search CI & Test Infrastructure

## Summary

CI and test infrastructure for the Neural Search plugin, covering integration test setup, cluster health checks, and test environment configuration in `BaseNeuralSearchIT`.

## Details

### Integration Test Base Class

`BaseNeuralSearchIT` extends `OpenSearchSecureRestTestCase` and provides shared setup for all neural-search integration tests, including cluster node discovery and health checks.

### Dynamic Node Count Discovery

The test base class dynamically determines the cluster node count at runtime by querying the `_cluster/health` API:

```java
protected int getClusterNodeCount() throws IOException, ParseException {
    Request request = new Request("GET", "/_cluster/health");
    Response response = client().performRequest(request);
    String responseBody = EntityUtils.toString(response.getEntity());
    Map<String, Object> health = createParser(
        XContentType.JSON.xContent(), responseBody
    ).map();
    return ((Number) health.get("number_of_nodes")).intValue();
}
```

This replaces a previous approach that relied on the `cluster.number_of_nodes` system property, which failed in remote cluster environments.

### Cluster Health Check

The `waitForClusterHealthGreen()` method uses `>=` syntax for `wait_for_nodes` to tolerate clusters with more nodes than expected:

```java
waitForGreen.addParameter("wait_for_nodes", ">=" + numOfNodes);
waitForGreen.addParameter("wait_for_status", "green");
waitForGreen.addParameter("wait_for_active_shards", "all");
```

## Limitations

- If the cluster is unreachable during test setup, the test fails immediately with no fallback

## Change History

- **v3.6.0**: Fixed integration test health check failures in remote clusters by dynamically discovering node count via `_cluster/health` API and using `>=` syntax for `wait_for_nodes`

## References

### Pull Requests

| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.6.0 | [#1776](https://github.com/opensearch-project/neural-search/pull/1776) | Fixed integ tests to read num of nodes dynamically | [#1774](https://github.com/opensearch-project/neural-search/issues/1774) |
