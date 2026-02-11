# Git Skill Suite - Architecture Documentation

Understanding the design and structure of the Git skill suite.

## Overview

The Git skill suite uses a **router architecture** with 8 specialized sub-skills, similar to the BigQuery skill suite. This design provides comprehensive Git coverage while keeping each skill focused and maintainable.

## Architecture Pattern

### Router + Sub-Skills

```
/git (Router)
 ├── /git/basics         (Sub-skill 1)
 ├── /git/branching      (Sub-skill 2)
 ├── /git/history        (Sub-skill 3)
 ├── /git/remote         (Sub-skill 4)
 ├── /git/conflicts      (Sub-skill 5)
 ├── /git/undo           (Sub-skill 6)
 ├── /git/workflows      (Sub-skill 7)
 └── /git/advanced       (Sub-skill 8)
```

## Directory Structure

```
skills/git/
├── SKILL.md                    # Main router skill
├── README.md                   # User documentation
├── QUICK_START.md             # 5-minute getting started guide
├── INSTALLATION.md            # Installation instructions
├── STRUCTURE.md               # This file - architecture docs
├── .claude.example            # Configuration template
│
├── basics/
│   └── SKILL.md               # Basic Git operations
│
├── branching/
│   └── SKILL.md               # Branch management
│
├── history/
│   └── SKILL.md               # History and inspection
│
├── remote/
│   └── SKILL.md               # Remote operations
│
├── conflicts/
│   └── SKILL.md               # Conflict resolution
│
├── undo/
│   └── SKILL.md               # Undo and recovery
│
├── workflows/
│   └── SKILL.md               # Team workflows
│
└── advanced/
    └── SKILL.md               # Advanced features
```

## Router Design (SKILL.md)

### Purpose

The main `SKILL.md` acts as an intelligent router that:

1. **Analyzes user questions** for Git-related keywords
2. **Routes to appropriate sub-skill** based on intent
3. **Provides direct access paths** for users who know which sub-skill they need
4. **Documents all sub-skills** with overview and use cases

### Routing Logic

```
User Query → Keyword Analysis → Route to Sub-Skill

Examples:
- "commit" → /git/basics
- "branch" → /git/branching
- "conflict" → /git/conflicts
- "undo" → /git/undo
- "history" → /git/history
- "push" → /git/remote
- "workflow" → /git/workflows
- "stash" → /git/advanced
```

### Decision Tree

The router uses a decision tree for keyword-based routing:

```yaml
Keywords Analysis:
  - [init, clone, commit, add, .gitignore] → basics/
  - [branch, merge, rebase, checkout] → branching/
  - [log, diff, blame, bisect] → history/
  - [remote, fetch, push, pull, upstream] → remote/
  - [conflict, resolve, merge conflict] → conflicts/
  - [undo, reset, revert, restore, reflog] → undo/
  - [workflow, github flow, git flow, PR] → workflows/
  - [stash, cherry-pick, hook, submodule] → advanced/
```

## Sub-Skill Design

Each sub-skill follows a consistent pattern:

### File Structure

```markdown
# [Sub-Skill Name]

**Parent Skill:** `/git`
**Path:** `/git/[sub-skill-name]`

## Purpose
Brief description of what this sub-skill covers

## When to Use
- Trigger keywords
- Common scenarios
- Chat command examples

## Requirements
<critical>
Prerequisites and dependencies
</critical>

## Verification
Commands to verify prerequisites

---

## Critical Rules
<critical>
Important safety rules and best practices
</critical>

---

## Patterns

### Pattern 1: [Name]
**Problem:** What problem does this solve
**Solution:** How to solve it
- ❌ BAD: Wrong way
- ✅ GOOD: Right way
**Impact:** Why this matters
**When to use:** Specific scenarios

### Pattern 2: [Name]
...

## Common Workflows
Real-world workflow examples

## Troubleshooting
Common issues and solutions

## Best Practices
Key recommendations

## Related Sub-Skills
Links to related skills

## Quick Command Reference
Essential commands
```

### Pattern Structure

Each pattern includes:

1. **Problem Statement** - What issue does this solve?
2. **Bad Example (❌)** - Common mistake or anti-pattern
3. **Good Example (✅)** - Correct approach
4. **Code Examples** - Actual Git commands with output
5. **Impact** - Why this matters
6. **When to Use** - Specific scenarios

## Domain Separation

### Why 8 Sub-Skills?

Git naturally divides into distinct domains:

1. **basics** - Foundation (init, clone, commit, push, pull)
2. **branching** - Branch operations (create, merge, rebase, delete)
3. **history** - Code archaeology (log, diff, blame, bisect)
4. **remote** - Collaboration (remote, fetch, push, pull, upstream)
5. **conflicts** - Resolution (merge conflicts, rebase conflicts, strategies)
6. **undo** - Recovery (restore, reset, revert, reflog)
7. **workflows** - Team patterns (GitHub Flow, Git Flow, PRs, code review)
8. **advanced** - Power features (stash, cherry-pick, hooks, submodules)

### Design Principles

**1. Single Responsibility**
- Each sub-skill focuses on one domain
- No overlap between sub-skills
- Clear boundaries

**2. Progressive Complexity**
- basics → intermediate → advanced
- New users start with basics
- Advanced users can skip ahead

**3. Self-Contained**
- Each sub-skill works independently
- Can be used without reading others
- Cross-references when needed

**4. Consistent Format**
- All sub-skills follow same structure
- Predictable user experience
- Easy to maintain

