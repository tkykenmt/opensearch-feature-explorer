---
tags:
  - ml-commons
---
# ML Commons Model Management

## Summary

Model management improvements in v3.3.2 include a new refresh policy option and checkpoint ID field, plus index prefix name validation.

## Details

### What's New in v3.3.2

- **Refresh Policy & Checkpoint ID** (ml-commons#4305): Added refresh policy support and a checkpoint ID field to model management operations, giving users more control over index refresh behavior and model checkpoint tracking.

- **Index Prefix Validation** (ml-commons#4332): Added name validation to index prefix to prevent invalid or potentially harmful index names from being used.

## References

| PR | Description |
|----|-------------|
| [#4305](https://github.com/opensearch-project/ml-commons/pull/4305) | Add refresh policy; add checkpoint id field |
| [#4332](https://github.com/opensearch-project/ml-commons/pull/4332) | Add name validation to index prefix |
