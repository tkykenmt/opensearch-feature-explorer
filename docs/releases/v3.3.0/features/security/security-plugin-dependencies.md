# Security Plugin Dependencies

## Summary

OpenSearch v3.3.0 includes 25 dependency updates for the Security plugin, addressing security vulnerabilities and keeping libraries current. The most critical update is nimbus-jose-jwt to address CVE-2025-53864.

## Details

### What's New in v3.3.0

This release focuses on routine dependency maintenance with one critical security fix:

- **CVE-2025-53864 Fix**: Upgraded nimbus-jose-jwt from 9.48 to 10.5 to address a security vulnerability in JWT processing
- **CI/CD Tooling Updates**: Updated GitHub Actions (checkout, setup-java, github-script) and related tools
- **Framework Updates**: Spring Framework 6.2.9 → 6.2.11, OpenSAML 5.1.4 → 5.1.6
- **Build Tool Updates**: SpotBugs 6.2.4 → 6.4.1, Gradle plugins

### Technical Changes

#### Security Vulnerability Fixes

| Dependency | From | To | CVE |
|------------|------|-----|-----|
| nimbus-jose-jwt | 9.48 | 10.5 | CVE-2025-53864 |

#### Runtime Dependency Updates

| Dependency | From | To |
|------------|------|-----|
| jjwt_version | 0.12.6 | 0.13.0 |
| spring_version | 6.2.9 | 6.2.11 |
| open_saml_version | 5.1.4 | 5.1.6 |
| open_saml_shib_version | 9.1.4 | 9.1.6 |
| guava | 33.4.8-jre | 33.5.0-jre |
| metrics-core | 4.2.33 | 4.2.37 |
| checker-qual | 3.49.5 | 3.51.0 |
| jakarta.xml.bind-api | 4.0.2 | 4.0.4 |
| org.eclipse.core.runtime | 3.33.100 | 3.34.0 |
| org.eclipse.equinox.common | 3.20.100 | 3.20.200 |
| error_prone_annotations | 2.41.0 | 2.42.0 |
| scala-logging_3 | 3.9.5 | 3.9.6 |
| j2objc-annotations | 3.0.0 | 3.1 |
| org.opensearch:protobufs | 0.6.0 | 0.13.0 |

#### Test Dependency Updates

| Dependency | From | To |
|------------|------|-----|
| mockito-core | 5.18.0 | 5.20.0 |
| byte-buddy | 1.17.6 | 1.17.7 |
| spring-kafka-test | 4.0.0-M3 | 4.0.0-M5 |

#### Build/CI Dependency Updates

| Dependency | From | To |
|------------|------|-----|
| com.github.spotbugs | 6.2.4 | 6.4.1 |
| actions/checkout | 4 | 5 |
| actions/setup-java | 4 | 5 |
| actions/github-script | 7 | 8 |
| 1password/load-secrets-action | 2 | 3 |
| derek-ho/start-opensearch | 7 | 8 |

### Migration Notes

No migration steps required. These are transparent dependency updates that maintain backward compatibility.

## Limitations

- Dependency updates are coordinated with OpenSearch core version requirements
- Some transitive dependencies may also be updated automatically

## Related PRs

| PR | Description |
|----|-------------|
| [#5595](https://github.com/opensearch-project/security/pull/5595) | Upgrade nimbus-jose-jwt 9.48 → 10.4.2 (CVE-2025-53864) |
| [#5629](https://github.com/opensearch-project/security/pull/5629) | Bump nimbus-jose-jwt 10.4.2 → 10.5 |
| [#5568](https://github.com/opensearch-project/security/pull/5568) | Bump jjwt_version 0.12.6 → 0.13.0 |
| [#5569](https://github.com/opensearch-project/security/pull/5569) | Bump spring_version 6.2.9 → 6.2.11 |
| [#5567](https://github.com/opensearch-project/security/pull/5567) | Bump open_saml_version 5.1.4 → 5.1.6 |
| [#5585](https://github.com/opensearch-project/security/pull/5585) | Bump open_saml_shib_version 9.1.4 → 9.1.6 |
| [#5665](https://github.com/opensearch-project/security/pull/5665) | Bump guava 33.4.8-jre → 33.5.0-jre |
| [#5589](https://github.com/opensearch-project/security/pull/5589) | Bump metrics-core 4.2.33 → 4.2.37 |
| [#5566](https://github.com/opensearch-project/security/pull/5566) | Bump mockito-core 5.18.0 → 5.20.0 |
| [#5586](https://github.com/opensearch-project/security/pull/5586) | Bump byte-buddy 1.17.6 → 1.17.7 |
| [#5584](https://github.com/opensearch-project/security/pull/5584) | Bump com.github.spotbugs 6.2.4 → 6.4.1 |
| [#5572](https://github.com/opensearch-project/security/pull/5572) | Bump actions/checkout 4 → 5 |
| [#5582](https://github.com/opensearch-project/security/pull/5582) | Bump actions/setup-java 4 → 5 |
| [#5610](https://github.com/opensearch-project/security/pull/5610) | Bump actions/github-script 7 → 8 |
| [#5573](https://github.com/opensearch-project/security/pull/5573) | Bump 1password/load-secrets-action 2 → 3 |
| [#5630](https://github.com/opensearch-project/security/pull/5630) | Bump derek-ho/start-opensearch 7 → 8 |
| [#5627](https://github.com/opensearch-project/security/pull/5627) | Bump checker-qual 3.49.5 → 3.51.0 |
| [#5628](https://github.com/opensearch-project/security/pull/5628) | Bump org.eclipse.core.runtime 3.33.100 → 3.34.0 |
| [#5651](https://github.com/opensearch-project/security/pull/5651) | Bump org.eclipse.equinox.common 3.20.100 → 3.20.200 |
| [#5649](https://github.com/opensearch-project/security/pull/5649) | Bump jakarta.xml.bind-api 4.0.2 → 4.0.4 |
| [#5648](https://github.com/opensearch-project/security/pull/5648) | Bump error_prone_annotations 2.41.0 → 2.42.0 |
| [#5663](https://github.com/opensearch-project/security/pull/5663) | Bump scala-logging_3 3.9.5 → 3.9.6 |
| [#5570](https://github.com/opensearch-project/security/pull/5570) | Bump j2objc-annotations 3.0.0 → 3.1 |
| [#5553](https://github.com/opensearch-project/security/pull/5553) | Bump org.opensearch:protobufs 0.6.0 → 0.13.0 |
| [#5583](https://github.com/opensearch-project/security/pull/5583) | Bump spring-kafka-test 4.0.0-M3 → 4.0.0-M5 |

## References

- [CVE-2025-53864](https://github.com/advisories/GHSA-xwmg-2g98-w7v9): nimbus-jose-jwt vulnerability
- [Issue #5593](https://github.com/opensearch-project/security/issues/5593): CVE-2025-53864 tracking issue
- [OpenSearch Security Repository](https://github.com/opensearch-project/security)

## Related Feature Report

- [Full feature documentation](../../../../features/security/security-plugin-dependencies.md)
