---
tags:
  - alerting
---
# Alerting Build Fixes

## Summary

Fixed build script issues in the Alerting plugin that prevented proper publishing of the alerting zip artifact to the staging repository. The fixes ensure only the main alerting plugin zip is published, excluding the sample remote monitor plugin from release artifacts.

## Details

### What's New in v2.16.0

Two related PRs addressed build script issues that were causing build failures:

1. **PR #1604**: Re-enabled publishing of the alerting zip to the staging repository by removing the exclusion of `publishPluginZipPublicationToMavenLocal` and `publishPluginZipPublicationToZipStagingRepository` tasks from `settings.gradle`. This fixed the error where the build script couldn't find the local staging repo directory.

2. **PR #1605**: Fixed a side-effect from PR #1604 where the sample remote monitor plugin zip was also being published to the artifacts folder. The build script was modified to explicitly copy only the alerting plugin zip (`./alerting/build/distributions/*.zip`) instead of using a wildcard find that matched all zip files.

### Technical Changes

**settings.gradle change (PR #1604)**:
- Removed: `startParameter.excludedTaskNames=["publishPluginZipPublicationToMavenLocal", "publishPluginZipPublicationToZipStagingRepository"]`
- This re-enabled the Gradle tasks needed for publishing the plugin zip

**build.sh change (PR #1605)**:
- Changed from wildcard zip discovery to explicit path
- Before: `zipPath=$(find . -path \*build/distributions/*.zip)` followed by `cp ${distributions}/*.zip`
- After: `cp ./alerting/build/distributions/*.zip $OUTPUT/plugins`
- This ensures only the main alerting plugin is included in release artifacts

### Build Error Fixed

The original error that was occurring:
```
cp: cannot stat './build/local-staging-repo/org/opensearch/.': No such file or directory
ERROR: Command 'bash /tmp/tmp3bqjkb5d/alerting/scripts/build.sh -v 3.0.0 -p linux -a x64 -s false -o builds' returned non-zero exit status 1.
```

## Limitations

None - these are build infrastructure fixes only.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1604](https://github.com/opensearch-project/alerting/pull/1604) | Fix pluginzippublish issue - re-enable publishing zip to staging repo | [#1599](https://github.com/opensearch-project/alerting/issues/1599) |
| [#1605](https://github.com/opensearch-project/alerting/pull/1605) | Fixing build script to only publish alerting zip | [#1599](https://github.com/opensearch-project/alerting/issues/1599) |

### Issues
- [#1599](https://github.com/opensearch-project/alerting/issues/1599): Build failure due to missing staging repo directory
