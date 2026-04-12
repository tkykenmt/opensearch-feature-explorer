---
tags:
  - opensearch
---
# Search Optimizations

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to Search Optimizations.

## Details

### New Features

- **Enable numeric sort optimisation for few numerical sort types**: Enabling numeric sort optimisation for below 4 numeric ypes. 1. DATE 2. DATE_NANOSECONDS 3. LONG 4. DOUBLE For above 4 types, we have same sort type and point type. So should not be any harm doing like that. Lucene gives us in-built ability to optimise sorting on certain sort field types where its p

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#6321](https://github.com/opensearch-project/OpenSearch/pull/6321) | Enable numeric sort optimisation for few numerical sort types | OpenSearch |
