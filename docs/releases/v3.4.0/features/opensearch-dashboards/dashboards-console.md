---
tags:
  - dashboards
---

# Dashboards Console

## Summary

This release fixes a bug where the `console_polling` setting (which controls the "Automatically refresh autocomplete suggestions" option) could not be updated through the Dev Tools console UI. The setting value would not persist when toggled, causing autocomplete refresh to remain disabled even when users enabled it.

## Details

### What's New in v3.4.0

Fixed the inability to update the `console_polling` setting through the UI in the Dev Tools console.

### Technical Changes

#### Bug Description

When users attempted to toggle the "Automatically refresh autocomplete suggestions" setting in the Dev Tools console settings panel, the `console_polling` value in localStorage would not update correctly. This prevented the autocomplete feature from automatically refreshing suggestions based on cluster mappings.

#### Root Cause

The `dataSourceId` parameter was not being passed to the `fetchAutocompleteSettingsIfNeeded` function when saving settings. Without this parameter, the function would fail silently and not trigger the autocomplete refresh mechanism.

#### Code Changes

The fix modifies `src/plugins/console/public/application/containers/settings.tsx`:

1. Added `dataSourceId` parameter to `fetchAutocompleteSettingsIfNeeded` function signature
2. Added null check for `dataSourceId` before calling `retrieveAutoCompleteInfo`
3. Updated the `onSaveSettings` callback to pass `dataSourceId` to the function

```typescript
// Before (broken)
const onSaveSettings = (newSettings: DevToolsSettings) => {
  const prevSettings = settings.toJSON();
  fetchAutocompleteSettingsIfNeeded(http, settings, newSettings, prevSettings);
  // ...
};

// After (fixed)
const onSaveSettings = (newSettings: DevToolsSettings) => {
  const prevSettings = settings.toJSON();
  fetchAutocompleteSettingsIfNeeded(http, settings, newSettings, prevSettings, dataSourceId);
  // ...
};
```

### Affected Versions

- Observed in OpenSearch Dashboards 2.19 and 3.1
- Fixed in v3.4.0

## Limitations

- The fix requires a valid `dataSourceId` to be present for autocomplete refresh to work

## References

### Documentation
- [Dev Tools Documentation](https://docs.opensearch.org/3.0/dashboards/dev-tools/run-queries/): Running queries in the Dev Tools console

### Pull Requests
| PR | Description |
|----|-------------|
| [#10595](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10595) | Allow updating of console_polling through the UI |

### Issues (Design / RFC)
- [Issue #10544](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/10544): Bug report - Cannot update console_polling value through UI

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/opensearch-dashboards-dashboards-console.md)
