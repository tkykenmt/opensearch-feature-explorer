---
tags:
  - opensearch
---
# Repository Verification

## Summary

OpenSearch v2.16.0 introduces the `prefix_mode_verification` setting for snapshot repositories. When enabled, this setting adds a hashed value to the prefix path during repository verification, distributing verification requests across different storage paths to reduce throttling on remote stores.

## Details

### What's New in v2.16.0

This release adds a new repository setting to address node bootstrap failures caused by remote store throttling during repository verification.

### Problem Addressed

With remote store enabled clusters, repository verification occurs during node bootstrap. When multiple nodes start simultaneously, all verification requests target the same storage path, which can trigger throttling from the remote store (e.g., S3). This throttling causes node bootstrap failures.

### Solution

The `prefix_mode_verification` setting distributes verification requests by prepending a hashed value (using FNV-1a hash algorithm) to the base path. This spreads the load across different storage prefixes, reducing the likelihood of throttling.

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `prefix_mode_verification` | When enabled, adds a hashed prefix to the verification path | `false` |

### Usage

#### Repository Registration

```json
PUT /_snapshot/my-repo
{
  "type": "s3",
  "settings": {
    "bucket": "my-bucket",
    "base_path": "snapshots",
    "prefix_mode_verification": true
  }
}
```

#### Remote Store Node Attributes

For remote store enabled clusters, configure via node attributes:

```yaml
node.attr.remote_store.segment.repository: my-segment-repo
node.attr.remote_store.segment.repository.type: s3
node.attr.remote_store.segment.repository.settings.bucket: my-bucket
node.attr.remote_store.segment.repository.settings.prefix_mode_verification: true
```

### Technical Implementation

When `prefix_mode_verification` is enabled:

1. A random seed (UUID) is generated for verification
2. The seed is hashed using FNV-1a composite algorithm
3. The hashed value is prepended to the base path using `HASHED_PREFIX` path type
4. Verification files are written to and read from this hashed path
5. Cleanup removes files from the hashed path

```mermaid
flowchart LR
    subgraph "Standard Verification"
        A1[base_path] --> B1[tests-{seed}]
    end
    
    subgraph "Prefix Mode Verification"
        A2[hash/base_path] --> B2[tests-{seed}]
    end
```

## Limitations

- Setting is static (node-scope) and requires repository re-registration to change
- Only affects verification operations, not actual snapshot data paths
- Hash distribution depends on the randomness of the seed UUID

## References

### Documentation

- [Register Snapshot Repository](https://docs.opensearch.org/2.16/api-reference/snapshots/create-repository/)

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14790](https://github.com/opensearch-project/OpenSearch/pull/14790) | Add prefix mode verification setting for repository verification | [#14741](https://github.com/opensearch-project/OpenSearch/issues/14741) |
