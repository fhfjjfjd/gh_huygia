# Pull Request Rules

## PR Title

- MUST follow Conventional Commits format: `<type>(<scope>): <description>`
- Same rules as commit messages: imperative mood, no uppercase start, no period, ≤72 chars

## PR Body Template

Every PR body MUST include ALL of the following sections:

```markdown
## Summary
<Brief description of what this PR does and why>

## Changes
- <Specific change 1>
- <Specific change 2>
- <Specific change 3>

## Related Issues
Closes #<issue-number>
<!-- or: Relates to #<issue-number> -->

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] All existing tests pass
<Describe how to test the changes>

## Checklist
- [ ] Code follows project conventions
- [ ] Commit messages follow Conventional Commits
- [ ] Documentation updated (if applicable)
- [ ] No secrets/keys/tokens committed
- [ ] Branch is up to date with main
- [ ] CI passes
```

---

## Merge Strategy

| Branch Type | Merge Strategy | Reason |
|-------------|---------------|--------|
| `feat/*` | Squash merge | Clean history, one commit per feature |
| `fix/*` | Squash merge | Clean history, one commit per fix |
| `hotfix/*` | Squash merge | Clean history |
| `release/*` | Merge commit | Preserve release branch history |
| `refactor/*` | Squash merge | Clean history |
| `docs/*` | Squash merge | Clean history |

---

## Solo Project Self-Review

For solo projects (no other reviewers available):
- MUST wait minimum 1 hour after creating PR before merging
- MUST re-read all changes with fresh eyes after the cooling period
- MUST verify CI passes
- MUST check the diff one final time before merge

---

## Examples

### ✅ GOOD: Creating a PR with gh CLI

```bash
gh pr create \
  --title "feat(auth): add OAuth2 login flow" \
  --body "## Summary
Add OAuth2 authentication using Google and GitHub providers.

## Changes
- Add OAuth2 client configuration
- Implement login redirect flow
- Add callback handler for token exchange
- Store tokens securely in session

## Related Issues
Closes #42

## Testing
- [ ] Unit tests added for OAuth client
- [ ] Manual testing: login with Google account
- [ ] Manual testing: login with GitHub account
- [ ] All existing tests pass

## Checklist
- [x] Code follows project conventions
- [x] Commit messages follow Conventional Commits
- [x] Documentation updated
- [x] No secrets/keys/tokens committed
- [x] Branch is up to date with main
- [x] CI passes" \
  --base main \
  --head feat/oauth2-login
```

### ✅ GOOD: Squash merge via gh CLI

```bash
gh pr merge <PR-NUMBER> --squash --delete-branch
```

### ❌ BAD Examples

```bash
# Vague title — REJECTED
gh pr create --title "Fix bug" --body ""
# Why: Title doesn't follow Conventional Commits. Body is empty.

# No body — REJECTED
gh pr create --title "feat: add login"
# Why: Body is required with all template sections.

# "please review" body — REJECTED
gh pr create --title "feat(auth): add login" --body "please review"
# Why: Body must follow the template (Summary, Changes, etc.)

# Merging with failing CI — FORBIDDEN
gh pr merge 42 --squash  # while CI is red
# Why: MUST NOT merge with failing CI. No exceptions.

# Regular merge for feature branch — REJECTED
gh pr merge 42 --merge --delete-branch
# Why: Feature branches MUST use squash merge, not regular merge.

# Not deleting branch after merge — REJECTED
gh pr merge 42 --squash
# Why: Missing --delete-branch. Branch must be deleted after merge.

# No issue reference — REJECTED
gh pr create --title "feat: add login" --body "## Summary\nAdd login\n## Changes\n..."
# Why: Missing "Related Issues" section. Must reference at least one issue.
```

---

## PR Review Checklist

When reviewing a PR, verify:

1. **Title**: Follows Conventional Commits format
2. **Body**: All template sections present and filled
3. **CI**: All checks pass (green)
4. **Changes**: Match the described scope (no unrelated changes)
5. **Commits**: Follow Conventional Commits (will be squashed anyway)
6. **Security**: No secrets, keys, tokens in diff
7. **Tests**: New/changed code has test coverage
8. **Docs**: Updated if behavior changed
9. **Issue**: Referenced and will be closed by merge
