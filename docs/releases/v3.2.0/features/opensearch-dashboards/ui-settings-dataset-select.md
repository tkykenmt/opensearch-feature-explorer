# UI Settings & Dataset Select

## Summary

This release includes two bug fixes for OpenSearch Dashboards: improved robustness of the UI settings client when handling non-existent setting keys, and visual updates to the dataset selector component in the Explore feature.

## Details

### What's New in v3.2.0

#### UI Settings Client Robustness (PR #9927)

The `UiSettingsClient` has been made more robust to handle cases where a non-existent setting key is passed. Previously, accessing undefined keys could cause errors; now the client handles these cases gracefully.

**Key Changes:**
- `validateScope()` now defaults to an empty object when the key doesn't exist in cache
- `getUserProvidedWithScope()` uses optional chaining for the type property
- Removed unused `scope` parameter from `mergeSettingsIntoCache()` method
- Added unit tests to verify no errors are thrown for non-existent keys

```typescript
// Before: Could throw error if key doesn't exist
private validateScope(key: string, scope: UiSettingScope) {
  const definition = this.cache[key]; // undefined if key doesn't exist
  // ...
}

// After: Gracefully handles missing keys
private validateScope(key: string, scope: UiSettingScope) {
  const definition = this.cache[key] || {}; // Defaults to empty object
  // ...
}
```

#### Dataset Selector UI Update (PR #10344)

The dataset selector component in the Explore feature received visual improvements for better layout and readability.

**Visual Changes:**
- Removed fixed width constraints (was 300px)
- Added bold font weight to dataset title text
- Improved text wrapper alignment with flexbox
- Simplified icon styling by removing separate icon class
- Set max-width to 275px for text overflow handling

```scss
// Updated styles
.datasetSelect {
  &__textWrapper {
    align-items: center;
    margin-inline-end: $euiSizeXS;
    gap: $euiSizeXS;
  }

  &__text {
    text-align: left;
    white-space: nowrap;
    font-weight: $euiFontWeightBold;
    flex: 1;
    max-width: 275px;
    text-overflow: ellipsis;
    height: $euiSizeL;
    line-height: $euiSizeL;
    overflow: hidden;
  }
}
```

### Technical Changes

#### Modified Components

| Component | File | Change |
|-----------|------|--------|
| UiSettingsClient | `src/core/public/ui_settings/ui_settings_client.ts` | Added null-safe access patterns |
| DatasetSelect | `src/plugins/data/public/ui/dataset_select/dataset_select.tsx` | Updated CSS class names |
| Dataset Select Styles | `src/plugins/data/public/ui/dataset_select/_dataset_select.scss` | Improved layout styles |

## Limitations

- The UI settings client fix only addresses the public (browser-side) client; server-side behavior remains unchanged
- Dataset selector visual changes are specific to the Explore feature

## References

### Documentation
- [PR #9927](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9927): UI settings client robustness fix
- [PR #10344](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10344): Dataset selector UI update

### Pull Requests
| PR | Description |
|----|-------------|
| [#9927](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9927) | Make UI setting client more robust when the setting key does not exist |
| [#10344](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10344) | UI update for dataset select |
