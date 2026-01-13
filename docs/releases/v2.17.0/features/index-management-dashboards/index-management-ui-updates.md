---
tags:
  - domain/data
  - component/dashboards
  - dashboards
  - indexing
  - neural-search
---
# Index Management UI Updates

## Summary

OpenSearch v2.17.0 introduces comprehensive UI/UX improvements to the Index Management Dashboards plugin. These changes implement the "Look and Feel" and "Fit and Finish" design guidelines across all Index Management pages, providing a more consistent, modern, and user-friendly experience.

## Details

### What's New in v2.17.0

This release includes 13 PRs focused on UI consistency and usability improvements across all Index Management pages:

- **Navigation Redesign**: Reordered features and updated titles/descriptions in the left navigation panel
- **Notification Modal**: Added notification modal on the Indexes page for better user feedback
- **Visual Consistency**: Applied consistent styling across ISM, Snapshots, Data Streams, Rollups, Transforms, Aliases, and Templates pages
- **MDS Support**: Added Multi-Data Source (MDS) support to the Shrink page
- **Bug Fixes**: Fixed history navigation issues in Rollups and Transform job pages

### Technical Changes

#### UI Components Updated

| Page | Changes |
|------|---------|
| Indexes | Notification modal, fit and finish styling |
| ISM Policies | Look and feel changes, smaller buttons, compressed bars |
| Composable Templates | Fit and finish styling |
| Aliases | Fit and finish styling |
| Policy Managed Indices | Fit and finish styling |
| Data Streams | Semantic headers, EuiPanel padding |
| Rollups | Semantic headers, job count in title, history navigation fix |
| Transforms | Fit and finish styling, job count in title, history navigation fix |
| Snapshot Management | Consistency and density improvements |
| Snapshot Policies | Fit and finish styling |
| Snapshot Repositories | Fit and finish styling |
| Notification Settings | Look and feel changes |

#### Design Guidelines Applied

| Guideline | Implementation |
|-----------|----------------|
| Typography | Small font size as standard paragraph text |
| Headers | Semantic headers (H1 on main pages, H2 on modals/flyouts) |
| Icons | Plus icons for create, PlusInCircle for add actions |
| Buttons | Small button size, compressed action bars |
| Layout | EuiPanel for consistent padding across content |
| Density | Improved information density |

### Usage Example

The UI changes are automatically applied when accessing Index Management in OpenSearch Dashboards:

1. Navigate to **OpenSearch Plugins** → **Index Management**
2. Select any page (Indices, Policies, Rollups, etc.)
3. Experience the updated, consistent UI

### Migration Notes

No migration required. UI changes are applied automatically upon upgrading to v2.17.0.

## Limitations

- UI changes are cosmetic and do not affect underlying functionality
- Some pages may require browser cache clearing to display updated styles

## References

### Documentation
- [Index Management Documentation](https://docs.opensearch.org/2.17/dashboards/im-dashboards/index/)
- [Snapshot Management Documentation](https://docs.opensearch.org/2.17/dashboards/sm-dashboards/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1106](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1106) | Reorder features and rename title/description in left navigation |
| [#1123](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1123) | Look and feel changes in ISM pages |
| [#1132](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1132) | Look and feel changes for snapshots, datastreams, rollups, notification settings |
| [#1141](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1141) | MDS support in Shrink page, bug fixes |
| [#1143](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1143) | Add notification modal on Indexes page |
| [#1148](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1148) | Consistency and density changes for Snapshot Management |
| [#1150](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1150) | Fit and finish for ISM policy & Composable template pages |
| [#1153](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1153) | Fit and finish for DataStreams and Rollups |
| [#1154](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1154) | Fit and finish for Indexes and Transform pages |
| [#1155](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1155) | Fit and finish for Aliases, Templates, Policy managed Indices |
| [#1157](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1157) | Fit and finish for Snapshot Management pages |
| [#1164](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1164) | Update rollup/transform jobs title with total numbers |
| [#1166](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1166) | Fix history navigation bugs in rollups and transform pages |

## Related Feature Report

- Full feature documentation
