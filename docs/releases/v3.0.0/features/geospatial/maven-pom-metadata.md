---
tags:
  - search
---

# Maven POM Metadata Fix

## Summary

This bugfix ensures that license, description, and developer information are properly persisted in Maven POM files when publishing the Geospatial plugin artifacts to Maven Central. Previously, these required metadata fields were missing, causing Nexus staging validation failures.

## Details

### What's New in v3.0.0

The Geospatial plugin's Gradle build configuration was updated to properly include required Maven Central metadata in all published POM files.

### Technical Changes

#### Problem

When publishing to Maven Central, the Nexus staging rules require POM files to include:
- Project description
- License information
- Developer information

The existing build configuration only applied these fields to specific publications, not all artifacts.

#### Solution

Changed the publication configuration from `pluginZip(MavenPublication)` to `all` clause, ensuring metadata is applied to all published artifacts. The fix uses `pom.withXml` to append XML nodes for:

- `inceptionYear`: 2021
- `licenses`: Apache License 2.0
- `developers`: OpenSearch project information

#### Affected Artifacts

| Artifact | Group ID |
|----------|----------|
| opensearch-geospatial | org.opensearch |
| geospatial-client | org.opensearch |
| geospatial | org.opensearch.plugin |
| opensearch-geospatial | org.opensearch.plugin |

#### Build Configuration Changes

```groovy
// Before: Only applied to pluginZip publication
publications {
    pluginZip(MavenPublication) {
        pom {
            licenses { ... }
            developers { ... }
        }
    }
}

// After: Applied to all publications via withXml
publications {
    all {
        pom {
            name = pluginName
            description = pluginDescription
        }
        pom.withXml { XmlProvider xml ->
            Node node = xml.asNode()
            node.appendNode('inceptionYear', '2021')
            
            Node license = node.appendNode('licenses').appendNode('license')
            license.appendNode('name', "The Apache License, Version 2.0")
            license.appendNode('url', "http://www.apache.org/licenses/LICENSE-2.0.txt")
            
            Node developer = node.appendNode('developers').appendNode('developer')
            developer.appendNode('name', 'OpenSearch')
            developer.appendNode('url', 'https://github.com/opensearch-project/geospatial')
        }
    }
}
```

### Verification

After the fix, the following POM files contain proper metadata:
- `~/.m2/repository/org/opensearch/opensearch-geospatial/{version}/opensearch-geospatial-{version}.pom`
- `~/.m2/repository/org/opensearch/geospatial-client/{version}/geospatial-client-{version}.pom`
- `~/.m2/repository/org/opensearch/plugin/geospatial/{version}/geospatial-{version}.pom`
- `~/.m2/repository/org/opensearch/plugin/opensearch-geospatial/{version}/opensearch-geospatial-{version}.pom`

## Limitations

- This is a build/release infrastructure fix with no runtime impact
- Only affects Maven artifact publishing

## References

### Documentation
- [Job Scheduler build.gradle](https://github.com/opensearch-project/job-scheduler/blob/main/build.gradle): Reference implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#732](https://github.com/opensearch-project/geospatial/pull/732) | Persist licenses and developer fields in pom file |

### Issues (Design / RFC)
- [Issue #731](https://github.com/opensearch-project/geospatial/issues/731): Missing necessary license, description, developer information in maven pom

## Related Feature Report

- [Full feature documentation](../../../features/geospatial/geospatial-plugin.md)
