# Flow Framework Bugfixes

## Summary

This release fixes a bug in the reprovision workflow where the template update was occurring at the wrong location in the execution flow, causing flaky integration tests. The fix also improves logger statements for better debugging and clarity.

## Details

### What's New in v2.18.0

Fixed the template update timing in `ReprovisionWorkflowTransportAction` to occur at the start of workflow execution rather than after completion. This resolves a race condition that caused the `testReprovisionWorkflow` integration test to fail intermittently across multiple platforms (Windows, Linux, macOS).

### Technical Changes

#### Bug Fix: Template Update Location

The original implementation updated the template document after all workflow steps completed successfully. This created a race condition where the workflow state could be checked before the template was fully updated.

**Before (v2.17.0):**
```java
// Template update happened AFTER workflow completion
private void executeWorkflow(...) {
    // Execute all workflow steps
    // ...
    // Then update template (race condition here)
    flowFrameworkIndicesHandler.updateTemplateInGlobalContext(...);
}
```

**After (v2.18.0):**
```java
// Template update now happens at START of execution
private void executeWorkflowAsync(...) {
    threadPool.executor(PROVISION_WORKFLOW_THREAD_POOL).execute(() -> {
        updateTemplate(template, workflowId);  // Update first
        executeWorkflow(template, workflowSequence, workflowId);
    });
}

private void updateTemplate(Template template, String workflowId) {
    flowFrameworkIndicesHandler.updateTemplateInGlobalContext(
        workflowId, 
        template, 
        ActionListener.wrap(
            templateResponse -> logger.info("Updated template for {}", workflowId),
            exception -> logger.error("Failed to update use case template for {}", workflowId, exception)
        ),
        true  // ignores NOT_STARTED state for reprovision
    );
}
```

#### Improved Logger Statements

Enhanced logging in the workflow execution to include the workflow step type for better debugging:

```java
// Before
logger.info("Queueing process [{}].{}", processNode.id(), ...);

// After  
logger.info("Queueing Process [{} (type: {})].{}", 
    processNode.id(), 
    processNode.workflowStep().getName(), 
    ...);
```

### Migration Notes

No migration required. This is a bug fix that improves reliability without changing the API or behavior.

## Limitations

- The fix addresses the specific race condition in reprovision workflows
- Template updates are now asynchronous at the start of execution

## References

### Documentation
- [Create or Update Workflow API](https://docs.opensearch.org/2.18/automating-configurations/api/create-workflow/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#918](https://github.com/opensearch-project/flow-framework/pull/918) | Fixed Template Update Location and Improved Logger Statements in ReprovisionWorkflowTransportAction |

### Issues (Design / RFC)
- [Issue #870](https://github.com/opensearch-project/flow-framework/issues/870): Reprovision Workflow IT is flaky

## Related Feature Report

- [Full feature documentation](../../../../features/flow-framework/flow-framework.md)
