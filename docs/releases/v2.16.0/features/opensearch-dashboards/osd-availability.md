---
tags:
  - opensearch-dashboards
---
# OSD Availability

## Summary

This bugfix prevents OpenSearch Dashboards from crashing when the disk is full by introducing a new configuration option `logging.ignoreEnospcError` that handles ENOSPC (no space left on device) errors gracefully in the logging pipeline.

## Details

### What's New in v2.16.0

Prior to this fix, when the disk became full, the OSD process would crash due to unhandled ENOSPC errors in the logging stream. This was particularly problematic in production environments where disk space issues could cause unexpected service outages.

### Technical Changes

The fix introduces a new feature flag `logging.ignoreEnospcError` that controls how ENOSPC errors are handled:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `logging.ignoreEnospcError` | boolean | `false` | When `true`, ENOSPC errors in the logging pipeline are caught and logged to console instead of crashing the process |

### Implementation

The changes modify the logging pipeline in `log_reporter.js`:

1. When `ignoreEnospcError` is enabled and logging to a file, the pipeline uses Node.js `pipeline()` with an error callback
2. ENOSPC errors are caught and logged to console instead of propagating and crashing the process
3. Other errors continue to throw as before to maintain existing behavior

### Configuration Example

```yaml
# opensearch_dashboards.yml
logging.ignoreEnospcError: true
```

For Docker deployments, the setting can be passed as an environment variable.

## Limitations

- This setting only affects file-based logging (not stdout)
- When enabled, log entries may be lost during disk-full conditions
- The setting is disabled by default to maintain backward compatibility

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6733](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6733) | Prevent OSD process crashes when disk is full | [#6607](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6607) |

### Issues

| Issue | Description |
|-------|-------------|
| [#6607](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6607) | Feature request: Allow admin to customize OSD logging exception handling behavior |
