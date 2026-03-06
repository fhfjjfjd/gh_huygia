# Branch Management Rules

## Naming Convention

Format: `<type>/<short-kebab-case-description>`

### Allowed Prefixes

| Prefix | Use Case | Example |
|--------|----------|---------|
| `feat/` | New features | `feat/oauth2-login` |
| `fix/` | Bug fixes | `fix/null-pointer-api` |
| `hotfix/` | Critical production fixes | `hotfix/auth-bypass` |
| `refactor/` | Code restructuring | `refactor/extract-utils` |
| `docs/` | Documentation changes | `docs/api-reference` |
| `ci/` | CI/CD pipeline changes | `ci/add-lint-workflow` |
| `release/` | Release preparation | `release/v1.2.0` |
| `experiment/` | Experimental/PoC work | `experiment/new-parser` |

### Rules

- Branch name MUST use kebab-case (lowercase, hyphens only)
- Branch name MUST NOT exceed 50 characters total
- Branch MUST be created from latest `main` (or default branch)
- Branch MUST be deleted after merge — no stale branches
- FORBIDDEN: working directly on `main`/`master`
- FORBIDDEN: force-pushing to `main`/`master`

### FORBIDDEN Branch Names

These names MUST NOT be used as branch names:
- `main`, `master` — protected default branches
- `develop`, `dev` — ambiguous
- `staging`, `production`, `prod` — environment names
- `temp`, `tmp` — meaningless
- `test`, `testing` — ambiguous
- `wip` — not descriptive
- `my-branch`, `branch1` — not descriptive
- Any name without a `type/` prefix

---

## Examples

### ✅ GOOD Examples

```bash
git checkout -b feat/oauth2-login
git checkout -b fix/null-pointer-user-api
git checkout -b hotfix/critical-auth-bypass
git checkout -b refactor/extract-validation
git checkout -b docs/add-api-reference
git checkout -b ci/add-test-workflow
git checkout -b release/v1.2.0
git checkout -b experiment/graphql-migration
git checkout -b feat/add-user-profile-page
git checkout -b fix/123-null-pointer-api       # with issue number
```

### ❌ BAD Examples

```bash
# No type prefix — REJECTED
git checkout -b oauth-login
# Why: Missing type/ prefix

# Underscore instead of hyphen — REJECTED
git checkout -b feat/oauth_login
# Why: Must use kebab-case (hyphens, not underscores)

# Uppercase — REJECTED
git checkout -b FEAT/OAuth-Login
# Why: Must be all lowercase

# Too long (>50 chars) — REJECTED
git checkout -b feat/add-the-new-oauth2-authentication-flow-with-google-provider
# Why: Exceeds 50 character limit

# Using forbidden name — REJECTED
git checkout -b develop
# Why: "develop" is a forbidden branch name

# WIP branch — REJECTED
git checkout -b wip
# Why: "wip" is forbidden and not descriptive

# Wrong prefix — REJECTED
git checkout -b feature/oauth-login
# Why: "feature/" is not valid. Use "feat/"

# Working on main — FORBIDDEN
git checkout main && git commit -m "feat: add login"
# Why: MUST NOT commit directly to main

# CamelCase — REJECTED
git checkout -b feat/oAuthLogin
# Why: Must use kebab-case
```

---

## Branch Lifecycle

```
1. Create:    git checkout -b feat/my-feature main
2. Work:      <make changes, commit following commit rules>
3. Push:      git push -u origin feat/my-feature
4. PR:        gh pr create --title "feat: my feature" --body "..."
5. Review:    <wait for review / self-review after 1h for solo projects>
6. Merge:     <squash merge via PR>
7. Delete:    git branch -d feat/my-feature && git push origin --delete feat/my-feature
```

### Cleanup Commands

```bash
# Delete local merged branches
git branch --merged main | grep -v "main" | xargs -r git branch -d

# Delete remote merged branch
git push origin --delete feat/my-feature

# Prune remote tracking branches
git fetch --prune
```
