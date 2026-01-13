---
tags:
  - domain/core
  - component/server
  - indexing
  - search
---
# Date Format

## Summary

OpenSearch v3.3.0 adds support for the `epoch_micros` date format, enabling users to store and query timestamps with microsecond precision. This enhancement addresses use cases where millisecond precision is insufficient, such as high-frequency trading systems, scientific data analysis, and detailed event logging.

## Details

### What's New in v3.3.0

The `epoch_micros` date format allows date fields to accept timestamps as the number of microseconds since the Unix epoch (January 1, 1970, 00:00:00 UTC). This complements the existing `epoch_millis` and `epoch_second` formats.

### Technical Changes

#### New Date Format

| Format | Description | Example |
|--------|-------------|---------|
| `epoch_micros` | Microseconds since epoch | `1680000430768123` |

The format supports:
- Positive and negative timestamps
- Fractional values with up to nanosecond precision (e.g., `123.456` for 123 microseconds and 456 nanoseconds)
- Values ending with a decimal point (e.g., `123.`)

#### Implementation Details

The implementation follows the same approach as `epoch_millis`:

1. Added `EPOCH_MICROS` to `FormatNames` enum
2. Created `MICROS_FORMATTER` in `EpochTime` class with:
   - `MICROS` field for absolute microsecond values
   - `NANOS_OF_MICRO` field for sub-microsecond precision
3. Registered the formatter in `DateFormatters.forPattern()`

#### Changed Files

| File | Change |
|------|--------|
| `FormatNames.java` | Added `EPOCH_MICROS` enum value |
| `EpochTime.java` | Added `MICROS_FORMATTER` and supporting fields |
| `DateFormatters.java` | Registered `epoch_micros` pattern |

### Usage Example

Create an index with a date field using `epoch_micros` format:

```json
PUT my-index
{
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date",
        "format": "epoch_micros"
      }
    }
  }
}
```

Index a document with a microsecond timestamp:

```json
PUT my-index/_doc/1
{
  "timestamp": 1680000430768123
}
```

Use multiple formats including `epoch_micros`:

```json
PUT my-index
{
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date",
        "format": "strict_date_optional_time||epoch_micros"
      }
    }
  }
}
```

### Migration Notes

No migration is required. The new format is additive and does not affect existing date fields or formats.

## Limitations

- The `epoch_micros` format is not supported by Joda time (used in legacy date parsing), only by the Java time API
- Maximum value is constrained by Java's `Long.MAX_VALUE` divided by 1,000,000

## References

### Documentation
- [Date field type documentation](https://docs.opensearch.org/3.0/field-types/supported-field-types/date/): Official date field documentation
- [Format mapping parameter](https://docs.opensearch.org/3.0/field-types/mapping-parameters/format/): Date format configuration

### Pull Requests
| PR | Description |
|----|-------------|
| [#19245](https://github.com/opensearch-project/OpenSearch/pull/19245) | Add `epoch_micros` date format |

### Issues (Design / RFC)
- [Issue #14669](https://github.com/opensearch-project/OpenSearch/issues/14669): Feature request for epoch_micros support

## Related Feature Report

- Full feature documentation
