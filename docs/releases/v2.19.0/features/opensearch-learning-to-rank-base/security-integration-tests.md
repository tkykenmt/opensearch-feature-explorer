---
tags:
  - opensearch-learning-to-rank-base
---
# Security Integration Tests

## Summary

Added support for running integration tests against an external OpenSearch cluster with the security plugin enabled. This infrastructure improvement enables testing the Learning to Rank plugin in secured environments, ensuring compatibility with authentication and authorization features.

## Details

### What's New in v2.19.0

This PR adds the ability to run integration tests against external OpenSearch clusters that have the security plugin enabled. Previously, integration tests could only run against local test clusters without security.

### Technical Changes

#### New Gradle Task

A new `integTestRemote` task was added to `build.gradle` for running tests against external clusters:

```groovy
task integTestRemote(type: RestIntegTestTask) {
    description = "Run integration tests from src/javaRestTest"
    testClassesDirs = sourceSets.javaRestTest.output.classesDirs
    classpath = sourceSets.javaRestTest.runtimeClasspath

    systemProperty 'tests.security.manager', 'false'
    systemProperty "https", System.getProperty("https")
    systemProperty "user", System.getProperty("user")
    systemProperty "password", System.getProperty("password")
}
```

#### System Properties

The following system properties are now supported for secure cluster testing:

| Property | Description |
|----------|-------------|
| `https` | Enable HTTPS connection to the cluster |
| `user` | Username for authentication |
| `password` | Password for authentication |

#### Spotless Integration

The PR also adds the Spotless code formatting plugin to the build:

```groovy
plugins {
    id 'com.diffplug.spotless' version '6.23.0'
}

spotless {
    java {
        removeUnusedImports()
        importOrder 'java', 'javax', 'org', 'com'
        eclipse().configFile rootProject.file('.eclipseformat.xml')
    }
}
```

### Usage

To run integration tests against a secured external cluster:

```bash
./gradlew integTestRemote -Dhttps=true -Duser=admin -Dpassword=<password>
```

## Limitations

- Requires manual setup of the external cluster with security plugin
- Test credentials must be provided via system properties

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#122](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/122) | [Backport to 2.x] Support Integration Tests against an external test cluster with security plugin enabled | [#120](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/120) |
| [#121](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/121) | Support Integration Tests against an external test cluster with security plugin enabled (main) | [#120](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/120) |
