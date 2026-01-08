# Remote Metadata Store Documentation

## Summary

This release item adds a comprehensive developer guide to the OpenSearch Remote Metadata SDK repository. The guide provides step-by-step instructions for plugin developers to integrate the SDK, enabling stateless OpenSearch plugins that use external data stores instead of local system indices.

## Details

### What's New in v3.0.0

PR #124 introduces a new `DEVELOPER_GUIDE.md` file that documents how to use the Remote Metadata SDK in OpenSearch plugins. This documentation fills a critical gap for developers looking to migrate their plugins to use remote metadata storage.

### Technical Changes

#### New Documentation

The developer guide covers six key integration steps:

| Step | Description |
|------|-------------|
| 1. Declare Dependencies | Add SDK dependencies to `build.gradle` |
| 2. Initialize SDK Client | Use `SdkClientFactory` in `createComponents()` |
| 3. Inject Client | Use `@Inject` to pass `SdkClient` to classes |
| 4. Migrate API Calls | Replace NodeClient requests with SDK equivalents |
| 5. Update Exception Handling | Expand exception checks for remote storage |
| 6. Handle Multitenancy | Optional tenant ID handling |

#### Supported Remote Storage Backends

| Client | Description |
|--------|-------------|
| `remote-client` | Remote OpenSearch cluster |
| `aos-client` | Amazon OpenSearch Service (AOS) or Serverless (AOSS) |
| `ddb-client` | DynamoDB with zero-ETL replication to AOS/AOSS |

#### API Migration Reference

| NodeClient | SDK Client |
|------------|------------|
| `IndexRequest` | `PutDataObjectRequest` |
| `GetRequest` | `GetDataObjectRequest` |
| `UpdateRequest` | `UpdateDataObjectRequest` |
| `DeleteRequest` | `DeleteDataObjectRequest` |
| `SearchRequest` | `SearchDataObjectRequest` |

### Usage Example

```java
// Initialize SDK Client
SdkClient sdkClient = SdkClientFactory.createSdkClient(
    client,
    xContentRegistry,
    Map.ofEntries(
        Map.entry(REMOTE_METADATA_TYPE_KEY, REMOTE_METADATA_TYPE.get(settings)),
        Map.entry(REMOTE_METADATA_ENDPOINT_KEY, REMOTE_METADATA_ENDPOINT.get(settings)),
        Map.entry(REMOTE_METADATA_REGION_KEY, REMOTE_METADATA_REGION.get(settings)),
        Map.entry(REMOTE_METADATA_SERVICE_NAME_KEY, REMOTE_METADATA_SERVICE_NAME.get(settings)),
        Map.entry(TENANT_AWARE_KEY, "true"),
        Map.entry(TENANT_ID_FIELD_KEY, TENANT_ID_FIELD)
    ),
    client.threadPool().executor(ThreadPool.Names.GENERIC)
);

// Migrate get operation
GetDataObjectRequest getDataObjectRequest = GetDataObjectRequest.builder()
    .index(indexName)
    .id(documentId)
    .build();
sdkClient.getDataObjectAsync(getDataObjectRequest)
    .whenComplete(SdkClientUtils.wrapGetCompletion(actionListener));
```

### Migration Notes

- The SDK client does not automatically create indices (OpenSearch) or tables (DynamoDB) - these must be created manually
- Exception handling should be expanded to check both specific exceptions and generic `OpenSearchException` status codes
- For multitenancy, extract tenant ID from REST request headers and add `.tenantId(tenantId)` to request objects

## Limitations

- Manual index/table creation required before using the SDK
- Currently unused thread pool parameter may be needed in future implementations

## Related PRs

| PR | Description |
|----|-------------|
| [#124](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/124) | Add a developer guide |

## References

- [PR #124](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/124): Add a developer guide
- [DEVELOPER_GUIDE.md](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/blob/main/DEVELOPER_GUIDE.md): Full developer guide
- [Plugin as a Service Documentation](https://docs.opensearch.org/3.0/developer-documentation/plugin-as-a-service/index/): Official OpenSearch documentation
- [SDK Client Repository](https://github.com/opensearch-project/opensearch-remote-metadata-sdk): Source repository

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-remote-metadata-sdk/remote-metadata-sdk.md)
