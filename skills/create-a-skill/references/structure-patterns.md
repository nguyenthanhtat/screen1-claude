# Skill Structure Patterns

Three patterns cover the majority of skills. Choose based on complexity and what resources the skill needs.

---

## Pattern A — Simple Skill (Single Domain)

Best for: focused, single-topic skills with mostly inline guidance.

```
~/.claude/skills/testing/
├── SKILL.md                    ← overview + all core guidance
├── references/
│   ├── jest-patterns.md        ← detailed Jest examples
│   └── rtl-patterns.md        ← React Testing Library patterns
└── examples/
    ├── unit-test.tsx
    └── integration-test.tsx
```

**SKILL.md size**: 200–400 lines
**When to use**: The skill covers one clear domain. Users ask similar questions each time.

**Real examples**: `testing`, `typescript-patterns`, `git-workflows`

---

## Pattern B — Complex Skill (Multi-Domain Routing Hub)

Best for: broad domains where you need to route to sub-topics.

```
~/.claude/skills/senior-backend/
├── SKILL.md                         ← routing only (~300 lines)
├── references/
│   ├── api_design_patterns.md       ← REST/GraphQL API design
│   ├── database_optimization.md     ← Query optimization
│   └── backend_security.md         ← Auth, validation, security
└── scripts/
    ├── api_scaffolder.py
    └── database_migration_tool.py
```

**SKILL.md size**: 300–400 lines (mostly routing links, not detail)
**When to use**: The domain has 3+ distinct sub-topics. SKILL.md would exceed 500 lines without splitting.

**Real examples**: `senior-backend`, `senior-frontend`, `nextjs-fullstack`

---

## Pattern C — Reference + Automation

Best for: skills that execute code, produce files, or need bundled assets.

```
~/.claude/skills/skill-creator/
├── SKILL.md                         ← workflow steps
├── references/                      ← process documentation
├── scripts/
│   ├── init_skill.py               ← generates skill folder
│   └── package_skill.py            ← validates + zips skill
└── assets/
    └── skill-template/             ← boilerplate to copy
```

**SKILL.md size**: 300–500 lines
**When to use**: Skill produces output files, runs tools, or needs copy-paste templates.

**Real examples**: `skill-creator`, `pdf-editor`, `code-formatter`

---

## Folder Naming Conventions

```
# Skills folder (kebab-case, match the `name` field in frontmatter)
~/.claude/skills/react-hooks/       ✓
~/.claude/skills/ReactHooks/        ✗
~/.claude/skills/react_hooks/       ✗

# References (topic-based, descriptive)
references/hooks-patterns.md        ✓  (what it covers)
references/error-handling.md        ✓  (specific topic)
references/doc1.md                  ✗  (meaningless)
references/stuff.md                 ✗  (vague)

# Scripts (action-verb naming)
scripts/rotate_pdf.py               ✓  (what it does)
scripts/analyze_bundle.py           ✓  (what it does)
scripts/script1.py                  ✗  (meaningless)

# Assets (descriptive)
assets/react-component-template/    ✓
assets/email-template.html          ✓
assets/template/                    ✗  (too vague)
```

---

## Depth Rules

**Maximum 2 levels deep** inside a skill folder.

```
# GOOD
references/hooks-patterns.md
references/state-management.md
scripts/rotate_pdf.py

# BAD (too deep)
references/advanced/patterns/hooks/custom-hooks.md
```

---

## What Goes Where

| Resource | Folder | When to include |
|----------|--------|----------------|
| Domain knowledge, schemas, docs | `references/` | When Claude needs to read it while working |
| Executable code | `scripts/` | When same code gets rewritten every session |
| Output templates, boilerplate, images | `assets/` | When Claude produces files using them |
| One-liners, short examples | `SKILL.md` inline | When it fits in <20 lines |

---

## Size Limits

| File | Limit | Reason |
|------|-------|--------|
| `SKILL.md` | < 500 lines | Loaded in full when skill triggers |
| `references/*.md` | < 2000 lines | Loaded on demand |
| `scripts/*` | No limit | Executed without loading into context |
| `assets/*` | No limit | Not loaded into context |

**If SKILL.md exceeds 500 lines**: move detail to `references/` and link with:
```markdown
See [references/topic.md](references/topic.md) for details.
```

---

## Progressive Disclosure Flow

```
User message
    ↓
Metadata scan (name + description) — ~50 tokens
    ↓ match
SKILL.md loads — ~300-500 tokens
    ↓ Claude references a topic
references/topic.md loads — ~200 tokens
    ↓ Claude needs to run code
scripts/tool.py executes — 0 tokens (not loaded into context)
```

Total for a full session: ~750 tokens vs ~17,500 for repeated web searches.
