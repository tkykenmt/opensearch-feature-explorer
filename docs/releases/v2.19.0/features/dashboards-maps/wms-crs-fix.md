---
tags:
  - dashboards-maps
---
# WMS CRS Fix

## Summary

Fixed a bug where custom WMS layers would generate incorrect bounding box (BBOX) parameters when using coordinate reference systems other than EPSG:3857. The fix locks the WMS CRS input to EPSG:3857, which is the only coordinate system supported by MapLibre GL.

## Details

### What's New in v2.19.0

The custom WMS layer configuration now enforces EPSG:3857 as the coordinate reference system:

- The CRS input field is disabled and locked to `EPSG:3857`
- If no CRS is specified in the layer source, it defaults to `EPSG:3857`
- This prevents incorrect BBOX calculations that previously occurred when users specified other CRS values like EPSG:4326

### Technical Changes

The fix modifies two components:

1. **UI Component** (`custom_map_source.tsx`): Disables the CRS input field and sets a constant value of `EPSG:3857`

2. **Layer Functions** (`customLayerFunctions.ts`): Adds a fallback to ensure `EPSG:3857` is used when building WMS URLs

```typescript
// Ensures CRS defaults to EPSG:3857 for WMS layers
if (!layerSource.crs) {
  layerSource.crs = "EPSG:3857"
}
```

### Root Cause

MapLibre GL only supports the Web Mercator projection (EPSG:3857). When users specified other coordinate systems like EPSG:4326 (WGS 84), the BBOX parameter values were calculated in EPSG:3857 coordinates but labeled with the user-specified CRS. This resulted in BBOX values that were approximately 100,000 times larger than expected, making WMS layers unusable.

For example, a request for Iowa would generate:
- **Before fix**: `bbox=-10644926.307106785,5009377.085697312,-10331840.239250705,5322463.153553393` (EPSG:3857 values with EPSG:4326 label)
- **After fix**: `bbox=-10644926.307106785,5009377.085697312,-10331840.239250705,5322463.153553393&srs=EPSG:3857` (correct CRS label)

## Limitations

- Custom WMS layers are now restricted to EPSG:3857 coordinate system only
- WMS servers that do not support EPSG:3857 cannot be used as custom map sources
- This is a workaround rather than a full fix; true multi-CRS support would require MapLibre to support coordinate transformations

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#632](https://github.com/opensearch-project/dashboards-maps/pull/632) | Lock WMS CRS input to EPSG:3857 | [#600](https://github.com/opensearch-project/dashboards-maps/issues/600) |

### Issues
- [#600](https://github.com/opensearch-project/dashboards-maps/issues/600): Maps miscalculates WMS BBOX
