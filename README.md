# Managing GitHub Events — Strict Ruleset

A **strict GitHub event management ruleset** enforcing non-negotiable standards for commits, branches, issues, PRs, releases, changelogs, security, CI/CD, and repository hygiene across all projects.

## 📋 Overview

This comprehensive skill ensures consistent, professional GitHub workflows by enforcing:

- ✅ **Conventional Commits v1.0.0** for all commit messages
- ✅ **Semantic Versioning (SemVer 2.0.0)** for releases
- ✅ **Keep a Changelog** format for changelogs
- ✅ **Strict branch naming** with type prefixes
- ✅ **Professional PR & issue management**
- ✅ **Security best practices** (SECURITY.md, secret scanning)
- ✅ **CI/CD standards** (pinned actions, permissions, timeouts)
- ✅ **Repository hygiene** (mandatory files, .gitignore, LICENSE, avoiding redundant prefixes)
- ✅ **AI agent compliance** (OpenAI Codex, Qwen Code, Amp, Claude Code, Gemini CLI, iFlow CLI)

**Violations are REJECTED. No exceptions.** — RFC 2119 compliance.

---

## 🚀 Quick Start

### 1. Using This Skill in iFlow CLI

This skill is designed to be used with iFlow CLI for managing GitHub events. To use this skill:

1. Ensure you have iFlow CLI installed and configured
2. Reference this skill when performing GitHub operations
3. Follow the rules defined in this skill for all GitHub events

### 2. Enforce Rules During Development

Use this skill when:
- Creating commit messages (follow Conventional Commits)
- Managing branches (use proper naming)
- Creating pull requests and issues
- Managing releases and changelogs
- Setting up repository hygiene
- Working with AI agents

---

## 📚 Rules at a Glance

### Commit Messages (Conventional Commits v1.0.0)

**Format**: `<type>[optional scope]: <description>`

**Allowed types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Examples**:
```
✅ feat(auth): add OAuth2 login flow
✅ fix(api): resolve null pointer in user endpoint
✅ feat(api)!: change response format to JSON:API
❌ "fixed stuff"
❌ "feat: Add OAuth2 login flow."  (uppercase + period)
```

**Rules**:
- Use imperative mood ("add" not "added")
- Max 72 characters on first line
- No uppercase first letter, no period at end
- Breaking changes use `!` after type/scope
- Each commit = one logical change (atomic)
- **FORBIDDEN**: `git add -A`, `git add .`, `git add --all`

→ Full spec: `reference/commit-rules.md`

---

### Branch Management

**Format**: `<type>/<short-kebab-case-description>`

**Allowed prefixes**: `feat/`, `fix/`, `hotfix/`, `refactor/`, `docs/`, `ci/`, `release/`, `experiment/`

**Examples**:
```
✅ feat/oauth2-login
✅ fix/null-pointer-user-api
✅ hotfix/critical-auth-bypass
❌ feature_oauth    (underscore, wrong prefix)
❌ my-branch        (no type prefix)
```

**Rules**:
- Must use kebab-case
- Max 50 characters
- Delete after merge
- **FORBIDDEN**: `main`, `master`, `develop`, `staging`, `production`, `temp`, `test`, `wip`

→ Full spec: `reference/branch-rules.md`

---

### Pull Requests

**Rules**:
- Title MUST follow Conventional Commits format
- Body MUST include: summary, changes list, related issues, testing, checklist
- Squash merge for feature branches (REQUIRED)
- **MUST NOT merge with failing CI** — NO EXCEPTIONS
- Delete branch after merge
- Self-review after 1-hour cooling period (solo projects)
- MUST reference at least one issue (`Closes #N` or `Relates to #N`)

→ Full spec: `reference/pr-rules.md`

---

### Issues

**Rules**:
- Bug reports MUST include: description, steps to reproduce, expected vs actual, environment, logs
- Feature requests MUST include: description, motivation, proposed solution, acceptance criteria
- MUST have ≥1 `type:*` label AND ≥1 `priority:*` label
- Priority: `P0` (critical), `P1` (high), `P2` (medium), `P3` (low)
- **FORBIDDEN**: title-only issues, unlabeled issues

→ Full spec: `reference/issue-rules.md`

---

### Release Management (SemVer 2.0.0)

**Format**: `MAJOR.MINOR.PATCH` (e.g., `v1.2.3`)

**Rules**:
- MAJOR: breaking API changes
- MINOR: backward-compatible new features (resets PATCH to 0)
- PATCH: backward-compatible bug fixes only
- Pre-release: `1.0.0-alpha.1`, `1.0.0-beta.2`, `1.0.0-rc.1`
- Tags MUST be annotated: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- **FORBIDDEN**: deleting/moving tags, non-annotated tags

