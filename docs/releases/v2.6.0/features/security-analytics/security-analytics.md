---
tags:
  - security-analytics
---
# Security Analytics

## Summary

OpenSearch 2.6.0 introduces 12 new feature(s) and 10 enhancement(s) to Security Analytics, along with 15 bug fixes.

## Details

### New Features

- **Added API to fetch all log types/rule categories**: Added in PR #327.
- **Added new log types**: Added in PR #439.
- **Added create dashboard feature**: Added in PR #437.
- **Improvements for field mappings**: Added in PR #432.
- **Added multi select data source for creating detector**: Added in PR #424.
- **Chart vertical domain UX improvement**: Added in PR #372.
- **Various detectors page UX/UI improvements**: Added in PR #387.
- **Various findings page UX/UI improvements**: Added in PR #369.
- **Upgrade vega tooltips to use custom formatting**: Added in PR #368.
- **Adds validation for trigger name in creating alert flyout**: Added in PR #367.
- **Create index pattern**: Added in PR #366.
- **Provide all unmapped fields when editing Rule field mapping**: Added in PR #353.

### Enhancements

- **Adds timestamp field alias and sets time range filter in bucket level monitor**
- **Update others_application mappings**
- **Update others_apt mappings.**
- **Index template conflict resolve; GetIndexMappings API changes**
- **Add nesting level to yaml constructor**
- **Update others_cloud mappings**
- **Update others_compliance mappings**
- **Update others_web mappings**
- **Log message change for debugging**
- **Windows CI Support**

### Bug Fixes

- Service Returns Unhandled Error Response
- Correct linux mapping error
- GetIndexMapping API timestamp alias bugfix
- Query_field_names bugfix
- Fixes bad breadcrumbs on page reload
- Fixes UX/UI bugs for edit detector page
- Add breadcrumbs for create detector page
- Removes sidebar from edit detector page
- Fixes interval field validation
- Fixes chart tooltip delay
- Fixes wrong alert colors
- Readme update
- Baselined MAINTAINERS and CODEOWNERS docs.
- Bumped version to 2.6.
- Updated lint-staged for consistency with other plugins.

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#327](https://github.com/opensearch-project/security/pull/327) | Added API to fetch all log types/rule categories | security |
| [#439](https://github.com/opensearch-project/security/pull/439) | Added new log types | security |
| [#437](https://github.com/opensearch-project/security/pull/437) | Added create dashboard feature | security |
| [#432](https://github.com/opensearch-project/security/pull/432) | Improvements for field mappings | security |
| [#424](https://github.com/opensearch-project/security/pull/424) | Added multi select data source for creating detector | security |
| [#372](https://github.com/opensearch-project/security/pull/372) | Chart vertical domain UX improvement | security |
| [#387](https://github.com/opensearch-project/security/pull/387) | Various detectors page UX/UI improvements | security |
| [#369](https://github.com/opensearch-project/security/pull/369) | Various findings page UX/UI improvements | security |
| [#368](https://github.com/opensearch-project/security/pull/368) | Upgrade vega tooltips to use custom formatting | security |
| [#367](https://github.com/opensearch-project/security/pull/367) | Adds validation for trigger name in creating alert flyout | security |
| [#366](https://github.com/opensearch-project/security/pull/366) | Create index pattern | security |
| [#353](https://github.com/opensearch-project/security/pull/353) | Provide all unmapped fields when editing Rule field mapping | security |
| [#262](https://github.com/opensearch-project/security/pull/262) | Adds timestamp field alias and sets time range filter in bucket level monitor | security |
| [#277](https://github.com/opensearch-project/security/pull/277) | Update others_application mappings | security |
| [#278](https://github.com/opensearch-project/security/pull/278) | Update others_apt mappings. | security |
| [#283](https://github.com/opensearch-project/security/pull/283) | Index template conflict resolve; GetIndexMappings API changes | security |
| [#286](https://github.com/opensearch-project/security/pull/286) | Add nesting level to yaml constructor | security |
| [#301](https://github.com/opensearch-project/security/pull/301) | Update others_cloud mappings | security |
| [#302](https://github.com/opensearch-project/security/pull/302) | Update others_compliance mappings | security |
| [#304](https://github.com/opensearch-project/security/pull/304) | Update others_web mappings | security |
| [#321](https://github.com/opensearch-project/security/pull/321) | Log message change for debugging | security |
| [#1320](https://github.com/opensearch-project/security/pull/1320) | Windows CI Support | security |
| [#248](https://github.com/opensearch-project/security/pull/248) | Service Returns Unhandled Error Response | security |
| [#263](https://github.com/opensearch-project/security/pull/263) | Correct linux mapping error | security |
| [#293](https://github.com/opensearch-project/security/pull/293) | GetIndexMapping API timestamp alias bugfix | security |
| [#335](https://github.com/opensearch-project/security/pull/335) | Query_field_names bugfix | security |
| [#395](https://github.com/opensearch-project/security/pull/395) | Fixes bad breadcrumbs on page reload | security |
| [#404](https://github.com/opensearch-project/security/pull/404) | Fixes UX/UI bugs for edit detector page | security |
| [#394](https://github.com/opensearch-project/security/pull/394) | Add breadcrumbs for create detector page | security |
| [#388](https://github.com/opensearch-project/security/pull/388) | Removes sidebar from edit detector page | security |
| [#379](https://github.com/opensearch-project/security/pull/379) | Fixes interval field validation | security |
| [#348](https://github.com/opensearch-project/security/pull/348) | Fixes chart tooltip delay | security |
| [#350](https://github.com/opensearch-project/security/pull/350) | Fixes wrong alert colors | security |
| [#363](https://github.com/opensearch-project/security/pull/363) | Readme update | security |
| [#329](https://github.com/opensearch-project/security/pull/329) | Baselined MAINTAINERS and CODEOWNERS docs. | security |
| [#351](https://github.com/opensearch-project/security/pull/351) | Bumped version to 2.6. | security |
| [#412](https://github.com/opensearch-project/security/pull/412) | Updated lint-staged for consistency with other plugins. | security |
