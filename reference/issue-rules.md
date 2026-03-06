# Issue Management Rules

## Bug Report Template

Every bug report MUST include ALL of the following sections:

```markdown
## Bug Report

### Description
<Clear, specific description of the bug>

### Steps to Reproduce
1. <Exact step 1>
2. <Exact step 2>
3. <Exact step 3>

### Expected Behavior
<What SHOULD happen>

### Actual Behavior
<What ACTUALLY happens>

### Environment
- OS: <e.g., Android 13 / Termux>
- Runtime: <e.g., Node.js 20.x, Java 17>
- Project version: <e.g., v1.2.3>
- Browser (if applicable): <e.g., Chrome 120>

### Logs / Screenshots
<Paste relevant error logs, stack traces, or attach screenshots>
<For crashes or UI issues, screenshots are MANDATORY>

### Additional Context
<Any other information that might help>
```

## Feature Request Template

Every feature request MUST include ALL of the following sections:

```markdown
## Feature Request

### Description
<Clear description of the proposed feature>

### Motivation
<Why is this needed? What problem does it solve?>

### Proposed Solution
<How should this feature work? Include technical details if possible>

### Alternatives Considered
<What other approaches were considered and why were they rejected?>

### Acceptance Criteria
- [ ] <Specific, testable criterion 1>
- [ ] <Specific, testable criterion 2>
- [ ] <Specific, testable criterion 3>
```

---

## Label System

### Type Labels (REQUIRED — exactly one per issue)

| Label | Color | Description |
|-------|-------|-------------|
| `type:bug` | `#d73a4a` | Bug report |
| `type:feature` | `#0075ca` | Feature request |
| `type:docs` | `#0e8a16` | Documentation |
| `type:chore` | `#e4e669` | Maintenance task |
| `type:refactor` | `#d4c5f9` | Code restructuring |
| `type:question` | `#d876e3` | Question or discussion |

### Priority Labels (REQUIRED — exactly one per issue)

| Label | Color | Response Time | Description |
|-------|-------|---------------|-------------|
| `priority:P0` | `#b60205` | Immediate | Critical: system down, data loss, security breach |
| `priority:P1` | `#d93f0b` | Within 24h | High: major feature broken, significant impact |
| `priority:P2` | `#fbca04` | Within 1 week | Medium: non-critical bug, minor feature |
| `priority:P3` | `#0e8a16` | Next release | Low: cosmetic, nice-to-have |

### Status Labels (OPTIONAL but recommended)

| Label | Description |
|-------|-------------|
| `status:triage` | Needs triage/review |
| `status:confirmed` | Bug confirmed, ready for work |
| `status:in-progress` | Being worked on |
| `status:blocked` | Blocked by dependency |
| `status:wontfix` | Will not be fixed |
| `status:duplicate` | Duplicate of another issue |

---

## Rules

- Every issue MUST have at minimum ONE `type:*` label AND ONE `priority:*` label
- FORBIDDEN: title-only issues (body MUST follow the appropriate template)
- FORBIDDEN: issues without labels
- FORBIDDEN: duplicate issues without referencing the original (use `Duplicate of #N`)
- Issue titles SHOULD be descriptive and specific
- Issue titles MUST NOT be vague (e.g., "bug", "help", "error", "not working")

---

## Examples

### ✅ GOOD: Creating a bug issue with gh CLI

```bash
gh issue create \
  --title "fix(api): null pointer when fetching user with invalid ID" \
  --body "## Bug Report

### Description
The API returns a 500 error instead of 404 when fetching a user with an invalid UUID format.

### Steps to Reproduce
1. Send GET request to \`/api/users/not-a-uuid\`
2. Observe 500 Internal Server Error

### Expected Behavior
Should return 404 Not Found with error message.

### Actual Behavior
Returns 500 with stack trace containing NullPointerException.

### Environment
- OS: Ubuntu 22.04
- Runtime: Java 17
- Project version: v2.1.0

### Logs / Screenshots
\`\`\`
java.lang.NullPointerException: Cannot invoke method on null object
  at com.app.UserService.findById(UserService.java:42)
\`\`\`" \
  --label "type:bug,priority:P1"
```

### ✅ GOOD: Creating a feature request with gh CLI

```bash
gh issue create \
  --title "feat(auth): add two-factor authentication support" \
  --body "## Feature Request

### Description
Add TOTP-based two-factor authentication for user accounts.

### Motivation
Security requirement for production deployment. Users need additional account protection.

### Proposed Solution
Implement TOTP using a library like \`speakeasy\`. Add QR code generation for authenticator apps.

### Alternatives Considered
- SMS-based 2FA: rejected due to SIM swap vulnerability
- Email-based 2FA: rejected due to email account compromise risk

### Acceptance Criteria
- [ ] User can enable 2FA from settings page
- [ ] QR code is generated for authenticator app setup
- [ ] Login requires TOTP code when 2FA is enabled
- [ ] Backup codes are generated (10 single-use codes)
- [ ] User can disable 2FA with password confirmation" \
  --label "type:feature,priority:P2"
```

### ❌ BAD Examples

```bash
# Title-only issue — REJECTED
gh issue create --title "fix login bug"
# Why: No body, no template, no labels

# No labels — REJECTED
gh issue create --title "Add dark mode" --body "We need dark mode"
# Why: Missing type and priority labels. Body doesn't follow template.

# Vague title — REJECTED
gh issue create --title "not working" --body "The app crashes"
# Why: Title is vague. Body doesn't follow template.

# Duplicate without reference — REJECTED
gh issue create --title "Login is broken" --body "Login doesn't work"
# Why: If duplicate, must reference original with "Duplicate of #N"
```

---

## Creating Labels with gh CLI

```bash
# Type labels
gh label create "type:bug" --color "d73a4a" --description "Bug report"
gh label create "type:feature" --color "0075ca" --description "Feature request"
gh label create "type:docs" --color "0e8a16" --description "Documentation"
gh label create "type:chore" --color "e4e669" --description "Maintenance task"
gh label create "type:refactor" --color "d4c5f9" --description "Code restructuring"

# Priority labels
gh label create "priority:P0" --color "b60205" --description "Critical: immediate action"
gh label create "priority:P1" --color "d93f0b" --description "High: within 24h"
gh label create "priority:P2" --color "fbca04" --description "Medium: within 1 week"
gh label create "priority:P3" --color "0e8a16" --description "Low: next release"

# Status labels
gh label create "status:triage" --color "ededed" --description "Needs triage"
gh label create "status:confirmed" --color "0e8a16" --description "Confirmed, ready for work"
gh label create "status:in-progress" --color "fbca04" --description "Being worked on"
gh label create "status:blocked" --color "d73a4a" --description "Blocked by dependency"
```
