---
tags:
  - domain/infra
  - component/server
  - search
---
# JDK 25 & Gradle 9.2 Upgrades

## Summary

OpenSearch v3.4.0 includes coordinated upgrades to Gradle 9.2 and JDK 25 across 24 plugin repositories. This maintenance effort ensures all plugins remain compatible with the latest build tooling and runtime environment used by OpenSearch core.

## Details

### What's New in v3.4.0

Following OpenSearch core's upgrade to Gradle 9.2 and JDK 25, all plugin repositories have been updated to maintain build compatibility:

- **Gradle 9.2.0/9.2.1**: Updated gradle-wrapper.properties and gradlew scripts
- **JDK 25**: Updated GitHub Actions CI workflows to test with JDK 25
- **Kotlin 2.2.0**: Some repositories also upgraded Kotlin plugin version

### Technical Changes

#### Files Modified

| File | Change |
|------|--------|
| `gradle/wrapper/gradle-wrapper.properties` | Updated distributionUrl to Gradle 9.2.x |
| `gradlew` / `gradlew.bat` | Updated wrapper scripts for Gradle 9.2 |
| `.github/workflows/*.yml` | Updated java matrix from `[21, 24]` to `[21, 25]` |
| `build.gradle` | Updated sourceCompatibility/targetCompatibility syntax |

#### Gradle Wrapper Changes

```properties
# Before
distributionUrl=https\://services.gradle.org/distributions/gradle-8.14.3-all.zip

# After
distributionUrl=https\://services.gradle.org/distributions/gradle-9.2.0-all.zip
distributionSha256Sum=16f2b95838c1ddcf7242b1c39e7bbbb43c842f1f1a1a0dc4959b6d4d68abcac3
```

#### CI Workflow Changes

```yaml
# Before
strategy:
  matrix:
    java: [21, 24]

# After
strategy:
  matrix:
    java: [21, 25]
```

#### Build.gradle Changes

```groovy
// Before (deprecated syntax)
plugins.withId('java') {
    sourceCompatibility = targetCompatibility = "21"
}

// After (Gradle 9.2 compatible)
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}
```

### Repositories Updated

| Repository | PRs |
|------------|-----|
| alerting | [#1993](https://github.com/opensearch-project/alerting/pull/1993), [#1995](https://github.com/opensearch-project/alerting/pull/1995) |
| anomaly-detection | [#1623](https://github.com/opensearch-project/anomaly-detection/pull/1623) |
| asynchronous-search | [#792](https://github.com/opensearch-project/asynchronous-search/pull/792) |
| common-utils | [#892](https://github.com/opensearch-project/common-utils/pull/892) |
| cross-cluster-replication | [#1605](https://github.com/opensearch-project/cross-cluster-replication/pull/1605) |
| custom-codecs | [#294](https://github.com/opensearch-project/custom-codecs/pull/294) |
| geospatial | [#816](https://github.com/opensearch-project/geospatial/pull/816) |
| index-management | [#1534](https://github.com/opensearch-project/index-management/pull/1534) |
| job-scheduler | [#864](https://github.com/opensearch-project/job-scheduler/pull/864) |
| k-NN | [#2984](https://github.com/opensearch-project/k-NN/pull/2984) |
| learning-to-rank | [#263](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/263) |
| ml-commons | [#4465](https://github.com/opensearch-project/ml-commons/pull/4465) |
| neural-search | [#1667](https://github.com/opensearch-project/neural-search/pull/1667) |
| notifications | [#1101](https://github.com/opensearch-project/notifications/pull/1101) |
| observability | [#1959](https://github.com/opensearch-project/observability/pull/1959) |
| performance-analyzer | [#896](https://github.com/opensearch-project/performance-analyzer/pull/896) |
| query-insights | [#486](https://github.com/opensearch-project/query-insights/pull/486) |
| reporting | [#1139](https://github.com/opensearch-project/reporting/pull/1139) |
| search-processor | [#319](https://github.com/opensearch-project/search-processor/pull/319) |
| security | [#1618](https://github.com/opensearch-project/security/pull/1618), [#5786](https://github.com/opensearch-project/security/pull/5786) |
| skills | [#675](https://github.com/opensearch-project/skills/pull/675) |
| system-templates | [#111](https://github.com/opensearch-project/opensearch-system-templates/pull/111) |
| user-behavior-insights | [#148](https://github.com/opensearch-project/user-behavior-insights/pull/148) |

## Limitations

- JDK 25 is used for CI testing; production deployments may use different JDK versions
- Some repositories use Gradle 9.2.0, others use 9.2.1 depending on merge timing
- Kotlin version upgrades were included in some but not all repositories

## References

### Documentation
- [Gradle 9.2 Release Notes](https://docs.gradle.org/9.2/release-notes.html): Official Gradle 9.2 release notes
- [JDK 25 Release](https://openjdk.org/projects/jdk/25/): OpenJDK 25 project page

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#2984](https://github.com/opensearch-project/k-NN/pull/2984) | k-NN | Gradle 9.2.0 and GitHub Actions JDK 25 Upgrade |
| [#1995](https://github.com/opensearch-project/alerting/pull/1995) | alerting | JDK upgrade to 25 and gradle upgrade to 9.2 |
| [#4465](https://github.com/opensearch-project/ml-commons/pull/4465) | ml-commons | Update JDK to 25 and Gradle to 9.2 |
| [#1667](https://github.com/opensearch-project/neural-search/pull/1667) | neural-search | Update to Gradle 9.2 and run CI checks with JDK 25 |
| [#1618](https://github.com/opensearch-project/security/pull/1618) | security | JDK upgrade to 25 and gradle upgrade to 9.2 |

### Issues (Design / RFC)
- [Issue #2976](https://github.com/opensearch-project/k-NN/issues/2976): k-NN Gradle/JDK upgrade tracking
- [Issue #1977](https://github.com/opensearch-project/alerting/issues/1977): Alerting Gradle/JDK upgrade tracking
- [Issue #4389](https://github.com/opensearch-project/ml-commons/issues/4389): ml-commons Gradle/JDK upgrade tracking

## Related Feature Report

- Full feature documentation
