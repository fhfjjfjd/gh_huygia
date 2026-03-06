---
name: managing-github-events
description: "Enforces strict GitHub event management rules across all projects. Covers commits (Conventional Commits v1.0.0), branches, issues, PRs, releases (SemVer 2.0.0), changelog (Keep a Changelog), security (SECURITY.md), CI/CD, repository hygiene (including avoiding redundant prefixes like 'gh_'), and AI agent compliance (OpenAI Codex, Qwen Code, Amp, Claude Code, Gemini CLI, iFlow CLI). Use when performing any git operation, creating commits, branches, PRs, issues, releases, changelogs, or managing GitHub repositories."
allowed-tools:
  - Bash
  - Read
  - Grep
  - edit_file
  - create_file
  - glob
  - finder
  - web_search
---

# Managing GitHub Events — Strict Ruleset

> **RFC 2119 Compliance**: The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
> "SHOULD", "SHOULD NOT", "FORBIDDEN", "REJECTED" in this document are to be interpreted as
> described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

This skill enforces **non-negotiable** rules for ALL GitHub event management across ANY project.
Violations are REJECTED. No exceptions.

---

## 1. Commit Messages (Conventional Commits v1.0.0)

See @reference/commit-rules.md for full specification, examples, and edge cases.

### Core Rules

- Format: `<type>[optional scope]: <description>` — this is REQUIRED
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- Description MUST use imperative mood ("add" not "added", "fix" not "fixed")
- First line MUST NOT exceed 72 characters
- Description MUST NOT start with uppercase letter
- Description MUST NOT end with a period
- Breaking changes MUST use `!` after type/scope AND/OR `BREAKING CHANGE:` footer
- Each commit MUST be atomic — one logical change per commit
- FORBIDDEN: `git add -A`, `git add .`, `git add --all` — MUST stage specific files only

### Quick Reference

```
✅ feat(auth): add OAuth2 login flow
✅ fix(api): resolve null pointer in user endpoint
✅ feat(api)!: change response format to JSON:API
❌ "fixed stuff"
❌ "WIP"
❌ "update"
❌ "misc changes"
❌ "feat: Add OAuth2 login flow."  (uppercase + period)
```

---

## 2. Branch Management

See @reference/branch-rules.md for full specification and examples.

### Core Rules

- Format: `<type>/<short-kebab-case-description>` — REQUIRED
- Allowed prefixes: `feat/`, `fix/`, `hotfix/`, `refactor/`, `docs/`, `ci/`, `release/`, `experiment/`
- Branch name MUST use kebab-case, MUST NOT exceed 50 characters
- Branches MUST be deleted after merge
- FORBIDDEN names: `main`, `master`, `develop`, `staging`, `production`, `temp`, `test`, `wip`

### Quick Reference

```
✅ feat/oauth2-login
✅ fix/null-pointer-user-api
✅ hotfix/critical-auth-bypass
❌ feature_oauth    (underscore, wrong prefix)
❌ my-branch        (no type prefix)
❌ FEAT/OAuth       (uppercase)
```

---

## 3. Issue Management

See @reference/issue-rules.md for full specification, templates, and label system.

### Core Rules

- Bug reports MUST include: description, steps to reproduce, expected vs actual, environment, logs
- Feature requests MUST include: description, motivation, proposed solution, acceptance criteria
- Every issue MUST have at minimum: one `type:*` label AND one `priority:*` label
- FORBIDDEN: title-only issues, issues without labels, duplicate issues without referencing original
- Priority labels: `P0` (critical), `P1` (high), `P2` (medium), `P3` (low)

---

## 4. Pull Request Rules

See @reference/pr-rules.md for full specification, templates, and merge strategies.

### Core Rules

