# Installation Guide - Test-Fully Skill

## Quick Start (5 minutes)

### Step 1: Locate the Skill

You should have the `test-fully/` folder from the screen1-claude repository.

### Step 2: Choose Installation Method

Pick the method that best fits your workflow:

---

## Installation Methods

### Method 1: Quick Install (Recommended for Single User)

**For Windows (PowerShell):**
```powershell
# Copy to Claude user skills directory
Copy-Item -Recurse -Path ".\screen1-claude\skills\test-fully" -Destination "$env:USERPROFILE\.claude\skills\test-fully"

# Verify installation
dir "$env:USERPROFILE\.claude\skills\test-fully\SKILL.md"
```

**For macOS/Linux (Bash):**
```bash
# Copy to Claude user skills directory
cp -r ./screen1-claude/skills/test-fully ~/.claude/skills/

# Verify installation
ls ~/.claude/skills/test-fully/SKILL.md
```

**Pros:**
- Available globally in all projects
- One-time setup
- No per-project configuration

**Cons:**
- Updates require manual copying
- Same version across all projects

---

### Method 2: Persistent Clone (Recommended for Teams)

**For Windows (PowerShell):**
```powershell
# Clone repository to a permanent location
git clone https://github.com/nguyenthanhtat/screen1-claude.git "$env:USERPROFILE\.claude\repos\screen1-claude"

# Create symlink to skills directory
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\test-fully" -Target "$env:USERPROFILE\.claude\repos\screen1-claude\skills\test-fully"

# Update later with git pull
cd "$env:USERPROFILE\.claude\repos\screen1-claude"
git pull
```

**For macOS/Linux (Bash):**
```bash
# Clone repository to a permanent location
git clone https://github.com/nguyenthanhtat/screen1-claude.git ~/.claude/repos/screen1-claude

# Create symlink to skills directory
ln -s ~/.claude/repos/screen1-claude/skills/test-fully ~/.claude/skills/test-fully

# Update later with git pull
cd ~/.claude/repos/screen1-claude
git pull
```

**Pros:**
- Easy updates with `git pull`
- Version controlled
- Team can share improvements

**Cons:**
- Requires git knowledge
- Slightly more complex setup

---

### Method 3: Project-Specific (Best for Different Versions per Project)

**For Windows (PowerShell):**
```powershell
# Navigate to your project
cd D:\MyProject

# Create skills directory
New-Item -ItemType Directory -Path ".\skills" -Force

# Copy test-fully skill
Copy-Item -Recurse -Path "D:\Screen1\screen1-claude\skills\test-fully" -Destination ".\skills\test-fully"

# Create .claude configuration file
@"
skills:
  - ./skills/test-fully
"@ | Out-File -FilePath ".\.claude" -Encoding UTF8
```

**For macOS/Linux (Bash):**
```bash
# Navigate to your project
cd ~/my-project

# Create skills directory
mkdir -p ./skills

# Copy test-fully skill
cp -r ~/screen1-claude/skills/test-fully ./skills/

# Create .claude configuration file
cat > .claude << 'EOF'
skills:
  - ./skills/test-fully
EOF
```

**Pros:**
- Different skill versions per project
- Project-specific customization
- Easy to version control with project

**Cons:**
- Must install for each project
- Updates require manual copying per project

---

### Method 4: Git Submodule (For Advanced Teams)

**For Windows (PowerShell) and macOS/Linux (Bash):**
```bash
# Navigate to your project (must be a git repository)
cd /path/to/your-project

# Add screen1-claude as a submodule
git submodule add https://github.com/nguyenthanhtat/screen1-claude.git .claude/screen1-claude

# Initialize submodule
git submodule update --init --recursive

# Create .claude configuration
cat > .claude << 'EOF'
skills:
  - ./.claude/screen1-claude/skills/test-fully
EOF

# Update later
git submodule update --remote
```

**Pros:**
- Proper version tracking
- Easy team synchronization
- Automatic updates with git

**Cons:**
- Requires git submodule knowledge
- More complex for beginners
- Entire repository included (not just test-fully)

---

## Verification

### Test Installation

After installation, verify the skill works:

**1. Check files exist:**

```bash
# Windows PowerShell
dir "$env:USERPROFILE\.claude\skills\test-fully\SKILL.md"

# macOS/Linux
ls ~/.claude/skills/test-fully/SKILL.md
```

**2. Test in Claude Code:**

```bash
# Start Claude Code in any directory
claude code

# Try the skill
/test-fully
```

You should see the test-fully skill activate and prompt you for code to test.

**3. Test with actual code:**

Create a simple test file:

```javascript
// test.js
function add(a, b) {
  return a + b;
}
module.exports = { add };
```

Then test it:
```bash
/test-fully test.js
```

Claude should generate comprehensive tests for the `add` function.

---

## Configuration

### Basic .claude File

```yaml
# .claude
skills:
  - ./skills/test-fully

# Optional: Set preferred model
model: claude-sonnet-4-5-20250929
```

### Advanced .claude File

```yaml
# .claude
skills:
  - ./skills/test-fully
  # - ./skills/other-skill  # Add more skills

# Optional shortcuts for common commands
commands:
  test: "Use /test-fully for comprehensive testing"
  unit: "Use /test-fully --focus unit"
  integration: "Use /test-fully --focus integration"
  e2e: "Use /test-fully --focus e2e"
  perf: "Use /test-fully --focus performance"

# Optional: Configure test preferences
testPreferences:
  framework: jest  # or pytest, junit, etc.
  coverage: true
  verbose: true
```

