---
tags:
  - domain/search
  - component/server
  - ml
  - search
---
# Learning to Rank Fixes

## Summary

OpenSearch v3.3.0 includes several build infrastructure and test stability improvements for the Learning to Rank plugin. These changes focus on Gradle 9 compatibility, improved floating-point comparison in tests, log4j dependency fixes, code coverage reporting, and spotless plugin upgrades.

## Details

### What's New in v3.3.0

This release addresses build and test infrastructure issues that improve plugin stability and maintainability:

1. **Log4j Dependency Fix** - Removed log4j from the plugin JAR to prevent "jar hell" conflicts when bundled with OpenSearch
2. **Gradle 9 Compatibility** - Updated environment variable syntax for Sonatype credentials
3. **Hybrid Float Comparison** - Improved test reliability with a hybrid approach to floating-point assertions
4. **Code Coverage** - Added JaCoCo code coverage report generation to CI
5. **Spotless Plugin Upgrade** - Updated to version 6.25.0 with build deprecation fixes

### Technical Changes

#### Log4j Exclusion (PR #226)

The plugin was incorrectly bundling log4j in its JAR, causing conflicts when OpenSearch itself is bundled:

```gradle
configurations {
  runtimeClasspath {
    exclude group: 'org.apache.logging.log4j', module: 'log4j-core'
    exclude group: 'org.apache.logging.log4j', module: 'log4j-api'
    exclude group: 'org.apache.logging.log4j', module: 'log4j-jul'
  }
}
```

#### Gradle 9 Environment Variable Syntax (PR #219)

Updated from deprecated `$System.env.VARIABLE` syntax to `System.getenv()`:

```gradle
// Before (deprecated in Gradle 9)
credentials {
    username "$System.env.SONATYPE_USERNAME"
    password "$System.env.SONATYPE_PASSWORD"
}

// After (Gradle 9 compatible)
credentials {
    username System.getenv("SONATYPE_USERNAME")
    password System.getenv("SONATYPE_PASSWORD")
}
```

#### Hybrid Float Comparison (PR #221)

Replaced simple ULP-based comparison with a hybrid approach for more reliable test assertions:

```java
// Tuned hybrid assertion parameters
private static final double ABS_FLOOR = 1e-4;
private static final double RELATIVE_TOLERANCE = 1e-2;
private static final int ULP_MULTIPLIER = 128;

// Hybrid comparison: max(ABS_FLOOR, max(REL_TOL * |mag|, ULP_MULT * ulp(expected)))
final double mag = Math.max(Math.abs((double) modelScore), Math.abs((double) queryScore));
final double ulp = Math.ulp((double) modelScore);
final double delta = Math.max(ABS_FLOOR, Math.max(RELATIVE_TOLERANCE * mag, ULP_MULTIPLIER * ulp));
```

This approach is based on the [C++ Boost math library](https://www.boost.org/doc/libs/boost_1_75_0/libs/math/doc/html/math_toolkit/float_comparison.html) recommendations for floating-point comparison.

#### Code Coverage (PR #228)

Added JaCoCo plugin for code coverage reporting:

```gradle
plugins {
    id 'jacoco'
}

jacocoTestReport {
    dependsOn test
    reports {
        xml.required = true
        html.required = true
        csv.required = false
    }
}
```

CI workflow updated to generate and upload coverage reports to Codecov.

#### Build Modernization (PR #222)

- Upgraded spotless plugin from 6.23.0 to 6.25.0
- Updated task definitions to use `tasks.register()` instead of deprecated syntax
- Updated test cluster configuration to use `testClusters.register()`
- Fixed deprecation warnings in Gradle build

## Limitations

- These are infrastructure changes only; no functional changes to the LTR plugin itself

## References

### Documentation
- [Learning to Rank Documentation](https://docs.opensearch.org/3.0/search-plugins/ltr/index/)
- [C++ Boost Float Comparison](https://www.boost.org/doc/libs/boost_1_75_0/libs/math/doc/html/math_toolkit/float_comparison.html): Reference for hybrid comparison approach

### Pull Requests
| PR | Description |
|----|-------------|
| [#226](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/226) | Fix bad inclusion of log4j in plugin JAR |
| [#219](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/219) | Update System.env syntax for Gradle 9 compatibility |
| [#228](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/228) | Add code coverage report generation |
| [#221](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/221) | Hybrid method for float comparison in assertions |
| [#222](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/222) | Upgrade spotless plugin and address build deprecations |

### Issues (Design / RFC)
- [GitHub Issue #227](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/227): Code coverage request

## Related Feature Report

- [Full feature documentation](../../../../features/learning/learning-to-rank.md)
