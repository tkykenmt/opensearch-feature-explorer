---
tags:
  - opensearch
---
# Node Decommissioning

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to Node Decommissioning.

## Details

### New Features

- **Cluster health call to throw decommissioned exception for local decommissioned node**: This PR adds a param to cluster health local call to check if a node is decommissioned or not before retrieving its health from a local cluster state. Example Request/Response - 1. In a non decommissioned cluster ``` > curl "localhost:9200/_cluster/health?pretty&local&ensure_local_node_commissioned"

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#6008](https://github.com/opensearch-project/OpenSearch/pull/6008) | Cluster health call to throw decommissioned exception for local decommissioned node | OpenSearch |
