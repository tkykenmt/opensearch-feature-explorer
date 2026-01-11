# Node Stats

## Summary

Node Stats provides comprehensive statistics about OpenSearch cluster nodes through the `/_nodes/stats` API. This feature enables monitoring of node health, resource usage, and performance metrics including CPU, memory, JVM, disk I/O, and various OpenSearch-specific statistics. The API is essential for cluster monitoring, capacity planning, and troubleshooting.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Client"
        REQ[Stats Request]
    end
    
    subgraph "OpenSearch Node"
        API[REST API Handler]
        NSA[NodesStatsAction]
        
        subgraph "Stats Collectors"
            OS[OS Stats]
            JVM[JVM Stats]
            PROC[Process Stats]
            FS[Filesystem Stats]
            IDX[Index Stats]
            TP[Thread Pool Stats]
        end
        
        subgraph "System Resources"
            CGROUP[cgroup Files]
            PROC_FS[/proc Filesystem]
            SYS_FS[/sys Filesystem]
        end
    end
    
    REQ --> API
    API --> NSA
    NSA --> OS
    NSA --> JVM
    NSA --> PROC
    NSA --> FS
    NSA --> IDX
    NSA --> TP
    
    OS --> CGROUP
    OS --> PROC_FS
    FS --> SYS_FS
```

### Data Flow

```mermaid
flowchart LR
    A[Client Request] --> B[REST Handler]
    B --> C[NodesStatsRequest]
    C --> D[Transport Action]
    D --> E[Node Stats Collection]
    E --> F[Aggregate Response]
    F --> G[JSON Response]
```

### Components

| Component | Description |
|-----------|-------------|
| `NodesStatsRequest` | Request object specifying which metrics to collect |
| `NodesStatsResponse` | Response containing statistics from all requested nodes |
| `NodeStats` | Statistics for a single node |
| `OsStats` | Operating system statistics (CPU, memory, swap) |
| `ProcessStats` | Process-level statistics (file descriptors, CPU time) |
| `JvmStats` | JVM statistics (heap, GC, threads) |
| `FsInfo` | Filesystem statistics (disk space, I/O) |
| `ThreadPoolStats` | Thread pool statistics per pool |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| N/A | Node stats is always available | - |

### API Endpoints

```
GET /_nodes/stats
GET /_nodes/<node_id>/stats
GET /_nodes/stats/<metric>
GET /_nodes/<node_id>/stats/<metric>
GET /_nodes/stats/<metric>/<index_metric>
```

### Available Metrics

| Metric | Description |
|--------|-------------|
| `indices` | Index statistics (docs, store, indexing, search, etc.) |
| `os` | OS statistics (CPU, memory, swap, cgroup) |
| `process` | Process statistics (file descriptors, CPU) |
| `jvm` | JVM statistics (heap, GC, threads, buffer pools) |
| `thread_pool` | Thread pool statistics |
| `fs` | Filesystem statistics |
| `transport` | Transport layer statistics |
| `http` | HTTP layer statistics |
| `breaker` | Circuit breaker statistics |
| `script` | Script compilation statistics |
| `discovery` | Cluster discovery statistics |
| `ingest` | Ingest pipeline statistics |

### Usage Example

```bash
# Get all stats for all nodes
GET /_nodes/stats

# Get specific metrics
GET /_nodes/stats/os,jvm

# Get stats for specific node
GET /_nodes/node1/stats

# Example response (partial)
{
  "nodes": {
    "node_id": {
      "os": {
        "cpu": {
          "percent": 12,
          "load_average": {
            "1m": 0.5,
            "5m": 0.4,
            "15m": 0.3
          }
        },
        "mem": {
          "total_in_bytes": 17179869184,
          "free_in_bytes": 8589934592,
          "used_percent": 50
        }
      }
    }
  }
}
```

### Security Policy (cgroup access)

OpenSearch requires read access to cgroup files for CPU statistics on Linux:

```
/sys/fs/cgroup/cpu
/sys/fs/cgroup/cpuacct
/sys/fs/cgroup/cpu,cpuacct  # Combined controller (added in v3.4.0)
/sys/fs/cgroup/cpuset
/sys/fs/cgroup/memory
```

## Limitations

- CPU statistics may show -1 on systems where cgroup files are not accessible
- Some metrics are platform-specific (e.g., cgroup stats are Linux-only)
- High-frequency polling can impact cluster performance

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.4.0 | [#20108](https://github.com/opensearch-project/OpenSearch/pull/20108) | Fix negative CPU usage values by adding cgroup permissions |
| v3.0.0 | [#17576](https://github.com/opensearch-project/OpenSearch/pull/17576) | Fix NPE in node stats due to QueryGroupTasks |

## References

- [Issue #19120](https://github.com/opensearch-project/OpenSearch/issues/19120): Bug report for negative CPU values
- [Issue #17518](https://github.com/opensearch-project/OpenSearch/issues/17518): NPE in node stats due to QueryGroupTasks
- [Nodes Stats API Documentation](https://docs.opensearch.org/3.0/api-reference/nodes-apis/nodes-stats/): Official API documentation

## Change History

- **v3.4.0** (2026-01-11): Fixed negative CPU usage values on Linux systems with combined cpu,cpuacct cgroup controller
- **v3.0.0** (2025-05-13): Fixed NullPointerException when gathering node stats with QueryGroupTasks that don't have queryGroupId set