→ Full spec: `reference/release-rules.md`

---

### Changelog (Keep a Changelog)

**File**: `CHANGELOG.md` in project root (REQUIRED)

**Format**:
- Categories (in order): Added, Changed, Deprecated, Removed, Fixed, Security
- Maintain `[Unreleased]` section at top
- Date format: ISO 8601 (`YYYY-MM-DD`)
- Order: reverse chronological (newest first)
- Include comparison URLs at bottom
- **FORBIDDEN**: git log dumps, auto-generated without curation

→ Full spec: `reference/changelog-rules.md`

---

### Security

**Rules**:
- `SECURITY.md` MUST exist in project root — NO EXCEPTIONS
- Vulnerability reporting via private channel (NOT public issues)
- Response timelines:
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 30 days
  - Low: next release
- **ZERO TOLERANCE** for committed secrets, API keys, `.env` files, private keys
- Maintain supported versions table in SECURITY.md

→ Full spec: `reference/security-rules.md`

---

### CI/CD

**Rules**:
- Third-party GitHub Actions MUST be pinned to full commit SHA (NOT tags/branches)
- Workflow files MUST include explicit `permissions` block (least privilege)
- **MUST NOT merge with failing CI** — NO EXCEPTIONS
- Dependencies MUST be cached
- All jobs MUST have timeout set
- Workflow files: `kebab-case.yml` in `.github/workflows/`

**Example**:
```yaml
✅ uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29  # v4.1.6
❌ uses: actions/checkout@v4
❌ uses: actions/checkout@main
```

→ Full spec: `reference/cicd-rules.md`

---

### Repository Hygiene

**Rules**:
- `.gitignore` MUST exist and cover: OS files, IDE configs, build artifacts, dependencies, `.env`
- `README.md` MUST exist (project name, description, setup, usage, license)
- `LICENSE` file MUST exist in project root
- `CHANGELOG.md` file MUST exist in project root
- `SECURITY.md` file MUST exist in project root
- Project names SHOULD avoid redundant prefixes like 'gh_' when the context is already clear
- **FORBIDDEN**: binary blobs (images >100KB, compiled binaries, archives)
- **FORBIDDEN**: committed `node_modules/`, `vendor/`, `__pycache__/`, `.venv/`, build outputs

→ Full spec: `reference/repo-hygiene-rules.md` and `reference/no-gh-prefix-rules.md`

---

## 🤖 AI Agent Compliance

This skill is designed for use with multiple AI CLI platforms to ensure consistent, professional GitHub workflows. When using any of these platforms, this skill will enforce all the rules defined below.

**Universal Rules for AI Agents**:
1. MUST use `git add <specific-file>` — FORBIDDEN: `git add -A`, `git add .`
2. MUST follow Conventional Commits exactly
3. MUST create branches with correct `type/` prefix before work
4. MUST use `gh pr create --title "<conventional>" --body "<template>"`
5. MUST use `gh issue create` with full template body and labels

→ Full spec: `reference/ai-agent-rules.md`

---

## 🔍 Full References

Complete specifications for each section:

- `reference/commit-rules.md` — Conventional Commits details, edge cases
- `reference/branch-rules.md` — Branch naming spec, examples
- `reference/issue-rules.md` — Templates, label system
- `reference/pr-rules.md` — Templates, merge strategies
- `reference/release-rules.md` — SemVer details, precedence rules
- `reference/changelog-rules.md` — Format, examples
- `reference/security-rules.md` — SECURITY.md template, response timelines
- `reference/cicd-rules.md` — Workflow examples
- `reference/repo-hygiene-rules.md` — Checklists
- `reference/no-gh-prefix-rules.md` — Guidelines for avoiding redundant prefixes
- `reference/ai-agent-rules.md` — Per-agent instructions

---

## 🌍 Environment

This skill is designed to work with iFlow CLI in various environments:
- Can be used on any platform that supports iFlow CLI
- Requires GitHub CLI for some operations
- Works with standard git configurations

Before using this skill, ensure git config is set:
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## ⚖️ Enforcement

**Violations of ANY MUST/MUST NOT/REQUIRED/FORBIDDEN rule SHALL result in:**

1. ❌ Immediate rejection of commit/PR/release
2. ✅ Required correction before proceeding
3. 🚫 No workarounds, no exceptions, no "just this once"

---

## 📖 RFC 2119 Compliance

The key words **"MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "FORBIDDEN", "REJECTED"** in this document are interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

---

## 📄 Usage Rights

This skill is created by Gia Huy for multiple AI CLI platforms including OpenAI Codex (with CLI version), Qwen Code, Amp, Claude Code, Gemini CLI, and iFlow CLI. When using this skill in any of these platforms, you agree to follow the rules and guidelines defined herein.