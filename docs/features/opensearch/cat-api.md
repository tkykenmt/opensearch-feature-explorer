---
tags:
  - opensearch
---
# CAT API

## Summary

The CAT (Compact and Aligned Text) API provides a human-readable format for cluster information. It returns data in a tabular format that is easy to read in terminals and command-line interfaces.

## Details

### Overview

CAT APIs are designed for human consumption using the command line or Kibana console. They return plain text output by default, making them ideal for quick cluster diagnostics.

### Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `_cat/nodes` | Node information including version, build, and resource usage |
| `_cat/indices` | Index information |
| `_cat/shards` | Shard allocation information |
| `_cat/health` | Cluster health status |
| `_cat/allocation` | Shard allocation per node |

### Help Parameter

Each CAT endpoint supports a `?help` parameter that displays available columns and their descriptions:

```bash
GET _cat/nodes?help
```

### Common Parameters

| Parameter | Description |
|-----------|-------------|
| `v` | Include column headers |
| `help` | Show available columns |
| `h` | Select specific columns |
| `format` | Output format (text, json, yaml) |
| `s` | Sort by column |

### Usage Example

```bash
# Get node information with headers
GET _cat/nodes?v

# Get specific columns
GET _cat/nodes?v&h=name,ip,heap.percent,ram.percent

# Get help for available columns
GET _cat/nodes?help
```

## Limitations

- CAT APIs are intended for human consumption; use JSON APIs for programmatic access
- Output format may change between versions

## Change History

- **v2.16.0** (2024-08-06): Updated help output to replace legacy "es" references with "os" (OpenSearch) terminology in `_cat/nodes` endpoint

## References

### Documentation
- [CAT API](https://docs.opensearch.org/latest/api-reference/cat/index/)
- [CAT nodes](https://docs.opensearch.org/latest/api-reference/cat/cat-nodes/)

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#14722](https://github.com/opensearch-project/OpenSearch/pull/14722) | Update help output for _cat |
