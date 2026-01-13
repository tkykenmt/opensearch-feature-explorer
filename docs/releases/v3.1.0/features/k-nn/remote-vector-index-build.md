---
tags:
  - domain/search
  - component/server
  - indexing
  - k-nn
  - observability
  - performance
---
# Remote Vector Index Build Enhancements

## Summary

OpenSearch v3.1.0 brings significant enhancements to the Remote Vector Index Build feature, preparing it for General Availability (GA). Key changes include tuned repository upload/download buffer sizes based on benchmarking results, a new segment size upper bound setting to prevent GPU OOM errors, renamed settings for consistency, and improved metrics accuracy with better exception logging.

## Details

### What's New in v3.1.0

1. **Tuned Repository Buffer Sizes**: Optimized upload/download buffer sizes based on extensive benchmarking with cohere-100k and cohere-1m datasets
2. **Segment Size Upper Bound**: New cluster setting to prevent GPU OOM by failing fast for oversized segments
3. **GA Settings Preparation**: Settings renamed from feature flag pattern to production-ready naming
4. **Metrics Fix**: Corrected timing for remote build metrics when falling back to CPU
5. **GPU Index Setting Fix**: GPU index setting now defaults to true and is only evaluated when cluster setting is enabled

### Technical Changes

#### Buffer Size Optimizations

Based on benchmarking on `r6g.4xlarge` instances with 3 data nodes:

| Buffer Type | New Size | Rationale |
|-------------|----------|-----------|
| Vector Upload | 50 MB | Optimal throughput without excessive memory |
| Doc ID Upload | 8 KB | Conservative for small doc ID files |
| Index Download | 50 MB | Improved download throughput (48→60 MiB/s) |

Benchmarking showed download throughput improved from ~48 MiB/s (64KB default) to ~60 MiB/s with 200MB buffers. The 50MB setting balances performance with memory usage since the minimum remote build threshold is 50MB.

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `knn.remote_index_build.enabled` | Cluster-level enable (moved from feature flag) | `false` |
| `knn.remote_index_build.repository` | Repository name (renamed from `vector_repo`) | - |
| `knn.remote_index_build.size.max` | Upper bound for segment size | `0` (no limit) |
| `knn.remote_index_build.service.endpoint` | Build service URL (renamed) | - |
| `knn.remote_index_build.poll.interval` | Status poll interval (renamed) | `5s` |
| `knn.remote_index_build.service.username` | Auth username (renamed) | - |
| `knn.remote_index_build.service.password` | Auth password (renamed) | - |
| `index.knn.remote_index_build.size.min` | Min segment size (renamed from `size_threshold`) | `50mb` |

#### Settings Migration

| Old Setting (v3.0.0) | New Setting (v3.1.0) |
|---------------------|---------------------|
| `knn.feature.remote_index_build.enabled` | `knn.remote_index_build.enabled` |
| `knn.remote_index_build.vector_repo` | `knn.remote_index_build.repository` |
| `knn.remote_index_build.client.endpoint` | `knn.remote_index_build.service.endpoint` |
| `knn.remote_index_build.client.poll_interval` | `knn.remote_index_build.poll.interval` |
| `knn.remote_index_build.client.username` | `knn.remote_index_build.service.username` |
| `knn.remote_index_build.client.password` | `knn.remote_index_build.service.password` |
| `index.knn.remote_index_build.size_threshold` | `index.knn.remote_index_build.size.min` |

### Usage Example

```yaml
# Configure cluster settings with new naming
PUT _cluster/settings
{
  "persistent": {
    "knn.remote_index_build.enabled": true,
    "knn.remote_index_build.repository": "vector-repo",
    "knn.remote_index_build.service.endpoint": "http://gpu-builder:8080",
    "knn.remote_index_build.size.max": "10gb"
  }
}

# Create index with remote build
PUT my-vectors
{
  "settings": {
    "index.knn": true,
    "index.knn.remote_index_build.enabled": true,
    "index.knn.remote_index_build.size.min": "100mb"
  },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "name": "hnsw",
          "engine": "faiss"
        }
      }
    }
  }
}
```

### Migration Notes

Users upgrading from v3.0.0 must update their cluster and index settings to use the new setting names. The old settings will not be recognized in v3.1.0.

## Limitations

- **Experimental Status**: Feature remains experimental
- **Engine Support**: Only Faiss engine with HNSW method
- **Vector Type**: Only 32-bit floating-point (FP32) vectors
- **Repository**: Only Amazon S3 repositories
- **Size Bounds**: Segments exceeding `knn.remote_index_build.size.max` fall back to CPU build

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/vector-search/remote-index-build/): Remote index build docs
- [Settings Reference](https://docs.opensearch.org/3.0/vector-search/settings/): k-NN settings documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#2662](https://github.com/opensearch-project/k-NN/pull/2662) | Add tuned repository upload/download buffer sizes |
| [#2734](https://github.com/opensearch-project/k-NN/pull/2734) | Add segment size upper bound setting and GA settings changes |
| [#2693](https://github.com/opensearch-project/k-NN/pull/2693) | Fix remote build metrics timing and add exception logging |
| [#2743](https://github.com/opensearch-project/k-NN/pull/2743) | Fix GPU index setting to only evaluate when cluster setting is set |

### Issues (Design / RFC)
- [Issue #2732](https://github.com/opensearch-project/k-NN/issues/2732): Upper bound setting request
- [Issue #2595](https://github.com/opensearch-project/k-NN/pull/2595): Benchmarking results for buffer sizes

## Related Feature Report

- Full feature documentation
