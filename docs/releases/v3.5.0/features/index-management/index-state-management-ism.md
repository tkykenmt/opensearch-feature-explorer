---
tags:
  - index-management
---
# Index State Management (ISM)

## Summary

OpenSearch v3.5.0 introduces significant enhancements to Index State Management (ISM), including multi-tier rollups, cardinality metrics support, a new `search_only` action for Reader/Writer Separation, and customizable rename patterns for the `convert_index_to_remote` action.

## Details

### What's New in v3.5.0

#### Multi-Tier Rollups

ISM now supports hierarchical data aggregations where rollup indices can serve as source indices for subsequent rollup operations. This enables progressive data summarization (e.g., raw data → 1-minute → 5-minute → 10-minute intervals) within a single ISM policy.

```mermaid
flowchart LR
    A[Raw Data] --> B[1-min Rollup]
    B --> C[5-min Rollup]
    C --> D[10-min Rollup]
```

Key features:
- **Smart Initial Timestamp Computation**: Automatically detects rollup indices and fetches the earliest timestamp from the `date_histogram` field
- **Source Index Field Support**: New optional `source_index` field in ISMRollup schema for explicit source specification
- **Template Variable Resolution**: Supports Mustache templates (`{{ctx.index}}`, `{{ctx.source_index}}`) for dynamic index naming
- **Interval Compatibility Enforcement**: Validates that target intervals are exact multiples of source intervals

Example multi-tier policy:
```json
{
  "policy": {
    "description": "Multi-tier rollup: 1m → 5m → 10m",
    "default_state": "rollup_1m",
    "states": [
      {
        "name": "rollup_1m",
        "actions": [
          {
            "rollup": {
              "ism_rollup": {
                "target_index": "my_index_rollup_1m-{{ctx.index}}",
                "dimensions": [
                  {"date_histogram": {"source_field": "timestamp", "fixed_interval": "1m"}}
                ],
                "metrics": [{"source_field": "value", "metrics": [{"sum": {}}, {"avg": {}}]}]
              }
            }
          }
        ],
        "transitions": [{"state_name": "rollup_5m"}]
      },
      {
        "name": "rollup_5m",
        "actions": [
          {
            "rollup": {
              "ism_rollup": {
                "source_index": "my_index_rollup_1m-{{ctx.index}}",
                "target_index": "my_index_rollup_5m-{{ctx.index}}",
                "dimensions": [
                  {"date_histogram": {"source_field": "timestamp", "fixed_interval": "5m"}}
                ],
                "metrics": [{"source_field": "value", "metrics": [{"sum": {}}, {"avg": {}}]}]
              }
            }
          }
        ],
        "transitions": []
      }
    ]
  }
}
```

#### Cardinality Metric Support for Rollups

Rollup jobs now support the **cardinality metric** using HyperLogLog++ (HLL++) sketches, enabling approximate distinct count aggregations in rolled-up data.

Key features:
- **HLL++ Sketch Storage**: Cardinality metrics stored as serialized HLL++ sketches using `.hll` field suffix
- **Configurable Precision**: `precision_threshold` parameter (default: 3000) balances accuracy vs. memory
- **Multi-Tier Support**: Sketches can be merged across rollup tiers maintaining approximate accuracy
- **Transparent Query Rewriting**: User queries automatically rewritten to use `.hll` field

Example configuration:
```json
{
  "metrics": [
    {
      "source_field": "user_id",
      "metrics": [
        {"cardinality": {"precision_threshold": 5000}}
      ]
    }
  ]
}
```

#### search_only ISM Action

New ISM action for Reader/Writer Separation that enables automatic scale-down of writer shards for indices.

When executed, this action calls the `_scale` API with `search_only: true`, which:
- Removes primary shards from data nodes
- Keeps search replicas available for queries
- Blocks further writes to the index

Example policy:
```json
{
  "policy": {
    "states": [
      {
        "name": "hot",
        "actions": [{"rollover": {"min_doc_count": 1000}}],
        "transitions": [{"state_name": "warm", "conditions": {"min_rollover_age": "7d"}}]
      },
      {
        "name": "warm",
        "actions": [{"search_only": {}}],
        "transitions": []
      }
    ]
  }
}
```

#### convert_index_to_remote rename_pattern Parameter

New optional `rename_pattern` parameter for the `convert_index_to_remote` action allows customizing the naming pattern for restored searchable snapshot indices.

- `$1` is replaced with the original index name
- Default is `$1_remote` for backward compatibility

Example:
```json
{
  "actions": [
    {
      "convert_index_to_remote": {
        "repository": "my_backup",
        "snapshot": "{{ctx.index}}",
        "rename_pattern": "remote_$1"
      }
    }
  ]
}
```

### Technical Changes

| Change | Description |
|--------|-------------|
| Multi-tier rollups | Rollup indices can now be used as source for subsequent rollups |
| Cardinality metric | HLL++ sketch-based approximate distinct counts in rollups |
| `search_only` action | Scale down writer shards for Reader/Writer Separation |
| `rename_pattern` parameter | Customizable naming for `convert_index_to_remote` action |
| Min version update | Source index support in ISM rollups requires v3.5.0+ |

## Limitations

- Multi-tier rollups require matching `precision_threshold` values across all tiers for cardinality metrics
- The `search_only` action requires Reader/Writer Separation to be enabled on the cluster
- Deleting a source rollup index while a downstream rollup job is processing will cause failure

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1533](https://github.com/opensearch-project/index-management/pull/1533) | Adding support for multi-tier rollups in ISM | [#1490](https://github.com/opensearch-project/index-management/issues/1490) |
| [#1567](https://github.com/opensearch-project/index-management/pull/1567) | Adding Cardinality as supported metric for Rollups | [#1493](https://github.com/opensearch-project/index-management/issues/1493) |
| [#1560](https://github.com/opensearch-project/index-management/pull/1560) | Add search_only ISM action for Reader/Writer Separation | [#1531](https://github.com/opensearch-project/index-management/issues/1531) |
| [#1568](https://github.com/opensearch-project/index-management/pull/1568) | Add optional rename_pattern parameter to convert_index_to_remote action | [#1426](https://github.com/opensearch-project/index-management/issues/1426) |
| [#1573](https://github.com/opensearch-project/index-management/pull/1573) | Change min version for supporting source index in ISM rollups to 3.5.0 | |
| [#1572](https://github.com/opensearch-project/index-management/pull/1572) | Improve CI speed by refactoring RollupActionIT | |
