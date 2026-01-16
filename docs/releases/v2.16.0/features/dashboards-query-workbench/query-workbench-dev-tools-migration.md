---
tags:
  - dashboards-query-workbench
---
# Query Workbench Dev Tools Migration

## Summary

OpenSearch Dashboards v2.16.0 migrates Query Workbench from the OpenSearch Plugins menu to the Dev Tools section as part of the navigation changes planned for this release. This improves the organization of developer-focused tools within the Dashboards interface.

## Details

### What's New in v2.16.0

#### Navigation Change
Query Workbench has been moved from `OpenSearch Plugins > Query Workbench` to `Management > Dev Tools`. This change aligns Query Workbench with other developer tools and improves the overall navigation structure.

**Previous location:** OpenSearch Plugins > Query Workbench
**New location:** Management > Dev Tools

#### MDS Data Source Integration
The migration includes updates to how the selected MDS (Multiple Data Sources) data connection ID is passed, ensuring Dev Tools correctly finds and connects to data sources.

### Technical Changes

| Change | Description |
|--------|-------------|
| Navigation category | Changed from `opensearchPlugins` to `devTools` |
| Data source handling | Updated `selectedMDSDataConnectionId` passing mechanism |
| MDS compatibility | Maintained full MDS functionality in new location |
| Flint integration | Preserved Apache Spark/Flint data source support |

## Limitations

- Users familiar with the previous location will need to navigate to the new Dev Tools location
- Bookmarks or saved links to the old location may need to be updated

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#349](https://github.com/opensearch-project/dashboards-query-workbench/pull/349) | Moving Query Workbench to Dev Tools | [#348](https://github.com/opensearch-project/dashboards-query-workbench/issues/348) |

### Documentation
- [Query Workbench Documentation](https://docs.opensearch.org/2.16/dashboards/query-workbench/)
- [Dev Tools Documentation](https://docs.opensearch.org/2.16/dashboards/dev-tools/index-dev/)
