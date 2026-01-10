# Version Bumps & Release Notes

## Summary

Version bumps and release notes are standard maintenance tasks performed across all OpenSearch repositories during each release cycle. These changes ensure consistent versioning across the project and provide documentation of changes for each release.

## Details

### Release Cycle Workflow

```mermaid
flowchart TB
    A[Development] --> B[Alpha]
    B --> C[Beta]
    C --> D[GA Release]
    D --> E[SNAPSHOT]
    
    subgraph "Version Examples"
        B1[3.0.0.0-alpha1]
        C1[3.0.0.0-beta1]
        D1[3.0.0.0]
        E1[3.0.0-SNAPSHOT]
    end
```

### Version String Format

OpenSearch plugins follow a consistent versioning scheme:

| Component | Format | Example |
|-----------|--------|---------|
| Major.Minor.Patch.Build | X.Y.Z.W | 3.0.0.0 |
| With Qualifier | X.Y.Z.W-qualifier | 3.0.0.0-alpha1 |
| SNAPSHOT | X.Y.Z-SNAPSHOT | 3.0.0-SNAPSHOT |

### Files Typically Modified

| File | Purpose |
|------|---------|
| `build.gradle` | Plugin version declaration |
| `gradle.properties` | Version properties |
| `release-notes/*.md` | Release documentation |
| `plugin-descriptor.properties` | Plugin metadata |

### Release Notes Structure

Each plugin maintains release notes in a standard format:

```
release-notes/
├── opensearch-{plugin}.release-notes-3.0.0.0.md
├── opensearch-{plugin}.release-notes-2.19.0.0.md
└── ...
```

## Limitations

- Version bumps are mechanical changes with no functional impact
- Release notes accuracy depends on PR descriptions and changelog entries
- Timing of version bumps must coordinate with release branch creation

## Related PRs

| Version | PR | Repository | Description |
|---------|-----|------------|-------------|
| v3.1.0 | [#1837](https://github.com/opensearch-project/alerting/pull/1837) | alerting | Auto-increment to 3.1.0-SNAPSHOT |
| v3.1.0 | [#1249](https://github.com/opensearch-project/alerting/pull/1249) | alerting | Upgrade Java to 21 for binary CI |
| v3.1.0 | [#1251](https://github.com/opensearch-project/alerting/pull/1251) | alerting | Increment to 3.1.0.0 |
| v3.1.0 | [#726](https://github.com/opensearch-project/asynchronous-search/pull/726) | asynchronous-search | Increment to 3.1.0 |
| v3.1.0 | [#820](https://github.com/opensearch-project/common-utils/pull/820) | common-utils | Auto-increment to 3.1.0-SNAPSHOT |
| v3.1.0 | [#735](https://github.com/opensearch-project/dashboards-notifications/pull/735) | dashboards-notifications | Increment to 3.1.0.0 |
| v3.1.0 | [#357](https://github.com/opensearch-project/notifications/pull/357) | notifications | Increment to 3.1.0.0 |
| v3.1.0 | [#579](https://github.com/opensearch-project/reporting/pull/579) | reporting | Increment to 3.1.0.0 |
| v3.1.0 | [#587](https://github.com/opensearch-project/reporting/pull/587) | reporting | Adding release notes for 3.1.0 |
| v3.1.0 | [#534](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/534) | index-management-dashboards | Increment to 3.1.0.0 |
| v3.1.0 | [#1414](https://github.com/opensearch-project/index-management/pull/1414) | index-management | Auto-increment to 3.1.0-SNAPSHOT |
| v3.1.0 | [#1313](https://github.com/opensearch-project/index-management/pull/1313) | index-management | Increment to 3.1.0.0 |
| v3.1.0 | [#572](https://github.com/opensearch-project/ml-commons/pull/572) | ml-commons | Bump version to 3.1.0.0 |
| v3.1.0 | [#2451](https://github.com/opensearch-project/observability/pull/2451) | observability | Workflows - Version bump to 3.1.0 |
| v3.1.0 | [#3671](https://github.com/opensearch-project/sql/pull/3671) | sql | Bump setuptools to 78.1.1 |
| v3.1.0 | [#18039](https://github.com/opensearch-project/OpenSearch/pull/18039) | OpenSearch | Bump Core main branch to 3.0.0 |
| v3.0.0 | [#1843](https://github.com/opensearch-project/alerting/pull/1843) | alerting | Added 3.0 release notes |
| v3.0.0 | [#775](https://github.com/opensearch-project/common-utils/pull/775) | common-utils | Update shadow plugin and bump to 3.0.0.0-alpha1 |
| v3.0.0 | [#1384](https://github.com/opensearch-project/index-management/pull/1384) | index-management | Bump Version to 3.0.0-alpha1 |
| v2.18.0 | [#1718](https://github.com/opensearch-project/alerting/pull/1718) | alerting | Added 2.18.0 release notes |
| v2.18.0 | [#750](https://github.com/opensearch-project/common-utils/pull/750) | common-utils | Added 2.18.0.0 release notes |
| v2.18.0 | [#980](https://github.com/opensearch-project/notifications/pull/980) | notifications | Added 2.18.0 release notes |
| v2.18.0 | [#148](https://github.com/opensearch-project/query-insights/pull/148) | query-insights | Add release notes for 2.18 |
| v2.18.0 | [#1399](https://github.com/opensearch-project/security/pull/1399) | security | Added 2.18.0 release notes |
| v2.17.0 | [#1650](https://github.com/opensearch-project/alerting/pull/1650) | alerting | Added 2.17 release notes |
| v2.17.0 | [#1635](https://github.com/opensearch-project/alerting/pull/1635) | alerting | Increment version to 2.17.0-SNAPSHOT |
| v2.17.0 | [#727](https://github.com/opensearch-project/common-utils/pull/727) | common-utils | Added 2.17.0.0 release notes |
| v2.17.0 | [#1221](https://github.com/opensearch-project/index-management/pull/1221) | index-management | Increment version to 2.17.0-SNAPSHOT |
| v2.17.0 | [#947](https://github.com/opensearch-project/notifications/pull/947) | notifications | Add 2.17.0 release notes |
| v2.17.0 | [#4615](https://github.com/opensearch-project/security/pull/4615) | security | Increment version to 2.17.0-SNAPSHOT |
| v2.17.0 | [#2892](https://github.com/opensearch-project/sql/pull/2892) | sql | Increment version to 2.17.0-SNAPSHOT |

## References

- [opensearch-build#5267](https://github.com/opensearch-project/opensearch-build/issues/5267): Release coordination
- [OpenSearch Release Process](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASING.md): Official release documentation

## Change History

- **v3.1.0** (2026-01-10): Version bumps across 11 repositories (alerting, asynchronous-search, common-utils, dashboards-notifications, notifications, reporting, index-management-dashboards, index-management, ml-commons, observability, sql, OpenSearch core)
- **v3.0.0** (2025-05-06): Version bumps and release notes across 9 repositories (alerting, common-utils, index-management, notifications, security, sql, and dashboard plugins)
- **v2.18.0** (2024-11-05): Release notes across 5 repositories (alerting, common-utils, notifications, query-insights, security)
- **v2.17.0** (2024-09-17): Version bumps and release notes across 12 repositories (alerting, anomaly-detection, asynchronous-search, common-utils, dashboards-notifications, index-management, job-scheduler, ml-commons, notifications, query-insights, security, sql)
