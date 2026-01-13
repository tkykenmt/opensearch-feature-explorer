---
tags:
  - opensearch
---
# gRPC Settings

## Summary

This release fixes inconsistencies in gRPC transport settings naming and removes lingering HTTP terminology from the codebase. The setting `aux.transport.experimental-transport-grpc.ports` is renamed to `aux.transport.experimental-transport-grpc.port` for consistency with other OpenSearch port settings like `http.port`.

## Details

### What's New in v2.19.0

**Setting Rename:**
The auxiliary transport port setting has been renamed for consistency:

| Before | After |
|--------|-------|
| `aux.transport.experimental-transport-grpc.ports` | `aux.transport.experimental-transport-grpc.port` |

**Terminology Cleanup:**
Internal variable names in `Netty4GrpcServerTransport.java` have been corrected:

| Before | After |
|--------|-------|
| `httpBindHost` | `grpcBindHost` |
| `httpPublishHost` | `grpcPublishHost` |

**Debug Logging:**
Added debug logging for gRPC transport settings during initialization to aid troubleshooting.

### Technical Changes

The following files were modified:

| File | Change |
|------|--------|
| `NetworkPlugin.java` | Renamed `AUX_TRANSPORT_PORTS` to `AUX_TRANSPORT_PORT`, changed affix from `ports` to `port` |
| `Netty4GrpcServerTransport.java` | Updated setting reference, fixed variable names, added debug logging |
| `GrpcPlugin.java` | Updated import and setting reference |
| `Security.java` | Updated setting reference for socket permissions |

### Migration

If you are using the gRPC transport plugin with a custom port configuration, update your `opensearch.yml`:

```yaml
# Before (v2.18.0 and earlier)
aux.transport.experimental-transport-grpc.ports: 9400-9500

# After (v2.19.0+)
aux.transport.experimental-transport-grpc.port: 9400-9500
```

## Limitations

- This is a breaking change for users who configured custom gRPC ports using the old setting name
- The gRPC transport remains experimental in v2.19.0

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#17037](https://github.com/opensearch-project/OpenSearch/pull/17037) | Fix GRPC AUX_TRANSPORT_PORT and SETTING_GRPC_PORT settings and remove lingering HTTP terminology | [#16556](https://github.com/opensearch-project/OpenSearch/issues/16556) |
