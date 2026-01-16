---
tags:
  - ml-commons
---
# ML Commons Connector & Model Fixes

## Summary

OpenSearch 2.16.0 includes multiple bug fixes for ML Commons connectors and model handling. These fixes address permission issues with connector access, improve model deployment settings for remote models, enhance connector update behavior, and fix various parsing and response handling issues.

## Details

### What's New in v2.16.0

#### Connector Access Permission Fix
Added `StashContext` to connector getter operations to prevent permission errors when accessing connectors. This ensures that connector retrieval works correctly regardless of the calling context's security permissions.

#### Remote Model Exclusion from Node Limits
Remote models are now excluded from the `plugins.ml_commons.max_model_on_node` setting. Previously, this setting counted all models including remote models, which was incorrect since remote models don't consume local node resources. This fix allows more local models to be deployed when remote models are also in use.

#### Connector Update Parameter Merging
When updating connectors, existing parameters are now merged with the updated parameters instead of being replaced entirely. This improves the user experience by allowing partial updates without needing to re-specify all existing parameters.

#### Config Index Mapping Fixes
Fixed config index mappings to use correct field types. Added new fields (`ml_configuration`, `config_type`, `last_updated_time`) to replace incorrectly typed fields from previous versions, ensuring smooth upgrades from 2.13+ versions.

#### ML Inference Processor Fixes
- Fixed `MLModelTool` returning null when LLM response is a pure JSON object
- Fixed JSON array parsing issues in ML inference request processor when running terms queries
- Removed extra `ignoreFailure` handling that caused issues

#### Index Creation Acknowledgment
Added acknowledgment checks for index creation in missing places to ensure index operations complete successfully before proceeding.

#### Logging Improvements
Added logging for throttling and guardrail events in connectors to improve observability and debugging.

### Technical Changes

| Area | Change | PR |
|------|--------|-----|
| Connector Security | Add StashContext to connector getter | [#2742](https://github.com/opensearch-project/ml-commons/pull/2742) |
| Model Deployment | Exclude remote models from max_model_on_node | [#2732](https://github.com/opensearch-project/ml-commons/pull/2732) |
| Connector Update | Merge existing parameters when updating | [#2784](https://github.com/opensearch-project/ml-commons/pull/2784) |
| Config Index | Fix field type mappings | [#2710](https://github.com/opensearch-project/ml-commons/pull/2710) |
| ML Inference | Fix null response for JSON objects | [#2675](https://github.com/opensearch-project/ml-commons/pull/2675) |
| ML Inference | Fix terms query JSON parsing | [#2770](https://github.com/opensearch-project/ml-commons/pull/2770) |
| Index Operations | Add acknowledge check for index creation | [#2715](https://github.com/opensearch-project/ml-commons/pull/2715) |
| Observability | Add throttling/guardrail logging | [#2725](https://github.com/opensearch-project/ml-commons/pull/2725) |

## Limitations

- Config index field migration requires using new field names (`ml_configuration`, `config_type`, `last_updated_time`) from v2.15+ onwards
- Old field names are retained in the index for backward compatibility but should not be used for new data

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2742](https://github.com/opensearch-project/ml-commons/pull/2742) | Add StashContext to connector getter | - |
| [#2732](https://github.com/opensearch-project/ml-commons/pull/2732) | Exclude remote models from max_model_on_node setting | - |
| [#2784](https://github.com/opensearch-project/ml-commons/pull/2784) | Merge existing parameters when updating connectors | [#2502](https://github.com/opensearch-project/ml-commons/issues/2502) |
| [#2710](https://github.com/opensearch-project/ml-commons/pull/2710) | Update config index mappings to use correct field types | [#2630](https://github.com/opensearch-project/ml-commons/issues/2630) |
| [#2675](https://github.com/opensearch-project/ml-commons/pull/2675) | Fix MLModelTool returns null for pure JSON response | [#2654](https://github.com/opensearch-project/ml-commons/issues/2654) |
| [#2770](https://github.com/opensearch-project/ml-commons/pull/2770) | Fix ML inference processor JSON array parsing | - |
| [#2715](https://github.com/opensearch-project/ml-commons/pull/2715) | Add acknowledge check for index creation | - |
| [#2725](https://github.com/opensearch-project/ml-commons/pull/2725) | Add logging for throttling and guardrail | - |
| [#2759](https://github.com/opensearch-project/ml-commons/pull/2759) | Add XContentType to CreateIndexRequest mappings | - |
| [#2700](https://github.com/opensearch-project/ml-commons/pull/2700) | Fix yaml test issue | - |
| [#2656](https://github.com/opensearch-project/ml-commons/pull/2656) | Bump ml config index schema version | - |
| [#2676](https://github.com/opensearch-project/ml-commons/pull/2676) | Fix final answer with extra meaningless symbol | - |
| [#2778](https://github.com/opensearch-project/ml-commons/pull/2778) | Add more logs for automated model interface creation | - |
| [#2582](https://github.com/opensearch-project/ml-commons/pull/2582) | Enable tests with mockStatic in MLEngineTest | - |
| [#2625](https://github.com/opensearch-project/ml-commons/pull/2625) | Fix GA workflow for Maven artifacts | - |
| [#2628](https://github.com/opensearch-project/ml-commons/pull/2628) | Temp use of older nodejs version | - |
