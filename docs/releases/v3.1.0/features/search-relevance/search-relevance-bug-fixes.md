# Search Relevance Bug Fixes

## Summary

OpenSearch v3.1.0 includes significant bug fixes and improvements to the Search Relevance Workbench plugin. These changes address data model issues, improve error handling, fix floating-point precision errors, and add input validation to enhance stability and usability.

## Details

### What's New in v3.1.0

This release focuses on stabilizing the Search Relevance Workbench with fixes across several areas:

1. **Data Model Improvements**: Restructured Judgment, Experiment, and Evaluation Result entities to use fixed field names instead of dynamic fields
2. **LLM Judgment Processing**: Improved error handling and fixed duplication issues
3. **Search Request Building**: Enhanced query parsing to support all search request fields
4. **Hybrid Optimizer Fixes**: Resolved floating-point precision errors in variant generation
5. **Input Validation**: Added text validation and query set file size limits

### Technical Changes

#### Data Model Restructuring

The plugin previously used dynamic field names based on values (e.g., search configuration IDs, metric names), which caused issues with field limits. The new model uses fixed field structures:

**Judgment Model (PR #77)**:
```json
{
  "name": "ESCI Judgments",
  "type": "IMPORT_JUDGMENT",
  "judgmentScores": [
    {
      "query": "laptop",
      "ratings": [
        { "docId": "B07NCQWCQS", "rating": "1.0" },
        { "docId": "B07NPC54DK", "rating": "0.7" }
      ]
    }
  ]
}
```

**Experiment Results Model (PR #99)**:
- Results stored as arrays with `queryText`, `metrics`, and `snapshots` fields
- Metrics use `metric` and `value` fields instead of dynamic metric names
- Search configuration IDs stored as values, not field names

#### Index Field Limit Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| `index.mapping.total_fields.limit` | 100,000 | Programmatically set for search relevance indexes |

#### LLM Judgment Processor Improvements (PR #27)

| Feature | Description |
|---------|-------------|
| `ignoreFailure` flag | Configurable error handling - continue on failure or fail immediately |
| Decoupled LLM judgment | Removed on-the-fly LLM generation during experiments |
| Experiment type redefinition | PAIRWISE_COMPARISON, POINTWISE_EVALUATION, HYBRID_SEARCH_OPTIMIZATION |
| Index migration | Moved judgment, evaluation_results, query_set, search_configuration out of system indices |

#### Search Request Builder Fix (PR #22)

The search request builder now properly handles all query fields:
- Uses `WrapperQuery` for custom query types (hybrid, neural) not registered in default QueryBuilders
- Parses all other fields (aggregations, source filtering) normally via SearchSourceBuilder
- Supports aggregations, `_source` filtering, and `search_pipeline` in search configurations

#### Hybrid Optimizer Floating-Point Fix (PR #124)

Fixed missing experiment variants caused by floating-point precision errors:
- Calculates exact number of steps needed
- Uses integer counter to avoid floating-point accumulation errors
- Ensures maximum value is precisely included by special-casing the last step

#### Input Validation (PR #116)

| Validation | Default | Description |
|------------|---------|-------------|
| Query set size limit | 150 queries | Prevents node overload from large batch processing |
| Text validation | Enabled | Validates input text fields |

### Usage Example

Running a pointwise evaluation with the fixed data model:

```json
POST _plugins/_search_relevance/experiments
{
  "querySetId": "62e3a24c-7d1a-48ef-82c1-98aafb090f0d",
  "searchConfigurationList": ["6dc64be4-7417-43d0-9758-444c1bb5dbb9"],
  "judgmentList": ["0d8f741a-0904-48ab-80ae-fde569d3405a"],
  "size": 8,
  "type": "POINTWISE_EVALUATION"
}
```

Response structure with fixed field names:
```json
{
  "results": [
    {
      "evaluationId": "debb9976-777c-4677-99f5-9c8820828ab0",
      "searchConfigurationId": "6dc64be4-7417-43d0-9758-444c1bb5dbb9",
      "queryText": "tv"
    }
  ]
}
```

### Migration Notes

- Existing judgment data using the old dynamic field model will need to be re-imported
- Query sets exceeding 150 queries may need to be split into smaller batches
- The `ignoreFailure` flag defaults to `false` for backward compatibility

## Limitations

- Query set size limited to 150 queries by default (configurable)
- Existing data using dynamic field names requires migration

## References

### Documentation
- [Search Relevance Workbench Documentation](https://docs.opensearch.org/3.1/search-plugins/search-relevance/using-search-relevance-workbench/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#22](https://github.com/opensearch-project/search-relevance/pull/22) | Build search request with normal parsing and wrapper query |
| [#27](https://github.com/opensearch-project/search-relevance/pull/27) | LLM Judgment Processor improvements |
| [#45](https://github.com/opensearch-project/search-relevance/pull/45) | Handle when no experiment variants exist |
| [#60](https://github.com/opensearch-project/search-relevance/pull/60) | Enable Search Relevance backend plugin in demo scripts |
| [#64](https://github.com/opensearch-project/search-relevance/pull/64) | Migrate from judgment score to judgment rating |
| [#65](https://github.com/opensearch-project/search-relevance/pull/65) | Added lazy index creation for APIs |
| [#69](https://github.com/opensearch-project/search-relevance/pull/69) | Extend hybrid search optimizer demo script |
| [#74](https://github.com/opensearch-project/search-relevance/pull/74) | Set limit for number of fields programmatically |
| [#77](https://github.com/opensearch-project/search-relevance/pull/77) | Change model for Judgment entity |
| [#93](https://github.com/opensearch-project/search-relevance/pull/93) | Fix judgment handling for implicit judgments |
| [#98](https://github.com/opensearch-project/search-relevance/pull/98) | Refactor and fix LLM judgment duplication issue |
| [#99](https://github.com/opensearch-project/search-relevance/pull/99) | Change model for Experiment and Evaluation Result entities |
| [#116](https://github.com/opensearch-project/search-relevance/pull/116) | Add text validation and query set file size check |
| [#124](https://github.com/opensearch-project/search-relevance/pull/124) | Fixed missing variants in Hybrid Optimizer |

### Issues (Design / RFC)
- [Issue #12](https://github.com/opensearch-project/search-relevance/issues/12): LLM Judgment improvements
- [Issue #14](https://github.com/opensearch-project/search-relevance/issues/14): Search request builder fix
- [Issue #55](https://github.com/opensearch-project/search-relevance/issues/55): Lazy index creation
- [Issue #71](https://github.com/opensearch-project/search-relevance/issues/71): Dynamic field mapping issues
- [Issue #95](https://github.com/opensearch-project/search-relevance/issues/95): LLM judgment duplication
- [Issue #109](https://github.com/opensearch-project/search-relevance/issues/109): Missing variants in Hybrid Optimizer
- [Issue #114](https://github.com/opensearch-project/search-relevance/issues/114): Input validation

## Related Feature Report

- [Full feature documentation](../../../../features/search-relevance/search-relevance-workbench.md)
