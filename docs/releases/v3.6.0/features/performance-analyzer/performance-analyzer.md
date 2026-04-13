---
tags:
  - performance-analyzer
---
# Performance Analyzer

## Summary

In v3.6.0, Performance Analyzer received a significant new feature — a shard operations collector that tracks per-shard indexing and search rates, latency, CPU utilization, and heap usage — along with optimizations to the node stats collector and two build/dependency fixes (CVE-2025-68161 log4j resolution and disabling the `dependencyLicenses` check).

## Details

### What's New in v3.6.0

#### Shard Operations Collector (PR #824)

A new `RTFShardOperationCollector` was added to measure per-shard indexing and search rates. It computes the delta between the current and previous collection windows and publishes metrics via OpenTelemetry counters:

- `shard_indexing_rate` — indexing operations per shard per interval
- `shard_search_rate` — search operations per shard per interval

A new singleton `ShardMetricsCollector` was introduced to record per-shard CPU utilization and heap usage histograms (`shard_cpu_utilization`, `shard_heap_allocated`) from both search and bulk indexing paths.

Additional metrics added:
- `shard_search_latency` — search latency per shard per phase (query/fetch), recorded as a histogram in milliseconds
- `shard_indexing_latency` — indexing latency per shard, recorded as a histogram in milliseconds
- Heap usage tracking for bulk indexing operations via `RTFPerformanceAnalyzerTransportChannel`

#### Node Stats Collector Optimization (PR #824)

Both `NodeStatsAllShardsMetricsCollector` and `RTFNodeStatsAllShardsMetricsCollector` were refactored:
- Removed mutable instance-level `currentShards` and `currentPerShardStats` maps
- `populatePerShardStats()` now returns a local map, reducing state and improving thread safety
- Added null check for `currentIndexShardStats` to prevent NPE on deleted/closing shards
- Improved handling of new shards: metrics are now correctly emitted for shards not present in the previous collection window

#### CVE-2025-68161 Fix (PR #932)

Force-resolved `log4j-core` and `log4j-api` dependencies to the project's `log4jVersion` in `build.gradle` to address CVE-2025-68161. Removed the previous explicit `implementation` declarations for log4j, relying on the forced resolution instead.

#### Disable dependencyLicenses Check (PR #926)

Disabled the `dependencyLicenses` Gradle task to align with other OpenSearch plugin repositories. This check was failing when core's Gradle version catalog received updates. Removed all associated license SHA and license/notice files from the `licenses/` directory.

### Technical Changes

| Area | Change |
|------|--------|
| New class: `RTFShardOperationCollector` | Collects per-shard indexing/search rate deltas every 5 seconds |
| New class: `ShardMetricsCollector` | Singleton for recording per-shard CPU and heap histograms |
| `RTFPerformanceAnalyzerSearchListener` | Added search latency histogram; records CPU/heap to `ShardMetricsCollector`; uses `tookInNanos` for accurate timing |
| `RTFPerformanceAnalyzerTransportChannel` | Added indexing latency and heap usage histograms; records to `ShardMetricsCollector` |
| `RTFPerformanceAnalyzerTransportRequestHandler` | Creates indexing latency and heap usage histograms |
| `NodeStatsAllShardsMetricsCollector` | Refactored to use local maps; added null safety for shard stats |
| `RTFNodeStatsAllShardsMetricsCollector` | Same refactoring; fixed log message from "RTFDisksCollector" to "RTFNodeStatsMetricsCollector" |
| `Utils` | Added `computeShareFactor()` utility; registered `RTFShardOperationCollector` with 5s interval |
| `build.gradle` | Force-resolved log4j dependencies; disabled `dependencyLicenses` task |

## Limitations

- The shard operations collector uses a 5-second sampling interval, so very short-lived spikes may not be captured
- Heap usage tracking for bulk indexing relies on `ThreadMXBean.getThreadAllocatedBytes()`, which may not be available on all JVM implementations

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#824](https://github.com/opensearch-project/performance-analyzer/pull/824) | Added shard operations collector and optimized node stats collector | |
| [#932](https://github.com/opensearch-project/performance-analyzer/pull/932) | Fix CVE-2025-68161: Force resolve log4j dependencies | CVE-2025-68161 |
| [#926](https://github.com/opensearch-project/performance-analyzer/pull/926) | Disable dependencyLicenses check in PA repo | |
