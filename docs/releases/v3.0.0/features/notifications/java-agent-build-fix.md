---
tags:
  - domain/observability
  - component/server
  - dashboards
  - ml
  - security
---
# Java Agent Build Fix

## Summary

This bugfix updates the Notifications plugin build configuration to support the Java Agent-based security model introduced in OpenSearch 3.0.0. The change adds the necessary Gradle configuration to run tests with the Java Agent, replacing the deprecated SecurityManager approach.

## Details

### What's New in v3.0.0

The Notifications plugin build was updated to work with OpenSearch's transition from Java SecurityManager to Java Agent for runtime security instrumentation. This change was required because SecurityManager is deprecated in JDK 17 and will be permanently disabled in JDK 24.

### Technical Changes

#### Build Configuration Updates

The `notifications/build.gradle` file was modified to:

1. Add an `agent` configuration for Java Agent dependencies
2. Create a `prepareAgent` task to copy agent JARs to the build directory
3. Configure all test tasks to run with the Java Agent

```groovy
configurations {
    agent
}

task prepareAgent(type: Copy) {
    from(configurations.agent)
    into "$buildDir/agent"
}

dependencies {
    agent "org.opensearch:opensearch-agent-bootstrap:${opensearch_version}"
    agent "org.opensearch:opensearch-agent:${opensearch_version}"
    agent "net.bytebuddy:byte-buddy:1.17.5"
}

tasks.withType(Test) {
    dependsOn prepareAgent
    jvmArgs += ["-javaagent:" + project.layout.buildDirectory.file("agent/opensearch-agent-${opensearch_version}.jar").get()]
}
```

#### Dependencies Added

| Dependency | Version | Purpose |
|------------|---------|---------|
| opensearch-agent-bootstrap | ${opensearch_version} | Agent bootstrap classes |
| opensearch-agent | ${opensearch_version} | Main Java Agent implementation |
| byte-buddy | 1.17.5 | Bytecode manipulation library |

### Migration Notes

Plugin developers maintaining forks or custom builds of the Notifications plugin should:

1. Update their `build.gradle` to include the agent configuration
2. Ensure JDK 21+ is used for building and testing
3. Run tests to verify compatibility with the Java Agent

## Limitations

- Requires JDK 21 or later
- Tests must run with the Java Agent enabled
- Legacy SecurityManager-based security checks are no longer supported

## References

### Documentation
- [PR #17861](https://github.com/opensearch-project/OpenSearch/pull/17861): Core OpenSearch SecurityManager replacement

### Pull Requests
| PR | Description |
|----|-------------|
| [#1013](https://github.com/opensearch-project/notifications/pull/1013) | Fix build due to phasing off SecurityManager usage in favor of Java Agent |

### Issues (Design / RFC)
- [Issue #16634](https://github.com/opensearch-project/OpenSearch/issues/16634): META - Replace Java Security Manager
- [Issue #17662](https://github.com/opensearch-project/OpenSearch/issues/17662): Phase off SecurityManager usage in favor of Java Agent

## Related Feature Report

- JDK 21 & Java Agent Migration
