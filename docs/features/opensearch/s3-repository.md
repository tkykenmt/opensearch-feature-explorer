# S3 Repository

## Summary

The S3 Repository plugin (`repository-s3`) enables OpenSearch to store snapshots in Amazon S3 buckets. It provides a reliable, scalable, and cost-effective solution for backing up and restoring OpenSearch indices using AWS cloud storage.

## Details

### Architecture

```mermaid
graph TB
    subgraph "OpenSearch Cluster"
        OS[OpenSearch Node]
        Plugin[repository-s3 Plugin]
        OS --> Plugin
    end
    
    subgraph "AWS"
        S3[Amazon S3 Bucket]
        IAM[IAM Credentials]
    end
    
    Plugin -->|Snapshot/Restore| S3
    Plugin -->|Authentication| IAM
    
    subgraph "Retry Mechanism"
        Retry[Standard Retry Mode]
        Backoff[Jittered Exponential Backoff]
        Circuit[Circuit Breaker]
        Retry --> Backoff
        Backoff --> Circuit
    end
    
    Plugin --> Retry
```

### Components

| Component | Description |
|-----------|-------------|
| `S3Service` | Manages synchronous S3 client operations |
| `S3AsyncService` | Manages asynchronous S3 client operations |
| `S3Repository` | Implements the repository interface for S3 storage |
| `S3BlobStore` | Handles blob storage operations in S3 |
| `S3BlobContainer` | Manages blob containers within S3 |

### Configuration

#### Repository Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `bucket` | Name of the S3 bucket | Required |
| `base_path` | Path within the bucket for snapshots | Root |
| `client` | Named client configuration to use | `default` |
| `compress` | Whether to compress metadata files | `false` |
| `chunk_size` | Size of file chunks for uploads | `1gb` |
| `max_retries` | Maximum number of retry attempts | `3` |
| `throttle_retries` | Use throttling backoff strategy | `true` |
| `canned_acl` | S3 canned ACL for created objects | `private` |
| `storage_class` | S3 storage class for snapshot files | `standard` |
| `server_side_encryption` | Enable S3 server-side encryption | `false` |
| `buffer_size` | Buffer size for multipart uploads | `5mb`-`5gb` |
| `max_restore_bytes_per_sec` | Maximum restore rate | `40mb` |
| `max_snapshot_bytes_per_sec` | Maximum snapshot rate | `40mb` |
| `readonly` | Whether repository is read-only | `false` |

#### Client Settings

Configure in `opensearch.yml`:

| Setting | Description |
|---------|-------------|
| `s3.client.default.access_key` | AWS access key |
| `s3.client.default.secret_key` | AWS secret key |
| `s3.client.default.endpoint` | Custom S3 endpoint |
| `s3.client.default.region` | AWS region |
| `s3.client.default.protocol` | HTTP or HTTPS |

### Usage Example

#### Register S3 Repository

```json
PUT _snapshot/my-s3-repo
{
  "type": "s3",
  "settings": {
    "bucket": "my-opensearch-snapshots",
    "base_path": "snapshots/production",
    "compress": true,
    "server_side_encryption": true
  }
}
```

#### Create Snapshot

```json
PUT _snapshot/my-s3-repo/snapshot-1
{
  "indices": "my-index-*",
  "ignore_unavailable": true,
  "include_global_state": false
}
```

#### Restore Snapshot

```json
POST _snapshot/my-s3-repo/snapshot-1/_restore
{
  "indices": "my-index-*",
  "rename_pattern": "(.+)",
  "rename_replacement": "restored-$1"
}
```

### Retry Behavior

The plugin uses AWS SDK's Standard retry mode (since v2.18.0):

- **Maximum Attempts**: 3 by default
- **Backoff Strategy**: Jittered exponential backoff
- **Circuit Breaker**: Prevents retries during outages
- **Throttling**: Automatic handling of S3 throttling responses

```mermaid
flowchart TB
    A[Request] --> B{Success?}
    B -->|Yes| C[Complete]
    B -->|No| D{Retryable?}
    D -->|No| E[Fail]
    D -->|Yes| F{Attempts < Max?}
    F -->|No| E
    F -->|Yes| G{Retry Quota Available?}
    G -->|No| E
    G -->|Yes| H[Exponential Backoff with Jitter]
    H --> I[Retry Request]
    I --> B
```

### Async Deletion (v2.18.0+)

The S3 repository supports asynchronous deletion operations for improved performance during snapshot deletion:

```mermaid
graph TB
    subgraph "Async Deletion Flow"
        BlobRepo[BlobStoreRepository]
        Container[S3BlobContainer]
        AsyncClient[S3 Async Client]
        S3[Amazon S3]
    end
    
    BlobRepo -->|deleteContainer| Container
    Container -->|deleteAsync| AsyncClient
    AsyncClient -->|DeleteObjectsRequest| S3
    
    subgraph "Batch Processing"
        List[List Objects]
        Batch[Create Batches]
        Delete[Delete Batch]
        List --> Batch
        Batch --> Delete
    end
    
    Container --> List
```

#### Async Deletion Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `cluster.snapshot.async-deletion.enable` | Enable/disable async deletion for S3 repositories | `true` |

## Limitations

- Glacier and Deep Archive storage classes are not supported
- Maximum chunk size is limited by S3 multipart upload limits
- IAM credentials must have appropriate S3 permissions
- Cross-region snapshot restore may incur data transfer costs
- Async deletion is only available for S3 repositories

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v2.18.0 | [#15621](https://github.com/opensearch-project/OpenSearch/pull/15621) | Add support for async deletion in S3BlobContainer |
| v2.18.0 | [#15978](https://github.com/opensearch-project/OpenSearch/pull/15978) | Change default retry mechanism to Standard Mode |
| v2.18.0 | [#16194](https://github.com/opensearch-project/OpenSearch/pull/16194) | Fix SLF4J warnings on startup |

## References

- [PR #15621](https://github.com/opensearch-project/OpenSearch/pull/15621): Async deletion implementation
- [Issue #15397](https://github.com/opensearch-project/OpenSearch/issues/15397): Add jitter to downloads from remote store
- [Issue #16152](https://github.com/opensearch-project/OpenSearch/issues/16152): SLF4J warnings when adding repository-s3
- [Register Snapshot Repository](https://docs.opensearch.org/2.18/api-reference/snapshots/create-repository/): OpenSearch documentation
- [AWS SDK Retry Behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html): AWS retry modes documentation

## Change History

- **v2.18.0** (2024-10-22): Added async deletion support, changed default retry mechanism to Standard Mode, fixed SLF4J warnings
