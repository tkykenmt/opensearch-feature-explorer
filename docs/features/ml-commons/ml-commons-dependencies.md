# ML Commons Dependencies

## Summary

ML Commons plugin manages various third-party dependencies to provide machine learning capabilities within OpenSearch. Keeping these dependencies aligned with OpenSearch core is essential to prevent runtime conflicts and ensure compatibility.

## Details

### Key Dependencies

| Dependency | Purpose |
|------------|---------|
| Gson | JSON serialization/deserialization |
| Guava | Core utilities |
| Apache Commons | Text processing, math operations |
| DJL (Deep Java Library) | ML model inference |

### Dependency Management Strategy

ML Commons uses Gradle's dependency management features to ensure version alignment:

1. **compileOnly**: Dependencies provided by OpenSearch core at runtime
2. **implementation**: Dependencies bundled with the plugin
3. **resolutionStrategy.force**: Ensures consistent versions across transitive dependencies

### Configuration Example

```groovy
configurations.all {
    resolutionStrategy.force 'com.google.code.gson:gson:2.13.2'
    resolutionStrategy.force "com.google.errorprone:error_prone_annotations:${versions.error_prone_annotations}"
}
```

## Limitations

- Dependency versions must be kept in sync with OpenSearch core to avoid conflicts
- Major version upgrades may require code changes

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.3.0 | [#4176](https://github.com/opensearch-project/ml-commons/pull/4176) | Update Gson from 2.11.0 to 2.13.2 |

## References

- [ML Commons Repository](https://github.com/opensearch-project/ml-commons)
- [OpenSearch Dependency Management](https://github.com/opensearch-project/OpenSearch/blob/main/buildSrc/version.properties)

## Change History

- **v3.3.0**: Updated Gson from 2.11.0 to 2.13.2 to resolve conflict with OpenSearch core
