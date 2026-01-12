# Maintainer Updates

## Summary

Administrative updates to MAINTAINERS.md files across multiple OpenSearch repositories in v2.17.0. These changes include adding new maintainers and transitioning inactive maintainers to emeritus status.

## Details

### What's New in v2.17.0

This release includes governance updates across four repositories:

| Repository | Change Type | Description |
|------------|-------------|-------------|
| security | Addition | Added Nils Bandener (nibix) as maintainer |
| index-management | Transition | Moved inactive maintainers to emeritus status |
| dashboards | Addition | Added sumukhswamy as maintainer |
| notifications | Addition | Added riysaxen as maintainer |

### Maintainer Changes by Repository

#### Security Plugin
- **New Maintainer**: Nils Bandener (GitHub: [nibix](https://github.com/nibix))
- Backported to 2.x branch

#### Index Management Plugin
- **Emeritus Transition**: Non-active maintainers moved to emeritus status
- Maintainer list sorted alphabetically
- Related Issue: [#1230](https://github.com/opensearch-project/index-management/issues/1230)

#### OpenSearch Dashboards
- **New Maintainer**: sumukhswamy

#### Notifications Plugin
- **New Maintainer**: riysaxen

## Limitations

- These are administrative changes only; no functional impact on the software
- Some PR references in the original tracking may have incorrect numbers

## References

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#4673](https://github.com/opensearch-project/security/pull/4673) | security | Add Nils Bandener as maintainer (backport 2.x) |
| [#1233](https://github.com/opensearch-project/index-management/pull/1233) | index-management | Move non-active maintainers to emeritus |

### Issues (Design / RFC)
- [Issue #1230](https://github.com/opensearch-project/index-management/issues/1230): Index Management maintainer update request

## Related Feature Report

- [Maintainer Updates](../../../features/multi-plugin/maintainer-updates.md)
