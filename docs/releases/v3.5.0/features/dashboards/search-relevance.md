---
tags:
  - dashboards-search-relevance
---
# Search Relevance

## Summary

OpenSearch v3.5.0 brings significant enhancements to the Search Relevance Workbench, including LLM judgment customization with dynamic prompt templates, new `_search` API endpoints for all entities, UBI sample datasets, improved UI/UX for judgment details and search configuration reuse, and version-based index mapping updates for seamless upgrades.

## Details

### What's New in v3.5.0

#### LLM Judgment Customization
- Customizable prompt templates for LLM-based relevance judgments
- Three rating types: `SCORE0_1` (0-1 scale), `SCORE1_5` (1-5 scale), `RELEVANT_IRRELEVANT` (binary)
- Enhanced caching system with prompt template differentiation
- `overwriteCache` parameter for forced cache refresh

#### New `_search` API Endpoints
Added OpenSearch DSL-based search endpoints for all Search Relevance entities:
- `POST _plugins/_search_relevance/query_sets/_search` - Search Query Sets
- `POST _plugins/_search_relevance/search_configurations/_search` - Search Search Configurations
- `POST _plugins/_search_relevance/judgments/_search` - Search Judgments (filters out ratings)
- `POST _plugins/_search_relevance/experiments/_search` - Search Experiments

#### UBI Sample Dataset
- Added User Behavior Insights (UBI) sample dataset for understanding user interaction patterns
- Pre-built UBI dashboards for visualization
- Integration with Search Relevance Workbench playground

#### UI/UX Improvements
- Search Configuration reuse in Single Query and Query Compare workflows
- Improved Judgment Detail page with structured table view (Query, Doc ID, Rating)
- Search/filter capability and pagination for judgment ratings
- Search Pipeline display in Search Configuration Detail page
- Optional `status=COMPLETED` filter for judgment dropdowns

#### Infrastructure Improvements
- Version-based index mapping updates with `_meta.schema_version` field
- Automatic mapping updates on API calls when schema version changes
- Description field support for Search Configurations

### Technical Changes

#### API Enhancements

| Endpoint | Change |
|----------|--------|
| `PUT _plugins/_search_relevance/judgments` | Added `promptTemplate`, `llmJudgmentRatingType`, `overwriteCache` parameters |
| `PUT _plugins/_search_relevance/search_configurations` | Added `description` field support |
| `*/_search` | New endpoints for all entity types |

#### Index Mapping Version System

```json
{
  "_meta": {
    "schema_version": 0
  }
}
```

Version comparison logic:
- Version -1: Error reading from cluster state → skip update
- Version 0: Legacy index or initial version
- Version 1+: Future versions when mappings are updated

## Limitations

- LLM judgment customization requires ML Commons connector configuration
- `_search` endpoints target system-protected indexes
- Index mapping updates are forward-only (no downgrade support)

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#667](https://github.com/opensearch-project/dashboards-search-relevance/pull/667) | Add FrontEnd Support for LLM Judgement Template Prompt | dashboards-search-relevance |
| [#727](https://github.com/opensearch-project/dashboards-search-relevance/pull/727) | Reuse Search Configurations with Single Query Comparison UI | dashboards-search-relevance |
| [#729](https://github.com/opensearch-project/dashboards-search-relevance/pull/729) | Add UBI sample dataset and dashboards | dashboards-search-relevance |
| [#674](https://github.com/opensearch-project/dashboards-search-relevance/pull/674) | Add optional status=COMPLETED parameter for filtering judgments | dashboards-search-relevance |
| [#699](https://github.com/opensearch-project/dashboards-search-relevance/pull/699) | Add Search Pipeline to Search Configuration Detail page | dashboards-search-relevance |
| [#713](https://github.com/opensearch-project/dashboards-search-relevance/pull/713) | Improve UX of the Judgment Detail page | dashboards-search-relevance |
| [#344](https://github.com/opensearch-project/search-relevance/pull/344) | Version-based index mapping update support | search-relevance |
| [#264](https://github.com/opensearch-project/search-relevance/pull/264) | LLM Judgement Customized Prompt Template Implementation | search-relevance |
| [#372](https://github.com/opensearch-project/search-relevance/pull/372) | Add `_search` endpoint for Search Configurations | search-relevance |
| [#371](https://github.com/opensearch-project/search-relevance/pull/371) | Add `_search` endpoint for Judgments | search-relevance |
| [#362](https://github.com/opensearch-project/search-relevance/pull/362) | Add `_search` endpoint for Query Sets | search-relevance |
| [#369](https://github.com/opensearch-project/search-relevance/pull/369) | Add `_search` endpoint for Experiments | search-relevance |
| [#354](https://github.com/opensearch-project/search-relevance/pull/354) | Better ESCI demo dataset with images | search-relevance |
| [#364](https://github.com/opensearch-project/search-relevance/pull/364) | Support for parsing custom UBI indexes | search-relevance |
| [#370](https://github.com/opensearch-project/search-relevance/pull/370) | Add description support in Search Configuration | search-relevance |
| [#349](https://github.com/opensearch-project/search-relevance/pull/349) | Add BWC and Integration tests for index mapping update | search-relevance |
| [#374](https://github.com/opensearch-project/search-relevance/pull/374) | Fix jackson annotations version | search-relevance |

### Issues
- [#695](https://github.com/opensearch-project/dashboards-search-relevance/issues/695): Search Configuration reuse in comparison UI
- [#691](https://github.com/opensearch-project/dashboards-search-relevance/issues/691): Judgment Detail page UX improvements
- [#730](https://github.com/opensearch-project/dashboards-search-relevance/issues/730): UBI sample dataset
- [#310](https://github.com/opensearch-project/search-relevance/issues/310): Index mapping update with version
- [#351](https://github.com/opensearch-project/search-relevance/issues/351): `_search` endpoints for entities
- [#281](https://github.com/opensearch-project/search-relevance/issues/281): Description field for Search Configuration
- [#266](https://github.com/opensearch-project/search-relevance/issues/266): Filter completed judgments in dropdown
