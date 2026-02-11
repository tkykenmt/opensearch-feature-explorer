---
tags:
  - opensearch-dashboards
---
# Prometheus Metrics in Explore

## Summary

OpenSearch Dashboards v3.5.0 introduces Prometheus as a first-class data source within the Explore plugin. Users can now write and execute PromQL queries directly in the Explore metrics page, view results in table and raw formats, run multiple queries using semicolon delimiters, and leverage AI-powered PromQL query generation via an ag-ui agent. This feature requires the Explore plugin with multi-datasource and observability workspace enabled.

## Details

### What's New in v3.5.0

#### PromQL Language Support
- Full PromQL grammar with ANTLR-based parser for syntax highlighting and validation
- Rich autocomplete for metrics, labels, label values, functions, aggregation operators, and time units
- Trigger characters and documentation links in autocomplete suggestions
- PromQL label displayed in the query editor with user-friendly language title ("PromQL" instead of "PROMQL")

#### Server-Side Prometheus Integration
- PromQL search strategy reusing OSD resources and search strategy infrastructure
- Direct-query PromQL endpoints through the SQL plugin
- Prometheus resource client for browsing labels, values, metrics, and metadata
- Pluggable per-connection query manager registration
- Public resource client factory accessible from the data plugin setup

#### Metrics Page UI
- New "Metrics" flavor page in Explore's Discover interface for Prometheus data sources
- Metrics data table showing Prometheus "instant" results with columns and client-side pagination
- "Raw" tab displaying results in `metric_name{label_1="value_1", label_2="value_2"}` format with expand/collapse, copy-to-clipboard functionality
- Flavor-aware dataset initialization and language propagation
- Language toggle hidden for Metrics flavor

#### Multi-Query Support
- Semicolon-delimited multi-query execution (e.g., `up; node_cpu_seconds_total`)
- Per-query value columns, labels, and gutter identifiers in the editor
- Autocomplete context awareness for multi-query positions

#### AI-Powered Query Generation
- PromQL query generation using `os_query_assist_promql` agent (initially via ml-commons, later migrated to ag-ui agent)
- `search_prometheus_metadata` tool that takes a regex pattern and returns matched metrics with labels and sample values
- Configurable limits for metrics (default 20), labels per metric (default 20), and sample values per label (default 5)
- `chat.observabilityAgentId` configuration for routing PromQL generation requests through the chat proxy API
- Gzip response streaming support in chat proxy API

#### Connection Simplification
- Removed Multi-Data Source (MDS) support for Prometheus connections
- Prometheus always uses the local OpenSearch cluster as proxy, eliminating the need to select a remote cluster
- Removed unused `meta` field from Prometheus data-connection saved objects to prevent potential credential exposure

#### Error Handling
- Improved error propagation for Prometheus API calls
- Errors from auth failures, Prometheus downtime, or invalid requests now properly surface in the UI instead of being silently swallowed

## Limitations

- Requires Explore plugin enabled with multi-datasource feature and observability workspace (`yarn start:explore` for development)
- Multi-query uses semicolon delimiters rather than stacked query editors (may change in future versions)
- AI query generation currently only includes the latest tool call result in the prompt (ag-ui agent limitation)
- System prompts for query generation are passed as user prompts due to ag-ui agent implementation constraints
- Prometheus connections always use the local cluster; remote cluster proxy is not supported

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11039](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11039) | Add prometheus server APIs and frontend type config | |
| [#11037](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11037) | Add prometheus grammar and autocomplete functions | |
| [#11073](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11073) | Add prometheus metrics page in explore | [#9535](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9535) |
| [#11095](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11095) | Add raw table to prometheus results page | [#9535](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9535) |
| [#11127](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11127) | Support multi query for prometheus in explore | |
| [#11153](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11153) | Support query generation for PromQL in Explore | |
| [#11154](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11154) | Remove MDS support for Prometheus connections | |
| [#11165](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11165) | Show PromQL label in explore metrics page query editor | |
| [#11201](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11201) | Change PromQL generation to use ag-ui agent | |
| [#11167](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11167) | Improve error handling for prometheus APIs in Explore | |
| [#11280](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11280) | Remove meta field for prometheus data-connection | |

### Issues
| Issue | Description |
|-------|-------------|
| [#9535](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9535) | [RFC] Prometheus as a first class datasource |
