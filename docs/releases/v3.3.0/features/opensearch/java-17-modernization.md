# Java 17 Modernization

## Summary

OpenSearch v3.3.0 introduces Java 17 language modernization improvements, refactoring legacy `if-else` chains to use Java 17 pattern matching switch expressions and removing the outdated Java version cap on forbidden APIs enforcement. These changes improve code readability, maintainability, and ensure proper enforcement of Java deprecation warnings.

## Details

### What's New in v3.3.0

This release includes two key improvements for Java 17 modernization:

1. **Pattern Matching Switch Expressions**: Refactored multiple `if-else` chains using `instanceof` checks to modern Java 17 pattern matching `switch` statements
2. **Forbidden APIs Update**: Removed the Java 14 version cap on forbidden APIs plugin, enabling proper deprecation enforcement for Java 15+

### Technical Changes

#### Pattern Matching Switch Refactoring

The following core files were refactored to use Java 17 pattern matching:

| File | Changes |
|------|---------|
| `Numbers.java` | `toLongExact`, `toBigIntegerExact` methods |
| `ExceptionsHelper.java` | Exception handling methods (`convertToRuntime`, `status`, `summaryMessage`) |
| `NestedHelper.java` | Query matching methods (`mightMatchNestedDocs`, `mightMatchNonNestedDocs`) |
| `ValueSource.java` | Value wrapping logic in `wrap()` method |
| `SearchSortValuesAndFormats.java` | Sort value formatting |
| `BulkItemResponse.java` | Response type serialization |
| `DocWriteRequest.java` | Request serialization methods |
| `BytesReference.java` | Stream type handling |
| `LoggerMessageFormat.java` | Primitive array type handling |
| `NioSelectorGroup.java` | Exception handling |
| `SocketChannelContext.java` | Connection exception handling |

#### Code Example: Before and After

**Before (if-else chain):**
```java
public static long toLongExact(Number n) {
    if (n instanceof Byte || n instanceof Short || n instanceof Integer || n instanceof Long) {
        return n.longValue();
    } else if (n instanceof Float || n instanceof Double) {
        double d = n.doubleValue();
        if (d != Math.round(d)) {
            throw new IllegalArgumentException(n + " is not an integer value");
        }
        return n.longValue();
    } else if (n instanceof BigDecimal) {
        return ((BigDecimal) n).toBigIntegerExact().longValueExact();
    } else if (n instanceof BigInteger) {
        return ((BigInteger) n).longValueExact();
    } else {
        throw new IllegalArgumentException("Cannot check whether [" + n + "] ...");
    }
}
```

**After (pattern matching switch):**
```java
public static long toLongExact(Number n) {
    return switch (n) {
        case Byte b -> b.longValue();
        case Short s -> s.longValue();
        case Integer i -> i.longValue();
        case Long l -> l;
        case Float f -> {
            double d = f.doubleValue();
            if (d != Math.round(d)) {
                throw new IllegalArgumentException(f + " is not an integer value");
            }
            yield f.longValue();
        }
        case Double d -> {
            if (d != Math.round(d)) {
                throw new IllegalArgumentException(d + " is not an integer value");
            }
            yield d.longValue();
        }
        case BigDecimal bd -> bd.toBigIntegerExact().longValueExact();
        case BigInteger bi -> bi.longValueExact();
        default -> throw new IllegalArgumentException("Cannot check whether [" + n + "] ...");
    };
}
```

#### Forbidden APIs Plugin Update

| Change | Details |
|--------|---------|
| Plugin version | Updated from 3.8 to 3.9 |
| Java version cap | Removed Java 14 cap that prevented deprecation enforcement |
| Security Manager APIs | Added warnings for deprecated `AccessController`, `SecurityManager`, `Policy` usage |

The forbidden APIs plugin now properly enforces Java deprecations for all Java versions, including Java 15+. Previously, a check capped the target compatibility at Java 14, meaning deprecation warnings from the past 5 years were not being enforced.

#### Deprecated API Warnings

The following deprecated Security Manager APIs are now set to warn globally:

- `java.security.AccessController`
- `java.security.AccessControlContext`
- `java.lang.System#getSecurityManager()`
- `java.lang.SecurityManager`
- `java.security.Policy`

#### Additional Deprecation Fixes

Several deprecated API usages were fixed across the codebase:

| Deprecated API | Replacement |
|----------------|-------------|
| `new URL(String)` | `URI.create(String).toURL()` |
| `X509Certificate.getSubjectDN()` | `X509Certificate.getSubjectX500Principal()` |
| `X509Certificate.getIssuerDN()` | `X509Certificate.getIssuerX500Principal()` |
| `Thread.getId()` | `Thread.threadId()` |
| `new Locale(String...)` | `new Locale.Builder().setLanguage(...).build()` |
| `Runtime.exec(String)` | `Runtime.exec(String[])` |

### Usage Example

Pattern matching switch expressions provide cleaner, more readable code:

```java
// Query type matching in NestedHelper
public boolean mightMatchNestedDocs(Query query) {
    return switch (query) {
        case ConstantScoreQuery csq -> mightMatchNestedDocs(csq.getQuery());
        case BoostQuery bq -> mightMatchNestedDocs(bq.getQuery());
        case MatchAllDocsQuery ignored -> true;
        case MatchNoDocsQuery ignored -> false;
        case TermQuery tq -> mightMatchNestedDocs(tq.getTerm().field());
        case TermInSetQuery tisq -> tisq.getTermsCount() > 0 && mightMatchNestedDocs(tisq.getField());
        case BooleanQuery bq -> {
            // Complex logic with yield
            yield bq.clauses().stream()
                .filter(BooleanClause::isRequired)
                .map(BooleanClause::query)
                .allMatch(this::mightMatchNestedDocs);
        }
        case null, default -> true;
    };
}
```

### Migration Notes

These changes are internal refactoring and do not affect the public API. No migration is required for users.

For plugin developers:
- If extending OpenSearch classes that were refactored, ensure your code is compatible with Java 17+
- Consider adopting pattern matching switch expressions in your own code for improved readability

## Limitations

- Pattern matching switch expressions require Java 17 or later
- The `ignored` pattern variable is used for cases where the matched value is not needed

## Related PRs

| PR | Description |
|----|-------------|
| [#18965](https://github.com/opensearch-project/OpenSearch/pull/18965) | Refactor if-else chains to use Java 17 pattern matching switch expressions |
| [#19163](https://github.com/opensearch-project/OpenSearch/pull/19163) | Remove cap on Java version used by forbidden APIs |

## References

- [Issue #17874](https://github.com/opensearch-project/OpenSearch/issues/17874): Feature request for Java 17 pattern matching
- [JEP 406](https://openjdk.org/jeps/406): Pattern Matching for switch (Preview)
- [JEP 441](https://openjdk.org/jeps/441): Pattern Matching for switch (Final)

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/java-17-modernization.md)
