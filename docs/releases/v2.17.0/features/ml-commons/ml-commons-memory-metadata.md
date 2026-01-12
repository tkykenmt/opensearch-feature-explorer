# ML Commons Memory Metadata

## Summary

This enhancement adds a new `additional_info` field to the memory metadata in ML Commons, allowing users to store custom key-value pairs alongside conversational memory. This enables applications to associate arbitrary metadata (such as agent IDs, prompt information, or application-specific data) with conversation memories for better context management in conversational search scenarios.

## Details

### What's New in v2.17.0

The Memory API now supports an `additional_info` field that can store flexible key-value metadata using the `flat_object` field type. This field can be set during memory creation, updated later, and queried using standard OpenSearch queries.

### Technical Changes

#### Index Schema Update

The memory metadata index (`.plugins-ml-memory-meta`) schema version was bumped from 1 to 2 with the new field:

| Field | Type | Description |
|-------|------|-------------|
| `additional_info` | `flat_object` | Stores arbitrary key-value pairs as metadata |

#### API Changes

**Create Memory with Additional Info:**

```json
POST /_plugins/_ml/memory
{
  "name": "test memory",
  "additional_info": {
    "agent_id": "abc123",
    "prompt_template": "default"
  }
}
```

**Response:**

```json
{
  "memory_id": "ZTjeBpEB_JGSOCuj5ARu"
}
```

**Get Memory Response:**

```json
{
  "memory_id": "ZTjeBpEB_JGSOCuj5ARu",
  "create_time": "2024-07-31T03:39:16.462676Z",
  "updated_time": "2024-07-31T03:39:16.462676Z",
  "name": "test memory",
  "user": "admin",
  "additional_info": {
    "agent_id": "abc123",
    "prompt_template": "default"
  }
}
```

**Search Memory by Additional Info:**

```json
POST /_plugins/_ml/memory/_search
{
  "query": {
    "match": {
      "additional_info.agent_id": "abc123"
    }
  }
}
```

#### New Components

| Component | Description |
|-----------|-------------|
| `ConversationalIndexConstants.META_ADDITIONAL_INFO_FIELD` | Constant for the new field name |
| `ConversationMeta.additionalInfos` | Field in the ConversationMeta class |
| `CreateConversationRequest.additionalInfos` | Request parameter for additional info |

#### Version Compatibility

The `additional_info` field is supported from version 2.17.0 onwards. The implementation includes version checks (`MINIMAL_SUPPORTED_VERSION_FOR_ADDITIONAL_INFO`) to ensure backward compatibility during rolling upgrades.

### Usage Example

```bash
# Create memory with additional info
curl -X POST "http://localhost:9200/_plugins/_ml/memory" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RAG conversation",
    "additional_info": {
      "agent_id": "my-agent",
      "session_type": "customer-support"
    }
  }'

# Update memory with additional info
curl -X PUT "http://localhost:9200/_plugins/_ml/memory/{memory_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated conversation",
    "additional_info": {
      "agent_id": "my-agent",
      "session_type": "sales"
    }
  }'
```

### Migration Notes

- Existing memories created before v2.17.0 will have an empty `additional_info` object (`{}`)
- No migration is required; the field is automatically available after upgrade
- The `flat_object` type allows flexible schema for the additional info content

## Limitations

- The `additional_info` field values must be strings (stored as `Map<String, String>`)
- The field uses `flat_object` type which has specific query limitations compared to nested objects

## References

### Documentation
- [Memory APIs Documentation](https://docs.opensearch.org/2.17/ml-commons-plugin/api/memory-apis/index/): Official Memory API docs
- [Create Memory API](https://docs.opensearch.org/2.17/ml-commons-plugin/api/memory-apis/create-memory/): Create memory documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#2750](https://github.com/opensearch-project/ml-commons/pull/2750) | Adding additional info for memory metadata |

### Issues (Design / RFC)
- [Issue #2755](https://github.com/opensearch-project/ml-commons/issues/2755): Feature request for additional_info field
- [Issue #2632](https://github.com/opensearch-project/ml-commons/issues/2632): Related discussion on application_type field

## Related Feature Report

- [Full feature documentation](../../../features/ml-commons/ml-commons-memory-metadata.md)
