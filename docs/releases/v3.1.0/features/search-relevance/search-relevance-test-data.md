---
tags:
  - domain/search
  - component/server
  - indexing
  - search
---
# Search Relevance Test Data

## Summary

This release adds a realistic test dataset based on Amazon's ESCI (Shopping Queries Dataset) to the Search Relevance Workbench. The dataset includes product data with images, 150 queries with matching judgments, enabling comprehensive demonstration and testing of search relevance evaluation capabilities.

## Details

### What's New in v3.1.0

PR [#70](https://github.com/opensearch-project/search-relevance/pull/70) introduces a complete test dataset sourced from the ESCI benchmark dataset, providing:

- **Product data**: E-commerce product catalog with images for all products
- **Query set**: 150 queries from the ESCI ranking task (`esci_us_queryset.json`)
- **Judgments**: Matching relevance judgments for query-document pairs (`esci_us_judgments.json`)

### Technical Changes

#### New Data Files

| File | Description | Records |
|------|-------------|---------|
| `esci_us_queryset.json` | Query set with 150 queries from ESCI | 150 queries |
| `esci_us_judgments.json` | Relevance judgments for query-document pairs | ~7000 judgments |
| `esci_us_opensearch-2025-06-06.json` | Product data (downloaded from S3) | Full catalog |

#### Demo Script Updates

The `demo.sh` and `demo_hybrid_optimizer.sh` scripts were updated to:

1. Download the new ESCI-based product data from S3
2. Process data in chunks (50,000 lines per chunk) for reliable bulk indexing
3. Upload ESCI query sets and judgments to Search Relevance Workbench
4. Increase field mapping limits for SRW indexes to handle dynamic fields

#### Data Source

The test data is derived from Amazon's ESCI (Shopping Queries Dataset):

```
@article{reddy2022shopping,
  title={Shopping Queries Dataset: A Large-Scale {ESCI} Benchmark for Improving Product Search},
  author={Chandan K. Reddy and Lluís Màrquez and Fran Valero and Nikhil Rao and Hugo Zaragoza and Sambaran Bandyopadhyay and Arnab Biswas and Anlu Xing and Karthik Subbian},
  year={2022},
  eprint={2206.06588},
  archivePrefix={arXiv}
}
```

### Usage Example

The demo script automatically sets up the test data:

```bash
cd search-relevance/src/test/scripts
./demo.sh
```

This will:
1. Download the ESCI product data from S3
2. Create and populate the `ecommerce` index
3. Upload the ESCI query set and judgments
4. Configure Search Relevance Workbench for experimentation

Query set format:
```json
{
  "name": "ESCI Queries",
  "description": "Queries from the ESCI ranking task",
  "sampling": "manual",
  "querySetQueries": [
    { "queryText": "laptop" },
    { "queryText": "red shoes" },
    { "queryText": "in-ear headphones" }
  ]
}
```

### Migration Notes

Users running the demo scripts should note:
- The data file has changed from `transformed_esci_1.json` to `esci_us_opensearch-2025-06-06.json`
- Data is now downloaded from a new S3 location: `https://o19s-public-datasets.s3.amazonaws.com/esci_us_opensearch-2025-06-06.json`

## Limitations

- The test dataset is a subset of the full ESCI dataset, optimized for demonstration purposes
- Product images are hosted externally and require internet connectivity

## References

### Documentation
- [Search Relevance Workbench Documentation](https://docs.opensearch.org/3.1/search-plugins/search-relevance/using-search-relevance-workbench/)
- [ESCI Dataset](https://github.com/amazon-science/esci-data): Amazon Shopping Queries Dataset

### Blog Posts
- [Taking your first steps towards search relevance](https://opensearch.org/blog/taking-your-first-steps-towards-search-relevance/): Blog post demonstrating SRW with ESCI data

### Pull Requests
| PR | Description |
|----|-------------|
| [#70](https://github.com/opensearch-project/search-relevance/pull/70) | Use realistic dataset based on ESCI |

## Related Feature Report

- [Full feature documentation](../../../features/search-relevance/search-relevance-workbench.md)
