# Dependency Bumps

## Summary

OpenSearch v3.0.0 includes 30 dependency updates that improve security, performance, and compatibility. Key highlights include switching to JDK 21 LTS as the default runtime, major AWS SDK upgrade from 2.20.x to 2.30.x, and updates to networking libraries like Reactor Netty and Apache HttpClient5.

## Details

### What's New in v3.0.0

This release consolidates numerous dependency updates across the OpenSearch codebase, focusing on:

- **Runtime upgrade**: JDK 21 LTS becomes the default Java runtime
- **AWS SDK modernization**: Major version bump enabling new AWS features
- **Networking improvements**: Updated HTTP clients and reactive networking libraries
- **Security patches**: Updated authentication and cryptography libraries

### Technical Changes

#### Key Dependency Updates

| Category | Dependency | Old Version | New Version |
|----------|------------|-------------|-------------|
| **Runtime** | JDK | 17 | 21 LTS |
| **AWS** | software.amazon.awssdk | 2.20.86 | 2.30.31 |
| **Networking** | reactor_netty | 1.1.26 | 1.2.3 |
| **Networking** | Apache HttpCore5 | 5.2.5 | 5.3.1 |
| **Networking** | Apache HttpClient5 | 5.3.1 | 5.4.1 |
| **Security** | nimbus-jose-jwt | 9.41.1 | 10.0.2 |
| **Security** | oauth2-oidc-sdk | 11.21 | 11.23.1 |
| **Storage** | azure-storage-blob | 12.28.1 | 12.30.0 |
| **Storage** | azure-core | 1.54.1 | 1.55.3 |
| **Compression** | zstd-jni | 1.5.5-1 | 1.5.6-1 |
| **Serialization** | gson | 2.11.0 | 2.13.0 |
| **Logging** | logback-classic | 1.5.16 | 1.5.18 |
| **Server** | jetty | 9.4.55.v20240627 | 9.4.57.v20241219 |
| **Testing** | awaitility | 4.2.0 | 4.3.0 |
| **Build** | japicmp | 0.4.5 | 0.4.6 |
| **Build** | ospackage-base | 11.10.1 | 11.11.2 |
| **Protobuf** | opensearch:protobufs | 0.2.0 | 0.3.0 |

#### JDK 21 LTS Migration

The switch to JDK 21 LTS brings:
- Improved performance with virtual threads support
- Enhanced garbage collection
- Pattern matching improvements
- Long-term support until 2029

#### AWS SDK 2.30.x Features

The major AWS SDK upgrade from 2.20.x to 2.30.x includes:
- Improved S3 transfer performance
- Enhanced credential provider chain
- Better async client support
- New service integrations

#### Reactor Netty 1.2.x

The Reactor Netty upgrade from 1.1.x to 1.2.x provides:
- Dynamic proxy configuration at HTTP protocol level
- Configurable compression levels
- Improved HTTP/2 connection pool management
- Bug fixes for TLS upgrade handling

#### Apache HttpClient5 Upgrade

The HttpCore5/HttpClient5 upgrade enables:
- `ExtendedSocketOption` support in `HttpAsyncClient`
- Better socket configuration options
- Improved connection management

### Migration Notes

- **JDK 21 required**: Ensure your deployment environment supports JDK 21
- **AWS SDK compatibility**: Review AWS SDK changelog for any breaking changes in your integrations
- **Plugin compatibility**: Verify third-party plugins are compatible with updated dependencies

## Limitations

- Some dependency updates may introduce subtle behavioral changes
- Third-party plugins may need updates for compatibility
- JDK 21 requirement may affect older deployment environments

## Related PRs

