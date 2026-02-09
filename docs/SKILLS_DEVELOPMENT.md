# Skills Development Guide

## Overview

This repository is a development environment for creating Claude Code skills and commands that will later be deployed to production projects.

## Current Skills

### BigQuery Skill Suite (v2.0.0)

**Location:** `skills/bigquery/`
**Status:** ✅ Installed to user skills
**Type:** Multi-skill suite with main router

**Structure:**
- Main router: Analyzes keywords and routes to appropriate sub-skill
- 8 specialized sub-skills covering all BigQuery features
- Comprehensive documentation and examples

**Usage:**
```bash
# Main router (auto-routing)
/bigquery optimize my slow query

# Direct sub-skill access
/bigquery/query-optimization
/bigquery/data-loading
/bigquery/bqml
/bigquery/scheduled-queries
/bigquery/cost-monitoring
/bigquery/security
/bigquery/schema-design
/bigquery/troubleshooting
```

See `skills/bigquery/DEPLOYMENT.md` for detailed installation and deployment instructions.

## Development Workflow

### 1. Create New Skill

```bash
# Create skill directory
mkdir -p skills/<skill-name>

# Create skill file
cat > skills/<skill-name>/SKILL.md << 'EOF'
# Your Skill Name

## Purpose
Brief description of what this skill does

## When to Use
Describe when this skill should be used

## Usage
Examples of how to use the skill

## Examples
Provide concrete examples
EOF
```

### 2. Test Locally

```bash
# Install to user skills for testing
cp -r skills/<skill-name> ~/.claude/skills/

# Test in Claude Code
/skill-name test command
```

### 3. Iterate and Improve

- Edit skill files based on testing
- Add real-world examples
- Document edge cases
- Update based on user feedback

### 4. Commit to Development Repo

```bash
git add skills/<skill-name>
git commit -m "Add <skill-name> skill"
```

### 5. Deploy to Production

When stable and tested:

```bash
# Copy to main project
cp -r skills/<skill-name> /path/to/main/project/skills/

# Or use git submodule
cd /path/to/main/project
git submodule add <this-repo-url> .claude-skills
```

## Skill Structure Best Practices

### Simple Skill
```
skill-name/
└── SKILL.md        # Single skill file
```

### Complex Skill Suite (like BigQuery)
```
skill-name/
├── SKILL.md                 # Main router
├── README.md                # Documentation
├── INSTALLATION.md          # Setup guide
├── sub-skill-1/
│   └── SKILL.md
├── sub-skill-2/
│   └── SKILL.md
└── sub-skill-3/
    └── SKILL.md
```

## SKILL.md Format

```markdown
# Skill Name

## Purpose
Clear, concise description (1-2 sentences)

## When to Use
- List specific scenarios
- Include keyword triggers if using auto-routing
- Mention related skills

## Requirements
- List any prerequisites
- Tools needed
- API access requirements

## Usage

### Basic Usage
\`\`\`bash
/skill-name basic command
\`\`\`

### Advanced Usage
\`\`\`bash
/skill-name advanced --options
\`\`\`

## Examples

### Example 1: Common Use Case
\`\`\`
Input: /skill-name do something
Output: [expected result]
\`\`\`

### Example 2: Complex Scenario
\`\`\`
[detailed example]
\`\`\`

## Patterns

### Pattern 1: [Pattern Name]
- Description
- Code example
- When to use

## Troubleshooting

### Issue 1: [Common Problem]
**Symptom:** [description]
**Solution:** [how to fix]

## Integration

How this skill works with:
- Other skills
- External tools
- APIs

## Related Skills
- `/other-skill` - description
- `/another-skill` - description
```

## Testing Checklist

Before deploying a skill, verify:

- [ ] SKILL.md file exists and is valid markdown
- [ ] Purpose is clear and concise
- [ ] Usage examples are accurate
- [ ] All code examples are tested
- [ ] Edge cases are documented
- [ ] Error handling is covered
- [ ] Integration notes are included
- [ ] File encoding is UTF-8
- [ ] No sensitive information (API keys, passwords)

## Skill Categories

### Data & Analytics
- BigQuery operations
- Database management
- Data transformation

### Development
- Code optimization
- Testing automation
- Debugging helpers

### DevOps & Infrastructure
- Deployment automation
- Monitoring setup
- Configuration management

### Documentation
- README generation
- API documentation
- Code commenting

### Security
- Security audits
- Vulnerability scanning
- Access control setup

## Multi-Skill Suites

For complex domains (like BigQuery), create a skill suite:

**Benefits:**
- Organized by functionality
- Main router for ease of use
- Can still access sub-skills directly
- Easier to maintain

**Structure:**
1. Main SKILL.md with routing logic
2. Sub-skills in subdirectories
3. Comprehensive README
4. Installation and deployment guides

**Example:** See `skills/bigquery/` for reference implementation

## Version Control

Tag skill versions for tracking:

```bash
# Tag a release
git tag -a <skill-name>-v1.0.0 -m "Description of release"

# Push tags
git push origin --tags

# List versions
git tag -l "<skill-name>-*"
```

## Deployment Strategies

### Strategy 1: Direct Copy
```bash
cp -r skills/<skill-name> /path/to/project/.claude/skills/
```
**Pros:** Simple, immediate
**Cons:** Manual updates needed

### Strategy 2: Git Submodule
```bash
git submodule add <repo-url> skills/<skill-name>
```
**Pros:** Version controlled, easy updates
**Cons:** Learning curve, submodule complexity

### Strategy 3: Package Distribution
```bash
# Create distributable package
tar -czf skill-name-v1.0.0.tar.gz skills/<skill-name>
```
**Pros:** Easy distribution to team
**Cons:** Manual installation for each user

### Strategy 4: Shared Network Location
```bash
# Copy to shared drive
cp -r skills/<skill-name> //shared/claude-skills/
```
**Pros:** Centralized, team access
**Cons:** Network dependency

## Maintenance

### Update Workflow

1. **Make changes** in dev repo
2. **Test** by copying to user skills
3. **Commit** to git
4. **Deploy** to production when stable
5. **Document** changes in skill README

### Regular Reviews

- Monthly review of skill usage
- Update examples based on real-world use
- Add new patterns discovered in production
- Remove deprecated patterns

### Versioning

Use semantic versioning:
- **Major (X.0.0):** Breaking changes
- **Minor (1.X.0):** New features, backwards compatible
- **Patch (1.0.X):** Bug fixes, small improvements

## Resources

- Claude Code Documentation: https://github.com/anthropics/claude-code
- Skills Examples: ~/.claude/skills/
- This Development Repo: D:\Screen1\screen1-claude

## Tips

1. **Start simple** - Create a basic skill first, add complexity later
2. **Test thoroughly** - Use real examples from your work
3. **Document everything** - Future you will thank current you
4. **Iterate based on usage** - Skills improve with real-world feedback
5. **Share learnings** - Good patterns help the whole team
6. **Version control** - Track changes and tag releases
7. **Keep it maintainable** - Clear structure, good documentation

---

**Happy skill building! 🚀**
