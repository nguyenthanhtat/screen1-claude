# screen1-claude

**Development repository for Claude Code skills, commands, and extensions**

Production-ready Claude Code skills that can be easily integrated into any project.

## 🎯 Purpose

Development and testing environment for Claude Code customizations before team-wide deployment.

## 📦 Available Skills

### BigQuery Skill Suite v2.0.0

Comprehensive BigQuery skills covering all major features:

- **query-optimization** - Performance tuning and cost reduction
- **data-loading** - Import/export operations (CSV, JSON, Parquet)
- **bqml** - Machine learning with BigQuery ML
- **scheduled-queries** - ETL automation and orchestration
- **cost-monitoring** - Budget tracking and analysis
- **security** - Row-level security, IAM, access control
- **schema-design** - Table structure optimization with partitioning/clustering
- **troubleshooting** - Debug errors and performance issues

**Features:**
- Auto-routing based on keywords
- Vietnamese market support
- Next.js integration examples
- Multi-tenant patterns
- Production-tested patterns

### Test-Fully Skill v1.0.0

Complete testing solution for any codebase covering unit, integration, E2E, and performance tests:

- **Unit Testing** - Test individual functions/methods in isolation
- **Integration Testing** - Test component interactions, APIs, databases
- **End-to-End Testing** - Test complete user workflows
- **Performance Testing** - Load testing, benchmarks, resource usage
- **Framework Detection** - Auto-detects Jest, pytest, JUnit, Mocha, Vitest, and more
- **Multi-Language Support** - JavaScript/TypeScript, Python, Java, Go, Ruby, C#, PHP, Rust

**Features:**
- Automatic framework detection
- Comprehensive test coverage (happy paths, edge cases, errors)
- Best practices for each language/framework
- Clear, documented test code
- Setup and execution instructions
- Coverage gap identification

**Supported Frameworks:**
- **JavaScript/TypeScript:** Jest, Vitest, Mocha, Jasmine
- **Python:** pytest, unittest, nose2
- **Java:** JUnit 5, JUnit 4, TestNG
- **E2E:** Playwright, Cypress, Selenium, Puppeteer

### Git Skill Suite v1.0.0

Comprehensive Git assistance for all workflows, from basics to advanced operations:

- **basics** - Repository setup, commits, .gitignore, and fundamental workflows
- **branching** - Branch management, merging, rebasing, and branch strategies
- **history** - Commit history, diffs, blame, bisect, and code archaeology
- **remote** - Remote operations, push/pull, multiple remotes, and fork syncing
- **conflicts** - Merge and rebase conflict resolution strategies
- **undo** - Undo changes, reset, revert, and reflog recovery
- **workflows** - GitHub Flow, Git Flow, trunk-based, PR best practices
- **advanced** - Stash, cherry-pick, hooks, submodules, worktrees, LFS

**Features:**
- Auto-routing based on Git keywords
- Beginner to advanced learning path
- Real-world workflows (GitHub Flow, Git Flow, trunk-based)
- Conflict resolution strategies
- Undo and recovery with reflog
- Team collaboration patterns
- Advanced power features

## 🚀 Quick Start for Team Members

### Installation (Simple & Proven to Work!)

**📖 For detailed instructions, see: [TEAM_SETUP.md](TEAM_SETUP.md)**

### Option 1: Marketplace (Easiest!)

Add as a marketplace source in Claude Code:
```
https://github.com/nguyenthanhtat/screen1-claude
```

Then install the skills you want from the marketplace UI.

### Option 2: Automated Scripts

**One-line install (Unix/Mac/Git Bash):**
```bash
git clone https://github.com/nguyenthanhtat/screen1-claude.git ~/claude-skills && cp -r ~/claude-skills/skills/bigquery ~/.claude/skills/ && cp -r ~/claude-skills/skills/test-fully ~/.claude/skills/ && cp -r ~/claude-skills/skills/git ~/.claude/skills/
```

**Automated install scripts:**
```bash
# Unix/Mac/Linux
curl -s https://raw.githubusercontent.com/nguyenthanhtat/screen1-claude/main/install.sh | bash

# Windows PowerShell (run as admin)
iwr -useb https://raw.githubusercontent.com/nguyenthanhtat/screen1-claude/main/install.ps1 | iex
```

