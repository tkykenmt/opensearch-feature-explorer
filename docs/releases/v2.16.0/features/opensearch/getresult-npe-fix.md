---
tags:
  - opensearch
---
# GetResult NPE Fix

## Summary

Fixed a NullPointerException (NPE) in `GetResult.fromXContentEmbedded()` that occurred when parsing a GetResult response with a missing `found` field. The fix adds proper null checking and throws a descriptive `ParsingException` instead of an unexpected NPE.

## Details

### What's New in v2.16.0

The `GetResult.fromXContentEmbedded()` method now validates that the required `found` field is present before constructing the GetResult object. If the field is missing, a `ParsingException` with the message "Missing required field [found]" is thrown.

### Technical Changes

The bug occurred because:
1. The `found` variable was initialized to `null` (as a `Boolean` wrapper type)
2. The field was only conditionally set when parsing the JSON
3. When `found` remained `null`, unboxing it to a primitive `boolean` for the constructor caused an NPE

The fix adds a null check after parsing completes:

```java
if (found == null) {
    throw new ParsingException(
        parser.getTokenLocation(),
        String.format(Locale.ROOT, "Missing required field [%s]", GetResult.FOUND)
    );
}
```

### Affected Component

| Component | File |
|-----------|------|
| GetResult | `server/src/main/java/org/opensearch/index/get/GetResult.java` |

## Limitations

None. This is a straightforward bug fix that improves error handling consistency.

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14552](https://github.com/opensearch-project/OpenSearch/pull/14552) | Handle NPE in GetResult if "found" field is missing | [#14519](https://github.com/opensearch-project/OpenSearch/issues/14519) |
