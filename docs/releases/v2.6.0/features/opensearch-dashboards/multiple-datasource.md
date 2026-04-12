---
tags:
  - opensearch-dashboards
---
# Multiple DataSource

## Summary

OpenSearch 2.6.0 introduces 2 new feature(s) and 0 enhancement(s) to Multiple DataSource.

## Details

### New Features

- **[Multiple DataSource] Add support for SigV4 authentication**: https://user-images.githubusercontent.com/32652829/217648195-55e86e9b-3740-4bd1-ab69-69e337dad26d.mp4 UI & Backend implementation to support SigV4 as a new auth type of datasource. It supports both legacy client and opensearch client. - Add new auth type `SigV4` - refactor data source save object wr
- **[Multiple DataSource] Refactor test connection to support SigV4 auth type**: [Multiple DataSource] Refactor test connection to support SigV4 auth type - update UI to enable test connection button with `Sigv4` auth type - Update test connection router, input validation - refactor to remove `configureTestClient`

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#3058](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/3058) | [Multiple DataSource] Add support for SigV4 authentication | OpenSearch-Dashboards |
| [#3456](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/3456) | [Multiple DataSource] Refactor test connection to support SigV4 auth type | OpenSearch-Dashboards |
