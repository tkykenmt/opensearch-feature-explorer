---
tags:
  - sql
---
# SQL/PPL Engine

## Summary

OpenSearch v3.6.0 delivers a major expansion of the SQL/PPL engine across 53 pull requests spanning the `sql` and `opensearch-dashboards` repositories. Key highlights include the Unified Query API with Calcite-native SQL planning, bi-directional graph traversal via `graphlookup`, PPL search result highlighting, `fetch_size` for PPL, query cancellation support, grammar bundle generation for client-side autocomplete, and six new PPL commands (`mvexpand`, `convert`, `nomv`, `fieldformat`, `graphlookup`, `contains`). The release also includes 20 bug fixes addressing memory leaks, PIT resource leaks, filter pushdown issues, and error handling improvements.

## Key Changes

### Unified Query API Enhancements

The Unified Query API introduced in v3.5.0 receives significant maturation:

- **Calcite-native SQL planning** (sql#5257): SQL queries now use Calcite's native parser pipeline (`SqlParser` → `SqlValidator` → `SqlToRelConverter` → `RelNode`), producing logical plans alongside the existing PPL path. Benchmarks show SQL planning at 0.055–0.114 ms/op vs PPL at 0.142–0.244 ms/op.
- **Unified query parser API** (sql#5274): Extracts parsing logic into a `UnifiedQueryParser<R>` interface with language-specific implementations: `PPLQueryParser` (returns `UnresolvedPlan`) and `CalciteSqlQueryParser` (returns `SqlNode`). Context-owned parser follows the Spark/Flink pattern.
- **Profiling support** (sql#5268): Enables per-phase timing metrics in the unified query API via `UnifiedQueryContext`, with auto-profiling inside components and a `measure()` API for external code.

### New PPL Commands

| Command | PR | Description |
|---------|-----|-------------|
| `graphlookup` | sql#5138, sql#5209, sql#5253 | Bi-directional graph traversal using BFS. Supports `direction=(uni\|bi)`, `batchMode`, `usePIT`, `filter`, and `supportArray`. 5–29x faster than MongoDB on SNB benchmarks. |
| `mvexpand` | sql#5144 | Expands multivalue fields (arrays) into separate rows. Supports optional `limit` parameter. Analogous to Splunk's `mvexpand`. |
| `convert` | sql#5157 | Unit conversion with 5 conversion functions (numeric and memory conversions). |
| `nomv` | sql#5130 | Converts multivalue fields to single values. |
| `fieldformat` | sql#5080 | Formats field values for display output. |
| `contains` | sql#5219 | CloudWatch-style contains operator for string matching. |

### PPL Highlight Support

- **Backend** (sql#5234): Adds search result highlighting via the `highlight` API parameter on `POST /_plugins/_ppl`. Supports simple array format (`["*"]`) and rich object format with `pre_tags`, `post_tags`, `fields`, and `fragment_size`. The `HighlightConfig` record threads through the full pipeline and is pushed down to OpenSearch's `HighlightBuilder`.
- **Dashboards** (opensearch-dashboards#11547): Renders highlighted search results in the Explore view.

### PPL `fetch_size` API

- **Backend** (sql#5109): Adds `fetch_size` parameter (1–10,000) to `POST /_plugins/_ppl`. Injects a `Head` AST node that pushes the limit down to OpenSearch. Unlike SQL's cursor-based `fetch_size`, PPL returns a single complete response.
- **Dashboards** (opensearch-dashboards#11359): Onboards `fetch_size` for PPL queries to limit rows at the OpenSearch level.
- **Dashboards fix** (opensearch-dashboards#11430): Skips `fetch_size` injection when PPL query ends with explicit `head` command.

### Query Cancellation

- sql#5254: PPL queries now register as `CancellableTask`, making them visible in `GET /_tasks` and cancellable via `POST /_tasks/{task_id}/_cancel`. Supports optional `queryId` in request body.

### Grammar Bundle Generation API

- sql#5162: New `@ExperimentalApi` endpoint serves a versioned grammar bundle containing serialized ANTLR ATNs, token vocabulary, rule names, and autocomplete metadata. Enables full client-side PPL parsing/autocomplete with zero per-keystroke server calls.
- opensearch-dashboards#11428: Adopts the backend grammar bundle as runtime source of truth for PPL autocomplete with safe fallback.

### Other Enhancements

- **Prometheus rules** (sql#5228): Support for creating/updating Prometheus rules.
- **Struct output change** (sql#5227): Final output of struct changed from list to map format.
- **LAST/FIRST/TAKE aggregation** (sql#5091): Now supports TEXT type and Scripts.
- **`spath` auto-extract** (sql#5140): Adds auto-extract mode for the `spath` command.
- **`reverse` optimization** (sql#4775): Performance optimization for the `reverse` operation.
- **Trailing pipes** (sql#5161): PPL queries now support trailing pipes and empty pipes.
- **ANTLR upgrade** (sql#5159): Bumped ANTLR version to 4.13.2.
- **FIPS awareness** (sql#5155): SQL plugin now recognizes the FIPS build parameter (`-Pcrypto.standard=FIPS-140-3`).
- **Resource monitor errors** (sql#5129): Improved error messages from the resource monitor.

### Bug Fixes

| PR | Description |
|-----|-------------|
| sql#5222 | Fix memory leak: `ExecutionEngine` recreated per query appending to global function registry |
| sql#5221 | Fix PIT (Point in Time) resource leaks in v2 query engine |
| sql#5238 | Fix `isnotnull()` not being pushed down when combined with multiple `!=` conditions |
| sql#5206, sql#5198 | Fix MAP path resolution for symbol-based PPL commands and `top/rare`, `join`, `lookup`, `streamstats` |
| sql#5163 | Return null for double overflow to Infinity in arithmetic |
| sql#5176 | Return actual null from `JSON_EXTRACT` for missing/null paths |
| sql#5145 | Fix multisearch UDT type loss through UNION |
| sql#5149 | Fix path navigation on map columns for `spath` command |
| sql#5114 | Preserve head/TopK semantics for sort-expression pushdown |
| sql#5133 | Fix fallback error handling to show original Calcite error |
| sql#5071 | Fix boolean comparison condition simplified to field |
| sql#5061 | Fix Prometheus connection by wrapping with `AccessController.doPrivilegedChecked` |
| sql#5139 | Revert dynamic column support |
| sql#5158 | Fix bc-fips jar hell by marking dependency as compileOnly |
| sql#5252 | Fix typo: rename `renameClasue` to `renameClause` |
| sql#5283 | Fix flaky TPC-H Q1 test due to bugs in `MatcherUtils.closeTo()` |
| opensearch-dashboards#11376 | Fix strip stats not correctly applied to multi-line PPL queries |
| opensearch-dashboards#11405 | Fix PPL head command to show simple result count in status bar |

## References

### sql Repository
- `https://github.com/opensearch-project/sql/pull/5274` - Add unified query parser API
- `https://github.com/opensearch-project/sql/pull/5268` - Add profiling support to unified query API
- `https://github.com/opensearch-project/sql/pull/5257` - Add Calcite native SQL planning in UnifiedQueryPlanner
- `https://github.com/opensearch-project/sql/pull/5254` - Add query cancellation support via _tasks/_cancel API
- `https://github.com/opensearch-project/sql/pull/5234` - PPL Highlight Support
- `https://github.com/opensearch-project/sql/pull/5228` - Support creating/updating prometheus rules
- `https://github.com/opensearch-project/sql/pull/5227` - Change struct output from list to map
- `https://github.com/opensearch-project/sql/pull/5219` - CloudWatch style contains operator
- `https://github.com/opensearch-project/sql/pull/5209` - Update graphlookup syntax
- `https://github.com/opensearch-project/sql/pull/5162` - Grammar bundle generation API
- `https://github.com/opensearch-project/sql/pull/5161` - Support trailing/empty pipes
- `https://github.com/opensearch-project/sql/pull/5159` - Bump ANTLR to 4.13.2
- `https://github.com/opensearch-project/sql/pull/5157` - PPL convert command
- `https://github.com/opensearch-project/sql/pull/5155` - FIPS build awareness
- `https://github.com/opensearch-project/sql/pull/5144` - PPL MvExpand command
- `https://github.com/opensearch-project/sql/pull/5140` - spath auto-extract mode
- `https://github.com/opensearch-project/sql/pull/5138` - Bi-directional graphlookup
- `https://github.com/opensearch-project/sql/pull/5130` - nomv command
- `https://github.com/opensearch-project/sql/pull/5129` - Improve resource monitor errors
- `https://github.com/opensearch-project/sql/pull/5109` - fetch_size API for PPL
- `https://github.com/opensearch-project/sql/pull/5091` - LAST/FIRST/TAKE TEXT and Scripts support
- `https://github.com/opensearch-project/sql/pull/5080` - fieldformat command
- `https://github.com/opensearch-project/sql/pull/4775` - reverse performance optimization
- `https://github.com/opensearch-project/sql/pull/5253` - graphLookup with literal start value
- `https://github.com/opensearch-project/sql/pull/5287` - Update mend config

### opensearch-dashboards Repository
- `https://github.com/opensearch-project/opensearch-dashboards/pull/11547` - PPL search result highlighting in Explore
- `https://github.com/opensearch-project/opensearch-dashboards/pull/11428` - Backend grammar bundle for autocomplete
- `https://github.com/opensearch-project/opensearch-dashboards/pull/11359` - fetch_size API for PPL queries
- `https://github.com/opensearch-project/opensearch-dashboards/pull/11430` - Skip fetch_size with explicit head
- `https://github.com/opensearch-project/opensearch-dashboards/pull/11405` - Fix PPL head result count
- `https://github.com/opensearch-project/opensearch-dashboards/pull/11376` - Fix strip stats for multi-line PPL
