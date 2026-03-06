# AI Coding Agent Compliance Rules

> ALL AI coding agents MUST comply with every rule defined in the parent SKILL.md.
> This file provides specific instructions for each agent on HOW to comply.

---

## Universal Rules (ALL Agents MUST Follow)

### 1. File Staging — FORBIDDEN: `git add -A`, `git add .`, `git add --all`

Every agent MUST stage files individually:

```bash
# ✅ CORRECT — stage specific files
git add src/auth/login.ts src/auth/login.test.ts

# ❌ FORBIDDEN — stages everything
git add -A
git add .
git add --all
```

Before committing, MUST verify what is staged:

```bash
git status
git diff --cached --name-only
```

### 2. Commit Messages — Conventional Commits Format

```bash
# ✅ CORRECT
git commit -m "feat(auth): add OAuth2 login flow"

# ❌ FORBIDDEN
git commit -m "update files"
git commit -m "WIP"
git commit -m "fixed stuff"
```

### 3. Branch Creation — Type Prefix Required

```bash
# ✅ CORRECT
git checkout -b feat/oauth2-login

# ❌ FORBIDDEN
git checkout -b my-changes
```

MUST NOT commit directly to `main` or `master`.

### 4. Creating PRs — Full Template Required

```bash
gh pr create \
  --title "feat(auth): add OAuth2 login flow" \
  --body "## Summary
<description>

## Changes
- <change 1>
- <change 2>

## Related Issues
Closes #42

## Testing
- [ ] Tests pass

## Checklist
- [ ] Conventional commits followed
- [ ] No secrets committed
- [ ] CI passes" \
  --base main
```

### 5. Creating Issues — Template + Labels Required

```bash
gh issue create \
  --title "fix(api): handle invalid user ID gracefully" \
  --body "<full bug report or feature request template>" \
  --label "type:bug,priority:P1"
```

### 6. Merging — Squash + Delete Branch

```bash
gh pr merge <number> --squash --delete-branch
```

MUST NOT merge with failing CI.

---

## Gemini CLI (Google)

### Context File: `GEMINI.md`

Gemini CLI reads `GEMINI.md` in the project root for persistent instructions.

### ⚠️ CRITICAL WARNING

Gemini CLI's default behavior when using Shell tool may execute `git add .` or chain
commands like `git add . && git commit`. This MUST be explicitly prevented.

### How to Enforce Rules in GEMINI.md

Add the following to your project's `GEMINI.md`:

```markdown
# Git Rules — STRICTLY ENFORCED

## Commit Rules
- ALL commits MUST follow Conventional Commits: <type>(<scope>): <description>
- Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- Use imperative mood, no uppercase start, no period, max 72 chars

## Staging Rules — CRITICAL
- NEVER use `git add -A`, `git add .`, or `git add --all`
- ALWAYS stage specific files: `git add <file1> <file2>`
- ALWAYS run `git status` before committing to verify staged files

## Branch Rules
- Create branches with type prefix: feat/, fix/, hotfix/, refactor/, docs/, ci/
- Use kebab-case, max 50 chars
- NEVER commit directly to main

## PR Rules
- Use `gh pr create` with Conventional Commits title and full body template
- Always include: Summary, Changes, Related Issues, Testing, Checklist

## Issue Rules
- Use `gh issue create` with full template body
- Always include labels: --label "type:bug,priority:P1"
```

### Gemini CLI Commands

```bash
# Gemini CLI uses Shell tool — same as regular bash commands
# All git and gh commands work normally

# Stage specific files (through Gemini's Shell tool)
git add src/auth/login.ts

# Commit with conventional format
git commit -m "feat(auth): add login endpoint"

# Create PR via gh CLI
gh pr create --title "feat(auth): add login endpoint" --body "..."

# Create issue via gh CLI
gh issue create --title "fix(api): handle error" --body "..." --label "type:bug,priority:P1"
```

---

## Claude Code (Anthropic)

### Context File: `CLAUDE.md`

Claude Code reads `CLAUDE.md` in the project root for persistent instructions.

### Built-in Git Integration

Claude Code has native git integration with permission tiers:
- **Read-only**: Can view diffs, status, log
- **Edit**: Can modify files
- **Shell**: Can run arbitrary commands including git and gh

### How to Enforce Rules in CLAUDE.md

Add the following to your project's `CLAUDE.md`:

```markdown
# Git Rules — STRICTLY ENFORCED

## CRITICAL: Staging
- NEVER use `git add -A`, `git add .`, or `git add --all`
- ALWAYS use `git add <specific-file>` for each relevant file
- Run `git diff --cached --name-only` before every commit

## Commits
- Follow Conventional Commits v1.0.0: <type>(<scope>): <description>
- Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- Imperative mood, lowercase start, no period, ≤72 chars

## Branches
- Always create: git checkout -b <type>/<kebab-case-name>
- Never commit to main directly

## PRs
- Use gh pr create with full template body
- Title must follow Conventional Commits

## Issues
- Use gh issue create with full template and labels
```

### Claude Code Custom Slash Commands

Create `.claude/commands/commit.md` to enforce commit rules:

```markdown
# /commit - Create a Conventional Commit

When the user runs /commit:
1. Run `git diff --cached --name-only` to see staged files
2. If no files staged, ask user to stage specific files (NEVER use git add -A)
3. Analyze the diff to determine the appropriate type
4. Generate a Conventional Commits message
5. Confirm with user before executing git commit
```

