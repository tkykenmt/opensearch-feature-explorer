# ML Commons Connector/Model Validation Bug Fixes

## Summary

OpenSearch v3.1.0 includes several important bug fixes for ML Commons connector and model validation. These fixes address issues with input validation for model groups and connectors, schema validation for string parameters, connector retry policy handling, MCP tool memory management, and Bedrock DeepSeek function calling format.

## Details

### What's New in v3.1.0

This release addresses five key validation and error handling issues in ML Commons:

1. **Input Validation for Name and Description Fields** - Added stricter validation to prevent script injection in model, model group, and connector name/description fields
2. **Schema String Type Preservation** - Fixed validation that incorrectly converted schema-defined strings to numbers
3. **Connector Retry Policy NPE Fix** - Graceful error handling when updating retry policy for models without inline connectors
4. **MCP Tool Memory Management** - Fixed tool registration/removal synchronization in MCP server memory
5. **Bedrock DeepSeek Tool Result Format** - Corrected JSON format for function calling results

### Technical Changes

#### Input Validation Enhancement

A new validation framework was added to prevent potentially malicious input in model and connector APIs:

| Component | Validation Added |
|-----------|------------------|
| `MLCreateConnectorRequest` | Name (required), Description (optional) |
| `MLUpdateConnectorRequest` | Name (optional), Description (optional) |
| `MLUpdateModelRequest` | Name (optional), Description (optional) |
| `MLRegisterModelGroupRequest` | Name (required), Description (optional) |
| `MLUpdateModelGroupRequest` | Name (optional), Description (optional) |
| `MLRegisterModelRequest` | Name (required), Description (optional) |

New utility classes:
- `FieldDescriptor` - Describes field validation requirements (value, required flag)
- `StringUtils.validateFields()` - Validates fields against safe character pattern

Allowed characters: letters, numbers, whitespace, and basic punctuation (.,!?():@-_'")

#### Schema Validation Fix

The `processRemoteInferenceInputDataSetParametersValue()` method was updated to check the schema before converting string values:

```java
// Before: Converted all parseable strings to JSON
JsonNode parsedValue = mapper.readTree(textValue);

// After: Only convert if schema doesn't define field as string type
if (value.isTextual() && !isStringTypeInSchema(parametersSchema, key)) {
    JsonNode parsedValue = mapper.readTree(value.asText());
    parametersNode.set(key, parsedValue);
}
```

This prevents strings like `"5.11"` from being incorrectly converted to numbers when the schema defines the field as a string type.

#### Connector Retry Policy NPE Fix

Added null check before updating connector settings:

```java
if (connector == null) {
    wrappedListener.onFailure(
        new OpenSearchStatusException(
            "Cannot update connector settings for this model. " +
            "The model was created with a connector_id and does not have an inline connector.",
            RestStatus.BAD_REQUEST
        )
    );
    return;
}
```

#### MCP Tool Memory Synchronization

Fixed the tool removal flow to properly clean up the in-memory tool map:

```java
// Before: Tool removed from MCP server but not from memory map
.subscribe();

// After: Remove from memory map on successful removal
.doOnSuccess(x -> McpAsyncServerHolder.IN_MEMORY_MCP_TOOLS.remove(toolName))
.subscribe();
```

#### Bedrock DeepSeek Tool Result Format

Fixed the tool result format for Bedrock DeepSeek R1 function calling:

```java
// Before: Nested object structure
toolMessage.getContent().add(Map.of("text", Map.of(TOOL_CALL_ID, toolUseId, TOOL_RESULT, result)));

// After: JSON escaped string
String textJson = StringUtils.toJson(Map.of(TOOL_CALL_ID, toolUseId, TOOL_RESULT, result));
toolMessage.getContent().add(Map.of("text", textJson));
```

### Usage Example

#### Input Validation Error Response

When attempting to create a connector with invalid characters:

```json
PUT /_plugins/_ml/connectors/_create
{
  "name": "<script>alert(1)</script>",
  "description": "Test connector"
}
```

Response:
```json
{
  "error": {
    "type": "action_request_validation_exception",
    "reason": "Validation Failed: 1: Model connector name can only contain letters, numbers, whitespace, and basic punctuation (.,!?():@-_'\");"
  },
  "status": 400
}
```

#### Schema Validation with String Numbers

With proper schema definition, string values containing numbers are preserved:

```json
POST /_plugins/_ml/models/{model_id}/_predict
{
  "parameters": {
    "inputText": "5.11"
  }
}
```

With schema defining `inputText` as string type, the value `"5.11"` is correctly passed as a string rather than being converted to the number `5.11`.

## Limitations

- Input validation uses a fixed character set; special characters outside the allowed set will be rejected
- The schema validation fix requires the model interface to properly define string types for parameters that should remain as strings

## References

### Documentation
- [Update Model API Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/api/model-apis/update-model/)
- [Update Connector API Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/api/connector-apis/update-connector/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#3805](https://github.com/opensearch-project/ml-commons/pull/3805) | Add validation for name and description for model, model group, and connector resources |
| [#3761](https://github.com/opensearch-project/ml-commons/pull/3761) | Don't convert schema-defined strings to other types during validation |
| [#3909](https://github.com/opensearch-project/ml-commons/pull/3909) | Fixed NPE for connector retrying policy |
| [#3931](https://github.com/opensearch-project/ml-commons/pull/3931) | Fix tool not found in MCP memory issue |
| [#3933](https://github.com/opensearch-project/ml-commons/pull/3933) | Fix: Ensure proper format for Bedrock DeepSeek tool result |

### Issues (Design / RFC)
- [Issue #3639](https://github.com/opensearch-project/ml-commons/issues/3639): Enhance Input Validation for UpdateModel and UpdateModelGroup APIs
- [Issue #3758](https://github.com/opensearch-project/ml-commons/issues/3758): Model interface validation failed when there is integer within text
- [Issue #3906](https://github.com/opensearch-project/ml-commons/issues/3906): Gracefully handle error when user attempts to update retry_policy for a model that doesn't use inline connector

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/connector-model-validation.md)
