# Sample Data Bugfixes

## Summary

This release updates the OTEL (OpenTelemetry) sample data description to inform users about OpenSearch version compatibility requirements. The OTEL sample data only works with OpenSearch 2.13+ domains, and this fix adds a clear warning message to help users understand this limitation.

## Details

### What's New in v2.18.0

The OTEL sample data description now includes compatibility information, warning users that the sample data requires OpenSearch 2.13 or later.

### Technical Changes

#### Description Update

The sample data description was updated from:

```
Correlated observability signals for an e-commerce application in OpenTelemetry standard.
```

To:

```
Correlated observability signals for an e-commerce application in OpenTelemetry standard (Compatible with 2.13+ OpenSearch domains)
```

#### Changed Files

| File | Change |
|------|--------|
| `src/plugins/home/server/services/sample_data/data_sets/otel/index.ts` | Updated description text |

### User Impact

Users attempting to load OTEL sample data on OpenSearch versions prior to 2.13 will now see a clear compatibility warning before installation, preventing confusion when the sample data fails to work properly.

## Limitations

- OTEL sample data remains incompatible with OpenSearch versions prior to 2.13
- Future releases plan to make the sample data compatible with all OpenSearch versions

## Related PRs

| PR | Description |
|----|-------------|
| [#8693](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8693) | Update OTEL sample data description with compatible OS version |

## References

- [OpenSearch Dashboards Quickstart Guide](https://docs.opensearch.org/2.18/dashboards/quickstart/): Documentation on adding sample data

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/sample-data.md)
