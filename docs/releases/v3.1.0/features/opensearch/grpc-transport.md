---
tags:
  - domain/core
  - component/server
  - observability
  - performance
  - search
---
# gRPC Transport Performance Optimization

## Summary

OpenSearch v3.1.0 introduces performance optimizations for the gRPC transport layer, focusing on reducing latency and CPU usage through pass-by-reference patterns in protobuf response construction. Additionally, package structure improvements consolidate gRPC-related code under the correct namespace.

## Details

### What's New in v3.1.0

This release includes two key improvements to the gRPC transport:

1. **Performance Optimization**: Response-side protobuf construction now uses pass-by-reference instead of copying objects, reducing memory allocation, garbage collection overhead, and CPU usage.

2. **Package Reorganization**: The `org.opensearch.transport.grpc` package has been renamed to `org.opensearch.plugin.transport.grpc` for consistency with the plugin structure.

### Technical Changes

#### Performance Improvements

The optimization targets the response conversion path where protobuf messages are constructed. Previously, partially constructed protobuf objects were copied between methods. The new approach passes builders by reference, populating them in place.

**Key Changes:**
- `SearchHitProtoUtils`: Refactored to use helper methods with builder references
- `SearchHitsProtoUtils`: Pass-by-reference for hits metadata construction
- `SearchResponseProtoUtils`: Builder pattern optimization for response construction
- `ObjectMapProtoUtils`: Optimized map/list value handling
- `FieldValueProtoUtils`: Direct builder population

#### Benchmark Results

Testing with a MatchAll query returning 30k documents (~2.27MB) on a single 8-core node:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| P50 Latency (subsequent) | 30.6ms | 29.1ms | ~5% |
| P95 Latency (subsequent) | 35.3ms | 31.6ms | ~10% |
| P99 Latency (subsequent) | 40.9ms | 36.5ms | ~11% |
| Avg CPU Usage | 0.27 | 0.24 | ~11% |
| Max CPU Usage | 0.30 | 0.28 | ~7% |

#### Package Structure

```
plugins/transport-grpc/src/main/java/org/opensearch/plugin/transport/grpc/
├── ssl/
│   ├── SecureNetty4GrpcServerTransport.java  # Moved from org.opensearch.transport.grpc.ssl
│   └── package-info.java
├── proto/
│   └── response/
│       ├── common/
│       │   ├── FieldValueProtoUtils.java
│       │   └── ObjectMapProtoUtils.java
│       ├── document/
│       │   └── get/
│       │       └── GetResultProtoUtils.java
│       └── search/
│           ├── SearchHitProtoUtils.java
│           ├── SearchHitsProtoUtils.java
│           ├── SearchResponseProtoUtils.java
│           └── SearchResponseSectionsProtoUtils.java
└── ...
```

### Usage Example

No API changes are required. The optimizations are internal and transparent to users.

```java
// Existing gRPC client code continues to work unchanged
SearchServiceGrpc.SearchServiceBlockingStub searchStub = 
    SearchServiceGrpc.newBlockingStub(channel);

SearchRequest searchRequest = SearchRequest.newBuilder()
    .addIndex("my-index")
    .setRequestBody(SearchRequestBody.newBuilder()
        .setQuery(QueryContainer.newBuilder()
            .setMatchAll(MatchAllQuery.newBuilder().build())
            .build())
        .setSize(1000)
        .build())
    .build();

// Response construction is now more efficient
SearchResponse response = searchStub.search(searchRequest);
```

### Migration Notes

- No migration required for existing gRPC clients
- If you have custom code importing from `org.opensearch.transport.grpc.ssl`, update imports to `org.opensearch.plugin.transport.grpc.ssl`

## Limitations

- Performance gains are most noticeable with large response payloads
- First request latency improvements are less significant than subsequent requests
- The gRPC feature remains experimental

## References

### Documentation
- [gRPC APIs Documentation](https://docs.opensearch.org/3.0/api-reference/grpc-apis/index/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#18303](https://github.com/opensearch-project/OpenSearch/pull/18303) | Optimize gRPC perf by passing by reference |
| [#18031](https://github.com/opensearch-project/OpenSearch/pull/18031) | Remove package org.opensearch.transport.grpc and replace with org.opensearch.plugin.transport.grpc |

### Issues (Design / RFC)
- [Issue #18291](https://github.com/opensearch-project/OpenSearch/issues/18291): gRPC Performance Improvements feature request
- [Issue #16787](https://github.com/opensearch-project/OpenSearch/issues/16787): META - Productionalizing Client/Server GRPC

## Related Feature Report

- Full feature documentation
