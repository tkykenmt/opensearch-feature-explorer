# Search Pipeline in Templates

## Summary

OpenSearch v3.2.0 adds support for specifying search pipelines directly in search template and multi-search template (msearch template) requests. This enhancement allows users to apply search pipelines to templated queries, enabling consistent query preprocessing and response postprocessing when using reusable search templates.

## Details

### What's New in v3.2.0

This release extends the search pipeline functionality to work with search templates:

- **Search Template API**: The `search_pipeline` parameter can now be specified in the request body when executing a search template
- **Multi-Search Template API**: Each template request in an msearch template batch can specify its own search pipeline
- **Stored Templates**: Search pipelines work with both inline and stored templates

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Search Template with Pipeline"
        ST[Search Template Request] --> TP[Template Processing]
        TP --> PP[Pipeline Assignment]
        PP --> SR[Search Request]
        SR --> SP[Search Pipeline]
        SP --> SE[Search Execution]
        SE --> RSP[Response Processors]
        RSP --> FR[Final Response]
    end
```

#### New Components

| Component | Description |
|-----------|-------------|
| `SearchTemplateRequest.searchPipeline` | New field to store the pipeline name in template requests |
| `RestSearchTemplateAction` pipeline handling | Logic to transfer pipeline from template request to search request |
| `RestMultiSearchTemplateAction` pipeline handling | Logic to handle per-request pipelines in msearch template |

#### API Changes

The `SearchTemplateRequest` class now supports a `search_pipeline` field:

```java
public String getSearchPipeline();
public void setSearchPipeline(String searchPipeline);
```

The `SearchTemplateRequestBuilder` also supports the new field:

```java
public SearchTemplateRequestBuilder setSearchPipeline(String searchPipeline);
```

### Usage Example

#### Search Template with Pipeline

```json
POST /my-index/_search/template
{
  "id": "my_search_template",
  "params": {
    "query_string": "opensearch"
  },
  "search_pipeline": "my_pipeline"
}
```

#### Multi-Search Template with Per-Request Pipelines

```
GET /_msearch/template
{"index":"my-nlp-index1"}
{"id":"search_template_1","params":{"play_name":"hello","from":0,"size":1}, "search_pipeline": "my_pipeline2"}
{"index":"my-nlp-index1"}
{"id":"search_template_2","params":{"play_name":"zoo","from":0,"size":1}, "search_pipeline": "my_pipeline1"}
```

### Migration Notes

- No migration required - this is a new optional feature
- Existing search templates continue to work without changes
- To use pipelines with templates, simply add the `search_pipeline` field to your template requests

## Limitations

- The `search_pipeline` parameter is only available in the request body, not as a query parameter for template APIs
- Pipeline must exist before being referenced in a template request
- Version compatibility: This feature requires OpenSearch 3.2.0 or later

## Related PRs

| PR | Description |
|----|-------------|
| [#18564](https://github.com/opensearch-project/OpenSearch/pull/18564) | Add support for search pipeline in search and msearch template |

## References

- [Issue #18508](https://github.com/opensearch-project/OpenSearch/issues/18508): Feature request for search pipeline support in msearch template
- [Search Templates Documentation](https://docs.opensearch.org/latest/api-reference/search-apis/search-template/): Official search template docs
- [Multi-Search Template Documentation](https://docs.opensearch.org/latest/api-reference/search-apis/msearch-template/): Official msearch template docs
- [Search Pipelines Documentation](https://docs.opensearch.org/latest/search-plugins/search-pipelines/index/): Search pipeline overview

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/search-pipeline.md)
