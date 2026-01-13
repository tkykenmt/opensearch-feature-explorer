---
tags:
  - domain/observability
  - component/dashboards
  - dashboards
  - indexing
---
# Anomaly Detection Dashboards Bugfixes

## Summary

Three bug fixes for the Anomaly Detection Dashboards plugin in v2.18.0 addressing issues with custom result index rendering, historical analysis execution, and preview functionality. These fixes improve the reliability of detector configuration and preview workflows.

## Details

### What's New in v2.18.0

This release includes three targeted bug fixes for the Anomaly Detection Dashboards plugin:

1. **Custom Result Index Session Rendering** - Fixed an issue where the custom result index section was not rendering correctly due to incorrect checkbox component usage.

2. **Historical Analysis and Custom Result Index** - Fixed two issues:
   - Wrong route path when running historical analysis
   - Custom result index field not resetting to `undefined` when disabled, causing validation errors on the create detector review page

3. **Preview Not Considering Rules and Imputation** - Fixed a bug where the anomaly preview did not account for suppression rules and imputation options when generating sample anomalies.

### Technical Changes

#### Custom Result Index Rendering Fix (PR #887)

Changed the checkbox component from `EuiCheckbox` to `EuiCompressedCheckbox` for proper rendering in the custom result index section:

```tsx
// Before
<EuiCheckbox
  id={'resultIndexConditionCheckbox'}
  ...
/>

// After
<EuiCompressedCheckbox
  id={'resultIndexConditionCheckbox'}
  ...
/>
```

#### Historical Analysis Route Fix (PR #889)

Fixed the URL construction for starting historical analysis with data source support:

```typescript
// Before (incorrect)
const baseUrl = `${AD_NODE_API.DETECTOR}/${detectorId}`;
const url = dataSourceId
  ? `${baseUrl}/${dataSourceId}/start`
  : `${baseUrl}/start`;

// After (correct)
const baseUrl = `${AD_NODE_API.DETECTOR}/${detectorId}/start`;
const url = dataSourceId ? `${baseUrl}/${dataSourceId}` : baseUrl;
```

#### Custom Result Index Reset Fix (PR #889)

Fixed the field reset behavior when disabling custom result index:

```typescript
// Before - caused validation error
form.setFieldValue('resultIndex', '');

// After - properly clears the field
form.setFieldValue('resultIndex', undefined);
```

#### Preview Rules and Imputation Fix (PR #898)

Extended the `prepareDetector` function to accept and pass imputation options and suppression rules to the preview:

```typescript
// Updated function signature
export function prepareDetector(
  featureValues: FeaturesFormikValues[],
  shingleSizeValue: number,
  categoryFields: string[],
  ad: Detector,
  forPreview: boolean = false,
  imputationOption?: ImputationFormikValues,  // New parameter
  suppressionRules?: RuleFormikValues[]       // New parameter
): Detector {
  // ...
  return {
    ...detector,
    imputationOption: formikToImputationOption(imputationOption),
    rules: formikToRules(suppressionRules),
  };
}
```

The `SampleAnomalies` component now passes these parameters when calling `prepareDetector`:

```typescript
prepareDetector(
  props.featureList,
  props.shingleSize,
  props.categoryFields,
  newDetector,
  true,
  props.imputationOption,      // Now passed
  props.suppressionRules,      // Now passed
);
```

### Files Changed

| PR | Files Modified |
|----|----------------|
| #887 | `CustomResultIndex.tsx` (checkbox component fix) |
| #889 | `CustomResultIndex.tsx` (field reset), `ad.ts` (route path) |
| #898 | `ConfigureModel.tsx`, `SampleAnomalies.tsx`, `helpers.ts` (preview parameters) |

## Limitations

- These fixes are specific to the Dashboards UI; backend anomaly detection functionality is unchanged
- The preview fix requires both imputation and suppression rules to be properly configured in the detector form

## References

### Documentation
- [Anomaly Detection Documentation](https://docs.opensearch.org/2.18/observing-your-data/ad/index/): Official documentation
- [Anomaly Detection Dashboards Plugin](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin): Source repository

### Pull Requests
| PR | Description |
|----|-------------|
| [#887](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/887) | Fix custom result index session not rendering issue |
| [#889](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/889) | Fix issues in running historical analysis and custom result index section |
| [#898](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/898) | Fix preview not considering rules and imputation options |

## Related Feature Report

- Full feature documentation
