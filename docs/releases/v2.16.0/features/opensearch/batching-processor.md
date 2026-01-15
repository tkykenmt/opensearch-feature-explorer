---
tags:
  - opensearch
---
# Batching Processor

## Summary

OpenSearch v2.16.0 introduces `AbstractBatchingProcessor`, a new base class for ingest processors that enables efficient batch processing of documents. This allows processors to handle multiple documents simultaneously rather than one at a time, improving performance for bulk ingestion workloads.

## Details

### What's New in v2.16.0

The `AbstractBatchingProcessor` abstract class provides a foundation for building ingest processors that can process documents in batches. It offers two key functionalities:

1. **Batch size configuration**: Parses the `batch_size` parameter from processor configuration
2. **Automatic batch splitting**: Splits incoming documents into batches based on the configured batch size

### Technical Changes

#### New Class: AbstractBatchingProcessor

Located at `org.opensearch.ingest.AbstractBatchingProcessor`, this class extends `AbstractProcessor` and provides:

| Component | Description |
|-----------|-------------|
| `BATCH_SIZE_FIELD` | Configuration field name (`batch_size`) |
| `DEFAULT_BATCH_SIZE` | Default value of 1 (single document processing) |
| `batchSize` | Protected field storing the configured batch size |

#### Key Methods

| Method | Description |
|--------|-------------|
| `batchExecute()` | Overrides the default batch execution to split documents into sub-batches |
| `subBatchExecute()` | Abstract method that concrete processors must implement for actual batch processing |
| `cutBatches()` | Internal method that splits documents into batches of the configured size |

#### Factory Class

The `AbstractBatchingProcessor.Factory` abstract class handles:
- Reading `batch_size` from processor configuration
- Validating that batch size is a positive integer
- Delegating to `newProcessor()` for concrete processor instantiation

### Configuration

Processors extending `AbstractBatchingProcessor` accept the following configuration:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `batch_size` | Integer | 1 | Number of documents to process in each batch |

### Usage Example

Processors that extend `AbstractBatchingProcessor` can be configured in an ingest pipeline:

```json
PUT _ingest/pipeline/my-batch-pipeline
{
  "processors": [
    {
      "my_batch_processor": {
        "batch_size": 10,
        "field_map": {
          "input_field": "output_field"
        }
      }
    }
  ]
}
```

## Limitations

- The default batch size is 1, meaning batch processing is opt-in
- Concrete processors must implement `subBatchExecute()` to leverage batch processing
- Batch processing is most beneficial when used with the Bulk API

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14554](https://github.com/opensearch-project/OpenSearch/pull/14554) | Add batching processor base type AbstractBatchingProcessor | [#14283](https://github.com/opensearch-project/OpenSearch/issues/14283) |
| [#14595](https://github.com/opensearch-project/OpenSearch/pull/14595) | Backport to 2.x branch | - |

### Related Issues

- [#14283](https://github.com/opensearch-project/OpenSearch/issues/14283) - Feature request for automatic batch ingestion

### Documentation

- [Ingest Processors](https://docs.opensearch.org/2.16/ingest-pipelines/processors/index-processors/)
- [Bulk API](https://docs.opensearch.org/2.16/api-reference/document-apis/bulk/)
