---
tags:
  - opensearch
---
# Ingest Pipeline Script Processor

## Summary

The Script Processor is an ingest pipeline processor that executes Painless scripts to modify or transform documents during ingestion. It supports inline and stored scripts with script caching for improved performance.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Script Processor Flow"
        A[Incoming Document] --> B[IngestDocument]
        B --> C[Script Processor]
        C --> D[Execute Painless Script]
        D --> E[Deep Copy Document]
        E --> F[Next Processor]
    end
```

### Configuration

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Optional* | Inline Painless script to execute |
| `id` | Optional* | ID of a stored script |
| `lang` | Optional | Script language (default: `painless`) |
| `params` | Optional | Parameters passed to the script |
| `description` | Optional | Description of the processor |
| `if` | Optional | Conditional execution |
| `ignore_failure` | Optional | Ignore processor failures |
| `on_failure` | Optional | Processors to run on failure |

*Either `source` or `id` must be specified, but not both.

### Supported Data Types

The script processor supports the following data types in document fields:

| Data Type | Support | Notes |
|-----------|---------|-------|
| `String` | ✅ Full | |
| `Integer` | ✅ Full | |
| `Long` | ✅ Full | |
| `Float` | ✅ Full | |
| `Double` | ✅ Full | |
| `Boolean` | ✅ Full | |
| `Short` | ✅ Full | Fixed in v2.16.0 |
| `Byte` | ✅ Full | Fixed in v2.16.0 |
| `Character` | ❌ Broken | See Limitations |
| `List` | ✅ Full | |
| `Map` | ✅ Full | |

### Usage Example

#### Basic Script Processor

```json
PUT _ingest/pipeline/my-script-pipeline
{
  "description": "Convert message to uppercase",
  "processors": [
    {
      "script": {
        "source": "ctx.message = ctx.message.toUpperCase()",
        "lang": "painless"
      }
    }
  ]
}
```

#### Using Parameters

```json
PUT _ingest/pipeline/parameterized-pipeline
{
  "processors": [
    {
      "script": {
        "source": "ctx.multiplied = ctx.value * params.factor",
        "params": {
          "factor": 2
        }
      }
    }
  ]
}
```

#### Using Numeric Types (Fixed in v2.16.0)

```json
PUT _ingest/pipeline/numeric-types-pipeline
{
  "processors": [
    {
      "script": {
        "source": "ctx.byte_field = (byte)127; ctx.short_field = (short)32767"
      }
    }
  ]
}
```

## Limitations

- `Character` data type is not supported in script processors and will cause failures
- Scripts are compiled per unique source, so dynamic scripts should use parameters instead of string concatenation
- The `lang` parameter only supports `painless`

## Change History

- **v2.16.0** (2024-08-06): Fixed handling of Short and Byte data types in ScriptProcessor deep copy
- **v2.8.0**: Added deep copy in ScriptProcessor flow (introduced regression for Short/Byte types)
- **v1.0.0**: Initial implementation

## References

### Documentation
- [Script Processor](https://docs.opensearch.org/latest/ingest-pipelines/processors/script/): Official documentation
- [Ingest Pipelines](https://docs.opensearch.org/latest/ingest-pipelines/): Ingest pipeline overview
- [Script APIs](https://docs.opensearch.org/latest/api-reference/script-apis/index/): Stored script management

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#14380](https://github.com/opensearch-project/OpenSearch/pull/14380) | Add missing data types to IngestDocument deep copy |
| v2.8.0 | [#11725](https://github.com/opensearch-project/OpenSearch/pull/11725) | Added deep copy in ScriptProcessor flow |
