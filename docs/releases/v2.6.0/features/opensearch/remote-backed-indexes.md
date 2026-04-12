---
tags:
  - opensearch
---
# Remote-Backed Indexes

## Summary

OpenSearch 2.6.0 introduces 2 new feature(s) and 0 enhancement(s) to Remote-Backed Indexes.

## Details

### New Features

- **Handle translog upload during primary relocation for remote-backed indexes**: Solves #5795 & #5844.
- **Batch translog sync/upload per x ms for remote-backed indexes**: Translog sync takes care of local fsync and translog upload onto remote store. Currently, there is implicit buffering that happens as the remote store upload is a time consuming operation. However, every upload adds extra cost of network interaction along with the actual file upload. If we can buffe

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#5804](https://github.com/opensearch-project/OpenSearch/pull/5804) | Handle translog upload during primary relocation for remote-backed indexes | OpenSearch |
| [#5854](https://github.com/opensearch-project/OpenSearch/pull/5854) | Batch translog sync/upload per x ms for remote-backed indexes | OpenSearch |
