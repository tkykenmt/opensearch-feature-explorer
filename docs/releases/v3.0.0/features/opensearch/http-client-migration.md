---
tags:
  - search
---

# HTTP Client Migration

## Summary

OpenSearch 3.0.0 migrates client transports from Apache HttpComponents/Core 4.x to Apache HttpClient/Core 5.x. This is a breaking change that affects all OpenSearch clients (rest-client, RHLC, opensearch-java) and provides access to modern HTTP features including HTTP/2 support while moving away from end-of-life libraries.

## Details

### What's New in v3.0.0

The migration updates the underlying HTTP client library used by OpenSearch's REST clients from the legacy Apache HttpComponents 4.x to the modern Apache HttpClient 5.x. This change was necessary because Apache HttpComponents 4.x has reached end-of-life status.

### Technical Changes

#### Package Migration

The migration involves updating import statements from the old `org.apache.http` packages to the new `org.apache.hc` packages:

| Old Package | New Package |
|-------------|-------------|
| `org.apache.http.HttpHost` | `org.apache.hc.core5.http.HttpHost` |
| `org.apache.http.HttpEntity` | `org.apache.hc.core5.http.HttpEntity` |
| `org.apache.http.client.methods.HttpGet` | `org.apache.hc.client5.http.classic.methods.HttpGet` |
| `org.apache.http.client.methods.HttpPost` | `org.apache.hc.client5.http.classic.methods.HttpPost` |
| `org.apache.http.client.methods.HttpPut` | `org.apache.hc.client5.http.classic.methods.HttpPut` |
| `org.apache.http.client.methods.HttpDelete` | `org.apache.hc.client5.http.classic.methods.HttpDelete` |
| `org.apache.http.entity.ContentType` | `org.apache.hc.core5.http.ContentType` |
| `org.apache.http.nio.entity.NByteArrayEntity` | `org.apache.hc.core5.http.io.entity.ByteArrayEntity` |
| `org.apache.http.nio.entity.NStringEntity` | `org.apache.hc.core5.http.io.entity.StringEntity` |
| `org.apache.http.message.BasicStatusLine` | `org.apache.hc.core5.http.message.StatusLine` |
| `org.apache.http.message.BasicRequestLine` | `org.apache.hc.core5.http.message.RequestLine` |

#### API Changes

| Change | Description |
|--------|-------------|
| `ContentType.getValue()` | Now returns `String` directly instead of `Header` |
| `NByteArrayEntity` | Replaced with `ByteArrayEntity` |
| `NStringEntity` | Replaced with `StringEntity` |
| `BasicHttpResponse` | Replaced with `BasicClassicHttpResponse` |
| `HttpResponse` | Replaced with `ClassicHttpResponse` |

#### New Dependencies

| Dependency | Version |
|------------|---------|
| `httpclient5` | 5.1.3 |
| `httpcore5` | 5.1.4 |

### Usage Example

```java
// Before (Apache HttpClient 4.x)
import org.apache.http.HttpHost;
import org.apache.http.entity.ContentType;
import org.apache.http.nio.entity.NByteArrayEntity;

HttpHost host = new HttpHost("localhost", 9200, "https");
NByteArrayEntity entity = new NByteArrayEntity(bytes, ContentType.APPLICATION_JSON);

// After (Apache HttpClient 5.x)
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.io.entity.ByteArrayEntity;

HttpHost host = new HttpHost("https", "localhost", 9200);
ByteArrayEntity entity = new ByteArrayEntity(bytes, ContentType.APPLICATION_JSON);
```

### Migration Notes

1. **Update imports**: Replace all `org.apache.http` imports with corresponding `org.apache.hc` packages
2. **HttpHost constructor**: The constructor parameter order has changed - protocol comes first in 5.x
3. **Entity classes**: Replace `NByteArrayEntity` and `NStringEntity` with `ByteArrayEntity` and `StringEntity`
4. **ContentType access**: `entity.getContentType()` now returns `String` directly instead of a `Header` object
5. **Response classes**: Use `ClassicHttpResponse` and `BasicClassicHttpResponse` instead of `HttpResponse` and `BasicHttpResponse`

## Limitations

- Custom HTTP client configurations may need to be updated to use the new API
- Third-party plugins using the REST client directly will need to update their dependencies
- The migration is a breaking change and requires code modifications for custom client implementations

## References

### Documentation
- [Java Client Documentation](https://docs.opensearch.org/3.0/clients/java/): Official Java client documentation with Apache HttpClient 5 examples
- [Apache HttpClient 5.x Migration Guide](https://hc.apache.org/httpcomponents-client-5.1.x/migration-guide/index.html): Official Apache migration guide

### Pull Requests
| PR | Description |
|----|-------------|
| [#4459](https://github.com/opensearch-project/OpenSearch/pull/4459) | Migrate client transports to Apache HttpClient / Core 5.x |

### Issues (Design / RFC)
- [Issue #4256](https://github.com/opensearch-project/OpenSearch/issues/4256): Feature request for migration

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-http-client.md)
