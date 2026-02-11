---
tags:
  - observability
---
# Observability Dependencies

## Summary

Dependency updates and security fixes for the Observability plugin in OpenSearch v3.5.0. These changes address CVE vulnerabilities, upgrade build tooling, and fix dependency version mismatches across both the backend (observability) and frontend (dashboards-observability) components.

## Details

### What's New in v3.5.0

#### Security Fixes
- **lodash 4.17.21 → 4.17.23**: Fixes prototype pollution vulnerability in `baseUnset` function. Applied to the dashboards-observability frontend.
- **js-yaml CVE-2025-64718**: Resolved by upgrading `cypress-parallel`, which pulls in a patched version of `mocha` → `js-yaml` transitive dependency chain.

#### Build Tooling
- **ktlint-cli 0.47.1 → 1.8.0**: Upgraded the Kotlin linter from the legacy `com.pinterest:ktlint` artifact to the new `com.pinterest.ktlint:ktlint-cli` artifact. This also triggered a comprehensive Kotlin code style reformatting across the backend plugin source (trailing commas, expression body functions, multi-line parameter formatting).

#### Dependency Version Alignment
- **Jackson annotations decoupling**: Changed `jackson-annotations` dependency from `${versions.jackson}` to `${versions.jackson_annotations}` in `build.gradle`. This aligns with the upstream OpenSearch build tools change ([OpenSearch#20343](https://github.com/opensearch-project/OpenSearch/pull/20343)) that introduced separate versioning for `jackson-annotations` (2.20) vs other Jackson artifacts (2.20.1). Resolves [observability#1967](https://github.com/opensearch-project/observability/issues/1967).

### Technical Changes

| Change | From | To | Component |
|--------|------|----|-----------|
| lodash | 4.17.21 | 4.17.23 | dashboards-observability |
| cypress-parallel (js-yaml) | vulnerable | patched | dashboards-observability |
| ktlint-cli | 0.47.1 | 1.8.0 | observability (backend) |
| jackson-annotations | `${versions.jackson}` | `${versions.jackson_annotations}` | observability (backend) |

## Limitations

- The ktlint upgrade caused widespread code formatting changes that are purely cosmetic (trailing commas, expression bodies). No functional behavior changed.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2569](https://github.com/opensearch-project/dashboards-observability/pull/2569) | Bump lodash from 4.17.21 to 4.17.23 | - |
| [#2577](https://github.com/opensearch-project/dashboards-observability/pull/2577) | Upgrade cypress-parallel for js-yaml CVE-2025-64718 fix | - |
| [#1962](https://github.com/opensearch-project/observability/pull/1962) | Upgrade to ktlint-cli 1.8.0 | - |
| [#1968](https://github.com/opensearch-project/observability/pull/1968) | Decouple jackson annotation version | [#1967](https://github.com/opensearch-project/observability/issues/1967) |
