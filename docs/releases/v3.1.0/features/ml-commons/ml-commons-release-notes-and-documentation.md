---
tags:
  - domain/ml
  - component/server
  - indexing
  - ml
---
# ML Commons Release Notes and Documentation

## Summary

This release item includes documentation and infrastructure improvements for the ML Commons plugin in OpenSearch v3.1.0. The changes focus on release note formatting fixes, Maven snapshot publishing endpoint migration, README branding updates, and adding a new Bedrock Claude v4 blueprint.

## Details

### What's New in v3.1.0

This release includes four bug fix PRs that improve documentation quality and build infrastructure:

1. **Release Note Formatting**: Fixed markdown link formatting in release notes and added MCP server feature documentation
2. **Maven Snapshot Publishing**: Migrated to new Sonatype Central Portal for snapshot publishing
3. **README Branding**: Replaced legacy "elasticsearch" references with "OpenSearch"
4. **Claude v4 Blueprint**: Added connector blueprint for Amazon Bedrock Claude 4 models

### Technical Changes

#### Release Notes Formatting Fix (PR #3811)

The release notes for v3.0.0 had incorrect markdown link formatting. Links were using the format `(#PR)[URL]` instead of the correct `[#PR](URL)` format. This PR:
- Fixed all markdown links in the release notes
- Added the MCP server feature (`#3781`) to the Features section
- Added MCP session management (`#3803`), customized message endpoint (`#3810`), and circuit breaker exclusion for Agent (`#3814`) to Bug Fixes

#### Maven Snapshot Publishing Migration (PR #3929)

Updated the Maven snapshot publishing infrastructure to use the new Sonatype Central Portal:
- Changed publish URL from `https://aws.oss.sonatype.org/content/repositories/snapshots` to `https://central.sonatype.com/repository/maven-snapshots/`
- Migrated from AWS Secrets Manager to 1Password for credential management
- Updated workflow to use `1password/load-secrets-action@v2`
- Modified `build.gradle`, `client/build.gradle`, `common/build.gradle`, `plugin/build.gradle`, `spi/build.gradle`, and `build-tools/repositories.gradle`

#### README Branding Update (PR #3876)

Fixed a legacy reference in the README.md file:
- Changed "elasticsearch" to "OpenSearch" in the documentation describing ML Commons challenges
- Resolves Issue #3875

#### Bedrock Claude v4 Blueprint (PR #3871)

Added a new connector blueprint for Amazon Bedrock Claude 4 models:
- Supports both Claude Sonnet 4 (`us.anthropic.claude-sonnet-4-20250514-v1:0`) and Claude Opus 4 (`us.anthropic.claude-opus-4-20250514-v1:0`)
- Includes standard mode and extended thinking mode configurations
- Uses inference profiles for US regions (`us-east-1`, `us-east-2`, `us-west-2`)
- Extended thinking mode allows configurable `budget_tokens` for internal reasoning

### Usage Example

#### Claude v4 Connector (Standard Mode)

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Amazon Bedrock claude v4",
    "description": "Connector for Amazon Bedrock claude v4",
    "version": 1,
    "protocol": "aws_sigv4",
    "credential": {
        "roleArn": "<AWS_ROLE_ARN>"
    },
    "parameters": {
        "region": "<AWS_REGION>",
        "service_name": "bedrock",
        "max_tokens": 8000,
        "temperature": 1,
        "anthropic_version": "bedrock-2023-05-31",
        "model": "us.anthropic.claude-sonnet-4-20250514-v1:0"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "headers": { "content-type": "application/json" },
            "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
            "request_body": "{ \"anthropic_version\": \"${parameters.anthropic_version}\", \"max_tokens\": ${parameters.max_tokens}, \"temperature\": ${parameters.temperature}, \"messages\": ${parameters.messages} }"
        }
    ]
}
```

## Limitations

- Claude v4 models require inference profiles and are only available in specific US regions
- Extended thinking mode increases token usage due to internal reasoning blocks
- Maven snapshot publishing requires 1Password service account token configuration

## References

### Documentation
- [Sonatype Central Portal Snapshots](https://central.sonatype.org/publish/publish-portal-snapshots/): Official migration documentation
- [Extended Thinking Mode](https://www.anthropic.com/news/visible-extended-thinking): Anthropic documentation

### Blog Posts
- [Claude 4 on Amazon Bedrock](https://www.aboutamazon.com/news/aws/anthropic-claude-4-opus-sonnet-amazon-bedrock): Announcement blog

### Pull Requests
| PR | Description |
|----|-------------|
| [#3811](https://github.com/opensearch-project/ml-commons/pull/3811) | Change release note - fix markdown formatting and add MCP server feature |
| [#3929](https://github.com/opensearch-project/ml-commons/pull/3929) | Update the maven snapshot publish endpoint and credential |
| [#3876](https://github.com/opensearch-project/ml-commons/pull/3876) | Replace the usage of elasticsearch with OpenSearch in README |
| [#3871](https://github.com/opensearch-project/ml-commons/pull/3871) | Added blueprint for Bedrock Claude v4 |

### Issues (Design / RFC)
- [Issue #3875](https://github.com/opensearch-project/ml-commons/issues/3875): Replace elasticsearch with OpenSearch in README
- [Issue #5551](https://github.com/opensearch-project/opensearch-build/issues/5551): Sonatype migration campaign

## Related Feature Report

- [ML Commons Blueprints](../../../features/ml-commons/ml-commons-blueprints.md)
