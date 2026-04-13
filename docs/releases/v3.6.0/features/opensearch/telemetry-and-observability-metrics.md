---
tags:
  - opensearch
---
# Telemetry & Observability Metrics

## Summary

OpenSearch v3.6.0 introduces two complementary enhancements to the telemetry framework: immutable `Tags` for allocation-efficient metric tagging, and `NodeRuntimeMetrics` for exposing ~30 JVM/CPU runtime gauges through the `MetricsRegistry` API following OpenTelemetry semantic conventions.

## Details

### What's New in v3.6.0

#### Immutable Tags (PR #20788)

The `Tags` class in `libs/telemetry` was redesigned from a mutable `HashMap`-backed container to an immutable sorted-array implementation with a precomputed hash. This eliminates per-call allocation overhead on the metrics hot path.

**Internal storage:**

```java
public final class Tags {
    private final String[] keys;      // sorted by key
    private final Object[] values;    // parallel to keys
    private final int hashCode;       // precomputed at construction
}
```

**New API:**

| Method | Description |
|--------|-------------|
| `Tags.of(key, value)` | 1-tag factory (String, long, double, boolean) |
| `Tags.ofStringPairs(String...)` | N-pair varargs factory |
| `Tags.concat(a, b)` | Merge-sort two Tags; `b` wins on collision |
| `Tags.fromMap(Map)` | Bridge from existing map-based callers |
| `size()`, `getKey(i)`, `getValue(i)` | Direct array access |
| `equals()`, `hashCode()` | Content-based, safe as map keys |

**Backward compatibility:** `Tags.create()` and all `addTag()` overloads are deprecated but not removed. `create()` returns `Tags.EMPTY`; each `addTag()` returns a new immutable instance via `Tags.concat()`. Existing fluent chains compile and produce correct results.

**Bug fix included:** Fixed `AutoForceMergeMetrics` silently dropping tags due to unreassigned `addTag()` return value — a latent bug exposed by the immutability change.

#### Node Runtime Metrics (PR #20844)

Added `NodeRuntimeMetrics`, a `Closeable` component that registers pull-based gauges through `MetricsRegistry`, covering:

| Category | Metrics | Tags |
|----------|---------|------|
| Memory | `jvm.memory.used`, `jvm.memory.committed`, `jvm.memory.limit`, `jvm.memory.used_after_last_gc` | `type` (heap/non_heap), `pool` (per memory pool) |
| GC | `jvm.gc.duration`, `jvm.gc.count` | `gc` (per collector) |
| Buffer pools | `jvm.buffer.memory.used`, `jvm.buffer.memory.limit`, `jvm.buffer.count` | `pool` (direct/mapped) |
| Threads | `jvm.thread.count` (total + per-state) | `state` (runnable, waiting, etc.) |
| Classes | `jvm.class.count`, `jvm.class.loaded`, `jvm.class.unloaded` | — |
| CPU | `jvm.cpu.recent_utilization`, `jvm.system.cpu.utilization` | — |
| Uptime | `jvm.uptime` | — |

**Design highlights:**
- All gauge suppliers read through `JvmService.stats()` with a 1-second TTL cache — a single collection sweep reuses one snapshot across all gauges
- Memory pools, GC collectors, and buffer pools are discovered dynamically from the initial `JvmStats` snapshot and tagged by name, working across G1, Parallel, CMS, ZGC, and other collectors
- Per-state thread counts use a separate synchronized cache (1s TTL) to avoid redundant `getThreadInfo()` calls
- `NodeRuntimeMetrics` implements `Closeable` with an idempotent `AtomicBoolean` guard and is added to `Node`'s `resourcesToClose`
- Metric names follow OpenTelemetry JVM semantic conventions (`jvm.memory.used`, `jvm.gc.duration`, `jvm.thread.count`, etc.)

### Technical Changes

**Files changed (PR #20788):**
- `libs/telemetry/src/main/java/org/opensearch/telemetry/metrics/tags/Tags.java` — Rewritten from mutable HashMap to immutable sorted-array
- `server/src/main/java/org/opensearch/index/autoforcemerge/AutoForceMergeMetrics.java` — Fixed unreassigned `addTag()` return value
- `test/telemetry/src/main/java/org/opensearch/test/telemetry/TestInMemoryHistogram.java` — Updated to use `Map` interface instead of `HashMap` cast

**Files changed (PR #20844):**
- `server/src/main/java/org/opensearch/monitor/NodeRuntimeMetrics.java` — New class (427 lines)
- `server/src/main/java/org/opensearch/node/Node.java` — Wires `NodeRuntimeMetrics` into node lifecycle

## Limitations

- JVM runtime metrics are pull-based gauges only; no event-driven GC pause duration histograms yet (noted as TODO in source)
- Metrics require a telemetry backend plugin (e.g., OTel plugin) to be configured for export
- CPU utilization values are clamped to [0.0, 1.0]; negative values from the OS probe are reported as 0.0

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/OpenSearch/pull/20788` | Make Telemetry Tags Immutable | — |
| `https://github.com/opensearch-project/OpenSearch/pull/20844` | Add node-level JVM and CPU runtime metrics | — |

### External References
- OpenTelemetry JVM semantic conventions: https://opentelemetry.io/docs/specs/semconv/runtime/jvm-metrics/
