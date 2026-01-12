# Anomaly Detection Enhancements

## Summary

OpenSearch v2.18.0 introduces several enhancements to the Anomaly Detection plugin, including improved suppression rule validation in the AnomalyDetector constructor, a fix for default rules not being applied when users provide an empty ruleset, and an upgrade to Random Cut Forest (RCF) version 4.2.0. These changes improve the reliability and usability of anomaly detection by providing immediate validation feedback and ensuring consistent rule application.

## Details

### What's New in v2.18.0

#### Suppression Rule Validation

A new validation mechanism has been added to the `AnomalyDetector` constructor that validates suppression rules at detector creation time. This ensures that any configuration errors are caught early and reported to users immediately, rather than failing silently during detection.

The validation checks:
- Feature name exists in the defined features list
- Referenced feature is enabled
- Threshold values are valid numbers (not NaN)
- Threshold values are positive for applicable threshold types

#### Default Rules Bug Fix

Fixed a bug where default suppression rules were not applied when users provided an empty ruleset. Previously, passing an empty rules array would result in no rules being applied. Now, the system correctly falls back to the default 20% suppression rule when the rules list is null or empty.

```java
// Before: Only checked for null
this.rules = rules == null ? getDefaultRule() : rules;

// After: Also checks for empty list
this.rules = rules == null || rules.isEmpty() ? getDefaultRule() : rules;
```

#### RCF Version Upgrade

The Random Cut Forest library has been upgraded from version 4.1.0 to 4.2.0, bringing performance improvements and bug fixes to the underlying anomaly detection algorithm.

### Technical Changes

#### New Validation Issue Type

A new `ValidationIssueType.RULE` has been added to support rule-specific validation errors:

| Issue Type | Field | Description |
|------------|-------|-------------|
| `RULE` | `rules` | Suppression rule validation errors |

#### Validation Error Messages

| Condition | Error Message |
|-----------|---------------|
| Features undefined with rules | "Features are not defined while suppression rules are provided." |
| Null rule or conditions | "A suppression rule or its conditions are not properly defined." |
| Null condition | "A condition within a suppression rule is not properly defined." |
| Missing feature name | "A condition is missing the feature name." |
| Non-existent feature | "Feature \"{name}\" specified in a suppression rule does not exist." |
| Disabled feature | "Feature \"{name}\" specified in a suppression rule is not enabled." |
| NaN threshold value | "The threshold value for feature \"{name}\" is not a valid number." |
| Non-positive threshold | "The threshold value for feature \"{name}\" must be a positive number." |

### Usage Example

#### Creating a Detector with Suppression Rules

```json
POST _plugins/_anomaly_detection/detectors
{
  "name": "cpu-detector-with-rules",
  "time_field": "timestamp",
  "indices": ["server-metrics-*"],
  "feature_attributes": [
    {
      "feature_name": "avg_cpu",
      "feature_enabled": true,
      "aggregation_query": {
        "avg_cpu": { "avg": { "field": "cpu_usage" } }
      }
    }
  ],
  "rules": [
    {
      "action": "IGNORE_ANOMALY",
      "conditions": [
        {
          "feature_name": "avg_cpu",
          "threshold_type": "actual_over_expected_ratio",
          "operator": "LTE",
          "value": 0.3
        }
      ]
    }
  ],
  "detection_interval": {
    "period": { "interval": 5, "unit": "Minutes" }
  }
}
```

If the feature name doesn't exist or is disabled, the API will return a validation error immediately.

### Migration Notes

- No migration required for existing detectors
- Detectors with empty rules arrays will now use default rules (20% threshold)
- Validation errors will be returned at detector creation/update time

## Limitations

- Rule validation only occurs at detector creation/update time
- Threshold value validation only applies to specific threshold types (margin and ratio types)

## References

### Documentation
- [Anomaly Detection Documentation](https://docs.opensearch.org/2.18/observing-your-data/ad/index/): Official documentation
- [Anomaly Detection API](https://docs.opensearch.org/2.18/observing-your-data/ad/api/): API reference
- [Suppression Rules](https://docs.opensearch.org/2.18/observing-your-data/ad/index/#suppressing-anomalies-with-threshold-based-rules): Threshold-based rule configuration

### Pull Requests
| PR | Description |
|----|-------------|
| [#1341](https://github.com/opensearch-project/anomaly-detection/pull/1341) | Add rule validation in AnomalyDetector constructor |
| [#1334](https://github.com/opensearch-project/anomaly-detection/pull/1334) | Bump RCF version and fix default rules bug in AnomalyDetector |

## Related Feature Report

- [Full feature documentation](../../../../features/anomaly-detection/anomaly-detection.md)
