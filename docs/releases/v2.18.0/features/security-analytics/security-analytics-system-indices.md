# Security Analytics System Indices

## Summary

This release includes several bugfixes for Security Analytics system indices in v2.18.0. The changes improve index configuration by standardizing replica settings, adding dedicated query indices for detectors, and fixing correlation alert refresh policies. These improvements enhance reliability and scalability of Security Analytics system indices.

## Details

### What's New in v2.18.0

#### System Index Configuration Standardization

All Security Analytics system indices now use consistent settings:
- Primary shards: 1 (optimized for small system indices)
- Auto-expand replicas: 1-20 (changed from 0-all)
- Minimum replicas: 0 (updated from 1)

#### Dedicated Query Indices for Detectors

A new setting `plugins.security_analytics.enable_detectors_with_dedicated_query_indices` allows detectors to use dedicated query indices instead of shared ones. When enabled:
- Each detector gets its own query index with UUID suffix
- Improves isolation between detectors
- Reduces contention on shared query indices

#### Correlation Alert Refresh Policy Fix

The refresh policy for correlation alert updates is now set to `IMMEDIATE`, ensuring alerts are visible immediately after acknowledgment.

### Technical Changes

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.security_analytics.enable_detectors_with_dedicated_query_indices` | Enable dedicated query indices per detector | `false` |
| `minSystemIndexReplicas` | Minimum replicas for system indices | `1` |
| `maxSystemIndexReplicas` | Maximum replicas for system indices | `20` |

#### Affected System Indices

| Index Pattern | Description |
|---------------|-------------|
| `.opensearch-sap-*-detectors-queries-*` | Detector query indices |
| `.opensearch-sap-iocs-*` | IOC feed indices |
| `.opensearch-sap-*-alerts` | Alert indices |
| `.opensearch-sap-*-findings` | Findings indices |
| Correlation indices | Correlation history and metadata |
| Log type config index | Log type configuration |
| Custom log type index | Custom log types |
| Detector index | Detector configurations |
| Rule indices | Detection rules |

### Usage Example

Enable dedicated query indices:
```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.security_analytics.enable_detectors_with_dedicated_query_indices": true
  }
}
```

After enabling, new detectors will create dedicated query indices with pattern:
`.opensearch-sap-{log_type}-detectors-queries-optimized-{uuid}`

### Migration Notes

- Existing detectors continue using shared query indices
- To use dedicated indices for existing detectors, delete and recreate them after enabling the setting
- Disabling the setting after enabling requires detector recreation

## Limitations

- Dedicated query indices increase the total number of indices in the cluster
- Changing the setting does not automatically migrate existing detectors

## References

### Documentation
- [Security Analytics Documentation](https://docs.opensearch.org/2.18/security-analytics/)
- [Security Analytics System Indexes](https://docs.opensearch.org/2.18/security-analytics/security/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1358](https://github.com/opensearch-project/security-analytics/pull/1358) | Update replicas to 1-20 and primary shards to 1 |
| [#1364](https://github.com/opensearch-project/security-analytics/pull/1364) | Update min replicas to 0 |
| [#1365](https://github.com/opensearch-project/security-analytics/pull/1365) | Enable dedicated query index settings |
| [#1324](https://github.com/opensearch-project/security-analytics/pull/1324) | Separate doc-level monitor query indices |
| [#1382](https://github.com/opensearch-project/security-analytics/pull/1382) | Set refresh policy to IMMEDIATE for correlation alerts |

## Related Feature Report

- [Full feature documentation](../../../features/security-analytics/security-analytics-system-indices.md)
