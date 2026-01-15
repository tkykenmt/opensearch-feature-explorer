---
tags:
  - opensearch-dashboards
---
# VisBuilder GA

## Summary

VisBuilder has been promoted from experimental to production status in OpenSearch Dashboards v2.16.0. This change removes the experimental banner, beaker icon, and lab mode dependency, making VisBuilder a fully supported visualization tool available to all users by default.

## Details

### What's New in v2.16.0

VisBuilder is now generally available (GA) as a production-ready visualization tool. Key changes include:

| Change | Description |
|--------|-------------|
| Experimental banner removed | No longer displays "This editor is experimental" warning |
| Beaker icon removed | Saved VisBuilder visualizations no longer show experimental icon |
| Lab mode dependency removed | VisBuilder loads regardless of `visualize:enableLabs` setting |
| Stage property updated | Changed from `experimental` to `production` |

### Technical Changes

The following components were removed or modified:

| File | Change |
|------|--------|
| `experimental_info.tsx` | Removed - experimental banner component |
| `disabled_embeddable.tsx` | Removed - disabled state for lab mode |
| `disabled_visualization.tsx` | Removed - disabled visualization message |
| `workspace.tsx` | Removed ExperimentalInfo component |
| `plugin.ts` | Removed `stage: 'experimental'` property |
| `vis_builder_embeddable_factory.tsx` | Removed lab mode check and DisabledEmbeddable |
| `types.ts` | Updated stage type to only allow `'production'` |

### User Impact

- VisBuilder is now available without enabling experimental features
- Existing VisBuilder visualizations continue to work without changes
- No migration required for saved visualizations
- VisBuilder visualizations can be embedded in dashboards without lab mode

## Limitations

None specific to this change. VisBuilder retains all existing functionality.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6436](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6436) | Change VisBuilder from experimental to production | [#6435](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6435) |
| [#6971](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6971) | Backport to 2.x branch | - |

### Documentation
- [VisBuilder Documentation](https://docs.opensearch.org/2.16/dashboards/visualize/visbuilder/)
