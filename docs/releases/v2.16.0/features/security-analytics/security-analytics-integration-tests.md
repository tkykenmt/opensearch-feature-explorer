---
tags:
  - security-analytics
---
# Security Analytics Integration Tests

## Summary

Bug fixes for Security Analytics integration tests and error handling improvements in v2.16.0. These changes improve test stability and provide better error handling when correlation alert indices don't exist.

## Details

### What's New in v2.16.0

#### Integration Test Fixes (PR #1082)

Fixed flaky integration tests by removing unnecessary explicit refresh calls that were causing timing issues. The changes affect multiple test files:

- `SecurityAnalyticsRestTestCase.java`
- `AlertsIT.java`
- `SecureAlertsRestApiIT.java`
- `FindingIT.java`
- `SecureFindingRestApiIT.java`
- `MapperRestApiIT.java`

#### IndexNotFoundException Handling (PR #1125)

Improved error handling in `CorrelationAlertService` to gracefully handle cases where the correlation alerts index doesn't exist yet. Instead of throwing an exception, the service now returns an empty response.

```java
// Before: Exception thrown when index not found
listener.onFailure(e);

// After: Return empty response for IndexNotFoundException
if (e instanceof IndexNotFoundException) {
    listener.onResponse(new GetCorrelationAlertsResponse(Collections.emptyList(), 0));
} else {
    listener.onFailure(e);
}
```

### Technical Changes

| Change | Description |
|--------|-------------|
| Test refresh removal | Commented out explicit `_refresh` API calls in integration tests |
| IndexNotFoundException handling | Return empty array instead of error when correlation alerts index doesn't exist |

## Limitations

- These are internal bug fixes with no user-facing API changes
- The IndexNotFoundException fix only applies to correlation alerts queries

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1082](https://github.com/opensearch-project/security-analytics/pull/1082) | Pass integ tests | - |
| [#1125](https://github.com/opensearch-project/security-analytics/pull/1125) | Set blank response when indexNotFound exception | - |
