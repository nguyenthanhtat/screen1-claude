# BigQuery Skills - Deployment Guide

## Development Repository

This skill is maintained in the `screen1-claude` development repository for testing and iteration before deployment to production.

## Current Status

**Version:** 2.0.0
**Status:** ✅ Installed in user skills directory
**Location:** `~/.claude/skills/bigquery/`

## Installation Verification

The skill has been installed to your Claude user skills directory. To verify it's working:

```bash
# Try using the main skill
/bigquery

# Try a specific sub-skill
/bigquery/query-optimization optimize this query "SELECT * FROM table"
```

## Structure Overview

```
bigquery/
├── SKILL.md                    # Main router (recognizes keywords and routes)
├── query-optimization/         # Performance & cost optimization
├── data-loading/              # Import/export operations
├── bqml/                      # Machine learning models
├── scheduled-queries/         # Automation & ETL
├── cost-monitoring/           # Budget tracking
├── security/                  # Access control & RLS
├── schema-design/             # Table design patterns
└── troubleshooting/           # Debug & fix issues
```

## How Claude Code Skills Work

**Important Notes:**
1. Skills are loaded when Claude Code starts
2. Claude Code may need to be restarted after installing new skills
3. The skill uses a router pattern - `/bigquery` analyzes your request and routes to the appropriate sub-skill
4. You can call sub-skills directly: `/bigquery/query-optimization`

## Testing the Skill

### Test 1: Main Router
```bash
/bigquery my query is slow
```
Should route to `/bigquery/query-optimization`

### Test 2: Direct Sub-Skill
```bash
/bigquery/data-loading help me load CSV data
```
Should provide data loading guidance

### Test 3: Keyword Recognition
```bash
/bigquery predict customer churn
```
Should route to `/bigquery/bqml`

## Deployment Workflow

### Stage 1: Development (Current)
1. Edit skills in `D:\Screen1\screen1-claude\skills\bigquery\`
2. Test changes locally
3. Commit to git

### Stage 2: User Installation
```bash
# Copy from dev repo to user skills
cp -r D:\Screen1\screen1-claude\skills\bigquery ~/.claude/skills/

# Or update existing
rm -rf ~/.claude/skills/bigquery
cp -r D:\Screen1\screen1-claude\skills\bigquery ~/.claude/skills/
```

### Stage 3: Team Deployment
When ready to share with your team:

```bash
# Option 1: Direct copy to their user skills
cp -r bigquery /path/to/shared/location/

# Option 2: Git submodule in main project
cd /path/to/main/project
git submodule add <this-repo-url> skills/bigquery

# Option 3: Package as plugin
# Create installable package for team distribution
```

## Update Workflow

When you make changes:

```bash
# 1. Edit in dev repo
cd D:\Screen1\screen1-claude\skills\bigquery

# 2. Test the changes
# Edit SKILL.md files as needed

# 3. Update user installation
cp -r D:\Screen1\screen1-claude\skills\bigquery ~/.claude/skills/

# 4. Restart Claude Code to reload
# (Claude Code picks up changes on restart)

# 5. Commit to git
git add skills/bigquery
git commit -m "Update BigQuery skill: <what changed>"
```

## Troubleshooting

### Skill Not Recognized

**Symptom:** `/bigquery` returns "Unknown skill: bigquery"

**Solutions:**
1. Verify installation:
   ```bash
   ls -la ~/.claude/skills/bigquery/SKILL.md
   ```

2. Check file encoding (must be UTF-8)

3. Restart Claude Code

4. Check Claude Code logs for errors

### Sub-Skills Not Working

**Symptom:** `/bigquery/query-optimization` doesn't work

**Possible Issue:** Claude Code might not support nested sub-skill routing pattern

**Solution:** Use the main router and let it route automatically:
```bash
# Instead of: /bigquery/query-optimization fix this query
# Use: /bigquery optimize my query "SELECT ..."
```

### Routing Not Working

**Symptom:** Keywords don't route to correct sub-skill

**Solution:** The SKILL.md router analyzes keywords. Review the decision tree in SKILL.md and ensure your request includes relevant keywords.

## Version Control

Track skill versions in this dev repository:

```bash
# Tag releases
git tag -a bigquery-v2.0.0 -m "Initial BigQuery skill suite"

# View history
git log -- skills/bigquery/
```

## Next Steps

1. **Test the skill** - Try various commands to ensure routing works
2. **Customize for your use cases** - Add company-specific patterns
3. **Document learnings** - Update skills based on real usage
4. **Share with team** - Deploy to main project when stable
5. **Iterate** - Keep improving based on feedback

## File Locations

- **Development:** `D:\Screen1\screen1-claude\skills\bigquery\`
- **Installed:** `~/.claude/skills/bigquery/` (same as `C:\Users\nguye\.claude\skills\bigquery\`)
- **Git Repo:** `D:\Screen1\screen1-claude`

## Quick Commands

```bash
# Update installation from dev repo
cp -r "D:\Screen1\screen1-claude\skills\bigquery" ~/.claude/skills/

# Check what's installed
ls -la ~/.claude/skills/

# View skill content
cat ~/.claude/skills/bigquery/SKILL.md

# Test skill
# (in Claude Code) /bigquery help
```

---

**Status:** Ready to test and use! 🚀

Try running `/bigquery` in Claude Code to verify the installation.
