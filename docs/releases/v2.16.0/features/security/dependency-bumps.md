---
tags:
  - security
---
# Security Dependency Bumps

## Summary

OpenSearch Security plugin v2.16.0 includes 7 dependency updates covering runtime, test, and build dependencies. These updates improve stability, fix bugs, and address potential security vulnerabilities.

## Details

### What's New in v2.16.0

| Dependency | Previous | New | Category |
|------------|----------|-----|----------|
| checker-qual | 3.44.0 | 3.45.0 | Build |
| kafka | 3.7.0 | 3.7.1 | Runtime |
| junit-jupiter | 5.10.2 | 5.10.3 | Test |
| woodstox-core | 6.6.2 | 6.7.0 | Runtime |
| jjwt | 0.12.5 | 0.12.6 | Runtime |
| eclipse.core.runtime | 3.31.0 | 3.31.100 | Build |
| spring | 5.3.36 | 5.3.37 | Runtime |

### Key Improvements

#### JJWT 0.12.6
- Fixes decompression memory leak in concurrent environments when using GZIP compression
- Ensures application-configured Base64Url decoder is used after JWS signature verification
- Upgrades internal BouncyCastle dependency to 1.78

#### Spring Framework 5.3.37
- Fixes AspectJ CTW aspects executed twice issue
- Fixes SpEL compilation failures when indexing into Map with primitives
- Fixes SpEL compilation failures when indexing into arrays/lists with Integer
- Improves AnnotationUtils performance with deep stacks

#### JUnit Jupiter 5.10.3
- Fixes NPE when deserializing TestIdentifier
- Fixes class-level execution conditions on GraalVM
- Uses same default seed for method and class ordering

#### Kafka 3.7.1
- Patch release with bug fixes and stability improvements

#### Woodstox 6.7.0
- Ensures events' immutable non-null location in WstxEventFactory

#### Checker Framework 3.45.0
- Adds Non-Empty Checker
- Replaces JavaParser with javac for improved performance

## Limitations

- These are routine dependency updates with no breaking changes
- All updates are backward compatible within the 2.x release line

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#4531](https://github.com/opensearch-project/security/pull/4531) | Bump checker-qual 3.44.0 → 3.45.0 |
| [#4501](https://github.com/opensearch-project/security/pull/4501) | Bump kafka 3.7.0 → 3.7.1 |
| [#4503](https://github.com/opensearch-project/security/pull/4503) | Bump junit-jupiter 5.10.2 → 5.10.3 |
| [#4483](https://github.com/opensearch-project/security/pull/4483) | Bump woodstox-core 6.6.2 → 6.7.0 |
| [#4484](https://github.com/opensearch-project/security/pull/4484) | Bump jjwt 0.12.5 → 0.12.6 |
| [#4467](https://github.com/opensearch-project/security/pull/4467) | Bump eclipse.core.runtime 3.31.0 → 3.31.100 |
| [#4466](https://github.com/opensearch-project/security/pull/4466) | Bump spring 5.3.36 → 5.3.37 |
