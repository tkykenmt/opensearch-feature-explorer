---
tags:
  - domain/observability
  - component/server
  - indexing
  - ml
  - security
---
# Doc Request Resource Type Support

## Summary

This release adds resource type support to `DocRequest` implementations in the Anomaly Detection plugin and OpenSearch core. The `type()` method enables the Security plugin's resource sharing framework to identify and authorize access to specific resource types (anomaly detectors, forecasters) rather than treating all document operations uniformly.

## Details

### What's New in v3.3.0

The `DocRequest` interface now includes a `type()` method that plugins can override to specify the resource type for authorization purposes. This change enables:

1. **Resource-level authorization**: The Security plugin can now distinguish between different resource types within the same index
2. **Plugin onboarding to resource sharing**: Anomaly Detection plugin requests now return appropriate resource types (`anomaly-detector` or `forecaster`)
3. **Multiple resource types per index**: Different resource types can coexist in the same system index with separate access controls

### Technical Changes

#### Core OpenSearch Change

The `DocRequest` interface adds a new default method:

```java
public interface DocRequest {
    String index();
    String id();
    
    /**
     * Get the type of the request for resource sharing context.
     * Plugins override this to specify their resource type.
     * @return the type (default: "indices")
     */
    default String type() {
        return "indices";
    }
}
```

#### Anomaly Detection Plugin Changes

The following request classes now override `type()`:

| Request Class | Resource Type |
|---------------|---------------|
| `IndexAnomalyDetectorRequest` | `anomaly-detector` |
| `PreviewAnomalyDetectorRequest` | `anomaly-detector` |
| `IndexForecasterRequest` | `forecaster` |
| `DeleteConfigRequest` | `anomaly-detector` or `forecaster` (based on index) |
| `GetConfigRequest` | `anomaly-detector` or `forecaster` (based on index) |
| `JobRequest` | `anomaly-detector` or `forecaster` (based on index) |
| `SuggestConfigParamRequest` | `anomaly-detector` or `forecaster` (based on context) |

#### Resource Type Constants

```java
// ADCommonName.java
public static final String AD_RESOURCE_TYPE = "anomaly-detector";

// ForecastCommonName.java  
public static final String FORECAST_RESOURCE_TYPE = "forecaster";
```

### Usage Example

When the Security plugin intercepts a request, it can now determine the resource type:

```java
// Security plugin evaluation
DocRequest request = (DocRequest) actionRequest;
String resourceType = request.type();  // Returns "anomaly-detector"
String resourceId = request.id();

// Evaluate access based on resource type and sharing configuration
boolean hasAccess = resourceAccessEvaluator.evaluate(user, resourceType, resourceId, action);
```

### Migration Notes

- No migration required for existing anomaly detectors or forecasters
- Resource sharing must be explicitly enabled via Security plugin settings
- Existing `filter_by_backend_role` behavior remains available as fallback

## Limitations

- Resource sharing requires Security plugin with experimental feature enabled
- Only single-document operations are supported (not bulk operations)

## References

### Blog Posts
- [Blog: Introducing resource sharing](https://opensearch.org/blog/introducing-resource-sharing-a-new-access-control-model-for-opensearch/): A new access control model for OpenSearch

### Pull Requests
| PR | Description |
|----|-------------|
| [opensearch#19313](https://github.com/opensearch-project/OpenSearch/pull/19313) | Add new extensible method to DocRequest to specify type |
| [anomaly-detection#1566](https://github.com/opensearch-project/anomaly-detection/pull/1566) | Adds resource types to DocRequests |

### Issues (Design / RFC)
- [Issue #4500](https://github.com/opensearch-project/security/issues/4500): Resource Permissions and Sharing

## Related Feature Report

- Full feature documentation
