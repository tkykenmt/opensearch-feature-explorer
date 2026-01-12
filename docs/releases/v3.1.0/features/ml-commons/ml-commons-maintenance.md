# ML Commons Maintenance

## Summary

This release includes maintenance updates for the ML Commons plugin in OpenSearch v3.1.0. The changes focus on security improvements for hidden models, enhanced debugging capabilities, dependency upgrades, code refactoring, and CVE fixes.

## Details

### What's New in v3.1.0

#### Security: Hidden Model Trusted Connector Check Bypass

PR [#3838](https://github.com/opensearch-project/ml-commons/pull/3838) excludes hidden models from the trusted connector check. This allows internal/system models to operate without requiring explicit trusted connector configuration, improving the user experience for built-in ML capabilities.

#### Enhanced Deploy/Undeploy Logging

PR [#3825](https://github.com/opensearch-project/ml-commons/pull/3825) adds more detailed logging to model deploy and undeploy flows. This improves debugging capabilities when troubleshooting model deployment issues in production environments.

#### Code Cleanup: Remove libs Folder

PR [#3824](https://github.com/opensearch-project/ml-commons/pull/3824) removes the deprecated `libs` folder from the repository, following up on previous refactoring work to clean up the codebase structure.

#### HTTP Client Version Alignment

PR [#3809](https://github.com/opensearch-project/ml-commons/pull/3809) upgrades the HTTP client to align with OpenSearch core's version. This ensures compatibility and reduces potential conflicts between plugin and core dependencies.

#### Core API Integration: Stream Optional EnumSet

PR [#3648](https://github.com/opensearch-project/ml-commons/pull/3648) refactors `MLStatsInput` to use `StreamInput::readOptionalEnumSet` and `StreamOutput::writeOptionalEnumSet` from OpenSearch core (added in [OpenSearch#17556](https://github.com/opensearch-project/OpenSearch/pull/17556)). This replaces the private helper implementation with the standardized core API, enabling code reuse across plugins.

#### SearchIndexTool Arguments Parsing Fix

PR [#3883](https://github.com/opensearch-project/ml-commons/pull/3883) changes the `SearchIndexTool` arguments parsing logic to align tool schemas between ReAct agents and MCP (Model Context Protocol). The fix allows `SearchIndexTool` to parse parameters both from the `input` key wrapper and directly from the parameters map, enabling consistent tool registration across different agent types.

#### CVE Fix: commons-beanutils Upgrade

PR [#3935](https://github.com/opensearch-project/ml-commons/pull/3935) forces the runtime classpath to use `commons-beanutils:1.11.0` to resolve CVE-48734. This addresses a security vulnerability from transitive dependencies.

### Technical Changes

#### Components Updated

| Component | Change |
|-----------|--------|
| Hidden Model Security | Bypass trusted connector check for hidden models |
| Deploy/Undeploy Flow | Enhanced logging for debugging |
| MLStatsInput | Use core's optional EnumSet streaming APIs |
| SearchIndexTool | Flexible argument parsing for agent/MCP compatibility |
| Dependencies | HTTP client alignment, commons-beanutils CVE fix |

## Limitations

- The SearchIndexTool parsing change maintains backward compatibility but may require schema updates for MCP tool registrations

## References

### Documentation
- [OpenSearch#17556](https://github.com/opensearch-project/OpenSearch/pull/17556): Core optional EnumSet streaming APIs

### Pull Requests
| PR | Description |
|----|-------------|
| [#3838](https://github.com/opensearch-project/ml-commons/pull/3838) | Exclude trusted connector check for hidden model |
| [#3825](https://github.com/opensearch-project/ml-commons/pull/3825) | Add more logging to deploy/undeploy flows for better debugging |
| [#3824](https://github.com/opensearch-project/ml-commons/pull/3824) | Remove libs folder |
| [#3809](https://github.com/opensearch-project/ml-commons/pull/3809) | Upgrade HTTP client to version align with core |
| [#3648](https://github.com/opensearch-project/ml-commons/pull/3648) | Use stream optional enum set from core in MLStatsInput |
| [#3883](https://github.com/opensearch-project/ml-commons/pull/3883) | Change SearchIndexTool arguments parsing logic |
| [#3935](https://github.com/opensearch-project/ml-commons/pull/3935) | Force runtime class path commons-beanutils:1.11.0 to avoid CVE |
| [#426](https://github.com/opensearch-project/ml-commons/pull/426) | Bump version to 3.1.0.0 |
| [#588](https://github.com/opensearch-project/ml-commons/pull/588) | Fix model deploy failure due to ml-commons update |

### Issues (Design / RFC)
- [Issue #3834](https://github.com/opensearch-project/ml-commons/issues/3834): SearchIndexTool MCP schema alignment

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-commons-bugfixes.md)
