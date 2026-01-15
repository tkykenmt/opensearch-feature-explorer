---
tags:
  - opensearch
---
# System Index Warning

## Summary

This change improves the handling of system index access warnings in the OpenSearch test framework. The `refreshAllIndices` method in `OpenSearchRestTestCase` now correctly ignores multiple system index warnings instead of only handling a single warning.

## Details

### What's New in v2.16.0

The `OpenSearchRestTestCase.refreshAllIndices()` method was updated to properly handle multiple system index access warnings. Previously, the warning handler only checked if there was exactly one warning and if it started with "this request accesses system indices:". This caused test failures when multiple system indices were accessed in a single refresh operation.

### Technical Changes

The warning handler logic was refactored from:

```java
if (warnings.isEmpty()) {
    return false;
} else if (warnings.size() > 1) {
    return true;
} else {
    return warnings.get(0).startsWith("this request accesses system indices:") == false;
}
```

To:

```java
if (warnings.isEmpty()) {
    return false;
}
boolean allSystemIndexWarnings = true;
for (String warning : warnings) {
    if (!warning.startsWith("this request accesses system indices:")) {
        allSystemIndexWarnings = false;
        break;
    }
}
return !allSystemIndexWarnings;
```

This change allows the test framework to ignore any number of system index warnings as long as all warnings are related to system index access.

### Affected Components

| Component | Description |
|-----------|-------------|
| `OpenSearchRestTestCase` | Base class for REST integration tests |
| `refreshAllIndices()` | Method that refreshes all indices including hidden ones |

### Use Case

This fix is particularly important for plugins that create multiple system indices, such as:
- Alerting plugin (`.opendistro-alerting-*`)
- Notifications plugin (`.opensearch-notifications-*`)
- Security plugin (`.opendistro_security`)

When running integration tests that refresh all indices, the previous implementation would fail if multiple system indices existed.

## Limitations

- This change only affects the test framework and does not modify production behavior
- System index warnings are still generated; they are just properly ignored in tests

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14635](https://github.com/opensearch-project/OpenSearch/pull/14635) | Allow system index warning in OpenSearchRestTestCase.refreshAllIndices | Related to [alerting#1584](https://github.com/opensearch-project/alerting/pull/1584) |
