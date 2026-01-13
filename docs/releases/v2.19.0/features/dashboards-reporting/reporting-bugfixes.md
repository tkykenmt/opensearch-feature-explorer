---
tags:
  - dashboards-reporting
---
# Reporting Bug Fixes

## Summary

OpenSearch v2.19.0 includes bug fixes for the Dashboards Reporting plugin addressing markdown sanitization in report headers/footers, CSV report generation with nested fields, and notebooks reporting button rendering with Multi-Data Source (MDS) enabled.

## Details

### What's New in v2.19.0

#### Markdown Sanitization for Report Headers/Footers

The report header and footer markdown preview now sanitizes HTML content using DOMPurify. Previously, sanitization was only applied during report generation, but not during the create/edit preview. This ensures consistent security behavior across the UI.

**Technical Changes:**
- Added `createDOMPurify` import from `dompurify` package
- Applied `DOMPurify.sanitize()` to markdown preview in `generateMarkdownPreview` callback
- Affects both header and footer markdown editors in `report_settings.tsx`

#### CSV Report Generation with Nested Fields

Fixed an issue where CSV reports from saved searches were missing nested field values. The previous implementation only checked for fields with a dot (`.`) in their key names, ignoring fields containing arrays of objects.

**Root Cause:**
The `dataReportHelpers.ts` code handling nested fields only checked if fields had a key with a `.` in them, ignoring fields which had an array of objects.

**Technical Changes:**
- Updated `flattenHits()` function to properly handle nested objects
- Enhanced `traverse()` function to extract values from arrays of objects
- Added logic to flatten nested array objects into dot-notation keys (e.g., `products.price`, `customer.address.city`)

#### Notebooks Reporting Button with MDS

Fixed the notebooks reporting button to hide when Multi-Data Source (MDS) is enabled. The reporting actions button was incorrectly displayed even when MDS was active, which is not supported.

**Technical Changes:**
- Added `dataSourceMDSEnabled` state check to `showReportingContextMenu` condition
- Added `data-test-subj="reporting-actions-button"` for testing
- Added unit tests for both MDS enabled and disabled scenarios

## Limitations

- Nested field flattening in CSV reports may produce large column counts for deeply nested data structures
- Reporting functionality remains unavailable when MDS is enabled in notebooks

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [dashboards-reporting#476](https://github.com/opensearch-project/dashboards-reporting/pull/476) | Sanitize markdown when previewing report header/footer | |
| [dashboards-reporting#502](https://github.com/opensearch-project/dashboards-reporting/pull/502) | CSV report generation had missing nested fields | [#375](https://github.com/opensearch-project/dashboards-reporting/issues/375) |
| [dashboards-observability#2278](https://github.com/opensearch-project/dashboards-observability/pull/2278) | Updated notebooks reporting button render | |
