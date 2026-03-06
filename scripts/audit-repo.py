#!/usr/bin/env python3
"""audit-repo.py — Audit a repository for compliance with managing-github-events rules.

Uses gh CLI for GitHub operations. No LLM.

Checks:
  1. Mandatory files (.gitignore, README.md, LICENSE, SECURITY.md, CHANGELOG.md)
  2. .gitignore required patterns
  3. Branch name validation
  4. Recent commit messages (Conventional Commits)
  5. Secret detection in local files
  6. Forbidden files (tracked on GitHub)

Usage:
    python3 audit-repo.py                # audit current directory
    python3 audit-repo.py /path/to/repo
    python3 audit-repo.py --commits 10   # check last 10 commits (default: 5)

Exit 0 = all pass, Exit 1 = violations found
"""

import os
import re
import sys
import subprocess
import json
from pathlib import Path

# ─── COLORS ──────────────────────────────────────────────────────────

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"
NC = "\033[0m"

# ─── CONSTANTS ───────────────────────────────────────────────────────

VALID_COMMIT_TYPES = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
COMMIT_REGEX = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(\([a-z0-9,\-]+\))?!?: [a-z].{1,68}[^.]$"
)

VALID_BRANCH_REGEX = re.compile(
    r"^(feat|fix|hotfix|refactor|docs|ci|release|experiment)/[a-z0-9][a-z0-9\-]{0,48}$"
)
FORBIDDEN_BRANCHES = {
    "main", "master", "develop", "dev", "staging", "production",
    "prod", "temp", "tmp", "test", "testing", "wip",
}

MANDATORY_FILES = [".gitignore", "README.md", "LICENSE", "SECURITY.md", "CHANGELOG.md"]

GITIGNORE_MUST_CONTAIN = [".env", "node_modules", "__pycache__", ".DS_Store"]

FORBIDDEN_PATHS = [
    "node_modules/", "vendor/", "__pycache__/", ".venv/", "venv/",
    ".env", ".env.local", ".env.production",
]

