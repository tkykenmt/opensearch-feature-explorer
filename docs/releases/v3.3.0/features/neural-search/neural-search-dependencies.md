# Neural Search Dependencies

## Summary

This release item addresses dependency management issues in the Neural Search plugin for OpenSearch v3.3.0. The changes resolve jar hell conflicts, update Lucene codec paths for backward compatibility, and migrate from the deprecated `commons-lang` to `commons-lang3` library.

## Details

### What's New in v3.3.0

Three key dependency-related fixes were implemented:

1. **commons-lang Migration**: Removed the deprecated `commons-lang:commons-lang` (v2.6) dependency and migrated to `commons-lang3` using Gradle version catalog
2. **Lucene Codec Path Update**: Updated Lucene101 codec imports from `org.apache.lucene.codecs.lucene101` to `org.apache.lucene.backward_codecs.lucene101` for backward compatibility
3. **Error Prone Version Fix**: Forced `error_prone_annotations` to version 2.21.1 to resolve version conflicts with Guava

### Technical Changes

#### Dependency Updates

| Change | Before | After |
|--------|--------|-------|
| commons-lang | `commons-lang:commons-lang:2.6` | `org.apache.commons:commons-lang3:${versions.commonslang}` |
| Lucene codec path | `org.apache.lucene.codecs.lucene101` | `org.apache.lucene.backward_codecs.lucene101` |
| error_prone_annotations | Conflicting versions | Forced to `2.21.1` |

#### Files Modified

**PR #1551 - commons-lang Migration**:
- `build.gradle`: Updated dependency declarations
- Multiple Java files updated imports from `org.apache.commons.lang.*` to `org.apache.commons.lang3.*`:
  - Query builders (`NeuralQueryBuilder`, `NeuralSparseQueryBuilder`, `HybridQueryBuilder`, `AgenticSearchQueryBuilder`)
  - Mapper DTOs (`ChunkingConfig`, `SparseEncodingConfig`)
  - Stats classes (`EventStatName`, `InfoStatName`)
  - Utility classes (`NeuralQueryValidationUtil`, `PruneType`)
  - Test classes

**PR #1574 - Lucene Codec Path Update**:
- `build.gradle`: Added resolution strategy for error_prone_annotations
- `ClusteredPostingTermsWriter.java`: Updated Lucene101PostingsFormat import
- `SparseCodec.java`: Updated Lucene101Codec import
- Test files updated accordingly

**PR #1589 - QA Gradle Dependency**:
- `qa/build.gradle`: Updated commons-lang dependency to commons-lang3

### Migration Notes

For plugin developers extending Neural Search:

1. Update any imports from `org.apache.commons.lang.*` to `org.apache.commons.lang3.*`
2. Note API differences between commons-lang 2.x and 3.x (e.g., `RandomUtils.nextFloat()` now requires parameters)
3. If using Lucene101 codecs directly, update import paths to use `backward_codecs`

## Limitations

- The error_prone_annotations version is forced to 2.21.1 as a temporary workaround until upstream dependencies resolve the version conflict

## Related PRs

| PR | Description |
|----|-------------|
| [#1551](https://github.com/opensearch-project/neural-search/pull/1551) | Remove commons-lang dependency and use gradle version catalog for commons-lang3 |
| [#1574](https://github.com/opensearch-project/neural-search/pull/1574) | Update Lucene101 codec path to backward path & force errorprone version |
| [#1589](https://github.com/opensearch-project/neural-search/pull/1589) | Upgrade QA Gradle Dependency Version with commons-lang3 |

## References

- [k-NN PR #2863 Comment](https://github.com/opensearch-project/k-NN/pull/2863#issuecomment-3251945721): Original jar hell issue report

## Related Feature Report

- [Full feature documentation](../../../../features/neural-search/neural-search-dependencies.md)
