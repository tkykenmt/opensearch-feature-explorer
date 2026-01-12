# Indexing Buffer Fix

## Summary

This breaking change fixes a long-standing bug where the `total_indexing_buffer_in_bytes` and `total_indexing_buffer` fields in the Nodes Info API response were swapped. The fix corrects the field formats so that `total_indexing_buffer_in_bytes` displays raw bytes and `total_indexing_buffer` displays human-readable format.

## Details

### What's New in v3.0.0

The Nodes Info API response now correctly formats the indexing buffer fields:

- `total_indexing_buffer_in_bytes`: Raw byte count (e.g., `53687091`)
- `total_indexing_buffer`: Human-readable format (e.g., `51.1mb`)

Previously, these values were reversed, which was inconsistent with other human-readable byte fields in OpenSearch APIs.

### Technical Changes

#### Bug Origin

The bug was introduced over 8 years ago when two explicit fields were merged to use the `humanReadableField` XContentBuilder method. The parameters to `byteSizeField` were accidentally swapped:

```java
// Before (incorrect)
builder.humanReadableField("total_indexing_buffer", "total_indexing_buffer_in_bytes", nodeInfo.getTotalIndexingBuffer());

// After (correct)
builder.humanReadableField("total_indexing_buffer_in_bytes", "total_indexing_buffer", nodeInfo.getTotalIndexingBuffer());
```

#### Changed Files

| File | Change |
|------|--------|
| `NodesInfoResponse.java` | Fixed parameter order in `humanReadableField()` call |
| `50_nodes_total_indexing_buffer_format.yml` | Added REST API test to verify correct formats |

### Usage Example

Before v3.0.0 (incorrect):
```json
GET /_nodes?human&filter_path=nodes.*.total_indexing_buffer*

{
  "nodes": {
    "741KuezCTUaGy0RDV7oxEA": {
      "total_indexing_buffer_in_bytes": "51.1mb",
      "total_indexing_buffer": 53687091
    }
  }
}
```

After v3.0.0 (correct):
```json
GET /_nodes?human&filter_path=nodes.*.total_indexing_buffer*

{
  "nodes": {
    "741KuezCTUaGy0RDV7oxEA": {
      "total_indexing_buffer_in_bytes": 53687091,
      "total_indexing_buffer": "51.1mb"
    }
  }
}
```

### Migration Notes

If your application parses the Nodes Info API response and relies on these fields:

1. **Update field type expectations**: `total_indexing_buffer_in_bytes` is now a number, `total_indexing_buffer` is now a string
2. **Review client code**: Any code that parsed `total_indexing_buffer_in_bytes` as a string or `total_indexing_buffer` as a number needs updating
3. **Test with v3.0.0**: Verify your monitoring and management tools handle the corrected format

## Limitations

- This is a breaking change that affects API response format
- No backward compatibility option is provided
- The change only takes effect in v3.0.0 and later

## References

### Documentation
- [Breaking Changes Documentation](https://docs.opensearch.org/3.0/breaking-changes/): Official v3.0.0 breaking changes
- [Nodes Info API Documentation](https://docs.opensearch.org/3.0/api-reference/nodes-apis/nodes-info/): API reference

### Pull Requests
| PR | Description |
|----|-------------|
| [#17070](https://github.com/opensearch-project/OpenSearch/pull/17070) | Fix interchanged formats of total_indexing_buffer_in_bytes and total_indexing_buffer |

### Issues (Design / RFC)
- [Issue #16910](https://github.com/opensearch-project/OpenSearch/issues/16910): Bug report - NodesInfoResponse serializes fields swapped

## Related Feature Report

- [Nodes Info API](../../../features/opensearch/nodes-info-api.md)
