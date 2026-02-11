---
tags:
  - skills
---
# Skills Dependencies

## Summary
Fixed jackson dependency version mismatches in the Skills plugin's `build.gradle`. The `jackson-annotations` artifact was referencing the wrong version variable (`versions.jackson` instead of `versions.jackson_annotations`), and `jackson-module-scala_3` was using a hardcoded version (`2.18.2`) instead of the centralized `${versions.jackson}` variable. Additionally, the `core-${opensearch_build}.jar` was added to the SQL dependency file tree.

## Details

### What's New in v3.5.0

This bugfix corrects dependency version management in the Skills plugin build configuration:

1. `jackson-annotations` dependency changed from `${versions.jackson}` to `${versions.jackson_annotations}`, ensuring the correct version is resolved for the annotations artifact
2. `jackson-module-scala_3` changed from hardcoded `2.18.2` to `${versions.jackson}`, aligning it with centralized version management
3. Added `core-${opensearch_build}.jar` to the SQL plugin dependency file tree inclusion pattern

### Technical Changes

| Change | Before | After |
|--------|--------|-------|
| `jackson-annotations` version variable | `${versions.jackson}` | `${versions.jackson_annotations}` |
| `jackson-module-scala_3` version | Hardcoded `2.18.2` | `${versions.jackson}` |
| SQL dependency jars | `opensearch-sql-thin`, `ppl`, `protocol` | Added `core` jar |

These changes ensure that jackson library versions are consistently managed through OpenSearch's centralized version properties, preventing potential classpath conflicts from version mismatches.

## Limitations
- The PR was bundled with the version increment to 3.5.0-SNAPSHOT, so the jackson fix is not isolated in a separate commit

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#683](https://github.com/opensearch-project/skills/pull/683) | Fix jackson version (included in version increment PR) | - |
