---
tags:
  - opensearch
---
# Processor Allowlist

## Summary

OpenSearch v2.16.0 introduces allowlist settings for ingest-common and search-pipeline-common processors. This feature enables operators to selectively enable specific processors by name, providing fine-grained control over which processors are available in a cluster.

## Details

### What's New in v2.16.0

This release adds static settings that allow operators to control which processors are enabled:

**Ingest Processors:**
- Setting: `ingest.common.processors.allowed`

**Search Pipeline Processors:**
- Setting: `search.pipeline.common.request.processors.allowed`
- Setting: `search.pipeline.common.response.processors.allowed`
- Setting: `search.pipeline.common.search.phase.results.processors.allowed`

### Behavior

| Scenario | Behavior |
|----------|----------|
| Setting not defined | All installed processors are enabled (default) |
| Empty list `[]` | All processors are disabled |
| List of processor names | Only specified processors are enabled |
| Unknown processor in list | Server fails to start with `IllegalArgumentException` |

### Configuration Example

```yaml
# opensearch.yml

# Enable only specific ingest processors
ingest.common.processors.allowed:
  - date
  - set
  - grok

# Enable only specific search pipeline request processors
search.pipeline.common.request.processors.allowed:
  - filter_query
  - script

# Enable only specific search pipeline response processors
search.pipeline.common.response.processors.allowed:
  - rename_field
  - truncate_hits
```

### Technical Changes

The implementation adds filtering logic to the processor registration in both modules:

1. **IngestCommonModulePlugin**: Added `PROCESSORS_ALLOWLIST_SETTING` and `filterForAllowlistSetting()` method
2. **SearchPipelineCommonModulePlugin**: Added three separate allowlist settings for request, response, and search phase results processors

### Use Case

This feature is particularly useful for:
- Dedicated coordinator nodes where CPU-bound work needs to be strictly controlled
- Security-conscious deployments that want to limit available functionality
- Environments where only specific pipeline processors are needed

## Limitations

- Settings are static (node-level) and require a node restart to take effect
- If the allowlist is changed between restarts, any pipeline using a now-disabled processor will fail
- The behavior is similar to uninstalling a plugin that provided a processor

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14479](https://github.com/opensearch-project/OpenSearch/pull/14479) | Add allowlist setting for ingest-common processors | [#14439](https://github.com/opensearch-project/OpenSearch/issues/14439) |
| [#14562](https://github.com/opensearch-project/OpenSearch/pull/14562) | Add allowlist setting for search-pipeline-common processors | [#14439](https://github.com/opensearch-project/OpenSearch/issues/14439) |

### Documentation

- [Ingest Processors](https://docs.opensearch.org/2.16/ingest-pipelines/processors/index-processors/)
- [Search Processors](https://docs.opensearch.org/2.16/search-plugins/search-pipelines/search-processors/)
