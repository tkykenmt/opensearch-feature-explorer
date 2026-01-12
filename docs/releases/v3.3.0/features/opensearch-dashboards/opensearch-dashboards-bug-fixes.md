# OpenSearch Dashboards Bug Fixes

## Summary

OpenSearch Dashboards v3.3.0 includes 25 bug fixes addressing issues across visualizations, Discover/Explore, workspaces, and UI components. Key improvements include fixes for Vega visualization data URLs and tooltip behavior, saved search state synchronization, chart axis title updates, banner persistence, table visualization pagination, and workspace URL handling.

## Details

### What's New in v3.3.0

This release focuses on stability and user experience improvements across multiple Dashboards components.

### Technical Changes

#### Visualization Fixes

| Area | Fix | PR |
|------|-----|-----|
| Vega | Data URL with signal not working | [#10339](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10339) |
| Vega | Tooltip flashing when mouse moves | [#10467](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10467) |
| Charts | Axis titles not updating after field switch | [#10316](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10316) |
| Charts | Tooltip date format not dynamic | [#10358](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10358) |
| Table | Max row per page not working in dashboard | [#10420](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10420) |
| Table | Max row per page allows values < 1 | [#10420](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10420) |
| Gauge | Added gauge visualization support | [#10451](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10451) |

#### Discover/Explore Fixes

| Area | Fix | PR |
|------|-----|-----|
| Saved Search | Query not applied with snapshot URL | [#10357](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10357) |
| Saved Search | Query reset to empty after saving | [#10357](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10357) |
| Query Editor | Error highlighting after language switch | [#10363](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10363) |
| Dataset | Legacy state not reset when switching | [#10366](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10366) |
| Dataset | Advanced selector ignores language config | [#10368](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10368) |
| Visualization | Empty state uses incorrect PPL | [#10365](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10365) |
| Field Selector | Functional issues with patterns | [#10394](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10394) |
| Index Selector | Shows when not needed | [#10400](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10400) |
| Value Suggestions | Columns with @ and . not working | [#10408](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10408) |
| Traces | Span redirection and hover fixes | [#10479](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10479) |

#### UI/UX Fixes

| Area | Fix | PR |
|------|-----|-----|
| Banner | Dismissal not persisting across reloads | [#10325](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10325) |
| Workspace | Global search URL incorrect | [#10414](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10414) |
| UI Settings | Remaining fixes | [#10410](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10410) |
| Console | Warn and error messages updated | [#10430](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10430) |
| Data Importer | Moved to Data Administration | [#10478](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10478) |
| Editor | Extra empty space and horizontal scroll | [#10486](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10486) |
| Gauge/Metric | Added units panel | [#10497](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10497) |
| Correlation | Entities field dynamic array fix | [#10403](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10403) |

### Key Improvements

#### Banner Persistence
The banner plugin now uses `sessionStorage` to persist dismissal state across page reloads within the same session. Previously, dismissed banners would reappear after refreshing the page.

#### Vega Visualization
- Fixed data URL with signal expressions not working properly
- Resolved tooltip flashing issue when moving the mouse over chart elements

#### Saved Search State Sync
Fixed issues where:
- Updated queries were not properly applied when loading a saved search via snapshot URL
- Queries would reset to empty after saving a saved search

#### Chart Axis Titles
Standardized axis title behavior across bar, line, and area charts. After switching x-axis and y-axis fields, the axis titles now correctly update to reflect the new field names.

#### Dynamic Tooltip Date Format
Chart tooltips now automatically determine the appropriate time unit (seconds, minutes, days) based on the actual timestamp values in the dataset.

#### Workspace URL Handling
Fixed global search URL handling within workspaces by correctly handling client base paths when formatting URLs with workspace IDs.

## Limitations

- Banner dismissal persists only for the current browser session (cleared when browser closes)
- Some fixes are specific to the new Explore interface

## References

### Documentation
- [OpenSearch Dashboards Repository](https://github.com/opensearch-project/OpenSearch-Dashboards)

### Pull Requests
| PR | Description |
|----|-------------|
| [#10316](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10316) | Standardize axis title behavior |
| [#10325](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10325) | Banner dismissal persistence |
| [#10339](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10339) | Vega data URL with signal |
| [#10357](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10357) | Saved search state sync |
| [#10358](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10358) | Dynamic tooltip date format |
| [#10363](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10363) | Error highlighting after language switch |
| [#10365](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10365) | Discover visualization empty state |
| [#10366](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10366) | Reset legacy state on dataset switch |
| [#10368](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10368) | Advanced dataset selector language config |
| [#10394](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10394) | Patterns field selector |
| [#10400](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10400) | Index selector visibility |
| [#10403](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10403) | Correlation entities field |
| [#10408](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10408) | Value suggestions for special characters |
| [#10410](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10410) | UI settings fixes |
| [#10414](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10414) | Global search URL in workspace |
| [#10420](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10420) | Table viz max row per page |
| [#10430](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10430) | Console warn/error messages |
| [#10451](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10451) | Add gauge visualization |
| [#10467](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10467) | Vega tooltip flashing |
| [#10478](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10478) | Data Importer location |
| [#10479](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10479) | Traces span redirection and hover |
| [#10486](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10486) | Editor spacing and scroll |
| [#10497](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10497) | Gauge/metric units panel |
