#!/usr/bin/env python3
"""OpenSearch Feature Explorer - Kiro CLI wrapper script."""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
AGENTS_DIR = SCRIPT_DIR / ".kiro" / "agents"

AGENTS = {
    "release-analyze": "release-analyze.json",
    "feature-report": "feature-report.json",
    "context-update": "context-update.json",
    "explore": "explore.json",
    "translate": "translate.json",
}

def build_prompt(mode: str, args: argparse.Namespace) -> str:
    """Build initial prompt based on mode and arguments."""
    lang_instruction = ""
    if hasattr(args, "lang") and args.lang:
        langs = [l.strip() for l in args.lang.split(",")]
        if len(langs) == 1 and langs[0] != "en":
            lang_instruction = f" Output in language code '{langs[0]}'. Use suffix '.{langs[0]}.md' for output files."
        elif len(langs) > 1:
            suffixes = ", ".join([f"'.{l}.md'" if l != "en" else "'.md'" for l in langs])
            lang_instruction = f" Output in languages: {', '.join(langs)}. Use suffixes: {suffixes}."
    
    if mode == "release-analyze":
        return f"Analyze OpenSearch release version {args.version}.{lang_instruction}"
    
    if mode == "feature-report":
        prompt = f'Create a feature report for "{args.feature}"'
        if args.pr:
            prompt += f" starting from PR #{args.pr}"
        if args.issue:
            prompt += f" starting from Issue #{args.issue}"
        if args.url:
            prompt += f" using documentation at {args.url}"
        return prompt + f".{lang_instruction}"
    
    if mode == "context-update":
        return f'Update the feature report for "{args.feature}" with context from {args.url}.{lang_instruction}'
    
    if mode == "explore":
        lang = args.lang if hasattr(args, "lang") and args.lang else "en"
        return f'Explore the "{args.feature}" feature in language code "{lang}"'
    
    if mode == "translate":
        suffix = f".{args.to}.md" if args.to != "en" else ".md"
        if args.feature:
            return f'Translate the feature report "features/{args.feature}.md" to language code "{args.to}". Save as "features/{args.feature}{suffix}"'
        if args.release:
            return f'Translate all reports in "releases/v{args.release}/" to language code "{args.to}". Use suffix "{suffix}" for output files.'
        return ""
    
    return ""

def run_kiro(mode: str, prompt: str, interactive: bool = False):
    """Run kiro-cli with the appropriate agent."""
    agent_name = AGENTS[mode].replace(".json", "")
    
    cmd = [
        "kiro-cli", "chat",
        "--agent", agent_name,
        "--model", "claude-opus-4.5",
    ]
    
    if prompt:
        cmd.append(prompt)
    
    subprocess.run(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="OpenSearch Feature Explorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py release-analyze 3.4.0
  python run.py release-analyze 3.4.0 --lang ja
  python run.py release-analyze 3.4.0 --lang en,ja
  python run.py feature-report "Segment Replication"
  python run.py feature-report "Star Tree" --pr 16233 --lang en,ja
  python run.py context-update --url https://... --feature "Remote Store"
  python run.py explore "Segment Replication" --lang ja
  python run.py translate --feature "Segment Replication" --to ja
  python run.py translate --release 3.4.0 --to ja
        """,
    )
    
    subparsers = parser.add_subparsers(dest="mode", required=True)
    
    # release-analyze
    ra = subparsers.add_parser("release-analyze", help="Analyze a release version")
    ra.add_argument("version", help="Version to analyze (e.g., 3.4.0)")
    ra.add_argument("--lang", help="Output language(s): en, ja, or en,ja")
    
    # feature-report
    fr = subparsers.add_parser("feature-report", help="Create/update a feature report")
    fr.add_argument("feature", help="Feature name")
    fr.add_argument("--pr", type=int, help="Starting PR number")
    fr.add_argument("--issue", type=int, help="Starting Issue number")
    fr.add_argument("--url", help="Documentation URL")
    fr.add_argument("--lang", help="Output language(s): en, ja, or en,ja")
    
    # context-update
    cu = subparsers.add_parser("context-update", help="Update feature with external context")
    cu.add_argument("--url", required=True, help="External URL to fetch context from")
    cu.add_argument("--feature", required=True, help="Feature to update")
    cu.add_argument("--lang", help="Output language(s): en, ja, or en,ja")
    
    # explore
    ex = subparsers.add_parser("explore", help="Explore a feature interactively and update reports")
    ex.add_argument("feature", help="Feature name to explore")
    ex.add_argument("--lang", help="Response language code (e.g., ja, zh, ko)")
    
    # translate
    tr = subparsers.add_parser("translate", help="Translate existing reports")
    tr.add_argument("--feature", help="Feature name to translate")
    tr.add_argument("--release", help="Release version to translate")
    tr.add_argument("--to", required=True, help="Target language code (e.g., ja, zh, ko)")
    
    args = parser.parse_args()
    prompt = build_prompt(args.mode, args)
    
    # explore mode is interactive
    interactive = args.mode == "explore"
    run_kiro(args.mode, prompt, interactive)

if __name__ == "__main__":
    main()
