# Events Correlation Engine

## Summary

The Events Correlation Engine plugin was **removed from OpenSearch core** in v3.0.0. The plugin, originally proposed in [Issue #6854](https://github.com/opensearch-project/OpenSearch/issues/6854), was never completed in the core repository and was removed via [PR #16885](https://github.com/opensearch-project/OpenSearch/pull/16885). The correlation engine functionality is available through the **Security Analytics plugin** instead.

## Details

### What's New in v3.0.0

The events-correlation-engine plugin code was removed from the OpenSearch core repository. This is a cleanup change rather than a feature removal, as the plugin was never backported to any release and the implementation was incomplete.

### Background

The Events Correlation Engine was originally designed as an "Events Knowledge Graph" to:
- Identify and store connected events data across multiple indices or data streams
- Generate insights by correlating recent/historical data based on time windows
- Allow customers to define Correlation Rules to automatically generate correlations between events from different log sources

### Technical Changes

#### Plugin Removal
The incomplete events-correlation-engine plugin was removed from the OpenSearch core repository. The decision was made to move this functionality to a separate repository, but the implementation was never completed in core.

#### Migration Path
Users seeking correlation capabilities should use the **Security Analytics plugin**, which provides:
- Correlation engine for security findings
- Correlation rules to define threat scenarios across log types
- Correlation graph visualization in OpenSearch Dashboards
- APIs for creating correlation rules and querying correlations

### Usage Example

The correlation engine functionality is available through Security Analytics:

```json
// Create a correlation rule via Security Analytics API
POST /_plugins/_security_analytics/correlation/rules
{
  "correlate": [
    {
      "index": "vpc_flow",
      "query": "dstaddr:4.5.6.7 or dstaddr:4.5.6.6",
      "category": "network"
    },
    {
      "index": "windows",
      "query": "winlog.event_data.SubjectDomainName:NTAUTHORI*",
      "category": "windows"
    }
  ]
}
```

```json
// Query correlations within a time window
GET /_plugins/_security_analytics/correlations?start_timestamp=1689289210000&end_timestamp=1689300010000
```

### Migration Notes

If you were planning to use the events-correlation-engine plugin:
1. Use the Security Analytics plugin instead
2. Create detectors for your log sources
3. Define correlation rules to identify threat scenarios
4. Use the correlation graph in OpenSearch Dashboards to visualize correlations

## Limitations

- The standalone events-correlation-engine plugin is not available in OpenSearch 3.0.0
- Correlation functionality is only available through Security Analytics for security-focused use cases
- General-purpose event correlation across non-security log sources requires custom implementation

## Related PRs

| PR | Description |
|----|-------------|
| [#16885](https://github.com/opensearch-project/OpenSearch/pull/16885) | Remove the events-correlation-engine plugin |
| [#6854](https://github.com/opensearch-project/OpenSearch/issues/6854) | [META] OpenSearch Events Correlation Engine (original proposal) |
| [#6779](https://github.com/opensearch-project/OpenSearch/issues/6779) | RFC: Events Correlation Engine |

## References

- [Issue #6854](https://github.com/opensearch-project/OpenSearch/issues/6854): Original META issue for Events Correlation Engine
- [PR #16885](https://github.com/opensearch-project/OpenSearch/pull/16885): Plugin removal PR
- [Security Analytics Documentation](https://docs.opensearch.org/3.0/security-analytics/): Official Security Analytics docs
- [Correlation Engine APIs](https://docs.opensearch.org/3.0/security-analytics/api-tools/correlation-eng/): API documentation
- [Creating Correlation Rules](https://docs.opensearch.org/3.0/security-analytics/sec-analytics-config/correlation-config/): Configuration guide
- [Blog: Correlating security events](https://opensearch.org/blog/correlating-security-events/): Overview of correlation capabilities

## Related Feature Report

- [Correlation Engine (Security Analytics)](../../../features/security-analytics/correlation-engine.md)
