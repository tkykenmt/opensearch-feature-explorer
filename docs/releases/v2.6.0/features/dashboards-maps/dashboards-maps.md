---
tags:
  - dashboards-maps
---
# Dashboards Maps

## Summary

OpenSearch 2.6.0 introduces 2 new feature(s) and 6 enhancement(s) to Dashboards Maps, along with 5 bug fixes.

## Details

### New Features

- **Add map as embeddable to dashboard**: Allow user to add maps to dashboard.  This PR contains: * Maps embeddable api * Refactor maps component to adapt embeddable * Saved map can be added and displayed to dashboards * Register maps into visualization entrypoint * Editing map can be saved and return to dashboard * Time range in dashboard 
- **Add maps saved object for sample datasets**: This PR includes the changes which adds the dashboards-maps saved object to the existing sample dataset. When the user install a sample dataset then in the dashboards-maps panel, we can see a default saved map which will help maps users to explore maps with that dataset instead of creating a new map

### Enhancements

- **Fix popup display while zoomed out**
- **Limit max number of layers**
- **Add close button to tooltip hover**
- **Add scroll bar when more layers added**
- **Align items in add new layer modal**
- **Add indexPatterns to map embeddable output for dashboard filters**

### Bug Fixes

- Force resolve glob-parent and debug libraries
- Fix custom layer render opacity config
- [Cypress fix] Wait map saved before open maps listing
- Refactor add layer operations
- Refactor layer operations

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#231](https://github.com/opensearch-project/dashboards-maps/pull/231) | Add map as embeddable to dashboard | dashboards-maps |
| [#240](https://github.com/opensearch-project/dashboards-maps/pull/240) | Add maps saved object for sample datasets | dashboards-maps |
| [#226](https://github.com/opensearch-project/dashboards-maps/pull/226) | Fix popup display while zoomed out | dashboards-maps |
| [#216](https://github.com/opensearch-project/dashboards-maps/pull/216) | Limit max number of layers | dashboards-maps |
| [#263](https://github.com/opensearch-project/dashboards-maps/pull/263) | Add close button to tooltip hover | dashboards-maps |
| [#254](https://github.com/opensearch-project/dashboards-maps/pull/254) | Add scroll bar when more layers added | dashboards-maps |
| [#256](https://github.com/opensearch-project/dashboards-maps/pull/256) | Align items in add new layer modal | dashboards-maps |
| [#272](https://github.com/opensearch-project/dashboards-maps/pull/272) | Add indexPatterns to map embeddable output for dashboard filters | dashboards-maps |
| [#158](https://github.com/opensearch-project/dashboards-maps/pull/158) | Force resolve glob-parent and debug libraries | dashboards-maps |
| [#289](https://github.com/opensearch-project/dashboards-maps/pull/289) | Fix custom layer render opacity config | dashboards-maps |
| [#218](https://github.com/opensearch-project/dashboards-maps/pull/218) | [Cypress fix] Wait map saved before open maps listing | dashboards-maps |
| [#222](https://github.com/opensearch-project/dashboards-maps/pull/222) | Refactor add layer operations | dashboards-maps |
| [#224](https://github.com/opensearch-project/dashboards-maps/pull/224) | Refactor layer operations | dashboards-maps |
