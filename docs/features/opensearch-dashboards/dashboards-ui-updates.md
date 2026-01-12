# Dashboards UI Updates (OUI)

## Summary

OpenSearch Dashboards uses the OpenSearch UI (OUI) component library for consistent visual design. This feature tracks OUI library upgrades and associated header/navigation styling improvements that enhance the look and feel of the application.

## Details

### Architecture

```mermaid
graph TB
    subgraph "OpenSearch Dashboards"
        subgraph "OUI Component Library"
            OUI[OUI Package]
            THEME[Theme System]
            COMP[UI Components]
        end
        
        subgraph "Header Components"
            HEADER[Application Header]
            TITLE[Page Title]
            NAV[Navigation Controls]
            RECENT[Recent Items]
        end
        
        subgraph "Styling"
            SCSS[SCSS Styles]
            CSS[CSS Variables]
        end
    end
    
    OUI --> THEME
    OUI --> COMP
    COMP --> HEADER
    HEADER --> TITLE
    HEADER --> NAV
    HEADER --> RECENT
    THEME --> SCSS
    SCSS --> CSS
```

### Components

| Component | Description |
|-----------|-------------|
| OUI Package | OpenSearch UI component library (`@opensearch-project/oui`) |
| Theme System | Light/dark theme support with CSS variables |
| Application Header | Top navigation bar with title, breadcrumbs, and controls |
| Page Title | Application/page title display using `EuiTitle` |
| Recent Items | Quick access to recently viewed items |
| Navigation Controls | Action buttons and menu items in header |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `home:useNewHomePage` | Enable new home page with updated header | `false` |
| Theme selection | Light/dark theme via Advanced Settings | System default |

### Usage Example

The OUI components are used throughout the application:

```typescript
import { EuiTitle, EuiButtonIcon, EuiToolTip } from '@elastic/eui';

// Page title in header
<EuiTitle size="l" className="newTopNavHeaderTitle">
  <h1>{pageTitle}</h1>
</EuiTitle>

// Recent items button with tooltip
<EuiToolTip content="Recents" delay="long" position="bottom">
  <EuiButtonIcon
    iconType="recent"
    color="text"
    size="xs"
    aria-label="View recents"
    onClick={handleClick}
  />
</EuiToolTip>
```

### CSS Classes

| Class | Purpose |
|-------|---------|
| `.newTopNavHeader` | Main header container with updated spacing |
| `.newTopNavHeaderTitle` | Page title styling (font-size: 2rem) |
| `.headerAppActionMenu` | Action menu container with gap spacing |
| `.headerRecentItemsButton` | Recent items button styling |
| `.primaryApplicationHeader` | Application-specific header with border |

## Limitations

- OUI upgrades may require snapshot test updates
- CSS `:has()` selector used in some styles may not work in older browsers
- Custom themes may need adjustment for new header styling

## Change History

- **v2.17.0** (2024-09-17): OUI upgrades from 1.9.0 to 1.12.0, header spacing improvements, recent items button refactoring

## References

### Documentation
- [OUI Repository](https://github.com/opensearch-project/oui)
- [OpenSearch Dashboards Repository](https://github.com/opensearch-project/OpenSearch-Dashboards)

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v2.17.0 | [#7741](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7741) | Revisit updated header spacing, bump OUI to 1.10.0 |
| v2.17.0 | [#7799](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7799) | Add iconGap to TopNavControl, bump OUI to 1.11.0 |
| v2.17.0 | [#7865](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7865) | Update OUI to 1.12 |
| v2.17.0 | [#7637](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7637) | Introduce redesign page and application headers, update OUI to 1.9.0 |
