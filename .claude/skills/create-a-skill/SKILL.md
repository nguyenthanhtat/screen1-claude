---
name: create-a-skill
description: Step-by-step tutorial for creating Claude Code skills. Use when creating a new skill, building a SKILL.md file, designing a skill folder structure, or learning how to write effective skill descriptions and frontmatter.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Create-A-Skill Tutorial

A guided workflow for building any Claude Code skill from scratch — covering planning, structure, writing, and packaging.

## When This Skill Applies

- "I want to create a skill for X"
- "Help me build a skill for our team's Y workflow"
- "Create a new skill that handles Z"
- "How do I write a SKILL.md?"
- "What should my skill folder look like?"

---

## Step 1 — Understand What the Skill Does

Before writing any files, answer these 3 questions:

1. **What domain / task does this skill cover?**
   - Be specific. Not "frontend" but "React hooks and state management"
   - Not "docs" but "team API documentation lookup"

2. **What would a user say to trigger it?**
   - List 3–5 concrete trigger phrases
   - Example: "Build a React component", "optimize my hook", "add state management"

3. **What reusable resources would help Claude every time?**
   - Scripts that get rewritten repeatedly → `scripts/`
   - Documentation Claude needs to reference → `references/`
   - Templates / assets used in output → `assets/`

See [references/structure-patterns.md](references/structure-patterns.md) for help choosing what to include.

---

## Step 2 — Choose a Structure Pattern

Three patterns cover most skills:

### Pattern A — Simple (single domain)
```
my-skill/
├── SKILL.md
├── references/
│   └── topic.md
└── examples/
    └── example.md
```
Use for: focused single-topic skills (testing, TypeScript, git workflows)

### Pattern B — Complex (multi-domain routing hub)
```
my-skill/
├── SKILL.md              ← routing only
├── references/
│   ├── topic-a.md
│   ├── topic-b.md
│   └── topic-c.md
└── scripts/
    └── helper.py
```
Use for: broad domains needing sub-topic routing (Next.js fullstack, senior-backend)

### Pattern C — Reference + Automation
```
my-skill/
├── SKILL.md
├── references/           ← documentation
├── scripts/              ← executable tools
└── assets/               ← templates / files for output
```
Use for: skills that produce artifacts or run code (skill-creator, pdf-editor, code-formatter)

---

## Step 3 — Create the Folder

```bash
# Global skill (available everywhere)
mkdir -p ~/.claude/skills/<skill-name>/references
mkdir -p ~/.claude/skills/<skill-name>/assets
mkdir -p ~/.claude/skills/<skill-name>/scripts

# Project skill (only in this repo)
mkdir -p .claude/skills/<skill-name>/references
```

Or use the init script if available:
```bash
python .claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path ~/.claude/skills/
```

Copy the template to start:
```bash
cp .claude/skills/create-a-skill/assets/SKILL-template.md ~/.claude/skills/<skill-name>/SKILL.md
```

---

## Step 4 — Write SKILL.md

The `description` field is the most critical part — it controls when Claude auto-triggers the skill.

**Frontmatter rules:**
```yaml
---
name: skill-name-in-kebab-case
description: "Specific action + domain. Use when [concrete trigger scenarios]."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---
```

**Body rules:**
- Keep under 500 lines
- Overview in 2–3 sentences
- List trigger scenarios
- Core principles (numbered, concise)
- Link to `references/` — never inline everything
- Quick example if helpful

See [references/frontmatter-guide.md](references/frontmatter-guide.md) for description writing rules and examples.

---

## Step 5 — Add Supporting Files

### references/ files
- One topic per file (e.g., `references/hooks-patterns.md`, not `references/everything.md`)
- Load only when Claude needs them — keep them detailed
- If file > 10k words, add grep search hints in SKILL.md

### scripts/ files
- Include when the same code gets rewritten every session
- Claude can execute without reading into context (token efficient)

### assets/ files
- Templates, boilerplate, icons used in final output
- Not loaded into context, just copied/referenced

---

## Step 6 — Test the Skill

```bash
# Open Claude Code in the skill's directory
claude

# Try natural trigger phrases:
"I want to build a React component for user profiles"
"Help me write tests for this API"

# Verify:
# ✓ Claude announces using the skill
# ✓ Skill guidance appears in response
# ✓ Supporting files load when relevant
```

---

## Step 7 — Package (optional, for sharing)

```bash
python .claude/skills/skill-creator/scripts/package_skill.py .claude/skills/<skill-name>/
```

This validates structure and creates a distributable `.zip`.

---

## Quick Reference

| File/Folder | Purpose | Size limit |
|-------------|---------|------------|
| `SKILL.md` | Entry point, routing, core guidance | < 500 lines |
| `references/*.md` | Detailed domain knowledge | < 2000 lines each |
| `scripts/*.py` | Reusable executable code | No limit |
| `assets/` | Output templates & files | No limit |

See [references/checklist.md](references/checklist.md) for the full creation checklist.
