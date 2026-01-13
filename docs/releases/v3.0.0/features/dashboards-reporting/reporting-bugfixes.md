---
tags:
  - domain/infra
  - component/dashboards
  - dashboards
---
# Reporting Bugfixes

## Summary

OpenSearch Dashboards Reporting v3.0.0 includes three bug fixes that improve the report generation experience. These fixes address issues with date range handling in report definitions and the positioning of the reporting popover UI.

## Details

### What's New in v3.0.0

This release fixes critical bugs in the Dashboards Reporting plugin that affected report generation and UI usability:

1. **Date Range Support**: Fixed an issue where absolute date ranges were incorrectly interpreted as relative to "now"
2. **Optional Time Parameters**: Made `timeFrom` and `timeTo` parameters optional to prevent errors when loading reports without time ranges
3. **Popover UI Positioning**: Fixed the reporting popover to use relative positioning instead of fixed positioning

### Technical Changes

#### Bug Fix 1: Date Range in Report Generation (PR #524)

**Problem**: When creating a report definition with an absolute time range (e.g., a specific date from a month ago), the generated PDF report would use a time interval relative to "now" instead of the specified absolute dates.

**Solution**: Updated the time picker component to correctly preserve and use absolute date ranges when generating reports.

**Affected Component**: Report definition creation and editing functionality

#### Bug Fix 2: Optional Time Parameters (PR #554)

**Problem**: Loading reports that did not have `timeFrom` and `timeTo` values would throw an error: "Error generating report".

**Solution**: Made the `timeFrom` and `timeTo` parameters optional in the report generation logic, allowing reports without explicit time ranges to load successfully.

**Affected Component**: Report loading and generation logic

#### Bug Fix 3: Reporting Popover UI (PR #570)

**Problem**: The reporting popover was set to a fixed position. When users scrolled down a dashboard and clicked the reporting button, the popover would appear at the top of the page (hidden from view) instead of near the button.

**Solution**: Changed the popover positioning from fixed to relative, ensuring it always opens correctly near the reporting button regardless of scroll position.

**Affected Component**: Reporting UI popover component

Additionally, this PR fixed a failing Cypress test that was looking for a non-existent nested span element.

### Usage Example

After these fixes, users can:

1. Create report definitions with absolute date ranges that are preserved correctly:
```
Time Range: Aug 1, 2024 00:00:00 to Aug 15, 2024 23:59:59
```

2. Load reports without time parameters without encountering errors

3. Access the reporting popover from any scroll position on a dashboard

## Limitations

- These fixes are specific to the OpenSearch Dashboards Reporting plugin
- The date range fix applies to new report definitions; existing definitions may need to be recreated

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/reporting/report-dashboard-index/): Reporting using OpenSearch Dashboards

### Pull Requests
| PR | Description |
|----|-------------|
| [#524](https://github.com/opensearch-project/dashboards-reporting/pull/524) | Support for date range in report generation |
| [#554](https://github.com/opensearch-project/dashboards-reporting/pull/554) | Updated optional parameters for timeFrom and timeTo |
| [#570](https://github.com/opensearch-project/dashboards-reporting/pull/570) | Reporting Popover UI fix |

### Issues (Design / RFC)
- [Issue #414](https://github.com/opensearch-project/dashboards-reporting/issues/414): Absolute date interval interpreted as relative to "now"
- [Issue #401](https://github.com/opensearch-project/dashboards-reporting/issues/401): Reporting UI issue (popover positioning)

## Related Feature Report

- Full feature documentation
