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
  # For multi-line messages, preserve the full message
  MSG="$1"
else
  # Get full commit message from git
  MSG=$(git log -1 --pretty=%B 2>/dev/null || gh api "repos/{owner}/{repo}/commits?per_page=1" --jq '.[0].commit.message' 2>/dev/null || echo "")
  if [ -z "$MSG" ]; then
    echo -e "${RED}❌ No commit message provided and no git/gh repo found${NC}"
    exit 1
  fi
  echo -e "${YELLOW}Validating last commit: ${MSG}${NC}"
fi

# Extract first line as subject
SUBJECT=$(echo -e "$MSG" | head -n 1)
ERRORS=()

# Check type prefix (with optional scope and breaking change indicator)
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

# Extract description (after type, scope, and colon)
DESC=$(echo "$SUBJECT" | sed -E "s/^($VALID_TYPES)(\(.+\))?!?: //")
if [[ "$SUBJECT" =~ ^($VALID_TYPES): ]]; then
  # No scope case
  DESC=$(echo "$SUBJECT" | sed -E "s/^($VALID_TYPES): //")
elif [[ "$SUBJECT" =~ ^($VALID_TYPES)\(.+\): ]]; then
  # With scope case
  DESC=$(echo "$SUBJECT" | sed -E "s/^($VALID_TYPES)\(.+\): //")
elif [[ "$SUBJECT" =~ ^($VALID_TYPES)\(.+\)!: ]]; then
  # With breaking change case
  DESC=$(echo "$SUBJECT" | sed -E "s/^($VALID_TYPES)\(.+\)!: //")
fi

# Check uppercase start of description
if echo "$DESC" | grep -qE "^[A-Z]"; then
  ERRORS+=("Description must not start with uppercase letter: '${DESC}'")
fi

# Check trailing period in subject
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

# Parse multi-line message for body and footer
LINES=()
while IFS= read -r line; do
  LINES+=("$line")
done <<< "$MSG"

# Check for multi-line message
if [ ${#LINES[@]} -gt 1 ]; then
  # Skip first line (subject) and empty lines between subject and body
  i=1
  while [ $i -lt ${#LINES[@]} ] && [ -z "${LINES[$i]}" ]; do
    ((i++))
  done
  
  # Validate body if present (after empty line following subject)
  if [ $i -lt ${#LINES[@]} ]; then
    # Check if this is actually a footer by looking for footer format
    FOOTER_FOUND=false
    j=$i
    while [ $j -lt ${#LINES[@]} ]; do
      line="${LINES[$j]}"
      
      # Check if line matches footer format (token: value or BREAKING CHANGE)
      if [[ "$line" =~ ^[A-Z][A-Za-z-]*: ]] || [[ "$line" =~ ^BREAKING[[:space:]]CHANGE(:|\() ]]; then
        FOOTER_FOUND=true
        if [ $j -gt $i ]; then
          # Validate body lines before footer
          k=$i
          while [ $k -lt $j ]; do
            body_line="${LINES[$k]}"
            if [ ${#body_line} -gt 72 ]; then
              ERRORS+=("Body line exceeds 72 characters: '${body_line}'")
            fi
            ((k++))
          done
        fi
      fi
      ((j++))
    done
    
    # If footer wasn't found and there are lines remaining, validate as body
    if [ "$FOOTER_FOUND" = false ]; then
      while [ $i -lt ${#LINES[@]} ]; do
        body_line="${LINES[$i]}"
        if [ ${#body_line} -gt 72 ]; then
          ERRORS+=("Body line exceeds 72 characters: '${body_line}'")
        fi
        ((i++))
      done
    fi
    
    # Now validate footers
    j=0
    while [ $j -lt ${#LINES[@]} ]; do
      line="${LINES[$j]}"
      if [[ "$line" =~ ^BREAKING[[:space:]]CHANGE(:|\() ]]; then
        # Validate BREAKING CHANGE footer format
        if [[ ! "$line" =~ ^BREAKING[[:space:]]CHANGE:[[:space:]]+.+ ]] && [[ ! "$line" =~ ^BREAKING[[:space:]]CHANGE\([a-zA-Z0-9_\-]+\):[[:space:]]+.+ ]]; then
          ERRORS+=("BREAKING CHANGE footer must follow format: 'BREAKING CHANGE: <description>' or 'BREAKING CHANGE(scope): <description>': '${line}'")
        fi
      elif [[ "$line" =~ ^[A-Z][A-Za-z-]*: ]]; then
        # Validate other footer tokens (like "Closes", "Refs", etc.)
        footer_key=$(echo "$line" | cut -d: -f1)
        footer_value=$(echo "$line" | cut -d: -f2- | sed 's/^ *//')
        
        if [ -z "$footer_value" ]; then
          ERRORS+=("Footer '${footer_key}:' must have a value after the colon")
        fi
      fi
      ((j++))
    done
  fi
fi

# Check breaking change marker consistency
if [[ "$SUBJECT" =~ ^($VALID_TYPES)\(.+\)!: ]] || [[ "$SUBJECT" =~ ^($VALID_TYPES)!: ]]; then
  # If breaking change marker (!) is in subject, ensure there's a BREAKING CHANGE footer
  has_breaking_footer=false
  for line in "${LINES[@]}"; do
    if [[ "$line" =~ ^BREAKING[[:space:]]CHANGE ]]; then
      has_breaking_footer=true
      break
    fi
  done
  
  if [ "$has_breaking_footer" = false ]; then
    ERRORS+=("Breaking change commit (with !) must include a BREAKING CHANGE footer")
  fi
elif [[ "$MSG" =~ BREAKING[[:space:]]CHANGE ]]; then
  # If there's a BREAKING CHANGE footer but no ! in subject, it's invalid
  ERRORS+=("BREAKING CHANGE footer requires a breaking change marker (!) in the subject line")
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
  echo -e "${YELLOW}Format: <type>(<scope>)!: <description>${NC}"
  echo -e "${YELLOW}      <BLANK LINE>${NC}"
  echo -e "${YELLOW}      <body>${NC}"
  echo -e "${YELLOW}      <BLANK LINE>${NC}"
  echo -e "${YELLOW}      BREAKING CHANGE: <breaking change description>${NC}"
  echo -e "${YELLOW}      <footer>${NC}"
  echo ""
  echo -e "${YELLOW}Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert${NC}"
  exit 1
fi