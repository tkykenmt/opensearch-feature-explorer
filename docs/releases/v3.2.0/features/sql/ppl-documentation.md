# SQL/PPL Documentation

## Summary

This release item updates the PPL documentation index and limitations documentation for the SQL plugin. The changes add missing function categories (Collection, Cryptographic, JSON) to the PPL documentation index and update the V3 Calcite engine limitations documentation to reflect the current state of supported features.

## Details

### What's New in v3.2.0

Two documentation updates improve the accuracy and completeness of PPL reference materials:

1. **PPL Documentation Index Update**: Added links to three new function categories that were missing from the main documentation index:
   - Collection Functions
   - Cryptographic Functions
   - JSON Functions

2. **V3 Engine Limitations Update**: Streamlined the limitations documentation to reflect features that are now supported in the V3 Calcite engine, removing items that were previously listed as unsupported but have since been implemented.

### Technical Changes

#### Documentation Index Changes

The PPL index (`docs/user/ppl/index.rst`) was updated to include links to function documentation that was added in previous releases but missing from the index:

| Function Category | Description | Related PR |
|-------------------|-------------|------------|
| Collection Functions | Array/multi-value field operations | [#3584](https://github.com/opensearch-project/sql/pull/3584) |
| Cryptographic Functions | Hash and encryption functions | [#3574](https://github.com/opensearch-project/sql/pull/3574) |
| JSON Functions | JSON parsing and manipulation | [#3559](https://github.com/opensearch-project/sql/pull/3559) |

#### Limitations Documentation Changes

The V3 engine limitations documentation was updated in multiple files:
- `docs/dev/intro-v3-engine.md`: Updated version references from "3.0.0-beta" to "3.0.0"
- `docs/user/limitations/limitations.rst`: Added Calcite engine limitations section
- `docs/user/ppl/limitations/limitations.rst`: Added unsupported functionalities section

Items removed from the unsupported list (now supported in V3):
- `trendline`
- `show datasource`
- `explain`
- `describe`
- `top` and `rare`
- `fillnull`
- `patterns`
- Query with metadata fields (`_id`, `_doc`, etc.)
- JSON relevant functions (`cast to json`, `json`, `json_valid`)

Items that remain unsupported in V3 (fallback to V2):
- All SQL queries
- `dedup` with `consecutive=true`
- Search relevant commands (AD, ML, Kmeans)
- Commands with `fetch_size` parameter
- Search relevant functions (match, match_phrase, etc.)

### Usage Example

After these documentation updates, users can find the new function categories in the PPL reference:

```ppl
# Collection Functions example
source=logs | eval arr_len = array_length(tags)

# Cryptographic Functions example
source=users | eval hash = md5(email)

# JSON Functions example
source=events | eval parsed = json_extract(payload, '$.status')
```

## Limitations

- Documentation updates only; no functional changes to the SQL/PPL plugin
- The V3 Calcite engine remains experimental

## Related PRs

| PR | Description |
|----|-------------|
| [#3868](https://github.com/opensearch-project/sql/pull/3868) | Update ppl documentation index for new functions |
| [#3801](https://github.com/opensearch-project/sql/pull/3801) | Update the limitation docs |

## References

- [PR #3559](https://github.com/opensearch-project/sql/pull/3559): JSON functions implementation
- [PR #3584](https://github.com/opensearch-project/sql/pull/3584): Array/Collection functions implementation
- [PR #3574](https://github.com/opensearch-project/sql/pull/3574): Cryptographic functions implementation
- [PPL Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/ppl/index/): Official PPL reference
- [SQL/PPL Limitations](https://docs.opensearch.org/3.0/search-plugins/sql/limitation/): Engine limitations

## Related Feature Report

- [Calcite Query Engine](../../../../features/sql/calcite-query-engine.md)
