---
tags:
  - search
---

# Workload Management (WLM)

## Summary

OpenSearch 3.0.0 includes two key improvements to Workload Management (WLM): scroll API support and the renaming of QueryGroup to WorkloadGroup. The scroll API fix resolves warning logs that occurred when using search scroll operations, while the renaming provides clearer terminology that better reflects the feature's purpose of managing diverse workloads beyond just queries.

## Details

### What's New in v3.0.0

#### 1. WLM Support for Search Scroll API

Prior to this release, using the search scroll API would generate warning logs because the `queryGroupId` was not being set for scroll operations. This fix ensures that scroll API requests are properly tracked within the WLM framework.

**Problem Resolved:**
```
[WARN] QueryGroup _id can't be null, It should be set before accessing it. This is abnormal behaviour
```

**Technical Changes:**
- Modified `TransportSearchScrollAction` to set the `queryGroupId` from thread context for scroll requests
- Added `isQueryGroupSet()` method to `QueryGroupTask` to track whether a query group has been assigned
- Updated `QueryGroupResourceUsageTrackerService` to filter out tasks without a query group set

#### 2. QueryGroup Renamed to WorkloadGroup

The terminology has been updated from "QueryGroup" to "WorkloadGroup" throughout the codebase to better reflect that WLM manages various workload types, not just queries. This change improves clarity and aligns with features like Query Insights and Cluster Insights.

**API Changes:**

| Old Endpoint | New Endpoint |
|--------------|--------------|
| `PUT _wlm/query_group` | `PUT _wlm/workload_group` |
| `GET _wlm/query_group/{name}` | `GET _wlm/workload_group/{name}` |
| `DELETE _wlm/query_group/{name}` | `DELETE _wlm/workload_group/{name}` |

**Response Field Changes:**

| Old Field | New Field |
|-----------|-----------|
| `query_groups` | `workload_groups` |

### Technical Changes

#### Modified Components

| Component | Change |
|-----------|--------|
| `TransportSearchScrollAction` | Added `ThreadPool` injection and `queryGroupId` setting for scroll requests |
| `QueryGroupTask` | Added `isQueryGroupSet` flag and getter method |
| `QueryGroupResourceUsageTrackerService` | Added filter to exclude tasks without query group set |
| `WorkloadManagementPlugin` | Updated action handlers and REST handlers to use new naming |
| `WorkloadGroupPersistenceService` | Renamed from `QueryGroupPersistenceService` |
| REST Actions | All renamed from `*QueryGroup*` to `*WorkloadGroup*` |

#### Backward Compatibility

- **Wire Protocol**: No breaking changes - underlying field types remain unchanged
- **Cluster State**: Compatible with mixed cluster setups during rolling upgrades
- **Stats API**: Output format changed from `query_groups` to `workload_groups`

### Usage Example

**Create Workload Group (v3.0.0+):**
```json
PUT _wlm/workload_group
{
  "name": "analytics",
  "resiliency_mode": "enforced",
  "resource_limits": {
    "cpu": 0.4,
    "memory": 0.2
  }
}
```

**Search with Scroll (now properly tracked):**
```bash
# Initial search with scroll
curl -X POST "localhost:9200/my_index/_search?scroll=30s" -H "Content-Type: application/json" -d '{
  "query": {"match_all": {}},
  "size": 100
}'

# Subsequent scroll requests are now properly tracked in WLM
curl -X POST "localhost:9200/_search/scroll" -H "Content-Type: application/json" -d '{
  "scroll": "30s",
  "scroll_id": "<scroll_id>"
}'
```

### Migration Notes

If you have existing scripts or applications using the WLM API:

1. Update API endpoints from `query_group` to `workload_group`
2. Update response parsing to use `workload_groups` instead of `query_groups`
3. No changes needed for the `workloadGroupId` header - it remains unchanged

## Limitations

- The renaming is a breaking change for API consumers using the old endpoints
- Scroll API tracking requires the workload-management plugin to be installed

## References

### Documentation
- [Workload Management Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/workload-management/wlm-feature-overview/)
- [Workload Group Lifecycle API](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/workload-management/workload-group-lifecycle-api/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#16981](https://github.com/opensearch-project/OpenSearch/pull/16981) | Add WLM support for search scroll API |
| [#17901](https://github.com/opensearch-project/OpenSearch/pull/17901) | Rename QueryGroup to WorkloadGroup |

### Issues (Design / RFC)
- [Issue #16874](https://github.com/opensearch-project/OpenSearch/issues/16874): Bug report for QueryGroupTask warning in 2.18

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-workload-management.md)
