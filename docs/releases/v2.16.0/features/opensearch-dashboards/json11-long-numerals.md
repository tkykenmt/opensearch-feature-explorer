---
tags:
  - opensearch-dashboards
---
# JSON11 Long Numerals

## Summary

OpenSearch Dashboards v2.16.0 replaces the custom regex-based long numeral handling logic with JSON11, an AST-based JSON parser. This change dramatically improves performance when processing JSON responses containing large numeric values (17+ digits), reducing processing time from ~90 seconds to ~200ms for samples with 10K false-positives.

## Details

### Background

JavaScript's `Number` type is a 64-bit floating-point value that can safely represent integers up to `Number.MAX_SAFE_INTEGER` (9,007,199,254,740,991 - 16 digits). However, OpenSearch can return numeric values from other languages that exceed this limit (up to 19 digits). The native JSON parser corrupts these values, making them unusable.

### Previous Implementation

The previous implementation used a complex regex-based approach:
- Custom regex patterns to detect long numerals in JSON strings
- Marker-based string replacement to preserve precision
- Error-prone parsing with fallback mechanisms
- Approximately 260 lines of custom code in `packages/osd-std/src/json.ts`

### New Implementation

The new implementation leverages JSON11, an AST-based JSON parser:
- Replaced ~250 lines of custom regex logic with ~10 lines using JSON11
- Uses `JSON11.parse()` with `withLongNumerals: true` option
- Uses `JSON11.stringify()` with `withBigInt: false` option
- Upgraded `@opensearch-project/opensearch` client from v2.6.0 to v2.9.0

### Technical Changes

| Component | Change |
|-----------|--------|
| `packages/osd-std/src/json.ts` | Replaced regex-based parsing with JSON11 |
| `@opensearch-project/opensearch` | Upgraded from v2.6.0 to v2.9.0 |
| `json11` | Added as new dependency (v1.1.2) |

### Performance Improvement

| Metric | Before | After |
|--------|--------|-------|
| Processing time (10K false-positives) | ~90 seconds | ~200ms |
| Code complexity | ~260 lines | ~10 lines |

## Limitations

- Requires `json11` package as a new dependency
- BigInt values are converted to strings in JSON output (not native numerals)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6915](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6915) | Use JSON11 for handling long numerals | [#6377](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6377) |

### Related Issues
| Issue | Description |
|-------|-------------|
| [#6377](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6377) | opensearch-with-long-numerals blocks and times out from Discover page |
