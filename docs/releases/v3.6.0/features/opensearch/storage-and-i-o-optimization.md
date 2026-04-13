---
tags:
  - opensearch
---
# Storage & I/O Optimization

## Summary

OpenSearch v3.6.0 updates `MMapDirectory` to use Lucene's `ReadAdviseByContext` (`ADVISE_BY_CONTEXT`) instead of the default read advice. This restores context-aware `madvise` behavior that was lost after the Lucene 10.3.0 upgrade, ensuring that file I/O operations use the appropriate read advice (e.g., random access for vector files, sequential for merges) based on the `IOContext` provided by the caller.

## Details

### What's New in v3.6.0

Prior to this change, all memory-mapped file reads in OpenSearch used a single `NORMAL` read advice regardless of the access pattern. This was a regression introduced by Lucene 10.3.0 (adopted in OpenSearch 3.3+), which changed `MMapDirectory` to no longer honor the `IOContext`-based read advice by default.

The fix applies `MMapDirectory.setReadAdvice(MMapDirectory.ADVISE_BY_CONTEXT)` in two places within `FsDirectoryFactory`:

1. **HYBRIDFS** store type — when the primary directory is an `MMapDirectory`, the read advice is set before wrapping it in `HybridDirectory`
2. **MMAPFS** store type — the read advice is set on the newly created `MMapDirectory` before applying preload settings

### Technical Changes

The change modifies `FsDirectoryFactory.newFSDirectory()` in `server/src/main/java/org/opensearch/index/store/FsDirectoryFactory.java`:

```java
// HYBRIDFS case
mMapDirectory.setReadAdvice(MMapDirectory.ADVISE_BY_CONTEXT);

// MMAPFS case
final MMapDirectory mMapDirectory = new MMapDirectory(location, lockFactory);
mMapDirectory.setReadAdvice(MMapDirectory.ADVISE_BY_CONTEXT);
```

With `ADVISE_BY_CONTEXT`, Lucene's `MMapDirectory` delegates read advice selection to the `IOContext` passed when opening an `IndexInput`. This means:

- **Vector files (`.vec`)**: Use `RANDOM` access advice, matching the random read pattern of vector search
- **Stored fields (`.fdt`)**: Use `RANDOM` access advice for point lookups
- **Merge operations**: Use `SEQUENTIAL` advice for bulk reads
- **Default reads**: Use `NORMAL` advice

This is particularly beneficial for vector search workloads (k-NN) where random access patterns on `.vec` files were previously being served with `NORMAL` advice, leading to suboptimal kernel page cache behavior.

## Limitations

- This change only affects `MMapDirectory`-based store types (`mmapfs` and `hybridfs`). The `niofs` store type is unaffected since it does not use memory-mapped I/O.
- No new user-facing configuration is introduced — the behavior change is automatic.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/OpenSearch/pull/21031` | Original PR: Updated MMapDirectory to use ReadAdviseByContext | `https://github.com/opensearch-project/OpenSearch/issues/21012` |
| `https://github.com/opensearch-project/OpenSearch/pull/21062` | Backport to 3.6 branch | — |

### Related
- Lucene change that introduced the regression: `https://github.com/apache/lucene/pull/15040`
