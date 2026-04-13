---
tags:
  - security
---
# Security Plugin Dependency Bumps

## Summary

OpenSearch Security plugin v3.6.0 includes 30 dependency updates covering runtime libraries, build tooling, CI actions, and test infrastructure. Notable updates include Kafka 4.2.0, OpenSAML 5.2.1, Spring Framework 7.0.6, nimbus-jose-jwt 10.8, and Gradle Wrapper 9.4.0.

## Details

### What's New in v3.6.0

This release includes a broad set of dependency bumps, primarily automated via Dependabot. The updates span several categories:

#### Security & Authentication Libraries
| Dependency | From | To | PR |
|------------|------|----|----|
| nimbus-jose-jwt | 10.7 | 10.8 | #6030 |
| OpenSAML (open_saml_version) | 5.1.6 | 5.2.1 | #5965 |
| OpenSAML Shibboleth (open_saml_shib_version) | 9.2.0 | 9.2.1 | #5982 |

The nimbus-jose-jwt 10.8 update fixes `getDeferredCriticalHeaderParams()` in multiple decrypter and verifier implementations (AESDecrypter, DirectDecrypter, RSADecrypter, ECDHDecrypter, etc.) and adds a new `PasswordBasedDecrypter` constructor for specifying deferred critical header parameters.

The OpenSAML update from 5.1.6 to 5.2.1 covers 14 OpenSAML modules including messaging, security, core, xmlsec, SAML, storage, profile, and SOAP APIs.

#### Runtime Libraries
| Dependency | From | To | PR(s) |
|------------|------|----|----|
| Kafka (kafka_version) | 4.1.1 | 4.2.0 | #5968 |
| Spring Framework (spring_version) | 7.0.3 | 7.0.6 | #5957, #5967, #6008 |
| ipaddress | 5.5.1 | 5.6.2 | #5949, #6010 |
| lz4-java | 1.10.3 | 1.10.4 | #5994, #6028 |
| logback-classic | 1.5.26 | 1.5.32 | #5948, #5995 |
| jakarta.xml.bind-api | 4.0.4 | 4.0.5 | #5978 |

The ipaddress library update (5.5.1 → 5.6.2) introduces new IP address collection types (`IPAddressSeqRangeList`, `IPAddressContainmentTrie`) with set operations and binary search capabilities.

#### Build & Tooling
| Dependency | From | To | PR(s) |
|------------|------|----|----|
| Gradle Wrapper | 9.2.0 | 9.4.0 | #5996 |
| google-java-format | 1.33.0 | 1.35.0 | #5947, #6011 |
| com.autonomousapps.build-health | 3.5.1 | 3.6.1 | #6029 |
| checker-qual | 3.53.0 | 3.54.0 | #5955, #6009 |
| eclipse.core.runtime | 3.34.100 | 3.34.200 | #6027 |

#### CI/CD Actions
| Dependency | From | To | PR |
|------------|------|----|-----|
| actions/download-artifact | 7 | 8 | #5979 |
| actions/upload-artifact | 6 | 7 | #5980 |
| aws-actions/configure-aws-credentials | 5 | 6 | #5946 |
| release-drafter/release-drafter | 6 | 7 | #6007 |

#### Test Dependencies
| Dependency | From | To | PR(s) |
|------------|------|----|----|
| byte-buddy | 1.18.4 | 1.18.7 | #6012 |
| randomizedtesting-runner | 2.8.3 | 2.8.4 | #5993 |
| junit-jupiter-api | 5.14.2 | 5.14.3 | #5956 |
| spring-kafka-test | 4.0.2 | 4.0.4 | #5981, #6026 |

### Technical Changes

