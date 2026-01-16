---
tags:
  - performance-analyzer
---
# Performance Analyzer Dependencies

## Summary

Security and compatibility updates for Performance Analyzer dependencies in v2.16.0, including BouncyCastle cryptographic library upgrade and PA Commons library version bump.

## Details

### What's New in v2.16.0

This release includes two dependency updates addressing security vulnerabilities and compatibility:

1. **BouncyCastle Upgrade (1.74 → 1.78.1)**: Addresses multiple security advisories
2. **PA Commons Library Update (1.4.0 → 1.5.0)**: Compatibility update for v2.16.0 release

### Technical Changes

#### BouncyCastle Security Update

Updated BouncyCastle cryptographic libraries to address security vulnerabilities:

| Library | Old Version | New Version |
|---------|-------------|-------------|
| `bcprov-jdk15to18` | 1.74 | 1.78.1 |
| `bcpkix-jdk18on` | 1.74 | 1.78.1 |

Security advisories resolved:
- [GHSA-m44j-cfrm-g8qc](https://github.com/advisories/GHSA-m44j-cfrm-g8qc)
- [GHSA-v435-xc8x-wvr9](https://github.com/advisories/GHSA-v435-xc8x-wvr9)
- [GHSA-8xfc-gm6g-vgpv](https://github.com/advisories/GHSA-8xfc-gm6g-vgpv)

#### PA Commons Library Update

Updated Performance Analyzer Commons library version:

| Setting | Old Value | New Value |
|---------|-----------|-----------|
| `paCommonsVersion` | 1.4.0 | 1.5.0 |

## Limitations

No functional changes or new limitations introduced. These are dependency-only updates.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#656](https://github.com/opensearch-project/performance-analyzer/pull/656) | Bump bouncycastle from 1.74 to 1.78.1 | Security advisories |
| [#698](https://github.com/opensearch-project/performance-analyzer/pull/698) | Bump PA to use 1.5.0 PA commons lib | Release 2.16 compatibility |
