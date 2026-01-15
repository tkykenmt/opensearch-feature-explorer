---
tags:
  - opensearch
---
# CAT API Help

## Summary

Updated the CAT API help output to replace legacy Elasticsearch references with OpenSearch terminology. This change affects the `_cat/nodes` endpoint help text.

## Details

### What's New in v2.16.0

The `_cat/nodes?help` endpoint previously displayed outdated terminology from the Elasticsearch fork:

| Field | Before | After |
|-------|--------|-------|
| version | es version | os version |
| type | es distribution type | os distribution type |
| build | es build hash | os build hash |

### Technical Changes

Modified `RestNodesAction.java` to update the description strings in the table cell definitions:

```java
// Before
table.addCell("version", "default:false;alias:v;desc:es version");
table.addCell("type", "default:false;alias:t;desc:es distribution type");
table.addCell("build", "default:false;alias:b;desc:es build hash");

// After
table.addCell("version", "default:false;alias:v;desc:os version");
table.addCell("type", "default:false;alias:t;desc:os distribution type");
table.addCell("build", "default:false;alias:b;desc:os build hash");
```

### Usage

```bash
GET _cat/nodes?help
```

Response now shows OpenSearch-specific terminology in the description column.

## Limitations

- Only the `_cat/nodes` endpoint was updated in this PR
- Other CAT API endpoints may still contain legacy references (see Issue #14653 for full scope)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14722](https://github.com/opensearch-project/OpenSearch/pull/14722) | Fix: update help output for _cat | [#14653](https://github.com/opensearch-project/OpenSearch/issues/14653) |

### Documentation
- [CAT nodes API](https://docs.opensearch.org/2.16/api-reference/cat/cat-nodes/)
- [CAT API](https://docs.opensearch.org/2.16/api-reference/cat/index/)
