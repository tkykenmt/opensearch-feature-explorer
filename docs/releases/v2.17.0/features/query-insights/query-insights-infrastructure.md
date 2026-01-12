# Query Insights Infrastructure

## Summary

This release item adds code hygiene checks and fixes snapshot publishing configuration for the Query Insights plugin. These infrastructure improvements ensure code quality through automated Spotless and Checkstyle checks, and enable proper snapshot artifact publishing to the Sonatype repository.

## Details

### What's New in v2.17.0

Two infrastructure improvements were made to the Query Insights plugin:

1. **Code Hygiene Checks (PR #51)**: Added automated code quality enforcement through Spotless and Checkstyle integration
2. **Snapshot Publishing Configuration (PR #90)**: Fixed the Maven snapshot publishing workflow to properly publish plugin artifacts

### Technical Changes

#### Code Hygiene Checks

Added GitHub Actions workflow for automated code quality checks:

| Check | Tool | Purpose |
|-------|------|---------|
| Spotless | `com.diffplug.spotless` | Code formatting enforcement |
| Checkstyle | `checkstyle` | Code style validation |

**New Files Added:**
- `.github/workflows/code-hygiene.yml` - GitHub Actions workflow
- `config/checkstyle/checkstyle.xml` - Checkstyle configuration (Sun coding conventions)
- `config/formatterConfig.xml` - Eclipse formatter configuration for Spotless

**Spotless Configuration:**
```groovy
spotless {
  java {
    target fileTree('.') {
      include '**/*.java'
      exclude '**/build/**', '**/build-*/**'
    }
    removeUnusedImports()
    importOrder()
    eclipse().configFile rootProject.file('config/formatterConfig.xml')
    trimTrailingWhitespace()
    endWithNewline()
  }
}
```

**Checkstyle Rules Include:**
- Import ordering and unused import detection (error severity)
- Star import prevention
- Illegal import detection (e.g., `sun.*` packages)
- System.out.println detection
- Inclusive language enforcement (e.g., "master" → "cluster manager")

#### Snapshot Publishing Fix

Fixed the Maven publish workflow by:

1. Adding Snapshots repository configuration to `build.gradle`:
```groovy
repositories {
  maven {
    name = "Snapshots"
    url = "https://aws.oss.sonatype.org/content/repositories/snapshots"
    credentials {
      username "$System.env.SONATYPE_USERNAME"
      password "$System.env.SONATYPE_PASSWORD"
    }
  }
}
```

2. Simplifying `.github/workflows/maven-publish.yml` to only publish the plugin zip:
```yaml
# For JS plugin zip
./gradlew publishPluginZipPublicationToSnapshotsRepository
```

The previous workflow attempted to publish `ShadowPublication` and `NebulaPublication` which don't exist in this plugin.

### Usage Example

**Run code hygiene checks locally:**
```bash
# Run Spotless check
./gradlew spotlessCheck

# Apply Spotless formatting
./gradlew spotlessApply

# Run Checkstyle
./gradlew checkstyleMain checkstyleTest
```

### Migration Notes

No migration required. These are infrastructure-only changes that don't affect plugin functionality.

## Limitations

- Checkstyle severity is set to `ignore` by default for most rules, with specific rules (imports, System.out.println) set to `error`
- The code hygiene workflow runs on every push and pull request

## References

### Documentation
- [Query Insights Repository](https://github.com/opensearch-project/query-insights)

### Pull Requests
| PR | Description |
|----|-------------|
| [#51](https://github.com/opensearch-project/query-insights/pull/51) | Add code hygiene checks for query insights |
| [#90](https://github.com/opensearch-project/query-insights/pull/90) | Add configuration for publishing snapshot |

### Issues (Design / RFC)
- [Issue #7](https://github.com/opensearch-project/query-insights/issues/7): Set up GitHub Actions
- [Issue #72](https://github.com/opensearch-project/query-insights/issues/72): Snapshots not being published bug report

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights.md)
