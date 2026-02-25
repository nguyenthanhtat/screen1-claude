# Frontmatter Writing Guide

The YAML frontmatter in `SKILL.md` controls everything about how Claude discovers and uses the skill.

## Required Fields

```yaml
---
name: your-skill-name
description: "What it does and when to use it."
---
```

## Optional Fields

```yaml
---
name: your-skill-name
description: "..."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---
```

---

## `name` Field Rules

- Use **kebab-case** (lowercase, hyphens only)
- Match the folder name exactly
- Be specific, not generic

```yaml
# BAD
name: frontend
name: code
name: helper

# GOOD
name: react-hooks
name: pdf-editor
name: bigquery-queries
```

---

## `description` Field Rules (Most Critical)

Claude matches the description against the user's message to decide whether to load the skill.
**A bad description = skill never triggers.**

### The formula:
```
"[What it does] for [domain]. Use when [trigger scenario 1], [trigger scenario 2], or [trigger scenario 3]."
```

### Good vs Bad

```yaml
# BAD — too vague
description: "Helps with React"
description: "Frontend stuff"
description: "Code helper"

# GOOD — specific actions + explicit triggers
description: "React hooks, state management, and component patterns for modern React apps. Use when building React components, writing custom hooks, optimizing renders, or managing state."

description: "Step-by-step PDF editing using pypdf. Use when rotating PDFs, extracting pages, merging documents, or modifying PDF metadata."

description: "BigQuery SQL query optimization and schema navigation for the analytics warehouse. Use when writing BigQuery queries, debugging slow queries, or exploring dataset schemas."
```

### Trigger phrases to include in description:
- Start with what Claude should DO: "Guides", "Provides", "Teaches", "Optimizes"
- End with "Use when [action]..." to give explicit trigger conditions
- Include synonyms: users say different things for the same task

---

## `allowed-tools` Field

Controls which tools Claude can use while running the skill.

| Tool | When to allow |
|------|--------------|
| `Read` | Reading files for context |
| `Write` | Creating new files |
| `Edit` | Modifying existing files |
| `Glob` | Finding files by pattern |
| `Grep` | Searching file contents |
| `Bash` | Running shell commands |
| `Bash(python:*)` | Running Python scripts specifically |
| `Bash(node:*)` | Running Node scripts specifically |

### Examples by skill type:

```yaml
# Read-only documentation skill
allowed-tools: Read, Grep, Glob

# Code generation skill
allowed-tools: Read, Write, Edit, Glob, Grep

# Skill with automation scripts
allowed-tools: Read, Write, Edit, Glob, Grep, Bash

# Specific script runner (safer)
allowed-tools: Read, Bash(python:*), Write
```

**Security tip**: Use narrowest allowed-tools set that works for the skill.

---

## Full Frontmatter Examples

### Simple knowledge skill:
```yaml
---
name: typescript-patterns
description: "TypeScript best practices for strict typing, generics, utility types, and error handling. Use when writing TypeScript code, adding types to JavaScript, using generics, or reviewing TypeScript files."
allowed-tools: Read, Grep, Glob
---
```

### Automation skill:
```yaml
---
name: pdf-editor
description: "PDF editing and manipulation using pypdf. Use when rotating PDFs, merging documents, extracting pages, adding watermarks, or modifying PDF files."
allowed-tools: Read, Write, Bash(python:*)
---
```

### Team knowledge skill:
```yaml
---
name: api-conventions
description: "Internal API design conventions, endpoint naming, error formats, and auth patterns for the screen1 platform. Use when designing API routes, writing API handlers, or reviewing endpoint implementations."
allowed-tools: Read, Grep, Glob, Write, Edit
---
```
