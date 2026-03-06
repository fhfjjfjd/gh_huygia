# Changelog Rules — Keep a Changelog Format

## Rules

- File MUST be named `CHANGELOG.md` and placed in project root
- MUST maintain an `[Unreleased]` section at the top for upcoming changes
- Categories MUST appear in this order: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
- Only include categories that have entries (do not include empty categories)
- Date format MUST be ISO 8601: `YYYY-MM-DD`
- Versions MUST be listed in reverse chronological order (newest first)
- Each version MUST have a comparison URL at the bottom of the file
- Entries MUST be human-readable — NOT auto-generated git log dumps
- Each entry SHOULD start with a verb in past tense describing what changed
- FORBIDDEN: dumping `git log --oneline` as a changelog

---

## Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- <new features go here as they are merged>

## [1.1.0] - 2026-03-05

### Added
- OAuth2 login flow with Google and GitHub providers (#42)
- User profile page with avatar upload (#45)

### Fixed
- Null pointer exception when fetching user with invalid ID (#38)
- Session timeout not being refreshed on activity (#40)

### Security
- Updated dependency `jsonwebtoken` to fix CVE-2026-XXXXX

## [1.0.0] - 2026-02-01

### Added
- Initial release with user authentication
- REST API for user management
- Basic web UI with dashboard

[Unreleased]: https://github.com/user/repo/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

---

## Category Definitions

| Category | What Belongs Here |
|----------|-------------------|
| `Added` | New features, new endpoints, new capabilities |
| `Changed` | Changes to existing functionality, behavior changes |
| `Deprecated` | Features marked for removal in future versions |
| `Removed` | Features removed in this release |
| `Fixed` | Bug fixes |
| `Security` | Vulnerability fixes, security-related changes |

---

## Examples

### ✅ GOOD Entries

```markdown
### Added
- OAuth2 login flow with Google and GitHub providers (#42)
- Rate limiting middleware for API endpoints (#50)
- Dark mode support for web UI (#55)

### Changed
- Migrated database from SQLite to PostgreSQL (#48)
- Improved error messages for validation failures (#51)

### Deprecated
- Legacy XML API endpoints (will be removed in v3.0.0) (#53)

### Removed
- Support for Node.js 16 (EOL) (#47)
- Unused `legacy-auth` module (#49)

### Fixed
- Race condition in concurrent session handling (#38)
- Memory leak in WebSocket connection pool (#41)
- Incorrect timezone conversion for UTC+13 (#44)

### Security
- Updated `jsonwebtoken` to 9.0.3 to fix CVE-2026-XXXXX (#52)
- Added CSRF protection to all form endpoints (#54)
```

### ❌ BAD Entries

```markdown
# BAD: git log dump — REJECTED
- a1b2c3d fix stuff
- d4e5f6g update
- g7h8i9j WIP
- j0k1l2m misc

# BAD: vague entries — REJECTED
- Fixed bug
- Updated code
- Various improvements
- Minor changes

# BAD: wrong date format — REJECTED
## [1.0.0] - March 5, 2026
## [1.0.0] - 05/03/2026
## [1.0.0] - 2026/03/05

# BAD: oldest first — REJECTED
## [1.0.0] - 2026-01-01
## [1.1.0] - 2026-02-01
## [1.2.0] - 2026-03-01
# Why: Must be newest first (reverse chronological)

# BAD: no comparison URLs — REJECTED
## [1.1.0] - 2026-03-05
# Why: Must include comparison URL at bottom of file

# BAD: missing [Unreleased] section — REJECTED
## [1.1.0] - 2026-03-05
# Why: [Unreleased] section must always exist at top
```

---

## Workflow: Updating Changelog

1. When merging a PR, add an entry to the `[Unreleased]` section
2. When releasing a new version:
   - Rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`
   - Create a new empty `[Unreleased]` section above it
   - Add comparison URL for the new version at the bottom
   - Update the `[Unreleased]` comparison URL
