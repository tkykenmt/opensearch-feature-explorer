---
tags:
  - search-relevance
---
# Search Evaluation (Experiments)

## Summary

OpenSearch v3.6.0 brings significant improvements to the Search Relevance Workbench's experiment evaluation capabilities. This release adds three new search quality metrics (Recall@K, MRR, DCG@K), introduces dynamic percentile-based relevance thresholding for binary metrics, adds optional name and description fields to experiments, fixes thread pool starvation in LLM judgment processing, and improves demo script usability.

## Details

### What's New in v3.6.0

#### New Search Quality Metrics

Three new metrics extend the evaluation framework beyond the existing Precision@K, MAP@K, and NDCG@K:

| Metric | Description | Relevance Type |
|--------|-------------|----------------|
| Recall@K | Proportion of relevant documents retrieved in top K results | Binary (uses threshold) |
| MRR (Mean Reciprocal Rank) | Reciprocal of the rank of the first relevant document | Binary (uses threshold) |
| DCG@K (Discounted Cumulative Gain) | Sum of graded relevance scores discounted by log position | Graded |

The full set of metrics now calculated per experiment:

| Metric | Formula Basis |
|--------|---------------|
| Coverage@K | Proportion of returned docs with judgment scores |
| Precision@K | Relevant docs in top K / K |
| Recall@K | Relevant docs in top K / total relevant docs |
| MAP@K | Mean of precision at each relevant rank position |
| MRR | 1 / rank of first relevant document |
| DCG@K | Σ (2^rel - 1) / log₂(i + 1) |
| NDCG@K | DCG@K / IDCG@K |

NDCG was refactored to depend directly on DCG internally, ensuring consistency between the two metrics.

#### Dynamic Relevance Thresholding

Binary-dependent metrics (Precision, MAP, Recall, MRR) now use a data-driven threshold instead of the previous hard-coded `j > 0` mapping:

```
T = max(0.5 × Jmax, P90)
```

Where:
- `Jmax` = maximum judgment value in the judgment list
- `P90` = 90th percentile of judgment values (nearest-rank method)
- A document is relevant when `j ≥ T` and `j > 0`

This prevents inflated binary metrics when using graded judgment scales (e.g., 1–5). For example, with a 1–5 graded dataset, Precision@5 drops from an artificially inflated 1.0 to a more accurate 0.2.

Edge cases handled:
- Empty input → threshold 0.0 (falls back to `> 0` behavior)
- All-zero ratings → threshold 0.0
- Constant non-zero value → P90 == Jmax, so T = Jmax (all docs remain relevant)

#### Experiment Name and Description

Experiments now support optional `name` (max 50 chars) and `description` (max 250 chars) fields:

- Auto-generated default names in format `{ExperimentType}-{shortId}` (e.g., `PAIRWISE_COMPARISON-a1b2c3d4`)
- New `PATCH /_plugins/_search_relevance/experiments/{id}` endpoint for updating metadata after creation
- Schema version bumped from 0 to 1 with new index mappings
- Validation: no quotes, backslashes, or HTML tags

#### Thread Pool Starvation Fix

Fixed a deadlock in `LlmJudgmentTaskManager` where all N queries were submitted simultaneously to the GENERIC thread pool. Each task blocked on `Semaphore.acquire()` while nested operations (search callbacks, cache lookups, ML predict calls) also required GENERIC pool threads, causing complete starvation with large query sets (~10K queries).

The fix introduces `BatchedAsyncExecutor`, a reusable abstraction that processes work items in sequential batches:
- At most `batchSize` tasks run concurrently per batch
- Next batch starts only after current batch completes
- Applied to both `LlmJudgmentTaskManager` and `ExperimentTaskManager` (hybrid optimizer)

#### Demo Script Improvements

Demo scripts (`demo.sh`, `demo_hybrid_optimizer.sh`) can now be run from any directory and point to any OpenSearch server, not just localhost.

### Technical Changes

Key classes modified:

| Class | Change |
|-------|--------|
| `Evaluation` | Added `calculateRecallAtK()`, `calculateReciprocalRank()`, `calculateDCGAtK()`; refactored NDCG to use internal `rawDCGAtK()` |
| `JudgmentThresholdCalculator` | New class implementing `T = max(0.5 * Jmax, P90)` threshold computation |
| `EvaluationMetrics` | Integrated threshold computation and new metric calculations |
| `BatchedAsyncExecutor` | New reusable batched async execution utility |
| `LlmJudgmentTaskManager` | Migrated to `BatchedAsyncExecutor` |
| `ExperimentTaskManager` | Migrated to `BatchedAsyncExecutor` |
| `Experiment` | Added `name` and `description` fields |
| `RestPatchExperimentAction` | New REST handler for PATCH endpoint |
| `TextValidationUtil` | Added name/description validation (50/250 char limits) |

## Limitations

- Position-sensitive metrics (DCG, MRR) may vary slightly in multi-node clusters due to per-shard BM25 IDF differences
- The dynamic threshold formula is fixed (`max(0.5 * Jmax, P90)`) and not user-configurable
- Experiment name and description cannot contain quotes, backslashes, or HTML tags

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#397](https://github.com/opensearch-project/search-relevance/pull/397) | Added Recall@K, MRR, and DCG@K metrics | [#388](https://github.com/opensearch-project/search-relevance/issues/388) |
| [#394](https://github.com/opensearch-project/search-relevance/pull/394) | Dynamic percentile-based relevance thresholding for binary metrics |   |
| [#408](https://github.com/opensearch-project/search-relevance/pull/408) | Optional name and description fields for experiments |   |
| [#387](https://github.com/opensearch-project/search-relevance/pull/387) | Fixed thread pool starvation in LLM judgment processing | [#386](https://github.com/opensearch-project/search-relevance/issues/386) |
| [#392](https://github.com/opensearch-project/search-relevance/pull/392) | Extract reusable BatchedAsyncExecutor; migrate task managers | [#386](https://github.com/opensearch-project/search-relevance/issues/386) |
| [#427](https://github.com/opensearch-project/search-relevance/pull/427) | Fix flaky DCG and MRR assertions in integration tests |   |
| [#415](https://github.com/opensearch-project/search-relevance/pull/415) | Improve demo scripts usability |   |
