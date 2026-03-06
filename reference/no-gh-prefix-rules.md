# No 'gh_' Prefix Rules

## Overview
This document defines best practices for project naming to avoid redundant prefixes in project names.
When the context is already clear (such as in a GitHub repository), using prefixes like 'gh_' is
unnecessary and adds redundancy.

## Guidelines

### Project Naming
- Project names SHOULD be concise and self-explanatory without redundant prefixes
- When creating new projects in GitHub context, avoid using 'gh_' as a prefix
- Use meaningful names that reflect the project's purpose rather than its hosting platform
- Existing projects with 'gh_' prefix MAY consider renaming to remove the prefix for consistency

### Rationale
- The 'gh_' prefix is redundant when the project is already in a GitHub context
- Shorter, cleaner project names are preferred
- Avoiding prefixes reduces naming redundancy and standardizes project naming
- Makes project names more portable across different platforms and contexts

### Examples
```
✅ RECOMMENDED names:
- project-name
- awesome-tool
- api-service
- mobile-app
- data-processor

❌ AVOID names with redundant prefixes:
- gh_project-name
- gh-awesome-tool
- gh_api-service
- gh_mobile-app
```

### Migration
- Existing projects with 'gh_' prefix MAY be migrated to new names as needed
- Update all references to the project name in documentation, code, and CI/CD configurations
- Create redirects if necessary to maintain backward compatibility
- Update all team members and stakeholders about the name change