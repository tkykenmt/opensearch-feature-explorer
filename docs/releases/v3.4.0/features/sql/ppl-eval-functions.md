---
tags:
  - indexing
  - sql
---

# PPL Eval Functions

## Summary

OpenSearch v3.4.0 adds several new eval functions to PPL (Piped Processing Language) for working with multivalue arrays and string conversion. These functions enhance data transformation capabilities within PPL queries, enabling users to manipulate arrays, remove duplicates, extract subsets, and convert values to strings with various formatting options.

## Details

### What's New in v3.4.0

This release introduces four new eval functions and one function alias:

| Function | Description |
|----------|-------------|
| `mvappend(value1, value2, ...)` | Combines multiple values or arrays into a single array |
| `mvindex(array, index)` / `mvindex(array, start, end)` | Returns element(s) from an array by index or range |
| `mvdedup(array)` | Removes duplicate values from an array (order-preserving) |
| `tostring(value, format)` | Converts values to strings with optional formatting |
| `regexp_replace()` | Alias for `replace()` function |

### Technical Changes

#### New Multivalue Functions

**mvappend** - Combines all arguments into a single array:
- Each argument can be a value, an array, or null
- Useful for merging extracted fields with existing fields (e.g., in `spath` command)

**mvindex** - Returns array elements by index:
- Supports 0-based indexing (first element at index 0)
- Supports negative indexing (-1 = last element, -2 = second-to-last)
- Range access is inclusive (start to end)

**mvdedup** - Removes duplicates from arrays:
- Order-preserving: keeps first occurrence of each value
- Empty arrays return empty arrays

#### String Conversion Function

**tostring** - Converts values to strings with formatting:
- Supports format options: `"binary"`, `"hex"`, `"commas"`, `"duration"`
- Boolean values return `"True"` or `"False"`

#### Function Alias

**regexp_replace** - Added as alias for `replace()`:
- Also renamed `regex_match()` to `regexp_match()` (keeping `regex_match()` as synonym)

### Usage Examples

#### mvappend
```ppl
source=index | eval combined = mvappend(array('a', 'b'), 'c', array('d'))
# Returns: ['a', 'b', 'c', 'd']
```

#### mvindex - Single Element
```ppl
source=people | eval array = array('a', 'b', 'c', 'd', 'e'), result = mvindex(array, 1)
# Returns: b

source=people | eval array = array('a', 'b', 'c', 'd', 'e'), result = mvindex(array, -1)
# Returns: e
```

#### mvindex - Range Access
```ppl
source=people | eval array = array(1, 2, 3, 4, 5), result = mvindex(array, 1, 3)
# Returns: [2, 3, 4]

source=people | eval array = array(1, 2, 3, 4, 5), result = mvindex(array, -3, -1)
# Returns: [3, 4, 5]
```

#### mvdedup
```ppl
source=index | eval result = mvdedup(array(1, 2, 2, 3, 1, 4))
# Returns: [1, 2, 3, 4]
```

#### tostring
```ppl
# Binary conversion
... | eval result = tostring(9, "binary")
# Returns: 1001

# Hex conversion
... | eval result = tostring(15, "hex")
# Returns: 0xF

# Commas formatting
... | eval result = tostring(12345.6789, "commas")
# Returns: 12,345.68

# Duration formatting (seconds to HH:MM:SS)
... | eval foo=615 | eval foo2 = tostring(foo, "duration")
# Returns: 00:10:15

# Boolean conversion
... | eval n = tostring(1==1)
# Returns: True
```

## Limitations

- `mvindex` range access is inclusive on both ends (differs from some programming languages)
- `tostring` format argument only applies to numeric values
- These functions are available in the Calcite-based PPL engine

## References

### Documentation
- [OpenSearch PPL Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/ppl/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#4438](https://github.com/opensearch-project/sql/pull/4438) | Add `mvappend` function for Calcite PPL |
| [#4497](https://github.com/opensearch-project/sql/pull/4497) | Support `tostring()` eval function |
| [#4765](https://github.com/opensearch-project/sql/pull/4765) | Add `regexp_replace()` function as alias of `replace()` |
| [#4794](https://github.com/opensearch-project/sql/pull/4794) | Support `mvindex` eval function |
| [#4828](https://github.com/opensearch-project/sql/pull/4828) | Support `mvdedup` eval function |

### Issues (Design / RFC)
- [Issue #4492](https://github.com/opensearch-project/sql/issues/4492): tostring implementation request
- [Issue #4433](https://github.com/opensearch-project/sql/issues/4433): mvappend function request
- [Issue #4764](https://github.com/opensearch-project/sql/issues/4764): regexp_replace alias request
- [RFC #4287](https://github.com/opensearch-project/sql/issues/4287): tostring function RFC

## Related Feature Report

- [Full feature documentation](../../../features/sql/sql-ppl-eval-functions.md)
