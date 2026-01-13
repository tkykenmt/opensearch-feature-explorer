---
tags:
  - domain/infra
  - component/server
  - dashboards
  - ml
  - security
---
# Java Agent Build Fix

## Summary

This bugfix updates the Reporting plugin's build configuration to support the Java Agent-based security model introduced in OpenSearch 3.0. The change ensures that tests run correctly with the new Java Agent instead of the deprecated SecurityManager.

## Details

### What's New in v3.0.0

The Reporting plugin's Gradle build configuration has been updated to integrate with OpenSearch's Java Agent infrastructure. This is a required change as OpenSearch 3.0 phases out SecurityManager usage in favor of Java Agent-based runtime instrumentation.

### Technical Changes

#### Build Configuration Updates

The `build.gradle` file now includes:

1. **Agent Configuration**: New `agent` configuration for Java Agent dependencies
2. **PrepareAgent Task**: Copies agent JARs to the build directory
3. **Test JVM Arguments**: Configures tests to run with the Java Agent

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
    agent "net.bytebuddy:byte-buddy:${versions.bytebuddy}"
}

tasks.withType(Test) {
    dependsOn prepareAgent
    jvmArgs += ["-javaagent:" + project.layout.buildDirectory.file("agent/opensearch-agent-${opensearch_version}.jar").get()]
}
```

#### New Dependencies

| Dependency | Description |
|------------|-------------|
| opensearch-agent-bootstrap | Bootstrap agent for OpenSearch runtime |
| opensearch-agent | Main Java Agent for security instrumentation |
| byte-buddy | Bytecode manipulation library used by the agent |

### Migration Notes

Plugin developers maintaining forks or custom builds of the Reporting plugin should:

1. Update their `build.gradle` to include the agent configuration
2. Ensure JDK 21 is used for building and testing
3. Remove any SecurityManager-related code or configurations

## Limitations

- Requires JDK 21 or later
- Tests must run with the Java Agent enabled
- Not backward compatible with OpenSearch 2.x

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/reporting/): Reporting plugin documentation
- [PR #17861](https://github.com/opensearch-project/OpenSearch/pull/17861): Phase off SecurityManager usage in favor of Java Agent

### Pull Requests
| PR | Description |
|----|-------------|
| [#1085](https://github.com/opensearch-project/reporting/pull/1085) | Fix build due to phasing off SecurityManager usage in favor of Java Agent |

### Issues (Design / RFC)
- [Issue #16634](https://github.com/opensearch-project/OpenSearch/issues/16634): META - Replace Java Security Manager

## Related Feature Report

- Full feature documentation
