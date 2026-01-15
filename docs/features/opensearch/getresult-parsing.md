---
tags:
  - opensearch
---
# GetResult Parsing

## Summary

The `GetResult` class handles parsing of document retrieval responses in OpenSearch. It provides methods to parse JSON responses from Get API operations and construct result objects containing document data, metadata, and status information.

## Details

### Components

| Component | Description |
|-----------|-------------|
| `GetResult` | Core class for parsing and representing Get API responses |
| `fromXContentEmbedded()` | Static method to parse embedded GetResult from XContent |
| `fromXContent()` | Static method to parse standalone GetResult from XContent |

### Required Fields

The `found` field is required when parsing a GetResult. If missing, a `ParsingException` is thrown with the message "Missing required field [found]".

### Usage Example

```java
// Parsing a GetResult from JSON
try (XContentParser parser = JsonXContent.jsonXContent.createParser(
    NamedXContentRegistry.EMPTY,
    LoggingDeprecationHandler.INSTANCE,
    jsonString
)) {
    GetResult result = GetResult.fromXContent(parser);
    if (result.isExists()) {
        // Document found - process source
        Map<String, Object> source = result.getSourceAsMap();
    }
}
```

## Limitations

- The `found` field must be present in the JSON response; omitting it results in a `ParsingException`
- Cannot assume a default value for `found` as it would mask potential data issues

## Change History

- **v2.16.0** (2024-08-06): Fixed NPE when `found` field is missing - now throws descriptive `ParsingException`

## References

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#14552](https://github.com/opensearch-project/OpenSearch/pull/14552) | Handle NPE in GetResult if "found" field is missing |

### Issues

| Issue | Description |
|-------|-------------|
| [#14519](https://github.com/opensearch-project/OpenSearch/issues/14519) | Parsing a GetResult returns NPE if "found" field is missing |
