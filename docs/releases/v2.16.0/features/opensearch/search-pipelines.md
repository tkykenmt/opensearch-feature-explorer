---
tags:
  - opensearch
---
# Search Pipelines

## Summary

OpenSearch 2.16.0 adds two new search response processors to search pipelines: `SortResponseProcessor` and `SplitResponseProcessor`. These processors enable post-processing of search results by sorting array fields and splitting string fields into arrays, respectively. They complement the existing ingest pipeline processors with equivalent functionality for search responses.

## Details

### What's New in v2.16.0

Two new `SearchResponseProcessor` implementations were added to the search-pipeline-common module:

| Processor | Type | Description |
|-----------|------|-------------|
| `sort` | Response | Sorts an array field in ascending or descending order |
| `split` | Response | Splits a string field into an array using a delimiter |

### SortResponseProcessor

The `sort` processor sorts array fields in search response documents. It supports both ascending and descending order, and can store results in a separate target field.

**Configuration Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `field` | String | Yes | - | The array field to sort |
| `order` | String | No | `asc` | Sort order: `asc` or `desc` |
| `target_field` | String | No | Same as `field` | Field to store sorted results |
| `tag` | String | No | - | Processor identifier |
| `description` | String | No | - | Processor description |
| `ignore_failure` | Boolean | No | `false` | Continue on failure |

**Example:**

```json
PUT /_search/pipeline/sort_pipeline
{
  "response_processors": [
    {
      "sort": {
        "field": "scores",
        "order": "desc",
        "target_field": "sorted_scores"
      }
    }
  ]
}
```

### SplitResponseProcessor

The `split` processor splits string fields into arrays using a separator pattern. It supports regular expressions for complex splitting patterns.

**Configuration Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `field` | String | Yes | - | The string field to split |
| `separator` | String | Yes | - | Delimiter pattern (supports regex) |
| `preserve_trailing` | Boolean | No | `false` | Keep empty trailing strings |
| `target_field` | String | No | Same as `field` | Field to store split results |
| `tag` | String | No | - | Processor identifier |
| `description` | String | No | - | Processor description |
| `ignore_failure` | Boolean | No | `false` | Continue on failure |

**Example:**

```json
PUT /_search/pipeline/split_pipeline
{
  "response_processors": [
    {
      "split": {
        "field": "tags_csv",
        "separator": ",",
        "target_field": "tags"
      }
    }
  ]
}
```

### Technical Implementation

Both processors:
- Implement the `SearchResponseProcessor` interface
- Process both document fields and `_source` content
- Support the standard processor options (`tag`, `description`, `ignore_failure`)
- Are registered in `SearchPipelineCommonModulePlugin`

## Limitations

- The `sort` processor throws an exception if the field is not an array or contains non-comparable values
- The `split` processor throws an exception if the field is not a string
- Both processors require the field to exist in the document (unless `ignore_failure` is set)

## References

### Documentation
- [Sort Processor](https://docs.opensearch.org/2.16/search-plugins/search-pipelines/sort-processor/): Official documentation
- [Search Processors](https://docs.opensearch.org/2.16/search-plugins/search-pipelines/search-processors/): Search processors overview

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14785](https://github.com/opensearch-project/OpenSearch/pull/14785) | Add SortResponseProcessor to Search Pipelines | [#14758](https://github.com/opensearch-project/OpenSearch/issues/14758) |
| [#14800](https://github.com/opensearch-project/OpenSearch/pull/14800) | Add SplitResponseProcessor to Search Pipelines | [#14758](https://github.com/opensearch-project/OpenSearch/issues/14758) |

### Related Documentation PRs
- [documentation-website#7767](https://github.com/opensearch-project/documentation-website/pull/7767): Documentation for sort and split processors
- [opensearch-api-specification#440](https://github.com/opensearch-project/opensearch-api-specification/pull/440): API specification updates
