# CI/CD Rules

## GitHub Actions — Strict Rules

### Action Pinning

- Third-party actions MUST be pinned to full-length commit SHA — NOT tags or branches
- First-party GitHub actions (`actions/*`) SHOULD also be pinned to SHA
- MUST include a comment with the version number for readability

### Permissions Block

- Every workflow MUST include an explicit `permissions` block
- Follow principle of least privilege — only grant what is needed
- Use `permissions: {}` at top level to deny all, then grant per-job

### CI Must Pass

- MUST NOT merge any PR with failing CI — NO EXCEPTIONS
- CI failures MUST be investigated and fixed, not ignored or retried blindly

### Caching

- Dependencies MUST be cached to speed up workflows
- Use `actions/cache` or built-in caching (e.g., `actions/setup-node` with cache)

### Timeouts

- Every job MUST have `timeout-minutes` set
- Default suggestion: 15 minutes for most jobs, 30 for heavy builds

### Workflow Naming

- Workflow files MUST use kebab-case: `ci-test.yml`, `deploy-staging.yml`
- Workflow files MUST be in `.github/workflows/` directory

---

## Examples

### ✅ GOOD: Properly configured workflow

```yaml
name: ci-test

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout
        uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29  # v4.1.6

      - name: Setup Node.js
        uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8  # v4.0.2
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Run linter
        run: npm run lint
```

### ✅ GOOD: Minimal permissions with per-job grants

```yaml
name: release

on:
  push:
    tags: ['v*']

permissions: {}  # deny all by default

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    permissions:
      contents: read

    steps:
      - uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29  # v4.1.6

  publish:
    needs: build
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: write
      packages: write

    steps:
      - uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29  # v4.1.6
```

### ❌ BAD Examples

```yaml
# Pinned to tag — REJECTED
- uses: actions/checkout@v4
# Why: Must pin to full commit SHA, not tag

# Pinned to branch — REJECTED
- uses: actions/checkout@main
# Why: Must pin to full commit SHA, not branch

# No permissions block — REJECTED
name: ci
on: push
jobs:
  test:
    runs-on: ubuntu-latest
# Why: Missing explicit permissions block

# Overly broad permissions — REJECTED
permissions:
  contents: write
  pull-requests: write
  issues: write
  actions: write
# Why: Grant only what is needed (least privilege)

# No timeout — REJECTED
jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]
# Why: Missing timeout-minutes. Jobs could run forever.

# No caching — REJECTED
- name: Install
  run: npm install
# Why: Must cache dependencies. Also use "npm ci" not "npm install".

# Wrong file naming — REJECTED
# File: .github/workflows/CI_Test.yml
# Why: Must use kebab-case: ci-test.yml

# File in wrong location — REJECTED
# File: .github/ci-test.yml
# Why: Must be in .github/workflows/ directory
```

---

## Workflow Checklist

Before committing a workflow file, verify:

- [ ] All third-party actions pinned to commit SHA
- [ ] Explicit `permissions` block present
- [ ] Each job has `timeout-minutes` set
- [ ] Dependencies are cached
- [ ] File is in `.github/workflows/` directory
- [ ] File uses kebab-case naming
- [ ] No secrets hardcoded in workflow file
- [ ] Secrets referenced via `${{ secrets.NAME }}`
