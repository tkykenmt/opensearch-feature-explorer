# Build Infrastructure (Gradle/JDK)

## Summary

OpenSearch maintains a coordinated build infrastructure across its ecosystem of repositories, ensuring consistent Gradle versions, JDK support, and CI/CD practices. This infrastructure enables reliable builds, comprehensive testing, and streamlined release processes across 50+ repositories.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Build Infrastructure"
        GW[Gradle Wrapper] --> GB[Gradle Build]
        GB --> UT[Unit Tests]
        GB --> IT[Integration Tests]
        IT --> SN[Single Node]
        IT --> MN[Multi-Node]
        GB --> CC[Code Coverage]
        CC --> CV[Codecov]
    end
    
    subgraph "CI/CD Pipeline"
        PR[Pull Request] --> GC[Gradle Check]
        GC --> GB
        GC --> PUB[Maven Publish]
        PUB --> SNAP[Snapshots]
        PUB --> REL[Releases]
    end
    
    subgraph "Runtime Environment"
        JDK[JDK Version] --> GB
        DEP[Dependencies] --> GB
    end
```

### Components

| Component | Description |
|-----------|-------------|
| Gradle Wrapper | Ensures consistent Gradle version across all builds |
| JDK Configuration | CI workflows configured for specific JDK versions |
| Maven Publishing | Snapshot and release artifact publishing |
| Code Coverage | JaCoCo integration with Codecov reporting |
| Integration Tests | Single and multi-node test configurations |

### Configuration

| Setting | Description | Current Value |
|---------|-------------|---------------|
| Gradle Version | Build tool version | 8.14.3 |
| JDK (CI) | CI workflow JDK version | 24 |
| JDK (Runtime) | Minimum runtime JDK | 21 |
| Kotlin Version | Kotlin plugin version | 2.2.0 |
| Codecov | Code coverage reporting | Enabled |

### Usage Example

```groovy
// build.gradle - Gradle wrapper configuration
wrapper {
    gradleVersion = '8.14.3'
    distributionType = Wrapper.DistributionType.ALL
}

// CI workflow - JDK configuration
// .github/workflows/ci.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-java@v4
        with:
          java-version: '24'
          distribution: 'temurin'
```

### Multi-Node Testing

```yaml
# Example multi-node integration test workflow
jobs:
  multi-node-test:
    runs-on: ubuntu-latest
    steps:
      - name: Run multi-node integration tests
        run: ./gradlew integTestMultiNode
```

## Limitations

- JDK 24 is used for CI builds; production deployments may use different JDK versions
- Some third-party dependencies may require updates for full JDK 24 compatibility
- Gradle version upgrades may require plugin compatibility updates

## Related PRs

| Version | PR | Repository | Description |
|---------|-----|------------|-------------|
| v3.2.0 | [#2792](https://github.com/opensearch-project/k-NN/pull/2792) | k-NN | Bump JDK to 24, Gradle to 8.14 |
| v3.2.0 | [#2828](https://github.com/opensearch-project/k-NN/pull/2828) | k-NN | Bump Gradle to 8.14.3 |
| v3.2.0 | [#3983](https://github.com/opensearch-project/ml-commons/pull/3983) | ml-commons | Gradle 8.14, JDK 24 |
| v3.2.0 | [#4026](https://github.com/opensearch-project/ml-commons/pull/4026) | ml-commons | Lombok update for JDK 24 |
| v3.2.0 | [#1445](https://github.com/opensearch-project/index-management/pull/1445) | index-management | Gradle 8.14, Kotlin 2.2.0, JDK 24 |
| v3.2.0 | [#1320](https://github.com/opensearch-project/neural-search/pull/1320) | neural-search | Multi-node integration tests |
| v3.2.0 | [#1911](https://github.com/opensearch-project/alerting/pull/1911) | alerting | Gradle 8.14, JDK 24 |

## References

- [OpenSearch automated build system](https://opensearch.org/blog/public-jenkins/): Public Jenkins infrastructure
- [Gradle Documentation](https://docs.gradle.org/): Official Gradle documentation
- [OpenJDK](https://openjdk.org/): OpenJDK project

## Change History

- **v3.2.0** (2025): Gradle 8.14/8.14.3, JDK 24 CI support, multi-node testing, Codecov integration, Maven endpoint updates
