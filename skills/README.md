# Skills

Custom Claude Code skills for extended functionality.

## What are Skills?

Skills are specialized tools that Claude can invoke when users request specific actions. They appear as slash commands (e.g., `/commit`, `/review-pr`).

## Creating a Skill

Skills are defined in `~/.claude/skills/` directory. Each skill needs:
- A skill definition file (YAML or JSON)
- Optional supporting scripts or tools

## Testing Skills

Place test cases in the `../tests/` directory to validate skill functionality before deployment.

## Examples

Check this directory for example skills to use as templates.
