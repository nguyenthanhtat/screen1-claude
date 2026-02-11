# Skills Directory

Custom Claude Code skills for extended functionality.

---

## What are Skills?

Skills are specialized instructions that Claude can follow when users request specific actions. They appear as slash commands (e.g., `/bigquery`, `/test-fully`) and provide Claude with detailed knowledge about how to perform specific tasks.

### How Skills Work

1. **Skills are markdown files** - Written in plain markdown with instructions for Claude
2. **Invoked with slash commands** - Users type `/skill-name` to activate
3. **Context-aware** - Skills can analyze code, detect frameworks, and adapt behavior
4. **Composable** - Multiple skills can be used together in workflows

---

## Available Skills

### 🧪 test-fully v1.0.0

**Complete testing solution for any codebase**

Generates comprehensive test suites covering unit, integration, E2E, and performance testing. Automatically detects testing frameworks and follows best practices for each language.

#### Features
- ✅ **Automatic framework detection** - Jest, pytest, JUnit, Mocha, Vitest, and more
- ✅ **Multi-language support** - JavaScript/TypeScript, Python, Java, Go, Ruby, C#, PHP, Rust
- ✅ **Comprehensive coverage** - Happy paths, edge cases, error conditions, boundary values
- ✅ **Production-ready** - Follows framework best practices, includes setup/teardown
- ✅ **Clear documentation** - Generated tests include helpful comments
- ✅ **Multiple test types** - Unit, integration, E2E, performance

#### Supported Frameworks

**JavaScript/TypeScript:**
- Jest (React, Node.js, Next.js)
- Vitest (Vite projects)
- Mocha + Chai
- Jasmine

**Python:**
- pytest (recommended)
- unittest (standard library)
- nose2

**Java:**
- JUnit 5 (Jupiter)
- JUnit 4 (Vintage)
- TestNG

**E2E Testing:**
- Playwright (cross-browser)
- Cypress (developer-friendly)
- Selenium (industry standard)
- Puppeteer (Chrome automation)

**Other Languages:**
- Go (testing package)
- Ruby (RSpec, Minitest)
- C# (xUnit, NUnit, MSTest)
- PHP (PHPUnit)
- Rust (built-in tests)

#### Usage Examples

```bash
# Test specific file
/test-fully src/utils/validator.js

# Focus on test type
/test-fully --focus unit
/test-fully --focus integration
/test-fully --focus e2e
/test-fully --focus performance

# Test entire module
/test-fully src/features/auth/

# Update existing tests
/test-fully update tests for payment.js
/test-fully improve coverage for api.py
```

#### Documentation
- **[QUICK_START.md](test-fully/QUICK_START.md)** - Get started in 5 minutes
- **[README.md](test-fully/README.md)** - Complete usage guide with examples
- **[INSTALLATION.md](test-fully/INSTALLATION.md)** - Detailed installation instructions
- **[STRUCTURE.md](test-fully/STRUCTURE.md)** - Architecture and design decisions
- **[.claude.example](test-fully/.claude.example)** - Configuration template

#### Example Output

**Input:**
```bash
/test-fully src/utils/formatCurrency.js
```

**Generated Test:**
```javascript
describe('formatCurrency', () => {
  test('should format positive numbers with commas and decimals', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56');
  });

  test('should handle zero', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });

  test('should handle negative numbers', () => {
    expect(formatCurrency(-100)).toBe('-$100.00');
  });

  test('should throw TypeError for non-numeric input', () => {
    expect(() => formatCurrency('invalid')).toThrow(TypeError);
  });

  test('should round to 2 decimal places', () => {
    expect(formatCurrency(10.999)).toBe('$11.00');
  });
});
```

---

### 📊 bigquery v2.0.0

**Comprehensive BigQuery development assistance**

Complete BigQuery skill suite with 8 specialized sub-skills covering optimization, data loading, ML, security, and more. Perfect for data engineers and analysts working with Google BigQuery.

