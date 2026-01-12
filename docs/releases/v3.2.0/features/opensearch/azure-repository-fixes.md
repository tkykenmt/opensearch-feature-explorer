---
tags:
  - security
---

# Azure Repository Fixes

## Summary

This bugfix resolves an issue with SOCKS5 proxy authentication settings (username and password) for the Azure repository plugin. Previously, SOCKS5 credentials were incorrectly configured using the JDK `Authenticator` class, but the Azure SDK client requires these credentials to be set through the `ProxyOptions` class.

## Details

### What's New in v3.2.0

The fix corrects the proxy authentication mechanism for Azure Blob Storage connections when using SOCKS5 proxies with username/password authentication.

### Technical Changes

#### Problem

When configuring a SOCKS5 proxy with authentication for the Azure repository plugin, the credentials were being set using Java's `Authenticator.setDefault()` method:

```java
// Previous incorrect implementation
Authenticator.setDefault(new Authenticator() {
    @Override
    protected PasswordAuthentication getPasswordAuthentication() {
        return new PasswordAuthentication(
            proxySettings.getUsername(), 
            proxySettings.getPassword().toCharArray()
        );
    }
});
clientBuilder.proxy(new ProxyOptions(proxySettings.getType().toProxyType(), proxySettings.getAddress()));
```

This approach doesn't work with the Azure SDK because the Azure client uses its own `ProxyOptions` class for proxy configuration, which has a dedicated method for setting credentials.

#### Solution

The fix properly configures proxy credentials through the Azure SDK's `ProxyOptions.setCredentials()` method:

```java
// Fixed implementation
final ProxyOptions proxyOptions = new ProxyOptions(
    proxySettings.getType().toProxyType(), 
    proxySettings.getAddress()
);
if (proxySettings.isAuthenticated()) {
    proxyOptions.setCredentials(proxySettings.getUsername(), proxySettings.getPassword());
}
clientBuilder.proxy(proxyOptions);
```

#### Changed Files

| File | Change |
|------|--------|
| `AzureStorageService.java` | Removed JDK Authenticator usage, added ProxyOptions.setCredentials() |

### Usage Example

To configure a SOCKS5 proxy with authentication for Azure repository:

```yaml
# opensearch.yml
azure.client.default.proxy.type: socks5
azure.client.default.proxy.host: proxy.example.com
azure.client.default.proxy.port: 1080
```

```bash
# Add proxy credentials to keystore
./bin/opensearch-keystore add azure.client.default.proxy.username
./bin/opensearch-keystore add azure.client.default.proxy.password
```

### Migration Notes

No migration required. This is a transparent bugfix that corrects the behavior of existing proxy authentication settings.

## Limitations

- This fix specifically addresses SOCKS5 proxy authentication
- HTTP/HTTPS proxy authentication was not affected by this issue

## References

### Documentation
- [Azure Repository Plugin Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [Azure SDK ProxyOptions](https://learn.microsoft.com/en-us/java/api/com.azure.core.http.proxyoptions)

### Pull Requests
| PR | Description |
|----|-------------|
| [#18904](https://github.com/opensearch-project/OpenSearch/pull/18904) | Fix socks5 user password settings for Azure repo |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-azure-repository.md)
