---
tags:
  - opensearch
---
# Derived Fields

## Summary

Fixed a race condition in derived field parsing when derived fields are defined within search requests. The issue caused `ConcurrentModificationException` errors during concurrent search operations.

## Details

### What's New in v2.16.0

This release fixes a critical race condition that occurred when derived fields were defined in search requests rather than index mappings.

### Technical Changes

The bug occurred because:
1. Derived fields are created per `QueryShardContext`
2. Multiple `QueryShardContext` instances can be created for a single search request
3. The `DocumentMapperParser.parse()` method modifies the map passed to it by removing parsed keys
4. When multiple contexts tried to parse the same derived field definition concurrently, a `ConcurrentModificationException` was thrown

The fix implements a `deepCopy()` method in `DefaultDerivedFieldResolver` that creates a complete copy of the derived field object map before passing it to the parser. This ensures each parsing operation works on its own copy of the data.

```java
// Before (race condition)
.parse(DerivedFieldMapper.CONTENT_TYPE, derivedFieldObject);

// After (thread-safe)
.parse(DerivedFieldMapper.CONTENT_TYPE, (Map) deepCopy(derivedFieldObject));
```

The `deepCopy()` method recursively copies:
- Maps (creating new HashMap instances)
- Lists (creating new ArrayList instances)
- Byte arrays (using Arrays.copyOf)
- Primitive values (passed through unchanged)

## Limitations

No new limitations introduced. See the Derived Fields feature documentation for existing limitations.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14445](https://github.com/opensearch-project/OpenSearch/pull/14445) | Fix race condition while parsing derived fields from search definition | [#14444](https://github.com/opensearch-project/OpenSearch/issues/14444) |
