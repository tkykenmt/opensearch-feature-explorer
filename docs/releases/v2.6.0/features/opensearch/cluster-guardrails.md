---
tags:
  - opensearch
---
# Cluster Guardrails

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to Cluster Guardrails.

## Details

### New Features

- **Add a guardrail to limit maximum number of shard on the cluster**: We have observed that as shard count on the cluster increases, it becomes more prone to instability and availability. We have observed multiple instances where user had issues in the past because of too many shards on their cluster. As of now, OpenSearch allows us to restrict the number of shards pe

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#6143](https://github.com/opensearch-project/OpenSearch/pull/6143) | Add a guardrail to limit maximum number of shard on the cluster | OpenSearch |
