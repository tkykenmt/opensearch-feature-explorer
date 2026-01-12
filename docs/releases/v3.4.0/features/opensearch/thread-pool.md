---
tags:
  - indexing
  - performance
---

# Thread Pool - ForkJoinPool Support

## Summary

OpenSearch v3.4.0 introduces support for a new `ForkJoinPool` thread pool type, enabling plugins to register and manage ForkJoinPool-based executors within the OpenSearch cluster lifecycle. This enhancement is particularly beneficial for components like jVector that leverage ForkJoinPool for parallel processing during index building operations.

## Details

### What's New in v3.4.0

This release adds a new `FORK_JOIN` thread pool type to the existing thread pool infrastructure, allowing plugins to create work-stealing thread pools optimized for recursive, divide-and-conquer style parallel computations.

### Technical Changes

#### New Thread Pool Type

A new `ThreadPoolType.FORK_JOIN` enum value has been added to the existing thread pool types:

| Type | Description |
|------|-------------|
| `DIRECT` | Executes tasks directly on the calling thread |
| `FIXED` | Fixed-size thread pool |
| `RESIZABLE` | Dynamically resizable thread pool |
| `SCALING` | Scales between min and max threads |
| `FORK_JOIN` | **New** - Work-stealing ForkJoinPool for parallel tasks |

#### New Components

| Component | Description |
|-----------|-------------|
| `ForkJoinPoolExecutorBuilder` | Builder class for creating ForkJoinPool executors |
| `ForkJoinPoolExecutorSettings` | Settings container for ForkJoinPool configuration |

#### New Configuration

Plugins can register ForkJoinPool executors with the following settings:

| Setting | Description | Default |
|---------|-------------|---------|
| `thread_pool.{name}.parallelism` | Number of worker threads (must be >= 1) | Required |
| `thread_pool.{name}.async_mode` | Enable FIFO scheduling for forked tasks | `false` |
| `thread_pool.{name}.thread_factory` | Custom ForkJoinWorkerThreadFactory class name | `""` (default factory) |
| `thread_pool.{name}.enable_exception_handling` | Enable uncaught exception logging | `true` |

#### API Changes

The CAT thread pool API (`_cat/thread_pool`) now includes a `parallelism` column for ForkJoinPool types:

```
GET _cat/thread_pool?v&h=name,type,parallelism
```

Thread pool stats now include a `parallelism` field in the response for ForkJoinPool executors.

### Usage Example

Plugins can register a ForkJoinPool executor using the `ExecutorBuilder` mechanism:

```java
public class MyPlugin extends Plugin {
    @Override
    public List<ExecutorBuilder<?>> getExecutorBuilders(final Settings settings) {
        return List.of(new ForkJoinPoolExecutorBuilder("jvector", 8));
    }
}
```

The executor can then be used within the plugin:

```java
ForkJoinPool pool = (ForkJoinPool) threadPool.executor("jvector");
pool.submit(() -> {
    // Parallel task execution
});
```

### Migration Notes

- This is a new feature with no breaking changes
- Existing thread pool configurations remain unchanged
- ForkJoinPool executors do not support dynamic setting updates (unlike FIXED/SCALING pools)
- The `parallelism` setting is mandatory and must be >= 1

## Limitations

- ForkJoinPool executors cannot be dynamically resized after creation
- Queue size and keep-alive settings are not applicable to ForkJoinPool types
- Stats for ForkJoinPool show fixed values (active=0, queue=0, etc.) as ForkJoinPool manages its own internal state differently

## References

### Documentation
- [opensearch-jvector PR #116](https://github.com/opensearch-project/opensearch-jvector/pull/116): Related jVector integration

### Pull Requests
| PR | Description |
|----|-------------|
| [#19008](https://github.com/opensearch-project/OpenSearch/pull/19008) | Add support for a ForkJoinPool type |

### Issues (Design / RFC)
- [Issue #18674](https://github.com/opensearch-project/OpenSearch/issues/18674): Feature request for ForkJoinPool support

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-thread-pool.md)
