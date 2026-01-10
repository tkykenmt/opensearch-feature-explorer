# Geospatial Deprecation Fixes

## Summary

This bugfix removes the deprecated `URL(String)` constructor usage in the Geospatial plugin's IP2Geo functionality. The change replaces the deprecated Java API with the recommended `URI.create(String).toURL()` pattern, ensuring compatibility with future Java versions and eliminating deprecation warnings.

## Details

### What's New in v3.3.0

The Geospatial plugin's IP2Geo processor has been updated to use modern Java URL handling APIs. The deprecated `new URL(String)` constructor, which has been marked for removal in future Java versions, has been replaced with the `URI.create(String).toURL()` pattern across all IP2Geo-related classes.

### Technical Changes

#### Code Migration Pattern

The change follows a consistent pattern across all affected files:

**Before (deprecated):**
```java
URL url = new URL(endpoint);
```

**After (recommended):**
```java
URL url = URI.create(endpoint).toURL();
```

#### Affected Components

| Component | File | Description |
|-----------|------|-------------|
| PutDatasourceRequest | `ip2geo/action/PutDatasourceRequest.java` | Validates endpoint URL when creating datasource |
| PutDatasourceTransportAction | `ip2geo/action/PutDatasourceTransportAction.java` | Validates manifest file URL |
| UpdateDatasourceRequest | `ip2geo/action/UpdateDatasourceRequest.java` | Validates endpoint URL when updating datasource |
| UpdateDatasourceTransportAction | `ip2geo/action/UpdateDatasourceTransportAction.java` | Validates manifest file and update interval |
| Ip2GeoSettings | `ip2geo/common/Ip2GeoSettings.java` | Validates datasource endpoint setting |
| URLDenyListChecker | `ip2geo/common/URLDenyListChecker.java` | Checks URL against deny list |
| DatasourceUpdateService | `ip2geo/jobscheduler/DatasourceUpdateService.java` | Gets header fields from manifest URL |

#### Exception Handling Update

The exception handling has been updated to catch `IllegalArgumentException` in addition to `MalformedURLException` and `URISyntaxException`, as `URI.create()` throws `IllegalArgumentException` for invalid URIs:

```java
// Before
catch (MalformedURLException | URISyntaxException e)

// After
catch (MalformedURLException | URISyntaxException | IllegalArgumentException e)
```

### Usage Example

The IP2Geo processor usage remains unchanged. This is an internal implementation change that does not affect the user-facing API:

```json
PUT /_plugins/geospatial/ip2geo/datasource/my-datasource
{
    "endpoint": "https://geoip.maps.opensearch.org/v1/geolite2-city/manifest.json",
    "update_interval_in_days": 3
}
```

### Migration Notes

No migration is required. This is a transparent internal change that maintains full backward compatibility with existing IP2Geo configurations and pipelines.

## Limitations

- No functional changes or new limitations introduced
- This is purely a code modernization change

## Related PRs

| PR | Description |
|----|-------------|
| [#795](https://github.com/opensearch-project/geospatial/pull/795) | Remove deprecated URL(String) usage |

## References

- [IP2Geo Documentation](https://docs.opensearch.org/3.0/ingest-pipelines/processors/ip2geo/): Official IP2Geo processor documentation
- [Java URL Deprecation](https://docs.oracle.com/en/java/javase/20/docs/api/java.base/java/net/URL.html): Java documentation on URL constructor deprecation

## Related Feature Report

- [Full feature documentation](../../../../features/geospatial/ip2geo.md)
