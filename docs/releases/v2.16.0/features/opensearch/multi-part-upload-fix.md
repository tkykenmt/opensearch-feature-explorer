---
tags:
  - opensearch
---
# Multi-Part Upload Fix

## Summary

Fixed S3 multipart upload failures for remote cluster state objects. When remote state files exceeded 5 MB, the S3 plugin attempted multipart upload but failed due to all upload parts sharing the same `IndexInput` instance, causing file pointer conflicts and content-length mismatches.

## Details

### What's New in v2.16.0

This release fixes a critical bug where S3 multipart uploads failed for remote cluster state objects when the payload exceeded 5 MB (the threshold for multipart upload).

### Technical Changes

The root cause was that when initializing parts for multipart upload, all parts shared the same `IndexInput` instance. Each part set the file pointer to its starting position, but since they shared the same backing `IndexInput`, the file pointer was overwritten by the last part. This caused:

1. Only one part could read data correctly
2. Other parts encountered content-length mismatches
3. Upload failures with errors like "Request content was only X bytes, but the specified content-length was Y bytes"

The fix ensures a new `ByteArrayIndexInput` instance is created for each part in the stream supplier function, rather than reusing a single instance.

**Affected Components:**

| Component | Change |
|-----------|--------|
| `BlobStoreTransferService` | Create new `ByteArrayIndexInput` per part in `OffsetRangeInputStreamSupplier` |
| `ChecksumBlobStoreFormat` | Create new `ByteArrayIndexInput` per part for async upload |
| `ConfigBlobStoreFormat` | Create new `ByteArrayIndexInput` per part for urgent priority uploads |

**Code Change Pattern:**

Before (broken):
```java
try (IndexInput input = new ByteArrayIndexInput(resourceDescription, bytes)) {
    uploadBlobAsyncInternal(
        ...,
        (size, position) -> new OffsetRangeIndexInputStream(input, size, position),
        ...
    );
}
```

After (fixed):
```java
uploadBlobAsyncInternal(
    ...,
    (size, position) -> new OffsetRangeIndexInputStream(
        new ByteArrayIndexInput(resourceDescription, bytes), size, position),
    ...
);
```

### Reproduction Scenario

1. Create a remote state publication enabled cluster with S3 as backing store
2. Add nodes until `DiscoveryNodes` in cluster state exceeds 5 MB
3. S3 plugin triggers multipart upload
4. Upload fails with content-length mismatch exception

## Limitations

- This fix only addresses the multipart upload issue for remote cluster state
- The 5 MB threshold for multipart upload is determined by the S3 plugin configuration

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14888](https://github.com/opensearch-project/OpenSearch/pull/14888) | Create new IndexInput for multi part upload | [#14808](https://github.com/opensearch-project/OpenSearch/issues/14808) |

### Issues
- [#14808](https://github.com/opensearch-project/OpenSearch/issues/14808): S3 Multi-part upload fails for remote cluster state
