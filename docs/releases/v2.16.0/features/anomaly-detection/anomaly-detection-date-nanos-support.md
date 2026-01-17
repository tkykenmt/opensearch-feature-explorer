---
tags:
  - anomaly-detection
---
# Anomaly Detection date_nanos Support

## Summary

OpenSearch 2.16.0 adds support for the `date_nanos` field type as a valid timestamp field in Anomaly Detection. Previously, only the `date` field type was accepted for the time field when creating anomaly detectors. This enhancement allows users with nanosecond-precision timestamps to use Anomaly Detection without needing to create a separate `date` type field.

## Details

### What's New in v2.16.0

The `date_nanos` field type provides nanosecond precision for timestamps, which is useful for high-frequency data ingestion scenarios. Prior to this release, Anomaly Detection only validated `date` type fields as valid timestamp fields, causing a validation exception when users attempted to create detectors with `date_nanos` fields.

### Technical Changes

#### Backend Plugin (anomaly-detection)

The validation logic in `AbstractTimeSeriesActionHandler.validateTimeField()` was updated to accept both `date` and `date_nanos` field types:

```java
// Before: Only date type was accepted
if (!typeName.equals(CommonName.DATE_TYPE)) {
    // throw ValidationException
}

// After: Both date and date_nanos are accepted
if (!typeName.equals(CommonName.DATE_TYPE) && !typeName.equals(CommonName.DATE_NANOS_TYPE)) {
    // throw ValidationException
}
```

A new constant `DATE_NANOS_TYPE` was added to `CommonName.java`:

```java
public static final String DATE_NANOS_TYPE = "date_nanos";
```

#### Dashboards Plugin (anomaly-detection-dashboards-plugin)

The timestamp field selector in the detector creation UI was updated to include `date_nanos` fields in the dropdown:

```typescript
// Timestamp.tsx
const dateNanoFields = Array.from(
  get(opensearchState, 'dataTypes.date_nanos', []) as string[]
);

const allDateFields = dateFields.concat(dateNanoFields);

const timeStampFieldOptions = isEmpty(allDateFields)
  ? []
  : allDateFields.map((dateField) => ({ label: dateField }));
```

The `DataTypes` interface in the Redux reducer was extended to include `date_nanos`:

```typescript
export interface DataTypes {
  // ... existing types
  date?: string[];
  date_nanos?: string[];  // Added
  // ...
}
```

### Usage Example

Create an index with a `date_nanos` timestamp field:

```json
PUT /my-index
{
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date_nanos",
        "format": "epoch_millis||yyyy-MM-dd HH:mm:ss.SSS||yyyy-MM-dd HH:mm:ss.SSSSSS"
      },
      "value": {
        "type": "double"
      }
    }
  }
}
```

Create an anomaly detector using the `date_nanos` field as the timestamp:

```json
POST /_plugins/_anomaly_detection/detectors
{
  "name": "my-detector",
  "description": "Detector with date_nanos timestamp",
  "time_field": "timestamp",
  "indices": ["my-index"],
  "feature_attributes": [
    {
      "feature_name": "value_avg",
      "feature_enabled": true,
      "aggregation_query": {
        "value_avg": {
          "avg": {
            "field": "value"
          }
        }
      }
    }
  ],
  "detection_interval": {
    "period": {
      "interval": 10,
      "unit": "Minutes"
    }
  }
}
```

## Limitations

- The internal processing still uses millisecond precision for anomaly detection intervals
- No changes to the anomaly detection algorithm itself; only the timestamp field validation was updated

## References

### Pull Requests

| PR | Repository | Description |
|----|------------|-------------|
| [#1238](https://github.com/opensearch-project/anomaly-detection/pull/1238) | anomaly-detection | Adding support for date_nanos to Anomaly Detection |
| [#795](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/795) | anomaly-detection-dashboards-plugin | Allow date_nanos dates in timestamp selection |

### Related Issues

| Issue | Repository | Description |
|-------|------------|-------------|
| [#1226](https://github.com/opensearch-project/anomaly-detection/issues/1226) | anomaly-detection | Support date_nanos as a date field in Anomaly Detection |
