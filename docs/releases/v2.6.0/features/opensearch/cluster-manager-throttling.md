---
tags:
  - opensearch
---
# Cluster Manager Throttling

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to Cluster Manager Throttling.

## Details

### New Features

- **Add cluster manager throttling stats in nodes/stats API**: Add throttling stats in _nodes/stats API. In Active master node's stats these stats will appear, for other nodes it will be 0. From active master node's stats we can get visibility on how many tasks are getting throttled. Below is sample stats for two node cluster. ``` curl "localhost:9200/_nodes/st

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#5790](https://github.com/opensearch-project/OpenSearch/pull/5790) | Add cluster manager throttling stats in nodes/stats API | OpenSearch |
