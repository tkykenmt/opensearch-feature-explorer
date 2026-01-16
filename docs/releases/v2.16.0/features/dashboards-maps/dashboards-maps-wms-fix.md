---
tags:
  - dashboards-maps
---
# Dashboards Maps WMS Fix

## Summary

Fixed a bug where editing a WMS custom layer configuration in OpenSearch Dashboards Maps caused the map to generate WMS URLs without parameters, resulting in broken tile requests.

## Details

### What's New in v2.16.0

This release fixes a critical bug in the `UpdateLayerConfig()` function that caused WMS custom layers to break after editing their configuration.

### Technical Changes

The fix replaces the complex `updateLayerConfig()` function with a simpler `refreshLayer()` approach that removes and re-adds the layer when configuration changes are made.

**Before (broken):**
```typescript
const updateLayerConfig = (layerConfig, maplibreRef) => {
  // Complex logic trying to update layer properties in-place
  // Line 36 threw object reference error:
  // maplibreInstance.style.sourceCaches[layerConfig.id].update(maplibreInstance.transform)
};
```

**After (fixed):**
```typescript
const refreshLayer = (layerConfig, maplibreRef) => {
  const maplibreInstance = maplibreRef.current;
  if (maplibreInstance) {
    maplibreInstance.removeLayer(layerConfig.id);
    maplibreInstance.removeSource(layerConfig.id);
    addNewLayer(layerConfig, maplibreRef);
  }
};
```

### Root Cause

The original `updateLayerConfig()` function attempted to update WMS layer properties in-place by:
1. Calling private MapLibre GL methods
2. Accessing `maplibreInstance.transform` which was no longer available at execution time
3. Using workarounds that were fragile and error-prone

The fix simplifies the approach by deleting and recreating the layer, which is appropriate since updating WMS fields requires a full refresh of tiles anyway.

### Files Changed

| File | Changes |
|------|---------|
| `public/model/customLayerFunctions.ts` | Replaced `updateLayerConfig()` with `refreshLayer()` |
| `public/model/customLayerFunctions.test.ts` | Removed obsolete test for update behavior |
| `CHANGELOG.md` | Added bug fix entry |

## Limitations

- Layer refresh causes a brief visual flicker as tiles are reloaded
- This is expected behavior since WMS configuration changes require new tile requests

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#631](https://github.com/opensearch-project/dashboards-maps/pull/631) | Refresh custom wms layer+source on update | [#601](https://github.com/opensearch-project/dashboards-maps/issues/601) |
| [#633](https://github.com/opensearch-project/dashboards-maps/pull/633) | Backport to 2.x branch | - |

### Issues
| Issue | Description |
|-------|-------------|
| [#601](https://github.com/opensearch-project/dashboards-maps/issues/601) | Maps produces WMS URLs without parameters after editing WMS layer configuration |