#### Sub-Skills
- **query-optimization** - Performance tuning and cost reduction
- **data-loading** - Import/export operations (CSV, JSON, Parquet)
- **bqml** - Machine learning with BigQuery ML
- **scheduled-queries** - ETL automation and orchestration
- **cost-monitoring** - Budget tracking and analysis
- **security** - Row-level security, IAM, access control
- **schema-design** - Table structure optimization with partitioning/clustering
- **troubleshooting** - Debug errors and performance issues

#### Features
- Auto-routing based on keywords
- Vietnamese market support (UTF-8, timezones)
- Next.js integration examples
- Multi-tenant patterns
- Production-tested patterns

#### Usage Examples

```bash
# Auto-routing (Claude decides which sub-skill)
/bigquery my query is slow
/bigquery load CSV from GCS
/bigquery predict customer churn

# Direct sub-skill access
/bigquery/query-optimization check my query "SELECT ..."
/bigquery/data-loading import CSV from gs://bucket/file.csv
/bigquery/bqml create prediction model
/bigquery/cost-monitoring show expensive queries
```

#### Documentation
- **[README.md](bigquery/README.md)** - Complete usage guide
- **[QUICK_START.md](bigquery/QUICK_START.md)** - Get started quickly
- **[INSTALLATION.md](bigquery/INSTALLATION.md)** - Installation instructions
- **[STRUCTURE.md](bigquery/STRUCTURE.md)** - Architecture overview
- **[DEPLOYMENT.md](bigquery/DEPLOYMENT.md)** - Deployment guide

---

### 🔧 git v1.0.0

**Comprehensive Git assistance for all workflows**

Complete Git skill suite with 8 specialized sub-skills covering everything from basics to advanced operations. Perfect for developers of all skill levels learning or mastering Git.

#### Sub-Skills
- **basics** - Repository setup, commits, .gitignore, and fundamental workflows
- **branching** - Branch management, merging, rebasing, and branch strategies
- **history** - Commit history, diffs, blame, bisect, and code archaeology
- **remote** - Remote operations, push/pull, multiple remotes, and fork syncing
- **conflicts** - Merge and rebase conflict resolution strategies
- **undo** - Undo changes, reset, revert, and reflog recovery
- **workflows** - GitHub Flow, Git Flow, trunk-based, PR best practices
- **advanced** - Stash, cherry-pick, hooks, submodules, worktrees, LFS

#### Features
- Auto-routing based on Git keywords
- Beginner to advanced learning path
- Real-world workflows (GitHub Flow, Git Flow, trunk-based)
- Conflict resolution strategies
- Undo and recovery with reflog
- Team collaboration patterns
- Advanced power features

#### Usage Examples

```bash
# Auto-routing (Claude decides which sub-skill)
/git how do I commit changes
/git create a feature branch
/git I have a merge conflict
/git undo my last commit

# Direct sub-skill access
/git/basics help me make first commit
/git/branching create and merge feature branch
/git/conflicts resolve merge conflict
/git/undo fix my commit message
/git/workflows explain GitHub Flow
/git/advanced stash my changes
```

#### Documentation
- **[QUICK_START.md](git/QUICK_START.md)** - Get started in 5 minutes
- **[README.md](git/README.md)** - Complete usage guide
- **[INSTALLATION.md](git/INSTALLATION.md)** - Installation instructions
- **[STRUCTURE.md](git/STRUCTURE.md)** - Architecture overview

---

## Installation

### Quick Install

```bash
# Clone repository
git clone https://github.com/nguyenthanhtat/screen1-claude.git ~/claude-skills

# Copy skills to Claude directory
cp -r ~/claude-skills/skills/bigquery ~/.claude/skills/
cp -r ~/claude-skills/skills/test-fully ~/.claude/skills/
cp -r ~/claude-skills/skills/git ~/.claude/skills/

# Verify installation
ls ~/.claude/skills/bigquery/SKILL.md
ls ~/.claude/skills/test-fully/SKILL.md
ls ~/.claude/skills/git/SKILL.md

# Test in Claude Code
# Run: /bigquery
# Run: /test-fully
# Run: /git
```

