# AI Agent Rules - Detailed Per-Agent Instructions

> **RFC 2119 Compliance**: The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
> "SHOULD", "SHOULD NOT", "FORBIDDEN", "REJECTED" in this document are to be interpreted as
> described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

This document provides **detailed, non-negotiable** instructions for each AI coding agent.
Each agent MUST follow these rules. Violations are REJECTED. No exceptions.

---

## 1. Universal Rules (ALL Agents)

### 1.1 Git Staging
- ALL agents MUST use `git add <specific-file>` — FORBIDDEN: `git add -A`, `git add .`
- Agents MUST NOT stage all files at once
- Specific files MUST be identified by name/path

### 1.2 Commit Messages
- ALL agents MUST follow Conventional Commits format exactly
- Format: `<type>(<scope>): <description>` with optional `!` for breaking changes
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### 1.3 Branch Management
- ALL agents MUST create branches with correct `type/` prefix before starting work
- Format: `<type>/<short-kebab-case-description>`
- Types: `feat/`, `fix/`, `hotfix/`, `refactor/`, `docs/`, `ci/`, `release/`, `experiment/`

### 1.4 Pull Requests
- ALL agents MUST use proper PR templates and full metadata
- Title MUST follow Conventional Commits format
- Body MUST include: summary, changes list, related issues, testing, checklist

### 1.5 Issue Management
- ALL agents MUST use `gh issue create` with full template body and proper labels
- Issues MUST have at minimum: one `type:*` label AND one `priority:*` label

---

## 2. OpenAI Codex / Codex CLI

### 2.1 Environment
- Runs in cloud sandboxed environments with repository pre-loaded
- CLI version runs locally with direct system access
- Uses AGENTS.md files for codebase navigation guidance

### 2.2 Git Integration
```bash
# Codex MUST use specific file staging:
git add path/to/specific-file.js
git add another-specific-file.py

# Codex MUST NOT use:
git add .
git add -A
git add --all
```

### 2.3 Commit Requirements
- Use `git commit -m "<conventional-commit-message>"`
- Breaking changes MUST include `!` and BREAKING CHANGE footer
- Commit messages MUST NOT exceed 72 characters in subject

### 2.4 Branch Creation
- Use `git checkout -b type/description` with proper prefix
- Verify branch name follows kebab-case conventions
- Push with `git push -u origin type/description`

### 2.5 GitHub CLI Usage
- Use `gh pr create --title "<conventional>" --body "<full template>"`
- Use `gh issue create --title "<title>" --body "<full template>" --label "type:bug,priority:P1"`

### 2.6 File Handling
- When reading files, Codex MUST use exact absolute paths
- When creating files, Codex MUST verify directory structure exists
- Codex MUST NOT create files in locations that violate project structure

---

## 3. Qwen Code

### 3.1 Environment
- Adapted from Gemini CLI for command-line workflow
- Specialized for understanding codebases and generating new code
- Uses chain-of-thought prompting for complex algorithmic challenges

### 3.2 Git Integration
```bash
# Qwen Code MUST use specific file staging:
git add path/to/specific-file.ts
git add path/to/directory/

# Qwen Code MUST NOT use:
git add .
git add -A
```

### 3.3 Context File
- Qwen Code reads `AGENTS.md` for project-specific instructions (NOT `QWEN.md`)
- This file SHOULD include:
  - Project architecture overview
  - Key integration points
  - Common patterns and anti-patterns
  - Specific tooling requirements

### 3.4 Commit Requirements
- Use `git commit -m "<conventional-commit-message>"`
- For breaking changes: include `!` and BREAKING CHANGE footer
- Validate with `scripts/validate-commit-msg.sh` before committing

### 3.5 Branch Management
- Create branches with `git checkout -b type/description`
- Use `scripts/validate-branch-name.sh` to validate branch names
- Follow kebab-case and type prefix requirements

### 3.6 Code Generation
- Prioritize code quality and maintainability
- Follow project-specific style guides
- Include appropriate error handling and edge case coverage
- Add meaningful comments and documentation

---

## 4. Amp (ampcode)

### 4.1 Environment
- Uses Bash tool for git/gh commands
- Features agentic code review capabilities
- Includes clickable diagrams and fast search subagents
- Uses AGENTS.md + Skills system
- Implements permission system for tool access

### 4.2 Git Integration
- Use `git add <specific-file>` exclusively
- Verify file existence before adding
- Use `git status` to verify staged files before commit

### 4.3 Commit Process
- Validate commit message with `scripts/validate-commit-msg.sh`
- Use `git commit -m "<message>"` with validated message
- Verify commit was created successfully

### 4.4 Branch Process
- Create branches with `git checkout -b type/description`
- Validate with `scripts/validate-branch-name.sh`
- Push with `git push --set-upstream origin <branch-name>`

### 4.5 Skills System
- Use available skills for common operations
- Follow skill-specific instructions and validation
- Leverage subagents for complex operations
- Respect permission boundaries of each skill

### 4.6 Code Review
- Perform internal code review before committing
- Check for common issues: security, performance, maintainability
- Verify compliance with project standards
- Test functionality when possible

---

## 5. Claude Code

### 5.1 Environment
- Has built-in git integration capabilities
- Uses CLAUDE.md for project-specific instructions
- Implements permission tiers: read-only/edit/shell
- Supports custom slash commands for workflow enforcement