- PR title MUST follow Conventional Commits format
- PR body MUST include: summary, changes list, related issues, testing, checklist
- Squash merge for feature branches — REQUIRED
- MUST NOT merge with failing CI — NO EXCEPTIONS
- Branch MUST be deleted after merge
- Solo projects: self-review after minimum 1 hour cooling period — REQUIRED
- Every PR MUST reference at least one issue (use `Closes #N` or `Relates to #N`)

### Quick Reference

```
✅ Title: "feat(auth): add OAuth2 login flow"
✅ Body: includes Summary, Changes, Related Issues, Testing, Checklist
❌ Title: "Fix bug"
❌ Body: empty or "please review"
❌ Merging with red CI checks
```

---

## 5. Release Management (SemVer 2.0.0)

See @reference/release-rules.md for full specification, precedence rules, and examples.

### Core Rules

- Version format: `MAJOR.MINOR.PATCH` (X.Y.Z) — no leading zeroes
- MAJOR: incompatible API changes — MUST increment on breaking changes
- MINOR: backward-compatible new functionality — MUST reset PATCH to 0
- PATCH: backward-compatible bug fixes — MUST NOT add new features
- Pre-release: `alpha` < `beta` < `rc` (e.g., `1.0.0-alpha.1`, `1.0.0-rc.1`)
- Build metadata: appended with `+` (e.g., `1.0.0+20260305`) — ignored for precedence
- Git tags MUST be annotated: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- Tags MUST follow format `v{MAJOR}.{MINOR}.{PATCH}`
- FORBIDDEN: deleting tags, moving tags, non-annotated tags

---

## 6. Changelog (Keep a Changelog)

See @reference/changelog-rules.md for full specification and examples.

### Core Rules