See [../INSTALL.md](../INSTALL.md) for detailed installation instructions.

---

## Creating New Skills

### Skill Structure

```
your-skill/
├── SKILL.md              # Main skill logic (required)
├── README.md             # Usage documentation
├── QUICK_START.md        # Quick start guide
├── INSTALLATION.md       # Installation instructions
├── STRUCTURE.md          # Architecture documentation
└── .claude.example       # Configuration template
```

### Basic SKILL.md Template

```markdown
# Your Skill Name

## Purpose
Brief description of what this skill does.

## How to Use This Skill

```bash
/your-skill [arguments]
```

## Instructions

When this skill is invoked:

1. **Step 1** - What to do first
2. **Step 2** - What to do next
3. **Step 3** - Final step

## Examples

### Example 1
```bash
/your-skill example input
```

Output: What user should expect

---

Now, please help me with:
```

### Best Practices

1. **Be specific** - Provide detailed instructions and examples
2. **Use patterns** - Show good and bad examples
3. **Add context** - Explain why, not just what
4. **Include edge cases** - Cover error scenarios
5. **Keep it organized** - Use clear headings and structure
6. **Add documentation** - Create README, QUICK_START, etc.
7. **Test thoroughly** - Verify skill works as expected

See [../docs/SKILLS_DEVELOPMENT.md](../docs/SKILLS_DEVELOPMENT.md) for detailed guide.

---

## Skill Workflows

### Example: Complete Testing Workflow

```bash
# 1. Generate tests
/test-fully src/api/users.js

# 2. Review generated tests (Claude writes them)
# 3. Run tests to verify they work
npm test

# 4. Improve coverage if needed
/test-fully improve coverage for users.js
```

### Example: BigQuery + Testing

```bash
# 1. Optimize BigQuery query
/bigquery/query-optimization optimize my query "SELECT ..."

# 2. Test the optimized query
/test-fully test query logic

# 3. Set up cost monitoring
/bigquery/cost-monitoring track this query
```

---

## Configuration

### Global Configuration (~/.claude/.claude)

```yaml
skills:
  - /Users/username/.claude/skills/bigquery
  - /Users/username/.claude/skills/test-fully
  - /Users/username/.claude/skills/git
```

### Project Configuration (.claude)

```yaml
# .claude file in your project root
skills:
  - ./skills/bigquery
  - ./skills/test-fully
  - ./skills/git

# Optional shortcuts
commands:
  test: "Use /test-fully for comprehensive testing"
  bq: "Use /bigquery for BigQuery tasks"
  g: "Use /git for Git operations"
```

---

## Troubleshooting

### Skill Not Found

```bash
# Check installation
ls ~/.claude/skills/skill-name/SKILL.md

# Verify SKILL.md exists and is readable
cat ~/.claude/skills/skill-name/SKILL.md

# Restart Claude Code
```

### Skill Not Working as Expected

1. Read the skill's README.md for usage instructions
2. Check examples in QUICK_START.md
3. Verify you're using correct syntax
4. Review STRUCTURE.md for how the skill works

---

## Support

- **General:** See [../README.md](../README.md)
- **Installation:** See [../INSTALL.md](../INSTALL.md)
- **Development:** See [../docs/SKILLS_DEVELOPMENT.md](../docs/SKILLS_DEVELOPMENT.md)
- **BigQuery:** See [bigquery/README.md](bigquery/README.md)
- **Test-Fully:** See [test-fully/README.md](test-fully/README.md)
- **Git:** See [git/README.md](git/README.md)

---

## Contributing

To contribute a new skill or improve existing ones:

1. Follow the skill structure guidelines above
2. Include comprehensive documentation
3. Test thoroughly with real use cases
4. Submit a pull request with examples
5. Update this README.md to list your skill

---

**Explore the skills directories for detailed documentation and examples! 🚀**
