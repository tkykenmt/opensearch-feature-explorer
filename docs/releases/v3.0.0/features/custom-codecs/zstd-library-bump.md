---
tags:
  - indexing
  - performance
---

# ZSTD Library Version Bump

## Summary

This release item updates the ZSTD (Zstandard) compression library in the custom-codecs plugin from version 1.5.5-5 to 1.5.6-1. This upgrade adds support for custom sequence producers, enabling future QAT-accelerated ZSTD compression alongside existing `qat_deflate` and `qat_lz4` codecs.

## Details

### What's New in v3.0.0

The custom-codecs plugin now uses zstd-jni version 1.5.6-1, which includes:

- Support for custom sequence producers
- Foundation for QAT-accelerated ZSTD compression
- Compatibility with OpenSearch 3.0.0-beta1

### Technical Changes

#### Dependency Update

| Dependency | Previous Version | New Version |
|------------|------------------|-------------|
| `com.github.luben:zstd-jni` | 1.5.5-5 | 1.5.6-1 |

#### Build Configuration Changes

The `build.gradle` file was updated:

```groovy
dependencies {
  api "com.github.luben:zstd-jni:1.5.6-1"
  api "com.intel.qat:qat-java:1.1.1"
}
```

#### Version Alignment

The plugin version was also aligned with OpenSearch 3.0.0-beta1:

| Setting | Previous | New |
|---------|----------|-----|
| `opensearch_version` | 3.0.0-alpha1-SNAPSHOT | 3.0.0-beta1-SNAPSHOT |
| `buildVersionQualifier` | alpha1 | beta1 |

### Custom Sequence Producers

The ZSTD 1.5.6 release introduces support for custom sequence producers, which is a key feature for hardware acceleration. This enables:

1. **QAT-accelerated ZSTD**: Future support for Intel QAT hardware acceleration for ZSTD compression
2. **Flexible compression pipelines**: Custom sequence producers allow external hardware or software to generate compression sequences
3. **Performance optimization**: Hardware offloading of compression workloads

### Usage Example

The ZSTD codecs can be used when creating an index:

```json
PUT /my-index
{
  "settings": {
    "index": {
      "codec": "zstd",
      "codec.compression_level": 3
    }
  }
}
```

Or with the no-dictionary variant:

```json
PUT /my-index
{
  "settings": {
    "index": {
      "codec": "zstd_no_dict"
    }
  }
}
```

## Limitations

- ZSTD codecs (`zstd` and `zstd_no_dict`) cannot be used for k-NN or Security Analytics indexes
- QAT-accelerated ZSTD is not yet available in this release (foundation only)
- Compression levels are limited to range [1, 6]

## References

### Documentation
- [Index Codecs Documentation](https://docs.opensearch.org/3.0/im-plugin/index-codecs/): Official OpenSearch documentation
- [ZSTD GitHub Repository](https://github.com/facebook/zstd): Zstandard compression algorithm
- [zstd-jni](https://github.com/luben/zstd-jni): JNI bindings for ZSTD
- [Intel QAT Overview](https://www.intel.com/content/www/us/en/developer/topic-technology/open/quick-assist-technology/overview.html): Hardware acceleration information

### Pull Requests
| PR | Description |
|----|-------------|
| [#232](https://github.com/opensearch-project/custom-codecs/pull/232) | Bump ZTD lib version to 1.5.6-1 |

## Related Feature Report

- [Full feature documentation](../../../features/custom-codecs/custom-codecs.md)
