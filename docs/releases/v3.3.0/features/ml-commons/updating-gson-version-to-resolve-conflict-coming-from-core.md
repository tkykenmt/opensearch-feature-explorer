# Updating Gson Version to Resolve Conflict Coming from Core

## Summary

This bugfix updates the Gson library version in ml-commons from 2.11.0 to 2.13.2 to resolve a dependency conflict with OpenSearch core. OpenSearch core upgraded Gson to 2.13.2 in September 2025, and ml-commons needed to align with this version to prevent runtime conflicts.

## Details

### What's New in v3.3.0

The Gson dependency was updated across all ml-commons modules to version 2.13.2 to match the version used by OpenSearch core.

### Technical Changes

#### Dependency Updates

| Module | Scope | Old Version | New Version |
|--------|-------|-------------|-------------|
| common | compileOnly | 2.11.0 | 2.13.2 |
| memory | testImplementation | 2.11.0 | 2.13.2 |
| ml-algorithms | implementation | 2.11.0 | 2.13.2 |
| plugin | implementation | 2.11.0 | 2.13.2 |
| search-processors | compileOnly | 2.11.0 | 2.13.2 |

#### Additional Changes

The plugin module also added:
- `error_prone_annotations` API dependency
- Resolution strategy force rules for both `gson:2.13.2` and `error_prone_annotations`

### Migration Notes

No migration required. This is a transparent dependency update that maintains backward compatibility.

## Limitations

None. Gson 2.13.2 is backward compatible with 2.11.0.

## Related PRs

| PR | Description |
|----|-------------|
| [#4176](https://github.com/opensearch-project/ml-commons/pull/4176) | Updating gson version to resolve conflict coming from core |

## References

- [OpenSearch PR #19290](https://github.com/opensearch-project/OpenSearch/pull/19290): Bump com.google.code.gson:gson from 2.13.1 to 2.13.2 in /plugins/repository-hdfs
- [Gson 2.13.2 Release](https://github.com/google/gson/releases/tag/gson-parent-2.13.2): Improved JPMS module packaging

## Related Feature Report

- [ML Commons Dependencies](../../../features/ml-commons/ml-commons-dependencies.md)
