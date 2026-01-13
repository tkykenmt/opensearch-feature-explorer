---
tags:
  - opensearch
---
# Ingest Pipeline Deprecation for Update Operations

## Summary

OpenSearch v2.19.0 deprecates the execution of default and final ingest pipelines during Update API operations. When an index has a `default_pipeline` or `final_pipeline` configured and an update operation is performed on an existing document, OpenSearch now emits a deprecation warning. This behavior will be removed entirely in v3.0.0.

## Details

### What's New in v2.19.0

The Update API does not officially support ingest pipelines. However, when an index has a default or final pipeline configured and a document exists, the pipeline was being executed during update operations. This behavior was inconsistent with the Bulk API (which does not trigger pipelines for update operations) and could produce unexpected results.

Starting in v2.19.0:
- Update operations on indexes with `default_pipeline` or `final_pipeline` settings emit a deprecation warning
- The warning message: `the index [<index-name>] has a default ingest pipeline or a final ingest pipeline, the support of the ingest pipelines for update operation causes unexpected result and will be removed in 3.0.0`
- The pipeline still executes (for backward compatibility), but users are warned to adjust their workflows

### Technical Changes

The change was implemented in `TransportUpdateAction.java`:

```java
final Settings indexSettings = indexService.getIndexSettings().getSettings();
if (IndexSettings.DEFAULT_PIPELINE.exists(indexSettings) || 
    IndexSettings.FINAL_PIPELINE.exists(indexSettings)) {
    deprecationLogger.deprecate(
        "update_operation_with_ingest_pipeline",
        "the index [" + indexRequest.index() + 
        "] has a default ingest pipeline or a final ingest pipeline, " +
        "the support of the ingest pipelines for update operation causes " +
        "unexpected result and will be removed in 3.0.0"
    );
}
```

### Behavior Comparison

| Operation | v2.18.0 and earlier | v2.19.0 | v3.0.0 (planned) |
|-----------|---------------------|---------|------------------|
| Index with default/final pipeline | Pipeline executes | Pipeline executes | Pipeline executes |
| Update with default/final pipeline | Pipeline executes (silently) | Pipeline executes + warning | Pipeline does NOT execute |
| Bulk update with default/final pipeline | Pipeline does NOT execute | Pipeline does NOT execute | Pipeline does NOT execute |

### Migration Guidance

If your application relies on ingest pipelines being executed during update operations:

1. **Review your update workflows**: Identify any update operations that depend on pipeline processing
2. **Consider alternatives**:
   - Use index operations instead of updates when pipeline processing is needed
   - Implement the transformation logic in your application before sending updates
   - Use the Bulk API with `doc_as_upsert: true` if you need pipeline execution
3. **Test with v3.0.0**: Before upgrading to v3.0.0, test your application to ensure update operations work correctly without pipeline execution

## Limitations

- The deprecation warning is emitted for every update operation on affected indexes, which may increase log volume
- No configuration option to suppress the warning while maintaining the deprecated behavior

## References

### Documentation
- [Update Document API](https://docs.opensearch.org/2.19/api-reference/document-apis/update-document/): Official documentation with deprecation notice

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16712](https://github.com/opensearch-project/OpenSearch/pull/16712) | Deprecate performing update operation with default pipeline or final pipeline | [#16663](https://github.com/opensearch-project/OpenSearch/issues/16663) |

### Issues
- [#16663](https://github.com/opensearch-project/OpenSearch/issues/16663): Bug report about inconsistent ingest pipeline behavior between Update API and Bulk API
