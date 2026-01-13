---
tags:
  - domain/infra
  - component/server
  - dashboards
  - indexing
---
# Version Increments

## Summary

Routine version increment to 3.4.0 across multiple OpenSearch plugin repositories. This includes version bumps in build configurations, package manifests, and CI workflows, along with necessary compatibility updates for the ActionFilter interface change in OpenSearch core.

## Details

### What's New in v3.4.0

Version increment PRs update the plugin versions to align with the OpenSearch 3.4.0 release cycle. These changes ensure plugins are built against the correct OpenSearch version and maintain compatibility with core API changes.

### Technical Changes

#### Repositories Updated

| Repository | PR | Changes |
|------------|-----|---------|
| index-management | [#1536](https://github.com/opensearch-project/index-management/pull/1536) | Version bump + ActionFilter interface update |
| notifications | [#1081](https://github.com/opensearch-project/notifications/pull/1081) | Version bump + Kotlin upgrade + dependency updates |
| dashboards-notifications | [#405](https://github.com/opensearch-project/dashboards-notifications/pull/405) | Version bump in package.json and opensearch_dashboards.json |

#### index-management Changes

- Updated `opensearch_version` from `3.3.0-SNAPSHOT` to `3.4.0-SNAPSHOT` in `build.gradle`
- Added `ActionRequestMetadata` parameter to `ActionFilter.apply()` implementations:
  - `IndexOperationActionFilter`
  - `FieldCapsFilter`
- Updated test version constants from legacy `6040399` to `136217927`
- Added `@Ignore` annotations to tests referencing removed legacy versions

#### notifications Changes

- Updated `opensearch_version` from `3.3.0-SNAPSHOT` to `3.4.0-SNAPSHOT`
- Upgraded Kotlin from `1.9.25` to `2.2.20`
- Added dependency version forcing for:
  - Jackson (using `${versions.jackson}`)
  - HTTP components (using `${versions.httpcore5}`, `${versions.httpclient5}`)
  - AWS SDK components
  - Netty components
  - DafnyRuntime 4.9.0
- Excluded `bcprov-jdk18on` from test runtime classpath
- Excluded `aws-java-sdk-core` from `opensearch-remote-metadata-sdk-ddb-client`

#### dashboards-notifications Changes

- Updated `version` from `3.3.0.0` to `3.4.0.0` in `package.json`
- Updated `version` and `opensearchDashboardsVersion` in `opensearch_dashboards.json`
- Updated `OPENSEARCH_VERSION` from `3.2.0-SNAPSHOT` to `3.4.0-SNAPSHOT` in CI workflow

### Migration Notes

For plugin developers extending `ActionFilter`:

```kotlin
// Before (3.3.x)
override fun <Request : ActionRequest, Response : ActionResponse> apply(
    task: Task,
    action: String,
    request: Request,
    listener: ActionListener<Response>,
    chain: ActionFilterChain<Request, Response>
)

// After (3.4.0)
override fun <Request : ActionRequest, Response : ActionResponse> apply(
    task: Task,
    action: String,
    request: Request,
    actionRequestMetadata: ActionRequestMetadata<Request, Response>,
    listener: ActionListener<Response>,
    chain: ActionFilterChain<Request, Response>
)
```

## Limitations

- These are maintenance changes with no functional impact
- Legacy version tests in index-management are now ignored due to removal of legacy version support in OpenSearch core

## References

### Documentation
- [OpenSearch PR #19793](https://github.com/opensearch-project/OpenSearch/pull/19793): Legacy version removal (referenced in ignored tests)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1536](https://github.com/opensearch-project/index-management/pull/1536) | index-management | Version increment + ActionFilter interface |
| [#1081](https://github.com/opensearch-project/notifications/pull/1081) | notifications | Version increment + dependency updates |
| [#405](https://github.com/opensearch-project/dashboards-notifications/pull/405) | dashboards-notifications | Version increment |
