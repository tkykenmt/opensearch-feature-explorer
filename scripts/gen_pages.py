"""Generate index.md and .pages files for MkDocs navigation."""

import mkdocs_gen_files
import re
from pathlib import Path

DOCS_DIR = Path("docs")
FEATURES_DIR = DOCS_DIR / "features"
RELEASES_DIR = DOCS_DIR / "releases"

DOMAIN_MAPPINGS = {
    "search": ["k-nn", "neural-search", "sql", "asynchronous-search", "learning", "search-relevance", "dashboards-search-relevance"],
    "ml": ["ml-commons", "flow-framework", "skills", "ml-commons-dashboards", "dashboards-flow-framework", "dashboards-assistant"],
    "observability": ["alerting", "anomaly-detection", "notifications", "observability", "query-insights", "performance-analyzer",
                      "alerting-dashboards", "anomaly-detection-dashboards", "dashboards-observability", "dashboards-notifications"],
    "security": ["security", "security-analytics", "security-dashboards", "security-analytics-dashboards"],
    "data": ["index-management", "cross-cluster-replication", "custom-codecs", "job-scheduler", "index-management-dashboards"],
    "geo": ["geospatial", "dashboards-maps"],
    "core": ["opensearch", "common-utils", "opensearch-remote-metadata-sdk", "opensearch-system-templates", "opensearch-dashboards"],
    "infra": ["ci", "multi-plugin", "reporting", "user-behavior-insights", "dashboards-reporting", "dashboards-query-workbench"],
}

DOMAIN_LABELS = {
    "core": "Core",
    "search": "Search & Query",
    "ml": "Machine Learning",
    "observability": "Observability",
    "security": "Security",
    "data": "Data Management",
    "geo": "Geospatial",
    "infra": "Infrastructure",
    "other": "Other",
}

def get_domain(repo_name: str) -> str:
    for domain, repos in DOMAIN_MAPPINGS.items():
        if repo_name in repos:
            return domain
    return "other"

def get_title_from_file(filepath: Path) -> str:
    """Extract H1 title from markdown file."""
    try:
        content = filepath.read_text()
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except:
        pass
    return filepath.stem.replace("-", " ").title()

def generate_subdir_index(subdir: Path):
    """Generate index.md for a feature subdirectory."""
    md_files = sorted([f for f in subdir.glob("*.md") if f.name != "index.md"])
    if not md_files:
        return
    
    repo_name = subdir.name
    title = repo_name.replace("-", " ").title()
    
    content = f"# {title}\n\n"
    content += "| Document | Description |\n"
    content += "|----------|-------------|\n"
    
    for f in md_files:
        desc = get_title_from_file(f)
        content += f"| [{f.stem}]({f.name}) | {desc} |\n"
    
    with mkdocs_gen_files.open(f"features/{repo_name}/index.md", "w") as out:
        out.write(content)

def generate_features_index():
    """Generate main features/index.md."""
    if not FEATURES_DIR.exists():
        return
    
    subdirs = sorted([d for d in FEATURES_DIR.iterdir() if d.is_dir()])
    by_domain = {}
    for subdir in subdirs:
        domain = get_domain(subdir.name)
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(subdir.name)
    
    content = "# OpenSearch Features\n\n"
    
    for domain in ["core", "search", "ml", "observability", "security", "data", "geo", "infra", "other"]:
        if domain not in by_domain:
            continue
        content += f"## {DOMAIN_LABELS[domain]}\n\n"
        content += "| Category | Description |\n"
        content += "|----------|-------------|\n"
        for repo in sorted(by_domain[domain]):
            title = repo.replace("-", " ").title()
            content += f"| [{title}]({repo}/) | {title} features |\n"
        content += "\n"
    
    with mkdocs_gen_files.open("features/index.md", "w") as f:
        f.write(content)

