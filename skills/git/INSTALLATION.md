# Git Skill Suite - Installation Guide

Complete installation instructions for all platforms.

## Prerequisites

### Required
- ✅ Git 2.30 or later installed
- ✅ Claude Code CLI or Claude AI access
- ✅ Skills directory (will be created if needed)

### Check Git Installation

```bash
# Verify Git is installed
git --version

# Should show: git version 2.30.0 or higher
```

If Git is not installed:
- **macOS:** `brew install git`
- **Ubuntu/Debian:** `sudo apt-get install git`
- **Windows:** Download from [git-scm.com](https://git-scm.com/)

## Installation Methods

### Method 1: Quick Install (Recommended)

**Linux / macOS:**
```bash
# Copy to Claude skills directory
cp -r skills/git ~/.claude/skills/git
```

**Windows (PowerShell):**
```powershell
Copy-Item -Recurse skills\git $env:USERPROFILE\.claude\skills\git
```

**Windows (Command Prompt):**
```cmd
xcopy /E /I skills\git %USERPROFILE%\.claude\skills\git
```

### Method 2: Manual Installation

**Step 1: Create skills directory**
```bash
# Linux / macOS
mkdir -p ~/.claude/skills

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.claude\skills
```

**Step 2: Copy skill files**
```bash
# Linux / macOS
cp -r skills/git ~/.claude/skills/git

# Windows (PowerShell)
Copy-Item -Recurse skills\git $env:USERPROFILE\.claude\skills\git
```

**Step 3: Verify installation**
```bash
# Linux / macOS
ls ~/.claude/skills/git

# Windows (PowerShell)
Get-ChildItem $env:USERPROFILE\.claude\skills\git
```

You should see:
```
SKILL.md
README.md
QUICK_START.md
INSTALLATION.md
STRUCTURE.md
.claude.example
basics/
branching/
history/
remote/
conflicts/
undo/
workflows/
advanced/
```

### Method 3: Using Team Installation Scripts

If you're using the screen1-claude repository:

**Linux / macOS:**
```bash
# From repository root
./install.sh
```

**Windows (PowerShell):**
```powershell
# From repository root
.\install.ps1
```

These scripts install all skills (BigQuery, Test-Fully, and Git).

## Configuration

### Optional: Add Shortcuts

Copy the example configuration:

**Linux / macOS:**
```bash
cp ~/.claude/skills/git/.claude.example ~/.claude/.claude
```

**Windows (PowerShell):**
```powershell
Copy-Item $env:USERPROFILE\.claude\skills\git\.claude.example $env:USERPROFILE\.claude\.claude
```

Or add to your existing `.claude` file:
```yaml
skills:
  - ~/.claude/skills/git

# Optional shortcuts (customize as needed)
commands:
  gcommit: "Use /git/basics for commit workflow"
  gbranch: "Use /git/branching for branch operations"
  gmerge: "Use /git/branching to merge branches"
  gconflict: "Use /git/conflicts to resolve conflicts"
  gundo: "Use /git/undo to undo changes"
  glog: "Use /git/history to view commit history"
```

## Verification

### Test the Installation

**1. Basic skill access:**
```bash
# Try the main skill
/git

# Should show Git skill router information
```

**2. Test sub-skills:**
```bash
# Try specific sub-skills
/git/basics
/git/branching
/git/undo

# Each should load successfully
```

**3. Test auto-routing:**
```bash
# Ask a Git question
/git how do I commit changes

# Should route to /git/basics automatically
```

**4. Test with actual Git question:**
```bash
# Ask about a specific operation
/git help me create a branch
/git I have a merge conflict
/git undo my last commit

# Should provide relevant help
```

## Troubleshooting

### Skill Not Found

**Error:** "Skill not found: /git"

**Solution:**
```bash
# Check if skill is in correct location
ls ~/.claude/skills/git/SKILL.md

# If not, copy again
cp -r skills/git ~/.claude/skills/git
```

### Permission Issues (Linux/macOS)

**Error:** Permission denied

**Solution:**
```bash
# Fix permissions
chmod -R 755 ~/.claude/skills/git
```

### Path Issues (Windows)

**Error:** Can't find skills directory

**Solution:**
```powershell
# Verify path
Write-Host $env:USERPROFILE\.claude\skills\git

# Create directory structure if needed
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.claude\skills\git
```

### Skill Loads But Doesn't Work

**Issue:** Skill shows but doesn't respond

**Solution:**
1. Check Git is installed: `git --version`
2. Verify SKILL.md exists: `cat ~/.claude/skills/git/SKILL.md`
3. Check sub-skill files exist: `ls ~/.claude/skills/git/*/SKILL.md`

## Updating

### Update to Latest Version

```bash
# Linux / macOS
rm -rf ~/.claude/skills/git
cp -r skills/git ~/.claude/skills/git

# Windows (PowerShell)
Remove-Item -Recurse -Force $env:USERPROFILE\.claude\skills\git
Copy-Item -Recurse skills\git $env:USERPROFILE\.claude\skills\git
```

### Check Version

The version is listed at the top of `SKILL.md`:
```bash
# View version
grep "Version:" ~/.claude/skills/git/SKILL.md
```

## Uninstallation

### Remove Skill

**Linux / macOS:**
```bash
rm -rf ~/.claude/skills/git
```

**Windows (PowerShell):**
```powershell
Remove-Item -Recurse -Force $env:USERPROFILE\.claude\skills\git
```

### Remove Configuration

Remove from `.claude` file if you added custom configuration.

## Platform-Specific Notes

### macOS

- Default location: `~/.claude/skills/git`
- Works with zsh and bash
- Homebrew Git recommended: `brew install git`

### Linux

- Default location: `~/.claude/skills/git`
- Works with all distributions
- Use package manager: `apt-get install git` or `yum install git`

### Windows

- Default location: `%USERPROFILE%\.claude\skills\git`
- Works with PowerShell, Command Prompt, and Git Bash
- Git for Windows recommended: [git-scm.com](https://git-scm.com/)
- Path separator: use `\` in Windows paths

### WSL (Windows Subsystem for Linux)

- Use Linux instructions
- Location: `/home/username/.claude/skills/git`
- Works like native Linux

## Advanced Installation

### Custom Skills Directory

If you use a custom skills directory:

```bash
# Set custom location
export CLAUDE_SKILLS_DIR=/custom/path

# Copy to custom location
cp -r skills/git $CLAUDE_SKILLS_DIR/git
```

Configure in `.claude`:
```yaml
skills:
  - /custom/path/git
```

### Project-Specific Installation

For project-specific skills:

```bash
# Copy to project
cp -r skills/git ./claude-skills/git

# Configure in project .claude file
echo "skills:" > .claude
echo "  - ./claude-skills/git" >> .claude
```

### Multiple Installations

You can have multiple versions:

```bash
# User-level (default)
~/.claude/skills/git

# Project-level (overrides user)
./claude-skills/git
```

Claude uses project-level if it exists, otherwise user-level.

## Integration with Other Tools

### VS Code

If using Claude Code in VS Code, the skill is automatically available once installed in `~/.claude/skills/`.

### Terminal

Works in any terminal where Claude Code CLI is installed.

### CI/CD

For CI/CD environments:
```bash
# Install in CI pipeline
mkdir -p ~/.claude/skills
cp -r skills/git ~/.claude/skills/git
```

## Next Steps

After installation:

1. **Quick Start:** Read `QUICK_START.md`
2. **Documentation:** Check `README.md`
3. **Architecture:** Review `STRUCTURE.md`
4. **Try It:** Run `/git help me commit changes`

## Getting Help

**Installation issues:**
1. Check Git is installed: `git --version`
2. Verify file location: `ls ~/.claude/skills/git`
3. Check permissions: `ls -la ~/.claude/skills/git`
4. Review error messages

**Still having issues?**
- Check Claude Code documentation
- Verify Claude Code is properly configured
- Test with other skills to isolate issue

## Support

For Git skill-specific issues:
- Review `README.md` for usage
- Check `TROUBLESHOOTING.md` if available
- Consult Claude Code documentation

---

**Installation complete?** Start with `/git` or read `QUICK_START.md`!
