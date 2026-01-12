# Secure Transport Settings

## Summary

The `SecureTransportSettingsProvider` and `SecureHttpTransportSettingsProvider` interfaces provide security-related settings for OpenSearch transport layer communication. They allow security plugins to configure SSL/TLS settings, exception handlers, and dynamic transport parameters for secure node-to-node and client-to-node communication.

## Details

### Architecture

```mermaid
graph TB
    subgraph "OpenSearch Core"
        A[NetworkModule] --> B[SecureNetty4Transport]
        A --> B2[ReactorNetty4HttpServerTransport]
        B --> C[SSLServerChannelInitializer]
        B --> D[SSLClientChannelInitializer]
    end
    
    subgraph "Security Plugin"
        E[OpenSearchSecurityPlugin] --> F[OpenSearchSecureSettingsFactory]
        F --> G[SecureTransportSettingsProvider]
        F --> G2[SecureHttpTransportSettingsProvider]
        H[SSLConfig] --> G
        H --> G2
    end
    
    subgraph "Configuration Sources"
        I[opensearch.yml] --> H
        J[Cluster Settings API] --> H
    end
    
    G --> B
    G2 --> B2
    C --> K[DualModeSslHandler]
    D --> L[SSL Engine]
```

### Data Flow

```mermaid
flowchart TB
    A[Cluster Settings Update] --> B[SSLConfig Listener]
    B --> C[Update Parameters]
    C --> D1[SecureTransportSettingsProvider.parameters]
    C --> D2[SecureHttpTransportSettingsProvider.parameters]
    D1 --> E1[SecureNetty4Transport]
    D2 --> E2[ReactorNetty4HttpServerTransport]
    E1 --> F[Apply to new connections]
    E2 --> F
```

### Components

| Component | Description |
|-----------|-------------|
| `SecureTransportSettingsProvider` | Interface for providing security settings to inter-node transport layer |
| `SecureHttpTransportSettingsProvider` | Interface for providing security settings to HTTP transport layer |
| `SecureTransportParameters` | Interface for dynamic inter-node transport parameters (e.g., dual mode) |
| `SecureHttpTransportParameters` | Interface for dynamic HTTP transport SSL parameters |
| `DefaultSecureTransportParameters` | Default implementation reading from static settings |
| `DefaultSecureHttpTransportParameters` | Default implementation returning empty/default values |
| `SecureNetty4Transport` | Netty-based secure transport implementation |
| `DualModeSslHandler` | Handler for SSL dual mode (mixed SSL/non-SSL connections) |
| `SSLConfig` | Security plugin class managing SSL configuration with cluster settings listener |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.security_config.ssl_dual_mode_enabled` | Enable SSL dual mode for mixed SSL/non-SSL transport | `false` |
| `plugins.security.ssl_only` | Run security plugin in SSL-only mode | `false` |
| `http.type` | HTTP transport type (use `reactor-netty4-secure` for secure reactor netty) | `netty4` |

### Interface Definitions

#### SecureTransportSettingsProvider

```java
@ExperimentalApi
public interface SecureTransportSettingsProvider {
    
    // Get transport adapter providers
    default Collection<TransportAdapterProvider<Transport>> getTransportAdapterProviders(Settings settings) {
        return Collections.emptyList();
    }
    
    // Get dynamic transport parameters
    default Optional<SecureTransportParameters> parameters(Settings settings) {
        return Optional.of(new DefaultSecureTransportParameters(settings));
    }
    
    // Build exception handler for transport errors
    Optional<TransportExceptionHandler> buildServerTransportExceptionHandler(
        Settings settings, Transport transport);
    
    // Build SSL engine for server transport
    Optional<SSLEngine> buildSecureServerTransportEngine(
        Settings settings, Transport transport) throws SSLException;
    
    // Build SSL engine for client transport
    Optional<SSLEngine> buildSecureClientTransportEngine(
        Settings settings, String hostname, int port) throws SSLException;
    
