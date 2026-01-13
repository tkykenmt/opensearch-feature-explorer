---
tags:
  - opensearch
---
# Phone Search Analyzer

## Summary

In v2.19.0, the `phone-search` analyzer behavior was changed to no longer emit certain tokens that could cause false positive matches. The analyzer now produces fewer, more precise tokens to improve search accuracy.

## Details

### What's New in v2.19.0

The `phone-search` analyzer (used at search time) was modified to stop emitting the following tokens:

| Token Type | Before v2.19.0 | After v2.19.0 |
|------------|----------------|---------------|
| `tel:` / `sip:` prefix | Emitted as separate token | Not emitted |
| International calling code (e.g., `41`) | Emitted as separate token | Not emitted |
| Extension numbers | Emitted as separate token | Not emitted |
| Unformatted national number | Emitted as separate token | Not emitted |

### Token Output Comparison

**Before v2.19.0:**
```
Input: "tel:+441344840400"
Tokens: ["tel:+441344840400", "tel:", "441344840400", "44", "1344840400"]
```

**After v2.19.0:**
```
Input: "tel:+441344840400"
Tokens: ["tel:+441344840400", "441344840400"]
```

### Technical Changes

The `PhoneNumberTermTokenizer` class was modified to conditionally emit tokens based on the `addNgrams` flag:

- The `phone` analyzer (index time) continues to emit all tokens including n-grams
- The `phone-search` analyzer (search time) now only emits:
  - The original input
  - The full number with country code (e.g., `441344840400`)

### Rationale

The previous behavior could cause unintended matches:

- Emitting just the country code (`41`, `44`) would match all numbers from that country
- Emitting the national number without country code could match numbers in different countries
- Emitting `tel:` or `sip:` prefixes as tokens served no useful search purpose

### Migration Impact

This is a **breaking change** for existing indexes. After upgrading to v2.19.0:

- Existing indexed documents retain their original tokens
- New searches will produce fewer tokens
- Some previously matching queries may no longer match

**Recommendation**: Reindex documents after upgrading to ensure consistent behavior.

## Limitations

- This change affects only the `phone-search` analyzer, not the `phone` analyzer
- Existing indexes need reindexing to benefit from the improved precision

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16993](https://github.com/opensearch-project/OpenSearch/pull/16993) | `phone-search` analyzer: don't emit sip/tel prefix, int'l prefix, extension & unformatted input | - |

### Documentation
- [Phone number analyzers](https://docs.opensearch.org/2.19/analyzers/supported-analyzers/phone-analyzers/)
