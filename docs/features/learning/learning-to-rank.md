---
tags:
  - learning
---
# Learning to Rank

## Summary

Learning to Rank (LTR) is an OpenSearch plugin that enables machine learning-based search relevance ranking. It uses models from XGBoost and RankLib libraries to rescore search results based on query-dependent features like click-through data or field matches.

The plugin allows you to:
- Define features as OpenSearch queries
- Log feature scores for training data collection
- Upload trained models (RankLib, XGBoost, linear)
- Apply ML models to rescore search results

## Details

### Architecture

```mermaid
graph TB
    subgraph "Training Phase"
        A[Judgment Data] --> B[Feature Logging]
        B --> C[Training Data]
        C --> D[ML Training]
        D --> E[Trained Model]
    end
    
    subgraph "OpenSearch LTR Plugin"
        F[Feature Set] --> G[Model Store]
        E --> G
        H[Search Query] --> I[Feature Extraction]
        F --> I
        I --> J[Model Scoring]
        G --> J
        J --> K[Rescored Results]
    end
```

### Data Flow

```mermaid
flowchart TB
    subgraph "Model Upload"
        A[Model File] --> B{Parser}
        B -->|RankLib| C[RanklibModelParser]
        B -->|XGBoost JSON| D[XGBoostJsonParser]
        B -->|XGBoost Raw| E[XGBoostRawJsonParser]
        B -->|Linear| F[LinearRankerParser]
        C --> G[NaiveAdditiveDecisionTree]
        D --> G
        E --> G
        F --> H[LinearRanker]
    end
```

### Components

| Component | Description |
|-----------|-------------|
| Feature Set | Collection of features defined as OpenSearch queries |
| Feature Store | Storage for feature sets and models (`.ltrstore` index) |
| Model Parsers | Parsers for different model formats (RankLib, XGBoost, Linear) |
| SLTR Query | Special query type for applying LTR models at search time |
| Feature Logging | Mechanism to log feature scores for training data |

### Supported Model Types

| Type | Format | Description |
|------|--------|-------------|
| `model/ranklib` | RankLib XML | LambdaMART, RankNet, and other RankLib models |
| `model/xgboost+json` | XGBoost `get_dump` | XGBoost models in dump format (visualization) |
| `model/xgboost+json+raw` | XGBoost `save_model` | XGBoost models in proper serialization format |
| `model/linear` | JSON weights | Simple linear models (SVM, linear regression) |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `ltr.plugin.enabled` | Enable/disable the LTR plugin | `true` |
| `ltr.breaker.enabled` | Enable/disable the circuit breaker | `true` |

### Circuit Breaker

The LTR plugin includes a memory-based circuit breaker that protects the cluster from resource exhaustion:

- Monitors JVM heap usage with a default threshold of 85%
- Blocks feature set additions, model creation, and feature store updates when memory is constrained
- Can be disabled via `ltr.breaker.enabled` setting

### Stats API

The plugin exposes statistics for monitoring via REST endpoints:

```
GET /_plugins/_ltr/stats
GET /_plugins/_ltr/stats/{stat}
GET /_plugins/_ltr/{nodeId}/stats
GET /_plugins/_ltr/{nodeId}/stats/{stat}
```

Available statistics:
- `plugin_status` - Plugin health status (cluster-level)
- `cache_stats` - Cache performance metrics (node-level)
- `stores` - Feature store information (cluster-level)
- `request_total_count` - Total request count (node-level)
- `request_error_count` - Error request count (node-level)

### Security Roles

Predefined roles for LTR access control (requires Security plugin):

| Role | Permissions |
|------|-------------|
| `ltr_read_access` | Read-only access to LTR stats, cache stats, and feature store listing |
| `ltr_full_access` | Full access to all LTR operations |

### Usage Example

#### Define a Feature Set

```json
PUT _ltr/_featureset/my_features
{
    "featureset": {
        "name": "my_features",
        "features": [
            {
                "name": "title_match",
                "params": ["keywords"],
                "template": {
                    "match": { "title": "{{keywords}}" }
                }
            },
            {
                "name": "description_match",
                "params": ["keywords"],
                "template": {
                    "match": { "description": "{{keywords}}" }
                }
            }
        ]
    }
}
```

#### Upload a Model

```json
POST _ltr/_featureset/my_features/_createmodel
{
    "model": {
        "name": "my_model",
        "model": {
            "type": "model/xgboost+json+raw",
            "definition": "{...xgboost model json...}"
        }
    }
}
```

#### Search with LTR

```json
POST my_index/_search
{
    "query": {
        "sltr": {
            "params": {
                "keywords": "search terms"
            },
            "model": "my_model"
        }
    }
}
```

## Limitations

- Only `float` feature types are supported for XGBoost raw models
- Feature names in models must match feature set definitions
- Models are copied at creation time; changes to feature sets don't affect existing models

## Change History

