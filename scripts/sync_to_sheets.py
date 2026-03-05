#!/usr/bin/env python3
"""Sync kanban boards and journal entries to Google Sheets via Apps Script webhook.

Usage:
    python3 scripts/sync_to_sheets.py              # sync all
    python3 scripts/sync_to_sheets.py --kanban      # kanban tab only
    python3 scripts/sync_to_sheets.py --journal     # daily log tab only
    python3 scripts/sync_to_sheets.py --this-week   # this week tab only
    python3 scripts/sync_to_sheets.py --dry-run     # print payload, don't POST

Requires SHEETS_WEBHOOK_URL environment variable (or .env file in repo root).
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
KANBAN_DIR = REPO_ROOT / "kanban"
JOURNAL_DIR = REPO_ROOT / "journal"
ENV_FILE = REPO_ROOT / ".env"


def load_env():
    """Load SHEETS_WEBHOOK_URL from .env if not already set."""
    if os.environ.get("SHEETS_WEBHOOK_URL"):
        return
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip("\"'"))


def get_webhook_url():
    load_env()
    url = os.environ.get("SHEETS_WEBHOOK_URL", "")
    if not url:
        print("ERROR: SHEETS_WEBHOOK_URL not set. Add it to .env or export it.", file=sys.stderr)
        sys.exit(1)
    return url


# -- Kanban parsing -----------------------------------------------------------

def parse_kanban_file(filepath):
    """Parse a kanban markdown file into task dicts."""
    text = filepath.read_text()
    board_name = filepath.stem  # e.g., "today", "this_week"

    tasks = []
    current_section = None
    today_str = date.today().isoformat()

    for line in text.splitlines():
        stripped = line.strip()

        # Detect section headers
        if stripped.startswith("## To Do"):
            current_section = "To Do"
        elif stripped.startswith("## Doing"):
            current_section = "Doing"
        elif stripped.startswith("## Done"):
            current_section = "Done"
        elif stripped.startswith("## "):
            current_section = None  # Metadata or other section
        elif current_section and stripped.startswith("- ") and not stripped.startswith("<!--"):
            task_text = stripped[2:].strip()
            if task_text:
                tasks.append({
                    "board": board_name,
                    "task": task_text,
                    "status": current_section,
                    "updated": today_str,
                })

    return tasks


def collect_kanban():
    """Collect tasks from all kanban board files."""
    all_tasks = []
    for md_file in sorted(KANBAN_DIR.glob("*.md")):
        all_tasks.extend(parse_kanban_file(md_file))
    return all_tasks


# -- Journal parsing ----------------------------------------------------------

def parse_journal_file(filepath):
    """Parse a journal markdown file into a daily log entry."""
    text = filepath.read_text()

    # Extract date from filename
    journal_date = filepath.stem  # e.g., "2026-03-02"

    intentions = extract_section(text, "Today's Intentions")
    work_log = extract_section(text, "Repo Work Log (Required)")

    # Extract recent commit hashes from work log lines
    commits = []
    for line in work_log.splitlines():
        # Look for 7-char hex commit refs in brackets or standalone
        hashes = re.findall(r'\b[0-9a-f]{7,40}\b', line)
        commits.extend(hashes)

    return {
        "date": journal_date,
        "intentions": intentions.strip() or "-",
        "work_completed": work_log.strip() or "-",
        "commits": ", ".join(commits) if commits else "-",
    }


def extract_section(text, heading):
    """Extract content between a ## heading and the next ## heading."""
    pattern = rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        return ""

    content = match.group(1).strip()
    # Clean up: remove empty list items and join meaningful lines
    lines = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped and stripped != "-" and not stripped.startswith("<!--"):
            # Remove leading "- " for cleaner sheet display
            if stripped.startswith("- "):
                stripped = stripped[2:]
            lines.append(stripped)
    return "\n".join(lines)


