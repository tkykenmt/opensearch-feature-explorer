---
tags:
  - opensearch-dashboards
---
# Field Name Search

## Summary

The field name search filter in Discover's sidebar is now case insensitive, improving usability when searching for fields in the field selector.

## Details

### What's New in v2.16.0

Prior to this change, the "Search field names" filter in Discover's sidebar required exact case matching. Users had to type field names with the correct capitalization to find them.

With this enhancement, the field name search now performs case-insensitive matching. For example, searching for "timestamp", "TIMESTAMP", or "TimeStamp" will all find a field named `@timestamp`.

### Technical Changes

The change modifies the `isFieldFiltered` function in the Discover plugin's field filter logic:

```typescript
// Before: Case-sensitive matching
const matchName = !filterState.name || field.name.indexOf(filterState.name) !== -1;

// After: Case-insensitive matching
const matchName = !filterState.name || 
  field.name.toLowerCase().indexOf(filterState.name.toLowerCase()) !== -1;
```

**Changed File:**
- `src/plugins/discover/public/application/components/sidebar/lib/field_filter.ts`

### Usage

1. Navigate to Discover
2. In the left sidebar, use the "Search field names" input
3. Type any field name (case doesn't matter)
4. Fields matching the search term will be displayed regardless of case

## Limitations

- This change only affects the field name search in Discover's sidebar
- Other search/filter functionality in OpenSearch Dashboards is not affected

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#6759](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6759) | Make Field Name Search Filter Case Insensitive |
