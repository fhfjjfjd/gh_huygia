#!/usr/bin/env bash
# validate-branch-name.sh — Validate branch name against naming rules
# Usage: ./validate-branch-name.sh "feat/oauth2-login"
#    or: ./validate-branch-name.sh  (validates current branch)
# Exit 0 = valid, Exit 1 = invalid

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

VALID_PREFIXES="feat|fix|hotfix|refactor|docs|ci|release|experiment"
FORBIDDEN_NAMES="main|master|develop|dev|staging|production|prod|temp|tmp|test|testing|wip"

if [ $# -ge 1 ]; then
  BRANCH="$1"
else
  BRANCH=$(cat .git/HEAD 2>/dev/null | sed 's|ref: refs/heads/||' || echo "")
  if [ -z "$BRANCH" ]; then
    echo -e "${RED}❌ No branch name provided and not in a gh repo${NC}"
    exit 1
  fi
  echo -e "${YELLOW}Validating current branch: ${BRANCH}${NC}"
fi

ERRORS=()

# Check forbidden names
if echo "$BRANCH" | grep -qE "^($FORBIDDEN_NAMES)$"; then
  ERRORS+=("'${BRANCH}' is a forbidden branch name")
fi

# Check type prefix
if ! echo "$BRANCH" | grep -qE "^($VALID_PREFIXES)/"; then
  ERRORS+=("Missing valid type prefix. Allowed: feat/, fix/, hotfix/, refactor/, docs/, ci/, release/, experiment/")
fi

# Check kebab-case (lowercase + hyphens only after prefix)
if echo "$BRANCH" | grep -qE "[A-Z]"; then
  ERRORS+=("Branch name must be lowercase (kebab-case)")
fi

if echo "$BRANCH" | grep -qE "[_]"; then
  ERRORS+=("Use hyphens (-) not underscores (_) in branch names")
fi

if echo "$BRANCH" | grep -qE " "; then
  ERRORS+=("Branch name must not contain spaces")
fi

# Check length
if [ ${#BRANCH} -gt 50 ]; then
  ERRORS+=("Branch name exceeds 50 characters (${#BRANCH} chars)")
fi

# Check for empty description after prefix
DESC_PART=$(echo "$BRANCH" | sed -E "s/^($VALID_PREFIXES)\///")
if [ -z "$DESC_PART" ] || [ "$DESC_PART" = "$BRANCH" ]; then
  ERRORS+=("Branch must have a description after the type prefix")
fi

# Report results
if [ ${#ERRORS[@]} -eq 0 ]; then
  echo -e "${GREEN}✅ Valid branch name: ${BRANCH}${NC}"
  exit 0
else
  echo -e "${RED}❌ Invalid branch name: ${BRANCH}${NC}"
  echo ""
  for err in "${ERRORS[@]}"; do
    echo -e "${RED}  • ${err}${NC}"
  done
  echo ""
  echo -e "${YELLOW}Format: <type>/<kebab-case-description>${NC}"
  echo -e "${YELLOW}Types: feat, fix, hotfix, refactor, docs, ci, release, experiment${NC}"
  exit 1
fi
