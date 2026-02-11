---
tags:
  - observability
---
# Observability Dependencies

## Summary

Tracks dependency management, security patches, and build tooling updates for the OpenSearch Observability plugin ecosystem, covering both the backend plugin (`observability`) and the frontend Dashboards plugin (`dashboards-observability`).

## Details

### Components

| Component | Repository | Language |
|-----------|-----------|----------|
| Backend plugin | opensearch-project/observability | Kotlin/Java |
| Frontend plugin | opensearch-project/dashboards-observability | TypeScript/JavaScript |

### Key Dependencies

| Dependency | Purpose | Component |
|-----------|---------|-----------|
| lodash | Utility library | dashboards-observability |
| cypress-parallel | Parallel test execution | dashboards-observability |
| ktlint-cli | Kotlin code linting | observability |
| Jackson | JSON serialization | observability |

## Limitations

- Dependency updates are typically maintenance-only and do not change plugin functionality.
- CVE fixes in transitive dependencies may require upgrading parent packages.

## Change History

- **v3.5.0**: Bumped lodash to 4.17.23 (prototype pollution fix), upgraded cypress-parallel for js-yaml CVE-2025-64718, upgraded ktlint-cli to 1.8.0, decoupled jackson-annotations version

## References

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v3.5.0 | [#2569](https://github.com/opensearch-project/dashboards-observability/pull/2569) | Bump lodash from 4.17.21 to 4.17.23 |
| v3.5.0 | [#2577](https://github.com/opensearch-project/dashboards-observability/pull/2577) | Upgrade cypress-parallel for js-yaml CVE-2025-64718 fix |
| v3.5.0 | [#1962](https://github.com/opensearch-project/observability/pull/1962) | Upgrade to ktlint-cli 1.8.0 |
| v3.5.0 | [#1968](https://github.com/opensearch-project/observability/pull/1968) | Decouple jackson annotation version |
