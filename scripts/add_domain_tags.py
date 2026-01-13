#!/usr/bin/env python3
"""Add domain tags to existing documentation files."""

import re
from pathlib import Path

DOMAIN_MAP = {
    # search
    'k-nn': 'search',
    'neural-search': 'search',
    'sql': 'search',
    'asynchronous-search': 'search',
    'learning': 'search',
    'search-relevance': 'search',
    'opensearch-learning-to-rank-base': 'search',
    'dashboards-search-relevance': 'search',
    # ml
    'ml-commons': 'ml',
    'flow-framework': 'ml',
    'skills': 'ml',
    'dashboards-assistant': 'ml',
    'dashboards-flow-framework': 'ml',
    'ml-commons-dashboards': 'ml',
    # observability
    'alerting': 'observability',
    'anomaly-detection': 'observability',
    'notifications': 'observability',
    'observability': 'observability',
    'query-insights': 'observability',
    'performance-analyzer': 'observability',
    'alerting-dashboards': 'observability',
    'alerting-dashboards-plugin': 'observability',
    'anomaly-detection-dashboards': 'observability',
    'anomaly-detection-dashboards-plugin': 'observability',
    'dashboards-notifications': 'observability',
    'dashboards-observability': 'observability',
    'query-insights-dashboards': 'observability',
    # security
    'security': 'security',
    'security-analytics': 'security',
    'security-dashboards': 'security',
    'security-dashboards-plugin': 'security',
    'security-analytics-dashboards': 'security',
    'security-analytics-dashboards-plugin': 'security',
    # data
    'index-management': 'data',
    'cross-cluster-replication': 'data',
    'custom-codecs': 'data',
    'job-scheduler': 'data',
    'index-management-dashboards': 'data',
    # geo
    'geospatial': 'geo',
    'dashboards-maps': 'geo',
    # core
    'opensearch': 'core',
    'common-utils': 'core',
    'opensearch-remote-metadata-sdk': 'core',
    'opensearch-dashboards': 'core',
    # infra
    'ci': 'infra',
    'multi-plugin': 'infra',
    'multi-repo': 'infra',
    'reporting': 'infra',
    'user-behavior-insights': 'infra',
    'dashboards-reporting': 'infra',
    # common
    'common': 'core',
}

DASHBOARDS_PATTERNS = [
    'dashboards',
    '-dashboards-',
    'dashboards-plugin',
]


def is_dashboards(dir_name: str) -> bool:
    """Check if directory represents a dashboards component."""
    return any(p in dir_name for p in DASHBOARDS_PATTERNS)


def get_domain(dir_name: str) -> str:
    """Get domain from directory name."""
    return DOMAIN_MAP.get(dir_name, 'core')


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """Parse YAML frontmatter from content."""
    if not content.startswith('---'):
        return None, content
    
    end = content.find('---', 3)
    if end == -1:
        return None, content
    
    fm_text = content[3:end].strip()
    body = content[end + 3:].lstrip('\n')
    
    # Simple YAML parsing for tags
    fm = {}
    current_key = None
    current_list = []
    
    for line in fm_text.split('\n'):
        if line.startswith('  - '):
            current_list.append(line[4:].strip())
        elif ':' in line:
            if current_key and current_list:
                fm[current_key] = current_list
            key, val = line.split(':', 1)
            current_key = key.strip()
            val = val.strip()
            if val:
                fm[current_key] = val
            current_list = []
    
    if current_key and current_list:
        fm[current_key] = current_list
    
    return fm, body


def build_frontmatter(fm: dict) -> str:
    """Build YAML frontmatter string."""
    lines = ['---']
    for key, val in fm.items():
        if isinstance(val, list):
            lines.append(f'{key}:')
            for item in val:
                lines.append(f'  - {item}')
        else:
            lines.append(f'{key}: {val}')
    lines.append('---')
    return '\n'.join(lines)


def process_file(path: Path) -> bool:
    """Process a single file. Returns True if modified."""
    # Get directory name (repository)
    parts = path.parts
    try:
        if 'features' in parts:
            idx = parts.index('features')
            dir_name = parts[idx + 1]
        elif 'releases' in parts:
            idx = parts.index('features', parts.index('releases'))
            dir_name = parts[idx + 1]
        else:
            return False
    except (ValueError, IndexError):
        return False
    
    content = path.read_text()
    fm, body = parse_frontmatter(content)
    
    # Determine tags
    domain = get_domain(dir_name)
    component = 'dashboards' if is_dashboards(dir_name) else 'server'
    
    domain_tag = f'domain/{domain}'
    component_tag = f'component/{component}'
    
    # Build new tags list
    if fm is None:
        fm = {}
    
    existing_tags = fm.get('tags', [])
    if isinstance(existing_tags, str):
        existing_tags = [existing_tags]
    
    # Remove old domain/component tags
    new_tags = [t for t in existing_tags if not t.startswith('domain/') and not t.startswith('component/')]
    
    # Add domain and component tags at the beginning
    new_tags = [domain_tag, component_tag] + new_tags
    
    fm['tags'] = new_tags
    
    # Write back
    new_content = build_frontmatter(fm) + '\n' + body
    
    if new_content != content:
        path.write_text(new_content)
        return True
    return False


def main():
    docs_dir = Path(__file__).parent.parent / 'docs'
    
    modified = 0
    total = 0
    
    for pattern in ['features/**/*.md', 'releases/**/*.md']:
        for path in docs_dir.glob(pattern):
            if path.name in ['index.md', 'summary.md']:
                continue
            total += 1
            if process_file(path):
                modified += 1
                print(f'✓ {path.relative_to(docs_dir)}')
    
    print(f'\nProcessed {total} files, modified {modified}')


if __name__ == '__main__':
    main()
