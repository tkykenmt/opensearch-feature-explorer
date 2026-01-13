---
tags:
  - domain/core
  - component/server
  - security
---
# Plugin Installation Fix

## Summary

This release fixes a critical bug in the native plugin installation process that caused a `NullPointerException` when verifying plugin signatures. The issue was caused by a PGP public key change introduced in OpenSearch 3.0.0, where the new signing key (`release@opensearch.org`) required proper initialization of the BouncyCastle FIPS provider.

## Details

### What's New in v3.1.0

The fix addresses a signature verification failure that occurred when installing bundled plugins (e.g., `analysis-icu`, `repository-s3`) using the `opensearch-plugin install` command.

### Technical Changes

#### Root Cause

Starting from OpenSearch 3.0.0, artifacts are signed with a new PGP key (`release@opensearch.org`) instead of the previous key (`opensearch@amazon.com`). The signature verification code in `InstallPluginCommand.java` failed because the BouncyCastle FIPS provider was not properly registered before initializing the signature verifier.

#### Code Changes

The fix adds explicit registration of the BouncyCastle FIPS provider before signature verification:

```java
// Added imports
import org.bouncycastle.jcajce.provider.BouncyCastleFipsProvider;
import java.security.Security;

// In verifySignature method
Security.addProvider(new BouncyCastleFipsProvider());
signature.init(new JcaPGPContentVerifierBuilderProvider().setProvider("BCFIPS"), key);
```

#### Updated Public Key

The `public_key.sig` file was updated with the new PGP public key for `release@opensearch.org`, replacing the previous `opensearch@amazon.com` key.

### Error Before Fix

```
./bin/opensearch-plugin install analysis-icu --batch
-> Installing analysis-icu
-> Downloading analysis-icu from opensearch
-> Failed installing analysis-icu
-> Rolling back analysis-icu
-> Rolled back analysis-icu
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "org.bouncycastle.openpgp.PGPPublicKey.getVersion()" because "<parameter2>" is null
    at org.bouncycastle.openpgp.PGPSignature.init(Unknown Source)
    at org.opensearch.tools.cli.plugin.InstallPluginCommand.verifySignature(InstallPluginCommand.java:635)
```

### Usage Example

After the fix, plugin installation works correctly:

```bash
./bin/opensearch-plugin install repository-s3
-> Installing repository-s3
-> Downloading repository-s3 from opensearch
[=================================================] 100%   
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.io.FilePermission config#plus read
...
Continue with installation? [y/N]y
-> Installed repository-s3 with folder name repository-s3
```

## Limitations

- This fix is specific to OpenSearch 3.x releases that use the new `release@opensearch.org` signing key
- Users running OpenSearch 2.x should continue using the previous key for signature verification

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/install-and-configure/plugins/): Installing plugins

### Pull Requests
| PR | Description |
|----|-------------|
| [#18147](https://github.com/opensearch-project/OpenSearch/pull/18147) | Fix the native plugin installation error |

### Issues (Design / RFC)
- [Issue #5308](https://github.com/opensearch-project/opensearch-build/issues/5308): New PGP key for signing artifacts starting 3.0.0
- [Issue #3747](https://github.com/opensearch-project/opensearch-build/issues/3747): Release version 3.0.0

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-plugin-installation.md)
