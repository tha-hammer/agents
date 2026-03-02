#!/usr/bin/env bash
# validate-indexes.sh
# Validates that RULES.md indexes match the actual filesystem contents.
# Read-only — reports mismatches but never modifies files.
#
# Usage: ./scripts/validate-indexes.sh [path-to-repo-root]
# Exit codes: 0 = all indexes valid, 1 = mismatches found

set -euo pipefail

REPO_ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
RULES_FILE="$REPO_ROOT/RULES.md"
ERRORS=0

# Colors (disable if not a terminal)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' NC=''
fi

pass() { echo -e "  ${GREEN}OK${NC}: $1"; }
fail() { echo -e "  ${RED}FAIL${NC}: $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo -e "  ${YELLOW}WARN${NC}: $1"; }

# Extract indexed paths from RULES.md for a given directory prefix.
# Looks for lines matching: * `./dir/filename.md` - description
extract_index_paths() {
    local prefix="$1"
    grep -oP "\* \`\./$(echo "$prefix" | sed 's/\//\\\//g')[^\`]*\.md\`" "$RULES_FILE" 2>/dev/null \
        | sed "s/\* \`\.\/\(.*\)\`/\1/" \
        | sort
}

# List actual .md files in a directory (non-recursive, excluding README.md)
list_actual_files() {
    local dir="$1"
    local exclude_readme="${2:-true}"
    if [ -d "$REPO_ROOT/$dir" ]; then
        local find_cmd="find $REPO_ROOT/$dir -maxdepth 1 -name '*.md' -type f"
        if [ "$exclude_readme" = "true" ]; then
            find_cmd="$find_cmd ! -name 'README.md'"
        fi
        eval "$find_cmd" | sed "s|$REPO_ROOT/||" | sort
    fi
}

echo "Validating RULES.md indexes against filesystem..."
echo "Repo root: $REPO_ROOT"
echo ""

# --- Playbooks Index ---
echo "Checking playbooks index..."
indexed_playbooks=$(extract_index_paths "playbooks/")
actual_playbooks=$(list_actual_files "playbooks")

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if [ ! -f "$REPO_ROOT/$path" ]; then
        fail "Indexed in RULES.md but missing from filesystem: $path"
    fi
done <<< "$indexed_playbooks"

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if ! echo "$indexed_playbooks" | grep -qF "$path"; then
        fail "Exists on filesystem but missing from RULES.md index: $path"
    fi
done <<< "$actual_playbooks"

indexed_count=$(echo "$indexed_playbooks" | grep -c . || true)
actual_count=$(echo "$actual_playbooks" | grep -c . || true)
if [ "$indexed_count" -eq "$actual_count" ] && [ "$ERRORS" -eq 0 ]; then
    pass "Playbooks index ($indexed_count entries)"
fi

# --- Contexts Index ---
prev_errors=$ERRORS
echo "Checking contexts index..."
indexed_contexts=$(extract_index_paths "contexts/")
actual_contexts=$(list_actual_files "contexts")

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if [ ! -f "$REPO_ROOT/$path" ]; then
        fail "Indexed in RULES.md but missing from filesystem: $path"
    fi
done <<< "$indexed_contexts"

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if ! echo "$indexed_contexts" | grep -qF "$path"; then
        fail "Exists on filesystem but missing from RULES.md index: $path"
    fi
done <<< "$actual_contexts"

indexed_count=$(echo "$indexed_contexts" | grep -c . || true)
actual_count=$(echo "$actual_contexts" | grep -c . || true)
if [ "$indexed_count" -eq "$actual_count" ] && [ "$ERRORS" -eq "$prev_errors" ]; then
    pass "Contexts index ($indexed_count entries)"
fi

# --- References Index ---
prev_errors=$ERRORS
echo "Checking references index..."
indexed_refs=$(extract_index_paths "references/")
actual_refs=$(list_actual_files "references")

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if [ ! -f "$REPO_ROOT/$path" ]; then
        fail "Indexed in RULES.md but missing from filesystem: $path"
    fi
done <<< "$indexed_refs"

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if ! echo "$indexed_refs" | grep -qF "$path"; then
        fail "Exists on filesystem but missing from RULES.md index: $path"
    fi
done <<< "$actual_refs"

indexed_count=$(echo "$indexed_refs" | grep -c . || true)
actual_count=$(echo "$actual_refs" | grep -c . || true)
if [ "$indexed_count" -eq "$actual_count" ] && [ "$ERRORS" -eq "$prev_errors" ]; then
    pass "References index ($indexed_count entries)"
fi

# --- Templates Index ---
prev_errors=$ERRORS
echo "Checking templates index..."
indexed_templates=$(extract_index_paths "templates/")
actual_templates=$(list_actual_files "templates")

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if [ ! -f "$REPO_ROOT/$path" ]; then
        fail "Indexed in RULES.md but missing from filesystem: $path"
    fi
done <<< "$indexed_templates"

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if ! echo "$indexed_templates" | grep -qF "$path"; then
        fail "Exists on filesystem but missing from RULES.md index: $path"
    fi
done <<< "$actual_templates"

indexed_count=$(echo "$indexed_templates" | grep -c . || true)
actual_count=$(echo "$actual_templates" | grep -c . || true)
if [ "$indexed_count" -eq "$actual_count" ] && [ "$ERRORS" -eq "$prev_errors" ]; then
    pass "Templates index ($indexed_count entries)"
fi

# --- Downtime Tasks Index ---
prev_errors=$ERRORS
echo "Checking downtime tasks index..."
indexed_downtime=$(extract_index_paths "downtime/")
actual_downtime=$(list_actual_files "downtime")

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if [ ! -f "$REPO_ROOT/$path" ]; then
        fail "Indexed in RULES.md but missing from filesystem: $path"
    fi
done <<< "$indexed_downtime"

while IFS= read -r path; do
    [ -z "$path" ] && continue
    if ! echo "$indexed_downtime" | grep -qF "$path"; then
        fail "Exists on filesystem but missing from RULES.md index: $path"
    fi
done <<< "$actual_downtime"

indexed_count=$(echo "$indexed_downtime" | grep -c . || true)
actual_count=$(echo "$actual_downtime" | grep -c . || true)
if [ "$indexed_count" -eq "$actual_count" ] && [ "$ERRORS" -eq "$prev_errors" ]; then
    pass "Downtime tasks index ($indexed_count entries)"
fi

# --- Summary ---
echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo -e "${GREEN}All indexes are valid.${NC}"
    exit 0
else
    echo -e "${RED}Found $ERRORS index mismatch(es).${NC}"
    exit 1
fi
