# Security Rules

## SECURITY.md — MANDATORY

Every project MUST have a `SECURITY.md` file in the project root. NO EXCEPTIONS.

### SECURITY.md Template

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.2.x   | :white_check_mark: |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**DO NOT open a public issue for security vulnerabilities.**

Please report security vulnerabilities through one of these private channels:

1. **GitHub Security Advisories**: Use the "Report a vulnerability" button
   on the Security tab of this repository
2. **Email**: security@example.com

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

| Severity | Initial Response | Fix Timeline |
|----------|-----------------|--------------|
| Critical | 24-48 hours     | ASAP         |
| High     | 7 days          | 14 days      |
| Medium   | 30 days         | 60 days      |
| Low      | Next release    | Next release |

### Process

1. **Acknowledgment**: We will acknowledge receipt within the timeline above
2. **Assessment**: We will assess the vulnerability and determine severity
3. **Fix**: We will develop and test a fix
4. **Disclosure**: We will coordinate disclosure with the reporter
5. **Release**: We will release the fix and publish a security advisory

## Security Best Practices

- All dependencies are regularly audited
- Secrets are never committed to the repository
- Access is restricted on a need-to-know basis
```

---

## Zero Tolerance — Committed Secrets

The following MUST NEVER be committed to any repository:

| Type | Examples | Detection |
|------|----------|-----------|
| API Keys | `AKIA...`, `sk-...`, `ghp_...` | Pattern matching |
| Tokens | JWT tokens, OAuth tokens, session tokens | Pattern matching |
| Passwords | Database passwords, service passwords | String search |
| Private Keys | SSH keys (`-----BEGIN`), PGP keys | Header detection |
| Environment Files | `.env`, `.env.local`, `.env.production` | Filename matching |
| Certificates | `.pem`, `.p12`, `.pfx` files with private keys | Extension matching |
| Config with Secrets | `config.json` with passwords, `application.yml` with DB creds | Content scanning |

### Prevention

- `.gitignore` MUST include: `.env`, `.env.*`, `*.pem`, `*.key`
- Use environment variables for all secrets
- Use secret management tools (GitHub Secrets, vault, etc.)
- Run `git diff --cached` before every commit to review staged changes
- Consider using `git-secrets` or `gitleaks` as pre-commit hooks

### If a Secret is Accidentally Committed

1. **IMMEDIATELY** rotate/revoke the compromised secret
2. Remove the secret from the repository history (use `git filter-branch` or BFG Repo Cleaner)
3. Force-push the cleaned history
4. Notify affected parties
5. Create a security advisory if applicable

---

## Vulnerability Reporting Rules

- Vulnerabilities MUST be reported through private channels — NEVER through public issues
- Public disclosure MUST NOT happen until a fix is available
- The reporter SHOULD be credited in the security advisory (with their permission)

---

## Response Timeline

| Severity | Initial Response | Fix Deadline | Description |
|----------|-----------------|--------------|-------------|
| **Critical** | 24-48 hours | ASAP (48h target) | System down, data breach, RCE, auth bypass |
| **High** | 7 days | 14 days | Significant data exposure, privilege escalation |
| **Medium** | 30 days | 60 days | Limited impact, requires specific conditions |
| **Low** | Next release | Next release | Cosmetic, minimal risk, defense-in-depth |

---

## Examples

### ✅ GOOD

```bash
# .gitignore includes secret patterns
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "*.pem" >> .gitignore
echo "*.key" >> .gitignore

# Using environment variables
export DATABASE_URL="postgres://user:pass@localhost/db"

# SECURITY.md exists in project root
ls SECURITY.md  # file exists with proper template
```

### ❌ BAD

```bash
# Committing .env file — ZERO TOLERANCE
git add .env
git commit -m "chore: add config"
# Why: .env contains secrets. MUST be in .gitignore.

# Hardcoded API key in source — ZERO TOLERANCE
# const API_KEY = "sk-abc123def456";
# Why: Secrets must use environment variables.

# Public issue for vulnerability — FORBIDDEN
gh issue create --title "SQL injection in login endpoint"
# Why: Security vulnerabilities MUST use private channels.

# No SECURITY.md — REJECTED
# Why: Every project MUST have SECURITY.md in root.
```
