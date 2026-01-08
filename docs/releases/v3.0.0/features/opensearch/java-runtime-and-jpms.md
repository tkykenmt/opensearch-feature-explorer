# Java Runtime & JPMS

## Summary

OpenSearch 3.0 introduces two major breaking changes: JDK 21 as the minimum supported Java runtime and Phase-0 JPMS (Java Platform Module System) support. These changes modernize the codebase, eliminate split packages, and prepare OpenSearch for future modularization while enabling performance improvements from modern JVM features.

## Details

### What's New in v3.0.0

#### JDK 21 Minimum Requirement

OpenSearch 3.0 requires JDK 21 as the minimum supported Java runtime, a significant upgrade from JDK 11 in OpenSearch 2.x. This enables:
- Virtual threads for improved concurrency
- Pattern matching for `switch` statements
- Sequenced collections
- MemorySegment API for improved mmap performance (finalized from JDK 19+ preview APIs)
- Better overall performance (benchmarks showed JDK 17+ significantly outperformed earlier versions)

#### JPMS Phase-0: Split Package Elimination

The codebase has been refactored to eliminate top-level split packages, preparing for full JPMS support:

| Original Package | New Package | Module |
|-----------------|-------------|--------|
| `org.opensearch.bootstrap` | `org.opensearch.common.bootstrap` | `:libs:opensearch-common` |
| `org.opensearch.cli` | `org.opensearch.common.cli` | `:server` |
| `org.opensearch.client` | `org.opensearch.transport.client` | `:server` |
| `org.opensearch.common.settings` | `org.opensearch.cli.keystore` | `:distribution:tools:keystore-cli` |
| `org.apache.lucene.*` | `org.opensearch.lucene.*` | `:server` |

### Technical Changes

#### Package Refactoring

1. **Bootstrap Package** ([#17117](https://github.com/opensearch-project/OpenSearch/pull/17117)): Moved from `:libs:opensearch-common` and `:server` split to unified `org.opensearch.common.bootstrap`

2. **CLI Package** ([#17153](https://github.com/opensearch-project/OpenSearch/pull/17153)): 
   - Refactored `:server` module's `org.opensearch.cli` to `org.opensearch.common.cli`
   - Removed unused `LoggingAwareCommand.java`
   - Moved common CLI tests from `:server` to `:libs`
   - Refactored `plugin-cli` to `org.opensearch.tools.cli.plugin`
   - Refactored `upgrade-cli` to `org.opensearch.tools.cli.upgrade`
   - Removed `:libs:plugin-classloader`, moved `ExtendedPluginsClassLoader` to `:server`

3. **Client Package** ([#17272](https://github.com/opensearch-project/OpenSearch/pull/17272)): Refactored `org.opensearch.client` to `org.opensearch.transport.client` to resolve split package with REST client

4. **Lucene Package** ([#17241](https://github.com/opensearch-project/OpenSearch/pull/17241)): Refactored `org.apache.lucene` classes to `org.opensearch.lucene`:
   - Removed `OneMergeHelper.java`, merged into `OpenSearchConcurrentMergeScheduler`
   - Moved `Packed64` implementation directly to `CuckooFilter`
   - Updated `ShuffleForcedMergePolicy` to use `addDiagnostics`
   - Added `MinimizationOperations` with new `Automaton` class from Lucene
   - Updated `QueryStringQueryParser` from `XQueryParser` to standard `QueryParser`
   - Updated `CustomFieldHighlighter` with `getFieldOffsetStrategy` method

#### MMap Preview API Support

When running with JDK 19+, OpenSearch can use the MemorySegment API for improved mmap performance ([#5151](https://github.com/opensearch-project/OpenSearch/pull/5151)):

```bash
# Enable preview features for MemorySegment API
OPENSEARCH_JAVA_OPTS="--enable-preview" ./bin/opensearch
```

With `--enable-preview`:
```
[INFO] Using MemorySegmentIndexInput with Java 21
```

Without `--enable-preview`:
```
[WARN] You are running with Java 21. To make full use of MMapDirectory, please pass '--enable-preview' to the Java command line.
```

### Migration Notes

1. **Upgrade JDK**: Ensure JDK 21 or later is installed
2. **Update Dependencies**: Plugins using affected packages must update imports:
   - `org.opensearch.cli.*` → `org.opensearch.common.cli.*`
   - `org.opensearch.client.*` → `org.opensearch.transport.client.*`
   - `org.opensearch.bootstrap.*` → `org.opensearch.common.bootstrap.*`
3. **Java High-Level REST Client**: No longer supports JDK 8
4. **Environment Variables**: Use `OPENSEARCH_JAVA_HOME` to specify JDK path (takes precedence over `JAVA_HOME`)

## Limitations

- Full JPMS modularization (Phase 1+) is still in progress
- Some `org.apache.lucene` packages remain (codecs, index, search.grouping) pending Star Tree implementation

## Related PRs

| PR | Description |
|----|-------------|
| [#5151](https://github.com/opensearch-project/OpenSearch/pull/5151) | Allow mmap to use JDK-19 preview APIs |
| [#17117](https://github.com/opensearch-project/OpenSearch/pull/17117) | Refactor `:libs` bootstrap package |
| [#17153](https://github.com/opensearch-project/OpenSearch/pull/17153) | Refactor CLI and plugin packages |
| [#17241](https://github.com/opensearch-project/OpenSearch/pull/17241) | Refactor `org.apache.lucene` packages |
| [#17272](https://github.com/opensearch-project/OpenSearch/pull/17272) | Refactor `org.opensearch.client` package |

## References

- [Issue #8110](https://github.com/opensearch-project/OpenSearch/issues/8110): META - Split and modularize the server monolith
- [Breaking Changes](https://docs.opensearch.org/3.0/breaking-changes/): JDK 21 requirement documentation
- [OpenSearch 3.0 Blog](https://opensearch.org/blog/opensearch-3-0-what-to-expect/): What to expect in OpenSearch 3.0
- [Java Runtime Blog](https://opensearch.org/blog/opensearch-java-runtime/): Using different Java runtimes with OpenSearch

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/java-runtime-and-jpms.md)
