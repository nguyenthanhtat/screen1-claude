# Team Setup Guide - Quick Install

Simple instructions for installing Claude Code skills on your computer.

## ⚡ Quick Install (Copy & Paste)

### For Mac / Linux / Git Bash (Windows)

```bash
git clone https://github.com/nguyenthanhtat/screen1-claude.git ~/claude-skills && cp -r ~/claude-skills/skills/test-fully ~/.claude/skills/ && cp -r ~/claude-skills/skills/git ~/.claude/skills/
```

### For Windows PowerShell

```powershell
git clone https://github.com/nguyenthanhtat/screen1-claude.git $env:USERPROFILE\claude-skills
Copy-Item -Recurse $env:USERPROFILE\claude-skills\skills\test-fully $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse $env:USERPROFILE\claude-skills\skills\git $env:USERPROFILE\.claude\skills\
```

### Test Installation

Open Claude Code and type:
```
/test-fully
/git
```

If you see the skill information, it's working! ✅

---

## 📋 Step-by-Step (If One-Line Fails)

### Step 1: Clone Repository

**Mac/Linux/Git Bash:**
```bash
git clone https://github.com/nguyenthanhtat/screen1-claude.git ~/claude-skills
```

**Windows PowerShell:**
```powershell
git clone https://github.com/nguyenthanhtat/screen1-claude.git $env:USERPROFILE\claude-skills
```

### Step 2: Copy Skills

**Mac/Linux/Git Bash:**
```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy the skills
cp -r ~/claude-skills/skills/test-fully ~/.claude/skills/
cp -r ~/claude-skills/skills/git ~/.claude/skills/
```

**Windows PowerShell:**
```powershell
# Create skills directory if it doesn't exist
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.claude\skills

# Copy the skills
Copy-Item -Recurse $env:USERPROFILE\claude-skills\skills\test-fully $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse $env:USERPROFILE\claude-skills\skills\git $env:USERPROFILE\.claude\skills\
```

### Step 3: Verify Installation

Check that files are in the right place:

**Mac/Linux/Git Bash:**
```bash
ls ~/.claude/skills/
# Should show: git  test-fully
```

**Windows PowerShell:**
```powershell
Get-ChildItem $env:USERPROFILE\.claude\skills\
# Should show: git  test-fully
```

### Step 4: Test in Claude Code

1. Open Claude Code
2. Type: `/test-fully`
3. Type: `/git`

If both commands show skill information, you're done! ✅

---

## 🔄 Updating Skills

To get the latest version:

**Mac/Linux/Git Bash:**
```bash
cd ~/claude-skills
git pull origin main
cp -r skills/test-fully ~/.claude/skills/
cp -r skills/git ~/.claude/skills/
```

**Windows PowerShell:**
```powershell
cd $env:USERPROFILE\claude-skills
git pull origin main
Copy-Item -Recurse -Force skills\test-fully $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse -Force skills\git $env:USERPROFILE\.claude\skills\
```

---

## ❓ Troubleshooting

### Problem: "git: command not found"

**Solution:** Install Git first
- **Mac:** `brew install git` or download from https://git-scm.com/
- **Windows:** Download from https://git-scm.com/download/win
- **Linux:** `sudo apt install git` or `sudo yum install git`

### Problem: Skills don't show up in Claude Code

**Solutions:**
1. Restart Claude Code
2. Check files are in correct location:
   - Mac/Linux: `~/.claude/skills/git/`
   - Windows: `C:\Users\YourName\.claude\skills\git\`
3. Verify SKILL.md files exist:
   ```bash
   # Mac/Linux/Git Bash
   ls ~/.claude/skills/test-fully/SKILL.md
   ls ~/.claude/skills/git/SKILL.md
   ```

### Problem: Permission denied

**Mac/Linux:**
```bash
chmod -R 755 ~/.claude/skills/
```

**Windows:** Run PowerShell as Administrator

### Problem: Directory already exists

**Solution:** Remove old version first
```bash
# Mac/Linux/Git Bash
rm -rf ~/.claude/skills/git
rm -rf ~/.claude/skills/test-fully
# Then copy again
```

```powershell
# Windows PowerShell
Remove-Item -Recurse -Force $env:USERPROFILE\.claude\skills\git
Remove-Item -Recurse -Force $env:USERPROFILE\.claude\skills\test-fully
# Then copy again
```

---

## 📖 Using the Skills

### BigQuery Skill

Moved to its own plugin: https://github.com/nguyenthanhtat/bigquery-skills
Install with `/plugin marketplace add nguyenthanhtat/bigquery-skills` then `/plugin install bigquery-skills@bigquery-skills`.

### Test-Fully Skill

```bash
# Test specific files
/test-fully src/utils/validator.js
/test-fully app/services/auth.py

# Focus on test types
/test-fully --focus unit
/test-fully --focus integration
/test-fully --focus e2e

# Test directories
/test-fully src/features/auth/
```

---

## 🆘 Need Help?

1. **Check documentation:**
   - Main README: https://github.com/nguyenthanhtat/screen1-claude
   - Detailed install guide: [INSTALL.md](INSTALL.md)

2. **Contact your team lead** with:
   - What command you ran
   - What error you got
   - Your operating system

3. **Verify requirements:**
   - ✅ Claude Code installed
   - ✅ Git installed
   - ✅ Internet connection

---

## ✅ Success Checklist

After installation, you should have:

- [ ] Cloned repository to `~/claude-skills` (or `%USERPROFILE%\claude-skills`)
- [ ] Copied test-fully skill to `~/.claude/skills/test-fully`
- [ ] Tested `/test-fully` command - shows skill info

**If all boxes are checked, you're ready to use the skills!** 🎉

---

## 📊 Installation Time

- **Quick install:** ~30 seconds
- **Step-by-step:** ~2 minutes
- **First time setup (with Git install):** ~5 minutes

---

**Repository:** https://github.com/nguyenthanhtat/screen1-claude
**Questions?** Ask your team lead or check the [troubleshooting guide](INSTALL.md)
