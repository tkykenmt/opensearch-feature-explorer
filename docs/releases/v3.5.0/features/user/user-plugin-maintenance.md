---
tags:
  - user
---
# User Plugin Maintenance

## Summary

Routine maintenance for the User Behavior Insights (UBI) plugin in OpenSearch v3.5.0. This update increments the plugin version to 3.5.0-SNAPSHOT, upgrades Jackson dependencies, and removes the deprecated `java.security.AccessController` usage that is no longer applicable in OpenSearch 3.x.

## Details

### What's New in v3.5.0

- Version bumped from 3.4.0-SNAPSHOT to 3.5.0-SNAPSHOT
- Jackson annotations upgraded from 2.18.2 to 2.20
- Jackson databind upgraded from 2.18.2 to 2.20.1
- Decoupled `jackson-annotations` version from `jackson-core` by using `versions.jackson_annotations` instead of `versions.jackson`
- Removed deprecated `AccessController.doPrivileged` wrapper in `QueryRequest.java`, replacing it with a direct `ObjectMapper.writeValueAsString()` call

### Technical Changes

The `QueryRequest.toString()` method previously wrapped JSON serialization in `AccessController.doPrivileged()`, which was a Java Security Manager pattern. Since Java Security Manager is deprecated and removed in OpenSearch 3.x, this code was simplified to a direct try-catch block.

## Limitations

None specific to this maintenance update.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#156](https://github.com/opensearch-project/user-behavior-insights/pull/156) | Increment version to 3.5.0-SNAPSHOT | - |
