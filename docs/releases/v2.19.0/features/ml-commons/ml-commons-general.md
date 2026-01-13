---
tags:
  - ml-commons
---
# ML Commons General Enhancements

## Summary

OpenSearch v2.19.0 brings significant enhancements to ML Commons, including improved conversational AI capabilities, multi-modal model support, enhanced Memory API validation, batch task management, and various bug fixes for stability and reliability.

## Details

### What's New in v2.19.0

#### Conversational AI Enhancements

**Application Type in Conversations**
- Added `application_type` field to `ConversationMeta` data model
- Enables categorization of conversations by application context
- Returned in `getMemory` (Conversation) API responses

**Action Input Parameters for Tools**
- Conversational agents can now pass action input as parameters during tool execution
- Improves flexibility in agent-tool interactions
- Enables more dynamic tool invocation patterns

**Memory API Validation and Storage Optimization**
- Skip saving empty fields in interactions and conversations to optimize storage
- GET requests for interactions and conversations return only non-null fields
- Throws exception if all fields in create interaction call are empty or null

#### Multi-Modal Support

**Cohere Multi-Modal Pre-Processor**
- New pre-processor for Cohere multi-modal embedding models
- Supports array of texts or single base64 image input
- Enables image embedding use cases with Cohere models

#### Model Management

**Adagrad Optimizer for Linear Regression**
- Changed default optimizer from SIMPLE_SGD to ADA_GRAD
- Improves convergence for linear regression training

**Undeploy Models with No Worker Nodes**
- Models with no associated worker nodes are now properly undeployed
- Fixes issue where model index showed `PARTIALLY_DEPLOYED` with no serving nodes
- Ensures model state consistency after cluster topology changes

#### Batch Task Management

**Periodic Remote Task Polling**
- New cron job for periodically polling remote batch tasks
- Enables better management of long-running batch inference jobs
- Automatic status synchronization with remote services

#### Connector and Endpoint Updates

**New Trusted Endpoints**
- Added DeepSeek as a trusted endpoint
- Added Amazon Rekognition as a trusted endpoint

**Connector Validation Enhancement**
- Enhanced validation for create connector API
- Improved error messages for invalid connector configurations

#### ML Inference Search Extension

**Search Request Extension**
- Introduced `ml_inference` search request extension
- Complements the existing search response extension from v2.18
- Enables ML inference during search request/query phase

#### Bedrock Rerank Support

**Pre/Post Process Functions**
- Added pre and post process functions for Bedrock Rerank API
- Enables integration with Amazon Bedrock's reranking capabilities

#### Skills Plugin Enhancements

**S3 Data Source Support**
- Support for S3 data sources using repackage in text-to-PPL
- Enables schema and sample passing from frontend for non-indexed data sources

**Model Related Fields for Tools**
- Added model related field tracking for tools
- Enables downstream task validation before model deletion

### Technical Changes

#### System Index Mappings
- Fetch system index mappings from JSON files instead of string constants
- Added schema validation and placeholders to index mappings

#### Logging Improvements
- Modified log levels for better error visibility
- Added detailed error logging for debugging

#### Check Before Delete
- Added validation checks before deleting resources
- Prevents accidental deletion of resources with dependencies

## Limitations

- Cohere multi-modal pre-processor supports only single image in array (Cohere API limitation)
- Batch task polling interval is fixed by cron job configuration
- Memory API validation may reject previously valid requests with all-empty fields

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#3282](https://github.com/opensearch-project/ml-commons/pull/3282) | Add application_type to ConversationMeta | ml-commons |
| [#3283](https://github.com/opensearch-project/ml-commons/pull/3283) | Enhance Message and Memory API Validation and storage | ml-commons |
| [#3291](https://github.com/opensearch-project/ml-commons/pull/3291) | Use Adagrad optimizer for Linear regression by default | ml-commons |
| [#3200](https://github.com/opensearch-project/ml-commons/pull/3200) | Add action input as parameters for tool execution | ml-commons |
| [#3219](https://github.com/opensearch-project/ml-commons/pull/3219) | Adding multi-modal pre-processor for Cohere | ml-commons |
| [#3380](https://github.com/opensearch-project/ml-commons/pull/3380) | Undeploy models with no WorkerNodes | ml-commons |
| [#3421](https://github.com/opensearch-project/ml-commons/pull/3421) | Support batch task management by periodic polling | ml-commons |
| [#3440](https://github.com/opensearch-project/ml-commons/pull/3440) | Add DeepSeek as a trusted endpoint | ml-commons |
| [#3419](https://github.com/opensearch-project/ml-commons/pull/3419) | Added Amazon Rekognition as a trusted endpoint | ml-commons |
| [#3260](https://github.com/opensearch-project/ml-commons/pull/3260) | Enhance validation for create connector API | ml-commons |
| [#3284](https://github.com/opensearch-project/ml-commons/pull/3284) | Introduce ML Inference Search Request Extension | ml-commons |
| [#3254](https://github.com/opensearch-project/ml-commons/pull/3254) | Add pre and post process functions for Bedrock Rerank API | ml-commons |
| [#3153](https://github.com/opensearch-project/ml-commons/pull/3153) | Fetch system index mappings from JSON file | ml-commons |
| [#3240](https://github.com/opensearch-project/ml-commons/pull/3240) | Add schema validation and placeholders to index mappings | ml-commons |
| [#3337](https://github.com/opensearch-project/ml-commons/pull/3337) | Refactor: modifying log levels and adding more logs | ml-commons |
| [#3209](https://github.com/opensearch-project/ml-commons/pull/3209) | Check before delete | ml-commons |
| [#482](https://github.com/opensearch-project/skills/pull/482) | Support S3 using repackage | skills |
| [#491](https://github.com/opensearch-project/skills/pull/491) | Add model related field for tools | skills |

### Bug Fixes

| PR | Description | Repository |
|----|-------------|------------|
| [#3226](https://github.com/opensearch-project/ml-commons/pull/3226) | getFirst is not allowed in Java 17 | ml-commons |
| [#3198](https://github.com/opensearch-project/ml-commons/pull/3198) | Fix FileUtils long to int cast issue | ml-commons |
| [#3241](https://github.com/opensearch-project/ml-commons/pull/3241) | Fix sync up job not working in 2.17 upgrades | ml-commons |
| [#3289](https://github.com/opensearch-project/ml-commons/pull/3289) | Fix remote model with embedding input issue | ml-commons |
| [#3281](https://github.com/opensearch-project/ml-commons/pull/3281) | Adds preset contentRegistry for IngestProcessors | ml-commons |
| [#2976](https://github.com/opensearch-project/ml-commons/pull/2976) | Revert filter out remote model auto redeployment | ml-commons |
| [#3434](https://github.com/opensearch-project/ml-commons/pull/3434) | Fix JsonGenerationException in Local Sample Calculator | ml-commons |
| [#3468](https://github.com/opensearch-project/ml-commons/pull/3468) | Fix guardrail IT for 2.19 | ml-commons |
| [#3474](https://github.com/opensearch-project/ml-commons/pull/3474) | Addressing client changes due to adding tenantId | ml-commons |
