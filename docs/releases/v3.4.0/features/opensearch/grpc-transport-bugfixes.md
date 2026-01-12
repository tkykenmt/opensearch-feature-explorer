# GRPC Transport Bugfixes

## Summary

OpenSearch v3.4.0 includes critical bugfixes for the gRPC transport layer, addressing issues with large request handling, bulk API operations, and node bootstrap when using streaming transport with remote cluster state. These fixes improve stability and reliability for production deployments using gRPC.

## Details

### What's New in v3.4.0

This release addresses three key issues in the gRPC transport:

1. **ClassCastException for Large Requests**: Fixed a crash when handling requests larger than 16KB
2. **Bulk API Fixes**: Multiple improvements to the gRPC Bulk API for correctness and performance
3. **Node Bootstrap Fix**: Resolved bootstrap failure when streaming transport is used with remote cluster state

### Technical Changes

#### Fix ClassCastException in FlightClientChannel (PR #20010)

**Problem**: The `serializeToTicket()` method in `FlightClientChannel` cast `BytesReference` directly to `BytesArray`, which fails for requests larger than 16KB that use `PagedBytesReference`.

```
ClassCastException: class org.opensearch.core.common.bytes.PagedBytesReference 
cannot be cast to class org.opensearch.core.common.bytes.BytesArray
```

**Solution**: Replace unsafe cast with `BytesReference.toBytes()`:

```java
// Before (broken for large requests)
byte[] data = Arrays.copyOfRange(((BytesArray) reference).array(), 0, reference.length());

// After (works for all BytesReference types)
return new Ticket(BytesReference.toBytes(reference));
```

#### gRPC Bulk API Fixes (PR #19937)

Multiple fixes to align gRPC Bulk API behavior with REST API:

| Fix | Description |
|-----|-------------|
| Update operation `doc` field | Use `doc` field instead of `object` field (with backward compatibility fallback) |
| Default `fetchSource` | Changed default from `true` to `null` to match REST API behavior |
| Pipeline support for upsert | Added pipeline support for upsert operations |
| Zero-copy optimization | Optimized document bytes copying to pass `BytesReference` directly |

**Key Code Changes:**

```java
// Fix 1: fetchSource default changed to null
public static FetchSourceContext parseFromProtoRequest(BulkRequest request) {
    Boolean fetchSource = null;  // Was: true
    // ...
}

// Fix 2: Use doc field for update operations
ByteString updateDocBytes = ByteString.EMPTY;
if (bulkRequestBodyEntry.hasUpdateAction() && bulkRequestBodyEntry.getUpdateAction().hasDoc()) {
    updateDocBytes = bulkRequestBodyEntry.getUpdateAction().getDoc();
} else if (bulkRequestBodyEntry.hasObject()) {
    // Fallback for backward compatibility
    updateDocBytes = bulkRequestBodyEntry.getObject();
}

// Fix 3: Pipeline support for upsert
IndexRequest upsertRequest = updateRequest.upsertRequest();
if (upsertRequest != null) {
    upsertRequest.setPipeline(pipeline);
}
```

#### Fix Node Bootstrap with Streaming Transport (PR #19948)

**Problem**: When streaming transport is enabled with remote cluster state, nodes fail to start with:

```
can't overwrite as repositories are already present
at org.opensearch.repositories.RepositoriesService.updateRepositoriesMap
```

**Root Cause**: Two separate `LocalNodeFactory` instances are created - one for regular `TransportService` and another for `StreamTransportService`. Both attempt to register the same remote store repositories during startup.

**Solution**: Split `LocalNodeFactory` into two classes:

```java
// Base factory - no remote store verification
private static class LocalNodeFactory implements Function<BoundTransportAddress, DiscoveryNode> {
    @Override
    public DiscoveryNode apply(BoundTransportAddress boundTransportAddress) {
        // Creates DiscoveryNode without repository verification
        return discoveryNode;
    }
}

// Extended factory - with remote store verification (used by main TransportService)
private static class RemoteStoreVerifyingLocalNodeFactory extends LocalNodeFactory {
    @Override
    public DiscoveryNode apply(BoundTransportAddress boundTransportAddress) {
        final DiscoveryNode discoveryNode = super.apply(boundTransportAddress);
        if (isRemoteStoreAttributePresent(settings)) {
            remoteStoreNodeService.createAndVerifyRepositories(discoveryNode);
        }
        return discoveryNode;
    }
}
```

### Usage Example

These fixes are automatically applied. No configuration changes required.

**Testing Large Requests (>16KB):**

```java
// This now works correctly for large documents
LargeTestRequest testRequest = new LargeTestRequest("X".repeat(20 * 1024));
streamTransportService.sendRequest(remoteNode, action, testRequest, options, handler);
```

**Using gRPC Bulk with Update Operations:**

```protobuf
// Preferred: Use UpdateAction.doc field
BulkRequestBody {
  operation_container { update { x_index: "test" x_id: "1" } }
  update_action {
    doc: "{\"field\": \"value\"}"  // Use doc field
  }
}
```

### Migration Notes

- **Update operations**: Migrate from `object` field to `UpdateAction.doc` field for update operations. The `object` field fallback remains for backward compatibility but will be removed in a future release.
- **No action required**: All fixes are backward compatible and apply automatically.

## Limitations

- The `object` field fallback for update operations is deprecated and will be removed in a future release.

## References

### Documentation
- [gRPC APIs Documentation](https://docs.opensearch.org/3.0/api-reference/grpc-apis/index/): Official gRPC documentation
- [Bulk (gRPC) API](https://docs.opensearch.org/3.0/api-reference/grpc-apis/bulk/): Bulk endpoint reference

### Pull Requests
| PR | Description |
|----|-------------|
| [#20010](https://github.com/opensearch-project/OpenSearch/pull/20010) | Fix ClassCastException in FlightClientChannel for requests larger than 16KB |
| [#19937](https://github.com/opensearch-project/OpenSearch/pull/19937) | Fix GRPC Bulk - update doc field, fetchSource default, pipeline support, zero-copy |
| [#19948](https://github.com/opensearch-project/OpenSearch/pull/19948) | Fix node bootstrap error when enable stream transport and remote cluster state |

## Related Feature Report

- [Full gRPC Transport documentation](../../../features/opensearch/grpc-transport--services.md)
