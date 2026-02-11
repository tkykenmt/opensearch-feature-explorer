---
tags:
  - user
---
# User Plugin Maintenance

## Summary

Tracks maintenance activities for the User Behavior Insights (UBI) plugin, including version bumps, dependency upgrades, and code modernization. The UBI plugin enables capturing and analyzing user search behavior within OpenSearch.

## Details

### Overview

The User Behavior Insights plugin provides the ability to capture user queries and click-through events, enabling search relevance analysis. Maintenance activities ensure the plugin stays compatible with each OpenSearch release and follows current best practices.

### Key Maintenance Areas

| Area | Description |
|------|-------------|
| Version management | Automated version bumps to align with OpenSearch releases |
| Dependency upgrades | Jackson and other library updates for compatibility and security |
| Code modernization | Removal of deprecated APIs (e.g., `AccessController`) |

## Limitations

None.

## Change History

- **v3.5.0**: Version bump to 3.5.0-SNAPSHOT, Jackson upgrade (annotations 2.18.2→2.20, databind 2.18.2→2.20.1), removed deprecated `AccessController.doPrivileged` usage

## References

### Pull Requests
| Version | PR | Description |
|---------|----|-------------|
| v3.5.0 | [#156](https://github.com/opensearch-project/user-behavior-insights/pull/156) | Increment version to 3.5.0-SNAPSHOT |
