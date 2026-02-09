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

## 🚀 Quick Start for Team Members

### Installation

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

**Quick install:**

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/screen1-claude.git ~/claude-skills

# Copy BigQuery skill to your Claude directory
cp -r ~/claude-skills/skills/bigquery ~/.claude/skills/

# Test in Claude Code
# Run: /bigquery
```

### Usage

Once installed, use in Claude Code:

```bash
# Auto-routing (recommended)
/bigquery my query is slow
/bigquery load CSV from GCS
/bigquery predict customer churn
/bigquery setup daily ETL at 2am
/bigquery analyze costs by tenant
```

## 📁 Repository Structure

```
screen1-claude/
├── skills/                    # All skills
│   └── bigquery/             # BigQuery skill suite
│       ├── SKILL.md          # Main router
│       ├── README.md         # Usage guide
│       ├── DEPLOYMENT.md     # Deployment instructions
│       └── [8 sub-skills]/   # Specialized skills
├── commands/                  # Custom commands (future)
├── tests/                     # Test suite (future)
├── docs/                      # Documentation
│   └── SKILLS_DEVELOPMENT.md # Development guide
├── INSTALL.md                 # Installation guide
└── README.md                  # This file
```

## 📖 Documentation

- **[INSTALL.md](INSTALL.md)** - Installation guide for team members
- **[docs/SKILLS_DEVELOPMENT.md](docs/SKILLS_DEVELOPMENT.md)** - How to create and maintain skills
- **[skills/bigquery/README.md](skills/bigquery/README.md)** - BigQuery skill usage
- **[skills/bigquery/DEPLOYMENT.md](skills/bigquery/DEPLOYMENT.md)** - Deployment instructions

## 🔄 Keeping Skills Updated

```bash
# Update from remote
cd ~/claude-skills
git pull origin master

# Copy updated skills
cp -r skills/bigquery ~/.claude/skills/

# Restart Claude Code if needed
```

## 🔧 For Developers

### Local Development

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/screen1-claude.git
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

### v1.0.0 (2024-02-09)
- Initial repository setup
- BigQuery Skill Suite v2.0.0
  - 8 comprehensive sub-skills
  - Auto-routing capability
  - Vietnamese market support
  - Production patterns

## 📄 License

Free to use and modify for personal and commercial projects.

## 🆘 Support

**For Skill Usage Questions:**
- Check skill documentation in `skills/bigquery/README.md`
- Use `/bigquery/troubleshooting` for BigQuery issues
- Review `docs/SKILLS_DEVELOPMENT.md`

**For Repository Issues:**
- Check existing issues on GitHub
- Create new issue with details
- Include Claude Code version and error messages

## 🔗 Links

- **Claude Code**: https://github.com/anthropics/claude-code
- **BigQuery Documentation**: https://cloud.google.com/bigquery/docs

---

**Made with ❤️ for the Claude Code community**

Start using professional BigQuery skills in minutes! 🚀
