# Installation Guide for Team Members

Quick guide for installing skills from this repository.

## Prerequisites

- Claude Code installed and working
- Git installed
- Command line access (bash/zsh/PowerShell)

## Installation Methods

Choose the method that works best for you:

---

## Method 1: Quick Install (Fastest) ⚡

**Best for:** Quick testing or one-time use

```bash
# 1. Clone repository to a temporary location
git clone https://github.com/nguyenthanhtat/screen1-claude.git /tmp/claude-skills-temp

# 2. Copy skills to your Claude directory
# Install BigQuery skill
cp -r /tmp/claude-skills-temp/skills/bigquery ~/.claude/skills/

# Install Test-Fully skill
cp -r /tmp/claude-skills-temp/skills/test-fully ~/.claude/skills/

# 3. Clean up
rm -rf /tmp/claude-skills-temp

# 4. Verify installation
ls ~/.claude/skills/bigquery/
ls ~/.claude/skills/test-fully/

# 5. Test in Claude Code
# Run: /bigquery
# Run: /test-fully
```

**Windows (PowerShell):**
```powershell
# 1. Clone repository
git clone https://github.com/nguyenthanhtat/screen1-claude.git $env:TEMP\claude-skills-temp

# 2. Copy skills
Copy-Item -Recurse $env:TEMP\claude-skills-temp\skills\bigquery $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse $env:TEMP\claude-skills-temp\skills\test-fully $env:USERPROFILE\.claude\skills\

# 3. Clean up
Remove-Item -Recurse $env:TEMP\claude-skills-temp

# 4. Test
# Run: /bigquery
# Run: /test-fully
```

---

## Method 2: Persistent Clone (Recommended) 🎯

**Best for:** Regular updates and development

```bash
# 1. Clone to a permanent location
mkdir -p ~/Development
git clone https://github.com/nguyenthanhtat/screen1-claude.git ~/Development/screen1-claude

# 2. Create symlink (Linux/Mac) or copy (Windows)
# Linux/Mac - Using symlinks:
ln -s ~/Development/screen1-claude/skills/bigquery ~/.claude/skills/bigquery
ln -s ~/Development/screen1-claude/skills/test-fully ~/.claude/skills/test-fully

# Windows (run as Administrator):
# mklink /D "%USERPROFILE%\.claude\skills\bigquery" "%USERPROFILE%\Development\screen1-claude\skills\bigquery"
# mklink /D "%USERPROFILE%\.claude\skills\test-fully" "%USERPROFILE%\Development\screen1-claude\skills\test-fully"

# OR just copy (all platforms):
cp -r ~/Development/screen1-claude/skills/bigquery ~/.claude/skills/
cp -r ~/Development/screen1-claude/skills/test-fully ~/.claude/skills/

# 3. Test
# Run: /bigquery
# Run: /test-fully
```

**To update later:**
```bash
# Pull latest changes
cd ~/Development/screen1-claude
git pull origin master

# Recopy if not using symlink
cp -r skills/bigquery ~/.claude/skills/
cp -r skills/test-fully ~/.claude/skills/
```

---

## Method 3: Project-Specific Installation 📂

**Best for:** Using skills only in specific projects

```bash
# 1. Navigate to your project
cd /path/to/your/project

# 2. Clone skills repo
git clone https://github.com/nguyenthanhtat/screen1-claude.git .claude-skills

# 3. Create .claude config file
cat > .claude << 'EOF'
skills:
  - ./.claude-skills/skills/bigquery
  - ./.claude-skills/skills/test-fully
EOF

# 4. Test (must be in project directory)
# Run: /bigquery
# Run: /test-fully
```

**To update:**
```bash
cd /path/to/your/project/.claude-skills
git pull origin master
```

---

## Method 4: Git Submodule (Advanced) 🔧

**Best for:** Projects tracked in Git with multiple developers

```bash
# 1. Navigate to your project
cd /path/to/your/project

# 2. Add as submodule
git submodule add https://github.com/nguyenthanhtat/screen1-claude.git .claude-skills

# 3. Copy skills to user directory
cp -r .claude-skills/skills/bigquery ~/.claude/skills/
cp -r .claude-skills/skills/test-fully ~/.claude/skills/

# 4. Commit submodule
git commit -m "Add Claude skills submodule"

# 5. Push
git push
```

