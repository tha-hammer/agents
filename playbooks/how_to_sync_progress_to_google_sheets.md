# Playbook: Sync Progress to Google Sheets

*Status: Stable*

## Objective
Push kanban state, daily intentions, and progress to a shared Google Sheet so the team has visibility without needing access to git.

## Prerequisites

- Google Sheet with three tabs: `Kanban`, `Daily Log`, `This Week`.
- Apps Script webhook deployed on the sheet (see `scripts/google_apps_script.js`).
- `SHEETS_WEBHOOK_URL` set in `.env` at the repo root.

## Setup (One-Time)

1. Open the Google Sheet.
2. Go to **Extensions > Apps Script**.
3. Replace the default code with the contents of `scripts/google_apps_script.js`.
4. Click **Deploy > New deployment**.
5. Set type to **Web app**, execute as **Me**, access **Anyone**.
6. Authorize and copy the deployment URL.
7. Create `.env` in the repo root (use `.env.example` as reference):
   ```
   SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/YOUR_ID/exec
   ```

## Step-by-Step Instructions

### Manual Sync

1. Run the sync script:
   ```bash
   python3 scripts/sync_to_sheets.py
   ```
2. Verify the Google Sheet updated with current kanban and journal state.

### Selective Sync

- Kanban only: `python3 scripts/sync_to_sheets.py --kanban`
- Daily log only: `python3 scripts/sync_to_sheets.py --journal`
- This week only: `python3 scripts/sync_to_sheets.py --this-week`

### Dry Run (Preview Without Posting)

```bash
python3 scripts/sync_to_sheets.py --dry-run
```

### Auto Sync on Commit

After any checkpoint commit (journal or general), run the sync script before or after push:
```bash
git commit ... && python3 scripts/sync_to_sheets.py && git push
```

Agents SHOULD run the sync script after every checkpoint commit when `SHEETS_WEBHOOK_URL` is configured.

## What Gets Synced

| Tab | Source | Behavior |
|---|---|---|
| Kanban | `kanban/*.md` | Snapshot replace — clears and rewrites all tasks |
| Daily Log | `journal/YYYY-MM-DD.md` | Upsert — updates today's row or appends new |
| This Week | `kanban/today.md` + `kanban/this_week.md` | Snapshot replace — planning horizon view |

## Verification

- Google Sheet `Kanban` tab matches tasks in `kanban/*.md`.
- Google Sheet `Daily Log` tab has an entry for today with correct intentions.
- Google Sheet `This Week` tab shows tasks from `today.md` and `this_week.md`.
- Dry run output matches expected payload structure.

## Lifecycle Compliance

This playbook extends the commit workflow. After checkpoint commits:
1. Run sync script.
2. Verify sheet updated.
3. Continue with push.

## Future: Service Account Migration

When ready for more robust sync, replace the webhook transport with direct Google Sheets API via a GCP service account and `gspread`. The Python script's `sync()` function is the integration point — swap the POST call for direct API writes.
