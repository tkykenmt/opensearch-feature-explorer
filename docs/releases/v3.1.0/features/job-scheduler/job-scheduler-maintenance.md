# Job Scheduler Maintenance

## Summary

OpenSearch v3.1.0 includes maintenance updates for the Job Scheduler plugin, focusing on version increment and removal of the Guava dependency. The Guava removal reduces potential jar hell and dependency conflicts for plugins that extend Job Scheduler, such as SQL, ML Commons, and others.

## Details

### What's New in v3.1.0

This release contains two maintenance changes:

1. **Version Increment**: Updated plugin version to 3.1.0-SNAPSHOT for the new release cycle
2. **Guava Dependency Removal**: Removed Google Guava library dependency to prevent jar hell issues

### Technical Changes

#### Guava Dependency Removal

The Guava library was removed from Job Scheduler to address dependency conflicts that occurred in extending plugins. This change:

- Removes `com.google.guava:guava` dependency from `build.gradle`
- Removes `com.google.guava:failureaccess` dependency
- Removes `com.google.googlejavaformat:google-java-format` dependency (which had Guava exclusion)
- Replaces `ImmutableList.of()` and `ImmutableMap.of()` with Java's native `List.of()` and `Map.of()`

#### Files Changed

| File | Change |
|------|--------|
| `build.gradle` | Removed Guava dependencies and resolution strategy |
| `JobSchedulerPlugin.java` | Replaced `ImmutableList` with `List.of()` |
| `RestGetJobDetailsAction.java` | Replaced `ImmutableList` with `List.of()` |
| `RestGetLockAction.java` | Replaced `ImmutableList` with `List.of()` |
| `RestReleaseLockAction.java` | Replaced `ImmutableList` with `List.of()` |
| Test files | Replaced `ImmutableMap` with `Map.of()` |

#### Code Changes

Before (using Guava):
```java
import com.google.common.collect.ImmutableList;

@Override
public List<Route> routes() {
    return ImmutableList.of(
        new Route(GET, String.format(Locale.ROOT, "%s/%s", JS_BASE_URI, "_lock"))
    );
}
```

After (using Java standard library):
```java
@Override
public List<Route> routes() {
    return List.of(
        new Route(GET, String.format(Locale.ROOT, "%s/%s", JS_BASE_URI, "_lock"))
    );
}
```

### Migration Notes

This is a transparent change for users. Plugin developers extending Job Scheduler will benefit from reduced dependency conflicts without any code changes required.

## Limitations

- No functional changes in this release
- This is a maintenance-only release for Job Scheduler

## References

### Documentation
- [Job Scheduler Documentation](https://docs.opensearch.org/3.1/monitoring-your-cluster/job-scheduler/index/)
- [v3.1.0 Release Notes](https://github.com/opensearch-project/job-scheduler/blob/main/release-notes/opensearch-job-scheduler.release-notes-3.1.0.0.md)

### Pull Requests
| PR | Description |
|----|-------------|
| [#766](https://github.com/opensearch-project/job-scheduler/pull/766) | Increment version to 3.1.0-SNAPSHOT |
| [#773](https://github.com/opensearch-project/job-scheduler/pull/773) | Remove guava dependency |

### Issues (Design / RFC)
- [Issue #18113](https://github.com/opensearch-project/OpenSearch/issues/18113): Remove Guava from plugins

## Related Feature Report

- [Full feature documentation](../../../../features/job-scheduler/job-scheduler.md)
