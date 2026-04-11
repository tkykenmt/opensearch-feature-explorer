#!/usr/bin/env python3
"""Migrate issues: create new with fixed links, delete old, update groups.json.

Reads migration.json for state. Resumable - saves progress after each issue.

Usage:
    # Dry run (preview first 3)
    python scripts/migrate_issues.py --dry-run --limit 3

    # Migrate one issue for testing
    python scripts/migrate_issues.py --limit 1

    # Migrate a batch
    python scripts/migrate_issues.py --limit 50

    # Migrate all remaining
    python scripts/migrate_issues.py

    # Show progress
    python scripts/migrate_issues.py --status
"""
import argparse
import json
import subprocess
import sys
import time

MIGRATION_FILE = "scripts/migration.json"


def gh(*args):
    result = subprocess.run(["gh"] + list(args), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    gh error: {result.stderr.strip()}", file=sys.stderr)
        return None
    return result.stdout.strip()


def load_migration():
    with open(MIGRATION_FILE) as f:
        return json.load(f)


def save_migration(data):
    with open(MIGRATION_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_node_id(owner, repo, number):
    out = gh("api", f"repos/{owner}/{repo}/issues/{number}", "--jq", ".node_id")
    return out


def create_issue(owner, repo, title, body, labels):
    """Create issue and return new number. Handles secondary rate limits."""
    label_args = []
    for label in labels:
        label_args.extend(["--label", label])

    for attempt in range(5):
        result = subprocess.run(
            ["gh", "api", f"repos/{owner}/{repo}/issues",
             "-f", f"title={title}", "-f", f"body={body}"]
            + [item for label in labels for item in ("-f", f"labels[]={label}")],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data["number"]
        if "secondary rate limit" in result.stderr.lower() or "HTTP 403" in result.stderr:
            wait = 60 * (attempt + 1)
            print(f"    Secondary rate limit hit. Waiting {wait}s (attempt {attempt+1}/5)...")
            time.sleep(wait)
        else:
            print(f"    gh error: {result.stderr.strip()}", file=sys.stderr)
            return None
    return None


def add_comment(owner, repo, number, body):
    for attempt in range(3):
        result = subprocess.run(
            ["gh", "issue", "comment", str(number), "-R", f"{owner}/{repo}", "--body", body],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return
        if "secondary rate limit" in result.stderr.lower() or "submitted too quickly" in result.stderr.lower():
            wait = 30 * (attempt + 1)
            print(f"    Comment rate limited. Waiting {wait}s...")
            time.sleep(wait)
        else:
            break


def close_issue(owner, repo, number):
    gh("issue", "close", str(number), "-R", f"{owner}/{repo}")


def delete_issue(owner, repo, number):
    node_id = get_node_id(owner, repo, number)
    if not node_id:
        print(f"    Could not get node_id for #{number}")
        return False
    out = gh("api", "graphql", "-f", f"query=mutation {{ deleteIssue(input: {{issueId: \"{node_id}\"}}) {{ clientMutationId }} }}")
    return out is not None


def update_groups_json(groups_files, version, old_number, new_number):
    """Update issue_number in the appropriate groups.json."""
    if not version or version not in groups_files:
        return False
    filepath = groups_files[version]
    with open(filepath) as f:
        data = json.load(f)
    updated = False
    for g in data.get("groups", []):
        if g.get("issue_number") == old_number:
            g["issue_number"] = new_number
            updated = True
            break
    if updated:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    return updated


def add_to_project(owner, repo, new_number, version):
    """Add new issue to the corresponding GitHub Project."""
    # Find project by version
    project_title = f"{version} Investigation"
    out = gh("api", "graphql", "-f", f"""query={{
  user(login: "{owner}") {{
    projectsV2(first: 50) {{
      nodes {{ id title }}
    }}
  }}
}}""")
    if not out:
        return
    projects = json.loads(out)["data"]["user"]["projectsV2"]["nodes"]
    project_id = None
    for p in projects:
        if p["title"] == project_title:
            project_id = p["id"]
            break
    if not project_id:
        return

    # Get issue node_id
    node_id = get_node_id(owner, repo, new_number)
    if not node_id:
        return

    gh("api", "graphql", "-f",
       f'query=mutation {{ addProjectV2ItemById(input: {{projectId: "{project_id}", contentId: "{node_id}"}}) {{ item {{ id }} }} }}')


def migrate_one(entry, owner, repo, groups_files, dry_run=False):
    """Migrate a single issue. Returns True if successful."""
    old_num = entry["old_number"]
    status = entry["status"]
    title = entry["title"]

    print(f"\n  #{old_num}: {title} [status={status}]")

    # Step 1: Create new issue
    if status == "pending":
        if dry_run:
            print(f"    [DRY] Would create new issue with fixed body")
            print(f"    [DRY] Labels: {entry['labels']}")
            print(f"    [DRY] Comments to copy: {len(entry['fixed_comments'])}")
            return True

        new_num = create_issue(owner, repo, title, entry["fixed_body"], entry["labels"])
        if not new_num:
            print(f"    FAILED to create new issue")
            return False
        entry["new_number"] = new_num
        entry["status"] = "created"
        print(f"    Created #{new_num}")

        # Copy comments
        for i, c in enumerate(entry["fixed_comments"]):
            add_comment(owner, repo, new_num, c["fixed"])
            print(f"    Comment {i+1}/{len(entry['fixed_comments'])} copied")

        # Close new issue if old was closed
        if entry["state"] == "CLOSED":
            close_issue(owner, repo, new_num)
            print(f"    Closed #{new_num}")

        # Add to project
        if entry.get("version"):
            add_to_project(owner, repo, new_num, entry["version"])

        status = "created"

    # Step 2: Delete old issue
    if status == "created":
        if dry_run:
            print(f"    [DRY] Would delete #{old_num}")
            return True

        if delete_issue(owner, repo, old_num):
            entry["status"] = "deleted"
            print(f"    Deleted #{old_num}")
        else:
            print(f"    FAILED to delete #{old_num}")
            return False
        status = "deleted"

    # Step 3: Update groups.json
    if status == "deleted":
        if entry["in_groups_json"] and entry.get("new_number"):
            if dry_run:
                print(f"    [DRY] Would update groups.json {entry['version']}: {old_num} -> {entry['new_number']}")
                return True
            if update_groups_json(groups_files, entry["version"], old_num, entry["new_number"]):
                print(f"    Updated groups.json: {old_num} -> {entry['new_number']}")
            else:
                print(f"    groups.json entry not found (may be OK)")
        entry["status"] = "done"

    return True


def show_status(data):
    counts = {}
    for entry in data["issues"]:
        s = entry["status"]
        counts[s] = counts.get(s, 0) + 1
    total = len(data["issues"])
    print(f"Total: {total}")
    for s in ["done", "deleted", "created", "pending"]:
        print(f"  {s}: {counts.get(s, 0)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, help="Max issues to process")
    parser.add_argument("--status", action="store_true", help="Show progress")
    args = parser.parse_args()

    data = load_migration()

    if args.status:
        show_status(data)
        return

    owner = data["owner"]
    repo = data["repo"]
    groups_files = data["groups_files"]

    pending = [e for e in data["issues"] if e["status"] != "done"]
    if not pending:
        print("All issues migrated!")
        return

    print(f"Remaining: {len(pending)}")
    if args.limit:
        pending = pending[:args.limit]
    print(f"Processing: {len(pending)}")

    for i, entry in enumerate(pending):
        print(f"\n[{i+1}/{len(pending)}]", end="")
        ok = migrate_one(entry, owner, repo, groups_files, args.dry_run)

        if not args.dry_run:
            save_migration(data)

        if not ok:
            print(f"\nStopping due to error. Progress saved.")
            break

        # Rate limit: ~15 sec between issues
        if not args.dry_run and i < len(pending) - 1:
            time.sleep(15)

    if not args.dry_run:
        print("\nProgress saved to migration.json")
        show_status(data)


if __name__ == "__main__":
    main()
