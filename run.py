#!/usr/bin/env python3
"""OpenSearch Feature Explorer - Kiro CLI wrapper script."""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
AGENTS_DIR = SCRIPT_DIR / ".kiro" / "agents"

AGENTS = {
    "dev": "dev.json",
    "group-release": "group-release.json",
    "review-groups": "review-groups.json",
    "review-release": "review-release.json",
    "planner": "planner.json",
    "create-issues": "create-issues.json",
    "investigate": "investigate.json",
    "explore": "explore.json",
    "summarize": "summarize.json",
    "translate": "translate.json",
    "generate-release-docs": "generate-release-docs.json",
}


def fetch_release_notes(version: str) -> dict:
    """Fetch and parse release notes from GitHub."""
    sources = [
        ("opensearch-project", "opensearch-build", f"release-notes/opensearch-release-notes-{version}.md"),
        ("opensearch-project", "OpenSearch", f"release-notes/opensearch.release-notes-{version}.md"),
        ("opensearch-project", "OpenSearch-Dashboards", f"release-notes/opensearch-dashboards.release-notes-{version}.md"),
    ]
    
    items = []
    fetched_sources = []
    
    for owner, repo, path in sources:
        cmd = ["gh", "api", f"repos/{owner}/{repo}/contents/{path}", "--jq", ".content"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            continue
        
        import base64
        content = base64.b64decode(result.stdout.strip()).decode("utf-8")
        fetched_sources.append(f"{repo}/{path}")
        
        # Parse release notes
        parsed = parse_release_notes(content, repo)
        items.extend(parsed)
    
    # Build summary
    summary = {"total": len(items), "breaking": 0, "feature": 0, "enhancement": 0, "bugfix": 0, "deprecation": 0}
    for item in items:
        cat = item.get("category", "")
        if cat in summary:
            summary[cat] += 1
    
    return {
        "version": version,
        "parsed_at": datetime.now(timezone.utc).isoformat(),
        "sources": fetched_sources,
        "summary": summary,
        "items": items,
    }


def parse_release_notes(content: str, repo: str) -> list[dict]:
    """Parse release notes markdown and extract items."""
    items = []
    current_category = None
    current_component = None
    
    # Map section headers to categories
    category_map = {
        "breaking": "breaking",
        "feature": "feature",
        "enhancement": "enhancement",
        "bug fix": "bugfix",
        "bugfix": "bugfix",
        "deprecat": "deprecation",
        "added": "feature",
    }
    
    # Determine repository name
    repo_lower = repo.lower()
    if repo_lower in ("opensearch", "opensearch-build"):
        default_repo = "opensearch"
    elif repo_lower == "opensearch-dashboards":
        default_repo = "opensearch-dashboards"
    else:
        default_repo = repo_lower
    
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        
        # Check for section headers
        if line.startswith("#"):
            header = line.lstrip("#").strip().lower()
            # Check category
            for key, cat in category_map.items():
                if key in header:
                    current_category = cat
                    break
            # Check for component/plugin name in header
            if "opensearch" in header and current_category:
                # Extract component name like "OpenSearch Security", "OpenSearch k-NN"
                match = re.search(r"opensearch[- ](\w+)", header, re.IGNORECASE)
                if match:
                    current_component = match.group(1).lower()
                    if current_component in ("core", "build"):
                        current_component = None
        
        # Parse list items with PR references
        if line.startswith(("-", "*")) and current_category:
            # Extract PR number
            pr_match = re.search(r"#(\d+)", line) or re.search(r"\[#?(\d+)\]", line)
            if not pr_match:
                continue
            
            pr_num = int(pr_match.group(1))
            
            # Extract item name/description
            # Remove markdown links and PR references
            name = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)  # [text](url) -> text
            name = re.sub(r"\(#\d+\)", "", name)  # (#123) -> ""
            name = re.sub(r"#\d+", "", name)  # #123 -> ""
            name = re.sub(r"^\s*[-*]\s*", "", name)  # Remove list marker
            name = re.sub(r"\s+", " ", name).strip()  # Normalize whitespace
            
            if not name or len(name) < 5:
                continue
            
            # Determine repository for this item
            item_repo = default_repo
            if current_component:
                item_repo = current_component
            # Check for plugin references in the line
            plugin_match = re.search(r"\b(k-nn|knn|neural-search|ml-commons|sql|security|alerting|anomaly-detection|index-management|observability|reporting|notifications|geospatial|cross-cluster-replication|asynchronous-search)\b", line.lower())
            if plugin_match:
                item_repo = plugin_match.group(1).replace("knn", "k-nn")
            
            items.append({
                "name": name[:200],  # Truncate long names
                "category": current_category,
                "repository": item_repo,
                "pr": pr_num,
                "description": name[:300],
            })
    
    return items


