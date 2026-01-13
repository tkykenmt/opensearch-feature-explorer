---
tags:
  - domain/observability
  - component/server
  - dashboards
  - observability
  - security
---
# Observability Cypress Updates

## Summary

This maintenance update addresses security advisories in the Cypress test framework dependencies used by the OpenSearch Dashboards Observability plugin. The `@cypress/request` package was updated to resolve vulnerabilities in transient development dependencies.

## Details

### What's New in v3.3.0

The `@cypress/request` dependency was updated from version 3.0.1 to 3.0.9 to address security advisories flagged by dependency scanning tools. This is a development-only change that does not affect production functionality.

### Technical Changes

#### Dependency Updates

| Package | Previous Version | New Version |
|---------|------------------|-------------|
| @cypress/request | 3.0.1 | 3.0.9 |
| form-data | 2.3.3 | 4.0.4 |
| http-signature | 1.3.6 | 1.4.0 |
| qs | 6.10.4 | 6.14.0 |
| tough-cookie | 4.1.3 | 5.0.0 |
| sshpk | 1.17.0 | 1.18.0 |

#### Changes Made

1. Removed explicit `@cypress/request` override from `package.json` resolutions
2. Updated `yarn.lock` with new dependency versions
3. Added newline at end of `package.json` file

### Impact

- **Production**: No impact - these are development dependencies only
- **Development**: Resolves security advisory warnings during dependency installation
- **Testing**: No functional changes to Cypress test execution

## Limitations

- This update only addresses transient development dependencies
- The vulnerabilities were in dependencies never directly called by the codebase

## References

### Documentation
- [Observability Documentation](https://docs.opensearch.org/3.3/observing-your-data/): Official docs
- [PR #2507](https://github.com/opensearch-project/dashboards-observability/pull/2507): Main implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#2507](https://github.com/opensearch-project/dashboards-observability/pull/2507) | Update cypress/requests |

## Related Feature Report

- [Full feature documentation](../../../features/observability/observability-cypress-updates.md)
