---
tags:
  - custom-codecs
---
# QAT Security Permission Fix

## Summary

Fixed a Java security permission issue that prevented `qat_deflate` and `qat_lz4` codecs from working correctly. The `isQATAvailable()` method was returning `false` due to a `java.security` permission failure when checking QAT hardware availability.

## Details

### Problem

Users reported that `qat_deflate` and `qat_lz4` hardware-accelerated codecs were not functioning. Investigation revealed that `isQATAvailable()` in `QatZipperFactory` was returning `false` because the call to `QatZipper` constructor triggered a Java security permission check that failed.

### Solution

The fix wraps the `QatZipper` instantiation with `AccessController.doPrivileged()` to grant the necessary permissions for QAT hardware detection and initialization.

### Code Change

```java
// Before
public static QatZipper createInstance(...) {
    return new QatZipper(algorithm, level, mode, retryCount, pmode);
}

// After
public static QatZipper createInstance(...) {
    return java.security.AccessController.doPrivileged(
        (java.security.PrivilegedAction<QatZipper>) () -> 
            new QatZipper(algorithm, level, mode, retryCount, pmode)
    );
}
```

### Files Changed

| File | Change |
|------|--------|
| `QatZipperFactory.java` | Wrapped `QatZipper` constructor call with `AccessController.doPrivileged` |
| `.github/workflows/check.yml` | Updated CI workflow configuration |

## Limitations

- This fix addresses the security permission issue but does not change the underlying QAT hardware requirements
- QAT hardware acceleration still requires Intel 4th/5th Gen Xeon processors with Linux kernel 3.10+

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#211](https://github.com/opensearch-project/custom-codecs/pull/211) | Wrap a call to QatZipper with AccessController.doPrivileged | Customer-reported issue |
