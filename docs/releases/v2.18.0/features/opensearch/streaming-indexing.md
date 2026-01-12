---
tags:
  - indexing
---

# Streaming Indexing

## Summary

This release includes bug fixes for the Streaming Bulk API (`/_bulk/stream`) that resolve issues with request hangs and intermittent newline termination errors when indexing large documents. These fixes improve the reliability of streaming bulk operations, particularly for documents exceeding 8KB in size.

## Details

### What's New in v2.18.0

Two critical bug fixes were backported to v2.18.0 to address stability issues in the Streaming Bulk API:

1. **Request Hang Fix** ([#16158](https://github.com/opensearch-project/OpenSearch/pull/16158)): Fixed an issue where streaming bulk requests would hang indefinitely when processing certain document patterns, particularly when combining scripted requests with larger documents.

2. **Newline Termination Error Fix** ([#16337](https://github.com/opensearch-project/OpenSearch/pull/16337)): Fixed intermittent "The bulk request must be terminated by a newline [\n]" failures that occurred when bulk indexing documents larger than 1KB.

### Technical Changes

#### Root Cause Analysis

The issues stemmed from how Netty handles HTTP chunked transfer encoding:

- Netty could emit chunks partially, causing incomplete document parsing
- The Reactor Netty library lacked configuration options to control this behavior
- Documents exceeding the default 8KB chunk size were particularly affected

#### Fixes Applied

| Component | Change | PR |
|-----------|--------|-----|
| RestController | Changed `Mono.ignoreElements(this).then()` to `Mono.from(this).ignoreElement().then()` for proper stream handling | [#16158](https://github.com/opensearch-project/OpenSearch/pull/16158) |
| ReactorNetty4HttpServerTransport | Added `.allowPartialChunks(false)` configuration to prevent partial chunk emission | [#16337](https://github.com/opensearch-project/OpenSearch/pull/16337) |
| Reactor Netty | Upgraded from 1.1.22 to 1.1.23 which includes the fix for partial chunk handling | [#16337](https://github.com/opensearch-project/OpenSearch/pull/16337) |

#### Architecture

```mermaid
graph TB
    subgraph Client
        A[HTTP Client] -->|Chunked Transfer| B[/_bulk/stream]
    end
    subgraph "OpenSearch (transport-reactor-netty4)"
        B --> C[ReactorNetty4HttpServerTransport]
        C -->|allowPartialChunks=false| D[HTTP Decoder]
        D --> E[RestController]
        E -->|Mono.from.ignoreElement| F[BulkStreamingRestHandler]
    end
    subgraph Processing
        F --> G[Document Parser]
        G --> H[Index Operations]
        H --> I[Streaming Response]
    end
```

### Usage Example

The Streaming Bulk API allows continuous document ingestion with immediate responses:

```bash
curl -X POST "http://localhost:9200/_bulk/stream" \
  -H "Transfer-Encoding: chunked" \
  -H "Content-Type: application/json" -d'
{ "index": { "_index": "test", "_id": "1" } }
{ "field": "value with large content..." }
'
```

After these fixes, documents of any size (including those exceeding 8KB) are processed reliably without hanging or newline errors.

### Migration Notes

No migration required. These are bug fixes that improve existing functionality. Users experiencing intermittent failures with the Streaming Bulk API should upgrade to v2.18.0 or later.

## Limitations

- The Streaming Bulk API requires the `transport-reactor-netty4` plugin to be installed
- The feature remains experimental and is not recommended for production use
- HTTP/2 or HTTP/1.1 with chunked transfer encoding is required

## References

### Documentation
- [Streaming Bulk API Documentation](https://docs.opensearch.org/2.18/api-reference/document-apis/bulk-streaming/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#16158](https://github.com/opensearch-project/OpenSearch/pull/16158) | Fix streaming bulk request hangs |
| [#16337](https://github.com/opensearch-project/OpenSearch/pull/16337) | Fix intermittent newline termination failures |

### Issues (Design / RFC)
- [Issue #16035](https://github.com/opensearch-project/OpenSearch/issues/16035): Streaming bulk request hangs
- [Issue #16214](https://github.com/opensearch-project/OpenSearch/issues/16214): Intermittent newline termination failures
- [Reactor Netty Issue #3452](https://github.com/reactor/reactor-netty/issues/3452): Partial chunk handling

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/streaming-indexing.md)
