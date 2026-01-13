---
tags:
  - opensearch
---
# Ingest Pipeline - Verbose Pipeline Parameter

## Summary

OpenSearch 2.19.0 introduces the `verbose_pipeline` parameter for search pipelines, enabling detailed debugging and tracing of processor execution. When enabled, the search response includes a `processor_results` array containing input/output data, execution time, and status for each processor in the pipeline.

## Details

### What's New in v2.19.0

The `verbose_pipeline` parameter provides transparency into search pipeline execution by tracking:

- **Processor name and tag**: Identifies each processor in the pipeline
- **Execution duration**: Time taken by each processor in milliseconds
- **Input/output data**: The data before and after processor transformation
- **Status**: Success or failure status of each processor
- **Error messages**: Detailed error information when processors fail

### Technical Changes

#### New Parameter

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `verbose_pipeline` | Boolean | `false` | Enables detailed processor execution tracking |

#### New Response Field

When `verbose_pipeline=true`, the response includes:

```json
{
  "processor_results": [
    {
      "processor_name": "filter_query",
      "tag": "tag1",
      "duration_millis": 288541,
      "status": "success",
      "input_data": { ... },
      "output_data": { ... }
    }
  ]
}
```

#### New Classes

| Class | Description |
|-------|-------------|
| `ProcessorExecutionDetail` | Captures execution details for each processor |
| `TrackingSearchRequestProcessorWrapper` | Wraps request processors to track execution |
| `TrackingSearchResponseProcessorWrapper` | Wraps response processors to track execution |

### Usage Examples

#### With Query Parameter

```
GET /my_index/_search?search_pipeline=my_pipeline&verbose_pipeline=true
```

#### With Default Pipeline

```json
PUT /my_index/_settings
{
  "index.search.default_pipeline": "my_pipeline"
}

GET /my_index/_search?verbose_pipeline=true
```

#### With Temporary Pipeline

```json
POST /my_index/_search?verbose_pipeline=true
{
  "query": { "match": { "text_field": "search text" }},
  "search_pipeline": {
    "request_processors": [
      {
        "filter_query": {
          "query": { "term": { "visibility": "public" }}
        }
      }
    ]
  }
}
```

### Error Handling

When `verbose_pipeline` is enabled, processor failures are logged but do not interrupt the search execution. The error details are captured in the `processor_results`:

```json
{
  "processor_name": "rename_field",
  "duration_millis": 0,
  "status": "fail",
  "error": "Document with id 1 is missing field message",
  "input_data": [ ... ],
  "output_data": null
}
```

## Limitations

- Enabling verbose mode adds computational overhead due to additional tracking
- The `verbose_pipeline` parameter requires a search pipeline to be defined; using it without a pipeline throws an error
- Input/output data serialization may increase response size significantly for large result sets

## References

### Documentation
- [Debugging a Search Pipeline](https://docs.opensearch.org/2.19/search-plugins/search-pipelines/debugging-search-pipeline/)

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16843](https://github.com/opensearch-project/OpenSearch/pull/16843) | Add verbose pipeline parameter to output each processor's execution details | [#14745](https://github.com/opensearch-project/OpenSearch/issues/14745) |

### Issues
- [#14745](https://github.com/opensearch-project/OpenSearch/issues/14745): Feature request for verbose/debugging param in search pipelines
- [#16705](https://github.com/opensearch-project/OpenSearch/issues/16705): RFC for tracking search pipeline execution
