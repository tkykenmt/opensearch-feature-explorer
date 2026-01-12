# Pipeline ID Limits

## Summary

OpenSearch v3.0.0 introduces a 512-byte limit for both ingest pipeline and search pipeline IDs. This validation prevents excessively long pipeline identifiers that could cause issues with cluster state management and storage.

## Details

### What's New in v3.0.0

Prior to this change, there was no validation on pipeline ID length, allowing users to create pipelines with arbitrarily long identifiers. This could lead to:
- Excessive cluster state size
- Potential storage and memory issues
- Difficulty in managing and referencing pipelines

The new validation enforces a maximum of 512 UTF-8 bytes for pipeline IDs in both:
- **Ingest pipelines** (used for document transformation during indexing)
- **Search pipelines** (used for query/response transformation during search)

### Technical Changes

#### Validation Logic

The validation uses Lucene's `UnicodeUtil.calcUTF16toUTF8Length()` to accurately calculate the UTF-8 byte length of pipeline IDs, ensuring proper handling of multi-byte characters.

```java
private static final int MAX_PIPELINE_ID_BYTES = 512;

int pipelineIdLength = UnicodeUtil.calcUTF16toUTF8Length(
    request.getId(), 0, request.getId().length()
);

if (pipelineIdLength > MAX_PIPELINE_ID_BYTES) {
    throw new IllegalArgumentException(
        String.format(
            Locale.ROOT,
            "Pipeline id [%s] exceeds maximum length of %d UTF-8 bytes (actual: %d bytes)",
            request.getId(),
            MAX_PIPELINE_ID_BYTES,
            pipelineIdLength
        )
    );
}
```

#### Modified Components

| Component | File | Description |
|-----------|------|-------------|
| IngestService | `server/src/main/java/org/opensearch/ingest/IngestService.java` | Validates ingest pipeline ID length |
| SearchPipelineService | `server/src/main/java/org/opensearch/search/pipeline/SearchPipelineService.java` | Validates search pipeline ID length |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| MAX_PIPELINE_ID_BYTES | Maximum allowed UTF-8 bytes for pipeline ID | 512 |

### Usage Example

```json
// Valid pipeline ID (within 512 bytes)
PUT _ingest/pipeline/my-ingest-pipeline
{
  "description": "A sample ingest pipeline",
  "processors": [
    {
      "set": {
        "field": "processed",
        "value": true
      }
    }
  ]
}

// Response: HTTP/1.1 200 OK
// {"acknowledged":true}
```

```json
// Invalid pipeline ID (exceeds 512 bytes)
PUT _ingest/pipeline/very-long-pipeline-id-that-exceeds-512-bytes...

// Response: HTTP/1.1 400 Bad Request
// {
//   "error": {
//     "type": "illegal_argument_exception",
//     "reason": "Pipeline id [...] exceeds maximum length of 512 UTF-8 bytes (actual: 513 bytes)"
//   }
// }
```

### Migration Notes

If you have existing pipelines with IDs longer than 512 bytes:
1. Create new pipelines with shorter IDs
2. Update any index settings or templates referencing the old pipeline IDs
3. Delete the old pipelines

Note: Existing pipelines with long IDs will continue to work, but you cannot update them without first renaming to a compliant ID.

## Limitations

- The limit is fixed at 512 bytes and is not configurable
- The validation is based on UTF-8 byte length, not character count (multi-byte characters consume more of the limit)
- Existing pipelines with non-compliant IDs are not automatically migrated

## References

### Documentation
- [Ingest Pipeline Documentation](https://docs.opensearch.org/3.0/ingest-pipelines/create-ingest/): Official docs for creating ingest pipelines
- [Search Pipeline Documentation](https://docs.opensearch.org/3.0/search-plugins/search-pipelines/creating-search-pipeline/): Official docs for creating search pipelines

### Pull Requests
| PR | Description |
|----|-------------|
| [#17786](https://github.com/opensearch-project/OpenSearch/pull/17786) | Introduce 512 byte limit to search and ingest pipeline IDs |

### Issues (Design / RFC)
- [Issue #17766](https://github.com/opensearch-project/OpenSearch/issues/17766): Original bug report for weak validation

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/pipeline-id-limits.md)
