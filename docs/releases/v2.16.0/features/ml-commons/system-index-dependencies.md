---
tags:
  - ml-commons
---
# ML Commons System Index & Dependencies

## Summary

OpenSearch v2.16.0 includes several bug fixes for ML Commons related to system index registration and dependency management. The key changes include formal registration of system indices through the SystemIndexPlugin extension point, DJL version upgrade, and connector naming improvements.

## Details

### System Index Registration

ML Commons now registers its system indices through the `SystemIndexPlugin.getSystemIndexDescriptors()` extension point in OpenSearch core. This change:

- Formally registers ML Commons indices as system indices
- Enables better integration with the security plugin for system index protection
- Aligns with the broader initiative to strengthen system index protection across the plugin ecosystem

Related to [opensearch-project/security#4439](https://github.com/opensearch-project/security/issues/4439) which aims to restrict plugin actions to only their own system indices when the ThreadContext is stashed.

### DJL Version Upgrade

Deep Java Library (DJL) upgraded from previous version to 0.28.0, which provides:

- Bug fixes and stability improvements for ML model inference
- Updated model support

### Connector Naming Fix

The multimodal connector name was changed to "bedrock multimodal connector" for clarity and consistency with AWS Bedrock naming conventions.

### Dependency Updates

- Bumped `braces` from 3.0.2 to 3.0.3 (security fix)
- ML Configuration Index mapping made compatible with ml-commons plugin

## Limitations

- System index registration is a formal change; indices function the same as before
- DJL upgrade may require testing with custom models

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2586](https://github.com/opensearch-project/ml-commons/pull/2586) | Register system index descriptors through SystemIndexPlugin.getSystemIndexDescriptors | [security#4439](https://github.com/opensearch-project/security/issues/4439) |
| [#2578](https://github.com/opensearch-project/ml-commons/pull/2578) | Upgrade DJL version to 0.28.0 | |
| [#2672](https://github.com/opensearch-project/ml-commons/pull/2672) | Change multimodal connector name to bedrock multimodal connector | |
| [#239](https://github.com/opensearch-project/ml-commons/pull/239) | Make ML Configuration Index Mapping compatible with ml-commons plugin | |
| [#341](https://github.com/opensearch-project/ml-commons/pull/341) | Bump braces from 3.0.2 to 3.0.3 | |
