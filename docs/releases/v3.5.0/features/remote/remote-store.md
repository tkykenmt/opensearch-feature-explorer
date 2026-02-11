---
tags:
  - remote
---
# Remote Store

## Summary

This release adds utility methods to the OpenSearch Remote Metadata SDK that simplify ActionListener handling when using async operations with CompletableFuture's `whenComplete` method. These wrapper methods handle response parsing and exception unwrapping automatically, significantly reducing boilerplate code for plugin developers migrating to the SDK.

## Details

### What's New in v3.5.0

#### ActionListener Completion Wrappers

New utility methods in `SdkClientUtils` wrap async operation completions into ActionListener-compatible format:

| Method | Description |
|--------|-------------|
| `wrapPutCompletion()` | Wraps PUT operation completion, parses `IndexResponse` |
| `wrapGetCompletion()` | Wraps GET operation completion, parses `GetResponse` |
| `wrapUpdateCompletion()` | Wraps UPDATE operation completion, parses `UpdateResponse` |
| `wrapDeleteCompletion()` | Wraps DELETE operation completion, parses `DeleteResponse` |
| `wrapBulkCompletion()` | Wraps BULK operation completion, parses `BulkResponse` |
| `wrapSearchCompletion()` | Wraps SEARCH operation completion, parses `SearchResponse` |

#### Migration Example

Before (manual handling):
```java
sdkClient.getDataObjectAsync(getRequest).whenComplete((response, throwable) -> {
    if (throwable == null) {
        try {
            GetResponse getResponse = response.parser() == null 
                ? null 
                : GetResponse.fromXContent(response.parser());
            listener.onResponse(getResponse);
        } catch (IOException e) {
            listener.onFailure(new OpenSearchStatusException("Failed to parse", INTERNAL_SERVER_ERROR));
        }
    } else {
        listener.onFailure(unwrapException(throwable));
    }
});
```

After (using wrapper):
```java
sdkClient.getDataObjectAsync(getRequest).whenComplete(SdkClientUtils.wrapGetCompletion(listener));
```

#### Exception Handling

The wrapper methods automatically unwrap exceptions, defaulting to unwrap both `CompletionException` (typical for CompletableFuture) and `OpenSearchStatusException` (current wrapper for client implementations). Callers can optionally override this with custom exception types via vararg parameters.

### Infrastructure Updates

- Updated `aws-actions/configure-aws-credentials` GitHub Action from v4.0.3 to v4.1.0 for snapshot publishing workflow

## Limitations

- Wrapper methods return `null` response when parser is `null`
- Parse failures result in `OpenSearchStatusException` with `INTERNAL_SERVER_ERROR` status

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#75](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/75) | Add util methods to handle ActionListeners in whenComplete | [#67](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/67) |
| [#76](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/76) | Update aws-actions/configure-aws-credentials action to v4.1.0 | - |