# Regex patterns for secrets (local detection)
SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key ID"),
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "OpenAI/Stripe Secret Key"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "GitHub Personal Access Token"),
    (re.compile(r"gho_[a-zA-Z0-9]{36}"), "GitHub OAuth Token"),
    (re.compile(r"glpat-[a-zA-Z0-9\-_]{20,}"), "GitLab Personal Access Token"),
    (re.compile(r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----"), "Private Key"),
    (re.compile(r"-----BEGIN CERTIFICATE-----"), "Certificate (may contain private key)"),
    (re.compile(r"xox[baprs]-[0-9a-zA-Z\-]{10,}"), "Slack Token"),
]

PAST_TENSE_WORDS = re.compile(
    r"^(added|fixed|removed|updated|changed|deleted|created|modified|improved|implemented) ",
    re.IGNORECASE,
)


# ─── HELPERS ─────────────────────────────────────────────────────────

def run_gh(args: list[str], cwd: str = ".") -> tuple[int, str]:
    """Run a gh command and return (exit_code, stdout)."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True, text=True, cwd=cwd,
        )
        return result.returncode, result.stdout.strip()
    except FileNotFoundError:
        return 1, ""


def get_repo_slug(cwd: str = ".") -> str:
    """Get owner/repo slug from gh CLI."""
    code, slug = run_gh(
        ["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
        cwd=cwd,
    )
    return slug if code == 0 else ""


def is_gh_repo(path: str) -> bool:
    """Check if path is inside a GitHub repository."""
    return bool(get_repo_slug(path))


def get_current_branch(repo: str) -> str:
    """Read current branch from .git/HEAD (no git command needed)."""
    head_path = os.path.join(repo, ".git", "HEAD")
    if not os.path.isfile(head_path):
        return ""
    with open(head_path) as f:
        content = f.read().strip()
    if content.startswith("ref: refs/heads/"):
        return content.replace("ref: refs/heads/", "")
    return ""  # detached HEAD


# ─── CHECKS ──────────────────────────────────────────────────────────

def check_mandatory_files(repo: str) -> list[str]:
    """Check that all mandatory files exist."""
    errors = []
    for f in MANDATORY_FILES:
        filepath = os.path.join(repo, f)
        if not os.path.isfile(filepath):
            errors.append(f"Missing mandatory file: {f}")
    return errors


def check_gitignore_patterns(repo: str) -> list[str]:
    """Check that .gitignore contains required patterns."""
    errors = []
    gitignore_path = os.path.join(repo, ".gitignore")
    if not os.path.isfile(gitignore_path):
        return ["Cannot check .gitignore patterns: file does not exist"]

    with open(gitignore_path, "r") as f:
        content = f.read()

    for pattern in GITIGNORE_MUST_CONTAIN:
        if pattern not in content:
            errors.append(f".gitignore missing required pattern: {pattern}")
    return errors


def check_branch_name(repo: str) -> list[str]:
    """Check current branch name against naming rules."""
    errors = []
    branch = get_current_branch(repo)
    if not branch:
        return []  # detached HEAD or not in a repo

    if branch in ("main", "master"):
        return []  # default branches are fine to BE on

    if branch in FORBIDDEN_BRANCHES:
        errors.append(f"Forbidden branch name: '{branch}'")
        return errors

    if not VALID_BRANCH_REGEX.match(branch):
        issues = []
        if re.search(r"[A-Z]", branch):
            issues.append("contains uppercase (must be lowercase)")
        if "_" in branch:
            issues.append("contains underscore (use hyphens)")
        if "/" not in branch:
            issues.append("missing type/ prefix")
        if len(branch) > 50:
            issues.append(f"too long ({len(branch)} chars, max 50)")
        detail = "; ".join(issues) if issues else "does not match <type>/<kebab-case>"
        errors.append(f"Invalid branch name: '{branch}' — {detail}")

    return errors


def check_commit_messages(repo: str, count: int = 5) -> list[str]:
    """Check recent commit messages via gh api (Conventional Commits)."""
    errors = []
    slug = get_repo_slug(repo)
    if not slug:
        return []

    jq_expr = '.[] | (.sha[:7] + "|||" + (.commit.message | split("\\n") | .[0]))'
    code, output = run_gh(
        ["api", f"repos/{slug}/commits?per_page={count}", "--jq", jq_expr],
        cwd=repo,
    )
    if code != 0 or not output:
        return []

    for line in output.split("\n"):
        if "|||" not in line:
            continue
        sha, subject = line.split("|||", 1)
        issues = []

        # Check type prefix
        if not re.match(VALID_COMMIT_TYPES, subject):
            issues.append("missing/invalid type prefix")

        # Check format
        if not COMMIT_REGEX.match(subject):
            if len(subject) > 72:
                issues.append(f"exceeds 72 chars ({len(subject)})")

            desc_match = re.match(
                r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
                r"(\([^)]+\))?!?: (.+)$",
                subject,
            )
            if desc_match:
                desc = desc_match.group(3)
                if desc and desc[0].isupper():
                    issues.append("description starts with uppercase")
                if subject.endswith("."):
                    issues.append("ends with period")
                if PAST_TENSE_WORDS.match(desc):
                    issues.append("uses past tense (should be imperative mood)")

        # Check for vague messages
        vague = {"update", "fix", "wip", "temp", "stuff", "changes", "misc", "minor"}
        desc_part = re.sub(
            r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
            r"(\([^)]+\))?!?: ",
            "", subject,
        )
        if desc_part.lower().strip() in vague:
            issues.append(f"vague description: '{desc_part}'")

        if issues:
            detail = "; ".join(issues)
            errors.append(f"Commit {sha}: '{subject}' — {detail}")

    return errors


def check_forbidden_files(repo: str) -> list[str]:
    """Check for forbidden tracked files via gh api."""
    errors = []
    slug = get_repo_slug(repo)
    if not slug:
        return []

    # Get default branch
    code, branch = run_gh(
        ["repo", "view", "--json", "defaultBranchRef", "-q", ".defaultBranchRef.name"],
        cwd=repo,
    )
    if code != 0 or not branch:
        return []

    code, output = run_gh(
        ["api", f"repos/{slug}/git/trees/{branch}?recursive=1", "--jq", ".tree[].path"],
        cwd=repo,
    )
    if code != 0 or not output:
        return []

    for filepath in output.split("\n"):
        if not filepath:
            continue
        for forbidden in FORBIDDEN_PATHS:
            if filepath.startswith(forbidden) or filepath == forbidden.rstrip("/"):
                errors.append(f"Forbidden tracked file: {filepath}")
                break

    return errors


def check_local_secrets(repo: str) -> list[str]:
    """Scan local files for potential secrets."""
    errors = []
    skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "vendor"}

    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in files:
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, repo)
            # skip binary-looking files
            if any(fname.endswith(ext) for ext in [".png", ".jpg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".zip", ".tar", ".gz", ".jar", ".class", ".so", ".dylib", ".exe"]):
                continue
            try:
                with open(full_path, "r", errors="ignore") as f:
                    content = f.read(50000)  # read first 50KB only
            except (IOError, OSError):
                continue

            for pattern, name in SECRET_PATTERNS:
                if pattern.search(content):
                    errors.append(f"⚠️  Potential {name} in file: {rel_path}")
                    break

    return errors


def check_changelog_format(repo: str) -> list[str]:
    """Basic validation of CHANGELOG.md format."""
    errors = []
    changelog_path = os.path.join(repo, "CHANGELOG.md")
    if not os.path.isfile(changelog_path):
        return []  # already caught by mandatory files check

    with open(changelog_path, "r") as f:
        content = f.read()

    if "[Unreleased]" not in content:
        errors.append("CHANGELOG.md missing [Unreleased] section")

    # Check for commit hash dumps (forbidden)
    git_dump_pattern = re.compile(r"^[a-f0-9]{7,40} ", re.MULTILINE)
    if len(git_dump_pattern.findall(content)) > 3:
        errors.append("CHANGELOG.md appears to contain commit log dumps (forbidden)")

    return errors


# ─── MAIN ────────────────────────────────────────────────────────────

def main() -> None:
    # Parse args
    repo = "."
    commit_count = 5

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--commits" and i + 1 < len(args):
            commit_count = int(args[i + 1])
            i += 2
        elif not args[i].startswith("-"):
            repo = args[i]
            i += 1
        else:
            i += 1

    repo = os.path.abspath(repo)

    print(f"\n{BOLD}{CYAN}🔍 Auditing repository: {repo}{NC}\n")

    if not is_gh_repo(repo):
        print(f"{RED}❌ Not a GitHub repository (gh CLI cannot detect repo): {repo}{NC}")
        sys.exit(1)

    # Run all checks
    checks = [
        ("📄 Mandatory Files", check_mandatory_files(repo)),
        ("📝 .gitignore Patterns", check_gitignore_patterns(repo)),
        ("🌿 Branch Name", check_branch_name(repo)),
        (f"💬 Commit Messages (last {commit_count})", check_commit_messages(repo, commit_count)),
        ("🚫 Forbidden Files", check_forbidden_files(repo)),
        ("🔑 Secret Detection", check_local_secrets(repo)),
        ("📋 Changelog Format", check_changelog_format(repo)),
    ]

    total_errors = 0

    for name, errors in checks:
        if errors:
            print(f"  {RED}❌ {name}{NC}")
            for err in errors:
                print(f"     {RED}• {err}{NC}")
            total_errors += len(errors)
        else:
            print(f"  {GREEN}✅ {name}{NC}")

    # Summary
    print()
    if total_errors == 0:
        print(f"{GREEN}{BOLD}✅ All checks passed! Repository is compliant.{NC}")
        sys.exit(0)
    else:
        print(f"{RED}{BOLD}❌ {total_errors} violation(s) found. Fix before proceeding.{NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
