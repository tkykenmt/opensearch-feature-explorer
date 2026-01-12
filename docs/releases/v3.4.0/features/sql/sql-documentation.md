---
tags:
  - search
  - sql
---

# SQL Documentation

## Summary

This release includes multiple documentation improvements for the SQL/PPL plugin, focusing on standardizing PPL command documentation structure, fixing typos, adding examples, and enhancing function documentation. These changes improve the user experience by providing clearer, more consistent, and comprehensive documentation.

## Details

### What's New in v3.4.0

The documentation improvements in this release cover several areas:

1. **PPL Command Documentation Standardization** - Consistent section ordering across all PPL command files
2. **Typo Fixes** - Corrected typos in eventstats and other command documentation
3. **Enhanced Examples** - Added comprehensive examples for the `where` command
4. **Function Documentation** - Improved documentation for `isnull`/`isnotnull` and `json_valid` functions
5. **IP Datatype Documentation** - Added information about IP datatypes in search command

### Technical Changes

#### Documentation Structure Standardization

The PPL command documentation has been reorganized with a consistent structure:

| Section | Description |
|---------|-------------|
| Description | Clear explanation of command functionality |
| Syntax | Command syntax with parameter details |
| Optional sections | Behavior notes, configuration details, or usage guidance |
| Examples | Practical usage examples with expected output |
| Limitations | Known constraints or considerations |

#### Content Improvements

| Area | Change |
|------|--------|
| Version Information | Removed outdated version references to reduce maintenance overhead |
| Aggregation Functions | Extracted to dedicated functions file for better organization |
| Example Descriptions | Changed from "The example" to "This example" for consistency |
| Parameter Formatting | Standardized default value formatting with **Default:** notation |

### Documentation Files Updated

The following documentation files were updated:

- `docs/user/ppl/cmd/eventstats.rst` - Fixed typo (evenstats → eventstats)
- `docs/user/ppl/cmd/where.rst` - Added 7 new practical examples
- `docs/user/ppl/cmd/search.rst` - Added IP datatype information
- `docs/user/ppl/functions/condition.rst` - Enhanced `isnull`/`isnotnull` documentation
- `docs/user/ppl/functions/json.rst` - Added `json_valid` function documentation
- Multiple command files - Standardized structure and formatting

### Usage Example

The enhanced `where` command documentation now includes examples for:

```ppl
# Basic field comparison
source=accounts | where age > 30

# Pattern matching with LIKE
source=accounts | where firstname LIKE 'J%'

# Multiple conditions with AND
source=accounts | where age > 25 AND gender = 'M'

# IN operator for multiple values
source=accounts | where state IN ('CA', 'NY', 'TX')

# NULL value checks
source=accounts | where ISNULL(employer)

# Complex conditions with parentheses
source=accounts | where (age > 30 OR balance > 10000) AND gender = 'F'

# NOT operator for exclusion
source=accounts | where NOT state = 'CA'
```

## Limitations

- Documentation changes are in-repo RST files, not the official documentation website
- Some examples may require specific index configurations to run

## References

### Documentation
- [PPL Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/ppl/index/): Official PPL reference
- [SQL Plugin Repository](https://github.com/opensearch-project/sql): Source code and in-repo documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#4562](https://github.com/opensearch-project/sql/pull/4562) | Update PPL Command Documentation - Major standardization effort |
| [#4803](https://github.com/opensearch-project/sql/pull/4803) | Doc update for `json_valid` function |
| [#4724](https://github.com/opensearch-project/sql/pull/4724) | Enhance tests and doc for eval isnull/isnotnull functions |
| [#4686](https://github.com/opensearch-project/sql/pull/4686) | Update search.rst documentation for IP datatypes |
| [#4457](https://github.com/opensearch-project/sql/pull/4457) | Add more examples to the `where` command doc |
| [#4447](https://github.com/opensearch-project/sql/pull/4447) | Fix typo: evenstats → eventstats |

### Issues (Design / RFC)
- [Issue #4220](https://github.com/opensearch-project/sql/issues/4220): Documentation improvement tracking issue
- [Issue #4227](https://github.com/opensearch-project/sql/issues/4227): Where command examples request

## Related Feature Report

- [Full feature documentation](../../../../features/sql/ppl-documentation.md)
