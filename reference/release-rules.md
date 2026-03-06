# Release Management — SemVer 2.0.0

## Version Format

`MAJOR.MINOR.PATCH` (X.Y.Z)

### Increment Rules

| Component | When to Increment | Reset |
|-----------|-------------------|-------|
| MAJOR (X) | Incompatible API changes (breaking) | Resets MINOR and PATCH to 0 |
| MINOR (Y) | Backward-compatible new functionality | Resets PATCH to 0 |
| PATCH (Z) | Backward-compatible bug fixes | Nothing reset |

### Strict Rules

- Version numbers MUST be non-negative integers
- MUST NOT contain leading zeroes: `1.02.3` is FORBIDDEN
- Once released, version contents MUST NOT be modified — release new version instead
- Version `0.y.z` is for initial development — anything MAY change at any time
- Version `1.0.0` defines the public API — all rules apply from this point

### Pre-release Versions

Format: `X.Y.Z-<pre-release>`

Precedence order (lowest to highest):
1. `alpha` — early testing, unstable
2. `beta` — feature-complete, may have bugs
3. `rc` (release candidate) — ready for release unless critical bugs found

Examples:
```
1.0.0-alpha.1
1.0.0-alpha.2
1.0.0-beta.1
1.0.0-beta.2
1.0.0-rc.1
1.0.0-rc.2
1.0.0          ← final release
```

Pre-release rules:
- Pre-release version has LOWER precedence than normal version
- `1.0.0-alpha.1` < `1.0.0`
- Dot-separated identifiers: numeric compare numerically, alphanumeric compare lexically
- `1.0.0-alpha` < `1.0.0-alpha.1` < `1.0.0-beta` < `1.0.0-rc.1` < `1.0.0`

### Build Metadata

Format: `X.Y.Z+<build>`

- Appended with `+` sign
- MUST be ignored for version precedence
- `1.0.0+20260305` = `1.0.0+build.123` (same precedence)
- Use for build timestamps, CI build numbers, etc.

---

## Git Tags

### Rules

- Tags MUST be annotated: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- Tag format MUST be `v{MAJOR}.{MINOR}.{PATCH}` (with `v` prefix)
- FORBIDDEN: lightweight tags (non-annotated)
- FORBIDDEN: deleting published tags
- FORBIDDEN: moving/rewriting tags
- Tags MUST point to a merge commit on `main` (or default branch)

### Creating a Release

```bash
# 1. Ensure on main and up to date
git checkout main
git pull origin main

# 2. Create annotated tag
git tag -a v1.2.0 -m "Release v1.2.0: add OAuth2 support

Changes:
- feat(auth): add OAuth2 login flow
- fix(api): resolve null pointer in user endpoint
- docs: update API reference"

# 3. Push tag
git push origin v1.2.0

# 4. Create GitHub release
gh release create v1.2.0 \
  --title "v1.2.0" \
  --notes "## Changes
- feat(auth): add OAuth2 login flow
- fix(api): resolve null pointer in user endpoint
- docs: update API reference"
```

---

## Examples

### ✅ GOOD Examples

```bash
# Annotated tag with message
git tag -a v1.0.0 -m "Release v1.0.0: initial stable release"

# Pre-release tag
git tag -a v2.0.0-alpha.1 -m "Release v2.0.0-alpha.1: early preview"

# Patch release
git tag -a v1.2.1 -m "Release v1.2.1: fix authentication bug"

# Minor release
git tag -a v1.3.0 -m "Release v1.3.0: add user profile feature"

# Major release (breaking changes)
git tag -a v2.0.0 -m "Release v2.0.0: migrate to new API format

BREAKING CHANGE: v1 API endpoints removed"

# GitHub release with gh CLI
gh release create v1.2.0 --title "v1.2.0" --notes "Release notes here"
```

### ❌ BAD Examples

```bash
# Lightweight tag — REJECTED
git tag v1.0.0
# Why: Must be annotated with -a flag and -m message

# No v prefix — REJECTED
git tag -a 1.0.0 -m "Release 1.0.0"
# Why: Tag must start with "v" prefix

# Leading zero — REJECTED
git tag -a v1.02.0 -m "Release"
# Why: Leading zeroes are forbidden (02 should be 2)

# Deleting a tag — FORBIDDEN
git tag -d v1.0.0 && git push origin :refs/tags/v1.0.0
# Why: Published tags MUST NOT be deleted

# Moving a tag — FORBIDDEN
git tag -f v1.0.0 HEAD && git push --force origin v1.0.0
# Why: Tags MUST NOT be moved/rewritten

# Invalid pre-release — REJECTED
git tag -a v1.0.0-SNAPSHOT -m "Snapshot"
# Why: Use alpha/beta/rc, not SNAPSHOT

# Tagging without being on main — REJECTED
git checkout feat/my-feature
git tag -a v1.0.0 -m "Release"
# Why: Tags must point to commits on main/default branch
```

---

## Version Decision Tree

```
Did you make incompatible API changes?
├── YES → Bump MAJOR (reset MINOR and PATCH to 0)
└── NO
    ├── Did you add backward-compatible functionality?
    │   ├── YES → Bump MINOR (reset PATCH to 0)
    │   └── NO
    │       ├── Did you make backward-compatible bug fixes?
    │       │   ├── YES → Bump PATCH
    │       │   └── NO → No version bump needed
    └── Is this a pre-release?
        └── YES → Append -alpha.N / -beta.N / -rc.N
```
