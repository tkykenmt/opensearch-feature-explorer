---
tags:
  - observability
---
# Observability Security Maintenance

## Summary

This document tracks security-related maintenance activities for the OpenSearch Dashboards Observability plugin, including CVE remediation, dependency updates, and security patches.

## Details

### Security Practices

The Observability plugin follows OpenSearch security practices for dependency management:

- Regular dependency audits for known vulnerabilities
- Prompt remediation of critical and high-severity CVEs
- Compatibility testing before dependency upgrades
- Fallback strategies when upgrades cause breaking changes

### Dependency Management

Key frontend dependencies requiring security monitoring:

| Category | Packages |
|----------|----------|
| Data Grid | ag-grid (removed in v2.16.0) |
| WebSocket | ws |
| Utilities | braces, micromatch |

## Limitations

- Some CVE fixes may require removing functionality when upgrades are incompatible
- Build system constraints may limit upgrade options

## Change History

- **v2.16.0** (2024-08-06): Addressed CVE-2024-38996, CVE-2024-39001, CVE-2024-37890 by removing ag-grid and upgrading ws/braces packages

## References

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#1987](https://github.com/opensearch-project/dashboards-observability/pull/1987) | Fix CVEs for ag-grid, ws and braces packages |
| v2.16.0 | [#1989](https://github.com/opensearch-project/dashboards-observability/pull/1989) | CVE fix for ag (rollback) |
| v2.16.0 | [#2001](https://github.com/opensearch-project/dashboards-observability/pull/2001) | Remove ag grid package |
