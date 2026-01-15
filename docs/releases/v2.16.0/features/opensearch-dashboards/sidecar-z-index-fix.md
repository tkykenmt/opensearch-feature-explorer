---
tags:
  - opensearch-dashboards
---
# Sidecar Z-Index Fix

## Summary

Fixed a z-index issue where the Sidecar panel was being covered by UI mask overlays. The Sidecar container's z-index was increased from 1000 to 1001 to ensure it renders above modal masks.

## Details

### What's New in v2.16.0

The Sidecar component is a fixed-position panel used by features like the AI Chat assistant. When flyout dialogs or modals with masks were opened, the mask overlay (z-index 1000) would cover the Sidecar panel, making it inaccessible.

### Technical Changes

The fix updates the Sidecar's z-index to be one level above the EUI mask:

```scss
// Before
.osdSidecarFlyout {
  z-index: 1000;
}

// After
.osdSidecarFlyout {
  // Sidecar z-index should more than mask. Actually will be 1001.
  z-index: $euiZMaskBelowHeader + 1;
}
```

The change uses the EUI variable `$euiZMaskBelowHeader` (value: 1000) plus 1, ensuring the Sidecar always renders above mask overlays while maintaining proper layering with other UI elements.

### Changed Files

| File | Change |
|------|--------|
| `src/core/public/overlays/sidecar/components/sidecar.scss` | Updated z-index from 1000 to `$euiZMaskBelowHeader + 1` |

## Limitations

- The Sidecar will now render above all mask overlays, which is the intended behavior for an independent container

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6964](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6964) | Update sidecar z-index style | - |
