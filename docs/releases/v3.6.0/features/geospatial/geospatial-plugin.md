---
tags:
  - geospatial
---
# Geospatial Plugin

## Summary

Fixed a typo in the `MAX_MULTI_GEOMETRIES` cluster setting key used for GeoJSON upload validation. The setting name was corrected from `plugins.geospatial.geojson.max_multi_gemoetries` to `plugins.geospatial.geojson.max_multi_geometries`.

## Details

### What's New in v3.6.0

The `GeospatialSettings.java` class contained a typo in the setting key for `MAX_MULTI_GEOMETRIES`. The misspelled setting `plugins.geospatial.geojson.max_multi_gemoetries` ("gemoetries") was corrected to `plugins.geospatial.geojson.max_multi_geometries` ("geometries").

This setting controls the maximum number of multi geometries allowed while parsing uploaded GeoJSON data. The default value remains `100`. The official documentation already referenced the correct spelling, so this fix aligns the code with the documentation.

### Technical Changes

| Before | After |
|--------|-------|
| `plugins.geospatial.geojson.max_multi_gemoetries` | `plugins.geospatial.geojson.max_multi_geometries` |

The change is a single-line fix in `GeospatialSettings.java`:

```java
public static final Setting<Integer> MAX_MULTI_GEOMETRIES = Setting.intSetting(
    "plugins.geospatial.geojson.max_multi_geometries",  // was "max_multi_gemoetries"
    100,
    Setting.Property.NodeScope,
    Setting.Property.Dynamic
);
```

### Migration Note

If you previously configured the old (typo'd) setting name `plugins.geospatial.geojson.max_multi_gemoetries` in your cluster settings, you will need to update it to `plugins.geospatial.geojson.max_multi_geometries` after upgrading to v3.6.0. The old setting name will no longer be recognized.

## Limitations

- This is a breaking change for clusters that explicitly configured the old setting name

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#837](https://github.com/opensearch-project/geospatial/pull/837) | Fix typo in max multi geometries validation cluster setting | - |
