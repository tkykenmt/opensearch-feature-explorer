---
tags:
  - domain/core
  - component/server
  - indexing
  - neural-search
  - search
---
# System Ingest Processor

## Summary

This enhancement adds the ability to pass index settings to system ingest processor factories, enabling plugins to make decisions about processor creation based on index-level configuration. Previously, system ingest processors could only access index mappings; now they can also access index settings from both the index itself and matched templates.

## Details

### What's New in v3.2.0

Added two new configuration keys for system ingest processor factories:
- `INDEX_SETTINGS`: Access settings from an existing index
- `INDEX_TEMPLATE_SETTINGS`: Access settings from matched index templates (v1 and v2)

This enables plugins like Neural Search to configure system ingest processor behavior through index settings rather than relying solely on index mappings.

### Technical Changes

#### New Configuration Keys

| Key | Type | Description |
|-----|------|-------------|
| `INDEX_SETTINGS` | `Settings` | Settings from the existing index |
| `INDEX_TEMPLATE_SETTINGS` | `List<Settings>` | Settings from matched templates (later templates can override earlier ones) |

#### API Changes

The `SystemIngestPipelineConfigKeys` class now includes:

```java
public class SystemIngestPipelineConfigKeys {
    // Existing keys
    public static final String INDEX_MAPPINGS = "index_mappings";
    public static final String INDEX_TEMPLATE_MAPPINGS = "index_template_mappings";
    
    // New in v3.2.0
    public static final String INDEX_SETTINGS = "index_settings";
    public static final String INDEX_TEMPLATE_SETTINGS = "index_template_settings";
}
```

#### IngestService Changes

The `IngestService` now passes settings to processor factories in three scenarios:

1. **Existing Index**: Settings from `IndexMetadata.getSettings()`
2. **V1 Templates**: Settings collected from all matched `IndexTemplateMetadata`
3. **V2 Templates**: Settings resolved via `MetadataIndexTemplateService.resolveSettings()`

### Usage Example

#### Defining a Custom Index Setting

```java
public class ExampleSystemIngestProcessorPlugin extends Plugin implements IngestPlugin {
    
    public static final Setting<Boolean> TRIGGER_SETTING = Setting.boolSetting(
        "index.example_system_ingest_processor_plugin.trigger_setting",
        false,
        Setting.Property.IndexScope,
        Setting.Property.Dynamic
    );
    
    @Override
    public List<Setting<?>> getSettings() {
        return List.of(TRIGGER_SETTING);
    }
    
    @Override
    public Map<String, Processor.Factory> getSystemIngestProcessors(Processor.Parameters parameters) {
        return Map.of(ExampleSystemIngestProcessorFactory.TYPE, new ExampleSystemIngestProcessorFactory());
    }
}
```

#### Using Settings in Factory

```java
public class ExampleSystemIngestProcessorFactory extends AbstractBatchingSystemProcessor.Factory {
    
    @Override
    protected AbstractBatchingSystemProcessor newProcessor(String tag, String description, Map<String, Object> config) {
        final List<Settings> settings = new ArrayList<>();
        
        // Get settings from index
        final Object settingsFromIndex = config.get(INDEX_SETTINGS);
        if (settingsFromIndex instanceof Settings) {
            settings.add((Settings) settingsFromIndex);
        }
        
        // Get settings from templates
        final Object settingsFromTemplates = config.get(INDEX_TEMPLATE_SETTINGS);
        if (settingsFromTemplates instanceof List) {
            settings.addAll((Collection<? extends Settings>) settingsFromTemplates);
        }
        
        // Check trigger setting (later settings override earlier ones)
        boolean isTriggerEnabled = false;
        for (final Settings setting : settings) {
            if (setting.hasValue(TRIGGER_SETTING.getKey())) {
                isTriggerEnabled = TRIGGER_SETTING.get(setting);
            }
        }
        
        return isTriggerEnabled ? new ExampleSystemIngestProcessor(tag, description, DEFAULT_BATCH_SIZE) : null;
    }
}
```

#### Creating Index with Trigger Setting

```json
PUT /my-index
{
  "settings": {
    "index.example_system_ingest_processor_plugin.trigger_setting": true
  }
}
```

#### Using Index Template

```json
PUT _index_template/example-template
{
  "index_patterns": ["example-*"],
  "template": {
    "settings": {
      "index.example_system_ingest_processor_plugin.trigger_setting": true
    }
  }
}
```

### Migration Notes

- Existing system ingest processors continue to work without changes
- To use index settings, update your processor factory to read from `INDEX_SETTINGS` or `INDEX_TEMPLATE_SETTINGS`
- For v1 templates with multiple matches, settings are provided as a list in order of precedence

## Limitations

- Settings from templates are provided as a list; the factory must handle precedence logic
- Dynamic setting changes require index mapping update to trigger cache invalidation

## References

### Documentation
- [Ingest Pipelines Documentation](https://docs.opensearch.org/3.2/ingest-pipelines/): Official documentation

### Blog Posts
- [Blog: Making ingestion smarter](https://opensearch.org/blog/making-ingestion-smarter-system-ingest-pipelines-in-opensearch/): System ingest pipeline overview

### Pull Requests
| PR | Description |
|----|-------------|
| [#18708](https://github.com/opensearch-project/OpenSearch/pull/18708) | Pass index settings to system ingest processor factories |

### Issues (Design / RFC)
- [Issue #1349](https://github.com/opensearch-project/neural-search/issues/1349): Semantic Field Enhancement - Configure Batch Size for Embedding Generation

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-system-ingest-pipeline.md)
