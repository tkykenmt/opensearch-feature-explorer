---
tags:
  - ml-commons
---
# Agentic Search

## Summary

OpenSearch v3.6.0 enhances Agentic Search with three improvements across ml-commons and neural-search: custom fallback queries in QueryPlanningTool, alias and wildcard index pattern support in QueryPlanningTool, and embedding model ID support in the agentic query translator processor.

## Details

### What's New in v3.6.0

#### 1. Custom Fallback Query in QueryPlanningTool (ml-commons)

Previously, when the LLM failed to generate a valid DSL query, QueryPlanningTool always fell back to a basic `match_all` query. Users can now configure a custom `fallback_query` parameter on the QueryPlanningTool to provide a more meaningful fallback.

The fallback query supports parameter substitution using `${parameters.question}` and `${parameters.embedding_model_id}` placeholders, allowing dynamic values to be injected at runtime.

Configuration example:

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Agent with Custom Fallback",
  "type": "flow",
  "tools": [
    {
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "<model-id>",
        "fallback_query": "{\"size\":10,\"query\":{\"multi_match\":{\"query\":\"${parameters.question}\",\"fields\":[\"title\",\"description\"]}}}"
      }
    }
  ]
}
```

The system prompt template now uses a `{{FALLBACK_QUERY}}` placeholder that is replaced with the configured fallback query (or the default `match_all` if none is configured), ensuring the LLM is aware of the correct fallback behavior.

#### 2. Alias and Wildcard Index Pattern Support in QueryPlanningTool (ml-commons)

QueryPlanningTool previously failed with a `NullPointerException` when `index_name` was an alias (e.g., `logs`) or wildcard pattern (e.g., `logs_*`). The `GetIndexResponse` returns mappings keyed by resolved concrete index names, not the original pattern/alias, causing `mappings().get(indexName)` to return `null`.

The fix picks the first index's mapping from the response since indices matching a pattern or alias generally share the same mapping. A warning is logged when multiple indices are resolved to alert users about potential mapping differences.

#### 3. Embedding Model ID in Agentic Query Translator Processor (neural-search)

The `agentic_query_translator` search request processor now accepts an optional `embedding_model_id` parameter. This model ID is passed to the ML agent during execution, enabling the agent to generate neural search queries that reference the correct embedding model.

Configuration example:

```json
PUT _search/pipeline/agentic_pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "<agent-id>",
        "embedding_model_id": "<embedding-model-id>"
      }
    }
  ]
}
```

The `embedding_model_id` parameter:
- Is validated for format (alphanumeric, hyphens, underscores only) and length (max 100 characters)
- Requires cluster version 3.6.0+ at runtime (validated via `MinClusterVersionUtil`)
- Is passed as a parameter to the agent execution, available as `${parameters.embedding_model_id}` in prompts and fallback queries

### Technical Changes

| Component | Change | Repository |
|-----------|--------|------------|
| `QueryPlanningTool` | Added `fallback_query` field and `{{FALLBACK_QUERY}}` prompt placeholder | ml-commons |
| `QueryPlanningTool` | Fixed alias/wildcard index resolution using first mapping from response | ml-commons |
| `QueryPlanningPromptTemplate` | Replaced hardcoded `DEFAULT_QUERY` in prompts with `FALLBACK_QUERY_PROMPT_PLACEHOLDER` | ml-commons |
| `AgenticQueryTranslatorProcessor` | Added `embedding_model_id` optional parameter with validation | neural-search |
| `MLCommonsClientAccessor` | Extended `executeAgent` to pass `embeddingModelId` to agent parameters | neural-search |
| `MinClusterVersionUtil` | Added `isClusterOnOrAfterMinReqVersionForAgenticEmbeddingModelId()` for v3.6.0 check | neural-search |
| BWC Tests | Added `AgenticSearchIT` for restart-upgrade and rolling-upgrade scenarios | neural-search |

## Limitations

- The `embedding_model_id` parameter requires all cluster nodes to be on v3.6.0+; it fails at runtime on older cluster versions
- When using alias/wildcard patterns, only the first resolved index's mapping is used; indices with different mappings may produce incorrect queries

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [ml-commons#4729](https://github.com/opensearch-project/ml-commons/pull/4729) | Add support for custom fallback query in QueryPlanningTool for agentic search |  |
| [ml-commons#4726](https://github.com/opensearch-project/ml-commons/pull/4726) | Support aliases and wildcard index patterns in QueryPlanningTool | [neural-search#1799](https://github.com/opensearch-project/neural-search/issues/1799) |
| [neural-search#1800](https://github.com/opensearch-project/neural-search/pull/1800) | Support embedding model id in agentic query translator processor for neural queries | [neural-search#1801](https://github.com/opensearch-project/neural-search/issues/1801) |
