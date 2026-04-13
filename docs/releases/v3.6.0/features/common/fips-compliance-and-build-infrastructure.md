---
tags:
  - common
---
# FIPS Compliance & Build Infrastructure

## Summary

OpenSearch v3.6.0 includes a broad set of FIPS compliance and build infrastructure fixes across 9 repositories (common, custom, flow-framework, security, ml-commons, performance-analyzer, sql, alerting, opensearch). These changes ensure that all plugins build correctly with the `-Pcrypto.standard=FIPS-140-3` Gradle parameter enabled by default, resolve jar hell errors caused by duplicate BouncyCastle FIPS jars, and introduce the `OPENSEARCH_FIPS_MODE` environment variable for explicit FIPS enforced mode activation at runtime.

## Details

### What's New in v3.6.0

The v3.6.0 release advances FIPS compliance from core-only support to ecosystem-wide build compatibility. Key themes:

1. **Default FIPS build parameter**: Multiple plugins (flow-framework, ml-commons, sql) now include `gradle.properties` files that set `-Pcrypto.standard=FIPS-140-3` by default, eliminating the need to pass it manually on every build command.

2. **Jar hell prevention**: When OpenSearch core is built with FIPS, BC-FIPS jars are included in `lib/`. Plugins that also bundle BC-FIPS jars cause jar hell errors at install time. Plugins (ml-commons, performance-analyzer, flow-framework) now conditionally scope BC-FIPS dependencies as `compileOnly` when the FIPS build parameter is present, deferring to core-provided jars at runtime.

3. **FIPS mode environment variable**: The `OPENSEARCH_FIPS_MODE` environment variable replaces the previous approach of detecting `bc-fips*` jars under `lib/` to enable FIPS enforced mode. This prevents FIPS mode from being automatically activated when distributions ship with BC-FIPS jars by default, giving cluster administrators explicit control.

4. **Reduced FIPS demo installer size**: The `Randomness` class was moved from `server` to `lib/common`, removing the need to include the large `server` jar in the FIPS demo installer CLI.

5. **Gradle Shadow Plugin v9 compatibility**: The alerting and ml-commons plugins updated their shadow plugin usage to replace deprecated APIs, adapting to the Gradle Shadow Plugin v9 upgrade in OpenSearch core.

### Technical Changes

| Area | Change | Repositories |
|------|--------|-------------|
| Default FIPS build | Added `gradle.properties` with `crypto.standard=FIPS-140-3` | flow-framework, ml-commons, sql |
| BC-FIPS dependency scoping | Changed BC-FIPS from `implementation` to `compileOnly` when FIPS param present | flow-framework, ml-commons, performance-analyzer |
| FIPS mode activation | New `OPENSEARCH_FIPS_MODE` env var in `bin/opensearch-env` | opensearch |
| Code relocation | Moved `Randomness` from `server` to `lib/common` | opensearch |
| Shadow plugin v9 | Replaced deprecated shadow plugin API calls | common, alerting, ml-commons |
| CI workflow fixes | Quoted FIPS parameter in CI workflow YAML files | ml-commons, custom |
| Integration test fixes | Provided FIPS build parameter to security integration tests | security |

### FIPS Mode Activation (New)

```bash
# Explicitly enable FIPS enforced mode at runtime
OPENSEARCH_FIPS_MODE=true ./bin/opensearch

# Build without FIPS (override default)
./gradlew assemble -Pcrypto.standard=any-supported
```

## Limitations

- Plugins must be built with the same FIPS build parameter as core to avoid jar hell
- The `OPENSEARCH_FIPS_MODE` environment variable must be explicitly set; FIPS mode is no longer auto-detected from jar presence

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [opensearch#20625](https://github.com/opensearch-project/OpenSearch/pull/20625) | Use `OPENSEARCH_FIPS_MODE` env var for FIPS enforced mode | [opensearch-build#5979](https://github.com/opensearch-project/opensearch-build/issues/5979) |
| [opensearch#20570](https://github.com/opensearch-project/OpenSearch/pull/20570) | Move `Randomness` from server to lib/common | [opensearch#20520](https://github.com/opensearch-project/OpenSearch/issues/20520) |
| [ml-commons#4654](https://github.com/opensearch-project/ml-commons/pull/4654) | Fix ML build for Gradle Shadow v9 + FIPS build param | [opensearch-build#5979](https://github.com/opensearch-project/opensearch-build/issues/5979) |
| [ml-commons#4719](https://github.com/opensearch-project/ml-commons/pull/4719) | Enable FIPS flag by default via gradle.properties | - |
| [ml-commons#4659](https://github.com/opensearch-project/ml-commons/pull/4659) | Quote FIPS parameter in CI workflow files | - |
| [performance-analyzer#915](https://github.com/opensearch-project/performance-analyzer/pull/915) | FIPS build param awareness for BouncyCastle handling | [opensearch-build#5979](https://github.com/opensearch-project/opensearch-build/issues/5979) |
| [sql#5231](https://github.com/opensearch-project/sql/pull/5231) | Add gradle.properties for default FIPS build | - |
| [flow-framework#1344](https://github.com/opensearch-project/flow-framework/pull/1344) | Add gradle.properties for default FIPS build | - |
| [flow-framework#1346](https://github.com/opensearch-project/flow-framework/pull/1346) | Set bc-fips to compileOnly to avoid runtime conflicts | - |
| [common#904](https://github.com/opensearch-project/common-utils/pull/904) | Update shadow plugin usage for deprecated API | - |
| [alerting#2040](https://github.com/opensearch-project/alerting/pull/2040) | Upgrade Gradle wrapper from 9.2.0 to 9.4.0 | - |
| [alerting#2022](https://github.com/opensearch-project/alerting/pull/2022) | Update shadow plugin usage for deprecated API | - |
| [custom#270](https://github.com/opensearch-project/opensearch-plugins/pull/270) | Update delete-backport-branch workflow | - |
| [security#887](https://github.com/opensearch-project/security/pull/887) | Fix integration tests with FIPS build parameter | - |
