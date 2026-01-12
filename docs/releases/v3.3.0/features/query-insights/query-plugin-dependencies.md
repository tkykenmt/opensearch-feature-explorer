---
tags:
  - performance
  - search
  - security
---

# Query Plugin Dependencies

## Summary

This release addresses critical security vulnerabilities in the Query Insights plugin by updating transitive dependencies. The fixes resolve CVE-2025-27820 (Apache HttpClient domain check bypass) and CVE-2025-48734 (Apache Commons BeanUtils improper access control).

## Details

### What's New in v3.3.0

Security dependency updates to address high-severity CVEs affecting the Query Insights plugin's transitive dependencies.

### Technical Changes

#### Dependency Updates

| Dependency | Previous Version | Updated Version | CVE Fixed |
|------------|------------------|-----------------|-----------|
| httpclient5 | 5.4.x | 5.4.4 | CVE-2025-27820 |
| httpcore5 | - | 5.3.4 | CVE-2025-27820 |
| httpcore5-h2 | - | 5.3.4 | CVE-2025-27820 |
| commons-beanutils | < 1.11.0 | 1.11.0 | CVE-2025-48734 |
| commons-beanutils2 | < 2.0.0-M2 | 2.0.0-M2 | CVE-2025-48734 |

#### CVE-2025-27820: Apache HttpClient Domain Check Bypass

- Severity: High (CVSS 7.5)
- A bug in PSL validation logic in Apache HttpClient 5.4.x disables domain checks
- Affects cookie management and host name verification
- Fixed by upgrading to httpclient5 5.4.3+

#### CVE-2025-48734: Apache Commons BeanUtils Improper Access Control

- Severity: High (CVSS 8.8)
- BeanIntrospector protection against classloader access via enum's declared class property was not enabled by default
- Could allow attackers to access the classloader through Java enum objects
- Fixed by upgrading to commons-beanutils 1.11.0 / commons-beanutils2 2.0.0-M2

#### Build Configuration Changes

The `build.gradle` file was updated to force specific dependency versions:

```groovy
configurations.all {
  resolutionStrategy {
    force("org.apache.httpcomponents.client5:httpclient5:5.4.4")
    force("org.apache.httpcomponents:httpcore:5.3.4")
    force("org.apache.httpcomponents.core5:httpcore5-h2:5.3.4")
    force("commons-beanutils:commons-beanutils:1.11.0")
    force("org.apache.commons:commons-beanutils2:2.0.0-M2")
  }
}
```

### Migration Notes

No migration required. These are transparent dependency updates that do not change the plugin's API or behavior.

## Limitations

- These fixes address transitive dependencies; direct usage of affected libraries should also be reviewed in custom implementations

## References

### Documentation
- [Apache HttpClient 5.4.x](https://hc.apache.org/httpcomponents-client-5.4.x/index.html): Official documentation
- [CVE-2025-27820](https://github.com/advisories/GHSA-73m2-qfq3-56cx): Apache HttpClient domain check bypass
- [CVE-2025-48734](https://github.com/advisories/GHSA-wxr5-93ph-8wr9): Apache Commons BeanUtils improper access control

### Pull Requests
| PR | Description |
|----|-------------|
| [#371](https://github.com/opensearch-project/query-insights/pull/371) | CVE-2025-27820 and CVE-2025-48734 fix (main) |
| [#375](https://github.com/opensearch-project/query-insights/pull/375) | Backport to 3.1 branch |

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights-dependencies.md)
