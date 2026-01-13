---
tags:
  - domain/ml
  - component/dashboards
  - dashboards
  - search
---
# Dashboards Flow Framework Bugfixes

## Summary

This release includes a fix for gracefully handling workflows with no provisioned resources in the Flow Framework Dashboards plugin.

## Details

### What's New in v3.4.0

#### Graceful Handling of Workflows Without Provisioned Resources

Previously, the workflow deletion UI did not properly handle workflows that had no provisioned resources. This fix introduces dynamic behavior:

- **Workflows with provisioned resources**: Shows the option to deprovision/delete associated resources along with the workflow
- **Workflows without provisioned resources**: Hides the deprovision option and skips the deprovision step entirely

This improvement is particularly useful for agentic search workflows, which by default do not have any provisioned resources.

### Technical Changes

| Fix | Description | Impact |
|-----|-------------|--------|
| No Provisioned Resources | Dynamic checkbox rendering based on resource state | Improved UX for agentic search workflows |

### Usage Example

When deleting a workflow:

1. **Agentic search workflow**: No checkbox shown, deletion proceeds directly
2. **Non-agentic workflow with resources**: Checkbox shown to optionally delete resources
3. **Non-agentic workflow without resources**: No checkbox shown, deletion proceeds directly

## Limitations

None identified.

## References

### Documentation
- [dashboards-flow-framework](https://github.com/opensearch-project/dashboards-flow-framework): Flow Framework Dashboards plugin repository

### Pull Requests
| PR | Description |
|----|-------------|
| [#821](https://github.com/opensearch-project/dashboards-flow-framework/pull/821) | Gracefully handle workflows with no provisioned resources |