def generate_pages_file():
    """Generate .pages for features directory."""
    if not FEATURES_DIR.exists():
        return
    
    subdirs = sorted([d.name for d in FEATURES_DIR.iterdir() if d.is_dir()])
    by_domain = {}
    for subdir in subdirs:
        domain = get_domain(subdir)
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(subdir)
    
    content = "nav:\n  - index.md\n"
    for domain in ["core", "search", "ml", "observability", "security", "data", "geo", "infra", "other"]:
        if domain in by_domain:
            for repo in sorted(by_domain[domain]):
                content += f"  - {repo}\n"
    
    with mkdocs_gen_files.open("features/.pages", "w") as f:
        f.write(content)

# Generate all
generate_features_index()
generate_pages_file()
for subdir in FEATURES_DIR.iterdir():
    if subdir.is_dir():
        generate_subdir_index(subdir)

def generate_releases_index():
    """Generate releases/index.md with version list."""
    if not RELEASES_DIR.exists():
        return
    
    versions = sorted(
        [d.name for d in RELEASES_DIR.iterdir() if d.is_dir() and d.name.startswith("v")],
        key=lambda v: [int(x) for x in v[1:].split(".")],
        reverse=True
    )
    
    content = "# OpenSearch Releases\n\n"
    content += "| Version | Summary |\n"
    content += "|---------|--------|\n"
    for ver in versions:
        content += f"| [{ver}]({ver}/) | [Summary]({ver}/summary.md) |\n"
    
    with mkdocs_gen_files.open("releases/index.md", "w") as f:
        f.write(content)

def generate_release_version_index():
    """Generate releases/v{version}/index.md for each version."""
    if not RELEASES_DIR.exists():
        return
    
    for version_dir in RELEASES_DIR.iterdir():
        if not version_dir.is_dir() or not version_dir.name.startswith("v"):
            continue
        
        version = version_dir.name
        content = f"# OpenSearch {version}\n\n"
        content += "| Page | Description |\n"
        content += "|------|-------------|\n"
        content += f"| [Summary](summary.md) | Release highlights |\n"
        content += f"| [Features](features/) | Detailed feature reports |\n"
        
        with mkdocs_gen_files.open(f"releases/{version}/index.md", "w") as f:
            f.write(content)

def generate_release_features_index():
    """Generate releases/v{version}/features/index.md and subdirectory indexes."""
    if not RELEASES_DIR.exists():
        return
    
    for version_dir in RELEASES_DIR.iterdir():
        if not version_dir.is_dir() or not version_dir.name.startswith("v"):
            continue
        
        features_dir = version_dir / "features"
        if not features_dir.exists():
            continue
        
        repos = sorted([d.name for d in features_dir.iterdir() if d.is_dir()])
        if not repos:
            continue
        
        version = version_dir.name
        
        # Generate features/index.md
        content = f"# {version} Features\n\n"
        content += "| Category | Documents |\n"
        content += "|----------|----------|\n"
        
        for repo in repos:
            repo_dir = features_dir / repo
            docs = sorted([f.stem for f in repo_dir.glob("*.md")])
            doc_count = len(docs)
            title = repo.replace("-", " ").title()
            content += f"| [{title}]({repo}/) | {doc_count} |\n"
        
        with mkdocs_gen_files.open(f"releases/{version}/features/index.md", "w") as f:
            f.write(content)
        
        # Generate features/{repo}/index.md
        for repo in repos:
            repo_dir = features_dir / repo
            md_files = sorted([f for f in repo_dir.glob("*.md") if f.name != "index.md"])
            if not md_files:
                continue
            
            title = repo.replace("-", " ").title()
            content = f"# {title} ({version})\n\n"
            content += "| Document | Title |\n"
            content += "|----------|-------|\n"
            
            for f in md_files:
                doc_title = get_title_from_file(f)
                content += f"| [{f.stem}]({f.name}) | {doc_title} |\n"
            
            with mkdocs_gen_files.open(f"releases/{version}/features/{repo}/index.md", "w") as out:
                out.write(content)

generate_releases_index()
generate_release_version_index()
generate_release_features_index()