| PR | Description |
|----|-------------|
| [#17515](https://github.com/opensearch-project/OpenSearch/pull/17515) | Switch main/3.x to use JDK21 LTS version |
| [#17396](https://github.com/opensearch-project/OpenSearch/pull/17396) | Bump software.amazon.awssdk from 2.20.86 to 2.30.31 |
| [#17322](https://github.com/opensearch-project/OpenSearch/pull/17322) | Bump reactor_netty from 1.1.26 to 1.2.3 |
| [#16757](https://github.com/opensearch-project/OpenSearch/pull/16757) | Bump Apache HttpCore5/HttpClient5 for ExtendedSocketOption support |
| [#17395](https://github.com/opensearch-project/OpenSearch/pull/17395) | Bump jetty from 9.4.55 to 9.4.57 |
| [#17607](https://github.com/opensearch-project/OpenSearch/pull/17607) | Bump nimbus-jose-jwt from 9.41.1 to 10.0.2 |
| [#17562](https://github.com/opensearch-project/OpenSearch/pull/17562) | Bump azure-storage-blob from 12.28.1 to 12.30.0 |
| [#17674](https://github.com/opensearch-project/OpenSearch/pull/17674) | Bump zstd-jni from 1.5.5-1 to 1.5.6-1 |
| [#17229](https://github.com/opensearch-project/OpenSearch/pull/17229) | Bump gson from 2.11.0 to 2.13.0 |
| [#17497](https://github.com/opensearch-project/OpenSearch/pull/17497) | Bump logback-classic from 1.5.16 to 1.5.18 |
| [#17230](https://github.com/opensearch-project/OpenSearch/pull/17230) | Bump awaitility from 4.2.0 to 4.3.0 |
| [#17231](https://github.com/opensearch-project/OpenSearch/pull/17231) | Bump dnsjava from 3.6.2 to 3.6.3 |
| [#17136](https://github.com/opensearch-project/OpenSearch/pull/17136) | Bump joni from 2.2.1 to 2.2.6 |
| [#17288](https://github.com/opensearch-project/OpenSearch/pull/17288) | Bump ant from 1.10.14 to 1.10.15 |
| [#17375](https://github.com/opensearch-project/OpenSearch/pull/17375) | Bump japicmp from 0.4.5 to 0.4.6 |
| [#17379](https://github.com/opensearch-project/OpenSearch/pull/17379) | Bump proto-google-common-protos from 2.37.1 to 2.54.1 |
| [#17378](https://github.com/opensearch-project/OpenSearch/pull/17378) | Bump json-smart from 2.5.1 to 2.5.2 |
| [#17374](https://github.com/opensearch-project/OpenSearch/pull/17374) | Bump ospackage-base from 11.10.1 to 11.11.2 |
| [#17560](https://github.com/opensearch-project/OpenSearch/pull/17560) | Bump jcodings from 1.0.61 to 1.0.63 |
| [#17604](https://github.com/opensearch-project/OpenSearch/pull/17604) | Bump api-common from 1.8.1 to 2.46.1 |
| [#17609](https://github.com/opensearch-project/OpenSearch/pull/17609) | Bump logback-core from 1.5.16 to 1.5.18 |
| [#17498](https://github.com/opensearch-project/OpenSearch/pull/17498) | Bump dependabot-changelog-helper from 3 to 4 |
| [#17465](https://github.com/opensearch-project/OpenSearch/pull/17465) | Bump gax from 2.35.0 to 2.63.1 |
| [#17666](https://github.com/opensearch-project/OpenSearch/pull/17666) | Bump tj-actions/changed-files from 46.0.1 to 46.0.5 |
| [#17731](https://github.com/opensearch-project/OpenSearch/pull/17731) | Bump lychee-action from 2.3.0 to 2.4.0 |
| [#17729](https://github.com/opensearch-project/OpenSearch/pull/17729) | Bump oauth2-oidc-sdk from 11.21 to 11.23.1 |
| [#17811](https://github.com/opensearch-project/OpenSearch/pull/17811) | Bump proto-google-iam-v1 from 1.33.0 to 1.49.1 |
| [#17810](https://github.com/opensearch-project/OpenSearch/pull/17810) | Bump azure-core from 1.54.1 to 1.55.3 |
| [#17887](https://github.com/opensearch-project/OpenSearch/pull/17887) | Bump Apache POI from 5.2.5 to 5.4.1 |
| [#17888](https://github.com/opensearch-project/OpenSearch/pull/17888) | Bump opensearch:protobufs from 0.2.0 to 0.3.0 |

## References

- [Issue #15927](https://github.com/opensearch-project/OpenSearch/issues/15927): ExtendedSocketOption support request
- [Reactor Netty 1.2.3 Release Notes](https://github.com/reactor/reactor-netty/releases/tag/v1.2.3)
- [AWS SDK for Java 2.x Changelog](https://github.com/aws/aws-sdk-java-v2/blob/master/CHANGELOG.md)

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/dependency-management.md)
