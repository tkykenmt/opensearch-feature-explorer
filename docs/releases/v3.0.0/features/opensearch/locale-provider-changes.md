---
tags:
  - search
---

# Locale Provider Changes

## Summary

OpenSearch v3.0.0 changes the default locale provider from COMPAT to CLDR (Common Locale Data Repository). This change prepares OpenSearch for future JDK versions where the COMPAT provider will be removed, and aligns with the JDK's default behavior since JDK 9.

## Details

### What's New in v3.0.0

The locale provider setting `java.locale.providers` has been changed from `SPI,COMPAT` to `SPI,CLDR` across all OpenSearch components:

- JVM options for OpenSearch runtime
- Gradle test configuration
- IDE run configurations

### Technical Changes

#### Background

Starting from JDK 21, a deprecation warning appears when using the COMPAT locale provider:

```
WARNING: COMPAT locale provider will be removed in a future release
```

The COMPAT provider was maintained for backward compatibility with JDK 8's locale data. Since JDK 9, CLDR has been the default locale data source.

#### Changed Files

| File | Change |
|------|--------|
| `SystemJvmOptions.java` | Changed `-Djava.locale.providers=SPI,COMPAT` to `SPI,CLDR` |
| `OpenSearchTestBasePlugin.java` | Updated test system property to use CLDR |
| `gradle/ide.gradle` | Updated IntelliJ run configuration |

#### Locale Data Differences

CLDR locale data has minor differences from COMPAT. For example, German (`de`) locale short names for days and months include periods in CLDR:

| Format | COMPAT | CLDR |
|--------|--------|------|
| Wednesday (short) | `Mi` | `Mi.` |
| Thursday (short) | `Do` | `Do.` |
| December (short) | `Dez` | `Dez.` |

### Migration Notes

If your application uses locale-specific date parsing with custom formats, you may need to update date patterns to account for CLDR formatting differences:

```java
// Before (COMPAT format for German locale)
"Mi, 06 Dez 2000 02:55:00 -0800"

// After (CLDR format for German locale)
"Mi., 06 Dez. 2000 02:55:00 -0800"
```

## Limitations

- Applications relying on exact locale-specific string matching may need updates
- Custom date formats using locale-specific day/month names should be tested

## References

### Documentation
- [JDK-8305402](https://bugs.openjdk.org/browse/JDK-8305402): COMPAT locale provider removal notice

### Blog Posts
- [Blog: How to start contributing to OpenSearch](https://opensearch.org/blog/how-to-start-contributing-to-opensearch-a-beginners-guide-based-on-my-journey/): Contributor journey including this fix

### Pull Requests
| PR | Description |
|----|-------------|
| [#14345](https://github.com/opensearch-project/OpenSearch/pull/14345) | Changed locale provider from COMPAT to CLDR |

### Issues (Design / RFC)
- [Issue #11550](https://github.com/opensearch-project/OpenSearch/issues/11550): COMPAT locale provider deprecation warning

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/locale-provider.md)
