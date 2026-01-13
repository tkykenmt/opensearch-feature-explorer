---
tags:
  - domain/core
  - component/server
  - indexing
---
# Remote Client Enhancements

## Summary

OpenSearch Remote Metadata SDK v3.3.0 introduces enhancements to write request handling and bug fixes for API compatibility. The release adds support for sequence number and primary term on Put and Delete requests for optimistic concurrency control, adds RefreshPolicy and timeout configuration for write operations, and fixes issues with empty string ID validation and ThreadContextAccess API compatibility.

## Details

### What's New in v3.3.0

This release focuses on improving the write request API with better concurrency control and configuration options, along with critical bug fixes for API compatibility.

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `WriteDataObjectRequest` | New abstract parent class for Put, Update, and Delete requests with shared seqNo/primaryTerm handling |
| `RefreshPolicy` support | Configurable refresh behavior for write operations (IMMEDIATE, WAIT_UNTIL, NONE) |
| `timeout` support | Configurable timeout for write operations |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `refreshPolicy` | When to refresh written data (IMMEDIATE, WAIT_UNTIL, NONE) | `IMMEDIATE` |
| `timeout` | Timeout for write operations | `1m` |
| `ifSeqNo` | Sequence number for optimistic concurrency control | `null` |
| `ifPrimaryTerm` | Primary term for optimistic concurrency control | `null` |

#### API Changes

**SeqNo and PrimaryTerm Support (PR #234)**

Put and Delete requests now support optimistic concurrency control via sequence numbers and primary terms:

```java
// Put with version check
PutDataObjectRequest request = PutDataObjectRequest.builder()
    .index("my-index")
    .id("doc-id")
    .dataObject(myObject)
    .ifSeqNo(5L)
    .ifPrimaryTerm(2L)
    .build();

// Delete with version check
DeleteDataObjectRequest request = DeleteDataObjectRequest.builder()
    .index("my-index")
    .id("doc-id")
    .ifSeqNo(5L)
    .ifPrimaryTerm(2L)
    .build();
```

**RefreshPolicy and Timeout Support (PR #244)**

Write operations now support configurable refresh policy and timeout:

```java
PutDataObjectRequest request = PutDataObjectRequest.builder()
    .index("my-index")
    .id("doc-id")
    .dataObject(myObject)
    .refreshPolicy(RefreshPolicy.WAIT_UNTIL)
    .timeout("30s")
    .build();

// Bulk requests also support these settings
BulkDataObjectRequest bulkRequest = BulkDataObjectRequest.builder()
    .globalIndex("my-index")
    .build()
    .setRefreshPolicy(RefreshPolicy.WAIT_UNTIL)
    .timeout("45s")
    .add(putRequest)
    .add(deleteRequest);
```

### Usage Example

```java
// Complete example with all new features
PutDataObjectRequest putRequest = PutDataObjectRequest.builder()
    .index("my-index")
    .id("doc-id")
    .tenantId("tenant-1")
    .dataObject(myDataObject)
    .ifSeqNo(currentSeqNo)        // Optimistic concurrency
    .ifPrimaryTerm(currentTerm)   // Optimistic concurrency
    .refreshPolicy(RefreshPolicy.IMMEDIATE)  // Refresh immediately
    .timeout("30s")               // 30 second timeout
    .build();

sdkClient.putDataObjectAsync(putRequest)
    .whenComplete((response, error) -> {
        if (error != null) {
            if (error.getCause() instanceof OpenSearchStatusException) {
                OpenSearchStatusException ose = (OpenSearchStatusException) error.getCause();
                if (ose.status() == RestStatus.CONFLICT) {
                    // Handle version conflict
                }
            }
        }
    });
```

### Bug Fixes

| PR | Issue | Description |
|----|-------|-------------|
| #236 | #191 | Throw exception on empty string for put request ID - aligns with OpenSearch behavior |
| #250 | - | Update argument type for `ThreadContextAccess.doPrivileged()` to align with OpenSearch core changes |
| #254 | - | Use `AccessController` instead of `ThreadContextAccess` for internal use to fix `NoSuchMethodError` in ml-commons integration tests |

## Limitations

- RefreshPolicy and timeout may not be applicable on all client implementations (e.g., DynamoDB doesn't have an equivalent concept for refresh)
- Bulk request individual items always use `RefreshPolicy.NONE` - the refresh policy applies to the bulk request as a whole

## References

### Documentation
- [Plugin as a Service Documentation](https://docs.opensearch.org/3.0/developer-documentation/plugin-as-a-service/index/): Official OpenSearch documentation
- [OpenSearch PR #19239](https://github.com/opensearch-project/OpenSearch/pull/19239): ThreadContextAccess API change in OpenSearch core

### Pull Requests
| PR | Description |
|----|-------------|
| [#234](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/234) | Add SeqNo and PrimaryTerm support to Put and Delete requests |
| [#244](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/244) | Add RefreshPolicy and timeout support to Put, Update, Delete, and Bulk requests |
| [#236](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/236) | Throw exception on empty string for put request ID |
| [#250](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/250) | Update argument type for ThreadContextAccess:doPrivileged |
| [#254](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/254) | Use AccessController instead of ThreadContextAccess as it's for internal use |

### Issues (Design / RFC)
- [Issue #233](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/issues/233): SeqNo/PrimaryTerm support request
- [Issue #136](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/issues/136): Timeout support request
- [Issue #178](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/issues/178): RefreshPolicy support request
- [Issue #191](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/issues/191): Empty string ID validation

## Related Feature Report

- Full feature documentation
