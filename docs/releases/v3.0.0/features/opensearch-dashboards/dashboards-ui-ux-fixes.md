# Dashboards UI/UX Fixes

## Summary

OpenSearch Dashboards v3.0.0 includes a collection of UI/UX bug fixes and improvements that enhance the overall user experience. These fixes address issues across multiple areas including navigation, query editor, data source management, Discover panel, and dependency modernization.

## Details

### What's New in v3.0.0

This release includes 13 bug fixes and improvements across the Dashboards UI:

#### Navigation & Workspace Fixes
- Fixed left navigation menu staying in "Settings and Setup" when opening visualizations from asset relationships
- Moved sample data to the correct "Settings and Setup" category instead of "Custom"
- Fixed dataset selector flashing issue in Discover panel

#### Query Editor Improvements
- Updated query editor loading UI with immediate spinner display and progress bar
- Fixed suggestions popup not closing after query submission with Enter key

#### Data Source Management Fixes
- Fixed issue with adding sample data to data sources (Content-Length header type error)
- Fixed AWS SigV4 signature mismatch for special characters in query parameters
- Copied essential properties to generated requests for proper request handling
- Updated data source details tabs to use small buttons for better UI consistency

#### Discover Panel Fixes
- Fixed single document page content padding
- Made histogram colors match the current theme

#### Dependency Modernization
- Replaced `@elastic/filesaver` with `file-saver` library
- Replaced custom `formatNumWithCommas` utility with native `toLocaleString()`

### Technical Changes

#### Navigation Fix
The workspace navigation was incorrectly categorizing items when workspace was disabled. The fix ensures:
- Visualizations opened from asset relationships display in the correct nav group
- Sample data appears under "Settings and Setup" instead of "Custom"

#### Data Source Connector Fixes
Two critical fixes for AWS-hosted OpenSearch connections:

1. **Content-Length Header Fix**: The `Content-Length` header was being set as a numeric value instead of a string, causing AWS SigV4 signature verification to fail when calling `.trim()` on header values.

```javascript
// Before (caused error)
request.headers['Content-Length'] = body.length;

// After (fixed)
request.headers['Content-Length'] = body.length.toString();
```

2. **Query Parameter Encoding**: Special characters (`*`, `?`) in query parameters caused signature mismatches. The fix properly parses query parameters and encodes special characters per RFC3986.

#### Query Editor Loading UX
- Spinner now shows immediately when query starts
- Time elapsed text appears after 3 seconds
- Added progress bar in query editor
- Updated loading text font styling

## Limitations

- These are incremental UI fixes; no new features are introduced
- Some fixes are specific to workspace-disabled mode

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#9665](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9665) | Fix workspace disabled navigation issues |
| [#9666](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9666) | Close suggestions after query submission |
| [#9668](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9668) | Fix dataset selector flashing |
| [#9674](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9674) | Copy essential property to generated request |
| [#9676](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9676) | Fix sample data to data source issue |
| [#9678](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9678) | Fix query params signer error |
| [#9344](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9344) | Update query editor loading UI |
| [#9382](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9382) | Fix single document page padding |
| [#9405](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9405) | Make histogram color match theme |
| [#9484](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9484) | Replace @elastic/filesaver with file-saver |
| [#9488](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9488) | Replace formatNumWithCommas with toLocaleString |
| [#9057](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9057) | Update data source details to use small buttons |

### Issues (Design / RFC)
- [Issue #9474](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9474): Dataset selector flashing issue
- [Issue #9673](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9673): Essential property copy issue
- [Issue #9679](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9679): Query params signer error
- [Issue #9341](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9341): Remove @elastic/filesaver

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/dashboards-ui-ux-fixes.md)
