# Repository Hygiene Rules

## Mandatory Files

Every repository MUST contain these files in the project root:

| File | Purpose |
|------|---------|
| `.gitignore` | Exclude build artifacts, dependencies, secrets, OS/IDE files |
| `README.md` | Project documentation (name, description, setup, usage, license) |
| `LICENSE` | Legal license file |
| `SECURITY.md` | Security policy (see security-rules.md) |
| `CHANGELOG.md` | Change history (see changelog-rules.md) |

---

## .gitignore Rules

The `.gitignore` MUST cover at minimum:

### OS Files
```gitignore
.DS_Store
Thumbs.db
Desktop.ini
*.swp
*.swo
*~
```

### IDE / Editor Configs
```gitignore
.idea/
.vscode/
*.iml
*.suo
*.user
.project
.classpath
.settings/
```

### Dependencies
```gitignore
node_modules/
vendor/
__pycache__/
*.pyc
.venv/
venv/
```

### Build Outputs
```gitignore
dist/
build/
out/
target/
*.class
*.jar
*.war
*.o
*.so
*.dylib
```

### Secrets / Environment
```gitignore
.env
.env.*
*.pem
*.key
*.p12
*.pfx
```

### Package Manager
```gitignore
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

---

## README.md Requirements

Every README.md MUST include at minimum:

1. **Project Name** — clear, descriptive title
2. **Description** — what the project does (1-3 sentences)
3. **Installation / Setup** — how to get it running
4. **Usage** — basic usage examples
5. **License** — which license applies

### README.md Template

```markdown
# Project Name

Brief description of what this project does.

## Installation

```bash
# Installation steps
```

## Usage

```bash
# Usage examples
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the [MIT License](LICENSE).
```

---

## FORBIDDEN in Git

| What | Why | Alternative |
|------|-----|-------------|
| Binary blobs >100KB | Bloats repo permanently | Use Git LFS or external storage |
| Compiled binaries | Build artifacts, not source | Build from source in CI |
| Archive files (.zip, .tar.gz) | Not diffable, bloats history | Use release assets |
| `node_modules/` | Dependencies, massive size | Use `npm ci` from `package-lock.json` |
| `vendor/` | Same as node_modules | Use package manager |
| `__pycache__/` | Python bytecode cache | Auto-generated, never commit |
| `.venv/` / `venv/` | Python virtual environment | Recreate from requirements.txt |
| Build outputs | Generated files | Build in CI |
| `.env` files | Contains secrets | Use environment variables |
| Database dumps | Large, contains data | Use migrations |

---

## Examples

### ✅ GOOD Repository Structure

```
my-project/
├── .github/
│   └── workflows/
│       └── ci-test.yml
├── src/
│   └── ...
├── tests/
│   └── ...
├── .gitignore          ✅ Required
├── CHANGELOG.md        ✅ Required
├── LICENSE             ✅ Required
├── README.md           ✅ Required
├── SECURITY.md         ✅ Required
└── package.json
```

### ❌ BAD Repository

```
my-project/
├── src/
├── node_modules/       ❌ FORBIDDEN — must be in .gitignore
├── .env                ❌ FORBIDDEN — contains secrets
├── build/              ❌ FORBIDDEN — build output
├── logo.psd            ❌ FORBIDDEN — binary blob (>100KB)
├── backup.sql          ❌ FORBIDDEN — database dump
└── (no .gitignore)     ❌ REJECTED — .gitignore is mandatory
└── (no README.md)      ❌ REJECTED — README.md is mandatory
└── (no LICENSE)        ❌ REJECTED — LICENSE is mandatory
```

---

## New Repository Checklist

When creating a new repository, verify:

- [ ] `.gitignore` created with all required patterns
- [ ] `README.md` created with all required sections
- [ ] `LICENSE` file added (choose appropriate license)
- [ ] `SECURITY.md` created from template
- [ ] `CHANGELOG.md` initialized with `[Unreleased]` section
- [ ] No secrets in any committed file
- [ ] No binary blobs committed
- [ ] Default branch is `main` (not `master`)
- [ ] Branch protection enabled on `main` (if supported)
