# PlanExecuteReflect Agent Test Coverage

## Summary

This release item adds comprehensive unit test and integration test coverage for the PlanExecuteReflect Agent in ML Commons. The PlanExecuteReflect Agent was released as an experimental feature in OpenSearch 3.0-beta but lacked adequate test coverage. This bugfix addresses that gap by adding test cases for the agent runner and related utility methods.

## Details

### What's New in v3.1.0

This PR improves code quality by adding test coverage for the `MLPlanExecuteAndReflectAgentRunner` class and related agent utilities. The changes ensure the experimental PlanExecuteReflect Agent feature has proper test validation.

### Technical Changes

#### Modified Components

| Component | Description |
|-----------|-------------|
| `MLPlanExecuteAndReflectAgentRunner` | Changed method visibility from `private` to package-private with `@VisibleForTesting` annotation to enable unit testing |
| `AgentUtilsTest` | Added 243 lines of new test cases for agent utility methods |
| `MLPlanExecuteAndReflectAgentRunnerTest` | New test class with 547 lines covering agent runner functionality |
| `ConnectorUtilsTest` | Added 49 lines of tests for remote inference input data escaping |
| `RegisterAgentTransportActionTests` | Added 88 lines of tests for agent registration with/without executor agent ID |

#### New Test Coverage

The following methods now have test coverage:

- `setupPromptParameters()` - Tests prompt parameter initialization
- `usePlannerPromptTemplate()` - Tests planner prompt template usage
- `useReflectPromptTemplate()` - Tests reflection prompt template usage
- `usePlannerWithHistoryPromptTemplate()` - Tests planner with history template
- `populatePrompt()` - Tests prompt population with parameters
- `parseLLMOutput()` - Tests LLM output parsing including error cases
- `extractJsonFromMarkdown()` - Tests JSON extraction from markdown code blocks
- `addToolsToPrompt()` - Tests tool description injection into prompts
- `addSteps()` - Tests step list formatting
- `saveAndReturnFinalResult()` - Tests final result persistence and response
- `createModelTensors()` - Tests model tensor creation

#### Visibility Changes

Methods in `MLPlanExecuteAndReflectAgentRunner` were changed from `private` to package-private with `@VisibleForTesting` annotation:

```java
@VisibleForTesting
void setupPromptParameters(Map<String, String> params) { ... }

@VisibleForTesting
void usePlannerPromptTemplate(Map<String, String> params) { ... }

@VisibleForTesting
Map<String, String> parseLLMOutput(Map<String, String> allParams, ModelTensorOutput modelTensorOutput) { ... }
```

### Usage Example

The test cases validate agent execution scenarios:

```java
@Test
public void testBasicExecution() {
    MLAgent mlAgent = createMLAgentWithTools();
    
    // Setup LLM response for planning phase
    doAnswer(invocation -> {
        ActionListener<Object> listener = invocation.getArgument(2);
        ModelTensor modelTensor = ModelTensor.builder()
            .dataAsMap(ImmutableMap.of("response", 
                "{\"steps\":[\"step1\"], \"result\":\"final result\"}"))
            .build();
        // ... mock setup
        listener.onResponse(mlTaskResponse);
        return null;
    }).when(client).execute(eq(MLPredictionTaskAction.INSTANCE), any(), any());
    
    mlPlanExecuteAndReflectAgentRunner.run(mlAgent, params, agentActionListener);
    
    verify(agentActionListener).onResponse(objectCaptor.capture());
    // Assertions...
}
```

## Limitations

- This is a code quality improvement only; no functional changes to the PlanExecuteReflect Agent
- The PlanExecuteReflect Agent remains an experimental feature

## References

### Documentation
- [Plan-execute-reflect agents documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/)
- [PR #3716](https://github.com/opensearch-project/ml-commons/pull/3716): Related PlanExecuteReflect Agent implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#3778](https://github.com/opensearch-project/ml-commons/pull/3778) | Adding test cases for PlanExecuteReflect Agent |

### Issues (Design / RFC)
- [Issue #3750](https://github.com/opensearch-project/ml-commons/issues/3750): Original feature request for test coverage

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/planexecutereflect-agent.md)
