---
tags:
  - domain/core
  - component/dashboards
  - dashboards
  - search
---
# Dashboards Maintenance

## Summary

This release includes routine maintenance updates for OpenSearch Dashboards: a version bump from 2.17.0 to 2.18.0 following the 2.17 release, and cleanup of the enhanced search API including removal of unused services and improved error handling.

## Details

### What's New in v2.18.0

#### Version Bump Post 2.17 Release
- Updated `package.json` version from `2.17.0` to `2.18.0`
- Standard post-release version increment on the 2.x branch

#### Enhanced Search API Cleanup
The Discover plugin's enhanced search functionality received significant cleanup:

1. **Deleted ConnectionsService**: Removed the unused `connections_service.ts` that was no longer needed
2. **Removed dataframe from requests**: Eliminated the `df` (dataframe) object being passed into search requests
3. **Deleted unused APIs**: Removed deprecated server routes:
   - Removed `GET /api/enhancements/datasource/external` endpoint
   - Removed `GET /api/enhancements/{queryId}` and `GET /api/enhancements/{queryId}/{dataSourceId}` routes
4. **Improved error handling**: Added proper error handling for 404/400 responses when fetching data connections
5. **API path consolidation**: Simplified API paths:
   - `datasource/jobs` → `jobs`
   - `datasource/connections` → `connections`

#### UI Text Updates
- Changed "Local Cluster" to "Default Cluster" for local data source display
- Changed column header from "Cluster" to "Clusters" for data source selection

### Technical Changes

#### Removed Components
| Component | Description |
|-----------|-------------|
| `ConnectionsService` | Unused service for managing data source connections |
| `ConnectionsServiceDeps` | Type definition for ConnectionsService dependencies |
| `df` parameter | Dataframe object in search request body |

#### API Changes
| Old Path | New Path | Change |
|----------|----------|--------|
| `/api/enhancements/datasource/external` | Removed | Endpoint deleted |
| `/api/enhancements/datasource/jobs` | `/api/enhancements/jobs` | Path simplified |
| `/api/enhancements/datasource/connections` | `/api/enhancements/connections/{id?}` | Path simplified, optional ID |

#### Modified Files
| File | Change |
|------|--------|
| `package.json` | Version 2.17.0 → 2.18.0 |
| `src/plugins/data/common/constants.ts` | "Local Cluster" → "Default Cluster" |
| `src/plugins/data/public/query/query_string/dataset_service/lib/index_type.ts` | "Cluster" → "Clusters" |
| `src/plugins/query_enhancements/common/constants.ts` | API path updates |
| `src/plugins/query_enhancements/public/datasets/s3_type.ts` | Updated fetch calls, added abort controllers |
| `src/plugins/query_enhancements/server/routes/data_source_connection/routes.ts` | Consolidated routes, added error handling |
| `src/plugins/query_enhancements/server/routes/index.ts` | Removed deprecated routes |

## Limitations

- These are internal maintenance changes with no user-facing feature impact
- The API path changes may affect custom integrations using the old endpoints

## References

### Documentation
- [PR #8225](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8225): Version bump
- [PR #8226](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8226): API cleanup

### Pull Requests
| PR | Description |
|----|-------------|
| [#8225](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8225) | Post 2.17 version bump to 2.18.0 |
| [#8226](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8226) | Clean up enhanced search API |

## Related Feature Report

- Full feature documentation
