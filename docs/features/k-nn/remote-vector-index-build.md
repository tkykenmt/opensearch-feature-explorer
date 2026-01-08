# Remote Vector Index Build

## Summary

Remote Vector Index Build is an experimental feature that enables OpenSearch to offload vector index construction to external GPU-accelerated services. By leveraging GPUs for the computationally intensive HNSW graph building process, this feature dramatically reduces index build times and operational costs for large-scale vector search workloads.

The feature introduces a client-server architecture where OpenSearch uploads vectors to an intermediate object store (Amazon S3), a remote GPU-powered service builds the index, and OpenSearch downloads the completed index for use in search operations.

## Details

### Architecture

```mermaid
graph TB
    subgraph OpenSearch Cluster
        KNN[k-NN Plugin]
        RBS[RemoteIndexBuildStrategy]
        RC[RemoteIndexClient]
        RW[RemoteIndexWaiter]
        RS[Repository Service]
    end
    
    subgraph Object Store
        S3[(Amazon S3)]
    end
    
    subgraph Remote Build Service
        API[Build API]
        GPU[GPU Workers]
        FAISS[Faiss Library]
    end
    
    KNN --> RBS
    RBS -->|Decide Local/Remote| RC
    RBS --> RS
    RS -->|Upload Vectors + DocIDs| S3
    RC -->|POST /build| API
    API --> GPU
    GPU --> FAISS
    FAISS -->|Read Vectors| S3
    FAISS -->|Write Index| S3
    RW -->|Poll Status| API
    RS -->|Download Index| S3
```

### Data Flow

```mermaid
flowchart TB
    subgraph Indexing
        A[Documents] --> B[Extract Vectors]
        B --> C{Size > Threshold?}
        C -->|Yes| D[Remote Build]
        C -->|No| E[Local Build]
    end
    
    subgraph Remote Build
        D --> F[Upload to S3]
        F --> G[Submit Build Request]
        G --> H[Poll for Completion]
        H --> I[Download Index]
    end
    
    subgraph Local Build
        E --> J[Build HNSW Graph]
    end
    
    I --> K[Merge with Segment]
    J --> K
```

### Components

| Component | Description |
|-----------|-------------|
| `RemoteIndexBuildStrategy` | Decides whether to use local or remote build based on segment size threshold |
| `RemoteIndexClient` | Interface for communicating with remote build services |
| `RemoteIndexHTTPClient` | HTTP client implementation with connection pooling and retry logic |
| `RemoteIndexWaiter` | Interface for awaiting build completion |
| `RemoteIndexPoller` | Polling-based implementation that checks build status periodically |
| `RemoteBuildRequest` | Request object containing vectors, parameters, and S3 paths |
| `RemoteBuildResponse` | Response object with build status and result file location |
| `remote-index-build-client` | Separate Gradle module for client code (supports future extraction) |

### Configuration

| Setting | Description | Default | Dynamic |
|---------|-------------|---------|---------|
| `knn.feature.remote_index_build.enabled` | Enable remote build feature for the cluster | `false` | Yes |
| `index.knn.remote_index_build.enabled` | Enable remote build for specific index | `false` | Yes |
| `knn.remote_index_build.client.endpoint` | URL of the remote build service | - | Yes |
| `knn.remote_index_build.vector_repo` | Name of registered S3 repository | - | Yes |
| `index.knn.remote_index_build.size_threshold` | Minimum segment size (bytes) to trigger remote build | - | Yes |

### Metrics

Remote build statistics are exposed via the k-NN stats API (`GET /_plugins/_knn/stats`):

**Repository Stats**
- `read_success_count` / `read_failure_count`: S3 read operations
- `write_success_count` / `write_failure_count`: S3 write operations
- `successful_read_time_in_millis` / `successful_write_time_in_millis`: Latency metrics

**Client Stats**
- `build_request_success_count` / `build_request_failure_count`: Build submission
- `status_request_success_count` / `status_request_failure_count`: Status polling
- `index_build_success_count` / `index_build_failure_count`: Overall build outcomes
- `waiting_time_in_ms`: Total time spent waiting for builds

**Build Stats**
- `remote_index_build_flush_time_in_millis`: Time for flush-triggered builds
- `remote_index_build_merge_time_in_millis`: Time for merge-triggered builds
- `remote_index_build_current_flush_operations`: In-progress flush builds
- `remote_index_build_current_merge_operations`: In-progress merge builds

### Usage Example

```yaml
# Step 1: Register S3 repository
PUT _snapshot/vector-repo
{
  "type": "s3",
  "settings": {
    "bucket": "my-vector-bucket",
    "base_path": "vectors"
  }
}

# Step 2: Enable remote build cluster-wide
PUT _cluster/settings
{
  "persistent": {
    "knn.feature.remote_index_build.enabled": true,
    "knn.remote_index_build.client.endpoint": "http://gpu-builder.example.com:8080",
    "knn.remote_index_build.vector_repo": "vector-repo"
  }
}

# Step 3: Create index with remote build
PUT my-vectors
{
  "settings": {
    "index.knn": true,
    "index.knn.remote_index_build.enabled": true
  },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "parameters": {
            "m": 16,
            "ef_construction": 100
          }
        }
      }
    }
  }
}

# Step 4: Index documents (remote build happens automatically)
POST my-vectors/_bulk
{"index": {}}
{"embedding": [0.1, 0.2, ...]}
```

## Limitations

- **Experimental Status**: Feature is experimental and not recommended for production
- **Engine Support**: Only Faiss engine with HNSW method
- **Vector Type**: Only 32-bit floating-point (FP32) vectors
- **Encoder**: Only flat encoding (HNSWFlat), no product quantization
- **Repository**: Only Amazon S3 repositories
- **Space Types**: L2, inner product, and cosine similarity
- **Network**: Requires connectivity between OpenSearch, S3, and build service

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.0.0 | [#2576](https://github.com/opensearch-project/k-NN/pull/2576) | Client polling, encoder validation, parameter retrieval |
| v3.0.0 | [#2603](https://github.com/opensearch-project/k-NN/pull/2603) | Separate client module for reduced dependencies |
| v3.0.0 | [#2615](https://github.com/opensearch-project/k-NN/pull/2615) | Metric collection for monitoring |
| v3.0.0 | [#2627](https://github.com/opensearch-project/k-NN/pull/2627) | COSINESIMIL space type fix |

## References

- [Issue #2391](https://github.com/opensearch-project/k-NN/issues/2391): Meta issue tracking all remote build work
- [Issue #2518](https://github.com/opensearch-project/k-NN/issues/2518): Low-level design document
- [Documentation](https://docs.opensearch.org/3.0/vector-search/remote-index-build/): Official OpenSearch docs
- [Remote Vector Index Builder](https://github.com/opensearch-project/remote-vector-index-builder): GPU build service
- [User Guide](https://github.com/opensearch-project/remote-vector-index-builder/blob/main/USER_GUIDE.md): Service setup instructions
- [GPU Acceleration Blog](https://opensearch.org/blog/GPU-Accelerated-Vector-Search-OpenSearch-New-Frontier/): Performance benchmarks

## Change History

- **v3.0.0** (2025-05-06): Initial experimental implementation with HTTP client, S3 repository integration, metrics, and COSINESIMIL support
