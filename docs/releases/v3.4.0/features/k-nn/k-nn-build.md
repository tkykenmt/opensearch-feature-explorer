---
tags:
  - domain/search
  - component/server
  - indexing
  - k-nn
  - performance
  - security
---
# k-NN Build

## Summary

This release includes two build infrastructure improvements for the k-NN plugin: adding SIMD library support to build configurations and migrating snapshot publishing from Sonatype to the OpenSearch S3 repository.

## Details

### What's New in v3.4.0

#### SIMD Library Build Support

The `opensearchknn_simd` library is now included in build configurations for all AVX variants. This ensures that SIMD-optimized vector operations are properly built and packaged with the k-NN plugin.

#### S3 Snapshots Migration

The k-NN plugin has migrated from Sonatype snapshot repositories to the OpenSearch CI S3 repository for publishing and consuming Maven snapshots. This change was part of a broader OpenSearch project initiative to consolidate snapshot management.

### Technical Changes

#### Build Script Updates

The build script (`scripts/build.sh`) now includes `opensearchknn_simd` alongside `opensearchknn_faiss` in all build configurations:

```bash
# Base build (no AVX)
./gradlew :buildJniLib -Pknn_libs=opensearchknn_faiss,opensearchknn_simd -Davx512.enabled=false -Davx512_spr.enabled=false -Davx2.enabled=false

# AVX2 build
./gradlew :buildJniLib -Pknn_libs=opensearchknn_faiss,opensearchknn_simd -Davx2.enabled=true -Davx512.enabled=false -Davx512_spr.enabled=false

# AVX512 build
./gradlew :buildJniLib -Pknn_libs=opensearchknn_faiss,opensearchknn_simd -Davx512.enabled=true -Davx512_spr.enabled=false

# AVX512_SPR build
./gradlew :buildJniLib -Pknn_libs=opensearchknn_faiss,opensearchknn_simd -Davx512_spr.enabled=true
```

#### Security Permissions

New security permissions were added to `plugin-security.policy` for loading SIMD libraries:

| Permission | Description |
|------------|-------------|
| `loadLibrary.opensearchknn_simd` | Base SIMD library |
| `loadLibrary.opensearchknn_simd_avx2` | AVX2-optimized SIMD library |
| `loadLibrary.opensearchknn_simd_avx512` | AVX512-optimized SIMD library |
| `loadLibrary.opensearchknn_simd_avx512_spr` | AVX512 Sapphire Rapids SIMD library |

#### Repository Configuration Changes

| Setting | Old Value | New Value |
|---------|-----------|-----------|
| Snapshot Repository URL | `https://central.sonatype.com/repository/maven-snapshots/` | `https://ci.opensearch.org/ci/dbc/snapshots/maven/` |
| Authentication | Sonatype username/password | AWS credentials (IAM role) |

The Gradle build configuration now uses AWS credentials for S3 access:

```groovy
repositories {
    maven {
        name = "Snapshots"
        url = System.getenv("MAVEN_SNAPSHOTS_S3_REPO")
        credentials(AwsCredentials) {
            accessKey = System.getenv("AWS_ACCESS_KEY_ID")
            secretKey = System.getenv("AWS_SECRET_ACCESS_KEY")
            sessionToken = System.getenv("AWS_SESSION_TOKEN")
        }
    }
}
```

### Migration Notes

For developers building the k-NN plugin locally:

1. **SIMD Library**: No action required - the SIMD library is now automatically built with the plugin
2. **Snapshot Dependencies**: Update any local Gradle configurations to use the new S3 repository URL if pulling snapshot dependencies

## Limitations

- The S3 snapshot repository requires AWS credentials for publishing (handled automatically in CI)
- SIMD optimizations are only available on x64 architectures

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#3025](https://github.com/opensearch-project/k-NN/pull/3025) | Include opensearchknn_simd in build configurations |
| [#2943](https://github.com/opensearch-project/k-NN/pull/2943) | Onboard to S3 snapshots |

### Issues (Design / RFC)
- [Issue #5360](https://github.com/opensearch-project/opensearch-build/issues/5360): Migration from Sonatype snapshots repo to ci.opensearch.org snapshots repo

## Related Feature Report

- Full feature documentation
