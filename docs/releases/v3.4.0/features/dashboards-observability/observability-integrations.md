---
tags:
  - domain/observability
  - component/dashboards
  - observability
  - security
---
# Observability Integrations

## Summary

This enhancement improves the static file serving interface for integrations by adding proper image type validation and SVG sanitization. Previously, the integrations router could serve non-image files, causing rendering issues when displayed in `<img>` tags. This change introduces a clean error response for unsupported file types and sanitizes SVG content to prevent XSS attacks.

## Details

### What's New in v3.4.0

- Added `serveStaticImage()` function to handle static file serving with proper content type validation
- Implemented SVG sanitization using `isomorphic-dompurify` to prevent XSS vulnerabilities
- Added explicit support for common image formats: GIF, JPEG, PNG, TIFF, WebP, AVIF
- Returns HTTP 400 error for unsupported image types instead of serving potentially malicious content

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `serveStaticImage()` | New function that validates image types and sanitizes SVG content before serving |
| `RequestError` interface | TypeScript interface for consistent error handling |

#### Security Improvements

The change addresses a security concern where arbitrary files could be served through the static endpoint:

```typescript
export const serveStaticImage = (
  path: string,
  content: Buffer,
  response: OpenSearchDashboardsResponseFactory
): OpenSearchDashboardsResponse => {
  const mtype = mime.getType(path);
  switch (mime.getType(path)) {
    case 'image/gif':
    case 'image/jpeg':
    case 'image/png':
    case 'image/tiff':
    case 'image/webp':
    case 'image/avif':
      return response.ok({
        headers: { 'Content-Type': mtype },
        body: content,
      });
    case 'image/svg+xml':
      return response.ok({
        headers: { 'Content-Type': mtype },
        body: DOMPurify.sanitize(content.toString('utf8')),
      });
    default:
      return response.custom({
        body: `not a supported image type: ${mtype}`,
        statusCode: 400,
      });
  }
};
```

#### New Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| `isomorphic-dompurify` | ^2.33.0 | Server-side SVG sanitization |

### Usage Example

The static file endpoint now properly validates and serves integration assets:

```
GET /api/integrations/repository/{id}/static/{path}
```

- For supported image types (GIF, JPEG, PNG, etc.): Returns the image with correct Content-Type
- For SVG files: Returns sanitized SVG content (scripts and malicious elements removed)
- For unsupported types: Returns HTTP 400 with error message

## Limitations

- Only image file types are supported for static serving
- SVG sanitization may remove legitimate interactive elements
- BMP and other less common image formats are not supported

## References

### Documentation
- [Integrations in OpenSearch Dashboards](https://docs.opensearch.org/3.0/dashboards/integrations/index/): Official documentation
- [DOMPurify](https://github.com/cure53/DOMPurify): XSS sanitization library

### Pull Requests
| PR | Description |
|----|-------------|
| [#2530](https://github.com/opensearch-project/dashboards-observability/pull/2530) | Clean up interface for integrations static serving |

## Related Feature Report

- [Full feature documentation](../../../../features/observability/observability-integrations.md)