def run_fetch_release(version: str) -> int:
    """Fetch release notes and parse with Python. Saves to raw-items.json."""
    print(f"Fetching release notes for v{version}...")
    
    data = fetch_release_notes(version)
    
    cache_dir = SCRIPT_DIR / ".cache" / "releases" / f"v{version}"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / "raw-items.json"
    
    with open(cache_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Parsed {data['summary']['total']} items from {len(data['sources'])} sources")
    print(f"  Breaking: {data['summary']['breaking']}")
    print(f"  Features: {data['summary']['feature']}")
    print(f"  Enhancements: {data['summary']['enhancement']}")
    print(f"  Bug Fixes: {data['summary']['bugfix']}")
    print(f"Saved to: {cache_file}")
    return 0


def run_group_release(version: str, batch_size: int = 50, process_all: bool = False) -> int:
    """Group raw items into feature groups using LLM. Processes in batches."""
    cache_dir = SCRIPT_DIR / ".cache" / "releases" / f"v{version}"
    raw_file = cache_dir / "raw-items.json"
    groups_file = cache_dir / "groups.json"
    
    if not raw_file.exists():
        print(f"Error: {raw_file} not found. Run fetch-release first.")
        return 1
    
    with open(raw_file) as f:
        data = json.load(f)
    
    items = data["items"]
    total = len(items)
    
    while True:
        # Load current state
        if groups_file.exists():
            with open(groups_file) as f:
                groups_data = json.load(f)
        else:
            groups_data = {
                "version": data["version"],
                "sources": data["sources"],
                "groups": [],
                "processed_offset": 0
            }
        
        offset = groups_data.get("processed_offset", 0)
        
        if offset >= total:
            print(f"\nAll {total} items processed. {len(groups_data['groups'])} groups created.")
            return 0
        
        # Process next batch
        batch = items[offset:offset + batch_size]
        print(f"\nProcessing items {offset+1}-{min(offset+batch_size, total)} of {total}...")
        
        # Save batch to temp file for LLM
        batch_file = cache_dir / "batch.json"
        with open(batch_file, "w") as f:
            json.dump({"items": batch, "offset": offset, "total": total}, f, indent=2)
        
        # Call LLM to group this batch
        prompt = f"Group the items in .cache/releases/v{version}/batch.json into feature groups. Append results to .cache/releases/v{version}/groups.json"
        result = run_kiro("group-release", prompt, no_interactive=True)
        
        if result != 0:
            print(f"Error processing batch. Stopping.")
            return result
        
        if not process_all:
            # Reload to get updated offset
            with open(groups_file) as f:
                groups_data = json.load(f)
            remaining = total - groups_data.get("processed_offset", offset + batch_size)
            if remaining > 0:
                print(f"\n{remaining} items remaining. Run with --all to process all.")
            return 0


def build_prompt(mode: str, args: argparse.Namespace) -> str:
    """Build initial prompt based on mode and arguments."""
    lang_instruction = ""
    if hasattr(args, "lang") and args.lang:
        lang_instruction = f" Output in language code '{args.lang}'."
    
    if mode == "review-groups":
        return f"Review .cache/releases/v{args.version}/groups.json. Look for groups with items that have different [Feature Name] prefixes and split them into separate groups. For example, k-NN Plugin group may contain [Lucene On Faiss], [Remote Vector Index Build], [Explain API Support] items that should be separate groups."
    
    if mode == "planner":
        return f"Create GitHub Project and Issues for OpenSearch v{args.version} from .cache/releases/v{args.version}/groups.json. Create max 20 Issues per run. Resume from where left off."
    
    if mode == "create-issues":
        limit = f" Create only {args.limit} Issues." if getattr(args, "limit", None) else ""
        category = f" Only create Issues for category: {args.category}." if getattr(args, "category", None) else ""
        return f"Create investigation Issues from tracking Issue #{args.tracking}.{limit}{category}"
    
    if mode == "investigate":
        use_pr = not getattr(args, "no_pr", False)
        force = getattr(args, "overwrite", False)
        pr_mode = " Use PR workflow (create branch, pull request, and auto-merge)." if use_pr else " Push directly to main."
        force_mode = " Overwrite existing reports." if force else ""
        if hasattr(args, "issue") and args.issue:
            return f"Investigate GitHub Issue #{args.issue}.{pr_mode}{force_mode}{lang_instruction}"
        if hasattr(args, "feature") and args.feature:
            prompt = f'Investigate feature "{args.feature}"'
            if args.pr:
                prompt += f" starting from PR #{args.pr}"
            return prompt + f".{pr_mode}{force_mode}{lang_instruction}"
        # No issue or feature specified - pick oldest open issue
        return f"Find the oldest open Issue with label 'new-feature' or 'update-feature' and investigate it.{pr_mode}{force_mode}{lang_instruction}"
    
    if mode == "explore":
        lang = args.lang if hasattr(args, "lang") and args.lang else "en"
        return f'Explore the "{args.feature}" feature in language code "{lang}"'
    
    if mode == "summarize":
        return f"Create release summary for OpenSearch v{args.version}.{lang_instruction}"
    
    if mode == "translate":
        suffix = f".{args.to}.md" if args.to != "en" else ".md"
        if args.feature:
            return f'Translate "docs/features/{args.feature}.md" to "{args.to}". Save as "docs/features/{args.feature}{suffix}"'
        if args.release:
            return f'Translate reports in "docs/releases/v{args.release}/" to "{args.to}".'
        return ""
    
    if mode == "generate-release-docs":
        use_pr = not getattr(args, "no_pr", False)
        pr_mode = " Use PR workflow." if use_pr else " Push directly to main."
        return f"Generate release documents for v{args.version} from existing feature documents.{pr_mode}"
    
    return ""


def run_kiro(mode: str, prompt: str, no_interactive: bool = False) -> int:
    """Run kiro-cli with the appropriate agent. Returns exit code."""
    agent_name = AGENTS[mode].replace(".json", "")
    
    cmd = [
        "kiro-cli", "chat",
        "--agent", agent_name,
        "--model", "claude-opus-4.5",
        "--trust-all-tools",
    ]
    
    if no_interactive:
        cmd.append("--no-interactive")
    
    if prompt:
        cmd.append(prompt)
    
    result = subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    return result.returncode


def get_open_issues(labels: list[str], limit: int | None = None) -> list[dict]:
    """Get open issues with specified labels using gh CLI."""
    import json
    label_filter = ",".join(labels)
    cmd = [
        "gh", "issue", "list",
        "--state", "open",
        "--label", label_filter,
        "--json", "number,title",
        "--limit", str(limit) if limit else "1000",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return json.loads(result.stdout)


def run_batch(count: int | None, lang: str | None = None, no_pr: bool = False, version: str | None = None):
    """Run investigate in batch mode. If count is None, process all open issues."""
    lang_instruction = f" Output in language code '{lang}'." if lang else ""
    pr_mode = " Push directly to main." if no_pr else " Use PR workflow (create branch, pull request, and auto-merge)."
    
    # Get open issues first
    labels = ["status/todo"]
    if version:
        labels.append(f"release/v{version}")
    issues = get_open_issues(labels, count)
    if not issues:
        print(f"No open issues found with labels: {', '.join(labels)}")
        return
    
    total = len(issues)
    results = []
    
    for i, issue in enumerate(issues, 1):
        issue_num = issue["number"]
        issue_title = issue["title"]
        
        print(f"\n{'='*50}")
        print(f"Batch {i}/{total}: Issue #{issue_num}")
        print(f"  {issue_title}")
        print(f"{'='*50}\n")
        
        prompt = f"Investigate GitHub Issue #{issue_num}.{pr_mode}{lang_instruction}"
        exit_code = run_kiro("investigate", prompt, no_interactive=True)
        results.append((issue_num, issue_title, "success" if exit_code == 0 else "failed"))
    
    # Summary
    print(f"\n{'='*50}")
    print("Batch Summary")
    print(f"{'='*50}")
    success = sum(1 for _, _, status in results if status == "success")
    print(f"Success: {success}/{total}")
    for issue_num, issue_title, status in results:
        print(f"  #{issue_num}: {status} - {issue_title}")


def run_release_investigate(version: str, lang: str | None = None, no_pr: bool = False) -> int:
    """Full release investigation: fetch → group → plan → investigate all → summarize."""
    print(f"=== Release Investigation: v{version} ===\n")
    
    # Step 1: Fetch
    print("Step 1/5: Fetching release notes...")
    if run_fetch_release(version) != 0:
        return 1
    
    # Step 2: Group (all batches)
    print("\nStep 2/5: Grouping items...")
    if run_group_release(version, batch_size=50, process_all=True) != 0:
        return 1
    
    # Step 3: Plan (create project & issues)
    print("\nStep 3/5: Creating GitHub Project & Issues...")
    prompt = f"Create GitHub Project and Issues for OpenSearch v{version} from .cache/releases/v{version}/groups.json. Create max 20 Issues per run. Resume from where left off."
    while True:
        if run_kiro("planner", prompt, no_interactive=True) != 0:
            return 1
        # Check if all issues created
        groups_file = SCRIPT_DIR / ".cache" / "releases" / f"v{version}" / "groups.json"
        with open(groups_file) as f:
            groups_data = json.load(f)
        pending = sum(1 for g in groups_data["groups"] if not g.get("issue_number"))
        if pending == 0:
            break
        print(f"  {pending} groups remaining, continuing...")
    
    # Step 4: Investigate all
    print("\nStep 4/5: Investigating all Issues...")
    run_batch(count=None, lang=lang, no_pr=no_pr)
    
    # Step 5: Summarize
    print("\nStep 5/5: Creating release summary...")
    lang_instruction = f" Output in language code '{lang}'." if lang else ""
    prompt = f"Create release summary for OpenSearch v{version}.{lang_instruction}"
    if run_kiro("summarize", prompt, no_interactive=True) != 0:
        return 1
    
    print(f"\n=== Release Investigation Complete: v{version} ===")
    return 0


def run_feature_investigate(feature: str, pr: int | None = None, lang: str | None = None, no_pr: bool = False) -> int:
    """Single feature investigation wrapper."""
    lang_instruction = f" Output in language code '{lang}'." if lang else ""
    pr_mode = " Push directly to main." if no_pr else " Use PR workflow (create branch, pull request, and auto-merge)."
    
    prompt = f'Investigate feature "{feature}"'
    if pr:
        prompt += f" starting from PR #{pr}"
    prompt += f".{pr_mode}{lang_instruction}"
    
    return run_kiro("investigate", prompt, no_interactive=False)


def main():
    parser = argparse.ArgumentParser(
        description="OpenSearch Feature Explorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py planner 3.0.0
  python run.py parse-release 3.0.0
  python run.py planner 3.0.0
  python run.py create-issues --tracking 123
  python run.py create-issues --tracking 123 --limit 20
  python run.py investigate --issue 123
  python run.py investigate "Star Tree" --pr 16233
  python run.py explore "Segment Replication" --lang ja
  python run.py summarize 3.0.0
  python run.py translate --feature "Segment Replication" --to ja
        """,
    )
    
    subparsers = parser.add_subparsers(dest="mode", required=True)
    
    # fetch-release
    fr = subparsers.add_parser("fetch-release", help="Fetch release notes and save to raw-items.json")
    fr.add_argument("version", help="Version to fetch (e.g., 3.0.0)")
    
    # group-release
    gr_rel = subparsers.add_parser("group-release", help="Group raw items into feature groups (runs in batches)")
    gr_rel.add_argument("version", help="Version to group (e.g., 3.0.0)")
    gr_rel.add_argument("--batch-size", type=int, default=50, help="Items per batch (default: 50)")
    gr_rel.add_argument("--all", action="store_true", help="Process all remaining batches")
    
    # review-groups
    rg = subparsers.add_parser("review-groups", help="Review and refine groups.json")
    rg.add_argument("version", help="Version to review (e.g., 3.0.0)")
    
    # planner
    pl = subparsers.add_parser("planner", help="Create tracking Issue from groups.json")
    pl.add_argument("version", help="Version to plan (e.g., 3.0.0)")
    pl.add_argument("--lang", help="Output language code (e.g., ja)")
    pl.add_argument("-i", "--ignore-existing", action="store_true", help="Ignore existing tracking Issue and create new one")
    
    # create-issues
    ci = subparsers.add_parser("create-issues", help="Create investigation Issues from tracking Issue")
    ci.add_argument("--tracking", type=int, required=True, help="Tracking Issue number")
    ci.add_argument("--limit", type=int, help="Maximum number of Issues to create")
    ci.add_argument("--category", choices=["features", "enhancements", "breaking", "bugfixes"], help="Filter by category")
    
    # investigate
    inv = subparsers.add_parser("investigate", help="Investigate a single feature")
    inv.add_argument("feature", nargs="?", help="Feature name")
    inv.add_argument("--issue", type=int, help="GitHub Issue number to investigate")
    inv.add_argument("--pr", type=int, help="Starting PR number")
    inv.add_argument("--lang", help="Output language code (e.g., ja)")
    inv.add_argument("--no-pr", action="store_true", help="Push directly to main instead of creating PR")
    inv.add_argument("--overwrite", action="store_true", help="Overwrite existing reports")
    
    # batch-investigate
    ba = subparsers.add_parser("batch-investigate", help="Run investigate in batch mode")
    ba.add_argument("version", nargs="?", help="Target version (e.g., 3.0.0)")
    ba.add_argument("count", type=int, nargs="?", help="Number of issues to process (default: 5, or all with --all)")
    ba.add_argument("--all", action="store_true", help="Process all open issues")
    ba.add_argument("--lang", help="Output language code (e.g., ja)")
    ba.add_argument("--no-pr", action="store_true", help="Push directly to main instead of creating PR")
    
    # explore
    ex = subparsers.add_parser("explore", help="Explore a feature interactively")
    ex.add_argument("feature", help="Feature name to explore")
    ex.add_argument("--lang", help="Response language code (e.g., ja)")
    
    # summarize
    su = subparsers.add_parser("summarize", help="Create release summary from feature reports")
    su.add_argument("version", help="Version to summarize (e.g., 3.0.0)")
    su.add_argument("--lang", help="Output language code (e.g., ja)")
    
    # translate
    tr = subparsers.add_parser("translate", help="Translate existing reports")
    tr.add_argument("--feature", help="Feature name to translate")
    tr.add_argument("--release", help="Release version to translate")
    tr.add_argument("--to", required=True, help="Target language code (e.g., ja)")
    
    # generate-release-docs
    gr = subparsers.add_parser("generate-release-docs", help="Generate release docs from existing feature documents")
    gr.add_argument("version", help="Version to generate release docs for (e.g., 3.0.0)")
    gr.add_argument("--no-pr", action="store_true", help="Push directly to main instead of creating PR")
    
    # release-investigate (orchestrator)
    ri = subparsers.add_parser("release-investigate", help="Full release investigation (fetch → group → plan → investigate → summarize)")
    ri.add_argument("version", help="Version to investigate (e.g., 3.0.0)")
    ri.add_argument("--lang", help="Output language code (e.g., ja)")
    ri.add_argument("--no-pr", action="store_true", help="Push directly to main instead of creating PR")
    
    # feature-investigate (wrapper)
    fi = subparsers.add_parser("feature-investigate", help="Investigate a single feature (wrapper for investigate)")
    fi.add_argument("feature", help="Feature name to investigate")
    fi.add_argument("--pr", type=int, help="Starting PR number")
    fi.add_argument("--lang", help="Output language code (e.g., ja)")
    fi.add_argument("--no-pr", action="store_true", help="Push directly to main instead of creating PR")
    
    # dev
    subparsers.add_parser("dev", help="Development mode - interactive tool development")
    
    args = parser.parse_args()
    
    if args.mode == "dev":
        run_kiro("dev", "", no_interactive=False)
    elif args.mode == "release-investigate":
        sys.exit(run_release_investigate(args.version, getattr(args, "lang", None), getattr(args, "no_pr", False)))
    elif args.mode == "feature-investigate":
        sys.exit(run_feature_investigate(args.feature, getattr(args, "pr", None), getattr(args, "lang", None), getattr(args, "no_pr", False)))
    elif args.mode == "batch-investigate":
        count = None if getattr(args, "all", False) else (args.count or 5)
        run_batch(count, getattr(args, "lang", None), getattr(args, "no_pr", False), getattr(args, "version", None))
    elif args.mode == "fetch-release":
        run_fetch_release(args.version)
    elif args.mode == "group-release":
        run_group_release(args.version, args.batch_size, getattr(args, "all", False))
    else:
        prompt = build_prompt(args.mode, args)
        # These modes run non-interactively by default
        no_interactive = args.mode in ("planner", "create-issues", "summarize", "generate-release-docs", "investigate")
        run_kiro(args.mode, prompt, no_interactive=no_interactive)


if __name__ == "__main__":
    main()
