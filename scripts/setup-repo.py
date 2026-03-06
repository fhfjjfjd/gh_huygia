#!/usr/bin/env python3
"""setup-repo.py — Initialize a new repository with all mandatory files.

Creates: .gitignore, README.md, LICENSE (MIT), SECURITY.md, CHANGELOG.md
Skips files that already exist. Sets up GitHub labels via gh CLI.

Usage:
    python3 setup-repo.py                    # uses current directory name
    python3 setup-repo.py my-project         # custom project name
    python3 setup-repo.py --labels-only      # only create GitHub labels
"""

import os
import sys
import subprocess
import datetime

# ─── CONFIG ──────────────────────────────────────────────────────────

AUTHOR = "Gia Huy"
YEAR = datetime.datetime.now().year
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

LABELS = {
    # type labels
    "type:bug":      {"color": "d73a4a", "desc": "Bug report"},
    "type:feature":  {"color": "0075ca", "desc": "Feature request"},
    "type:docs":     {"color": "0e8a16", "desc": "Documentation"},
    "type:chore":    {"color": "e4e669", "desc": "Maintenance task"},
    "type:refactor": {"color": "d4c5f9", "desc": "Code restructuring"},
    "type:question": {"color": "d876e3", "desc": "Question or discussion"},
    # priority labels
    "priority:P0":   {"color": "b60205", "desc": "Critical: immediate action required"},
    "priority:P1":   {"color": "d93f0b", "desc": "High: within 24 hours"},
    "priority:P2":   {"color": "fbca04", "desc": "Medium: within 1 week"},
    "priority:P3":   {"color": "0e8a16", "desc": "Low: next release"},
    # status labels
    "status:triage":      {"color": "ededed", "desc": "Needs triage/review"},
    "status:confirmed":   {"color": "0e8a16", "desc": "Confirmed, ready for work"},
    "status:in-progress": {"color": "fbca04", "desc": "Being worked on"},
    "status:blocked":     {"color": "d73a4a", "desc": "Blocked by dependency"},
    "status:wontfix":     {"color": "ffffff", "desc": "Will not be fixed"},
    "status:duplicate":   {"color": "cfd3d7", "desc": "Duplicate of another issue"},
}

# ─── TEMPLATES ───────────────────────────────────────────────────────

GITIGNORE = """\
# OS
.DS_Store
Thumbs.db
Desktop.ini
*.swp
*.swo
*~

# IDE / Editor
.idea/
.vscode/
*.iml
*.suo
*.user
.project
.classpath
.settings/

# Dependencies
node_modules/
vendor/
__pycache__/
*.pyc
.venv/
venv/

# Build
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

# Secrets / Environment
.env
.env.*
*.pem
*.key
*.p12
*.pfx

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Package manager
package-lock.json
yarn.lock
"""


def readme_template(name: str) -> str:
    return f"""\
# {name}

Brief description of what this project does.

## Installation

```bash
# Installation steps here
```

## Usage

```bash
# Usage examples here
```

## Contributing

Please read the contributing guidelines before submitting a PR.

## License

This project is licensed under the [MIT License](LICENSE).
"""


def license_template() -> str:
    return f"""\
MIT License

Copyright (c) {YEAR} {AUTHOR}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def security_template() -> str:
    return """\
# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| latest  | :white_check_mark: |

## Reporting a Vulnerability

**DO NOT open a public issue for security vulnerabilities.**

Please report security vulnerabilities through one of these private channels:

1. **GitHub Security Advisories**: Use the "Report a vulnerability" button
   on the Security tab of this repository
2. **Email**: (add your security contact email)

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
"""


def changelog_template() -> str:
    return f"""\
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
"""


# ─── HELPERS ─────────────────────────────────────────────────────────

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"


def write_if_missing(path: str, content: str) -> None:
    if os.path.exists(path):
        print(f"  {YELLOW}⏭  Skipped{NC}  {path} (already exists)")
    else:
        with open(path, "w") as f:
            f.write(content)
        print(f"  {GREEN}✅ Created{NC} {path}")


def create_labels() -> None:
    print(f"\n{CYAN}📌 Setting up GitHub labels...{NC}\n")

    # Check gh CLI
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"  {RED}❌ gh CLI not found or not authenticated. Skipping labels.{NC}")
        return

    # Check if in a GitHub repo
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "name"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  {YELLOW}⚠️  Not in a GitHub repository. Skipping labels.{NC}")
        return

    for name, info in LABELS.items():
        result = subprocess.run(
            ["gh", "label", "create", name,
             "--color", info["color"],
             "--description", info["desc"],
             "--force"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  {GREEN}✅{NC} {name}")
        else:
            err = result.stderr.strip()
            if "already exists" in err:
                print(f"  {YELLOW}⏭ {NC} {name} (already exists)")
            else:
                print(f"  {RED}❌{NC} {name}: {err}")


# ─── MAIN ────────────────────────────────────────────────────────────

def main() -> None:
    labels_only = "--labels-only" in sys.argv

    if labels_only:
        create_labels()
        return

    # Determine project name
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        project_name = sys.argv[1]
    else:
        project_name = os.path.basename(os.getcwd())

    print(f"\n{CYAN}🚀 Setting up repository: {project_name}{NC}\n")
    print(f"{CYAN}📁 Creating mandatory files...{NC}\n")

    write_if_missing(".gitignore", GITIGNORE)
    write_if_missing("README.md", readme_template(project_name))
    write_if_missing("LICENSE", license_template())
    write_if_missing("SECURITY.md", security_template())
    write_if_missing("CHANGELOG.md", changelog_template())

    # Create labels
    create_labels()

    # Summary
    print(f"\n{GREEN}✅ Repository setup complete!{NC}")
    print(f"\n{CYAN}Next steps:{NC}")
    print(f"  1. Review and customize the generated files")
    print(f"  2. Stage files: gh repo sync  # or use gh api to commit")
    print(f"  3. Commit via gh: gh api repos/{{owner}}/{{repo}}/... or push directly")
    print()


if __name__ == "__main__":
    main()
