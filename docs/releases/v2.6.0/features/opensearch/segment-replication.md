---
tags:
  - opensearch
---
# Segment Replication

## Summary

OpenSearch 2.6.0 introduces 4 new feature(s) and 0 enhancement(s) to Segment Replication.

## Details

### New Features

- **Add new cat/segment_replication API to surface Segment Replication metrics .**: This PR implements segment_replication API to fetch each segment replication event stats. This PR implements first two points in [comment](https://github.com/opensearch-project/OpenSearch/issues/4554#issuecomment-1315735767). -> This API is built by taking reference of `_cat/recovery` API as many co
- **Use ReplicationFailedException instead of OpensearchException in ReplicationTarget**: Uses a narrower ReplicationFailedException instead of OpensearchException in ReplicationTarget and ReplicationListener
- **[Segment Replication] Fix for peer recovery**: Update the peer recovery logic to work with segment replication. The existing primary relocation is broken because of segment files conflicts. This happens because of target (new primary) is started with InternalEngine writes its own version of segment files which later on conflicts with file copies
- **[Segment Replication] Fix bug where inaccurate sequence numbers are sent during replication**: Added in PR #6122.

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#5718](https://github.com/opensearch-project/OpenSearch/pull/5718) | Add new cat/segment_replication API to surface Segment Replication metrics . | OpenSearch |
| [#4725](https://github.com/opensearch-project/OpenSearch/pull/4725) | Use ReplicationFailedException instead of OpensearchException in ReplicationTarget | OpenSearch |
| [#5344](https://github.com/opensearch-project/OpenSearch/pull/5344) | [Segment Replication] Fix for peer recovery | OpenSearch |
| [#6122](https://github.com/opensearch-project/OpenSearch/pull/6122) | [Segment Replication] Fix bug where inaccurate sequence numbers are sent during replication | OpenSearch |
