# No 'gh_' Prefix Rules

## Overview
This document defines rules to ensure project names do not use the 'gh_' prefix. 
These rules are designed to enforce naming conventions that avoid redundant prefixes 
in project names, repository names, and related identifiers.

## Rules

### Project Naming
- Project names MUST NOT start with the prefix 'gh_'
- Repository names MUST NOT start with the prefix 'gh_'
- When creating new projects, avoid using 'gh_' as a prefix
- Existing projects with 'gh_' prefix SHOULD be renamed to remove the prefix

### Enforcement
- All project names will be validated to ensure they do not start with 'gh_'
- Repository creation will fail if the name starts with 'gh_'
- CI/CD pipelines SHOULD include a check to validate project name format
- Naming validation tools MUST reject any name starting with 'gh_'

### Rationale
- The 'gh_' prefix is redundant as the context of GitHub is already understood
- Shorter, cleaner project names are preferred
- Avoiding prefixes reduces naming confusion and standardizes project naming
- Makes project names more flexible for use in different contexts

### Examples
```
✅ VALID names:
- project-name
- awesome-tool
- api-service
- mobile-app

❌ INVALID names:
- gh_project-name
- gh-awesome-tool
- gh_api-service
- gh_mobile-app
```

### Migration
- Existing projects with 'gh_' prefix SHOULD be migrated to new names
- Update all references to the project name in documentation, code, and CI/CD configurations
- Create redirects if necessary to maintain backward compatibility
- Update all team members and stakeholders about the name change