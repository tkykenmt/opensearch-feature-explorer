# Lucene Upgrade

## Summary

OpenSearch relies on Apache Lucene as its core search library. Lucene upgrades bring performance improvements, new features, bug fixes, and security enhancements to OpenSearch. These upgrades are essential for maintaining compatibility with the latest search capabilities and ensuring optimal performance.

## Details

### Architecture

```mermaid
graph TB
    subgraph OpenSearch
        OS[OpenSearch Core]
        Codec[Codec Layer]
        Index[Index Management]
    end
    
    subgraph Lucene
        LC[Lucene Core]
        PF[Postings Format]
        DV[Doc Values]
        KNN[KNN Vectors]
        Analysis[Analysis]
    end
    
    OS --> Codec
    Codec --> LC
    Index --> LC
    LC --> PF
    LC --> DV
    LC --> KNN
    LC --> Analysis
```

### Components

| Component | Description |
|-----------|-------------|
| Lucene Core | Core search library providing indexing and search capabilities |
| Postings Format | Encodes term frequencies, positions, and skip data |
| Doc Values | Column-oriented storage for sorting and aggregations |
| KNN Vectors | Vector similarity search support |
| Analysis | Text analysis and tokenization |

### Configuration

No specific configuration is required for Lucene upgrades. The version is managed at the OpenSearch build level.

| Setting | Description | Default |
|---------|-------------|---------|
| N/A | Lucene version is bundled with OpenSearch | Determined by OpenSearch version |

### Usage Example

Lucene version can be verified through the nodes info API:

```bash
GET /_nodes?filter_path=nodes.*.version
```

## Limitations

- Lucene upgrades may require index format changes
- Major Lucene version upgrades may require reindexing
- Some Lucene features may not be exposed through OpenSearch APIs

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v2.18.0 | [#15333](https://github.com/opensearch-project/OpenSearch/pull/15333) | Update Apache Lucene to 9.12.0 |
| v3.0.0 | [#16366](https://github.com/opensearch-project/OpenSearch/pull/16366) | Apache Lucene 10 update |

## References

- [Lucene 9.12.0 Changelog](https://lucene.apache.org/core/9_12_0/changes/Changes.html): Official Lucene 9.12.0 release notes
- [Apache Lucene](https://lucene.apache.org/): Official Apache Lucene project
- [OpenSearch Documentation](https://docs.opensearch.org/): OpenSearch official documentation

## Change History

- **v3.0.0**: Upgrade to Apache Lucene 10
- **v2.18.0**: Upgrade to Apache Lucene 9.12.0 with new Lucene912PostingsFormat, JDK 23 Panama Vectorization support, dynamic range facets, and various performance optimizations