**Or step-by-step:**
```bash
# 1. Clone repository
git clone https://github.com/nguyenthanhtat/screen1-claude.git ~/claude-skills

# 2. Copy skills to your Claude directory
cp -r ~/claude-skills/skills/bigquery ~/.claude/skills/
cp -r ~/claude-skills/skills/test-fully ~/.claude/skills/
cp -r ~/claude-skills/skills/git ~/.claude/skills/

# 3. Test in Claude Code
# Run: /bigquery
# Run: /test-fully
# Run: /git
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/nguyenthanhtat/screen1-claude.git $env:USERPROFILE\claude-skills
Copy-Item -Recurse $env:USERPROFILE\claude-skills\skills\bigquery $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse $env:USERPROFILE\claude-skills\skills\test-fully $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse $env:USERPROFILE\claude-skills\skills\git $env:USERPROFILE\.claude\skills\
```

See [INSTALL.md](INSTALL.md) for more installation options.

### Usage

Once installed, use in Claude Code:

**BigQuery Skill:**
```bash
# Auto-routing (recommended)
/bigquery my query is slow
/bigquery load CSV from GCS
/bigquery predict customer churn
/bigquery setup daily ETL at 2am
/bigquery analyze costs by tenant
```

**Test-Fully Skill:**
```bash
# Test specific files
/test-fully src/utils/validator.js
/test-fully app/services/auth.py

# Focus on test types
/test-fully --focus unit
/test-fully --focus integration
/test-fully --focus e2e

# Test entire modules
/test-fully src/features/auth/
```

**Git Skill:**
```bash
# Auto-routing (recommended)
/git how do I commit changes?
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

## 📁 Repository Structure

```
screen1-claude/
├── skills/                    # All skills
│   ├── bigquery/             # BigQuery skill suite
│   │   ├── SKILL.md          # Main router
│   │   ├── README.md         # Usage guide
│   │   ├── DEPLOYMENT.md     # Deployment instructions
│   │   └── [8 sub-skills]/   # Specialized skills
│   ├── test-fully/           # Test-Fully skill
│   │   ├── SKILL.md          # Core testing logic
│   │   ├── README.md         # Usage guide
│   │   ├── QUICK_START.md    # 5-minute getting started
│   │   ├── INSTALLATION.md   # Detailed install guide
│   │   ├── STRUCTURE.md      # Architecture docs
│   │   └── .claude.example   # Config template
│   └── git/                  # Git skill suite
│       ├── SKILL.md          # Main router
│       ├── README.md         # Usage guide
│       ├── QUICK_START.md    # 5-minute getting started
│       ├── INSTALLATION.md   # Detailed install guide
│       ├── STRUCTURE.md      # Architecture docs
│       ├── .claude.example   # Config template
│       └── [8 sub-skills]/   # basics, branching, history, etc.
├── commands/                  # Custom commands (future)
├── tests/                     # Test suite (future)
├── docs/                      # Documentation
│   └── SKILLS_DEVELOPMENT.md # Development guide
├── INSTALL.md                 # Installation guide
├── TEAM_SETUP.md              # Team setup guide
├── install.sh                 # Unix/Mac install script
├── install.ps1                # Windows install script
└── README.md                  # This file
```

## 📖 Documentation

### General
- **[INSTALL.md](INSTALL.md)** - Installation guide for team members
- **[docs/SKILLS_DEVELOPMENT.md](docs/SKILLS_DEVELOPMENT.md)** - How to create and maintain skills

### BigQuery Skill
- **[skills/bigquery/README.md](skills/bigquery/README.md)** - BigQuery skill usage
- **[skills/bigquery/DEPLOYMENT.md](skills/bigquery/DEPLOYMENT.md)** - Deployment instructions

### Test-Fully Skill
- **[skills/test-fully/QUICK_START.md](skills/test-fully/QUICK_START.md)** - Get started in 5 minutes
- **[skills/test-fully/README.md](skills/test-fully/README.md)** - Complete usage guide
- **[skills/test-fully/INSTALLATION.md](skills/test-fully/INSTALLATION.md)** - Installation instructions
- **[skills/test-fully/STRUCTURE.md](skills/test-fully/STRUCTURE.md)** - Architecture and design

### Git Skill
- **[skills/git/QUICK_START.md](skills/git/QUICK_START.md)** - Get started in 5 minutes
- **[skills/git/README.md](skills/git/README.md)** - Complete usage guide
- **[skills/git/INSTALLATION.md](skills/git/INSTALLATION.md)** - Installation instructions
- **[skills/git/STRUCTURE.md](skills/git/STRUCTURE.md)** - Architecture and design

## 🔄 Keeping Skills Updated

```bash
# Update from remote
cd ~/claude-skills
git pull origin master

