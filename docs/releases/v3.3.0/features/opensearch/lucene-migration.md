# Lucene Migration

## Summary

This release migrates deprecated usages of Lucene's `Operations#union(Automaton, Automaton)` method to the non-deprecated `Operations#union(Collection<Automaton>)` variant. This is a code maintenance change that ensures OpenSearch remains compatible with future Lucene versions while preserving existing behavior.

## Details

### What's New in v3.3.0

The deprecated two-argument `Operations#union` method from Apache Lucene's automaton utilities has been replaced with the collection-based variant across multiple OpenSearch components.

### Technical Changes

#### API Migration

The Lucene `Operations` class provides automaton manipulation utilities. The two-argument union method was deprecated in favor of a more flexible collection-based approach:

| Old API (Deprecated) | New API |
|---------------------|---------|
| `Operations.union(Automaton, Automaton)` | `Operations.union(Collection<Automaton>)` |

#### Modified Components

| Component | File | Change |
|-----------|------|--------|
| AutomatonQueries | `server/src/main/java/org/opensearch/common/lucene/search/AutomatonQueries.java` | Updated `toCaseInsensitiveChar()` to use `Arrays.asList()` wrapper |
| XContentMapValues | `server/src/main/java/org/opensearch/common/xcontent/support/XContentMapValues.java` | Refactored `makeMatchDotsInFieldNames()` to use collection-based union |
| SystemIndices | `server/src/main/java/org/opensearch/indices/SystemIndices.java` | Simplified `buildCharacterRunAutomaton()` using stream collection |

### Code Changes

#### AutomatonQueries.java

```java
// Before (deprecated)
result = Operations.union(case1, Automata.makeChar(altCase));

// After
result = Operations.union(Arrays.asList(case1, Automata.makeChar(altCase)));
```

#### XContentMapValues.java

```java
// Before (deprecated)
return Operations.determinize(
    Operations.union(automaton, Operations.concatenate(...)),
    Operations.DEFAULT_DETERMINIZE_WORK_LIMIT
);

// After
Automaton automatonMatchingFields = Operations.concatenate(
    Arrays.asList(automaton, Automata.makeChar('.'), Automata.makeAnyString())
);
return Operations.determinize(
    Operations.union(Arrays.asList(automaton, automatonMatchingFields)),
    Operations.DEFAULT_DETERMINIZE_WORK_LIMIT
);
```

#### SystemIndices.java

```java
// Before (deprecated)
Optional<Automaton> automaton = descriptors.stream()
    .map(descriptor -> Regex.simpleMatchToAutomaton(descriptor.getIndexPattern()))
    .reduce(Operations::union);
return new CharacterRunAutomaton(
    Operations.determinize(automaton.orElse(Automata.makeEmpty()), ...)
);

// After
List<Automaton> automatons = descriptors.stream()
    .map(descriptor -> Regex.simpleMatchToAutomaton(descriptor.getIndexPattern()))
    .collect(Collectors.toList());
return new CharacterRunAutomaton(
    Operations.determinize(Operations.union(automatons), ...)
);
```

### Migration Notes

This is an internal code change with no user-facing impact. No migration steps are required.

## Limitations

- This is a code maintenance change only
- No functional changes to automaton behavior
- No configuration changes required

## Related PRs

| PR | Description |
|----|-------------|
| [#19397](https://github.com/opensearch-project/OpenSearch/pull/19397) | Migrate deprecated usages of Operations#union |

## References

- [Apache Lucene Operations API](https://lucene.apache.org/core/10_0_0/core/org/apache/lucene/util/automaton/Operations.html): Lucene automaton operations documentation

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/lucene-upgrade.md)
