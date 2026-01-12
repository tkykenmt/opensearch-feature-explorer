---
tags:
  - indexing
  - security
---

# Security Analytics IOC Bug Fixes

## Summary

This release includes three bug fixes for the Security Analytics IOC (Indicators of Compromise) functionality, addressing issues with null pointer exceptions during multi-indicator type scans, incorrect IOC and findings count limits in the ListIOCs API, and index creation race conditions when indexing large numbers of IOCs.

## Details

### What's New in v2.18.0

Three critical bug fixes improve the stability and accuracy of IOC-related operations:

1. **Null Check for Multi-Indicator Type Scans** - Prevents NullPointerException when threat intel monitors are configured with multiple indicator types
2. **ListIOCs API Count Fixes** - Removes the 10,000 cap on total IOC count and findings per IOC
3. **IOC Index Exists Check** - Prevents `resource_already_exists_exception` when indexing more than 10,000 IOCs

### Technical Changes

#### Bug Fix 1: Null Check in IoCScanService

**Problem**: When a threat intel monitor was configured with multiple indicator types (e.g., IPv4, hashes, domain names), a `NullPointerException` occurred in `IoCScanService.extractIocsPerType()` because the `fields` variable could be null when iterating over indicator types.

**Solution**: Added null check for `fieldsConfiguredInMonitorForCurrentIndex` before iterating:

```java
List<String> fieldsConfiguredInMonitorForCurrentIndex = 
    iocTypeToIndexFieldMapping.getIndexToFieldsMap().get(index);
if (fieldsConfiguredInMonitorForCurrentIndex != null && 
    !fieldsConfiguredInMonitorForCurrentIndex.isEmpty()) {
    // Process fields
}
```

**Files Changed**:
- `IoCScanService.java` - Added null check in `extractIocsPerType()` method

#### Bug Fix 2: ListIOCs API Count Limits

**Problem**: The ListIOCs API had two issues:
1. Total IOC count was capped at 10,000 due to missing `trackTotalHits(true)`
2. Number of findings per IOC was capped at 10,000 because it used the GetIocFindings API which had pagination limits

**Solution**: 
1. Added `.trackTotalHits(true)` to the search request to get accurate total counts
2. Replaced the GetIocFindings API call with a direct aggregation query using terms aggregation to count findings per IOC

```java
SearchSourceBuilder findingsCountSourceBuilder = new SearchSourceBuilder()
    .fetchSource(false)
    .trackTotalHits(true)
    .query(QueryBuilders.termsQuery(IOC_ID_KEYWORD_FIELD, iocIds))
    .size(0)
    .aggregation(
        AggregationBuilders
            .terms(IOC_COUNT_AGG_NAME)
            .field(IOC_ID_KEYWORD_FIELD)
            .size(iocIds.size())
    );
```

**Files Changed**:
- `TransportListIOCsAction.java` - Refactored findings count logic to use aggregations

#### Bug Fix 3: IOC Index Exists Check

**Problem**: When indexing more than 10,000 IOCs, a `ResourceAlreadyExistsException` could occur because the batch indexing process attempted to create the same index multiple times concurrently.

**Solution**: Added exception handling in `STIX2IOCFeedStore.initFeedIndex()` to gracefully handle the case when the index already exists:

```java
if (e instanceof ResourceAlreadyExistsException || 
    (e instanceof RemoteTransportException && 
     e.getCause() instanceof ResourceAlreadyExistsException)) {
    log.debug("index {} already exist", feedIndexName);
    listener.onResponse(null);
    return;
}
```

**Files Changed**:
- `STIX2IOCFeedStore.java` - Added exists check in `initFeedIndex()` method

### Migration Notes

No migration required. These are bug fixes that improve existing functionality without changing APIs or data formats.

## Limitations

- The aggregation-based findings count still has a practical limit based on the terms aggregation bucket size, but this is configurable and much higher than the previous 10,000 limit
- Multi-indicator type monitors require proper field mappings for each indicator type in the monitored indices

## References

### Documentation
- [Threat Intelligence Documentation](https://docs.opensearch.org/2.18/security-analytics/threat-intelligence/index/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#1335](https://github.com/opensearch-project/security-analytics/pull/1335) | Add null check while adding fetched IOCs into per-indicator-type map |
| [#1373](https://github.com/opensearch-project/security-analytics/pull/1373) | Fixed ListIOCs number of findings cap |
| [#1392](https://github.com/opensearch-project/security-analytics/pull/1392) | Add exists check for IOCs index |

### Issues (Design / RFC)
- [Issue #1191](https://github.com/opensearch-project/security-analytics/issues/1191): ListIOCsAPI total hits and findings count per IOC are incorrect

## Related Feature Report

- [Threat Intelligence](../../../features/security-analytics/security-analytics-threat-intelligence.md)
