---
tags:
  - domain/core
  - component/server
  - security
---
# Security Kerberos Integration

## Summary

This release updates Hadoop to version 3.4.2 and re-enables Kerberos security integration tests for JDK-24 and above. The update addresses long-standing compatibility issues with deprecated and removed Java APIs that previously prevented Kerberos authentication tests from running on newer JDK versions.

## Details

### What's New in v3.4.0

The repository-hdfs plugin now supports Kerberos authentication testing on JDK-24+, enabling secure HDFS repository operations with modern Java runtimes.

### Technical Changes

#### Dependency Update

| Component | Previous Version | New Version |
|-----------|------------------|-------------|
| Hadoop | 3.3.6 | 3.4.2 |
| hadoop-client-api | 3.3.6 | 3.4.2 |
| hadoop-client-runtime | 3.3.6 | 3.4.2 |
| hadoop-hdfs | 3.3.6 | 3.4.2 |

#### Test Re-enablement

Previously disabled integration tests for JDK-24+ are now enabled:

- `integTestSecure` - Secure HDFS integration tests
- `integTestSecureHa` - Secure HDFS High Availability integration tests

The following code was removed from `plugins/repository-hdfs/build.gradle`:

```groovy
// Previously disabled for JDK-24+
if (BuildParams.runtimeJavaVersion >= JavaVersion.VERSION_24) {
  disabledIntegTestTaskNames += ['integTestSecure', 'integTestSecureHa']
  testingConventions.enabled = false
}
```

#### Security Policy Update

Added permission for Kerberos configuration file access in `server/src/main/resources/org/opensearch/bootstrap/security.policy`:

```java
// allow to access krb5.conf
permission java.io.FilePermission "${{java.security.krb5.conf}}", "read";
```

#### Third-Party Audit Updates

Updated class exclusions for the new Hadoop version:

| Removed | Added |
|---------|-------|
| `LittleEndianByteArray$UnsafeByteArray$3` | `MessageSchema` |
| | `UnsafeUtil$Android32MemoryAccessor` |
| | `UnsafeUtil$Android64MemoryAccessor` |

### Usage Example

Kerberos authentication for HDFS repository requires configuration in `opensearch.yml`:

```yaml
plugins.security.kerberos.krb5_filepath: '/etc/krb5.conf'
plugins.security.kerberos.acceptor_keytab_filepath: 'opensearch_keytab.tab'
plugins.security.kerberos.acceptor_principal: 'HTTP/localhost'
```

### Migration Notes

No migration required. The Hadoop upgrade is backward compatible. Existing HDFS repository configurations will continue to work.

## Limitations

- Kerberos integration tests require a properly configured Kerberos environment
- The `keytab` file must be placed in the `config` directory or a subdirectory

## References

### Documentation
- [Kerberos Authentication Documentation](https://docs.opensearch.org/3.0/security/authentication-backends/kerberos/): Official OpenSearch Kerberos configuration guide

### Pull Requests
| PR | Description |
|----|-------------|
| [#19952](https://github.com/opensearch-project/OpenSearch/pull/19952) | Update Hadoop to 3.4.2 and enable security (Kerberos) integration tests under JDK-24 and above |

## Related Feature Report

- Full feature documentation
