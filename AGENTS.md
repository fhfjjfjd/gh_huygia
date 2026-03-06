# AGENTS.md - AI Agent Configuration File

This file provides project-specific instructions for AI coding agents, particularly Qwen Code and Amp (ampcode).

## Project Overview

This project follows strict GitHub event management rules as defined in SKILL.md. All AI agents MUST comply with the rules in that file.

## Architecture

- Project type: GitHub repository management tools
- Primary language: Bash/Python
- Key components: Validation scripts, setup utilities, audit tools

## Key Integration Points

- Git operations: Follow conventional commits and branch naming
- GitHub CLI: Use proper formatting and labeling
- Validation scripts: Use scripts/validate-commit-msg.sh and scripts/validate-branch-name.sh

## Common Patterns

- Use specific file staging: `git add <specific-file>`
- Follow conventional commits format: `<type>(<scope>): <description>`
- Create branches with type prefixes: `feat/`, `fix/`, `hotfix/`, etc.

## Anti-Patterns

- Do NOT use `git add .` or `git add -A`
- Do NOT create branches without type prefixes
- Do NOT exceed 72 characters in commit subjects
- Do NOT commit without proper validation

## Tooling Requirements

- GitHub CLI must be authenticated
- Git must be properly configured with user.name and user.email
- Validation scripts must be used before commits/branches

## Special Instructions

1. **For Qwen Code**: 
   - Read and follow rules in SKILL.md
   - Use validation scripts before git operations
   - Refer to files in @reference/ directory for detailed specifications

2. **For Amp (ampcode)**:
   - Leverage available skills for common operations
   - Follow permission boundaries
   - Use subagents for complex operations

## Examples

### Valid Commit
```
feat(validation): enhance commit message validation with footer support

Add support for BREAKING CHANGE footers and multi-line commit bodies
with proper validation of each component.

BREAKING CHANGE: Previous commit validation was too restrictive
```

### Valid Branch
```
feat/validation-enhancement
```

## References

- See @reference/ai-agent-rules.md for detailed per-agent instructions
- See @reference/commit-rules.md for full commit specifications
- See @reference/branch-rules.md for full branch naming rules
- See SKILL.md for complete GitHub event management rules