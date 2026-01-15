---
tags:
  - opensearch
---
# PIT (Point In Time) API

## Summary

Added `getKeepAlive()` getter method to the `ListPitInfo` class, enabling programmatic access to the keep-alive duration of Point in Time (PIT) contexts. This was a missing API that prevented client libraries from retrieving the keep-alive value when listing PITs.

## Details

### What's New in v2.16.0

The `ListPitInfo` class now exposes the `keepAlive` property through a public getter method:

```java
public long getKeepAlive() {
    return keepAlive;
}
```

This allows client applications and integrations (such as Spring Data OpenSearch) to access the keep-alive duration when listing PIT contexts via the List All PITs API.

### Technical Changes

| Component | Change |
|-----------|--------|
| `ListPitInfo.java` | Added `getKeepAlive()` method returning the keep-alive value in milliseconds |
| Test utilities | Updated `PitTestsUtil.assertUsingGetAllPits()` to verify keep-alive values |

### API Response

The List All PITs API response includes the `keep_alive` field:

```json
{
  "pits": [
    {
      "pit_id": "...",
      "creation_time": 1718990725000,
      "keep_alive": 86400000
    }
  ]
}
```

## Limitations

- The `keepAlive` value is returned in milliseconds
- PIT contexts are lost on cluster or node failure

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14495](https://github.com/opensearch-project/OpenSearch/pull/14495) | Add ListPitInfo::getKeepAlive() getter | [spring-data-opensearch#218](https://github.com/opensearch-project/spring-data-opensearch/pull/218) |
