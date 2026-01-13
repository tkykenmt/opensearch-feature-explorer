---
tags:
  - domain/search
  - component/dashboards
  - dashboards
  - search
---
# Search Relevance Dashboards Fixes

## Summary

This bugfix addresses a schema validation error in the Search Relevance Workbench that prevented users from creating query sets using sampling methods (pptss, random, topn). The POST Query Sets endpoint was missing the `querySetSize` parameter in its schema validation specification, causing a "Bad Request" error when users attempted to create query sets through the frontend.

## Details

### What's New in v3.1.0

Fixed the schema validation for the POST Query Sets endpoint by adding the missing `querySetSize` parameter to the request body validation schema.

### Technical Changes

#### Bug Description

When creating a query set in the Search Relevance Workbench frontend using sampling methods (`pptss`, `random`, `topn`), users encountered a 400 Bad Request error:

```
error: "Bad Request"
message: "[request body.querySetSize]: definition for this key is missing"
statusCode: 400
```

The root cause was that the server-side route validation schema for the POST `/api/relevancy/query_sets` endpoint did not include the `querySetSize` field, even though the frontend was sending this parameter in the request body.

#### Code Change

The fix adds `querySetSize` to the schema validation in `server/routes/search_relevance_route_service.ts`:

```typescript
router.post(
  {
    path: ServiceEndpoints.QuerySets,
    validate: {
      body: schema.object({
        name: schema.string(),
        description: schema.string(),
        sampling: schema.string(),
        querySetSize: schema.number(),  // Added in this fix
      }),
    },
  },
  backendAction('POST', BackendEndpoints.QuerySets)
);
```

### Affected Components

| Component | Description |
|-----------|-------------|
| `search_relevance_route_service.ts` | Server-side route definitions with schema validation |
| POST Query Sets endpoint | API endpoint for creating query sets with sampling methods |

### Impact

- Users can now successfully create query sets using all sampling methods (pptss, random, topn) through the Search Relevance Workbench UI
- No migration required - this is a pure bugfix with no breaking changes

## Limitations

- This fix only addresses the schema validation issue; the underlying query set creation functionality was already working correctly on the backend

## References

### Blog Posts
- [Blog: Taking your first steps towards search relevance](https://opensearch.org/blog/taking-your-first-steps-towards-search-relevance/): Introduction to Search Relevance Workbench

### Pull Requests
| PR | Description |
|----|-------------|
| [#542](https://github.com/opensearch-project/dashboards-search-relevance/pull/542) | Fix schema validation in POST Query Sets endpoint |

### Issues (Design / RFC)
- [Issue #541](https://github.com/opensearch-project/dashboards-search-relevance/issues/541): [BUG] Creating a query set with sampling methods throws an error

## Related Feature Report

- [Search Comparison feature documentation](../../../../features/dashboards-search-relevance/dashboards-search-relevance-search-comparison.md)
