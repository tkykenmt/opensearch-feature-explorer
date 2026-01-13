---
tags:
  - domain/ml
  - component/server
  - indexing
  - ml
---
# ML Commons Testing & Coverage

## Summary

This release item improves the testing infrastructure and code coverage for the ML Commons plugin. The changes include fixing integration test stability issues, adding comprehensive unit tests for memory container functionality, and upgrading the JaCoCo code coverage tool.

## Details

### What's New in v3.2.0

The ML Commons plugin received significant testing improvements in v3.2.0:

1. **Integration Test Stability Fix**: Resolved a critical issue where integration tests would fail intermittently due to master key inconsistency in the `.plugins-ml-config` index
2. **Memory Container Unit Tests**: Added comprehensive unit tests for the new memory container feature
3. **JaCoCo Upgrade**: Upgraded JaCoCo from 0.8.12 to 0.8.13 for improved code coverage reporting
4. **SearchIndexTool Improvements**: Enhanced argument parsing logic for better MCP compatibility

### Technical Changes

#### Integration Test Fix (PR #3989)

The fix addresses a race condition in integration tests where:
- The `.plugins-ml-config` index was being deleted between tests
- The `MLSyncUpJob` (running every 10 seconds) would recreate the index with a new master key
- This caused "tag mismatch" exceptions when connectors encrypted with the old key were decrypted with the new key

**Solution**: The `.plugins-ml-config` index is now preserved during test cleanup to maintain master key consistency.

```java
// Before: Index was deleted
if (indexName != null && !".opendistro_security".equals(indexName)) {
    adminClient().performRequest(new Request("DELETE", "/" + indexName));
}

// After: Index is preserved
if (indexName != null && !".opendistro_security".equals(indexName) 
    && !".plugins-ml-config".equals(indexName)) {
    adminClient().performRequest(new Request("DELETE", "/" + indexName));
}
```

#### Memory Container Unit Tests (PRs #4056, #4057)

Added comprehensive test coverage for memory container functionality:

| Test Class | Coverage Area |
|------------|---------------|
| `MLMemoryContainerTests` | Memory container model serialization/deserialization |
| `MemoryStorageConfigTests` | Storage configuration validation |
| `MLCreateMemoryContainerInputTests` | Create request input validation |
| `MLCreateMemoryContainerRequestTests` | Transport request handling |
| `MLCreateMemoryContainerResponseTests` | Response serialization |
| `MLMemoryContainerGetRequestTests` | Get request validation |
| `MLMemoryContainerGetResponseTests` | Get response handling |
| `TransportCreateMemoryContainerActionTests` | Create action business logic |
| `TransportGetMemoryContainerActionTests` | Get action with access control |
| `RestMLCreateMemoryContainerActionTests` | REST API create endpoint |
| `RestMLGetMemoryContainerActionTests` | REST API get endpoint |

#### SearchIndexTool Enhancement (PR #3883)

Improved argument parsing to support both MCP and ReAct agent schemas:

```java
// Now supports both formats:
// 1. Arguments from "input" key (ReAct agent)
// 2. Arguments directly from parameters (MCP)
String index = Optional.ofNullable(jsonObject)
    .map(x -> x.get(INDEX_FIELD))
    .map(JsonElement::getAsString)
    .orElse(parameters.getOrDefault(INDEX_FIELD, null));
```

### JaCoCo Coverage Exclusions Removed

The following classes were removed from JaCoCo exclusions as they now have test coverage:

- `TransportCreateMemoryContainerAction`
- `TransportGetMemoryContainerAction`
- `TransportAddMemoryAction`
- `RestMLCreateMemoryContainerAction`
- `RestMLGetMemoryContainerAction`
- `RestMLAddMemoryAction`

## Limitations

- The integration test fix is specific to the ML Commons test infrastructure
- Memory container tests focus on unit testing; integration tests are planned for future releases

## References

### Documentation
- [ML Commons Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/): Official ML Commons docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#3883](https://github.com/opensearch-project/ml-commons/pull/3883) | SearchIndexTool arguments parsing logic improvement |
| [#3989](https://github.com/opensearch-project/ml-commons/pull/3989) | Keep .plugins-ml-config index for integration tests |
| [#4056](https://github.com/opensearch-project/ml-commons/pull/4056) | Unit tests for create and get memory container |
| [#4057](https://github.com/opensearch-project/ml-commons/pull/4057) | Additional unit tests and JaCoCo upgrade |

### Issues (Design / RFC)
- [Issue #2560](https://github.com/opensearch-project/ml-commons/issues/2560): Related to master key consistency
- [Issue #3834](https://github.com/opensearch-project/ml-commons/issues/3834): MCP tool schema alignment

## Related Feature Report

- ML Commons Agent Framework
