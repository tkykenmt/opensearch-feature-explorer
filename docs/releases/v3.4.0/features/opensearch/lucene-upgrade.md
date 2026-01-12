# Lucene Upgrade

## Summary

OpenSearch v3.4.0 upgrades Apache Lucene from 10.3.1 to 10.3.2. This is a bug fix release that addresses a potential EOF issue in the MaxScoreBulkScorer during optimized filter iterations.

## Details

### What's New in v3.4.0

This release bumps Lucene from version 10.3.1 to 10.3.2, incorporating a critical bug fix from the Lucene project.

### Technical Changes

#### Bug Fix: MaxScoreBulkScorer EOF Issue

Lucene 10.3.2 fixes a potential EOF (End of File) exception introduced by optimized filter iterations in `MaxScoreBulkScorer`. The issue occurred when the approximation and match verification could get out of sync, resulting in an `EOFException`.

This fix is tracked in [GITHUB#15380](https://github.com/apache/lucene/issues/15380).

#### Updated Components

| Component | Old Version | New Version |
|-----------|-------------|-------------|
| lucene-core | 10.3.1 | 10.3.2 |
| lucene-analysis-common | 10.3.1 | 10.3.2 |
| lucene-analysis-icu | 10.3.1 | 10.3.2 |
| lucene-analysis-kuromoji | 10.3.1 | 10.3.2 |
| lucene-analysis-nori | 10.3.1 | 10.3.2 |
| lucene-analysis-phonetic | 10.3.1 | 10.3.2 |
| lucene-analysis-smartcn | 10.3.1 | 10.3.2 |
| lucene-analysis-stempel | 10.3.1 | 10.3.2 |
| lucene-analysis-morfologik | 10.3.1 | 10.3.2 |
| lucene-backward-codecs | 10.3.1 | 10.3.2 |
| lucene-grouping | 10.3.1 | 10.3.2 |
| lucene-highlighter | 10.3.1 | 10.3.2 |
| lucene-expressions | 10.3.1 | 10.3.2 |

#### Version Mapping Update

The OpenSearch version mapping was updated to associate v3.4.0 with Lucene 10.3.2:

```java
public static final Version V_3_4_0 = new Version(3040099, org.apache.lucene.util.Version.LUCENE_10_3_2);
```

### Migration Notes

No migration steps are required. This is a minor version bump with backward-compatible changes.

## Limitations

- This is a bug fix release with no new features from Lucene

## References

### Documentation
- [Lucene 10.3.2 Release](https://github.com/apache/lucene/releases/tag/releases%2Flucene%2F10.3.2): Official Lucene 10.3.2 release

### Pull Requests
| PR | Description |
|----|-------------|
| [#20026](https://github.com/opensearch-project/OpenSearch/pull/20026) | Bump lucene version from 10.3.1 to 10.3.2 |

### Issues (Design / RFC)
- [GITHUB#15380](https://github.com/apache/lucene/issues/15380): Fix potential EOF in MaxScoreBulkScorer

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/lucene-upgrade.md)
