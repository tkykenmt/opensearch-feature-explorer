---
tags:
  - domain/ml
  - component/server
  - ml
  - security
---
# Skills Plugin Compatibility

## Summary

OpenSearch 3.0.0 includes compatibility updates for the Skills plugin to support upstream changes in ML Commons and the transition from Java SecurityManager to Java Agent. These changes ensure the Skills plugin tools work correctly with the new Plan-Execute-Reflect agent type and the modernized security model.

## Details

### What's New in v3.0.0

Two key compatibility updates were made to the Skills plugin:

1. **Tool Attributes Support**: Added `attributes` field to all tool classes to adapt to changes in ML Commons that introduced function calling interface for agents
2. **Java Agent Support**: Added support for running plugin tests under Java Agent instead of the deprecated SecurityManager

### Technical Changes

#### Tool Attributes Addition

The ML Commons [PR #3716](https://github.com/opensearch-project/ml-commons/pull/3716) introduced a new Plan-Execute-Reflect agent type with function calling interface. This required all tools to support an `attributes` field for enhanced tool metadata.

**Affected Tool Classes:**

| Tool Class | Change |
|------------|--------|
| `AbstractRetrieverTool` | Added `attributes` field |
| `CreateAlertTool` | Added `attributes` with getter/setter |
| `CreateAnomalyDetectorTool` | Added `attributes` field |
| `LogPatternTool` | Added `attributes` field |
| `PPLTool` | Added `attributes` field |
| `RAGTool` | Added `attributes` field |
| `SearchAlertsTool` | Added `attributes` with getter/setter |
| `SearchAnomalyDetectorsTool` | Added `attributes` with getter/setter |
| `SearchAnomalyResultsTool` | Added `attributes` with getter/setter |
| `SearchMonitorsTool` | Added `attributes` with getter/setter |
| `WebSearchTool` | Added `attributes` field |

**Code Change Example:**
```java
// Added to tool classes
@Getter
@Setter
private Map<String, Object> attributes;
```

#### Java Agent Plugin Support

Java's SecurityManager is deprecated and being phased out. OpenSearch 3.0.0 introduces Java Agent as the replacement security mechanism. The Skills plugin was updated to support running tests under Java Agent.

**Build Configuration Change:**
```gradle
apply plugin: 'opensearch.java-agent'
```

This allows the plugin tests to execute under the new Java Agent security model, ensuring compatibility with OpenSearch 3.0.0's modernized security infrastructure.

### Migration Notes

- **No user action required**: These are internal compatibility changes
- Tools continue to work as before with existing agent configurations
- The `attributes` field is optional and used internally by the agent framework

## Limitations

- These changes are purely for compatibility; no new user-facing features are added
- The `attributes` field usage is determined by the ML Commons agent framework

## References

### Documentation
- [Tools Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/tools/index/): Official tools documentation
- [Plan-Execute-Reflect Agent](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/): Agent documentation
- [ML Commons PR #3716](https://github.com/opensearch-project/ml-commons/pull/3716): Plan, Execute and Reflect Agent Type (upstream change)

### Pull Requests
| PR | Description |
|----|-------------|
| [#549](https://github.com/opensearch-project/skills/pull/549) | Add attributes to tools to adapt the upstream changes |
| [#553](https://github.com/opensearch-project/skills/pull/553) | Support phasing off SecurityManager usage in favor of Java Agent |

## Related Feature Report

- Full feature documentation
