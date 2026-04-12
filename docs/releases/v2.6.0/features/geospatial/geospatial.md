---
tags:
  - geospatial
---
# Geospatial

## Summary

OpenSearch 2.6.0 introduces 2 new feature(s) and 0 enhancement(s) to Geospatial, along with 3 bug fixes.

## Details

### New Features

- **Add limit to geojson upload API**: Upload API will limit number of features to be uploaded to 10_000. Since custom vector map will allow 10K documents to be fetched, we will add same constraint while upload for consistency .
- **Allow API to accept any index name without suffix**: Maps will support add import GeoJSON into an index. This will be used by more layers like document, cluster. The restriction was previously added since it was mainly used as Custom Vector map. This change is already incorporated by front end.

### Bug Fixes

- Upgrade snapshot version to 2.6 for 2.x
- Fix compilation error and test failure
- Replace Locale.getDefault() with Local.ROOT

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#218](https://github.com/opensearch-project/geospatial/pull/218) | Add limit to geojson upload API | geospatial |
| [#182](https://github.com/opensearch-project/geospatial/pull/182) | Allow API to accept any index name without suffix | geospatial |
| [#208](https://github.com/opensearch-project/geospatial/pull/208) | Upgrade snapshot version to 2.6 for 2.x | geospatial |
| [#210](https://github.com/opensearch-project/geospatial/pull/210) | Fix compilation error and test failure | geospatial |
| [#214](https://github.com/opensearch-project/geospatial/pull/214) | Replace Locale.getDefault() with Local.ROOT | geospatial |