- File: `CHANGELOG.md` in project root — REQUIRED
- Categories (in this order): `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
- MUST maintain `[Unreleased]` section at top
- Date format: ISO 8601 (`YYYY-MM-DD`) — REQUIRED
- Order: reverse chronological (newest first)
- MUST include comparison URLs at bottom of file
- FORBIDDEN: git log dumps, auto-generated changelogs without human curation

---

## 7. Security

See @reference/security-rules.md for full specification, SECURITY.md template, and response timelines.

### Core Rules

- `SECURITY.md` MUST exist in every project root — NO EXCEPTIONS
- Vulnerability reporting MUST use private channel (NOT public issues)
- Response timeline: Critical 24-48h, High 7d, Medium 30d, Low next release
- ZERO TOLERANCE: committed secrets, API keys, tokens, `.env` files, private keys
- Supported versions table MUST be maintained in SECURITY.md

---

## 8. CI/CD Rules

See @reference/cicd-rules.md for full specification and examples.

### Core Rules

- Third-party GitHub Actions MUST be pinned to full commit SHA — NOT tags/branches
- Workflow files MUST include explicit `permissions` block (least privilege)
- MUST NOT merge with failing CI — NO EXCEPTIONS
- Dependencies MUST be cached
- All jobs MUST have timeout set
- Workflow files: `kebab-case.yml` in `.github/workflows/`

### Quick Reference

```
✅ uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29  # v4.1.6
❌ uses: actions/checkout@v4
❌ uses: actions/checkout@main
```

---

## 9. Repository Hygiene

See all files in @reference/ directory for full specification, naming conventions, and rules.

### Core Rules

- `.gitignore` MUST exist — MUST cover: OS files, IDE configs, build artifacts, dependencies, `.env`
- `README.md` MUST exist — MUST include: project name, description, setup, usage, license
- `LICENSE` file MUST exist in project root
- Project names SHOULD avoid redundant prefixes like 'gh_' when the context is already clear
- FORBIDDEN: binary blobs in git (images >100KB, compiled binaries, archives)
- FORBIDDEN: committed `node_modules/`, `vendor/`, `__pycache__/`, `.venv/`, build outputs

---

## 10. AI Coding Agent Compliance

See @reference/ai-agent-rules.md for detailed per-agent instructions.

ALL AI coding agents MUST comply with every rule in this document. Below is a summary;
the reference file contains full instructions for each agent.

### Universal Rules (ALL Agents)

1. **Staging**: MUST use `git add <specific-file>` — FORBIDDEN: `git add -A`, `git add .`
2. **Commits**: MUST follow Conventional Commits format exactly
3. **Branches**: MUST create branches with correct `type/` prefix before starting work
4. **PRs**: MUST use `gh pr create --title "<conventional>" --body "<full template>"`
5. **Issues**: MUST use `gh issue create` with full template body and labels

### Agent-Specific Context Files

| Agent | Context File | Location |
|-------|-------------|----------|
| OpenAI Codex | `CODEX.md` | Project root |
| Qwen Code | `QWEN.md` | Project root |
| Amp (ampcode) | `AGENTS.md` | Project root |
| Claude Code | `CLAUDE.md` | Project root |
| Gemini CLI | `GEMINI.md` | Project root |
| iFlow CLI | `IFLOW.md` | Project root |

Each agent's context file SHOULD include a reference to this skill's rules. This skill is designed to be used across multiple AI CLI platforms.

### Per-Agent Summary

**OpenAI Codex**: Cloud-based software engineering agent that can perform multiple tasks in parallel. Supports writing features, answering questions about codebases, fixing bugs, and proposing changes for review. Each task runs in a separate sandboxed cloud environment with your repository pre-loaded. Available for ChatGPT Pro, Team, and Enterprise users. Can be guided by AGENTS.md files in your repository to understand how to navigate your codebase. Also includes a CLI version (Codex CLI) that runs locally on your computer, giving AI models direct access to your system's core tools and enabling terminal-based coding workflows.

**Qwen Code**: AI-powered command-line workflow tool adapted from Gemini CLI. Specialized for understanding codebases, generating new code, and solving complex algorithmic challenges using chain-of-thought prompting. Offers enhanced parsing and workflow support tailored to Qwen-Coder capabilities.

**Amp (ampcode)**: Uses Bash tool for git/gh commands. Features agentic code review, clickable diagrams, fast search subagents. Uses AGENTS.md + Skills system. This very skill enforces compliance. Permission system controls tool access.

**Claude Code**: Has built-in git integration. Uses CLAUDE.md for instructions. Has permission tiers (read-only/edit/shell). Custom slash commands can enforce workflows.

**Gemini CLI**: Uses Shell tool for git/gh commands. ⚠️ Default behavior may use `git add .` — MUST be explicitly instructed NOT to. Use GEMINI.md to enforce rules.

**iFlow CLI**: Uses Shell tool for git/gh commands. Uses IFLOW.md for instructions. Has 4 modes (YOLO/Accepting Edits/Plan/Default). SubAgent system available.

---

## Environment Context

- **Platform**: Various (including Termux on Android)
- **GitHub CLI**: `gh` authenticated with appropriate GitHub account
- **Author**: Created by Gia Huy for multiple AI CLI platforms
- **Git config**: Ensure `user.name` and `user.email` are set before any commit

---

## Scripts

### Bash Scripts
- Run `scripts/validate-commit-msg.sh "feat(auth): add login"` to validate a commit message
- Run `scripts/validate-branch-name.sh "feat/oauth2-login"` to validate a branch name
- Both scripts also work without arguments (validate current branch / last commit)

### Python Scripts (no API, no LLM — pure local logic)
- Run `python3 scripts/setup-repo.py` to initialize a repo with all mandatory files + GitHub labels
- Run `python3 scripts/audit-repo.py` to audit a repo for full compliance (files, commits, branches, secrets, changelog)
- Run `python3 scripts/audit-repo.py --commits 20` to check last 20 commits

---

## Enforcement

Violations of any MUST/MUST NOT/REQUIRED/FORBIDDEN rule in this document SHALL result in:
1. Immediate rejection of the commit/PR/release
2. Required correction before proceeding
3. No workarounds, no exceptions, no "just this once"
