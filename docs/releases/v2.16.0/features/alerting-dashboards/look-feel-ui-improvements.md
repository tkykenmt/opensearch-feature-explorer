---
tags:
  - alerting-dashboards
---
# Look & Feel UI Improvements

## Summary

OpenSearch Alerting Dashboards v2.16.0 introduces comprehensive UI consistency improvements as part of the "Look & Feel" initiative. These changes standardize typography, tab sizing, and helper text across the alerting experience to align with OpenSearch Dashboards design guidelines.

## Details

### What's New in v2.16.0

The Look & Feel improvements in v2.16.0 focus on visual consistency and user experience refinements:

#### Standard Paragraph Size
- Updated inline styling for fonts to use `<EuiText size="s">` for theme compatibility
- Standardized paragraph/freeform text to have denser look using `EuiText size="s"`
- Preserved `size="xs"` for elements already using extra-small text

#### Semantic Headers
- Refactored page, modal, and flyout components to use semantic headers
- Main pages use H1 headers under `<EuiText size="s">`
- Secondary experiences (modals/flyouts) use H2 headers under `<EuiText size="s">`
- Improved accessibility through proper heading hierarchy

#### Small EuiTabs
- Standardized `EuiTabs` and `EuiTabbedContent` to use small size across the alerting plugin
- Consistent tab appearance throughout the monitor and alert management interfaces

#### Pattern Guidance
- Applied missing pattern guidance to the Alerting experience
- Improved visual consistency with other OpenSearch Dashboards plugins

#### Helper Text Sizing
- Adjusted helper text size across the monitor page
- Consistent text sizing for form field descriptions and guidance

## Limitations

- Some styling changes may require snapshot test updates
- Theme-specific font sizes may vary between Next and V7 themes

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#992](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/992) | Use standard paragraph size |
| [#994](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/994) | Use semantic header with correct size for page, modal and flyout |
| [#997](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/997) | Use small EuiTabs across the board |
| [#1004](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1004) | Apply missing pattern guidance to Alerting experience |
| [#1012](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1012) | Adjust helper text size across monitor page |
