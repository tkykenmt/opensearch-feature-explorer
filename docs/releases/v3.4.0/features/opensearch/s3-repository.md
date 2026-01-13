---
tags:
  - domain/core
  - component/server
  - search
---
# S3 Repository

## Summary

This release adds the `LEGACY_MD5_CHECKSUM_CALCULATION` setting to the list of repository-s3 plugin settings, enabling it to be configured in `opensearch.yml` in addition to repository creation time. This completes the fix for S3-compatible storage compatibility that was introduced in v3.3.0.

## Details

### What's New in v3.4.0

The `s3.client.<client_name>.legacy_md5_checksum_calculation` setting was added to the list of registered settings in `S3RepositoryPlugin`, allowing users to configure legacy MD5 checksum calculation behavior through `opensearch.yml`.

### Background

In OpenSearch 3.0.0, the AWS SDK was upgraded to version 2.30.31, which introduced mandatory checksum trailing headers. This broke compatibility with S3-compatible storage providers (like Outscale, MinIO, etc.) that don't support the new checksum format.

The fix in v3.3.0 ([PR #19220](https://github.com/opensearch-project/OpenSearch/pull/19220)) introduced the `legacy_md5_checksum_calculation` setting to enable legacy MD5 checksum behavior for compatibility. However, this setting was only configurable at repository creation time, not in `opensearch.yml`.

### Technical Changes

#### Configuration Enhancement

The setting `S3ClientSettings.LEGACY_MD5_CHECKSUM_CALCULATION` is now registered in `S3RepositoryPlugin.getSettings()`:

```java
// S3RepositoryPlugin.java
public List<Setting<?>> getSettings() {
    return Arrays.asList(
        // ... other settings ...
        S3ClientSettings.LEGACY_MD5_CHECKSUM_CALCULATION,
        // ... other settings ...
    );
}
```

#### New Configuration Option

| Setting | Description | Default |
|---------|-------------|---------|
| `s3.client.<client_name>.legacy_md5_checksum_calculation` | Enable legacy MD5 checksum calculation for S3-compatible storage | `false` |

### Usage Example

Configure in `opensearch.yml` for cluster-wide S3-compatible storage support:

```yaml
# opensearch.yml
s3.client.default.legacy_md5_checksum_calculation: true
s3.client.default.endpoint: "https://s3-compatible-endpoint.example.com"
```

Or configure per-client:

```yaml
# opensearch.yml
s3.client.minio.legacy_md5_checksum_calculation: true
s3.client.minio.endpoint: "http://minio.local:9000"
```

### Migration Notes

If you're using S3-compatible storage and previously had to configure `legacy_md5_checksum_calculation` at repository creation time, you can now move this configuration to `opensearch.yml` for easier management across all repositories using the same client.

## Limitations

- The setting only affects S3-compatible storage providers that don't support AWS SDK v2's checksum trailing headers
- When enabled, uses MD5 checksums instead of the newer CRC-based checksums

## References

### Documentation
- [Register Snapshot Repository](https://docs.opensearch.org/3.0/api-reference/snapshots/create-repository/): OpenSearch documentation
- [PR #19220](https://github.com/opensearch-project/OpenSearch/pull/19220): Fix issue with s3-compatible repositories due to missing checksum trailing headers (v3.3.0)

### Pull Requests
| PR | Description |
|----|-------------|
| [#19788](https://github.com/opensearch-project/OpenSearch/pull/19788) | Add S3Repository.LEGACY_MD5_CHECKSUM_CALCULATION to list of repository-s3 settings |

### Issues (Design / RFC)
- [Issue #18240](https://github.com/opensearch-project/OpenSearch/issues/18240): Snapshot repositories don't work with S3 compatible storage in 3.0.0

## Related Feature Report

- Full feature documentation
