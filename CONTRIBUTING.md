# Contributing to screen1-claude

Thank you for your interest in contributing! This guide will help you get started.

## 🎯 Ways to Contribute

- **Report issues** - Found a bug or have a suggestion? Open an issue
- **Improve documentation** - Fix typos, clarify instructions, add examples
- **Add patterns** - Share new BigQuery patterns you've discovered
- **Create skills** - Develop new Claude Code skills for other tools

## 🚀 Getting Started

### 1. Fork the Repository

1. Click the "Fork" button on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/screen1-claude.git
   cd screen1-claude
   ```

### 2. Make Changes

```bash
# Create a branch for your changes
git checkout -b feature/your-feature-name

# Make your changes
# Edit files, add new patterns, etc.

# Test your changes
cp -r skills/bigquery ~/.claude/skills/
# Test with Claude Code
```

### 3. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "Add: description of your contribution"

# Push to your fork
git push origin feature/your-feature-name
```

### 4. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Describe your changes
4. Submit for review

## 📋 Contribution Guidelines

### Code Style

- Use clear, descriptive names
- Add comments for complex logic
- Follow existing file structure

### Documentation

- Update README.md if adding new skills
- Add usage examples
- Include before/after for optimizations

### BigQuery Patterns

When adding new patterns to BigQuery skills:

```markdown
### Pattern X: [Clear Name]

**Problem:** Describe the issue this solves

**Solution:**
\`\`\`sql
-- Optimized query
SELECT ...
\`\`\`

**Why it works:** Explain the optimization

**Savings:** Estimated cost/performance improvement
```

### Commit Messages

Use clear, descriptive commit messages:

- `Add: new cost optimization pattern for BigQuery`
- `Fix: typo in installation instructions`
- `Update: BigQuery ML examples with latest API`
- `Docs: improve troubleshooting guide`

## 🧪 Testing

Before submitting:

1. **Test the skill locally**
   ```bash
   cp -r skills/bigquery ~/.claude/skills/
   /bigquery [your test command]
   ```

2. **Verify documentation**
   - Check for typos
   - Ensure links work
   - Test code examples

3. **Review your changes**
   ```bash
   git diff
   ```

## 🐛 Reporting Issues

When reporting issues, include:

- **Description** - What's wrong or what you'd like to see
- **Steps to reproduce** - For bugs, how to recreate the issue
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Environment** - Claude Code version, OS, etc.

**Example:**

```markdown
**Issue:** Query optimization skill doesn't handle CTEs

**Steps:**
1. Run `/bigquery optimize "WITH cte AS (...) SELECT * FROM cte"`
2. Skill doesn't provide CTE-specific optimizations

**Expected:** Should analyze CTE usage and suggest optimizations

**Environment:** Claude Code v1.2.3, Windows 11
```

## 🎓 Development Workflow

### For New Skills

1. **Create skill directory**
   ```bash
   mkdir -p skills/new-skill
   ```

2. **Create SKILL.md**
   - Follow format in existing skills
   - Include purpose, usage, examples
   - Document all sub-skills if applicable

3. **Test thoroughly**
   ```bash
   cp -r skills/new-skill ~/.claude/skills/
   /new-skill test command
   ```

4. **Document in README.md**
   - Add to "Available Skills" section
   - Include brief description

5. **Submit PR**

### For Pattern Updates

1. **Identify the skill** - Which skill needs the pattern?
2. **Add to SKILL.md** - Follow existing pattern format
3. **Include example** - Real-world use case
4. **Document savings** - Performance/cost improvements
5. **Test** - Verify the pattern works

## 📚 Resources

- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Claude Code Documentation](https://github.com/anthropics/claude-code)
- [Skills Development Guide](docs/SKILLS_DEVELOPMENT.md)

## ❓ Questions?

- Open an issue for questions about contributing
- Check existing issues and PRs for similar work
- Review closed PRs for examples of good contributions

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as this project.

---

**Thank you for contributing! 🚀**

Every contribution helps make Claude Code more powerful for everyone.
