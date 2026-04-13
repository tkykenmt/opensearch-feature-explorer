---
tags:
  - ml-commons
---
# ML Commons CI & Test Infrastructure

## Summary

OpenSearch v3.6.0 includes significant improvements to the ML Commons CI and test infrastructure, reducing integration test execution time by ~50%, fixing flaky tests, upgrading Bedrock Claude models for higher rate limits, and onboarding automated code review tooling.

## Key Changes

### Integration Test Setup Optimization (PR #4667)

Eliminated redundant per-test setup work across 16+ test files, cutting measured test execution time by approximately 50%.

**Transport IT tests (4 files)**: Adopted `@SuiteScopeTestCase` annotation so expensive operations (model registration, iris data loading, ML model training) run once per class instead of per method.

| Class | Change |
|-------|--------|
| `SearchModelGroupITTests` | `@Before` → `setupSuiteScopeCluster()` |
| `UpdateModelGroupITTests` | `@Before` → `setupSuiteScopeCluster()` |
| `PredictionITTests` | `@Before` → `setupSuiteScopeCluster()` |
| `TrainAndPredictITTests` | `@Before` → `setupSuiteScopeCluster()` |

**Memory IT tests (3 files)**: Changed `@ClusterScope(scope = TEST)` to `scope = SUITE`, eliminating per-test cluster restarts.

| Class | Change |
|-------|--------|
| `ConversationalMemoryHandlerITTests` | `scope = TEST` → `scope = SUITE` |
| `ConversationMetaIndexITTests` | `scope = TEST` → `scope = SUITE` |
| `InteractionsIndexITTests` | `scope = TEST` → `scope = SUITE` |

**REST IT tests (9 files)**: Replaced `Thread.sleep(20000)` with active polling via new `waitForClusterSettingPropagation()` utility that polls `GET _cluster/settings?flat_settings=true` until the setting appears (typically <1s, 10s timeout).

**Additional fixes**:
- Fixed deploy timeout from 20,000 seconds to 20 seconds (`TimeUnit.SECONDS` → `TimeUnit.MILLISECONDS`)
- Removed unnecessary deploy calls for remote models (deploy is only needed for local models)

### CI Test Stability Improvements (PR #4668)

**OpenAI RAG test skip**: All four OpenAI tests in `RestMLRAGSearchProcessorIT` now skip when `api.openai.com` is unreachable, using the existing `isServiceReachable()` helper. Previously, tests failed because `OPENAI_KEY` was set in CI but the endpoint was not reachable, causing `deployRemoteModel(null)` to hit `/_plugins/_ml/models/null/_deploy`.

**Flaky IndexUtilsTests fix**: Fixed `testGetNumberOfDocumentsInIndex_SearchQuery` which failed intermittently due to:
1. Documents indexed with `index()` + `flushAndRefresh()` not guaranteeing all shards were searchable with random shard counts. Fixed by using `indexRandom(true, builders)`.
2. Assertion running inside async `ActionListener` callback on a search thread. Fixed by using `PlainActionFuture` to make the call synchronous.

### Bedrock Claude Model Upgrades (PR #4742)

Upgraded integration test models from older Claude versions (claude-v2, claude-3-sonnet, claude-3-5-sonnet) with low rate limits (50–500 RPM) to newer models with 10,000 RPM cross-region quotas:

| Use Case | Old Model | New Model |
|----------|-----------|-----------|
| Vision/image tasks | `anthropic.claude-3-5-sonnet-20241022-v2:0` | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Text/summarization | `anthropic.claude-3-sonnet-20240229-v1:0` | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |

Additional changes:
- Switched to inference profile model IDs (`us.anthropic.` prefix) required by newer Bedrock models
- Removed `topP` from `inferenceConfig` (newer models disallow specifying both `temperature` and `topP`)
- Deleted unused claude-v2 connector blueprints (dead code)
- Simplified redundant ternary expressions

### Code Diff Analyzer & Reviewer (PR #4666)

Added `.github/workflows/pr_review.yml` workflow that runs on `pull_request_target` events, invoking:
- `Code-Diff-Analyzer`: Analyzes code diffs using Bedrock and posts analysis reports as PR comments
- `Code-Diff-Reviewer`: Reviews code diffs after analysis completes

Both jobs use OIDC to assume AWS roles for Bedrock access and can be skipped via `skip-diff-analyzer` / `skip-diff-reviewer` labels.

## References

### Pull Requests
| PR | Description |
|----|-------------|
| `https://github.com/opensearch-project/ml-commons/pull/4666` | Onboard code diff analyzer and reviewer |
| `https://github.com/opensearch-project/ml-commons/pull/4667` | Optimize IT setup, remove redundant per-test work |
| `https://github.com/opensearch-project/ml-commons/pull/4668` | Fix CI test stability - skip unreachable OpenAI tests and fix flaky IndexUtilsTests |
| `https://github.com/opensearch-project/ml-commons/pull/4742` | Upgrade Bedrock Claude models in ITs for higher rate limits |

### Related Issues
| Issue | Description |
|-------|-------------|
| `https://github.com/opensearch-project/opensearch-build/issues/5912` | Onboard code diff analyzer and reviewer |