---

## Multiple Skills Installation

If you want both BigQuery and test-fully skills:

```yaml
# .claude
skills:
  - ./skills/bigquery
  - ./skills/test-fully
```

Or with global installation:
```bash
# Windows
Copy-Item -Recurse ".\screen1-claude\skills\bigquery" "$env:USERPROFILE\.claude\skills\bigquery"
Copy-Item -Recurse ".\screen1-claude\skills\test-fully" "$env:USERPROFILE\.claude\skills\test-fully"

# macOS/Linux
cp -r ./screen1-claude/skills/bigquery ~/.claude/skills/
cp -r ./screen1-claude/skills/test-fully ~/.claude/skills/
```

---

## Directory Structure After Installation

### Global Installation:
```
~/.claude/  (or %USERPROFILE%\.claude\ on Windows)
├── skills/
│   └── test-fully/
│       ├── SKILL.md
│       ├── README.md
│       ├── QUICK_START.md
│       ├── INSTALLATION.md
│       ├── STRUCTURE.md
│       └── .claude.example
```

### Project-Specific Installation:
```
your-project/
├── .claude                    # Config file
├── skills/
│   └── test-fully/
│       ├── SKILL.md
│       ├── README.md
│       ├── QUICK_START.md
│       ├── INSTALLATION.md
│       ├── STRUCTURE.md
│       └── .claude.example
└── [your project files]
```

---

## Troubleshooting

### Issue: Skill Not Found

**Problem:** `/test-fully` returns "skill not found"

**Solutions:**
1. Check the path in your `.claude` file is correct
2. Verify `SKILL.md` exists in the test-fully directory
3. Try using an absolute path instead of relative
4. Restart Claude Code

```bash
# Test with absolute path
# Windows
$env:USERPROFILE\.claude\skills\test-fully

# macOS/Linux
~/.claude/skills/test-fully
```

### Issue: Permission Denied (Windows)

**Problem:** Cannot create symbolic link

**Solution:**
```powershell
# Run PowerShell as Administrator, or
# Use Method 1 (Copy) instead of symbolic link
```

### Issue: Permission Denied (macOS/Linux)

**Problem:** Cannot copy to ~/.claude/skills/

**Solution:**
```bash
# Create directory first
mkdir -p ~/.claude/skills

# Ensure you have permissions
sudo chown -R $USER ~/.claude
```

### Issue: Skill Loads But Doesn't Work

**Problem:** Skill activates but commands don't work properly

**Solutions:**
1. Check `SKILL.md` file is not corrupted
2. Verify file encoding is UTF-8
3. Ensure you're using a compatible Claude Code version
4. Check Claude Code logs for errors

---

## Updating the Skill

### Method 1 (Quick Install):
```bash
# Windows
Copy-Item -Recurse -Force ".\screen1-claude\skills\test-fully" "$env:USERPROFILE\.claude\skills\test-fully"

# macOS/Linux
cp -r ./screen1-claude/skills/test-fully ~/.claude/skills/
```

### Method 2 (Persistent Clone):
```bash
# Navigate to cloned repo
cd ~/.claude/repos/screen1-claude  # or $env:USERPROFILE\.claude\repos\screen1-claude

# Pull latest changes
git pull origin main

# Skill automatically updated via symlink
```

### Method 3 (Project-Specific):
```bash
# Backup current version
cp -r ./skills/test-fully ./skills/test-fully.backup

# Copy new version
cp -r ~/screen1-claude/skills/test-fully ./skills/

# Test new version
/test-fully

# If issues, restore backup:
# rm -rf ./skills/test-fully && mv ./skills/test-fully.backup ./skills/test-fully
```

### Method 4 (Git Submodule):
```bash
# Update submodule
git submodule update --remote

# Commit the update
git add .claude/screen1-claude
git commit -m "Update test-fully skill to latest version"
```

---

## Uninstallation

To remove the skill:

**Global Installation:**
```bash
# Windows
Remove-Item -Recurse "$env:USERPROFILE\.claude\skills\test-fully"

# macOS/Linux
rm -rf ~/.claude/skills/test-fully
```

**Project-Specific:**
```bash
# Remove skill directory
rm -rf ./skills/test-fully

# Update .claude file to remove test-fully reference
```

---

## Next Steps

After successful installation:

1. **Read the documentation:**
   - [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes
   - [README.md](README.md) - Full feature documentation
   - [STRUCTURE.md](STRUCTURE.md) - Understanding how it works

2. **Try a simple test:**
   ```bash
   /test-fully path/to/your/code.js
   ```

3. **Customize for your needs:**
   - Edit SKILL.md to add team-specific patterns
   - Configure .claude file with shortcuts
   - Add your preferred testing frameworks

4. **Share with your team:**
   - Use Method 2 (Persistent Clone) for easy sharing
   - Document your team's testing conventions
   - Contribute improvements back to the repository

---

## Support

Having installation issues?

1. Check this guide first
2. Review [README.md](README.md) for usage help
3. Check [QUICK_START.md](QUICK_START.md) for basic usage
4. Verify your Claude Code version is up to date
5. Check the screen1-claude repository for updates

---

**Installation complete! Start testing your code now! 🚀**