    @ExperimentalApi
    interface SecureTransportParameters {
        boolean dualModeEnabled();
        Optional<KeyManagerFactory> keyManagerFactory();
        Optional<String> sslProvider();
        Optional<String> clientAuth();
        Collection<String> protocols();
        Collection<String> cipherSuites();
        Optional<TrustManagerFactory> trustManagerFactory();
    }
}
```

#### SecureHttpTransportSettingsProvider

```java
@ExperimentalApi
public interface SecureHttpTransportSettingsProvider {
    
    // Get HTTP transport adapter providers
    default Collection<TransportAdapterProvider<HttpServerTransport>> getHttpTransportAdapterProviders(Settings settings) {
        return Collections.emptyList();
    }
    
    // Get dynamic HTTP transport parameters (added in v3.2.0)
    default Optional<SecureHttpTransportParameters> parameters(Settings settings) {
        return Optional.of(new DefaultSecureHttpTransportParameters());
    }
    
    // Build exception handler for HTTP transport errors
    Optional<TransportExceptionHandler> buildHttpServerExceptionHandler(
        Settings settings, HttpServerTransport transport);
    
    // Build SSL engine for HTTP server transport
    Optional<SSLEngine> buildSecureHttpServerEngine(
        Settings settings, HttpServerTransport transport) throws SSLException;
    
    @ExperimentalApi
    interface SecureHttpTransportParameters {
        Optional<KeyManagerFactory> keyManagerFactory();
        Optional<String> sslProvider();
        Optional<String> clientAuth();
        Collection<String> protocols();
        Collection<String> cipherSuites();
        Optional<TrustManagerFactory> trustManagerFactory();
    }
}
```

### Usage Example

Dynamically toggle SSL dual mode via cluster settings:

```bash
# Enable dual mode (allow mixed SSL/non-SSL connections)
curl -XPUT https://localhost:9200/_cluster/settings \
  -k -H "Content-Type: application/json" \
  -d '{"persistent": {"plugins.security_config.ssl_dual_mode_enabled": true}}'

# Disable dual mode (require SSL for all connections)
curl -XPUT https://localhost:9200/_cluster/settings \
  -k -H "Content-Type: application/json" \
  -d '{"persistent": {"plugins.security_config.ssl_dual_mode_enabled": false}}'
```

Enable reactor-netty secure HTTP transport:

```yaml
# opensearch.yml
http.type: reactor-netty4-secure
```

## Limitations

- Both `SecureTransportParameters` and `SecureHttpTransportParameters` interfaces are marked as `@ExperimentalApi` and may change
- Dynamic updates only affect new connections; existing connections are not affected
- The `SecureHttpTransportParameters` default implementation returns empty values, requiring plugins to provide actual configuration

## Change History

- **v3.2.0** (2025-07-15): Added `SecureHttpTransportParameters` interface to `SecureHttpTransportSettingsProvider` for cleaner SSL configuration in Reactor Netty 4 HTTP transport
- **v2.18.0** (2024-10-29): Added `parameters()` method and `SecureTransportParameters` interface to support dynamic SSL dual mode settings

## References

### Documentation
- [Network Settings](https://docs.opensearch.org/3.0/install-and-configure/configuring-opensearch/network-settings/): Official network configuration documentation
- [TLS Configuration](https://docs.opensearch.org/3.0/security/configuration/tls/): Official TLS documentation
- [PR #18572](https://github.com/opensearch-project/OpenSearch/pull/18572): SecureHttpTransportParameters implementation
- [PR #16387](https://github.com/opensearch-project/OpenSearch/pull/16387): SecureTransportParameters implementation
- [Security PR #4820](https://github.com/opensearch-project/security/pull/4820): Security plugin implementation

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.2.0 | [#18572](https://github.com/opensearch-project/OpenSearch/pull/18572) | Introduce SecureHttpTransportParameters experimental API |   |
| v2.18.0 | [#16387](https://github.com/opensearch-project/OpenSearch/pull/16387) | Add method to return dynamic SecureTransportParameters |   |
| v2.18.0 | [#4820](https://github.com/opensearch-project/security/pull/4820) | Security plugin: propagate dual mode from cluster settings |   |

### Issues (Design / RFC)
- [Issue #18559](https://github.com/opensearch-project/OpenSearch/issues/18559): HTTP/2 communication bug with reactor-netty
