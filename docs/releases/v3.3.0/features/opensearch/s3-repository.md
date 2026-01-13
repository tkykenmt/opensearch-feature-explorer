---
tags:
  - domain/core
  - component/server
  - search
---
# S3 Repository Compatibility Fix

## Summary

This release fixes a critical compatibility issue with S3-compatible storage providers (such as Outscale, MinIO, and others) that was introduced in OpenSearch 3.0.0 due to the AWS SDK v2 upgrade. The fix ensures that checksum trailing headers are only sent when required by the storage provider, restoring compatibility with S3-compatible repositories.

## Details

### What's New in v3.3.0

The `repository-s3` plugin now properly handles checksum requirements for S3-compatible storage providers by:

1. Setting `RequestChecksumCalculation.WHEN_REQUIRED` - only calculates checksums when the storage provider requires them
2. Setting `ResponseChecksumValidation.WHEN_REQUIRED` - only validates response checksums when required
3. Adding `LegacyMd5Plugin` support for providers that require MD5 checksums instead of trailing headers

### Technical Changes

#### Root Cause

AWS SDK v2.30.31+ introduced mandatory checksum trailing headers by default. Many S3-compatible storage providers don't support these new trailing headers, causing errors like:

- `trailing checksum is not supported`
- `Invalid trailing header names in x-amz-trailer`
- `The Content-MD5 you specified did not match what we received`

#### Solution

The fix modifies `S3Service` and `S3AsyncService` to build S3 clients with conditional checksum behavior:

```java
final S3ClientBuilder builder = S3Client.builder()
    .requestChecksumCalculation(RequestChecksumCalculation.WHEN_REQUIRED)
    .responseChecksumValidation(ResponseChecksumValidation.WHEN_REQUIRED);

if (clientSettings.legacyMd5ChecksumCalculation) {
    builder.addPlugin(LegacyMd5Plugin.create());
}
```

#### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `legacyMd5ChecksumCalculation` | Enable legacy MD5 checksum calculation for providers that require it | `false` |

### Usage Example

For S3-compatible storage that requires MD5 checksums:

```yaml
# opensearch.yml
s3.client.default.legacy_md5_checksum_calculation: true
```

Register repository as usual:

```json
PUT _snapshot/my-s3-compatible-repo
{
  "type": "s3",
  "settings": {
    "bucket": "my-bucket",
    "endpoint": "s3.my-provider.com",
    "protocol": "https"
  }
}
```

### Migration Notes

- Users of S3-compatible storage providers who experienced issues after upgrading to OpenSearch 3.0.0+ should upgrade to v3.3.0
- No configuration changes required for standard AWS S3 usage
- For providers requiring MD5 checksums, enable `legacy_md5_checksum_calculation`

## Limitations

- Some S3-compatible providers may still have compatibility issues depending on their specific implementation
- The `LegacyMd5Plugin` adds overhead for MD5 calculation when enabled

## References

### Documentation
- [Register Snapshot Repository](https://docs.opensearch.org/3.0/api-reference/snapshots/create-repository/): OpenSearch documentation
- [AWS SDK Discussion #5802](https://github.com/aws/aws-sdk-java-v2/discussions/5802): Workaround for checksum trailing headers

### Pull Requests
| PR | Description |
|----|-------------|
| [#19220](https://github.com/opensearch-project/OpenSearch/pull/19220) | Fix issue with s3-compatible repositories due to missing checksum trailing headers |

### Issues (Design / RFC)
- [Issue #18240](https://github.com/opensearch-project/OpenSearch/issues/18240): Snapshot repositories don't work with S3 compatible storage in 3.0.0
- [Issue #19124](https://github.com/opensearch-project/OpenSearch/issues/19124): repository-s3 error x-amz-trailer

## Related Feature Report

- Full feature documentation
