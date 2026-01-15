---
tags:
  - opensearch
---
# System Index Warning Handling

## Summary

OpenSearch provides mechanisms to handle system index access warnings in the test framework. System indices are protected indexes used internally by OpenSearch and its plugins to store configuration and operational data. When tests access these indices, warnings are generated to indicate that direct access to system indices will be restricted in future versions.

## Details

### Overview

System indices in OpenSearch (prefixed with `.`) are protected and used by various plugins:
- `.opendistro_security` - Security plugin configuration
- `.opendistro-alerting-*` - Alerting plugin data
- `.opensearch-notifications-*` - Notifications configuration
- `.opendistro-anomaly-*` - Anomaly detection data

When REST API operations like `/_refresh` access these indices, OpenSearch generates warnings to inform users that direct access to system indices will be prevented by default in future major versions.

### Test Framework Support

The `OpenSearchRestTestCase` class provides a `refreshAllIndices()` method that refreshes all indices including hidden system indices. This method includes a custom warning handler to suppress system index access warnings during testing.

### Warning Handler Behavior

The warning handler in `refreshAllIndices()`:
1. Returns `false` (no failure) if there are no warnings
2. Iterates through all warnings to check if they are system index warnings
3. Returns `false` (no failure) only if ALL warnings are system index access warnings
4. Returns `true` (failure) if any non-system-index warning is present

### Configuration

System indices can be configured in `opensearch.yml`:

```yaml
plugins.security.system_indices.enabled: true
plugins.security.system_indices.indices:
  - ".opendistro-alerting-config"
  - ".opendistro-alerting-alert*"
  - ".opendistro-anomaly-results*"
  - ".opensearch-notifications-*"
```

## Limitations

- System index warnings are informational and do not affect functionality in current versions
- Direct access to system indices may be restricted in future major versions
- The warning suppression only applies to the test framework, not production code

## Change History

- **v2.16.0** (2024-07-05): Fixed handling of multiple system index warnings in `OpenSearchRestTestCase.refreshAllIndices()` ([#14635](https://github.com/opensearch-project/OpenSearch/pull/14635))

## References

### Documentation

- [System Indexes](https://docs.opensearch.org/latest/security/configuration/system-indices/)

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#14635](https://github.com/opensearch-project/OpenSearch/pull/14635) | Allow system index warning in OpenSearchRestTestCase.refreshAllIndices |