def get_today_journal():
    """Get today's journal entry, or the most recent one."""
    today_file = JOURNAL_DIR / f"{date.today().isoformat()}.md"
    if today_file.exists():
        return parse_journal_file(today_file)

    # Fall back to most recent
    journal_files = sorted(JOURNAL_DIR.glob("*.md"), reverse=True)
    if journal_files:
        return parse_journal_file(journal_files[0])

    return None


# -- This Week collection -----------------------------------------------------

def collect_this_week():
    """Collect tasks from this_week.md and today.md for the This Week view."""
    tasks = []
    for board_name in ["today", "this_week"]:
        filepath = KANBAN_DIR / f"{board_name}.md"
        if filepath.exists():
            tasks.extend(parse_kanban_file(filepath))
    return [
        {"task": t["task"], "board": t["board"], "status": t["status"], "notes": ""}
        for t in tasks
    ]


# -- Daily Metrics collection -------------------------------------------------

def collect_daily_metrics():
    """Calculate task completion ratio and scope creep indicator from today.md."""
    today_file = KANBAN_DIR / "today.md"
    if not today_file.exists():
        return None

    text = today_file.read_text()

    # Count tasks by status
    to_do_count = 0
    doing_count = 0
    done_count = 0
    current_section = None

    for line in text.splitlines():
        stripped = line.strip()

        # Detect section headers
        if stripped.startswith("## To Do"):
            current_section = "To Do"
        elif stripped.startswith("## Doing"):
            current_section = "Doing"
        elif stripped.startswith("## Done"):
            current_section = "Done"
        elif stripped.startswith("## "):
            current_section = None
        elif current_section and stripped.startswith("- ") and not stripped.startswith("<!--"):
            task_text = stripped[2:].strip()
            if task_text and not task_text.startswith("DEADLINE") and not task_text.startswith("Agent"):
                if current_section == "To Do":
                    to_do_count += 1
                elif current_section == "Doing":
                    doing_count += 1
                elif current_section == "Done":
                    done_count += 1

    total_tasks = to_do_count + doing_count + done_count
    if total_tasks == 0:
        return None

    completion_ratio = (done_count / total_tasks) * 100

    return {
        "date": date.today().isoformat(),
        "to_do": to_do_count,
        "doing": doing_count,
        "done": done_count,
        "total": total_tasks,
        "completion_ratio": round(completion_ratio, 1),
        "completion_pct": f"{round(completion_ratio, 1)}%"
    }


# -- Sync --------------------------------------------------------------------

def sync(kanban=True, journal=True, this_week=True, dry_run=False):
    """Build payload and POST to webhook."""
    payload = {}

    if kanban:
        payload["kanban"] = collect_kanban()
        # Always include daily metrics with kanban
        metrics = collect_daily_metrics()
        if metrics:
            payload["daily_metrics"] = metrics

    if journal:
        entry = get_today_journal()
        if entry:
            payload["daily_log"] = entry

    if this_week:
        payload["this_week"] = collect_this_week()

    if not payload:
        print("Nothing to sync.")
        return

    if dry_run:
        print(json.dumps(payload, indent=2))
        return

    url = get_webhook_url()
    print(f"Syncing to Google Sheets...")

    resp = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    if resp.status_code == 200:
        result = resp.json() if resp.text else {}
        status = result.get("status", "unknown")
        if status == "ok":
            print(f"Sync complete. Pushed: {', '.join(payload.keys())}")
        else:
            print(f"Webhook returned: {result}", file=sys.stderr)
    else:
        print(f"HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)


# -- CLI ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sync kanban/journal to Google Sheets")
    parser.add_argument("--kanban", action="store_true", help="Sync kanban tab only")
    parser.add_argument("--journal", action="store_true", help="Sync daily log tab only")
    parser.add_argument("--this-week", action="store_true", help="Sync this week tab only")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without POSTing")
    args = parser.parse_args()

    # If no specific tab selected, sync all
    sync_all = not (args.kanban or args.journal or args.this_week)

    sync(
        kanban=sync_all or args.kanban,
        journal=sync_all or args.journal,
        this_week=sync_all or args.this_week,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
