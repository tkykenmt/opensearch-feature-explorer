---
tags:
  - domain/core
  - component/server
  - security
---
# Dependency Bumps

## Summary

OpenSearch v3.1.0 includes 21 dependency updates addressing security vulnerabilities, improving stability, and keeping third-party libraries current. Notable updates include a critical CVE fix for Apache HttpClient5/HttpCore5 and major version bumps for Netty, Gson, and various Azure SDK components.

## Details

### What's New in v3.1.0

This release includes dependency updates across several categories:

- **Security Fix**: CVE-2025-27820 mitigation via Apache HttpClient5/HttpCore5 update
- **Networking**: Netty 4.1.118.Final → 4.1.121.Final
- **Serialization**: Gson 2.12.1 → 2.13.1
- **Cloud SDKs**: Multiple Azure SDK component updates
- **Build Tools**: Gradle Actions 3 → 4

### Security Updates

| Dependency | Update | CVE |
|------------|--------|-----|
| Apache HttpClient5/HttpCore5 | Security patch | CVE-2025-27820 |

CVE-2025-27820 affects Apache HttpCore5 and could potentially allow request smuggling attacks. The update ensures OpenSearch is protected against this vulnerability.

### Networking Updates

| Dependency | From | To |
|------------|------|-----|
| Netty | 4.1.118.Final | 4.1.121.Final |
| reactor-netty | 1.2.4 | 1.2.5 |

### Serialization & Data Processing

| Dependency | From | To |
|------------|------|-----|
| com.google.code.gson:gson | 2.12.1 | 2.13.1 |
| com.squareup.okio:okio | 3.10.2 | 3.12.0 |

Gson 2.13.x includes a bug fix for collection deserialization and internal class renaming.

### Azure SDK Updates

| Dependency | From | To |
|------------|------|-----|
| azure-core-http-netty | 1.15.7 | 1.15.10 |
| azure-json | 1.3.0 | 1.5.0 |
| azure-storage-common | 12.28.0 | 12.29.0 |
| azure-xml | 1.1.0 | 1.2.0 |
| msal4j | 1.18.0 | 1.20.0 |

### Security & Authentication Libraries

| Dependency | From | To |
|------------|------|-----|
| nimbus-jose-jwt | 10.0.2 | 10.3 |
| oauth2-oidc-sdk | 11.23.1 | 11.25 |
| spotbugs-annotations | 4.9.0 | 4.9.3 |

### Apache Commons Updates

| Dependency | From | To |
|------------|------|-----|
| commons-collections4 | 4.4 | 4.5 |
| commons-configuration2 | 2.11.0 | 2.12.0 |
| commons-text | 1.13.0 | 1.13.1 |

### GeoIP & Database

| Dependency | From | To |
|------------|------|-----|
| geoip2 | 4.2.1 | 4.3.1 |
| maxmind-db | 3.1.1 | 3.2.0 |

### Build & CI Tools

| Dependency | From | To |
|------------|------|-----|
| gradle/actions | 3 | 4 |
| lycheeverse/lychee-action | 2.4.0 | 2.4.1 |
| org.jline:jline | 3.29.0 | 3.30.4 |

## Limitations

- Dependency updates may introduce subtle behavioral changes
- Some updates are backported to 2.x and 3.0 branches where applicable

## References

### Documentation
- [CVE-2025-27820](https://www.mend.io/vulnerability-database/CVE-2025-27820): Apache HttpCore5 vulnerability
- [Gson 2.13.0 Release Notes](https://github.com/google/gson/releases/tag/gson-parent-2.13.0)
- [Netty Releases](https://github.com/netty/netty/releases)

### Pull Requests
| PR | Description |
|----|-------------|
| [#18152](https://github.com/opensearch-project/OpenSearch/pull/18152) | Update Apache HttpClient5 and HttpCore5 (CVE-2025-27820) |
| [#18192](https://github.com/opensearch-project/OpenSearch/pull/18192) | Bump netty from 4.1.118.Final to 4.1.121.Final |
| [#17923](https://github.com/opensearch-project/OpenSearch/pull/17923) | Bump com.google.code.gson:gson from 2.12.1 to 2.13.1 |
| [#17922](https://github.com/opensearch-project/OpenSearch/pull/17922) | Bump com.github.spotbugs:spotbugs-annotations from 4.9.0 to 4.9.3 |
| [#17925](https://github.com/opensearch-project/OpenSearch/pull/17925) | Bump com.microsoft.azure:msal4j from 1.18.0 to 1.20.0 |
| [#18101](https://github.com/opensearch-project/OpenSearch/pull/18101) | Bump org.apache.commons:commons-collections4 from 4.4 to 4.5 |
| [#18102](https://github.com/opensearch-project/OpenSearch/pull/18102) | Bump org.apache.commons:commons-text from 1.13.0 to 1.13.1 |
| [#18103](https://github.com/opensearch-project/OpenSearch/pull/18103) | Bump org.apache.commons:commons-configuration2 from 2.11.0 to 2.12.0 |
| [#18104](https://github.com/opensearch-project/OpenSearch/pull/18104) | Bump com.nimbusds:nimbus-jose-jwt from 10.0.2 to 10.3 |
| [#18243](https://github.com/opensearch-project/OpenSearch/pull/18243) | Bump reactor-netty from 1.2.4 to 1.2.5 |
| [#18263](https://github.com/opensearch-project/OpenSearch/pull/18263) | Bump com.maxmind.geoip2:geoip2 from 4.2.1 to 4.3.1 |
| [#18264](https://github.com/opensearch-project/OpenSearch/pull/18264) | Bump lycheeverse/lychee-action from 2.4.0 to 2.4.1 |
| [#18265](https://github.com/opensearch-project/OpenSearch/pull/18265) | Bump com.azure:azure-core-http-netty from 1.15.7 to 1.15.10 |
| [#18335](https://github.com/opensearch-project/OpenSearch/pull/18335) | Bump com.azure:azure-json from 1.3.0 to 1.5.0 |
| [#18368](https://github.com/opensearch-project/OpenSearch/pull/18368) | Bump org.jline:jline from 3.29.0 to 3.30.4 |
| [#18369](https://github.com/opensearch-project/OpenSearch/pull/18369) | Bump com.nimbusds:oauth2-oidc-sdk from 11.23.1 to 11.25 |
| [#18371](https://github.com/opensearch-project/OpenSearch/pull/18371) | Bump gradle/actions from 3 to 4 |
| [#18415](https://github.com/opensearch-project/OpenSearch/pull/18415) | Bump com.azure:azure-storage-common from 12.28.0 to 12.29.0 |
| [#18468](https://github.com/opensearch-project/OpenSearch/pull/18468) | Bump com.squareup.okio:okio from 3.10.2 to 3.12.0 |
| [#18469](https://github.com/opensearch-project/OpenSearch/pull/18469) | Bump com.azure:azure-xml from 1.1.0 to 1.2.0 |
| [#18470](https://github.com/opensearch-project/OpenSearch/pull/18470) | Bump com.maxmind.db:maxmind-db from 3.1.1 to 3.2.0 |

## Related Feature Report

- Full feature documentation
