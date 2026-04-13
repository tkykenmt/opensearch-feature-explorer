---
tags:
  - ml-commons
---
# ML Commons Infrastructure

## Summary

OpenSearch v3.6.0 includes 10 infrastructure-level fixes for the ML Commons plugin, addressing connection pool exhaustion from leaked HTTP clients, incorrect timeout defaults, telemetry tag loss, classloader resolution failures, numeric type handling in inference queries, stats collector early exits, broader 4XX error handling, and multiple CI/integration test stability improvements.

## Details

### What's New in v3.6.0

#### Connection Pool Exhaustion Fix (Critical)

`SdkAsyncHttpClient` instances created in `AwsConnectorExecutor` and `HttpJsonConnectorExecutor` were never closed, leaking Netty event loop threads and connection pools. This caused `"Acquire operation took longer than the configured maximum time"` errors under load.

- `RemoteConnectorExecutor` now extends `AutoCloseable`
- `AwsConnectorExecutor` and `HttpJsonConnectorExecutor` implement `close()` to atomically clear and close the `SdkAsyncHttpClient`
- `RemoteModel.close()` calls `connectorExecutor.close()` before nulling the reference
- Short-lived executors in `ExecuteConnectorTransportAction`, `GetTaskTransportAction`, `CancelBatchJobTransportAction`, and `RemoteAgenticConversationMemory` are now properly closed in both `onResponse` and `onFailure` callbacks

#### Timeout Default Fix (Critical)

`ConnectorClientConfig` default values for `connection_timeout` and `read_timeout` were `30000`, but the code passed these through `Duration.ofSeconds()`, resulting in effective timeouts of ~8.3 hours instead of 30 seconds. Defaults changed from `30000` to `30`.

#### Telemetry Tags Fix

The OpenSearch core `Tags` class changed from mutable to immutable implementation. `Tags.addTag()` now returns a new `Tags` instance instead of mutating in place. Several call sites in `MLModel` and `MLAgent` did not capture the return value, silently dropping tags for model format, URL, memory type, and LLM interface fields.

#### Classloader Fallback for Model Deserialization

`ValidatingObjectInputStream.resolveClass()` now falls back to the plugin classloader (`ModelSerDeSer.class.getClassLoader()`) when the default classloader cannot find a class. Security validation is preserved — rejected classes still throw `InvalidClassException`.

#### Numeric Type Preservation in ML Inference

Fixed ML inference range query rewrite integration test where the entire embedding array was substituted instead of its length due to post-process function transforming the response into a `ModelTensor` with `dataAsMap=null`.

#### Stats Collector Early Exit Fix

Fixed early exit in the stats collector job when a connector is fetched for model details, which prevented complete statistics collection.

#### Broader 4XX Error Handling

Error handling updated from `OpenSearchStatusException` to `OpenSearchException` for 4XX client error preservation. This covers additional exception types like `IndexNotFoundException` and `ResourceNotFoundException` that were previously masked as 500 errors. Affected components: `MemoryProcessingService`, `TransportAddMemoriesAction`, `TransportCreateSessionAction`, `MLPredictTaskRunner`.

#### CI/Integration Test Stability

- Disabled dedicated masters in `SearchModelGroupITTests` to prevent random 5-JVM cluster configurations causing suite timeouts
- Increased Bedrock connector `max_connection` to 200 for concurrent test environments
- Updated Cohere connector model from deprecated `command-r` to `command-r-08-2024` for v1 Chat API compatibility
- Added `isServiceReachable()` helper to gracefully skip tests when external services are unreachable
- `waitForTask()` now exits immediately on `FAILED`/`CANCELLED` states instead of looping until suite timeout
- Increased Cohere connector timeout to 120s with reachability checks
- Added `bc-fips` to unit test classpath via detached configuration for FIPS mode

#### Nova Clean Request Helper

Added helper method for Amazon Nova clean request handling in connector utilities.

## Limitations

- The `connection_timeout` and `read_timeout` default change from `30000` to `30` is a behavioral change — users who relied on the (unintentionally large) timeout values may need to explicitly configure longer timeouts
- Connection pool exhaustion may still occur if custom connector executors do not implement `AutoCloseable`

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#4716](https://github.com/opensearch-project/ml-commons/pull/4716) | Fix SdkAsyncHttpClient resource leak in connector executors |   |
| [#4759](https://github.com/opensearch-project/ml-commons/pull/4759) | Fix connection_timeout and read_timeout defaults from 30000 to 30 |   |
| [#4712](https://github.com/opensearch-project/ml-commons/pull/4712) | Fix Tags.addTag() return value not captured after immutable Tags change |   |
| [#4692](https://github.com/opensearch-project/ml-commons/pull/4692) | Override ValidatingObjectInputStream.resolveClass() for plugin classloader fallback |   |
| [#4656](https://github.com/opensearch-project/ml-commons/pull/4656) | Fix numeric type preservation in ML inference query template substitution |   |
| [#4560](https://github.com/opensearch-project/ml-commons/pull/4560) | Fix early exit in stats collector job | [#4539](https://github.com/opensearch-project/ml-commons/issues/4539) |
| [#4725](https://github.com/opensearch-project/ml-commons/pull/4725) | Fix error handling to use OpenSearchException for broader 4XX coverage | [#4724](https://github.com/opensearch-project/ml-commons/issues/4724) |
| [#4665](https://github.com/opensearch-project/ml-commons/pull/4665) | Prevent SearchModelGroupITTests timeout and fix Bedrock connection pool exhaustion |   |
| [#4767](https://github.com/opensearch-project/ml-commons/pull/4767) | Fix Cohere integration test timeouts with increased timeout and reachability checks |   |
| [#4676](https://github.com/opensearch-project/ml-commons/pull/4676) | Add helper method for Nova clean request |   |
