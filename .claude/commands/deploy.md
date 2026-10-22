---
name: deploy
description: "Full deployment pipeline: PM plans → Dev implements → QA tests → Ops deploys. Orchestrates all 4 agents in sequence with human checkpoints."
---

# Deployment Pipeline

Run the full autonomous deployment pipeline for: **$ARGUMENTS**

## Pipeline Steps

Execute agents in this exact sequence with checkpoints between each stage:

---

### Stage 1: Planning (PM Agent)

Use the `pm-agent` to analyze the requirement and create a development plan.

Pass this requirement to the agent: "$ARGUMENTS"

After the PM agent completes:
- Show the user the contents of `docs/plan.md`
- **CHECKPOINT**: Ask the user: "Does this plan look correct? (yes to continue / no to adjust)"
- If no: ask what to change, update the plan, re-confirm before continuing
- If yes: proceed to Stage 2

---

### Stage 2: Implementation (Dev Agent)

Use the `dev-agent` to implement the tasks in `docs/plan.md`.

The agent will:
- Create a feature branch
- Implement all tasks
- Commit changes

After the Dev agent completes, proceed to Stage 3.

---

### Stage 3: Quality Assurance (QA Agent)

Use the `qa-agent` to write and run tests for the implemented feature.

After QA completes:
- Show the user the contents of `docs/test-report.md`
- If status is **FAIL**:
  - **CHECKPOINT**: Show failed tests to the user
  - Ask: "QA failed. Options: (1) re-run dev-agent to fix issues, (2) abort pipeline"
  - Handle user choice accordingly
- If status is **PASS**: proceed to Stage 4

---

### Stage 4: Deployment (Ops Agent)

Use the `ops-agent` to deploy the application.

**CHECKPOINT before production**: The ops-agent will ask for confirmation before deploying to production. Respect this gate — do not bypass it.

After the Ops agent completes:
- Show the deployment URLs
- Show the contents of `docs/deploy-log.md`

---

## Pipeline Complete

When all stages finish successfully, print:

```
🚀 Pipeline Complete!

Feature: $ARGUMENTS
Plan:    docs/plan.md
Tests:   docs/test-report.md
Deploy:  docs/deploy-log.md

The feature is live.
```

## Error Handling

- If any agent fails unexpectedly, stop the pipeline and report the error clearly
- Never skip a checkpoint
- Never deploy if QA status is FAIL
