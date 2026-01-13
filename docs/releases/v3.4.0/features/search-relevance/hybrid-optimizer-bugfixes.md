---
tags:
  - domain/search
  - component/server
  - performance
  - search
---
# Hybrid Optimizer Bugfixes

## Summary

OpenSearch v3.4.0 includes two bug fixes for the Hybrid Optimizer experiment feature in the Search Relevance Workbench. These fixes address floating-point precision issues in weight generation and improve error handling when experiments reference deleted judgments.

## Details

### What's New in v3.4.0

Two critical bug fixes improve the reliability and accuracy of Hybrid Optimizer experiments:

1. **Floating-point precision fix**: Weight combinations now use clean decimal values (e.g., `0.4/0.6`) instead of imprecise floating-point values (e.g., `0.39999998/0.60000002`)
2. **Error handling fix**: Experiments now properly transition to ERROR state when referenced judgments are deleted, instead of hanging in PROCESSING state

### Technical Changes

#### Bug Fix 1: Floating-Point Precision in Weight Generation

**Problem**: When generating weight combinations for hybrid search experiments, cumulative floating-point addition caused precision drift. Weights like `0.39999998` or `0.60000002` appeared instead of clean values like `0.4` and `0.6`.

**Solution**: The fix in `ExperimentOptionsForHybridSearch.java` implements:
- Step-based iteration instead of floating-point accumulation
- Rounding both weight values to one decimal place
- Ensuring weight pairs cleanly sum to 1.0

```java
// Before (caused precision drift)
queryWeightsForCombination(new float[] { queryWeightForCombination, 1.0f - queryWeightForCombination })

// After (clean decimal values)
float w1 = Math.round(queryWeightForCombination * 10) / 10.0f;
float w2 = Math.round((1.0f - w1) * 10) / 10.0f;
queryWeightsForCombination(new float[] { w1, w2 })
```

#### Bug Fix 2: Experiment Status Handling for Deleted Judgments

**Problem**: When a judgment was deleted while an experiment was running, the experiment would hang indefinitely in `PROCESSING` state. The internal `hasFailure` flag was toggled prematurely inside the async block, preventing the caller's `handleFailure()` method from triggering.

**Solution**: The fix in `HybridOptimizerExperimentProcessor.java`:
- Removes the redundant `hasFailure` parameter passed by reference
- Creates a local `AtomicBoolean hasFailure` within the processor
- Allows exceptions to propagate correctly to the caller's failure handler
- Ensures experiments transition to ERROR state when judgment processing fails

```java
// Before: hasFailure passed by reference caused premature flag toggling
public void processHybridOptimizerExperiment(..., AtomicBoolean hasFailure, ...) {
    // Internal check blocked upstream recovery
}

// After: Local failure tracking with proper exception propagation
public void processHybridOptimizerExperiment(...) {
    AtomicBoolean hasFailure = new AtomicBoolean(false);
    // Exceptions propagate to caller's handleFailure()
}
```

### Impact

| Issue | Before Fix | After Fix |
|-------|------------|-----------|
| Weight precision | `0.39999998/0.60000002` | `0.4/0.6` |
| Deleted judgment | Stuck in PROCESSING | Transitions to ERROR |
| User experience | Confusing weight values | Clean, interpretable results |
| Error recovery | Manual intervention needed | Automatic error state |

## Limitations

- These fixes are specific to the Hybrid Optimizer experiment type
- The weight rounding is fixed at one decimal place (0.1 increments)

## References

### Blog Posts
- [Optimizing hybrid search in OpenSearch](https://opensearch.org/blog/hybrid-search-optimization/): Blog post on hybrid search optimization

### Pull Requests
| PR | Description |
|----|-------------|
| [#308](https://github.com/opensearch-project/search-relevance/pull/308) | Fix floating-point precision issues in hybrid optimizer weight generation |
| [#292](https://github.com/opensearch-project/search-relevance/pull/292) | Fix hybrid optimizer experiments stuck in PROCESSING after judgment deletion |

### Issues (Design / RFC)
- [Issue #298](https://github.com/opensearch-project/search-relevance/issues/298): Query weights not exact multiples of increment step
- [Issue #282](https://github.com/opensearch-project/search-relevance/issues/282): Hybrid Optimizer Result Stuck in Processing

## Related Feature Report

- Search Relevance Workbench
