"""Generate .pages files and index.md for MkDocs navigation."""

import mkdocs_gen_files
from pathlib import Path

DOCS_DIR = Path("docs")
FEATURES_DIR = DOCS_DIR / "features"

# Domain mappings for repositories
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

def get_domain(repo_name: str) -> str:
    """Get domain for a repository."""
    for domain, repos in DOMAIN_MAPPINGS.items():
        if repo_name in repos:
            return domain
    return "other"

def generate_features_pages():
    """Generate .pages for features directory."""
    if not FEATURES_DIR.exists():
        return
    
    # Get all subdirectories
    subdirs = sorted([d.name for d in FEATURES_DIR.iterdir() if d.is_dir()])
    
    # Group by domain
    by_domain = {}
    for subdir in subdirs:
        domain = get_domain(subdir)
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(subdir)
    
    # Generate .pages content
    pages_content = "nav:\n"
    for domain in ["core", "search", "ml", "observability", "security", "data", "geo", "infra", "other"]:
        if domain in by_domain:
            pages_content += f"  # {domain.upper()}\n"
            for repo in sorted(by_domain[domain]):
                pages_content += f"  - {repo}\n"
    
    with mkdocs_gen_files.open("features/.pages", "w") as f:
        f.write(pages_content)

generate_features_pages()
