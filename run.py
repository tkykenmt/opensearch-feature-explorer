#!/usr/bin/env python3
"""OpenSearch Feature Explorer - Kiro CLI wrapper script."""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
AGENTS_DIR = SCRIPT_DIR / ".kiro" / "agents"

AGENTS = {
    "planner": "planner.json",
    "investigate": "investigate.json",
    "explore": "explore.json",
    "summarize": "summarize.json",
    "translate": "translate.json",
}


def build_prompt(mode: str, args: argparse.Namespace) -> str:
    """Build initial prompt based on mode and arguments."""
    lang_instruction = ""
    if hasattr(args, "lang") and args.lang:
        lang_instruction = f" Output in language code '{args.lang}'."
    
    if mode == "planner":
        return f"Plan investigation for OpenSearch release v{args.version}.{lang_instruction}"
    
    if mode == "investigate":
        use_pr = not getattr(args, "no_pr", False)
        pr_mode = " Use PR workflow (create branch, pull request, and auto-merge)." if use_pr else " Push directly to main."
        if hasattr(args, "issue") and args.issue:
            return f"Investigate GitHub Issue #{args.issue}.{pr_mode}{lang_instruction}"
        if hasattr(args, "feature") and args.feature:
            prompt = f'Investigate feature "{args.feature}"'
            if args.pr:
                prompt += f" starting from PR #{args.pr}"
            return prompt + f".{pr_mode}{lang_instruction}"
        # No issue or feature specified - pick oldest open issue
        return f"Find the oldest open Issue with label 'new-feature' or 'update-feature' and investigate it.{pr_mode}{lang_instruction}"
    
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


def run_batch(count: int | None, lang: str | None = None, no_pr: bool = False):
    """Run investigate in batch mode. If count is None, process all open issues."""
    lang_instruction = f" Output in language code '{lang}'." if lang else ""
    pr_mode = " Push directly to main." if no_pr else " Use PR workflow (create branch, pull request, and auto-merge)."
    
    # Get open issues first
    issues = get_open_issues(["new-feature", "update-feature"], count)
    if not issues:
        print("No open issues found with labels 'new-feature' or 'update-feature'")
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


def main():
    parser = argparse.ArgumentParser(
        description="OpenSearch Feature Explorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py planner 3.0.0
  python run.py investigate --issue 123
  python run.py investigate "Star Tree" --pr 16233
  python run.py explore "Segment Replication" --lang ja
  python run.py summarize 3.0.0
  python run.py translate --feature "Segment Replication" --to ja
        """,
    )
    
    subparsers = parser.add_subparsers(dest="mode", required=True)
    
    # planner
    pl = subparsers.add_parser("planner", help="Plan release investigation and create GitHub Issues")
    pl.add_argument("version", help="Version to plan (e.g., 3.0.0)")
    pl.add_argument("--lang", help="Output language code (e.g., ja)")
    
    # investigate
    inv = subparsers.add_parser("investigate", help="Investigate a single feature")
    inv.add_argument("feature", nargs="?", help="Feature name")
    inv.add_argument("--issue", type=int, help="GitHub Issue number to investigate")
    inv.add_argument("--pr", type=int, help="Starting PR number")
    inv.add_argument("--lang", help="Output language code (e.g., ja)")
    inv.add_argument("--no-pr", action="store_true", help="Push directly to main instead of creating PR")
    
    # batch-investigate
    ba = subparsers.add_parser("batch-investigate", help="Run investigate in batch mode")
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
    
    args = parser.parse_args()
    
    if args.mode == "batch-investigate":
        count = None if getattr(args, "all", False) else (args.count or 5)
        run_batch(count, getattr(args, "lang", None), getattr(args, "no_pr", False))
    else:
        prompt = build_prompt(args.mode, args)
        run_kiro(args.mode, prompt)


if __name__ == "__main__":
    main()
