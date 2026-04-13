---
tags:
  - notifications
---
# Notifications

## Summary

OpenSearch v3.6.0 includes build infrastructure fixes, dependency resolution improvements, and a new multi-tenancy configuration setting for the Notifications plugin. These changes resolve jar hell issues, Jackson version conflicts, and build failures, while also adding configurable tenant-aware mode for the remote metadata SDK client and migrating settings to the proper `plugins.notifications` namespace.

## Details

### What's New in v3.6.0

#### Multi-Tenancy Setting and Settings Namespace Migration (PR #1148)

A new `plugins.notifications.multi_tenancy_enabled` boolean setting (default `false`) was added to control tenant-aware mode for the remote metadata SDK client. Previously, the `TENANT_AWARE_KEY` was hardcoded to `false`. This setting allows enabling tenant-aware mode via `opensearch.yml`.

Additionally, all remote metadata settings were migrated from the `plugins.alerting.*` prefix to `plugins.notifications.*`:

| Old Setting | New Setting |
|-------------|-------------|
| `plugins.alerting.remote_metadata_type` | `plugins.notifications.remote_metadata_type` |
| `plugins.alerting.remote_metadata_endpoint` | `plugins.notifications.remote_metadata_endpoint` |
| `plugins.alerting.remote_metadata_region` | `plugins.notifications.remote_metadata_region` |
| `plugins.alerting.remote_metadata_service_name` | `plugins.notifications.remote_metadata_service_name` |
| *(new)* | `plugins.notifications.multi_tenancy_enabled` |

### Technical Changes

#### Bouncy Castle Jar Hell Fix (PR #1141)

Excluded transitive Bouncy Castle (`org.bouncycastle`) dependencies from the `opensearch-remote-metadata-sdk-ddb-client` dependency to resolve a jar hell issue. The exclusion was moved from `testRuntimeClasspath` to the dependency declaration itself, ensuring it applies to all configurations.

#### Jackson Version Conflict Resolution (PR #1151)

Replaced individual `force` directives for Jackson dependencies with a dynamic `eachDependency` resolution strategy. This ensures all `com.fasterxml.jackson` group dependencies use consistent versions, with `jackson-annotations` using `versions.jackson_annotations` and all others using `versions.jackson`.

#### Shadow Plugin API Update (PR #1138)

Updated the `core-spi` module's Maven publication from the deprecated `project.shadow.component(it)` API to `from components.shadow`, preparing for future Gradle shadow plugin updates.

#### Maven Local Publishing Fix (PR #1063)

Removed the `startParameter.excludedTaskNames` entry that excluded `publishPluginZipPublicationToMavenLocal`, allowing developers to publish the plugin zip to Maven local via `./gradlew publishPluginZipPublicationToMavenLocal`.

#### Maven Local Ordering Fix (PR #1152)

Added proper task ordering in `build.gradle` to ensure `generatePomFileForPluginZipPublication` runs after `publishNebulaPublicationToMavenLocal` for the `opensearch-notifications-core` project, preventing build race conditions.

#### React 18 Upgrade (PR #419)

Upgraded the Notifications Dashboards plugin to React 18 and fixed unit tests to accommodate the upgrade.

## Limitations

- The `plugins.notifications.multi_tenancy_enabled` setting is `Final` (node-scope, not dynamically updatable) — requires a node restart to change.
- The settings namespace migration from `plugins.alerting.*` to `plugins.notifications.*` is a breaking change for existing configurations using the old prefix.

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1148](https://github.com/opensearch-project/notifications/pull/1148) | Add multi_tenancy_enabled setting and update settings prefix | [#1147](https://github.com/opensearch-project/notifications/issues/1147) |
| [#1141](https://github.com/opensearch-project/notifications/pull/1141) | Exclude transitive Bouncy Castle dependencies | [#1139](https://github.com/opensearch-project/notifications/issues/1139) |
| [#1151](https://github.com/opensearch-project/notifications/pull/1151) | Fix build failure due to Jackson version conflict | [#1150](https://github.com/opensearch-project/notifications/issues/1150) |
| [#1138](https://github.com/opensearch-project/notifications/pull/1138) | Update shadow plugin usage to replace deprecated API | — |
| [#1063](https://github.com/opensearch-project/notifications/pull/1063) | Allow publishing plugin zip to Maven local | [#1067](https://github.com/opensearch-project/notifications/issues/1067) |
| [#1152](https://github.com/opensearch-project/notifications/pull/1152) | Define mavenLocal ordering properly for both jars and zips | [#1149](https://github.com/opensearch-project/notifications/issues/1149), [#1150](https://github.com/opensearch-project/notifications/issues/1150) |
| [#419](https://github.com/opensearch-project/notifications/pull/419) | Upgrade to React 18 and fix unit tests | — |
