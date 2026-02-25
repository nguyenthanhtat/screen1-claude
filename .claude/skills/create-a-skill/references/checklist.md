# Skill Creation Checklist

Use this checklist when creating or reviewing any skill.

---

## Phase 1 — Before Writing Anything

```
□ Defined the domain clearly (specific, not vague)
□ Listed 3–5 concrete trigger phrases users would say
□ Identified what resources to include:
  □ Scripts — code that gets rewritten every session?
  □ References — docs Claude needs to read while working?
  □ Assets — templates/files used in output?
□ Chosen a structure pattern (Simple / Complex / Reference+Automation)
□ Picked a kebab-case skill name matching the folder name
```

---

## Phase 2 — Creating Files

### SKILL.md
```
□ YAML frontmatter present with name + description
□ name field: kebab-case, matches folder name
□ description field:
  □ Specific, not vague ("React hooks" not "frontend stuff")
  □ Includes "Use when [trigger scenarios]..."
  □ Lists synonyms / alternate phrasings
  □ Under 200 characters ideally
□ allowed-tools set to minimum needed
□ Body under 500 lines
□ Links to references/ instead of inlining everything
□ At least one concrete quick example
```

### references/ files
```
□ One topic per file (not one giant file)
□ Descriptive filenames (what the file covers)
□ Each file under 2000 lines
□ SKILL.md links to each reference file
□ No duplication between SKILL.md and references/
```

### scripts/ files
```
□ Script solves a real repetitive problem
□ Script has usage instructions (comment at top or in SKILL.md)
□ SKILL.md explains when/how to run each script
```

### assets/ files
```
□ Asset will actually be used in output (not just reference)
□ SKILL.md explains which asset to use for which situation
```

---

## Phase 3 — Testing

```
□ Open Claude Code in a relevant project
□ Ask a natural trigger phrase (don't say "use the skill")
  Example: "Build me a React component for user auth"
□ Verify:
  □ Claude announces the skill loaded
  □ Guidance is accurate and useful
  □ References load when their topic comes up
  □ Scripts run correctly if applicable
□ Ask 2–3 different trigger phrases to test description matching
□ Ask an OFF-TOPIC question — verify skill does NOT trigger
```

---

## Phase 4 — Quality Check

```
□ No walls of text (use bullet points, headers, code blocks)
□ Code examples actually work
□ No duplicated content between files
□ Folder structure is max 2 levels deep
□ Skill triggers automatically on natural phrases
□ SKILL.md readable in under 2 minutes
```

---

## Phase 5 — Packaging (if sharing)

```
□ Run package_skill.py to validate:
  python .claude/skills/skill-creator/scripts/package_skill.py .claude/skills/<skill-name>/
□ Fix any validation errors
□ Test the packaged .zip on a fresh install
□ Commit to git if sharing via repo
```

---

## Common Mistakes to Fix

| Mistake | Fix |
|---------|-----|
| SKILL.md > 500 lines | Move detail to references/, add link |
| Vague description ("helps with code") | Rewrite with specific domain + "Use when..." |
| Everything inlined in SKILL.md | Move to references/, link from SKILL.md |
| Folder deeper than 2 levels | Flatten the structure |
| Name doesn't match folder | Rename to match exactly |
| Skill triggers for wrong requests | Tighten the description |
| Skill never triggers | Broaden description, add more trigger phrases |
| Duplicate content in 2 files | Remove from one, keep in the authoritative file |
