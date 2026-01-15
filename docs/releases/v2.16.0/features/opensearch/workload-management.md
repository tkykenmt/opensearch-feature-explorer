---
tags:
  - opensearch
---
# Workload Management

## Summary

OpenSearch v2.16.0 introduces the foundational components for Workload Management, a new feature designed to provide node-level resiliency by organizing search requests into Query Groups with configurable resource limits. This release adds the QueryGroup schema and header propagation mechanism.

## Details

### What's New in v2.16.0

This release establishes the core infrastructure for Workload Management:

1. **QueryGroup Schema** - A new cluster metadata construct for defining resource-limited query groups
2. **Header Propagation** - Mechanism to propagate queryGroupId across child requests and nodes

### QueryGroup Schema

The QueryGroup is a logical construct for running search requests within virtual resource limits. Each QueryGroup includes:

| Field | Type | Description |
|-------|------|-------------|
| `_id` | String | Unique identifier (UUID) |
| `name` | String | Human-readable name (max 50 chars) |
| `resiliency_mode` | Enum | `soft`, `enforced`, or `monitor` |
| `resourceLimits` | Map | Resource type to threshold mapping |
| `updatedAt` | Long | Epoch timestamp in milliseconds |

Example schema:
```json
{
    "_id": "fafjafjkaf9ag8a9ga9g7ag0aagaga",
    "resourceLimits": {
        "memory": 0.4
    },
    "resiliency_mode": "enforced",
    "name": "analytics",
    "updatedAt": 4513232415
}
```

### Resiliency Modes

| Mode | Behavior |
|------|----------|
| `soft` | Can exceed limits if node is not in duress |
| `enforced` | Never breaches limits; cancels tasks immediately when exceeded |
| `monitor` | No cancellation; logs eligible task cancellations only |

### Resource Types

| Resource | Description |
|----------|-------------|
| `cpu` | CPU usage threshold |
| `memory` | Memory/heap usage threshold |

### Header Propagation

The `QueryGroupThreadContextStatePropagator` class propagates the `queryGroupId` header:
- Across child requests within the same node
- Across nodes in the cluster

This enables resource tracking and usage-based cancellation for Query Groups.

## Limitations

- This is foundational work; full Query Group management APIs are not yet available
- Resource monitoring and cancellation framework will be added in subsequent releases
- Marked as `@ExperimentalApi`

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#13669](https://github.com/opensearch-project/OpenSearch/pull/13669) | Add QueryGroup schema | [#12342](https://github.com/opensearch-project/OpenSearch/issues/12342) |
| [#14614](https://github.com/opensearch-project/OpenSearch/pull/14614) | Add queryGroupId header propagator | [#12342](https://github.com/opensearch-project/OpenSearch/issues/12342) |

### Related Issues

- [RFC: Search Query Sandboxing](https://github.com/opensearch-project/OpenSearch/issues/12342)
