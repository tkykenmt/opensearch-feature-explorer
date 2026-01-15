---
tags:
  - opensearch
---
# Fingerprint Ingest Processor

## Summary

OpenSearch v2.16.0 introduces the `fingerprint` ingest processor, which generates a hash value for specified fields or all fields in a document. The hash value can be used to deduplicate documents within an index and collapse search results.

## Details

### What's New in v2.16.0

The fingerprint processor is a new ingest processor that computes a cryptographic hash from document fields during ingestion. This enables:

- **Document deduplication**: Identify and remove duplicate documents based on content
- **Search result collapsing**: Group search results by fingerprint to show unique content

### How It Works

For each field, the processor concatenates:
- Field name
- Length of field value
- Field value itself

These are separated by the pipe character `|`. For example: `|field1|3:value1|field2|10:value2|`

For nested object fields, the field name is flattened using dot notation (e.g., `root_field.sub_field1`).

### Configuration Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `fields` | Optional | - | List of fields to include in hash calculation |
| `exclude_fields` | Optional | - | Fields to exclude from hash calculation (mutually exclusive with `fields`) |
| `hash_method` | Optional | `SHA-1@2.16.0` | Hash algorithm: `MD5@2.16.0`, `SHA-1@2.16.0`, `SHA-256@2.16.0`, or `SHA3-256@2.16.0` |
| `target_field` | Optional | `fingerprint` | Field to store the generated hash value |
| `ignore_missing` | Optional | `false` | Exit quietly if a required field is missing |
| `description` | Optional | - | Description of the processor |
| `if` | Optional | - | Condition for running the processor |
| `ignore_failure` | Optional | `false` | Ignore failures |
| `on_failure` | Optional | - | Processors to run on failure |
| `tag` | Optional | - | Identifier tag for debugging |

### Usage Examples

**Include specific fields:**
```json
{
  "processors": [
    {
      "fingerprint": {
        "fields": ["foo", "bar"],
        "target_field": "fingerprint",
        "hash_method": "SHA-256@2.16.0"
      }
    }
  ]
}
```

**Exclude specific fields:**
```json
{
  "processors": [
    {
      "fingerprint": {
        "exclude_fields": ["timestamp", "metadata"],
        "target_field": "fingerprint"
      }
    }
  ]
}
```

**Include all fields (default when both `fields` and `exclude_fields` are empty):**
```json
{
  "processors": [
    {
      "fingerprint": {}
    }
  ]
}
```

### Hash Method Versioning

The version number is appended to hash method names (e.g., `SHA-1@2.16.0`) to ensure consistent hashing across OpenSearch versions. If the processing logic changes in future versions, new hash methods with updated version numbers will be introduced.

### Technical Implementation

The processor is implemented in `FingerprintProcessor.java` within the `ingest-common` module. Key implementation details:

- Fields are deduplicated and sorted alphabetically for consistent hash generation
- Metadata fields (`_index`, `_id`, `_routing`) are automatically excluded
- Nested objects are flattened with dot notation
- Hash output is Base64-encoded with the method prefix (e.g., `SHA-1@2.16.0:YqpBTuHXCPV04j/7lGfWeUl8Tyo=`)

## Limitations

- Either `fields` or `exclude_fields` can be set, not both
- Field names in `fields` and `exclude_fields` cannot be null or empty
- Metadata fields are always excluded from hash calculation

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#13724](https://github.com/opensearch-project/OpenSearch/pull/13724) | Add fingerprint ingest processor | [#13612](https://github.com/opensearch-project/OpenSearch/issues/13612) |

### Documentation

- [Fingerprint Processor Documentation](https://docs.opensearch.org/2.16/ingest-pipelines/processors/fingerprint/)
