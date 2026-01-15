---
tags:
  - opensearch
---
# Alias API Validation

## Summary

This release fixes a bug in the Create or Update Alias API (`PUT _alias/{alias}`) where unsupported parameters in the request body were silently ignored instead of throwing an exception. Additionally, the `is_hidden` parameter was not being parsed correctly.

## Details

### What's New in v2.16.0

The Create or Update Alias API now properly validates request body parameters and throws an `IllegalArgumentException` when unknown fields are encountered.

### Technical Changes

The fix was implemented in `RestIndexPutAliasAction.java`:

1. **Unknown field validation**: Added exception throwing for unrecognized fields in the request body
2. **`is_hidden` parameter support**: Added parsing logic for the `is_hidden` parameter that was previously omitted

```java
// Now throws exception for unknown fields
} else {
    throw new IllegalArgumentException("unknown field [" + currentFieldName + "]");
}
```

### Supported Request Body Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `index` | String | Index name (overrides URL path) |
| `alias` | String | Alias name (overrides URL path) |
| `filter` | Object | Filter for the alias |
| `routing` | String | Custom routing value |
| `index_routing` | String | Custom routing for index operations |
| `search_routing` | String | Custom routing for search operations |
| `is_write_index` | Boolean | Whether this is the write index |
| `is_hidden` | Boolean | Whether the alias is hidden (newly supported) |

### API Endpoints

The fix applies to all Create or Update Alias API endpoints:
- `PUT /{index}/_alias/{name}`
- `POST /{index}/_alias/{name}`
- `PUT /{index}/_aliases/{name}`
- `PUT /_alias/{name}`
- `PUT /_aliases/{name}`

## Limitations

- The `is_hidden` parameter test is skipped for versions prior to 3.0.0 in the REST API spec tests

## References

### Documentation
- [Create or Update Alias API](https://docs.opensearch.org/2.16/api-reference/index-apis/update-alias/)

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14719](https://github.com/opensearch-project/OpenSearch/pull/14719) | Fix create or update alias API doesn't throw exception for unsupported parameters | [#14384](https://github.com/opensearch-project/OpenSearch/issues/14384) |
