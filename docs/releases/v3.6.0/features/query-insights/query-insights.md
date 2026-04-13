---
tags:
  - query-insights
---
# Query Insights

## Summary

OpenSearch v3.6.0 brings major new capabilities to Query Insights including remote repository export for top N queries, a rule-based recommendation engine, RBAC-based access control, shard-level live query visibility, finished queries cache, failed query tracking, streaming query categorization, and enhanced Dashboards visualizations. Alongside these features, multiple bug fixes improve exporter reliability, grouping settings initialization, streaming tag propagation, and CI/test infrastructure stability.

## Details

### What's New in v3.6.0

#### Remote Repository Exporter
A new `RemoteRepositoryExporter` enables exporting top N query data to remote blob store repositories (e.g., S3) alongside the existing local index exporter. Files are organized by timestamp: `{path}/top-queries/yyyy/MM/dd/HH/mm'UTC'/{node-id}-{metric-type}.json`. Currently requires async multi-stream blob upload support (available in repository-s3 plugin).

New cluster settings:
| Setting | Description | Default |
|---------|-------------|---------|
| `search.insights.top_queries.exporter.remote.enabled` | Enable/disable remote export | `false` |
| `search.insights.top_queries.exporter.remote.repository` | Repository name | - |
| `search.insights.top_queries.exporter.remote.path` | Base path for organizing files | - |

#### Rule-Based Recommendation Engine
A new recommendation engine framework analyzes search queries and provides actionable suggestions. Includes data models (`Recommendation`, `Action`, `ImpactVector`, `RecommendationType`), a `RecommendationService` for rule registration and evaluation, `RecommendationRule` interface with `QueryContext` for inspecting query structure via visitor pattern, and configurable filtering by confidence threshold and max count.

New cluster settings:
| Setting | Description | Default |
|---------|-------------|---------|
| `search.insights.recommendations.enabled` | Enable recommendation engine | `false` |
| `search.insights.recommendations.min_confidence` | Minimum confidence threshold | - |
| `search.insights.recommendations.max_count` | Maximum recommendations per query | - |
| `search.insights.recommendations.enabled_rules` | List of enabled recommendation rules | - |

#### Access Control (RBAC) for Query Insights Data
New `search.insights.top_queries.filter_by_mode` cluster setting controls access to top query records based on user identity. Supported modes: `none` (default, no filtering), `username` (users see only their own queries), and `backend_roles` (users see queries from users sharing at least one backend role). Users with `all_access` role bypass filtering. Adds `backend_roles` attribute to `SearchQueryRecord`. Filtering is applied in `TransportTopQueriesAction` via a listener wrapper covering both in-memory and historical query paths.

#### Shard-Level Task Details in Live Queries API
The live queries API now includes shard-level task details with a coordinator/shard task hierarchy. New `LiveQueryRecord` model groups shard tasks under their parent coordinator tasks using `TaskGroup` from `ListTasksResponse`. The response now shows `coordinator_task` and `shard_tasks` arrays with per-task metrics (task_id, node_id, action, status, running_time_nanos, cpu_nanos, memory_bytes).

#### Finished Queries Cache
A new `FinishedQueriesCache` captures recently completed/failed/cancelled queries via `QueryInsightsListener`. Accessible through `GET /_insights/live_queries?use_finished_cache=true`. Each `FinishedQueryRecord` includes a `top_n_id` field that correlates with the Top N queries API for cross-API query tracking. Cache is lazily initialized with configurable idle timeout (`search.insights.live_queries.cache.idle_timeout`, default 5 minutes, range 2–10 minutes, 0 to disable).

#### Failed Query Tracking
Queries that fail during execution are now tagged with a `failed` attribute in `SearchQueryRecord`, enabling identification of problematic queries in Top N results.

#### Streaming Dimension for Query Categorization
Query categorization metrics now include a streaming dimension. A streaming flag from the search request context is read during categorization and tagged on aggregation requests via `IS_STREAMING_TAG`. Works with OpenSearch core's streaming search support.

#### Dashboards Enhancements
- Added visualizations to Top N Queries page: P90/P99 stats, queries by node/index/user/WLM group pie charts, and performance analysis line charts
- Added heatmap visualization, interactive pie charts, collapsible sections, and sorting/pagination
- Switched latency graphs from Plotly to React ECharts for consistency

### Bug Fixes

#### Exporter Retry Logic Fix
Moved `MapperParsingException` detection and retry logic from `onFailure()` to `onResponse()` callback in `LocalIndexExporter.bulk()`. Per-document mapping errors are returned inside `BulkResponse` via `onResponse()`, not through `onFailure()` which only fires for complete request failures. Changed exception check from `MapperException` to `MapperParsingException` for precision.

