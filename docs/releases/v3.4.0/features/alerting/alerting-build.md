# Alerting Build

## Summary

This bugfix addresses an issue in the Alerting plugin's build script that was incorrectly publishing both the alerting plugin zip and the sample remote monitor plugin zip to the artifacts folder. The fix ensures only the alerting plugin zip is published during the build process.

## Details

### What's New in v3.4.0

The build script (`scripts/build.sh`) was modified to explicitly copy only the alerting plugin zip file instead of using a wildcard pattern that matched all zip files in the build distributions directory.

### Technical Changes

#### Build Script Fix

The original build script used `find` to locate all zip files in the build distributions, which inadvertently included the `sample-remote-monitor-plugin` zip file alongside the intended `opensearch-alerting` zip.

**Before (problematic):**
```bash
zipPath=$(find . -path \*build/distributions/*.zip)
distributions="$(dirname "${zipPath}")"
cp ${distributions}/*.zip ./$OUTPUT/plugins
```

**After (fixed):**
```bash
mkdir -p $OUTPUT/plugins
cp ./alerting/build/distributions/*.zip $OUTPUT/plugins
```

#### Root Cause

The Alerting repository contains multiple subprojects:
- `alerting` - The main alerting plugin
- `alerting-sample-remote-monitor-plugin` - A sample plugin for testing remote monitors

The wildcard `find` command matched zip files from both subprojects, causing the sample plugin to be incorrectly included in the release artifacts.

### Usage Example

Building the alerting plugin now correctly produces only the alerting zip:

```bash
./scripts/build.sh -v 2.15.0 -s true
# Output: artifacts/plugins/opensearch-alerting-2.15.0.0-SNAPSHOT.zip
```

### Migration Notes

No migration required. This is a build infrastructure fix that does not affect runtime behavior.

## Limitations

None specific to this fix.

## Related PRs

| PR | Description |
|----|-------------|
| [#1608](https://github.com/opensearch-project/alerting/pull/1608) | Backport to 2.15: Fixing build script to only publish alerting zip |
| [#1605](https://github.com/opensearch-project/alerting/pull/1605) | Original fix: Fixing build script to only publish alerting zip |
| [#1604](https://github.com/opensearch-project/alerting/pull/1604) | Related: Fix pluginzippublish issue |

## References

- [Issue #1599](https://github.com/opensearch-project/alerting/issues/1599): Maven failed publishPluginZipPublicationToZipStagingRepository
- [Alerting Repository](https://github.com/opensearch-project/alerting): OpenSearch Alerting plugin

## Related Feature Report

- [Full feature documentation](../../../../features/alerting/alerting.md)
