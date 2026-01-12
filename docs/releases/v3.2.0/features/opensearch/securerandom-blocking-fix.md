---
tags:
  - security
---

# SecureRandom Blocking Fix

## Summary

This bugfix reverts the `SecureRandom` instantiation method from `SecureRandom.getInstanceStrong()` back to `new SecureRandom()` in non-FIPS mode. The previous change caused OpenSearch to freeze on systems with low entropy (particularly older Linux kernels like 4.18.x), as `getInstanceStrong()` blocks when the system entropy pool is exhausted.

## Details

### What's New in v3.2.0

The `Randomness.createSecure()` method was modified to use `new SecureRandom()` instead of `SecureRandom.getInstanceStrong()` for the non-FIPS code path. This prevents blocking behavior on systems with limited entropy sources.

### Technical Changes

#### Root Cause

The issue stemmed from a previous change that switched from `new SecureRandom()` to `SecureRandom.getInstanceStrong()`. On Linux systems:

- `SecureRandom.getInstanceStrong()` typically uses `/dev/random`
- `/dev/random` blocks when the entropy pool is depleted
- Older kernels (4.18.x, used in AlmaLinux 8) have smaller entropy pools
- This caused OpenSearch to freeze during startup

#### Code Change

```java
// Before (blocking)
return SecureRandom.getInstanceStrong();

// After (non-blocking)
return new SecureRandom();
```

The fix is applied in `server/src/main/java/org/opensearch/common/Randomness.java`:

```java
public static SecureRandom createSecure() {
    try {
        // FIPS mode handling (unchanged)
        var registrarClass = Class.forName("org.bouncycastle.crypto.CryptoServicesRegistrar");
        var isApprovedOnlyMethod = registrarClass.getMethod("isInApprovedOnlyMode");
        var approvedOnly = (Boolean) isApprovedOnlyMethod.invoke(null);

        if (approvedOnly) {
            // FIPS-compliant DRBG implementation
            // ... (unchanged)
        }

        // Non-FIPS: Use new SecureRandom() to avoid blocking
        return new SecureRandom();
    } catch (ReflectiveOperationException | GeneralSecurityException e) {
        try {
            return SecureRandom.getInstanceStrong();
        } catch (NoSuchAlgorithmException ex) {
            throw new SecurityException("Failed to instantiate SecureRandom: " + e.getMessage(), e);
        }
    }
}
```

#### Behavior by Mode

| Mode | Implementation | Blocking Behavior |
|------|---------------|-------------------|
| FIPS | `FipsDRBG.SHA512_HMAC` via BouncyCastle | Non-blocking |
| Non-FIPS | `new SecureRandom()` | Non-blocking |
| Fallback | `SecureRandom.getInstanceStrong()` | May block |

### Affected Systems

Systems most likely to experience the blocking issue:
- AlmaLinux 8 (kernel 4.18.x)
- RHEL 8 / CentOS 8
- Other distributions with older kernels
- Virtual machines with limited entropy sources
- Containers without access to hardware RNG

### Workarounds (for older versions)

If upgrading is not immediately possible:
1. Upgrade to kernel 5.x or later
2. Install `haveged` or `rng-tools` to increase entropy
3. Use hardware RNG if available

## Limitations

- The fallback path still uses `getInstanceStrong()` and may block if BouncyCastle reflection fails
- FIPS mode behavior is unchanged and uses BouncyCastle DRBG

## References

### Documentation
- [OpenSearch Forum Discussion](https://forum.opensearch.org/t/docker-image-3-1-1-doesnt-seem-to-work/24875): Original bug report and investigation

### Pull Requests
| PR | Description |
|----|-------------|
| [#18758](https://github.com/opensearch-project/OpenSearch/pull/18758) | Use `new SecureRandom()` to avoid blocking |

### Issues (Design / RFC)
- [Issue #18729](https://github.com/opensearch-project/OpenSearch/issues/18729): OpenSearch 3.1.0 freezes when running on AlmaLinux 8

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-randomness.md)