### Claude Code Specific Commands

```bash
# Claude Code can use its built-in tools or shell
# All git and gh commands work via shell access

git add src/auth/login.ts
git commit -m "feat(auth): add login endpoint"
gh pr create --title "feat(auth): add login" --body "..."
```

---

## Amp / ampcode (Sourcegraph)

### Context File: `AGENTS.md`

Amp reads `AGENTS.md` in the project root and parent directories.

### Skills System

This very skill (`managing-github-events`) IS the enforcement mechanism for Amp.
When this skill is loaded, Amp MUST follow all rules automatically.

### How to Enforce Rules in AGENTS.md

Add the following to your project's `AGENTS.md`:

```markdown
# Git Rules

See @~/.config/agents/skills/managing-github-events/SKILL.md for full rules.

## Quick Rules
- Commits: Conventional Commits format (feat/fix/docs/etc.)
- Staging: NEVER use `git add -A` or `git add .` — stage specific files only
- Branches: Always use type/ prefix (feat/, fix/, etc.)
- PRs: Use gh pr create with full template
- Issues: Use gh issue create with template + labels
```

### Amp Specific Tools

```bash
# Amp uses Bash tool for all git/gh operations

# Stage specific files (Amp's Bash tool)
git add src/auth/login.ts

# Commit
git commit -m "feat(auth): add login endpoint"

# Create PR
gh pr create --title "feat(auth): add login" --body "..."

# Create issue
gh issue create --title "fix(api): error" --body "..." --label "type:bug,priority:P1"

# Squash merge and delete branch
gh pr merge 42 --squash --delete-branch
```

### Amp Permission Configuration

In `~/.config/amp/settings.json`, configure permissions to ask before git operations:

```json
{
  "amp.permissions": [
    {"tool": "Bash", "matches": {"cmd": "*git commit*"}, "action": "ask"},
    {"tool": "Bash", "matches": {"cmd": "*git push*"}, "action": "ask"},
    {"tool": "Bash", "matches": {"cmd": "*git add -A*"}, "action": "reject"},
    {"tool": "Bash", "matches": {"cmd": "*git add .*"}, "action": "reject"},
    {"tool": "Bash", "matches": {"cmd": "*git add --all*"}, "action": "reject"}
  ]
}
```

---

## iFlow CLI

### Context File: `IFLOW.md`

iFlow CLI reads `IFLOW.md` in the project root for persistent instructions.
Created via the `/init` command.

### Operating Modes

| Mode | Description | Recommendation |
|------|-------------|----------------|
| YOLO | Full access, no confirmation | ⚠️ DANGEROUS — not recommended for git ops |
| Accepting Edits | File modifications only | Safe for code changes |
| Plan | Plans first, executes after approval | ✅ RECOMMENDED for git operations |
| Default | Requires permission for actions | ✅ SAFE |

**RECOMMENDATION**: Use **Plan mode** or **Default mode** for any git operations
to ensure compliance with rules before execution.

### How to Enforce Rules in IFLOW.md

Add the following to your project's `IFLOW.md`:

```markdown
# Git Rules — STRICTLY ENFORCED

## CRITICAL: Staging
- NEVER use `git add -A`, `git add .`, or `git add --all`
- ALWAYS stage individual files: `git add <file>`
- Verify with `git status` before committing

## Commits
- Conventional Commits format: <type>(<scope>): <description>
- Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- Imperative mood, lowercase start, no trailing period, max 72 chars

## Branches
- Create with type prefix: feat/, fix/, hotfix/, refactor/, docs/, ci/
- Kebab-case, max 50 characters
- Never commit to main directly

## PRs and Issues
- Use gh CLI with full templates and labels
- PR title follows Conventional Commits
```

### iFlow CLI Commands

```bash
# iFlow uses Shell tool — same as regular bash commands

git add src/auth/login.ts
git commit -m "feat(auth): add login endpoint"
gh pr create --title "feat(auth): add login" --body "..."
gh issue create --title "fix(api): error" --body "..." --label "type:bug,priority:P1"
```

### iFlow Custom Commands

Create `.iflow/commands/commit.toml` for enforced commit workflow:

```toml
description = "Create a Conventional Commit with proper staging"
prompt = """
Before committing:
1. Run `git status` to check staged files
2. If files were staged with `git add -A` or `git add .`, REJECT and re-stage individually
3. Analyze the diff to determine commit type (feat/fix/docs/etc.)
4. Generate a Conventional Commits message
5. Confirm with user before running git commit
NEVER use git add -A, git add ., or git add --all.
"""
```

---

## Quick Reference: Agent Context Files

To set up a new project for all agents, create these files:

```bash
# For Gemini CLI
echo "See git rules in managing-github-events skill" > GEMINI.md

# For Claude Code
echo "See git rules in managing-github-events skill" > CLAUDE.md

# For Amp
echo "See @~/.config/agents/skills/managing-github-events/SKILL.md" > AGENTS.md

# For iFlow CLI (or use /init command)
echo "See git rules in managing-github-events skill" > IFLOW.md
```

Each file SHOULD contain the full set of rules from the "How to Enforce Rules" sections above.
