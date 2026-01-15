---
tags:
  - opensearch-dashboards
---
# Quick Range Selection Fix

## Summary

Fixed the quick range time picker to properly parse date math expressions like `now-15m` by using the `datemath` package. This ensures that relative time expressions in the time filter are correctly converted to absolute datetime values.

## Details

### What's New in v2.16.0

The quick range selection in the time picker was not correctly parsing date math expressions. This fix introduces a `formatTimePickerDate` utility function that uses the `datemath` package to properly parse relative time expressions.

### Technical Changes

A new utility function was added to `src/plugins/data/common/data_frames/utils.ts`:

```typescript
/**
 * Parses timepicker datetimes using datemath package.
 * Will attempt to parse strings such as "now - 15m"
 *
 * @param dateRange - of type TimeRange
 * @param dateFormat - formatting string (should work with Moment)
 * @returns object with `fromDate` and `toDate` strings in UTC
 */
export const formatTimePickerDate = (dateRange: TimeRange, dateFormat: string) => {
  const dateMathParse = (date: string) => {
    const parsedDate = datemath.parse(date);
    return parsedDate ? parsedDate.utc().format(dateFormat) : '';
  };

  const fromDate = dateMathParse(dateRange.from);
  const toDate = dateMathParse(dateRange.to);

  return { fromDate, toDate };
};
```

### Changed Files

| File | Change |
|------|--------|
| `src/plugins/data/common/data_frames/utils.ts` | Added `formatTimePickerDate` utility function |
| `src/plugins/data/common/data_frames/data_frame_utils.test.ts` | Added unit tests for the new function |

### Behavior

| Input | Output |
|-------|--------|
| `{ from: 'now-15m', to: 'now' }` | `{ fromDate: '2024-05-04 12:15:00.000', toDate: '2024-05-04 12:30:00.000' }` |
| `{ from: 'fake', to: 'date' }` | `{ fromDate: 'Invalid date', toDate: 'Invalid date' }` |

## Limitations

- Invalid date strings return `'Invalid date'` rather than throwing an error
- Output is always in UTC timezone

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6782](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6782) | Fix for quickrange to use datemath to parse datetime strings | - |
