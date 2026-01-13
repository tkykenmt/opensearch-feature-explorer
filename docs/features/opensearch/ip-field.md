---
tags:
  - opensearch
---
# IP Field Type

## Summary

The IP field type stores IP addresses in IPv4 or IPv6 format. It supports exact matching, CIDR notation queries, and range queries. IP fields can be configured with indexing, doc_values, or both for different query performance characteristics.

## Details

### Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `boost` | Floating-point value for relevance scoring weight | `1.0` |
| `doc_values` | Store on disk for aggregations, sorting, scripting | `true` |
| `ignore_malformed` | Ignore malformed values without throwing exception | `false` |
| `index` | Whether the field should be searchable | `true` |
| `null_value` | Value to use in place of `null` | `null` |
| `store` | Store field value separately from `_source` | `false` |

### Query Types

| Query Type | Description | Example |
|------------|-------------|---------|
| Term | Exact IP match | `"term": {"ip": "192.168.1.1"}` |
| Term (CIDR) | IP range via CIDR notation | `"term": {"ip": "192.168.0.0/24"}` |
| Range | IP address range | `"range": {"ip": {"gte": "192.168.0.0", "lte": "192.168.255.255"}}` |

### Doc Values Only Configuration

When storage optimization is needed, IP fields can be configured with `index: false` and `doc_values: true`:

```json
{
  "mappings": {
    "properties": {
      "ip_address": {
        "type": "ip",
        "index": false,
        "doc_values": true
      }
    }
  }
}
```

This configuration:
- Reduces index size by not creating inverted index
- Still allows searching via doc_values (slower but functional)
- Supports aggregations, sorting, and scripting

## Limitations

- Doc_values-only queries use slower query implementations
- IPv4 addresses are internally stored as IPv6-mapped addresses
- CIDR notation queries on doc_values-only fields may have performance implications

## Change History

- **v2.19.0** (2025-01-14): Fixed CIDR notation (IP mask) searching for doc_values-only IP fields ([#16628](https://github.com/opensearch-project/OpenSearch/pull/16628))
- **v2.12.0** (2024-01-30): Added support for searching IP fields with only doc_values enabled ([#11508](https://github.com/opensearch-project/OpenSearch/pull/11508))
- **v1.0.0**: Initial implementation of IP field type

## References

### Documentation
- [IP address field type](https://docs.opensearch.org/latest/field-types/supported-field-types/ip/)

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v2.19.0 | [#16628](https://github.com/opensearch-project/OpenSearch/pull/16628) | Fix doc_values only IP field searching for masks |
| v2.12.0 | [#11508](https://github.com/opensearch-project/OpenSearch/pull/11508) | Enable doc_values-only searching for IP fields |
