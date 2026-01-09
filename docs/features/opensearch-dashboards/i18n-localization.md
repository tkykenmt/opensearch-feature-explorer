# i18n & Localization

## Summary

OpenSearch Dashboards provides internationalization (i18n) support enabling the UI to be displayed in multiple languages. The i18n framework includes translation file management, ICU message format support, and developer tooling for maintaining translation quality.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Source Code"
        A[React Components] --> B[i18n.translate]
        C[TypeScript Files] --> B
    end
    subgraph "i18n Framework"
        B --> D[Message Extraction]
        D --> E[Default Messages Map]
        F[Locale Files] --> G[Translation Loader]
        G --> H[Runtime i18n Service]
    end
    subgraph "Validation"
        I[Precommit Hook] --> J[i18n Check]
        K[CI Workflow] --> J
        J --> L{Valid?}
        L -->|Yes| M[Pass]
        L -->|No| N[Fail with Errors]
    end
    E --> H
    H --> O[Rendered UI]
```

### Data Flow

```mermaid
flowchart TB
    A[Developer writes i18n.translate] --> B[Extract messages]
    B --> C[Generate default messages]
    C --> D[Translators update locale files]
    D --> E[i18n:check validates]
    E --> F[Build includes translations]
    F --> G[User selects language]
    G --> H[Load locale file]
    H --> I[Display translated UI]
```

### Components

| Component | Description |
|-----------|-------------|
| `@osd/i18n` | Core i18n package providing translation functions |
| `i18n.translate()` | Function to mark strings for translation |
| `FormattedMessage` | React component for translated strings |
| `i18n:check` | CLI tool to validate i18n usage |
| `i18n:extract` | CLI tool to extract messages from source |
| Precommit Hook | Git hook for local i18n validation |
| CI Workflow | GitHub Actions job for PR validation |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `i18n.locale` | Default locale for the application | `en` |
| `--ignore-incompatible` | Ignore mismatched keys in translations | `false` |
| `--ignore-malformed` | Ignore malformed ICU format | `false` |
| `--ignore-missing` | Ignore missing translations | `false` |
| `--ignore-unused` | Ignore unused translations | `false` |
| `--ignore-missing-formats` | Ignore missing formats object | `true` |

### Supported Locales

| Locale Code | Language |
|-------------|----------|
| `en` | English (default) |
| `de-DE` | German |
| `es-ES` | Spanish |
| `fr-FR` | French |
| `ko-KR` | Korean |
| `tr-TR` | Turkish |
| `zh-CN` | Chinese (Simplified) |

### Usage Example

Using i18n in React components:

```typescript
import { i18n } from '@osd/i18n';
import { FormattedMessage } from '@osd/i18n/react';

// Using i18n.translate
const title = i18n.translate('myPlugin.title', {
  defaultMessage: 'My Plugin Title',
});

// Using FormattedMessage component
<FormattedMessage
  id="myPlugin.description"
  defaultMessage="Welcome to {name}"
  values={{ name: 'OpenSearch' }}
/>
```

Running validation:

```bash
# Validate all i18n usage
yarn i18n:check

# Extract messages for translation
yarn i18n:extract
```

### i18n Key Naming Convention

Keys must be prefixed with the plugin name:

```typescript
// Correct
i18n.translate('workspace.title', { defaultMessage: 'Workspace' });

// Incorrect - will fail validation
i18n.translate('title', { defaultMessage: 'Workspace' });
```

## Limitations

- Translation files must include a `formats` object (can be ignored with `--ignore-missing-formats`)
- Dynamic i18n key construction is not supported and will fail validation
- ICU message format variables must use consistent casing between source and translations

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v2.18.0 | [#8411](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8411) | Add i18n checks to PR workflows |
| v2.18.0 | [#8412](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8412) | Fix unprefixed i18n identifiers in examples |
| v2.18.0 | [#8423](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8423) | Add precommit hook to validate i18n |
| v2.18.0 | [#8483](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8483) | Fix inconsistent i18n key names |
| v2.18.0 | [#8399](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8399) | Fix dynamic i18n in visBuilder plugin |
| v2.18.0 | [#8674](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8674) | Fix unsupported language from localStorage |

## References

- [OpenSearch Dashboards Repository](https://github.com/opensearch-project/OpenSearch-Dashboards)

## Change History

- **v2.18.0** (2024-10-22): Added i18n validation to CI/CD workflows, precommit hook, fixed malformed translations, fixed language selection bug
