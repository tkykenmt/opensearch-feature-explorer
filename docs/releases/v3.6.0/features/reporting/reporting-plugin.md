---
tags:
  - reporting
---
# Reporting Plugin

## Summary

In v3.6.0, the Reporting plugin received a bug fix to align with the Security plugin's resource sharing framework rename, plus a maintenance dependency bump. The `resource-action-groups.yml` file was renamed to `resource-access-levels.yml` to match the updated naming convention introduced by the Security plugin (security#6018), and the `assertj-core` test dependency was bumped from 3.16.1 to 3.27.7.

## Details

### What's New in v3.6.0

#### Resource Access Levels File Rename (Bug Fix)

The Security plugin's resource sharing framework renamed its configuration file from `resource-action-groups.yml` to `resource-access-levels.yml` in PR `https://github.com/opensearch-project/security/pull/6018`. This change introduced a new capability allowing plugin authors to specify a default access level directly in the YAML file, reducing friction when calling the migration API.

The Reporting plugin's `src/main/resources/resource-action-groups.yml` was renamed to `src/main/resources/resource-access-levels.yml` to match this convention. Without this rename, security checks for the Reporting plugin's resource types (`report-definition` and `report-instance`) would fail.

The file defines three access levels per resource type:
- `rd_read_only` / `ri_read_only` — read-only access to report definitions/instances
- `rd_read_write` / `ri_read_write` — read-write access
- `rd_full_access` / `ri_full_access` — full access including resource sharing

#### Dependency Bump (Maintenance)

The `assertj-core` test dependency was bumped from 3.16.1 to 3.27.7 in `build.gradle`. This is a major version jump that brings the test assertion library up to date.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/reporting/pull/1163` | Renamed resource-action-groups.yml to resource-access-levels.yml to fix security checks | `https://github.com/opensearch-project/security/pull/6018` |
| `https://github.com/opensearch-project/reporting/pull/1166` | Bump assertj-core to 3.27.7 | - |
