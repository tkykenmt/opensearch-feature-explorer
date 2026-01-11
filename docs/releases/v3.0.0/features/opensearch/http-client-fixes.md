# HTTP Client Fixes

## Summary

OpenSearch v3.0.0 includes several important bug fixes for the Apache HttpClient 5.x transport layer. These fixes address protocol version parsing errors under JDK 16+, compression support for HTTP/2 cleartext (h2c) protocol, memory over-allocation in response buffer handling, and add HTTP/2 protocol version support to the HttpRequest API.

## Details

### What's New in v3.0.0

This release addresses four key issues in the HTTP client layer:

1. **JDK 16+ Protocol Version Parsing Fix**: Resolves `org.apache.hc.core5.http.ParseException: Invalid protocol version` errors when using JDK 16 or later
2. **H2C Compression Support**: Fixes compression handling for HTTP/2 cleartext (h2c) protocol upgrade
3. **Memory Allocation Optimization**: Prevents over-allocation in `HeapBufferedAsyncEntityConsumer` when consuming responses
4. **HTTP/2 Protocol Version Support**: Adds `HTTP_2_0` to the `HttpRequest.HttpVersion` enum

### Technical Changes

#### JDK 16+ TLS Fix (PR #4827)

The fix addresses an issue with Apache HttpClient 5.x and JDK 16+ where TLS negotiation fails due to missing application protocol information. The solution adds a custom `TlsDetailsFactory` to properly extract the application protocol from the SSL engine.

```java
final TlsStrategy tlsStrategy = ClientTlsStrategyBuilder.create()
    .setSslContext(SSLContext.getDefault())
    // See https://issues.apache.org/jira/browse/HTTPCLIENT-2219
    .setTlsDetailsFactory(new Factory<SSLEngine, TlsDetails>() {
        @Override
        public TlsDetails create(final SSLEngine sslEngine) {
            return new TlsDetails(sslEngine.getSession(), sslEngine.getApplicationProtocol());
        }
    })
    .build();
```

**Affected Components:**
- `RestClientBuilder`
- `ReindexSslConfig`
- `OpenSearchRestTestCase`
- `RestClientDocumentation`

#### H2C Compression Fix (PR #4944)

Fixed the Netty pipeline configuration for HTTP/2 cleartext protocol upgrade. The issues were:
- The `decoder_compress` handler was placed after `aggregator` and couldn't decode requests
- The `encoder` was redundant as it's already present in `HttpServerCodec`

```java
// Before (broken)
pipeline.replace(this, "aggregator", aggregator);
ch.pipeline().addLast("decoder_compress", new HttpContentDecompressor());
ch.pipeline().addLast("encoder", new HttpResponseEncoder());

// After (fixed)
pipeline.replace(this, "decoder_compress", new HttpContentDecompressor());
pipeline.addAfter("decoder_compress", "aggregator", aggregator);
```

**Root Cause:** The default `CloseableHttpAsyncClient` doesn't support compression out of the box, so RestClient and RestHighLevelClient tests didn't catch this issue. Third-party clients like opensearch-go use compression by default and exposed the bug.

#### Memory Allocation Fix (PR #9993)

The `HeapBufferedAsyncEntityConsumer` was over-allocating response buffers up to the configured limit (default 100MB) regardless of actual response size. This caused significant memory overhead when many requests run in parallel.

```java
// Before: Always allocated bufferLimitBytes
buffer = new ByteArrayBuffer(bufferLimitBytes);

// After: Allocate based on actual content length
int len = src.limit();
if (len < 0) {
    len = 4096;
} else if (len > bufferLimitBytes) {
    throw new ContentTooLongException(...);
}
buffer = new ByteArrayBuffer(len);
```

**Impact:** Tests that previously required 1GB heap on main branch now run with 512MB, matching 2.x branch performance.

#### HTTP/2 Protocol Version (PR #17248)

Added `HTTP_2_0` enum value to `HttpRequest.HttpVersion` to properly identify HTTP/2 requests in both Netty4 and Reactor Netty4 transports.

```java
// server/src/main/java/org/opensearch/http/HttpRequest.java
enum HttpVersion {
    HTTP_1_0,
    HTTP_1_1,
    HTTP_2_0  // New in v3.0.0
}
```

**Affected Files:**
- `server/src/main/java/org/opensearch/http/HttpRequest.java`
- `modules/transport-netty4/src/main/java/org/opensearch/http/netty4/Netty4HttpRequest.java`
- `plugins/transport-reactor-netty4/src/main/java/org/opensearch/http/reactor/netty4/ReactorNetty4HttpRequest.java`

### Migration Notes

These are bug fixes with no breaking changes. Users upgrading from earlier versions will automatically benefit from:
- Improved JDK 16+ compatibility
- Working compression with h2c protocol
- Reduced memory usage under parallel request load
- Proper HTTP/2 protocol identification

## Limitations

- HTTP/2 support still requires explicit configuration
- The memory fix applies only to `HeapBufferedAsyncEntityConsumer`; custom entity consumers may need similar updates

## Related PRs

| PR | Description |
|----|-------------|
| [#4827](https://github.com/opensearch-project/OpenSearch/pull/4827) | Fix 'org.apache.hc.core5.http.ParseException: Invalid protocol version' under JDK 16+ |
| [#4944](https://github.com/opensearch-project/OpenSearch/pull/4944) | Fix compression support for h2c protocol |
| [#9993](https://github.com/opensearch-project/OpenSearch/pull/9993) | Don't over-allocate in HeapBufferedAsyncEntityConsumer |
| [#17248](https://github.com/opensearch-project/OpenSearch/pull/17248) | Add HTTP/2 protocol support to HttpRequest.HttpVersion |

## References

- [Issue #9866](https://github.com/opensearch-project/OpenSearch/issues/9866): Performance regression report (memory over-allocation)
- [Issue opensearch-go#163](https://github.com/opensearch-project/opensearch-go/issues/163): H2C compression bug report
- [HTTPCLIENT-2219](https://issues.apache.org/jira/browse/HTTPCLIENT-2219): Apache HttpClient JDK 16+ issue

## Related Feature Report

- [Full HTTP Client documentation](../../../features/opensearch/http-client.md)
