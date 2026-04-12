---
tags:
  - sql
---
# SQL/PPL Engine

## Summary

OpenSearch 2.6.0 brings 12 enhancement(s) to SQL/PPL Engine, along with 18 bug fixes.

## Details

### Enhancements

- **Extend comparison methods to accept different datetime types**
- **Enable concat() string function to support multiple string arguments**
- **Add more keywords as identifier in PPL**
- **Update DATE_ADD/ADDDATE and DATE_SUB/SUBDATE functions**
- **Escape character support for string literals**
- **Updated EXPM1() and Tests to New Engine**
- **Update TIMESTAMP function implementation and signatures**
- **Add GET_FORMAT Function To OpenSearch SQL Plugin**
- **Add TIME_FORMAT() Function To SQL Plugin**
- **Support More Formats For GET_FORMAT Function**
- **Add last_day Function To OpenSearch SQL Plugin**
- **Add WeekOfYear Function To OpenSearch**

### Bug Fixes

- Allow literal in aggregation
- Datetime aggregation fixes
- Modified returning NaN to NULL
- Fix index not found reported as server error bug
- Upgrade sqlite to 3.32.3.3
- Add publish snapshots to maven via GHA
- Added untriaged issue workflow
- Create custom integ test file for sql plugin
- Fix IT according to OpenSearch changes
- Fix ArgumentCaptor can't capture varargs
- Added Correctness Tests For Date And Time Functions
- Update usage of Strings.toString
- Update link checker CI workflow.
- Add micro benchmark by JMH
- Move PiTest to a new workflow.
- Adding mutation testing to build gradle with PiTest
- Reorganize development docs
- Remove obsolete links from README

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#1196](https://github.com/opensearch-project/sql/pull/1196) | Extend comparison methods to accept different datetime types | sql |
| [#1279](https://github.com/opensearch-project/sql/pull/1279) | Enable concat() string function to support multiple string arguments | sql |
| [#1319](https://github.com/opensearch-project/sql/pull/1319) | Add more keywords as identifier in PPL | sql |
| [#1182](https://github.com/opensearch-project/sql/pull/1182) | Update DATE_ADD/ADDDATE and DATE_SUB/SUBDATE functions | sql |
| [#1206](https://github.com/opensearch-project/sql/pull/1206) | Escape character support for string literals | sql |
| [#1334](https://github.com/opensearch-project/sql/pull/1334) | Updated EXPM1() and Tests to New Engine | sql |
| [#1254](https://github.com/opensearch-project/sql/pull/1254) | Update TIMESTAMP function implementation and signatures | sql |
| [#1299](https://github.com/opensearch-project/sql/pull/1299) | Add GET_FORMAT Function To OpenSearch SQL Plugin | sql |
| [#1301](https://github.com/opensearch-project/sql/pull/1301) | Add TIME_FORMAT() Function To SQL Plugin | sql |
| [#1343](https://github.com/opensearch-project/sql/pull/1343) | Support More Formats For GET_FORMAT Function | sql |
| [#1344](https://github.com/opensearch-project/sql/pull/1344) | Add last_day Function To OpenSearch SQL Plugin | sql |
| [#1345](https://github.com/opensearch-project/sql/pull/1345) | Add WeekOfYear Function To OpenSearch | sql |
| [#1288](https://github.com/opensearch-project/sql/pull/1288) | Allow literal in aggregation | sql |
| [#1061](https://github.com/opensearch-project/sql/pull/1061) | Datetime aggregation fixes | sql |
| [#1341](https://github.com/opensearch-project/sql/pull/1341) | Modified returning NaN to NULL | sql |
| [#1353](https://github.com/opensearch-project/sql/pull/1353) | Fix index not found reported as server error bug | sql |
| [#1283](https://github.com/opensearch-project/sql/pull/1283) | Upgrade sqlite to 3.32.3.3 | sql |
| [#1359](https://github.com/opensearch-project/sql/pull/1359) | Add publish snapshots to maven via GHA | sql |
| [#1338](https://github.com/opensearch-project/sql/pull/1338) | Added untriaged issue workflow | sql |
| [#1330](https://github.com/opensearch-project/sql/pull/1330) | Create custom integ test file for sql plugin | sql |
| [#1326](https://github.com/opensearch-project/sql/pull/1326) | Fix IT according to OpenSearch changes | sql |
| [#1320](https://github.com/opensearch-project/sql/pull/1320) | Fix ArgumentCaptor can't capture varargs | sql |
| [#1298](https://github.com/opensearch-project/sql/pull/1298) | Added Correctness Tests For Date And Time Functions | sql |
| [#1309](https://github.com/opensearch-project/sql/pull/1309) | Update usage of Strings.toString | sql |
| [#1304](https://github.com/opensearch-project/sql/pull/1304) | Update link checker CI workflow. | sql |
| [#1278](https://github.com/opensearch-project/sql/pull/1278) | Add micro benchmark by JMH | sql |
| [#1285](https://github.com/opensearch-project/sql/pull/1285) | Move PiTest to a new workflow. | sql |
| [#1204](https://github.com/opensearch-project/sql/pull/1204) | Adding mutation testing to build gradle with PiTest | sql |
| [#1200](https://github.com/opensearch-project/sql/pull/1200) | Reorganize development docs | sql |
| [#1303](https://github.com/opensearch-project/sql/pull/1303) | Remove obsolete links from README | sql |
