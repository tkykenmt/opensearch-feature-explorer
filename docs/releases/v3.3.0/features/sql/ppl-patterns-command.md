# PPL Patterns Command Enhancements

## Summary

OpenSearch v3.3.0 enhances the PPL `patterns` command with two key improvements: adding `sample_logs` output field to aggregation results for backward compatibility with V2 engine, and introducing a `show_numbered_token` option to control the output format of variable placeholders. These changes improve usability and provide more flexibility in log pattern analysis.

## Details

### What's New in v3.3.0

1. **sample_logs Output Field**: The `patterns` command in aggregation mode now includes `sample_logs` in the output, matching the V2 engine behavior. This field contains sample log messages that match each detected pattern.

2. **show_numbered_token Option**: A new `show_numbered_token` parameter allows users to choose between numbered token format (`<token1>`, `<token2>`) and standard wildcard format (`<*>`).

3. **Bug Fix for Continuous Wildcards**: Fixed an issue where the Brain algorithm could generate patterns with continuous variable placeholders like `<*><*><*>` instead of merging them into a single `<*>`.

### Technical Changes

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `show_numbered_token` | Controls whether to output numbered tokens (`<token1>`) or standard wildcards (`<*>`) | `false` |
| `plugins.ppl.pattern.show.numbered.token` | Cluster setting for default show_numbered_token value | `false` |

#### Output Format Changes

**Default Output (show_numbered_token=false)**:
- Pattern field uses `<*>` placeholders
- No `tokens` field in output
- Compatible with V2 engine format

**Numbered Token Output (show_numbered_token=true)**:
- Pattern field uses `<token1>`, `<token2>`, etc.
- Includes `tokens` field mapping token names to extracted values
- Useful for detailed variable extraction

### Usage Example

**Basic aggregation mode (default format)**:
```sql
source=logs | patterns message mode=aggregation | fields patterns_field, pattern_count, sample_logs
```

Output:
```
+-----------------------------------------------+---------------+---------------------------+
| patterns_field                                | pattern_count | sample_logs               |
+-----------------------------------------------+---------------+---------------------------+
| <*IP*> - <*> [<*>/Sep/<*>:<*>:<*>:<*> <*>]... | 4             | [log1, log2, log3, log4]  |
+-----------------------------------------------+---------------+---------------------------+
```

**With numbered tokens**:
```sql
source=logs | patterns message mode=aggregation show_numbered_token=true | fields patterns_field, pattern_count, tokens
```

Output:
```
+-------------------------------------------------------+---------------+----------------------------------+
| patterns_field                                        | pattern_count | tokens                           |
+-------------------------------------------------------+---------------+----------------------------------+
| <token1> - <token2> [<token3>/Sep/<token4>:...]       | 4             | {'<token1>': ['ip1', 'ip2',...]} |
+-------------------------------------------------------+---------------+----------------------------------+
```

### Migration Notes

- Existing queries using `patterns` command will continue to work
- The default output format now uses `<*>` placeholders (V2-compatible)
- To get numbered tokens (previous Calcite default), add `show_numbered_token=true`
- The `sample_logs` field is now automatically included in aggregation mode

## Limitations

- The `show_numbered_token` option only affects Calcite engine output
- V2 engine always uses the standard `<*>` format

## References

### Documentation
- [PPL Commands Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/ppl/functions/): Official PPL commands reference

### Pull Requests
| PR | Description |
|----|-------------|
| [#4155](https://github.com/opensearch-project/sql/pull/4155) | Add sample_logs output field to patterns command aggregation result |
| [#4402](https://github.com/opensearch-project/sql/pull/4402) | Fix numbered token bug and make it optional output |

### Issues (Design / RFC)
- [Issue #4139](https://github.com/opensearch-project/sql/issues/4139): Feature request for sample_logs field
- [Issue #4364](https://github.com/opensearch-project/sql/issues/4364): Feature request for optional numbered tokens
- [Issue #4363](https://github.com/opensearch-project/sql/issues/4363): Bug report for continuous wildcards
- [Issue #4362](https://github.com/opensearch-project/sql/issues/4362): Related bug fix
- [Issue #4366](https://github.com/opensearch-project/sql/issues/4366): Related bug fix

## Related Feature Report

- [Full feature documentation](../../../../features/sql/ppl-patterns-command.md)
