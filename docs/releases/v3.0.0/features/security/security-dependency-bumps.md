---
tags:
  - security
---

# Security Dependency Bumps

## Summary

OpenSearch Security plugin v3.0.0 includes 13 dependency version bumps to keep the plugin up-to-date with the latest library versions. These updates improve security, stability, and compatibility with newer Java versions.

## Details

### What's New in v3.0.0

This release includes routine dependency updates managed by Dependabot, covering security libraries, testing frameworks, and utility libraries.

### Dependency Updates

| Dependency | Previous Version | New Version | Category |
|------------|------------------|-------------|----------|
| Spring Framework | 6.2.4 | 6.2.5 | Core Framework |
| Bouncy Castle | 1.78 | 1.80 | Cryptography |
| Google Java Format | 1.25.2 | 1.26.0 | Code Quality |
| OpenSAML (Shibboleth) | 9.1.3 | 9.1.4 | SAML Authentication |
| OpenSAML | 5.1.3 | 5.1.4 | SAML Authentication |
| Randomized Testing Runner | 2.8.2 | 2.8.3 | Testing |
| ASM | 9.7.1 | 9.8 | Bytecode Manipulation |
| Nebula OS Package | 11.11.1 | 11.11.2 | Build Tools |
| Error Prone Annotations | 2.36.0 | 2.37.0 | Code Quality |
| Commons IO | 2.18.0 | 2.19.0 | Utilities |
| Commons Text | 1.13.0 | 1.13.1 | Utilities |
| JUnit Jupiter API | 5.12.1 | 5.12.2 | Testing |
| Guava Failure Access | 1.0.2 | 1.0.3 | Utilities |

### Key Updates

#### Bouncy Castle 1.80
The cryptography library update to version 1.80 includes security improvements and bug fixes for cryptographic operations used in TLS/SSL and certificate handling.

#### Spring Framework 6.2.5
Spring Framework update includes bug fixes for `PathMatchingResourcePatternResolver` and improvements to reactive transaction management.

#### OpenSAML Updates
Both OpenSAML versions (5.1.4 and Shibboleth 9.1.4) include maintenance updates for SAML-based authentication flows.

## Limitations

- These are maintenance updates with no new features
- No breaking changes expected from these dependency bumps

## References

### Documentation
- [OpenSearch Security Repository](https://github.com/opensearch-project/security)
- [Bouncy Castle Release Notes](https://www.bouncycastle.org/releasenotes.html)
- [Spring Framework 6.2.5 Release](https://github.com/spring-projects/spring-framework/releases/tag/v6.2.5)

### Pull Requests
| PR | Description |
|----|-------------|
| [#5203](https://github.com/opensearch-project/security/pull/5203) | Bump spring_version from 6.2.4 to 6.2.5 |
| [#5202](https://github.com/opensearch-project/security/pull/5202) | Bump bouncycastle_version from 1.78 to 1.80 |
| [#5231](https://github.com/opensearch-project/security/pull/5231) | Bump google-java-format from 1.25.2 to 1.26.0 |
| [#5230](https://github.com/opensearch-project/security/pull/5230) | Bump open_saml_shib_version from 9.1.3 to 9.1.4 |
| [#5229](https://github.com/opensearch-project/security/pull/5229) | Bump randomizedtesting-runner from 2.8.2 to 2.8.3 |
| [#5227](https://github.com/opensearch-project/security/pull/5227) | Bump open_saml_version from 5.1.3 to 5.1.4 |
| [#5244](https://github.com/opensearch-project/security/pull/5244) | Bump org.ow2.asm:asm from 9.7.1 to 9.8 |
| [#5246](https://github.com/opensearch-project/security/pull/5246) | Bump nebula.ospackage from 11.11.1 to 11.11.2 |
| [#5245](https://github.com/opensearch-project/security/pull/5245) | Bump error_prone_annotations from 2.36.0 to 2.37.0 |
| [#5267](https://github.com/opensearch-project/security/pull/5267) | Bump commons-io from 2.18.0 to 2.19.0 |
| [#5266](https://github.com/opensearch-project/security/pull/5266) | Bump commons-text from 1.13.0 to 1.13.1 |
| [#5268](https://github.com/opensearch-project/security/pull/5268) | Bump junit-jupiter-api from 5.12.1 to 5.12.2 |
| [#5265](https://github.com/opensearch-project/security/pull/5265) | Bump failureaccess from 1.0.2 to 1.0.3 |

## Related Feature Report

- [Full feature documentation](../../../features/security/security-plugin-dependencies.md)
