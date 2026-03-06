# Commit Message Rules — Conventional Commits v1.0.0

## Full Specification

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Allowed Types

| Type | Description | SemVer Impact |
|------|-------------|---------------|
| `feat` | New feature | MINOR bump |
| `fix` | Bug fix | PATCH bump |
| `docs` | Documentation only | None |
| `style` | Formatting, whitespace; no logic change | None |
| `refactor` | Code change that neither fixes a bug nor adds a feature | None |
| `perf` | Performance improvement | PATCH bump |
| `test` | Adding or correcting tests | None |
| `build` | Build system or external dependencies | None |
| `ci` | CI configuration files and scripts | None |
| `chore` | Maintenance tasks (e.g., .gitignore updates) | None |
| `revert` | Reverts a previous commit | Depends |

### Subject/Description Rules

- MUST use imperative mood: "add", "fix", "change" — NOT "added", "fixes", "changed"
- MUST NOT start with uppercase letter
- MUST NOT end with a period (.)
- MUST NOT exceed 72 characters on the first line
- MUST be meaningful and descriptive

### Body Rules

- MUST be separated from subject by a blank line
- SHOULD wrap at 72 characters per line
- SHOULD explain WHAT and WHY, not HOW
- MAY use bullet points with `-` or `*`

### Footer Rules

- `BREAKING CHANGE: <description>` — REQUIRED for breaking changes (MAY also use `!` in type)
- `Closes #<issue>` or `Fixes #<issue>` — SHOULD be included when applicable
- `Reviewed-by: <name>` — MAY be included
- `Refs: #<issue>` — MAY be included for related issues

### Breaking Changes

- MUST be indicated by `!` after type/scope: `feat(api)!: change response format`
- AND/OR by `BREAKING CHANGE:` footer in commit body
- Breaking changes ALWAYS correlate with MAJOR version bump

### Atomic Commits

- Each commit MUST represent ONE logical change
- FORBIDDEN: mixing unrelated changes in one commit
- FORBIDDEN: "fix typo" commits that also refactor code
- If you need to fix a typo AND add a feature, make TWO separate commits

### Staging Rules

- MUST use `git add <specific-file-1> <specific-file-2>` to stage only relevant files
- FORBIDDEN: `git add -A` — stages everything including unrelated changes
- FORBIDDEN: `git add .` — same problem as above
- FORBIDDEN: `git add --all` — same problem as above
- Before committing, MUST verify staged files with `git status` or `git diff --cached`

---

## Examples

### ✅ GOOD Examples

```bash
# Simple feature
git add src/auth/oauth.ts src/auth/oauth.test.ts
git commit -m "feat(auth): add OAuth2 login flow"

# Bug fix with scope
git add src/api/users.ts
git commit -m "fix(api): resolve null pointer in user endpoint"

# Breaking change with ! notation
git add src/api/response.ts src/api/types.ts
git commit -m "feat(api)!: change response format to JSON:API"

# Breaking change with footer
git add src/api/v2/
git commit -m "feat(api): migrate to v2 endpoint structure

BREAKING CHANGE: all v1 endpoints are removed. Clients must update to /api/v2/"

# Documentation
git add README.md
git commit -m "docs: add installation instructions for Termux"

# Performance improvement
git add src/utils/parser.ts
git commit -m "perf(parser): optimize JSON parsing with streaming"

# Chore with body
git add .gitignore
git commit -m "chore: update .gitignore for Android build artifacts

Add entries for .gradle/, build/, and .apk files"

# Revert
git commit -m "revert: revert feat(auth): add OAuth2 login flow

This reverts commit abc1234.
Reason: OAuth provider API is not stable yet."

# CI change
git add .github/workflows/ci.yml
git commit -m "ci: add automated test workflow for pull requests"

# Test
git add tests/auth.test.ts
git commit -m "test(auth): add unit tests for token refresh flow"

# Style
git add src/components/Button.tsx
git commit -m "style(ui): fix indentation in Button component"

# Build
git add package.json package-lock.json
git commit -m "build(deps): upgrade typescript to v5.4"
```

### ❌ BAD Examples

```bash
# Vague message — REJECTED
git commit -m "fixed stuff"
# Why: No type prefix. "stuff" is meaningless. Past tense.

# WIP commit — REJECTED
git commit -m "WIP"
# Why: No type prefix. Not descriptive. Not atomic.

# Generic "update" — REJECTED
git commit -m "update"
# Why: No type prefix. What was updated? Why?

# Past tense — REJECTED
git commit -m "feat: added login page"
# Why: "added" should be "add" (imperative mood)

# Uppercase first letter — REJECTED
git commit -m "feat: Add login page"
# Why: Description must not start with uppercase

# Period at end — REJECTED
git commit -m "feat: add login page."
# Why: Description must not end with period

# Too long (>72 chars) — REJECTED
git commit -m "feat(authentication): add the new OAuth2 login flow with Google and GitHub providers including error handling"
# Why: Exceeds 72 character limit. Break into subject + body.

# Wrong type — REJECTED
git commit -m "feature: add login page"
# Why: "feature" is not valid. Use "feat"

# Multiple unrelated changes — REJECTED
git add -A
git commit -m "feat: add login and fix header and update docs"
# Why: Not atomic. Three changes = three commits. Also git add -A is FORBIDDEN.

# No type prefix — REJECTED
git commit -m "add login page"
# Why: Missing type prefix (feat/fix/docs/etc.)

# Ticket number only — REJECTED
git commit -m "PROJ-123"
# Why: Not a Conventional Commit. No type, no description.

# Emoji prefix — REJECTED
git commit -m "✨ add login page"
# Why: Emojis are not part of Conventional Commits spec

# git add -A — FORBIDDEN
git add -A && git commit -m "feat: add login page"
# Why: git add -A stages EVERYTHING. Must stage specific files.

# git add . — FORBIDDEN
git add . && git commit -m "fix: resolve bug"
# Why: git add . stages all changes in current directory. Must be specific.
```

---

## Commit Message Template

```
<type>(<scope>): <imperative-mood-description-max-72-chars>

<optional body: explain WHAT changed and WHY, wrap at 72 chars>

<optional footers>
BREAKING CHANGE: <description if applicable>
Closes #<issue-number>
Reviewed-by: <name>
```