### 5.2 Git Integration
- Use specific file staging: `git add <file>`
- Leverage built-in git commands when available
- Validate operations before execution

### 5.3 Permission Tiers
- **Read-only**: Can read files, search, analyze code
- **Edit**: Can modify files in addition to read operations
- **Shell**: Can execute shell commands in addition to edit operations

### 5.4 Commit Requirements
- Follow conventional commits format exactly
- Use appropriate type and scope
- Include breaking change markers when applicable
- Add BREAKING CHANGE footer for breaking changes

### 5.5 Branch Management
- Create branches with proper type prefixes
- Use kebab-case for branch names
- Validate branch names before creation

### 5.6 Slash Commands
- Use `/git` commands for git operations when available
- Use `/gh` commands for GitHub operations when available
- Follow custom workflow commands as defined in CLAUDE.md

---

## 6. Gemini CLI

### 6.1 Environment
- Uses Shell tool for git/gh commands
- Default behavior may use `git add .` — THIS MUST BE PREVENTED
- Uses GEMINI.md for instructions

### 6.2 Critical Staging Rule
```bash
# Gemini CLI MUST use specific file staging:
git add path/to/specific-file.js
git add another-specific-file.ts

# Gemini CLI MUST NEVER use (this is CRITICAL):
git add .
git add -A
git add --all
```

### 6.3 Git Operations
- Verify individual files before staging
- Use `git status` to confirm what will be staged
- Validate with `git diff --cached` before committing

### 6.4 Commit Process
- Use `git commit -m "<validated-conventional-message>"`
- Include breaking change indicators when applicable
- Verify commit message format before committing

### 6.5 GitHub Operations
- Use `gh` commands with full parameters
- Include proper titles, bodies, and labels
- Follow templates for consistency

---

## 7. iFlow CLI

### 7.1 Environment
- Uses Shell tool for git/gh commands
- Uses IFLOW.md for instructions
- Implements 4 modes: YOLO/Accepting Edits/Plan/Default
- Supports SubAgent system

### 7.2 Operational Modes
- **YOLO Mode**: Quick execution with minimal validation
- **Accepting Edits**: Review and accept changes before applying
- **Plan Mode**: Create detailed execution plan before acting
- **Default Mode**: Standard validation and execution

### 7.3 Git Integration
- Use `git add <specific-file>` exclusively
- Verify file paths before staging
- Follow conventional commits for all messages

### 7.4 SubAgent System
- Leverage specialized subagents for specific tasks
- Coordinate between subagents for complex operations
- Maintain context consistency across subagent interactions

### 7.5 Commit Requirements
- Follow conventional commits format with validation
- Include breaking changes with proper markers and footers
- Use multi-line commits with proper body and footer formatting when needed

### 7.6 Quality Assurance
- Validate changes against project requirements
- Verify code quality and style compliance
- Test functionality when possible
- Ensure documentation updates are included

---

## 8. Agent-Specific Context Files

### 8.1 File Locations
| Agent | Context File | Purpose |
|-------|-------------|---------|
| OpenAI Codex | `CODEX.md` | Codex-specific instructions and patterns |
| Qwen Code | `AGENTS.md` | (NOT `QWEN.md`) - General agent instructions |
| Amp (ampcode) | `AGENTS.md` | Skills and permission system configuration |
| Claude Code | `CLAUDE.md` | Claude-specific workflow and commands |
| Gemini CLI | `GEMINI.md` | Gemini-specific instructions and restrictions |
| iFlow CLI | `IFLOW.md` | Mode-specific and subagent configurations |

### 8.2 Context File Contents
Each agent context file SHOULD include:
- Project-specific architecture details
- Key integration points
- Common patterns and anti-patterns
- Tooling requirements and configurations
- Special restrictions or requirements for the agent
- Examples of proper usage in this specific project

### 8.3 Cross-Reference Requirements
- All agent context files SHOULD reference `SKILL.md` for universal rules
- Include links to relevant reference files in `@reference/` directory
- Maintain consistency with overall project standards
- Document any agent-specific exceptions to universal rules (with approval)

---

## 9. Compliance Verification

### 9.1 Agent Self-Validation
Before executing any git operation, agents MUST:
1. Validate the operation against these rules
2. Verify file paths and arguments
3. Check for compliance with conventional formats
4. Confirm proper permissions and scope

### 9.2 Common Validation Scripts
Agents SHOULD use these scripts for validation:
- `scripts/validate-commit-msg.sh` for commit messages
- `scripts/validate-branch-name.sh` for branch names
- `scripts/audit-repo.py` for repository compliance
- `scripts/setup-repo.py` for repository initialization

### 9.3 Error Handling
When rules are violated:
- Agents MUST NOT proceed with the operation
- Agents MUST report the specific rule violation
- Agents SHOULD suggest the correct approach
- Agents MUST allow human intervention if needed

---

## 10. Violation Consequences

Violations of any rule in this document SHALL result in:
1. Immediate halt of the current operation
2. Detailed error reporting of the violation
3. Required correction before proceeding
4. No exceptions to the rules
5. Escalation to human review if automated correction fails

---

## 11. Updates and Maintenance

This document MUST be updated when:
- New AI agents are introduced to the workflow
- Conventional Commits or other standards are updated
- New security requirements are identified
- Agent-specific capabilities change
- Project-specific requirements evolve

Each agent implementation SHOULD include version tracking to ensure compatibility with these rules.