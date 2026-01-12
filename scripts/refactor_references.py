#!/usr/bin/env python3
"""
Refactor report files to comply with steering guidelines.

Transforms:
1. Section order: Summary → Details → Limitations → Change History → References
2. Merges "## Related PRs" into "## References" with subsections
"""

import re
import sys
from pathlib import Path


def parse_sections(content: str) -> dict:
    """Parse markdown into sections by ## headers."""
    sections = {}
    current_section = "preamble"
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('## '):
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_content:
        sections[current_section] = '\n'.join(current_content)
    
    return sections


def extract_references_parts(references_content: str) -> dict:
    """Extract documentation, blogs, and issues from References section."""
    parts = {'docs': [], 'blogs': [], 'issues': [], 'other': []}
    
    for line in references_content.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Check for issue links
        if re.search(r'\[.*Issue.*#\d+\]|github\.com/.*/issues/', line, re.I):
            parts['issues'].append(line)
        # Check for blog links
        elif re.search(r'blog|announcement', line, re.I):
            parts['blogs'].append(line)
        # Check for documentation links
        elif re.search(r'docs\.opensearch\.org|documentation', line, re.I):
            parts['docs'].append(line)
        else:
            parts['other'].append(line)
    
    return parts


def format_pr_table(related_prs_content: str) -> str:
    """Format Related PRs content as a table under References."""
    lines = related_prs_content.strip().split('\n')
    # Filter to keep only table content
    table_lines = [l for l in lines if l.strip() and (l.startswith('|') or l.startswith('-'))]
    return '\n'.join(table_lines) if table_lines else ''


def build_references_section(sections: dict) -> str:
    """Build the new References section with subsections."""
    result = []
    
    # Get existing references content
    refs_content = sections.get('References', '')
    refs_parts = extract_references_parts(refs_content)
    
    # Get Related PRs content
    related_prs = sections.get('Related PRs', '')
    pr_table = format_pr_table(related_prs)
    
    # Build Documentation subsection
    if refs_parts['docs'] or refs_parts['other']:
        result.append('### Documentation')
        for item in refs_parts['docs'] + refs_parts['other']:
            result.append(item)
        result.append('')
    
    # Build Blog Posts subsection (only if content exists)
    if refs_parts['blogs']:
        result.append('### Blog Posts')
        for item in refs_parts['blogs']:
            result.append(item)
        result.append('')
    
    # Build Pull Requests subsection
    if pr_table:
        result.append('### Pull Requests')
        result.append(pr_table)
        result.append('')
    
    # Build Issues subsection
    if refs_parts['issues']:
        result.append('### Issues (Design / RFC)')
        for item in refs_parts['issues']:
            result.append(item)
        result.append('')
    
    return '\n'.join(result).rstrip()


def refactor_file(filepath: Path) -> tuple[bool, str]:
    """Refactor a single file. Returns (changed, message)."""
    content = filepath.read_text()
    sections = parse_sections(content)
    
    # Check if file needs refactoring
    has_related_prs = 'Related PRs' in sections
    has_change_history = 'Change History' in sections
    has_references = 'References' in sections
    
    if not has_related_prs and not has_change_history:
        return False, "No changes needed"
    
    # Build new content
    lines = []
    
    # Title (first line)
    title_match = re.match(r'^# .+', content)
    if title_match:
        lines.append(title_match.group())
        lines.append('')
    
    # Standard sections in order
    section_order = ['Summary', 'Details', 'Limitations']
    
    for section_name in section_order:
        if section_name in sections:
            lines.append(f'## {section_name}')
            lines.append(sections[section_name].rstrip())
            lines.append('')
    
    # Change History (before References)
    if has_change_history:
        lines.append('## Change History')
        lines.append(sections['Change History'].rstrip())
        lines.append('')
    
    # References (with merged Related PRs)
    if has_references or has_related_prs:
        lines.append('## References')
        lines.append('')
        refs_section = build_references_section(sections)
        if refs_section:
            lines.append(refs_section)
        lines.append('')
    
    # Related Feature Report (if exists)
    if 'Related Feature Report' in sections:
        lines.append('## Related Feature Report')
        lines.append(sections['Related Feature Report'].rstrip())
        lines.append('')
    
    new_content = '\n'.join(lines).rstrip() + '\n'
    
    if new_content != content:
        filepath.write_text(new_content)
        return True, "Refactored"
    
    return False, "No changes needed"


def main():
    docs_path = Path('docs')
    if not docs_path.exists():
        print("Error: docs/ directory not found")
        sys.exit(1)
    
    files = list(docs_path.glob('features/**/*.md')) + list(docs_path.glob('releases/**/*.md'))
    
    # Exclude index files
    files = [f for f in files if f.name not in ('index.md', 'summary.md')]
    
    changed = 0
    skipped = 0
    errors = 0
    
    for filepath in files:
        try:
            was_changed, msg = refactor_file(filepath)
            if was_changed:
                changed += 1
                print(f"✓ {filepath}")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"✗ {filepath}: {e}")
    
    print(f"\nSummary: {changed} changed, {skipped} skipped, {errors} errors")


if __name__ == '__main__':
    main()
