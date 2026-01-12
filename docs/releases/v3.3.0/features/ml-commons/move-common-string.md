# Move Common String

## Summary

This bugfix moves the `NO_ESCAPE_PARAMS` constant from `AgentUtils.java` in the ml-algorithms module to `ToolUtils.java` in the common package. This refactoring enables the skills plugin to access this constant, improving code reusability across ML Commons components.

## Details

### What's New in v3.3.0

The `NO_ESCAPE_PARAMS` constant has been relocated to make it accessible from the common package, allowing other plugins (specifically the skills plugin) to use this shared string constant.

### Technical Changes

#### Code Relocation

| Before | After |
|--------|-------|
| `ml-algorithms/.../agent/AgentUtils.java` | `common/.../utils/ToolUtils.java` |

#### Changed Files

| File | Change |
|------|--------|
| `common/src/main/java/org/opensearch/ml/common/utils/ToolUtils.java` | Added `NO_ESCAPE_PARAMS` constant |
| `ml-algorithms/src/main/java/org/opensearch/ml/engine/algorithms/agent/AgentUtils.java` | Removed `NO_ESCAPE_PARAMS` constant |
| `ml-algorithms/src/main/java/org/opensearch/ml/engine/algorithms/remote/ConnectorUtils.java` | Updated import |
| `ml-algorithms/src/main/java/org/opensearch/ml/engine/function_calling/BedrockConverseDeepseekR1FunctionCalling.java` | Updated import |
| `ml-algorithms/src/main/java/org/opensearch/ml/engine/function_calling/BedrockConverseFunctionCalling.java` | Updated import |
| `ml-algorithms/src/main/java/org/opensearch/ml/engine/function_calling/OpenaiV1ChatCompletionsFunctionCalling.java` | Updated import |

#### New Constant Location

```java
// common/src/main/java/org/opensearch/ml/common/utils/ToolUtils.java
public static final String NO_ESCAPE_PARAMS = "no_escape_params";
```

### Migration Notes

If you have custom code that imports `NO_ESCAPE_PARAMS` from `AgentUtils`, update the import:

```java
// Before
import static org.opensearch.ml.engine.algorithms.agent.AgentUtils.NO_ESCAPE_PARAMS;

// After
import static org.opensearch.ml.common.utils.ToolUtils.NO_ESCAPE_PARAMS;
```

## Limitations

None. This is a backward-compatible refactoring change.

## References

### Documentation
- [PR #4173](https://github.com/opensearch-project/ml-commons/pull/4173): Implementation PR

### Pull Requests
| PR | Description |
|----|-------------|
| [#4173](https://github.com/opensearch-project/ml-commons/pull/4173) | Move common string |

## Related Feature Report

- [ML Commons Agent Framework](../../../features/ml-commons/ml-commons-agent-framework.md)