## Auto-Routing vs Direct Access

### Auto-Routing

Users can ask natural questions:
```bash
/git how do I commit changes
→ Routes to /git/basics

/git I have a merge conflict
→ Routes to /git/conflicts

/git undo my last commit
→ Routes to /git/undo
```

Claude analyzes the question and routes to the appropriate sub-skill.

### Direct Access

Power users can go directly:
```bash
/git/basics           # Skip routing, go to basics
/git/branching        # Direct to branching
/git/conflicts        # Direct to conflicts
```

Both methods work - auto-routing for convenience, direct access for speed.

## Critical Blocks

Throughout the skills, `<critical>` blocks highlight:

1. **Safety Rules** - Prevent data loss
2. **Requirements** - Prerequisites
3. **Best Practices** - Professional standards
4. **Warnings** - Dangerous operations

Example:
```markdown
<critical>
1. NEVER force push to shared branches
2. ALWAYS pull before push
3. NEVER commit secrets
</critical>
```

## Pattern Library

Each sub-skill contains 8 patterns:

- **Minimum:** 6 patterns (for focused topics)
- **Target:** 8 patterns (comprehensive coverage)
- **Maximum:** 10 patterns (very complex topics)

### Pattern Selection Criteria

Patterns are chosen based on:
1. **Frequency** - How often is this needed?
2. **Pain Points** - What causes problems?
3. **Best Practices** - What should users know?
4. **Real-World Use** - What do professionals do?

## Workflow Integration

### Common Workflows Section

Each sub-skill includes "Common Workflows" showing:

- **Daily Development** - Everyday operations
- **Code Review** - Preparing and reviewing code
- **Hotfix Process** - Emergency fixes
- **Open Source** - Contributing to projects

### Cross-Skill Workflows

Complex workflows span multiple sub-skills:

```
Feature Development:
1. /git/basics - Pull latest
2. /git/branching - Create feature branch
3. /git/basics - Make commits
4. /git/remote - Push to origin
5. /git/workflows - Create PR
6. /git/conflicts - Resolve any conflicts
7. /git/branching - Merge to main
8. /git/basics - Delete branch
```

## Relationship with Other Skills

### Related Skills

The Git skill complements:
- **BigQuery skill** - Version control for queries
- **Test-Fully skill** - Version control for tests
- **Any development skill** - Git is fundamental

### Independence

Git skill is fully independent:
- No dependencies on other skills
- Can be used standalone
- Self-contained documentation

## Maintenance and Updates

### Version Control

- **Skill Version:** Tracked in main SKILL.md
- **Format:** Semantic versioning (1.0.0)
- **Changelog:** Document all changes

### Update Process

1. Update relevant sub-skill SKILL.md
2. Update main router if routing changes
3. Update README.md if features added
4. Update version number
5. Document in changelog

### Backward Compatibility

- Maintain existing paths (/git/basics always works)
- Don't remove patterns without deprecation
- Add new patterns without breaking old ones

## Design Decisions

### Why Router Architecture?

**Pros:**
- ✅ Separate concerns (focused sub-skills)
- ✅ Easy to find specific topics
- ✅ Scalable (add more sub-skills)
- ✅ Maintainable (update one at a time)

**Cons:**
- ❌ More complex than single file
- ❌ More files to manage
- ❌ Routing logic needed

**Conclusion:** Pros outweigh cons for comprehensive skill suite.

### Why Not Unified (Like Test-Fully)?

**Unified approach** (single SKILL.md) works for:
- Narrow focused skills
- < 15 patterns total
- Simple domain

**Router approach** better for:
- Broad domain (Git has 50+ patterns)
- Multiple distinct areas
- Progressive learning path

Git has **64+ patterns** across 8 domains → Router architecture is appropriate.

### Why These 8 Sub-Skills?

Based on:
1. **Git's natural divisions** - How Git itself is organized
2. **User mental model** - How people think about Git
3. **Common questions** - What people ask most
4. **Learning progression** - Natural skill development path

## Future Enhancements

### Potential Additions

- **git/gui** - GUI tools (GitHub Desktop, GitKraken)
- **git/github** - GitHub-specific features (Actions, Pages)
- **git/gitlab** - GitLab-specific features
- **git/internals** - Git object model, plumbing commands

### Extensibility

New sub-skills can be added:
1. Create new directory: `skills/git/newskill/`
2. Add SKILL.md following pattern
3. Update main router with new keywords
4. Update README.md with new sub-skill
5. Version bump

## Performance Considerations

### Skill Loading

- Router loads first (fast)
- Sub-skill loads on demand (lazy loading)
- Only load what's needed

### File Size

- Main router: ~15KB
- Each sub-skill: ~15-25KB
- Total: ~200KB (acceptable)

### Response Time

- Auto-routing: < 1 second
- Direct access: < 0.5 seconds
- Pattern lookup: Instant

## Conclusion

The Git skill suite architecture provides:

✅ **Comprehensive Coverage** - All Git operations
✅ **Easy Navigation** - Auto-routing or direct access
✅ **Maintainability** - Modular, focused sub-skills
✅ **Scalability** - Easy to add new sub-skills
✅ **Consistency** - Standard pattern across all sub-skills
✅ **User-Friendly** - Beginner to advanced paths

This architecture balances complexity with usability, providing a powerful yet accessible Git learning and reference tool.

---

**Questions about architecture?** Consult this document or ask `/git`!
