# Query Sets & Judgment Lists

## Summary

This enhancement adds support for filtering Query Sets by their GUID (Globally Unique Identifier) in the Search Relevance Workbench. Previously, filtering only matched against the Query Set name, making it difficult to look up Query Sets using their unique identifier even though the backend returned this field. This improvement enables users to quickly locate specific Query Sets by searching for any part of their GUID.

## Details

### What's New in v3.4.0

- **GUID Filtering**: Query Sets can now be filtered by their `id` field (GUID) in addition to the `name` field
- **Strongly Typed Interface**: Introduced a new `QuerySetItem` TypeScript interface for better type safety
- **Aligned Structure**: The `QuerySetItem` interface now aligns with the existing `SearchConfigurationItem` structure for consistency

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `QuerySetItem` | New TypeScript interface defining the structure of Query Set items with `id`, `name`, `sampling`, `description`, `timestamp`, and `numQueries` fields |

#### Code Changes

The filtering logic in `useQuerySetList` hook was updated to include GUID matching:

**Before:**
```typescript
const filteredList = search
  ? list.filter((item) => item.name.toLowerCase().includes(search.toLowerCase()))
  : list;
```

**After:**
```typescript
const filteredList: QuerySetItem[] = search
  ? list.filter((qs: QuerySetItem) => {
      const s = search.toLowerCase();
      return qs.name.toLowerCase().includes(s) || qs.id.toLowerCase().includes(s);
    })
  : list;
```

### Usage Example

Users can now search for Query Sets using either the name or GUID:

```
# Search by name
"My Query Set"

# Search by GUID (partial match supported)
"guid-12345"

# Search by partial GUID
"98765"
```

### Migration Notes

No migration required. This is a backward-compatible enhancement that extends existing filtering functionality.

## Limitations

- GUID is not displayed in the Query Sets table UI, but can be used for filtering
- Filtering is case-insensitive and supports partial matches

## Related PRs

| PR | Description |
|----|-------------|
| [#687](https://github.com/opensearch-project/dashboards-search-relevance/pull/687) | Added support for filtering Query Sets by GUID and aligned QuerySetItem typing |

## References

- [Issue #679](https://github.com/opensearch-project/dashboards-search-relevance/issues/679): Feature request for GUID filtering
- [Issue #663](https://github.com/opensearch-project/dashboards-search-relevance/issues/663): Parent issue for Query Set improvements
- [Documentation](https://docs.opensearch.org/latest/search-plugins/search-relevance/index/): Search Relevance overview
- [Blog: Measuring and improving search quality metrics](https://opensearch.org/blog/measuring-and-improving-search-quality-metrics/): Detailed guide on using Query Sets and Judgment Lists

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-search-relevance/search-comparison.md)