# Copy updated skills
cp -r skills/bigquery ~/.claude/skills/
cp -r skills/test-fully ~/.claude/skills/
cp -r skills/git ~/.claude/skills/

# Restart Claude Code if needed
```

## 🔧 For Developers

### Local Development

```bash
# Clone the repo
git clone https://github.com/nguyenthanhtat/screen1-claude.git
cd screen1-claude

# Make changes to skills
cd skills/bigquery
# Edit SKILL.md files

# Test locally
cp -r ../bigquery ~/.claude/skills/

# Commit changes
git add .
git commit -m "Update BigQuery skill: description of changes"
git push origin master
```

### Adding New Skills

See [docs/SKILLS_DEVELOPMENT.md](docs/SKILLS_DEVELOPMENT.md) for detailed guide.

## 🌟 Features

- **Production-Ready**: All skills tested in real-world scenarios
- **Well-Documented**: Comprehensive guides and examples
- **Easy Integration**: Multiple installation options
- **Version Controlled**: Track changes and updates
- **Team-Friendly**: Easy for multiple developers to use

## 📋 Requirements

- Claude Code CLI installed
- Git for version control
- Access to this repository

## 🤝 Contributing

### Suggesting Improvements

1. Test the skill in your environment
2. Document issues or improvements needed
3. Create an issue or submit a pull request
4. Include examples and use cases

### Sharing New Patterns

If you discover useful patterns:

1. Update the relevant SKILL.md file
2. Add your example with explanation
3. Test thoroughly
4. Submit a pull request

## 📝 Version History

### v1.2.0 (2025-02-11)
- Added Git Skill Suite v1.0.0
  - 8 specialized sub-skills for Git operations
  - Comprehensive patterns for all Git workflows
  - Beginner to advanced learning path
  - Team collaboration best practices
  - Conflict resolution strategies
  - Undo and recovery with reflog
  - Advanced operations (stash, cherry-pick, hooks, worktrees)
  - Complete documentation suite

### v1.1.0 (2025-02-10)
- Added Test-Fully Skill v1.0.0
  - Comprehensive testing for all major languages
  - Unit, integration, E2E, and performance testing
  - Auto-detects testing frameworks
  - Multi-language support (JavaScript, Python, Java, etc.)
  - Complete documentation suite

### v1.0.0 (2024-02-09)
- Initial repository setup
- BigQuery Skill Suite v2.0.0
  - 8 comprehensive sub-skills
  - Auto-routing capability
  - Vietnamese market support
  - Production patterns

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Summary:** Free to use and modify for personal and commercial projects.

## 🆘 Support

**For Skill Usage Questions:**
- BigQuery: Check `skills/bigquery/README.md` or use `/bigquery/troubleshooting`
- Test-Fully: Check `skills/test-fully/README.md` or `skills/test-fully/QUICK_START.md`
- Git: Check `skills/git/README.md` or `skills/git/QUICK_START.md`
- General: Review `docs/SKILLS_DEVELOPMENT.md`

**For Repository Issues:**
- Check existing issues on GitHub
- Create new issue with details
- Include Claude Code version and error messages

## 🔗 Links

- **Claude Code**: https://github.com/anthropics/claude-code
- **BigQuery Documentation**: https://cloud.google.com/bigquery/docs

---

**Made with ❤️ for the Claude Code community**

Start using professional Claude Code skills in minutes! 🚀