#### Grouping Settings Initialization Fix
Fixed `QueryInsightsListener` `@Inject` constructor overwriting `groupingFieldNameEnabled` and `groupingFieldTypeEnabled` to `false` after the delegated constructor had correctly initialized them from cluster settings. Since both settings default to `true`, the settings update consumer would not fire when tests set them to `true`, causing flaky `MinMaxQueryGrouperBySimilarityIT` tests.

#### Streaming Tag Propagation Fix
Fixed `IS_STREAMING_TAG` not being propagated in `incrementAggCounter` due to `Tags` being immutable — `addTag` returns a new instance but the return value was being discarded.

#### Test and CI Infrastructure Fixes
- Fixed `MultiIndexDateRangeIT` test failure
- Enabled `internalClusterTest` and `yamlRestTest` tasks and fixed uncovered test issues (closes #514)
- Excluded `RemoteRepositoryExporterIT` and `TopQueriesRbacIT` from `integTestRemote`
- Fixed `integTestRemote` task spinning up unnecessary test cluster nodes by changing task type from `RestIntegTestTask` to `Test`
- Added cluster health check before running integration tests (120s timeout) — then reverted on 3.6 branch
- Pinned LocalStack to v4.4 and increased health check timeout from 30s to 120s for CI stability
- Removed flaky `verbose=false` API schema Cypress test
- Used poll-based check in Cypress `beforeEach` for improved test reliability
- Pinned Gradle wrapper version in Cypress workflows to prevent Gradle 9.x download

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#541](https://github.com/opensearch-project/query-insights/pull/541) | Add RemoteRepositoryExporter for remote blob store export | [#545](https://github.com/opensearch-project/query-insights/issues/545) |
| [#549](https://github.com/opensearch-project/query-insights/pull/549) | Add recommendation data models for rule-based engine | - |
| [#548](https://github.com/opensearch-project/query-insights/pull/548) | Add shard-level task details to live queries API | - |
| [#551](https://github.com/opensearch-project/query-insights/pull/551) | Add streaming dimension to query categorization metrics | - |
| [#552](https://github.com/opensearch-project/query-insights/pull/552) | Implement access control for query insights data | [#520](https://github.com/opensearch-project/query-insights/issues/520) |
| [#555](https://github.com/opensearch-project/query-insights/pull/555) | Rule-based recommendation service implementation | [#532](https://github.com/opensearch-project/query-insights/issues/532) |
| [#540](https://github.com/opensearch-project/query-insights/pull/540) | Tag failed queries with failed attribute | [#253](https://github.com/opensearch-project/query-insights/issues/253) |
| [#554](https://github.com/opensearch-project/query-insights/pull/554) | Add finished queries cache to live queries API | - |
| [#473](https://github.com/opensearch-project/query-insights-dashboards/pull/473) | Add visualizations to Top N Queries page | - |
| [#486](https://github.com/opensearch-project/query-insights-dashboards/pull/486) | Add heatmap, interactive pie charts, collapsible sections | - |
| [#487](https://github.com/opensearch-project/query-insights-dashboards/pull/487) | Switch latency graphs from Plotly to React ECharts | - |
| [#570](https://github.com/opensearch-project/query-insights/pull/570) | Fix IS_STREAMING_TAG not propagated in incrementAggCounter | - |
| [#558](https://github.com/opensearch-project/query-insights/pull/558) | Fix MultiIndexDateRangeIT test failure | - |
| [#556](https://github.com/opensearch-project/query-insights/pull/556) | Fix exporter retry logic for MapperParsingException | - |
| [#578](https://github.com/opensearch-project/query-insights/pull/578) | Fix grouping field_name/field_type settings overwritten on init | - |
| [#522](https://github.com/opensearch-project/query-insights/pull/522) | Enable internalClusterTest and yamlRestTest tasks | [#514](https://github.com/opensearch-project/query-insights/issues/514) |
| [#577](https://github.com/opensearch-project/query-insights/pull/577) | Exclude tests from integTestRemote | - |
| [#587](https://github.com/opensearch-project/query-insights/pull/587) | Fix integTestRemote task type to prevent extra cluster nodes | - |
| [#594](https://github.com/opensearch-project/query-insights/pull/594) | Revert cluster health check before integration tests | - |
| [#588](https://github.com/opensearch-project/query-insights/pull/588) | Add cluster health check before integration tests | - |
| [#572](https://github.com/opensearch-project/query-insights/pull/572) | Pin LocalStack v4.4 and increase health check timeout | - |
| [#480](https://github.com/opensearch-project/query-insights-dashboards/pull/480) | Remove flaky verbose=false Cypress test | - |
| [#482](https://github.com/opensearch-project/query-insights-dashboards/pull/482) | Use poll-based check in Cypress beforeEach | - |
| [#484](https://github.com/opensearch-project/query-insights-dashboards/pull/484) | Pin Gradle wrapper version in Cypress workflows | - |
