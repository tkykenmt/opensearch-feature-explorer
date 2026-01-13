---
tags:
  - domain/observability
  - component/dashboards
  - dashboards
  - indexing
  - observability
---
# Observability Enhancements

## Summary

This release includes maintenance and bug fix improvements for the OpenSearch Observability plugin and Dashboards Observability plugin. The changes address CI/CD build issues, navigation group registration errors, and index pattern mismatches in the Getting Started workflows.

## Details

### What's New in v2.17.0

Three enhancements improve the stability and usability of the Observability plugins:

1. **CI Build Fix**: Added support for unsecure Node.js versions in CI workflows to resolve GLIBC compatibility issues
2. **Navigation Fix**: Removed incorrect Notebook registration from the Analytics navigation group
3. **Index Pattern Fix**: Updated Getting Started workflow ndjson files to match actual index patterns

### Technical Changes

#### CI Workflow Updates

The observability plugin's CI workflow was updated to handle GLIBC version incompatibilities:

```yaml
env:
  ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true
```

This resolves build errors like:
```
/__e/node20/bin/node: /lib64/libm.so.6: version `GLIBC_2.27' not found
/__e/node20/bin/node: /lib64/libc.so.6: version `GLIBC_2.28' not found
```

#### Navigation Group Registration Fix

Removed accidental registration of Notebooks to the Analytics navigation group. Notebooks remain visible only under the Observability navigation group as intended:

```typescript
// Removed from plugin_nav.tsx
core.chrome.navGroup.addNavLinksToGroup(DEFAULT_NAV_GROUPS.analytics, [
  {
    id: observabilityNotebookID,
    category: DEFAULT_APP_CATEGORIES.visualizeAndReport,
    order: 400,
  },
]);
```

#### Index Pattern Corrections

| Workflow | Before | After |
|----------|--------|-------|
| CSV File Upload | `logs-index` | `logs-*` |
| OTel Services | Included `otel-metrics*` | Removed `otel-metrics*` |

### Files Changed

| File | Change |
|------|--------|
| `.github/workflows/opensearch-observability-test-and-build-workflow.yml` | Added `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION` env var |
| `public/plugin_nav.tsx` | Removed Notebook from Analytics nav group |
| `public/components/getting_started/.../fluent-bit-csv-upload-1.0.0.ndjson` | Changed index pattern to `logs-*` |
| `server/routes/getting_started/assets/fluent-bit-csv-upload-1.0.0.ndjson` | Changed index pattern to `logs-*` |
| `public/components/getting_started/.../otel-index-patterns-1.0.0.ndjson` | Removed `otel-metrics*` pattern |
| `server/routes/getting_started/assets/otel-index-patterns-1.0.0.ndjson` | Removed `otel-metrics*` pattern |

## Limitations

- The CI fix uses `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION` which may have security implications for CI environments
- These are maintenance fixes with no new user-facing features

## References

### Documentation
- [Observability Documentation](https://docs.opensearch.org/2.17/observing-your-data/)
- [OpenSearch Dashboards Observability Plugin](https://github.com/opensearch-project/dashboards-observability)
- [OpenSearch Observability Plugin](https://github.com/opensearch-project/observability)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1861](https://github.com/opensearch-project/observability/pull/1861) | observability | Add allow unsecure node versions to CI .env |
| [#2044](https://github.com/opensearch-project/dashboards-observability/pull/2044) | dashboards-observability | Remove useless registration of Notebook to analytics nav group |
| [#2016](https://github.com/opensearch-project/dashboards-observability/pull/2016) | dashboards-observability | Update ndjson so workflow matches patterns created |

## Related Feature Report

- Observability Integrations