All 30 PRs modify Gradle build files (`build.gradle`, `gradle/wrapper/gradle-wrapper.properties`, or GitHub Actions workflow YAML files). Most are automated Dependabot PRs with no functional code changes beyond version bumps. The Kafka 4.2.0 bump (#5968) was a manual PR by a maintainer to fix failing CI checks from the original Dependabot PR.

## Limitations

- Dependency updates are constrained by OpenSearch core compatibility requirements
- Some updates (e.g., lz4-java, ipaddress) were bumped twice during the release cycle as newer patch versions became available

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6030](https://github.com/opensearch-project/security/pull/6030) | Bump nimbus-jose-jwt 10.7 → 10.8 | |
| [#5965](https://github.com/opensearch-project/security/pull/5965) | Bump open_saml_version 5.1.6 → 5.2.1 | |
| [#5982](https://github.com/opensearch-project/security/pull/5982) | Bump open_saml_shib_version 9.2.0 → 9.2.1 | |
| [#5968](https://github.com/opensearch-project/security/pull/5968) | Bump kafka_version 4.1.1 → 4.2.0 | [#5966](https://github.com/opensearch-project/security/pull/5966) |
| [#5957](https://github.com/opensearch-project/security/pull/5957) | Bump spring_version 7.0.3 → 7.0.4 | |
| [#5967](https://github.com/opensearch-project/security/pull/5967) | Bump spring_version 7.0.4 → 7.0.5 | |
| [#6008](https://github.com/opensearch-project/security/pull/6008) | Bump spring_version 7.0.5 → 7.0.6 | |
| [#5949](https://github.com/opensearch-project/security/pull/5949) | Bump ipaddress 5.5.1 → 5.6.1 | |
| [#6010](https://github.com/opensearch-project/security/pull/6010) | Bump ipaddress 5.6.1 → 5.6.2 | |
| [#5994](https://github.com/opensearch-project/security/pull/5994) | Bump lz4-java 1.10.3 → 1.10.4 | |
| [#6028](https://github.com/opensearch-project/security/pull/6028) | Bump lz4-java 1.10.3 → 1.10.4 | |
| [#5948](https://github.com/opensearch-project/security/pull/5948) | Bump logback-classic 1.5.26 → 1.5.28 | |
| [#5995](https://github.com/opensearch-project/security/pull/5995) | Bump logback-classic 1.5.28 → 1.5.32 | |
| [#5978](https://github.com/opensearch-project/security/pull/5978) | Bump jakarta.xml.bind-api 4.0.4 → 4.0.5 | |
| [#5996](https://github.com/opensearch-project/security/pull/5996) | Bump Gradle Wrapper 9.2.0 → 9.4.0 | |
| [#5947](https://github.com/opensearch-project/security/pull/5947) | Bump google-java-format 1.33.0 → 1.34.1 | |
| [#6011](https://github.com/opensearch-project/security/pull/6011) | Bump google-java-format 1.34.1 → 1.35.0 | |
| [#6029](https://github.com/opensearch-project/security/pull/6029) | Bump build-health 3.5.1 → 3.6.1 | |
| [#5955](https://github.com/opensearch-project/security/pull/5955) | Bump checker-qual 3.53.0 → 3.53.1 | |
| [#6009](https://github.com/opensearch-project/security/pull/6009) | Bump checker-qual 3.53.1 → 3.54.0 | |
| [#6027](https://github.com/opensearch-project/security/pull/6027) | Bump eclipse.core.runtime 3.34.100 → 3.34.200 | |
| [#5979](https://github.com/opensearch-project/security/pull/5979) | Bump actions/download-artifact 7 → 8 | |
| [#5980](https://github.com/opensearch-project/security/pull/5980) | Bump actions/upload-artifact 6 → 7 | |
| [#5946](https://github.com/opensearch-project/security/pull/5946) | Bump aws-actions/configure-aws-credentials 5 → 6 | |
| [#6007](https://github.com/opensearch-project/security/pull/6007) | Bump release-drafter/release-drafter 6 → 7 | |
| [#6012](https://github.com/opensearch-project/security/pull/6012) | Bump byte-buddy 1.18.4 → 1.18.7 | |
| [#5993](https://github.com/opensearch-project/security/pull/5993) | Bump randomizedtesting-runner 2.8.3 → 2.8.4 | |
| [#5956](https://github.com/opensearch-project/security/pull/5956) | Bump junit-jupiter-api 5.14.2 → 5.14.3 | |
| [#5981](https://github.com/opensearch-project/security/pull/5981) | Bump spring-kafka-test 4.0.2 → 4.0.3 | |
| [#6026](https://github.com/opensearch-project/security/pull/6026) | Bump spring-kafka-test 4.0.3 → 4.0.4 | |
