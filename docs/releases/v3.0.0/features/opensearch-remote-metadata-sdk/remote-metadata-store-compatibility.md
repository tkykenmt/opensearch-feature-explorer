---
tags:
  - search
---

# Remote Metadata Store Compatibility

## Summary

This release item updates the OpenSearch Remote Metadata SDK to be compatible with OpenSearch 3.0.0 by refactoring the `Client` import path from `org.opensearch.client.Client` to `org.opensearch.transport.client.Client`. This change aligns with the JPMS (Java Platform Module System) refactoring in OpenSearch core that moved the client package to resolve split package issues.

## Details

### What's New in v3.0.0

The Remote Metadata SDK required an import path update to maintain compatibility with OpenSearch 3.0.0. The OpenSearch core team refactored the `:server` module's `org.opensearch.client` package to `org.opensearch.transport.client` as part of JPMS support work.

### Technical Changes

#### Import Path Migration

| Before (2.x) | After (3.0.0) |
|--------------|---------------|
| `org.opensearch.client.Client` | `org.opensearch.transport.client.Client` |

#### Affected Files

| File | Module |
|------|--------|
| `LocalClusterIndicesClient.java` | core |
| `SdkClientFactory.java` | core |
| `LocalClusterIndicesClientTests.java` | core (test) |
| `SdkClientFactoryTests.java` | core (test) |
| `AOSSdkClientFactoryTests.java` | aos-client (test) |
| `DDBSdkClientFactoryTests.java` | ddb-client (test) |
| `RemoteSdkClientFactoryTests.java` | remote-client (test) |

### Migration Notes

Plugin developers using the Remote Metadata SDK with OpenSearch 3.0.0 should ensure they are using the 3.0.0 version of the SDK. No code changes are required in consuming plugins as the SDK handles the client interface internally.

## Limitations

- This is a breaking change from OpenSearch 2.x - plugins must use the matching SDK version for their OpenSearch version

## References

### Documentation
- [PR #73](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/73): Import path update
- [OpenSearch PR #17272](https://github.com/opensearch-project/OpenSearch/pull/17272): JPMS refactoring in OpenSearch core

### Pull Requests
| PR | Description |
|----|-------------|
| [opensearch-remote-metadata-sdk#73](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/73) | Update o.o.client imports to o.o.transport.client |
| [OpenSearch#17272](https://github.com/opensearch-project/OpenSearch/pull/17272) | [JPMS Support] Refactoring of `org.opensearch.client` from `:server` module |

### Issues (Design / RFC)
- [Issue #8110](https://github.com/opensearch-project/OpenSearch/issues/8110): JPMS support tracking issue

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-remote-metadata-sdk/opensearch-remote-metadata-sdk-remote-metadata-sdk.md)
