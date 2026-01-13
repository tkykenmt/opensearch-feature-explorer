---
tags:
  - opensearch
---
# Build Infrastructure

## Summary

OpenSearch v2.19.0 includes build infrastructure improvements focused on plugin installation for SNAPSHOT distributions. The `opensearch-plugin` CLI now supports installing SNAPSHOT versions of official plugins when running a SNAPSHOT distribution of OpenSearch.

## Details

### What's New in v2.19.0

#### SNAPSHOT Plugin Installation Support

Previously, installing official plugins on SNAPSHOT distributions required a staging hash system property (`opensearch.plugins.staging`). This created friction for developers testing SNAPSHOT builds.

The new implementation simplifies this by:
1. Detecting if the current OpenSearch build is a SNAPSHOT
2. Automatically constructing the correct artifact URL for SNAPSHOT plugins
3. Removing the staging hash requirement

### Technical Changes

| Component | Change |
|-----------|--------|
| `InstallPluginCommand` | Removed `PROPERTY_STAGING_ID` and `getStagingHash()` |
| `InstallPluginCommand` | Simplified `getOpenSearchUrl()` to use `Build.CURRENT.getQualifiedVersion()` for SNAPSHOT builds |
| URL Construction | Changed from `snapshots/plugins/{id}/{version}-{stagingHash}/` to `snapshots/plugins/{id}/{qualifiedVersion}/` |

### URL Format Changes

**Before (with staging hash):**
```
https://artifacts.opensearch.org/snapshots/plugins/analysis-icu/2.19.0-abc123/analysis-icu-2.19.0-SNAPSHOT.zip
```

**After (simplified):**
```
https://artifacts.opensearch.org/snapshots/plugins/analysis-icu/2.19.0-SNAPSHOT/analysis-icu-2.19.0-SNAPSHOT.zip
```

### Usage Example

```bash
# On a SNAPSHOT distribution, install plugins directly
./bin/opensearch-plugin install analysis-icu
./bin/opensearch-plugin install transport-reactor-netty4

# No staging hash required - works automatically
```

## Limitations

- Only applies to official OpenSearch plugins
- Third-party plugins still require explicit URLs or Maven coordinates
- SNAPSHOT artifacts must be available in the OpenSearch snapshots repository

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16581](https://github.com/opensearch-project/OpenSearch/pull/16581) | Support installing plugin SNAPSHOTs with SNAPSHOT distribution | Part of [opensearch-build#5096](https://github.com/opensearch-project/opensearch-build/issues/5096) |
