---
tags:
  - opensearch
---
# Weighted Shard Routing

## Summary

OpenSearch 2.6.0 introduces 2 new feature(s) and 0 enhancement(s) to Weighted Shard Routing.

## Details

### New Features

- **Add support to disallow search request with preference parameter with strict weighted shard routing**: Disallow search requests with preference parameter in case of strict weighted routing
- **Fix weighted shard routing state across search requests**: This PR fixes issue due to which state is not maintained across weighted shard routing search requests . The shuffler is moved twice in a call which is causing the issue. The PR adds code logic to prevent unwanted shuffler movement.

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#5874](https://github.com/opensearch-project/OpenSearch/pull/5874) | Add support to disallow search request with preference parameter with strict weighted shard routing | OpenSearch |
| [#6004](https://github.com/opensearch-project/OpenSearch/pull/6004) | Fix weighted shard routing state across search requests | OpenSearch |
