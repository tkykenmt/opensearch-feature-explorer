---
tags:
  - domain/search
  - component/server
  - indexing
  - k-nn
  - observability
  - performance
---
# k-NN Testing Infrastructure

## Summary

This release improves the k-NN plugin's testing infrastructure by enabling all integration tests to run against the remote index builder feature and fixing test compatibility issues with OpenSearch core changes. These improvements ensure comprehensive test coverage for the remote vector index build feature and maintain CI stability.

## Details

### What's New in v3.1.0

Two key improvements to the k-NN testing infrastructure:

1. **Remote Index Builder Integration Test Support** (PR #2659): Enables running all integration tests with the remote index builder feature, providing comprehensive validation of remote build functionality.

2. **MockNode Constructor Fix** (PR #2700): Adapts k-NN tests to changes in OpenSearch core's `MockNode` constructor, ensuring continued CI stability.

### Technical Changes

#### New Test Annotation

A new `@ExpectRemoteBuildValidation` annotation marks integration tests for explicit remote index build verification:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface ExpectRemoteBuildValidation {
}
```

Tests annotated with `@ExpectRemoteBuildValidation` trigger an `@After` method that verifies the `INDEX_BUILD_SUCCESS_COUNT` metric has been incremented, confirming remote index build was triggered.

#### GitHub Actions Workflow Updates

The `remote_index_build.yml` workflow was updated to:

- Use official `opensearchstaging/remote-vector-index-builder:api-latest` Docker image instead of personal DockerHub
- Run all integration tests (removed `-Dtests.class` filter limiting to `RemoteBuildIT`)
- Configure proper S3 endpoint URL for LocalStack: `S3_ENDPOINT_URL=http://172.17.0.1:4566`
- Add `--no-build-cache` flag for consistent test execution
- Update success log verification pattern

#### MockNode Constructor Adaptation

The `KNNSettingsTests` was updated to work with the new `MockNode` constructor that accepts `PluginInfo` objects instead of class names:

```java
Collection<PluginInfo> plugins = basePlugins().stream()
    .map(p -> new PluginInfo(
        p.getName(),
        "classpath plugin",
        "NA",
        Version.CURRENT,
        "1.8",
        p.getName(),
        null,
        Collections.emptyList(),
        false
    ))
    .collect(Collectors.toList());
return new MockNode(baseSettings().build(), plugins, configDir, true);
```

#### Test Classes with Remote Build Validation

The following integration test classes now include `@ExpectRemoteBuildValidation` annotations:

| Test Class | Description |
|------------|-------------|
| `AdvancedFilteringUseCasesIT` | Nested k-NN and filter query tests |
| `FaissHNSWFlatE2EIT` | End-to-end HNSW flat tests |
| `FaissIT` | Faiss engine tests including radius search |
| `KNNCircuitBreakerIT` | Circuit breaker functionality |
| `KNNESSettingsTestIT` | Legacy space type indexing |
| `KNNMapperSearcherIT` | Force merge and update scenarios |
| `OpenSearchIT` | Core k-NN functionality |
| `SegmentReplicationIT` | Segment replication with k-NN |
| `DerivedSourceIT` | Derived source feature tests |
| `FilteredSearchANNSearchIT` | Filtered ANN search |
| `IndexIT` | Index recall tests |
| `KNNScriptScoringIT` | Script scoring tests |
| `ModeAndCompressionIT` | Mode and compression tests |
| `NestedSearchIT` | Nested field search |
| `ConcurrentSegmentSearchIT` | Concurrent segment search |
| `MOSFaissFloatIndexIT` | Memory-optimized search tests |
| `RestTrainModelHandlerIT` | Model training tests |
| `RecallTestsIT` | Recall validation tests |

### Usage Example

To run integration tests with remote index builder locally:

```bash
# Using LocalStack for S3
docker pull localstack/localstack:latest
docker run --rm -d -p 4566:4566 localstack/localstack:latest
aws --endpoint-url=http://localhost:4566 s3 mb s3://remote-index-build-bucket

# Pull and run remote index builder
docker pull opensearchstaging/remote-vector-index-builder:api-latest
docker run --gpus all -p 80:1025 \
  -e S3_ENDPOINT_URL=http://172.17.0.1:4566 \
  -e AWS_ACCESS_KEY_ID=test \
  -e AWS_SECRET_ACCESS_KEY=test \
  opensearchstaging/remote-vector-index-builder:api-latest

# Run integration tests
./gradlew :integTestRemoteIndexBuild \
  -Ds3.enabled=true \
  -Dtest.remoteBuild=s3.localStack \
  -Dtest.bucket=remote-index-build-bucket \
  -Dtest.base_path=vectors \
  -Daccess_key=test \
  -Dsecret_key=test
```

## Limitations

- Remote index builder tests require a GPU machine for full functionality
- LocalStack is used for local testing; production tests should use real S3
- The `@ExpectRemoteBuildValidation` annotation relies on metrics verification, which may not catch all edge cases

## References

### Documentation
- [OpenSearch PR #16908](https://github.com/opensearch-project/OpenSearch/pull/16908): MockNode constructor change in OpenSearch core
- [Remote Vector Index Builder](https://github.com/opensearch-project/remote-vector-index-builder): GPU build service repository
- [Developer Guide](https://github.com/opensearch-project/k-NN/blob/main/DEVELOPER_GUIDE.md): Instructions for running tests with remote index builder

### Pull Requests
| PR | Description |
|----|-------------|
| [#2659](https://github.com/opensearch-project/k-NN/pull/2659) | Add testing support to run all ITs with remote index builder |
| [#2700](https://github.com/opensearch-project/k-NN/pull/2700) | Fix KNNSettingsTests after change in MockNode constructor |

### Issues (Design / RFC)
- [Issue #2553](https://github.com/opensearch-project/k-NN/issues/2553): Meta issue for remote vector index build integration testing support

## Related Feature Report

- Remote Vector Index Build
