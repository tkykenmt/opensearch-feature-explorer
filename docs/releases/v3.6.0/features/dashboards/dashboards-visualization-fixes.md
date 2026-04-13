---
tags:
  - dashboards
---
# Dashboards Visualization Fixes

## Summary

Three bug fixes across Dashboards visualization plugins in v3.6.0: a JSON escape issue in Vega Express that broke chart rendering, a notebook type redirect issue that showed error pages instead of redirecting, and a geo_shape bounding box filter that was silently ignored in Maps.

## Details

### What's New in v3.6.0

#### Fix: JSON Escape in Vega Express (dashboards-investigation)

The Expression Parser in the data distribution embeddable performed escape parsing on strings, causing `\n` sequences in JSON to be interpreted as real line breaks. This broke the JSON structure and prevented Vega visualizations from rendering correctly.

The fix introduces a dedicated `escapeString` method that double-escapes backslashes (`\` → `\\`) before passing the JSON string into the Expression Pipeline. This ensures escape characters are preserved correctly after the parser processes them.

Changed file: `public/components/notebooks/components/data_distribution/embeddable/data_distribution_embeddable.ts`

Before:
```typescript
const jsonString = JSON.stringify(this.visInput?.spec).replace(/'/g, '\\u0027');
return `vega spec='${jsonString}'`;
```

After:
```typescript
private escapeString = (data: string): string => {
  return data.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
};

const jsonString = JSON.stringify(this.visInput?.spec);
return `vega spec='${this.escapeString(jsonString)}'`;
```

#### Fix: Notebook Type Redirect (dashboards-investigation)

When a user opened a notebook URL with an incorrect type (e.g., opening a classic notebook via an agentic notebook URL, or vice versa), the page displayed an error message instead of redirecting to the correct URL. The fix uses React Router's `<Redirect>` component to immediately redirect to the correct notebook type URL, preventing page jitter and improving user experience.

Key changes:
- Agentic notebook component now redirects to `/{openedNoteId}` when notebook type is `CLASSIC`
- Classic notebook component now redirects to `/agentic/{openedNoteId}` when notebook type is `Agentic`
- Redirect happens before rendering content, eliminating the error state entirely

Changed files:
- `public/components/notebooks/components/agentic_notebook.tsx`
- `public/components/notebooks/components/classic_notebook.tsx`

#### Fix: Geo_shape Bounding Box Filter (dashboards-maps)

The "Only request data around map extent" filter in Maps was only enabled for `geo_point` fields, silently ignoring `geo_shape` fields. For indices with more than 10,000 documents, this meant the top 10k documents returned were unlikely to be within the current viewport, making it appear as if there were no matches.

The fix adds `geo_shape` to the list of allowed field types for the bounding box filter.

Changed file: `public/model/layerRenderController.ts`

Before:
```typescript
disabled:
  !mapLayer.source.useGeoBoundingBoxFilter ||
  (mapLayer.type === DASHBOARDS_MAPS_LAYER_TYPE.DOCUMENTS && geoFieldType !== 'geo_point'),
```

After:
```typescript
disabled:
  !mapLayer.source.useGeoBoundingBoxFilter ||
  (mapLayer.type === DASHBOARDS_MAPS_LAYER_TYPE.DOCUMENTS && !['geo_point', 'geo_shape'].includes(geoFieldType)),
```

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/dashboards-investigation/pull/328` | Fix JSON escape issue in Vega Express | - |
| `https://github.com/opensearch-project/dashboards-investigation/pull/306` | Redirect when opening notebook with incorrect type URL | - |
| `https://github.com/opensearch-project/dashboards-maps/pull/798` | Fix filter by map extent ignored for geo_shape fields | `https://github.com/opensearch-project/dashboards-maps/issues/796` |
