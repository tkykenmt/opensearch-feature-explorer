# OUI (OpenSearch UI) Updates

## Summary

OpenSearch Dashboards v3.2.0 updates the OUI (OpenSearch UI) component library from version 1.19 to 1.21. These updates bring bug fixes, component improvements, and dependency updates to the UI framework.

## Details

### What's New in v3.2.0

This release includes two sequential OUI version updates:

1. **OUI 1.19 → 1.20** (PR #10153): Includes component fixes and snapshot updates for `EuiTabbedContent` with new `preserveTabContent` prop
2. **OUI 1.20 → 1.21** (PR #10284): Further refinements and bug fixes

### Technical Changes

#### Package Updates

The OUI dependency is updated across multiple package.json files:

| Package | Previous | Updated |
|---------|----------|---------|
| Root `package.json` | `@opensearch-project/oui@1.19.0` | `@opensearch-project/oui@1.21.0` |
| `osd-ui-framework` | `@opensearch-project/oui@1.19.0` | `@opensearch-project/oui@1.21.0` |
| `osd-ui-shared-deps` | `@opensearch-project/oui@1.19.0` | `@opensearch-project/oui@1.21.0` |
| Test plugins | `@opensearch-project/oui@1.19.0` | `@opensearch-project/oui@1.21.0` |

#### Component Changes

The update introduces the `preserveTabContent` prop to `EuiTabbedContent` component, affecting several plugins:

- `data` plugin: Shard failure modal
- `discover` plugin: Doc viewer
- `explore` plugin: Doc viewer and line visualization options
- `index_pattern_management` plugin: Scripting help flyout

### Files Changed

| File | Change Type |
|------|-------------|
| `package.json` | Version bump |
| `packages/osd-ui-framework/package.json` | Version bump |
| `packages/osd-ui-shared-deps/package.json` | Version bump |
| `yarn.lock` | Dependency resolution |
| Various `__snapshots__/*.snap` files | Updated component snapshots |

## Limitations

- OUI updates may require snapshot test updates in plugins using affected components
- The `preserveTabContent` prop defaults to `false`, maintaining backward compatibility

## References

### Documentation
- [OUI 1.20.0 Release](https://github.com/opensearch-project/oui/releases/tag/1.20.0): OUI version 1.20 release notes
- [OUI 1.21.0 Release](https://github.com/opensearch-project/oui/releases/tag/1.21.0): OUI version 1.21 release notes
- [OUI Repository](https://github.com/opensearch-project/oui): OpenSearch UI component library

### Pull Requests
| PR | Description |
|----|-------------|
| [#10153](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10153) | Update oui to 1.20 |
| [#10284](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10284) | Update oui to 1.21 |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/oui.md)
