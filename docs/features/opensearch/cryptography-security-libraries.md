---
tags:
  - security
---

# Cryptography & Security Libraries

## Summary

OpenSearch uses Bouncy Castle cryptographic libraries for SSL/TLS operations, PEM file parsing, certificate handling, and plugin signature verification. Starting with v3.0.0, OpenSearch migrated from standard Bouncy Castle libraries to their FIPS-certified counterparts (BC-FIPS), enabling a path toward FIPS 140-2/140-3 compliance for organizations with strict security requirements.

## Details

### Architecture

```mermaid
graph TB
    subgraph "OpenSearch Cryptography Stack"
        Core[OpenSearch Core]
        SSL[SSL Config Library]
        REST[REST Client]
        Plugin[Plugin CLI]
        
        Core --> SSL
        Core --> REST
        Core --> Plugin
    end
    
    subgraph "BC-FIPS Libraries"
        BCFIPS[bc-fips<br/>Core Provider]
        BCPKIX[bcpkix-fips<br/>PKIX/CMS Support]
        BCTLS[bctls-fips<br/>TLS/JSSE Provider]
        BCUTIL[bcutil-fips<br/>Utilities]
        BCPG[bcpg-fips<br/>OpenPGP Support]
    end
    
    SSL --> BCFIPS
    SSL --> BCPKIX
    SSL --> BCTLS
    SSL --> BCUTIL
    REST --> BCFIPS
    REST --> BCTLS
    REST --> BCUTIL
    Plugin --> BCFIPS
    Plugin --> BCPG
```

### Data Flow

```mermaid
flowchart TB
    subgraph "PEM Key Loading"
        PEM[PEM File] --> Parser[PEMParser]
        Parser --> |Encrypted| Decrypt[Decryptor]
        Parser --> |Unencrypted| PKI[PrivateKeyInfo]
        Decrypt --> PKI
        PKI --> Converter[JcaPEMKeyConverter]
        Converter --> Key[PrivateKey]
    end
    
    subgraph "TLS Handshake"
        Key --> KMF[KeyManagerFactory]
        Cert[Certificate] --> TMF[TrustManagerFactory]
        KMF --> SSLCtx[SSLContext]
        TMF --> SSLCtx
        SSLCtx --> Conn[Secure Connection]
    end
```

### Components

| Component | Library | Purpose |
|-----------|---------|---------|
| Core Provider | `bc-fips` | FIPS-certified JCE provider for cryptographic operations |
| PKIX Support | `bcpkix-fips` | Certificate parsing, CMS, PKCS operations |
| TLS Provider | `bctls-fips` | JSSE provider for TLS/SSL connections |
| Utilities | `bcutil-fips` | ASN.1, Base64, and other utility functions |
| OpenPGP | `bcpg-fips` | Plugin signature verification |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `security.provider.1` | Primary JCE security provider | `BouncyCastleFipsProvider` |
| `security.provider.2` | JSSE provider for TLS | `BouncyCastleJsseProvider` |
| `security.provider.3` | Fallback provider | `SUN` |
| `security.provider.4` | GSS-API provider | `SunJGSS` |
| `ssl.KeyManagerFactory.algorithm` | Algorithm for key managers | `PKIX` |
| `ssl.TrustManagerFactory.algorithm` | Algorithm for trust managers | `PKIX` |

### Usage Example

#### Loading Private Keys

```java
// PemUtils automatically handles various key formats
PrivateKey key = PemUtils.readPrivateKey(
    Paths.get("/path/to/key.pem"),
    () -> "password".toCharArray()
);
```

#### Supported Key Formats

```yaml
# PKCS#8 Unencrypted
-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----

# PKCS#8 Encrypted
-----BEGIN ENCRYPTED PRIVATE KEY-----
...
-----END ENCRYPTED PRIVATE KEY-----

# PKCS#1 RSA
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----

# EC Key
-----BEGIN EC PRIVATE KEY-----
...
-----END EC PRIVATE KEY-----

# DSA Key
-----BEGIN DSA PRIVATE KEY-----
...
-----END DSA PRIVATE KEY-----
```

#### Configuring SSL Context with BC-FIPS

```java
SecureRandom secureRandom = SecureRandom.getInstance("DEFAULT", "BCFIPS");

KeyStore keyStore = KeyStore.getInstance("JKS");
keyStore.load(keyStoreStream, password);

KeyManagerFactory kmf = KeyManagerFactory.getInstance("PKIX", "BCJSSE");
kmf.init(keyStore, password);

TrustManagerFactory tmf = TrustManagerFactory.getInstance("PKIX", "BCJSSE");
tmf.init(trustStore);

SSLContext sslContext = SSLContextBuilder.create()
    .setProvider("BCJSSE")
    .setProtocol("TLSv1.3")
    .setSecureRandom(secureRandom)
    .loadKeyMaterial(keyStore, password)
    .loadTrustMaterial(trustStore, null)
    .build();
```

## Limitations

- BC-FIPS runs in "general mode" by default; approved-only FIPS mode requires additional JVM configuration
- Legacy PBE algorithms (e.g., PBKDF-OPENSSL) not available in FIPS mode
- Some plugins with hard Bouncy Castle dependencies may require updates
- FIPS mode restricts certain cryptographic algorithms and key sizes

## Change History

- **v3.1.0** (2026-01-10): Updated FipsMode check to catch NoSuchMethodError for improved compatibility with security plugin during BC-FIPS transition
- **v3.0.0** (2025-05-06): Migrated from standard BC to BC-FIPS libraries; refactored PemUtils to use BC for PEM parsing; added java.security configuration for BC-FIPS providers

## Related Features
- [OpenSearch Dashboards](../opensearch-dashboards/ai-chat.md)

## References

### Documentation
- [Bouncy Castle FIPS Documentation](https://www.bouncycastle.org/fips-java/): Official BC-FIPS documentation
- [PR #14912](https://github.com/opensearch-project/OpenSearch/pull/14912): Original comprehensive FIPS support PR

### Blog Posts
- [Blog: Finding a replacement for JSM in OpenSearch 3.0](https://opensearch.org/blog/finding-a-replacement-for-jsm-in-opensearch-3-0/): Security architecture changes in 3.0

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.1.0 | [#18427](https://github.com/opensearch-project/OpenSearch/pull/18427) | Update FipsMode check to catch NoSuchMethodError | [#4915](https://github.com/opensearch-project/security/issues/4915) |
| v3.0.0 | [#17393](https://github.com/opensearch-project/OpenSearch/pull/17393) | Use BC libraries to parse PEM files, increase key length |   |
| v3.0.0 | [#17507](https://github.com/opensearch-project/OpenSearch/pull/17507) | Migrate BC libs to their FIPS counterparts |   |

### Issues (Design / RFC)
- [Issue #3420](https://github.com/opensearch-project/security/issues/3420): RFC - Proposal for supporting FIPS 140-2 enforced mode
- [Issue #4254](https://github.com/opensearch-project/security/issues/4254): RFC - FIPS-140 Compliance Roadmap for OpenSearch
