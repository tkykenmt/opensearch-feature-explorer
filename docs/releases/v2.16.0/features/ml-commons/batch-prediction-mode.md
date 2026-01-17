---
tags:
  - ml-commons
---
# Batch Prediction Mode

## Summary

Batch Prediction Mode adds a new `BATCH_PREDICT` action type to the ML Commons Connector Framework, enabling offline batch inference for large-scale ML workloads. This feature allows users to submit batch prediction jobs to external ML services (Amazon SageMaker, OpenAI, Cohere) through OpenSearch connectors and track job status via ML Tasks APIs.

## Details

### What's New in v2.16.0

This release introduces the foundational batch prediction capability in ML Commons:

- New `BATCH_PREDICT` action type in `ConnectorAction.ActionType` enum
- New REST endpoint: `POST /_plugins/_ml/models/{model_id}/_batch_predict`
- Action type detection from REST request path (no need to specify in request body)
- Support for Amazon SageMaker batch transform jobs
- Support for OpenAI batch API
- Task-based job tracking through ML Tasks APIs
- Added `api.sagemaker.*.amazonaws.com` to default trusted URL regex for batch operations

### Technical Changes

#### New Action Type

The `ConnectorAction.ActionType` enum now includes `BATCH_PREDICT`:

```java
public enum ActionType {
    PREDICT,
    EXECUTE,
    BATCH_PREDICT;
}
```

#### REST API Endpoint

New endpoint for batch prediction:

```
POST /_plugins/_ml/models/{model_id}/_batch_predict
```

The action type is automatically determined from the URL path, eliminating the need to specify it in the request body.

#### Connector Configuration

Connectors can now define a `batch_predict` action alongside the standard `predict` action:

```json
{
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://runtime.sagemaker.<region>.amazonaws.com/endpoints/<endpoint>/invocations",
      "request_body": "${parameters.input}"
    },
    {
      "action_type": "batch_predict",
      "method": "POST",
      "url": "https://api.sagemaker.<region>.amazonaws.com/CreateTransformJob",
      "request_body": "{ \"BatchStrategy\": \"${parameters.BatchStrategy}\", ... }"
    }
  ]
}
```

#### Input Data Set Enhancement

`RemoteInferenceInputDataSet` now includes an `actionType` field to specify the action type for remote inference operations.

#### Statistics Tracking

New `BATCH_PREDICT` action name added to `ActionName` enum for tracking batch prediction statistics separately from real-time predictions.

### Usage Example

1. Create a connector with batch_predict action:

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "SageMaker Batch Connector",
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "us-east-1",
    "service_name": "sagemaker",
    "ModelName": "my-embedding-model",
    "TransformInput": {
      "DataSource": {
        "S3DataSource": {
          "S3Uri": "s3://bucket/input/"
        }
      }
    },
    "TransformOutput": {
      "S3OutputPath": "s3://bucket/output/"
    }
  },
  "actions": [
    {
      "action_type": "batch_predict",
      "method": "POST",
      "url": "https://api.sagemaker.us-east-1.amazonaws.com/CreateTransformJob",
      "request_body": "..."
    }
  ]
}
```

2. Register and deploy a model with the connector

3. Invoke batch prediction:

```json
POST /_plugins/_ml/models/{model_id}/_batch_predict
{
  "parameters": {
    "TransformJobName": "my-batch-job"
  }
}
```

4. Check job status via Tasks API:

```json
GET /_plugins/_ml/tasks/{task_id}
```

## Limitations

- Experimental feature - not recommended for production use
- Supported external services: Amazon SageMaker, OpenAI, Cohere only
- Requires proper IAM permissions for external service access
- Batch job results must be retrieved from the external service's output location

## References

### Documentation
- [Batch Predict API](https://docs.opensearch.org/2.16/ml-commons-plugin/api/model-apis/batch-predict/): Official API documentation

### Blog Posts
- [Scaling Vector Generation: Batch ML Inference](https://opensearch.org/blog/scaling-vector-generation-batch-ml-inference-with-opensearch-ingestion-and-ml-commons/): End-to-end batch inference workflow

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2661](https://github.com/opensearch-project/ml-commons/pull/2661) | Add Batch Prediction Mode in the Connector Framework for batch inference | [#2488](https://github.com/opensearch-project/ml-commons/issues/2488) |

### Connector Blueprints
- [Amazon SageMaker batch predict connector blueprint](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/batch_inference_sagemaker_connector_blueprint.md)
- [OpenAI batch predict connector blueprint](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/batch_inference_openAI_connector_blueprint.md)
