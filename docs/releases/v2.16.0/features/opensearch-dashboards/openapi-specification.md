---
tags:
  - opensearch-dashboards
---
# OpenAPI Specification

## Summary

OpenSearch Dashboards v2.16.0 adds comprehensive OpenAPI specifications for the Saved Objects APIs and Index Patterns API. These specifications enable developers to understand and interact with Dashboards APIs using standard OpenAPI tooling like Swagger UI.

## Details

### What's New in v2.16.0

This release adds OpenAPI specification files (YAML format) documenting the following APIs:

#### Saved Objects APIs

| API | Method | Endpoint | Description |
|-----|--------|----------|-------------|
| Get | GET | `/api/saved_objects/{type}/{id}` | Retrieve a single saved object |
| Create | POST | `/api/saved_objects/{type}/{id}` | Create a new saved object |
| Find | GET | `/api/saved_objects/_find` | Search for saved objects |
| Bulk Get | POST | `/api/saved_objects/_bulk_get` | Retrieve multiple saved objects |
| Bulk Create | POST | `/api/saved_objects/_bulk_create` | Create multiple saved objects |
| Bulk Update | PUT | `/api/saved_objects/_bulk_update` | Update multiple saved objects |
| Update | PUT | `/api/saved_objects/{type}/{id}` | Update a saved object |
| Delete | DELETE | `/api/saved_objects/{type}/{id}` | Delete a saved object |
| Migrate | POST | `/api/saved_objects/_migrate` | Migrate saved objects |
| Import | POST | `/api/saved_objects/_import` | Import saved objects from file |
| Export | POST | `/api/saved_objects/_export` | Export saved objects to file |
| Resolve Import Errors | POST | `/api/saved_objects/_resolve_import_errors` | Resolve conflicts from import |

#### Index Patterns API

| API | Method | Endpoint | Description |
|-----|--------|----------|-------------|
| Get Fields | GET | `/api/index_patterns/_fields_for_wildcard` | Retrieve fields for index pattern |

### Technical Changes

The OpenAPI specifications are stored in the `docs/openapi/` directory within the OpenSearch Dashboards repository:
- `docs/openapi/saved_objects/` - Saved Objects API specifications
- `docs/openapi/index_patterns/` - Index Patterns API specifications

Each specification includes:
- Request/response schemas with detailed field descriptions
- Example payloads for common operations (index patterns, visualizations, dashboards)
- Error response definitions
- Query parameter documentation

### Usage

To view the API documentation locally:

```bash
cd docs/openapi/saved_objects
npx serve
# Open http://localhost:3000 in browser
```

The specifications can be used with:
- Swagger UI for interactive API exploration
- Code generation tools for client SDKs
- API testing tools
- Documentation generators

## Limitations

- Specifications cover Saved Objects and Index Patterns APIs only; other Dashboards APIs are not yet documented
- Tooling for bundling specifications is not yet available
- Linting and validation for specifications is planned but not implemented

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6799](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6799) | Add OpenAPI specification for GET and CREATE saved object APIs | [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) |
| [#6855](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6855) | Add examples for saved object creation (index pattern, vega, dashboards) | [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) |
| [#6856](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6856) | Add OpenAPI doc for saved_object find API | [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) |
| [#6859](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6859) | Add OpenAPI specification for bulk create and bulk update APIs | [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) |
| [#6860](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6860) | Add OpenAPI specification for bulk_get API | [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) |
| [#6864](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6864) | Add OpenAPI specification for update, delete and migrate APIs | [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) |
| [#6872](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6872) | Add OpenAPI specification for import and export APIs | [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) |
| [#6885](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6885) | Add OpenAPI specifications for resolve import errors API | [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) |
| [#7270](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7270) | Add OpenAPI specification for index pattern fields API | - |

### Issues

- [#6719](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6719) - [Proposal] OpenAPI specifications for dashboards APIs
