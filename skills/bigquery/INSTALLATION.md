# Installation Guide

## Quick Start (5 minutes)

### Step 1: Download Skills

You should already have the `bigquery-skills/` folder.

### Step 2: Choose Installation Method

#### Option A: Claude User Skills Directory (Recommended)

```bash
# Copy to Claude user skills
cp -r bigquery-skills /mnt/skills/user/bigquery

# Verify installation
ls /mnt/skills/user/bigquery/
```

#### Option B: Local Project Directory

```bash
# Create skills directory in your project
mkdir -p ./skills

# Copy skills
cp -r bigquery-skills ./skills/bigquery

# Create .claude configuration file
cat > .claude << 'EOF'
skills:
  - ./skills/bigquery
EOF
```

### Step 3: Verify Installation

Test the skills:

```bash
# From Claude Code or Claude AI chat
/bigquery

# Should show the main skill router with sub-skills listed
```

---

## Detailed Installation

### For Claude Code Users

1. **Navigate to your project:**
   ```bash
   cd /path/to/your/project
   ```

2. **Create skills directory:**
   ```bash
   mkdir -p .claude/skills
   ```

3. **Copy BigQuery skills:**
   ```bash
   cp -r /path/to/bigquery-skills .claude/skills/bigquery
   ```

4. **Create/update .claude file:**
   ```yaml
   # .claude
   skills:
     - .claude/skills/bigquery
   ```

5. **Test installation:**
   ```bash
   claude ask "/bigquery/query-optimization help"
   ```

---

### For Claude AI Web/App Users

BigQuery skills can be accessed directly if placed in:
```
/mnt/skills/user/bigquery/
```

No additional configuration needed.

---

## Directory Structure After Installation

```
your-project/
├── .claude                          # Config file
├── skills/                          # OR .claude/skills/
│   └── bigquery/
│       ├── README.md
│       ├── SKILL.md                 # Main router
│       ├── query-optimization/
│       │   └── SKILL.md
│       ├── data-loading/
│       │   └── SKILL.md
│       ├── bqml/
│       │   └── SKILL.md
│       ├── scheduled-queries/
│       │   └── SKILL.md
│       ├── cost-monitoring/
│       │   └── SKILL.md
│       ├── security/
│       │   └── SKILL.md
│       ├── schema-design/
│       │   └── SKILL.md
│       └── troubleshooting/
│           └── SKILL.md
└── [your project files]
```

---

## Configuration Options

### .claude File Format

```yaml
# .claude
skills:
  - ./skills/bigquery           # Relative path
  # - /absolute/path/to/skills  # OR absolute path
  # - /mnt/skills/user/bigquery # OR system skills path

# Optional: Set default model
model: claude-sonnet-4-5-20250929

# Optional: Custom commands
commands:
  bq-optimize: "Use /bigquery/query-optimization to check this query"
```

---

## Verification Checklist

After installation, verify:

- [ ] Skills directory exists
- [ ] All 8 sub-skill folders present
- [ ] Each folder has SKILL.md file
- [ ] Main SKILL.md in bigquery root
- [ ] README.md accessible
- [ ] .claude file configured (if using local installation)

**Test each sub-skill:**

```bash
# Test main router
/bigquery

# Test each sub-skill
/bigquery/query-optimization
/bigquery/data-loading
/bigquery/bqml
/bigquery/scheduled-queries
/bigquery/cost-monitoring
/bigquery/security
/bigquery/schema-design
/bigquery/troubleshooting
```

---

## Troubleshooting Installation

### Skills Not Found

**Problem:** `/bigquery` returns "skill not found"

**Solutions:**
1. Check path in .claude file is correct
2. Verify SKILL.md exists in bigquery folder
3. Try absolute path instead of relative
4. Restart Claude Code if using CLI

### Permission Issues

**Problem:** Cannot copy to /mnt/skills/user/

**Solution:**
```bash
# Use sudo if needed
sudo cp -r bigquery-skills /mnt/skills/user/bigquery

# Or use local installation instead
```

### Skill Not Loading

**Problem:** Skill loads but commands don't work

**Solutions:**
1. Check SKILL.md file is not corrupted
2. Verify file encoding is UTF-8
3. Check for syntax errors in SKILL.md
4. Review Claude logs for errors

---

## Next Steps

After successful installation:

1. **Read the README:** `cat skills/bigquery/README.md`
2. **Try a simple task:** `/bigquery/query-optimization check my query "SELECT * FROM table"`
3. **Customize skills:** Add your own patterns and examples
4. **Share feedback:** Update skills based on your use cases

---

## Updating Skills

To update to a newer version:

```bash
# Backup current version
cp -r skills/bigquery skills/bigquery.backup

# Copy new version
cp -r bigquery-skills-v2 skills/bigquery

# Test new version
/bigquery

# If issues, restore backup
# rm -rf skills/bigquery && mv skills/bigquery.backup skills/bigquery
```

---

## Uninstallation

To remove skills:

```bash
# Remove from user skills
rm -rf /mnt/skills/user/bigquery

# OR remove from project
rm -rf ./skills/bigquery

# Update .claude file
# Remove the bigquery skills line
```

---

## Support

Having installation issues?

1. Check this guide first
2. Review README.md in bigquery-skills folder
3. Use `/bigquery/troubleshooting` for BigQuery-specific issues
4. Check Claude Code documentation

---

**Installation complete! Start using BigQuery skills now! 🚀**