**For other team members:**
```bash
# Clone your project
git clone <YOUR_PROJECT_URL>
cd your-project

# Initialize submodules
git submodule init
git submodule update

# Copy skills
cp -r .claude-skills/skills/bigquery ~/.claude/skills/
cp -r .claude-skills/skills/test-fully ~/.claude/skills/
```

**To update:**
```bash
# Update submodule
git submodule update --remote

# Recopy skills
cp -r .claude-skills/skills/bigquery ~/.claude/skills/
cp -r .claude-skills/skills/test-fully ~/.claude/skills/

# Commit update
git add .claude-skills
git commit -m "Update Claude skills"
```

---

## Verification

After installation, verify it works:

```bash
# Check files exist
ls ~/.claude/skills/bigquery/
ls ~/.claude/skills/test-fully/

# BigQuery should show:
# SKILL.md, README.md, DEPLOYMENT.md, and sub-skill directories

# Test-Fully should show:
# SKILL.md, README.md, QUICK_START.md, INSTALLATION.md, STRUCTURE.md, .claude.example

# Test in Claude Code
# Open Claude Code and type: /bigquery
# Should display skill information and sub-skills

# Test Test-Fully skill
# Type: /test-fully
# Should activate the testing skill
```

---

## Troubleshooting

### Skill Not Found

**Symptom:** `/bigquery` or `/test-fully` returns "Unknown skill"

**Solutions:**
1. Verify installation path:
   ```bash
   ls ~/.claude/skills/bigquery/SKILL.md
   ls ~/.claude/skills/test-fully/SKILL.md
   ```

2. Check file exists and has content:
   ```bash
   head ~/.claude/skills/bigquery/SKILL.md
   head ~/.claude/skills/test-fully/SKILL.md
   ```

3. Restart Claude Code

4. Check Claude Code logs for errors

### Permission Denied (Linux/Mac)

```bash
# Fix permissions for all skills
chmod -R 755 ~/.claude/skills/
```

### Symlink Doesn't Work (Windows)

On Windows, symlinks require admin privileges. Use **copy** method instead:

```powershell
Copy-Item -Recurse source-path $env:USERPROFILE\.claude\skills\
```

### Git Clone Fails

**Check:**
1. Repository URL is correct
2. You have access to the repository
3. Git is installed: `git --version`
4. SSH key is configured (if using SSH URL)

---

## Platform-Specific Notes

### Windows

- Use PowerShell or Git Bash
- Paths use backslashes: `C:\Users\username\.claude\skills\`
- Symlinks require Administrator privileges
- Recommend using **copy** method

### macOS

- Claude directory: `~/.claude/skills/`
- Symlinks work without admin
- Use Terminal or iTerm

### Linux

- Claude directory: `~/.claude/skills/`
- Symlinks work without root
- Works on all distributions

---

## Quick Reference

| Method | Speed | Updates | Best For |
|--------|-------|---------|----------|
| Quick Install | ⚡⚡⚡ | Manual | Testing |
| Persistent Clone | ⚡⚡ | Easy | Regular use |
| Project-Specific | ⚡⚡ | Easy | Single project |
| Git Submodule | ⚡ | Automatic | Team development |

---

## Getting Help

1. Check [README.md](README.md) for overview
2. Review skill documentation:
   - [BigQuery README](skills/bigquery/README.md) for BigQuery usage
   - [Test-Fully Quick Start](skills/test-fully/QUICK_START.md) for testing
3. See [SKILLS_DEVELOPMENT.md](docs/SKILLS_DEVELOPMENT.md) for development
4. Open issue on GitHub
5. Ask in your team chat

---

## Next Steps

After installation:

**For BigQuery:**
1. **Test the skill:** `/bigquery`
2. **Try optimization:** `/bigquery optimize my query "SELECT ..."`
3. **Read documentation:** `skills/bigquery/README.md`
4. **Explore sub-skills:** Try each specialized skill

**For Test-Fully:**
1. **Test the skill:** `/test-fully`
2. **Quick start:** Read `skills/test-fully/QUICK_START.md`
3. **Generate tests:** `/test-fully path/to/your/code.js`
4. **Try focused testing:** `/test-fully --focus unit`

**General:**
- **Share feedback:** Report issues or improvements
- **Customize:** Edit SKILL.md files for your team's needs
- **Stay updated:** Pull latest changes regularly

---

**Installation complete! Start using professional Claude Code skills now! 🚀**
