---
tags:
  - anomaly-detection
---
# Anomaly Detection

## Summary

OpenSearch 2.19.0 introduces significant enhancements to the Anomaly Detection plugin, including feature direction rules for more precise anomaly filtering, flattened custom result index support for improved query performance, and increased replica count for custom result indices to enhance data durability.

## Details

### What's New in v2.19.0

#### Feature Direction Rules

Users can now configure suppression rules based on feature direction, allowing anomalies to be ignored when the actual value is either above or below the expected value. This expands on the custom suppression rules introduced in v2.17.

New threshold types:
- `ACTUAL_IS_OVER_EXPECTED`: Ignore anomalies when actual value exceeds expected
- `ACTUAL_IS_BELOW_EXPECTED`: Ignore anomalies when actual value is below expected

Example configuration:
```json
"rules": [
  {
    "action": "IGNORE_ANOMALY",
    "conditions": [
      {
        "feature_name": "sum_http_4xx",
        "threshold_type": "ACTUAL_IS_OVER_EXPECTED"
      }
    ]
  }
]
```

#### Flattened Custom Result Index

A new option to flatten nested fields in custom result indices enables easier querying and analysis. When enabled, nested fields like `feature_data`, `entity`, `relevant_attribution`, `expected_values`, and `past_values` are flattened into top-level fields.

Configuration:
```json
{
  "flatten_custom_result_index": true
}
```

This creates:
- A separate flattened result index with `_flattened_` suffix
- An ingest pipeline that transforms nested structures to flat fields
- Dynamic mapping enabled for the flattened index

#### Custom Result Index Replica Enhancement

The auto-expand replica setting for custom result indices changed from `0-1` to `0-2`, ensuring at least 2 replicas when node count exceeds 2 for improved data durability.

### Technical Changes

| Component | Change |
|-----------|--------|
| `ThresholdType` | Added `ACTUAL_IS_OVER_EXPECTED` and `ACTUAL_IS_BELOW_EXPECTED` enums |
| `Condition` | Updated to support nullable `value` and `operator` fields |
| `AnomalyResult` | Added rule-based anomaly grade override logic |
| `Config` | Added `flatten_custom_result_index` field and related methods |
| `IndexManagement` | Added `initFlattenedResultIndex()` method |
| `AbstractTimeSeriesActionHandler` | Added ingest pipeline setup for flattened indices |

### Dashboards Updates

The Anomaly Detection Dashboards plugin was updated to support the new feature direction capability:
- Moved suppression rules into feature creation workflow
- Added UI for selecting feature direction (above/below expected)
- Fixed toast message display for multiple rules with negative values

## Limitations

- Flattened result index cannot be enabled for existing detectors (only new detectors)
- Once flattened result index is disabled, the ingest pipeline is deleted but the flattened index remains
- Feature direction rules require null values for `operator` and `value` fields

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#1358](https://github.com/opensearch-project/anomaly-detection/pull/1358) | Adding feature direction rules | anomaly-detection |
| [#1401](https://github.com/opensearch-project/anomaly-detection/pull/1401) | Add flattened custom result index | anomaly-detection |
| [#1362](https://github.com/opensearch-project/anomaly-detection/pull/1362) | Changing replica count to 0-2 for custom result index | anomaly-detection |
| [#960](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/960) | Adding feature direction and moving suppression rules to each feature | anomaly-detection-dashboards-plugin |

### Documentation

- [Anomaly Detection](https://docs.opensearch.org/2.19/observing-your-data/ad/index/)
- [Anomaly Detection API](https://docs.opensearch.org/2.19/observing-your-data/ad/api/)
