---
tags:
  - sql
---
# SQL/PPL Engine Maintenance

## Summary

Routine maintenance for the OpenSearch SQL plugin in v3.6.0. Changes include maintainer roster updates (two new maintainers added, eight moved to Emeritus status), addition of a CLAUDE.md AI coding guide, and the automated version bump to 3.6.0-SNAPSHOT.

## Details

### What's New in v3.6.0

#### Maintainer Roster Changes

Two new maintainers were added to the SQL plugin:

| Maintainer | PR | Rationale |
|------------|-----|-----------|
| Kai Huang (@ahkcs) | sql#5223 | 144 merged PRs spanning PPL/Calcite features, bug fixes, and backports |
| SongKan Tang (@songkant-aws) | sql#5244 | 33 merged PRs covering Calcite engine migration, pushdown optimization, and patterns command enhancements |

Eight inactive maintainers were moved to Emeritus status via sql#5260: @kavithacm, @derek-ho, @YANG-DB, @seankao-az, @MaxKsyunz, @Yury-Fridlyand, @forestmvey, @GumpacG. The affiliation column was also removed for emeritus maintainers. This change was motivated by LF license quota constraints.

#### CLAUDE.md AI Coding Guide

PR sql#5259 added a `CLAUDE.md` file to the repository, providing structured context for AI coding assistants. The guide covers:

- Project overview (Java 21, multi-module Gradle)
- Build commands (build, test, format, ANTLR generation, local run, doctest)
- Code style (Google Java Format, Lombok, license headers, pre-commit hooks)
- Architecture (query pipeline flow, module dependency graph, core abstractions, design patterns)
- Adding new PPL commands checklist
- Adding new PPL functions (three approaches: reuse Calcite operators, adapt UDF, implement from scratch)
- Calcite engine dual-engine architecture and toggle (`plugins.calcite.enabled`)
- Integration test directory structure and key base classes

#### Version Bump

PR sql#5115 incremented the version to 3.6.0-SNAPSHOT via automated tooling.

## Limitations

- These changes have no impact on SQL/PPL query behavior or API surface
- Maintainer changes affect only repository governance (code review assignments, CODEOWNERS)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [sql#5260](https://github.com/opensearch-project/sql/pull/5260) | Move some maintainers from active to Emeritus | |
| [sql#5259](https://github.com/opensearch-project/sql/pull/5259) | Add CLAUDE.md | [sql#5242](https://github.com/opensearch-project/sql/issues/5242) |
| [sql#5244](https://github.com/opensearch-project/sql/pull/5244) | Add songkant-aws as maintainer | |
| [sql#5223](https://github.com/opensearch-project/sql/pull/5223) | Add ahkcs as maintainer | |
| [sql#5115](https://github.com/opensearch-project/sql/pull/5115) | Increment version to 3.6.0-SNAPSHOT | |
