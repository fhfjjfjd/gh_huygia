#!/usr/bin/env bash
# validate-commit-msg.sh — Validate a commit message against Conventional Commits v1.0.0
# Usage: ./validate-commit-msg.sh "feat(auth): add login flow"
#    or: ./validate-commit-msg.sh  (reads last commit message)
# Exit 0 = valid, Exit 1 = invalid

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

VALID_TYPES="feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"

if [ $# -ge 1 ]; then
  MSG="$1"
else
  MSG=$(gh api "repos/{owner}/{repo}/commits?per_page=1" --jq '.[0].commit.message | split("\n") | .[0]' 2>/dev/null || echo "")
  if [ -z "$MSG" ]; then
    echo -e "${RED}❌ No commit message provided and no gh repo found${NC}"
    exit 1
  fi
  echo -e "${YELLOW}Validating last commit: ${MSG}${NC}"
fi

SUBJECT=$(echo "$MSG" | head -1)
ERRORS=()

# Check type prefix
if ! echo "$SUBJECT" | grep -qE "^($VALID_TYPES)(\(.+\))?!?:"; then
  ERRORS+=("Missing or invalid type prefix. Allowed: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert")
fi

# Check colon+space after type
if ! echo "$SUBJECT" | grep -qE "^($VALID_TYPES)(\(.+\))?!?: .+"; then
  ERRORS+=("Must have a space after colon: '<type>: <description>'")
fi

# Check length
if [ ${#SUBJECT} -gt 72 ]; then
  ERRORS+=("Subject exceeds 72 characters (${#SUBJECT} chars)")
fi

# Check uppercase start of description
DESC=$(echo "$SUBJECT" | sed -E "s/^($VALID_TYPES)(\(.+\))?!?: //")
if echo "$DESC" | grep -qE "^[A-Z]"; then
  ERRORS+=("Description must not start with uppercase letter: '${DESC}'")
fi

# Check trailing period
if echo "$SUBJECT" | grep -qE '\.$'; then
  ERRORS+=("Description must not end with a period")
fi

# Check imperative mood (common past tense patterns)
if echo "$DESC" | grep -qiE "^(added|fixed|removed|updated|changed|deleted|created|modified|improved|implemented) "; then
  ERRORS+=("Use imperative mood: 'add' not 'added', 'fix' not 'fixed'")
fi

# Check for vague messages
if echo "$DESC" | grep -qiE "^(stuff|things|misc|various|minor|wip|temp|tmp|update|changes|fix)$"; then
  ERRORS+=("Description is too vague: '${DESC}'")
fi

# Report results
if [ ${#ERRORS[@]} -eq 0 ]; then
  echo -e "${GREEN}✅ Valid Conventional Commit: ${SUBJECT}${NC}"
  exit 0
else
  echo -e "${RED}❌ Invalid commit message: ${SUBJECT}${NC}"
  echo ""
  for err in "${ERRORS[@]}"; do
    echo -e "${RED}  • ${err}${NC}"
  done
  echo ""
  echo -e "${YELLOW}Format: <type>(<scope>): <description>${NC}"
  echo -e "${YELLOW}Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert${NC}"
  exit 1
fi
