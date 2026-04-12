---
tags:
  - opensearch
---
# Index Create Block

## Summary

OpenSearch 2.6.0 introduces 3 new feature(s) and 0 enhancement(s) to Index Create Block.

## Details

### New Features

- **Add index create block when all nodes have breached high disk watermark**: OpenSearch stops allocating any shards to nodes that have breached High Disk Watermark. If a scenario arises that all the nodes in the cluster breached high disk watermark, no new shards will be created on this cluster. Now if we try to create a new index on this cluster, it will be a red index (sin
- **Add support to apply index create block**: Added in PR #4603.
- **Add a setting to control auto release of OpenSearch managed index creation block**: OpenSearch controls (applies and remove)```create_index``` block (when all node are breaching high disk watermark) inside ```DiskThresholdMonitor```. Now, if the user tries to apply this block from their end, it may be possible that ```DiskThresholdMonitor``` removes it (```create_index``` gets remo

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#5852](https://github.com/opensearch-project/OpenSearch/pull/5852) | Add index create block when all nodes have breached high disk watermark | OpenSearch |
| [#4603](https://github.com/opensearch-project/OpenSearch/pull/4603) | Add support to apply index create block | OpenSearch |
| [#6277](https://github.com/opensearch-project/OpenSearch/pull/6277) | Add a setting to control auto release of OpenSearch managed index creation block | OpenSearch |
