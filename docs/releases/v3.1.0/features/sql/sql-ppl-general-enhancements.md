---
tags:
  - domain/search
  - component/server
  - observability
  - sql
---
# SQL/PPL General Enhancements

## Summary

OpenSearch v3.1.0 introduces significant enhancements to the SQL/PPL plugin, adding new function categories including JSON manipulation, array/lambda operations, cryptographic hashing, time-based condition functions, and improved aggregation capabilities. These additions expand PPL's data processing capabilities for complex log analysis and data transformation workflows.

## Details

### What's New in v3.1.0

This release adds 8 major enhancements to the SQL/PPL plugin:

1. **JSON Functions** - Comprehensive JSON manipulation capabilities
2. **Lambda and Array Functions** - Functional programming constructs for array processing
3. **Cryptographic Hash Functions** - SHA2, MD5, SHA1 for data hashing
4. **Time Condition Functions** - `earliest` and `latest` for relative time calculations
5. **Approximate Distinct Count** - HyperLogLog++ based cardinality estimation
6. **Object Field Merging** - Schema merging across multiple indices
7. **match_only_text Support** - New field type support in PPL
8. **Percentile Algorithm Change** - MergingDigest implementation for OpenSearch alignment

### Technical Changes

#### New Functions

| Category | Functions | Description |
|----------|-----------|-------------|
| JSON | `json`, `json_valid`, `json_object`, `json_array`, `json_array_length`, `json_extract`, `json_delete`, `json_set`, `json_append`, `json_extend`, `json_keys` | JSON creation, validation, and manipulation |
| Array/Lambda | `array`, `array_length`, `forall`, `exists`, `filter`, `transform`, `reduce` | Array operations with lambda expressions |
| Cryptographic | `md5`, `sha1`, `sha2` (SHA224, SHA256, SHA384, SHA512) | Cryptographic hash functions |
| Time Condition | `earliest`, `latest` | Relative time calculation from current time |
| Aggregation | `distinct_count_approx` | Approximate cardinality using HyperLogLog++ |

#### JSON Functions Detail

| Function | Syntax | Description |
|----------|--------|-------------|
| `json` | `json(value)` | Returns value if valid JSON, else null |
| `json_valid` | `json_valid(value)` | Returns true if value is valid JSON |
| `json_object` | `json_object(key1, val1, ...)` | Creates JSON object from key-value pairs |
| `json_array` | `json_array(val1, val2, ...)` | Creates JSON array from values |
| `json_array_length` | `json_array_length(json_string)` | Returns array length |
| `json_extract` | `json_extract(target, path1, ...)` | Extracts values using paths |
| `json_delete` | `json_delete(target, path1, ...)` | Removes values at paths |
| `json_set` | `json_set(target, path1, val1, ...)` | Sets values at paths |
| `json_append` | `json_append(target, path, val)` | Appends to array at path |
| `json_extend` | `json_extend(target, path, array)` | Extends array at path |
| `json_keys` | `json_keys(target)` | Returns object keys |

#### Lambda Functions Detail

| Function | Syntax | Description |
|----------|--------|-------------|
| `array` | `array(val1, val2, ...)` | Creates array with type inference |
| `array_length` | `array_length(arr)` | Returns array length |
| `forall` | `forall(arr, x -> predicate)` | True if all elements satisfy predicate |
| `exists` | `exists(arr, x -> predicate)` | True if any element satisfies predicate |
| `filter` | `filter(arr, x -> predicate)` | Returns elements satisfying predicate |
| `transform` | `transform(arr, x -> expr)` or `transform(arr, (x, i) -> expr)` | Transforms each element |
| `reduce` | `reduce(arr, init, (acc, x) -> expr)` or `reduce(arr, init, acc_fn, reduce_fn)` | Reduces array to single value |

### Usage Examples

```sql
-- JSON functions
source=data | eval obj = json_object("name", "test", "value", 123)
source=data | eval arr = json_array(1, 2, 3)
source=data | eval val = json_extract(json_field, "user.name")
source=data | eval updated = json_set(json_field, "status", "active")

-- Lambda functions
source=data | eval filtered = filter(array(1, 2, 3, 4, 5), x -> x > 2)
source=data | eval doubled = transform(array(1, 2, 3), x -> x * 2)
source=data | eval sum = reduce(array(1, 2, 3), 0, (acc, x) -> acc + x)
source=data | eval all_positive = forall(values, x -> x > 0)

-- Cryptographic hash functions
source=data | eval hash = sha2(password, 256)
source=data | eval md5_hash = md5(content)

-- Time condition functions
source=logs | where timestamp > earliest("-1d")
source=logs | where timestamp < latest("-1h")

-- Approximate distinct count
source=logs | stats distinct_count_approx(user_id) as unique_users

-- Multi-index object field merging
source=index1, index2 | fields machine.os1, machine.os2
```

### Migration Notes

- **Percentile Breaking Change**: The percentile function now uses MergingDigest algorithm instead of the previous implementation. This aligns with OpenSearch's native percentile aggregation but may produce slightly different results for existing queries.

## Limitations

- Lambda functions do not support nested object access (e.g., `x -> x.field.subfield`)
- JSON path syntax uses `{index}` for array access (e.g., `"a{0}.b"`)
- `distinct_count_approx` provides approximate results with HyperLogLog++ precision

## References

### Documentation
- [SQL/PPL Functions Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/functions/): Official function reference
- [OpenSearch Spark Collection Functions](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/ppl-lang/functions/ppl-collection.md): Lambda function reference

### Pull Requests
| PR | Description |
|----|-------------|
| [#3559](https://github.com/opensearch-project/sql/pull/3559) | Add JSON functions |
| [#3584](https://github.com/opensearch-project/sql/pull/3584) | Add lambda function and array related functions |
| [#3574](https://github.com/opensearch-project/sql/pull/3574) | Implement cryptographic hash UDFs |
| [#3640](https://github.com/opensearch-project/sql/pull/3640) | Add earliest and latest condition functions |
| [#3654](https://github.com/opensearch-project/sql/pull/3654) | Add DISTINCT_COUNT_APPROX function |
| [#3653](https://github.com/opensearch-project/sql/pull/3653) | Support merging object-type fields from multiple indices |
| [#3663](https://github.com/opensearch-project/sql/pull/3663) | Support match_only_text field type |
| [#3698](https://github.com/opensearch-project/sql/pull/3698) | Switch percentile to MergingDigest algorithm |

### Issues (Design / RFC)
- [Issue #3573](https://github.com/opensearch-project/sql/issues/3573): Cryptographic hash functions request
- [Issue #3575](https://github.com/opensearch-project/sql/issues/3575): Lambda and array functions request
- [Issue #3565](https://github.com/opensearch-project/sql/issues/3565): JSON functions request
- [Issue #3639](https://github.com/opensearch-project/sql/issues/3639): Earliest/latest functions request
- [Issue #3353](https://github.com/opensearch-project/sql/issues/3353): Approximate distinct count request
- [Issue #3625](https://github.com/opensearch-project/sql/issues/3625): Object field merging request
- [Issue #3655](https://github.com/opensearch-project/sql/issues/3655): match_only_text support request
- [Issue #3697](https://github.com/opensearch-project/sql/issues/3697): Percentile algorithm alignment

## Related Feature Report

- Full feature documentation
