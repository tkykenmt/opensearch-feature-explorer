# Asynchronous Search Bugfix

## Summary

Infrastructure maintenance updates for the Asynchronous Search plugin in v3.2.0, including Gradle upgrade to 8.14.3, JDK 24 CI support, and Maven snapshot publishing endpoint migration to Sonatype Central Portal.

## Details

### What's New in v3.2.0

This release focuses on build infrastructure improvements and CI/CD pipeline updates:

1. **Gradle 8.14.3 Upgrade**: Updated build system from Gradle 8.10.2 to 8.14.3
2. **JDK 24 CI Support**: CI workflows now test against JDK 21 and JDK 24 (replacing JDK 23)
3. **Maven Snapshot Publishing Migration**: Updated to new Sonatype Central Portal endpoints

### Technical Changes

#### Build System Updates

| Component | Before | After |
|-----------|--------|-------|
| Gradle | 8.10.2 | 8.14.3 |
| nebula.ospackage plugin | 11.10.0 | 12.0.0 |
| CI JDK matrix | [21, 23] | [21, 24] |

#### Maven Snapshot Publishing Migration

The Maven snapshot publishing workflow was updated to accommodate Sonatype's migration to the Central Portal:

| Setting | Before | After |
|---------|--------|-------|
| Snapshot URL | `https://aws.oss.sonatype.org/content/repositories/snapshots` | `https://central.sonatype.com/repository/maven-snapshots/` |
| Credential Source | AWS Secrets Manager | 1Password via `OP_SERVICE_ACCOUNT_TOKEN` |
| Authentication | AWS IAM role assumption | Sonatype username/password |

#### CI Workflow Changes

```yaml
# build.yml - JDK matrix update
strategy:
  matrix:
    java: [21, 24]  # Previously [21, 23]
```

The credential retrieval was migrated from AWS Secrets Manager to 1Password:

```yaml
# maven-publish.yml - New credential loading
- name: Load secret
  uses: 1password/load-secrets-action@v2
  with:
    export-env: true
  env:
    OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
    SONATYPE_USERNAME: op://opensearch-infra-secrets/maven-central-portal-credentials/username
    SONATYPE_PASSWORD: op://opensearch-infra-secrets/maven-central-portal-credentials/password
```

### Migration Notes

These changes are internal infrastructure updates and do not affect plugin functionality or user-facing APIs. No migration steps are required for users.

## Limitations

- No functional changes in this release
- These are maintenance updates only

## References

### Documentation
- [Asynchronous Search Documentation](https://docs.opensearch.org/3.0/search-plugins/async/index/)
- [Sonatype Central Portal Snapshots](https://central.sonatype.org/publish/publish-portal-snapshots/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#754](https://github.com/opensearch-project/asynchronous-search/pull/754) | Bump gradle to 8.14.3 and use JDK 24 in CI workflow |
| [#748](https://github.com/opensearch-project/asynchronous-search/pull/748) | Update the Maven snapshot publish endpoint and credential |

### Issues (Design / RFC)
- [opensearch-build#5551](https://github.com/opensearch-project/opensearch-build/issues/5551): Maven snapshot migration campaign

## Related Feature Report

- [Full feature documentation](../../../../features/asynchronous-search/asynchronous-search.md)
