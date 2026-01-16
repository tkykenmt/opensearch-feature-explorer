---
tags:
  - security-analytics
---
# Threat Intel IOC & Source Config

## Summary

OpenSearch v2.16.0 includes enhancements to the Threat Intelligence feature in Security Analytics, focusing on List IOC API improvements, source config model changes, and the addition of URL download as a new threat intel source type.

## Details

### What's New in v2.16.0

#### List IOC API Filter Enhancement
Added a filter to the List IOC API to fetch IOCs only from sources in `AVAILABLE` and `REFRESHING` states. This ensures users only see IOCs from active, valid sources and prevents errors when querying IOCs from sources that are still being created or have failed.

- Added null check for alias of IOC indices to prevent NPE errors
- IOCs from sources in `CREATING`, `FAILED`, or `DELETING` states are now excluded from results

#### Default Store Config Model Changes
Updated the threat intel default store config model to:
- Ensure no duplicates in `ioc_types` field
- Allow partial IOC downloads based on specified `ioc_types`
- Fail source creation if no IOC types are present

#### URL Download Source Type
Added `URL_DOWNLOAD` as a new threat intel source config type, enabling users to download IOCs directly from a URL endpoint. This complements the existing `S3_CUSTOM` and `IOC_UPLOAD` source types.

```json
POST _plugins/_security_analytics/threat_intel/sources/
{
  "type": "URL_DOWNLOAD",
  "name": "external-threat-feed",
  "format": "STIX2",
  "enabled": true,
  "schedule": {
    "interval": {
      "start_time": 1717097122,
      "period": "1",
      "unit": "DAYS"
    }
  },
  "source": {
    "url": {
      "url": "https://example.com/threat-feed.json"
    }
  },
  "ioc_types": ["ipv4-addr", "domain-name"]
}
```

### Technical Changes

| Change | Description |
|--------|-------------|
| List IOC API filter | Only returns IOCs from AVAILABLE/REFRESHING sources |
| Null check for aliases | Prevents NPE when IOC index alias is null |
| Store config validation | Ensures unique ioc_types and fails on empty list |
| URL_DOWNLOAD type | New source type for downloading IOCs from URLs |

## Limitations

- URL_DOWNLOAD sources require the URL to be accessible from the OpenSearch cluster
- URL endpoints must return data in a supported format (e.g., STIX2)
- Schedule-based refresh is required for URL_DOWNLOAD sources

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1131](https://github.com/opensearch-project/security-analytics/pull/1131) | Add filter to list IOC API for available/refreshing sources |  |
| [#1133](https://github.com/opensearch-project/security-analytics/pull/1133) | Changes threat intel default store config model |  |
| [#1142](https://github.com/opensearch-project/security-analytics/pull/1142) | Adds new TIF source config type - URL download |  |