- **v3.4.0** (2026-02-18): Bug fixes - legacy version ID computation update for OpenSearch compatibility, integration test stability improvements (ML index warning fix, implicit refresh), rescore-only SLTR logging fix; Test infrastructure enhancements - narrowed index cleanup scope to LTR indexes only, improved test isolation for parallel execution
- **v2.19.0** (2025-02-18): Major enhancements - plugin settings for enable/disable control (`ltr.plugin.enabled`, `ltr.breaker.enabled`), memory-based circuit breaker (85% heap threshold), stats REST API (`/_plugins/_ltr/stats`), security roles (`ltr_read_access`, `ltr_full_access`), system index registration for `.ltrstore*`; System index handling - REST handlers now stash thread context before accessing `.ltrstore*` system indices (RestAddFeatureToSet, RestCreateModelFromSet, RestFeatureManager, RestStoreManager); Integration test fixes for system index warnings; Build infrastructure improvements (Java 11/17 builds, LTR onboarding scripts)
- **v3.3.0** (2026-01-14): Build infrastructure fixes - log4j exclusion from JAR, Gradle 9 compatibility, hybrid float comparison for tests, code coverage reporting, spotless plugin upgrade
- **v3.2.0** (2025-09-16): Added XGBoost missing values support for correct NaN handling; Build infrastructure upgrade (Gradle 8.14, JDK 24 support); fixed flaky test with ULP tolerance adjustment
- **v3.0.0** (2025-05-13): Added XGBoost raw JSON parser for proper `save_model` format support; fixed ApproximateScoreQuery test


## References

### Documentation
- [Learning to Rank Documentation](https://docs.opensearch.org/3.0/search-plugins/ltr/index/)
- [ML Ranking Core Concepts](https://docs.opensearch.org/3.0/search-plugins/ltr/core-concepts/)
- [Working with Features](https://docs.opensearch.org/3.0/search-plugins/ltr/working-with-features/)
- [Uploading Trained Models](https://docs.opensearch.org/3.0/search-plugins/ltr/training-models/)
- [Searching with LTR](https://docs.opensearch.org/3.0/search-plugins/ltr/searching-with-your-model/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [RankLib Documentation](https://sourceforge.net/p/lemur/wiki/RankLib/)
- [GitHub Repository](https://github.com/opensearch-project/opensearch-learning-to-rank-base)

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.4.0 | [#264](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/264) | Use OpenSearch Version.computeID for legacy version IDs |   |
| v3.4.0 | [#269](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/269) | Fix ML index warning in YAML test parsing | [#265](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/265) |
| v3.4.0 | [#271](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/271) | Use implicit wait_for instead of explicit refresh |   |
| v3.4.0 | [#266](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/266) | Fix rescore-only feature SLTR logging |   |
| v3.4.0 | [#256](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/256) | Allow warnings about directly accessing the .plugins-ml-config index | [#249](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/249) |
| v3.4.0 | [#259](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/259) | Test isolation improvements - narrow index cleanup scope | [#245](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/245) |
| v3.3.0 | [#226](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/226) | Fix bad inclusion of log4j in plugin JAR |   |
| v3.3.0 | [#219](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/219) | Update System.env syntax for Gradle 9 compatibility |   |
| v3.3.0 | [#228](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/228) | Add code coverage report generation | [#227](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/227) |
| v3.3.0 | [#221](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/221) | Hybrid method for float comparison in assertions |   |
| v3.3.0 | [#222](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/222) | Upgrade spotless plugin and address build deprecations |   |
| v3.2.0 | [#206](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/206) | Add support to handle missing values for XGBoost models | [#200](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/200) |
| v3.2.0 | [#202](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/202) | Bump gradle to 8.14, codecov to v5 and support JDK24 | [#196](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/196) |
| v3.2.0 | [#205](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/205) | Fix flaky test with ULP tolerance adjustment |   |
| v3.0.0 | [#151](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/151) | Add XGBoost model parser for correct serialization format | [#497](https://github.com/o19s/elasticsearch-learning-to-rank/issues/497) |
| v3.0.0 | [#158](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/158) | Fix test for ApproximateScoreQuery |   |
| v2.19.0 | [#76](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/76) | Implemented LTR Settings for plugin enable/disable | [#75](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/75) |
| v2.19.0 | [#71](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/71) | Implemented circuit breaker | [#70](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/70) |
| v2.19.0 | [#79](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/79) | Collect stats for usage and health | [#78](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/78) |
| v2.19.0 | [#89](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/89) | Supplier plugin health and store usage refactoring | |
| v2.19.0 | [#90](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/90) | Implemented REST endpoint for stats | [#87](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/87) |
| v2.19.0 | [#125](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/125) | Add .ltrstore* as system index | |
| v2.19.0 | [#5067](https://github.com/opensearch-project/security/pull/5067) | Added roles for LTR read and full access (security) | |
| v2.19.0 | [#126](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/126) | Modified Rest Handlers to stash context before modifying system indices | [#120](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/120) |
| v2.19.0 | [#129](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/129) | Stashed context for GET calls |  |
| v2.19.0 | [#132](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/132) | Modify ITs to ignore transient warning |  |
| v2.19.0 | [#135](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/135) | Refactor index refresh logic in ITs |  |
| v2.19.0 | [#122](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/122) | Support integration tests against external cluster with security plugin | [#120](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/120) |
