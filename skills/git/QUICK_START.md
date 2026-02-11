# Git Skill Suite - Quick Start Guide

Get started with the Git skill in 5 minutes!

## 📥 Installation (30 seconds)

```bash
# Copy to Claude skills directory
cp -r skills/git ~/.claude/skills/git
```

**Windows:**
```powershell
Copy-Item -Recurse skills/git $env:USERPROFILE\.claude\skills\git
```

## 🚀 First Steps (2 minutes)

### 1. Try the Main Skill

```bash
# Ask any Git question
/git how do I commit my changes?
/git what's the difference between merge and rebase?
/git I have a merge conflict, help!
```

Claude automatically routes to the right sub-skill!

### 2. Try a Specific Sub-Skill

```bash
# Go directly to a topic
/git/basics           # Learn fundamentals
/git/branching        # Branch management
/git/undo            # Fix mistakes
```

### 3. Get Help on Common Tasks

```bash
# I'm new to Git
/git/basics what's the basic workflow

# I need to create a branch
/git/branching create feature branch

# I made a mistake
/git/undo help me undo my last commit

# I have conflicts
/git/conflicts resolve merge conflict
```

## 🎯 Most Common Commands (2 minutes)

### Your First Commit

```bash
# Ask the skill
/git/basics help me make my first commit

# You'll learn:
git init
git add .
git commit -m "Initial commit"
```

### Create a Branch

```bash
# Ask the skill
/git/branching create feature branch

# You'll learn:
git switch -c feature/my-feature
# ... make changes ...
git push -u origin feature/my-feature
```

### Undo a Mistake

```bash
# Ask the skill
/git/undo I accidentally committed to main

# You'll learn how to fix it safely
```

### Resolve Conflicts

```bash
# Ask the skill
/git/conflicts I have merge conflicts in app.js

# Get step-by-step conflict resolution
```

## 💡 Quick Tips

### Use Auto-Routing
```bash
# Just describe what you need
/git I need to commit my changes
/git how do I create a branch
/git undo my last commit
/git resolve conflict

# Claude figures out which sub-skill to use!
```

### Go Direct When You Know
```bash
# If you know the topic
/git/basics         # Basic operations
/git/branching      # Branches
/git/history        # View history
/git/remote         # Push/pull
/git/conflicts      # Resolve conflicts
/git/undo           # Undo changes
/git/workflows      # Team workflows
/git/advanced       # Power features
```

## 🎓 Learning Path

### Day 1: Basics
```bash
/git/basics initialize repository
/git/basics commit workflow
/git/basics push to GitHub
```

### Day 2: Branching
```bash
/git/branching create feature branch
/git/branching merge branches
/git/branching delete old branches
```

### Day 3: Fixing Mistakes
```bash
/git/undo unstage files
/git/undo fix commit message
/git/undo undo last commit
```

### Week 2: Team Collaboration
```bash
/git/workflows explain GitHub Flow
/git/conflicts resolve merge conflicts
/git/remote sync with team
```

## 📋 Essential Commands

### Daily Workflow
```bash
git pull                  # Get latest
git switch -c feature     # Create branch
git add .                 # Stage changes
git commit -m "message"   # Commit
git push                  # Push to remote
```

### When Things Go Wrong
```bash
git status                # Check state
git restore --staged .    # Unstage all
git restore .             # Discard changes
git commit --amend        # Fix last commit
```

### Collaboration
```bash
git pull                  # Get updates
git push                  # Share work
git merge feature         # Integrate work
git rebase main           # Update branch
```

## 🔥 Common Scenarios

### Scenario 1: "I'm new to Git"
```bash
/git/basics
# Start here! Learn fundamentals
```

### Scenario 2: "I need to work on a feature"
```bash
/git/branching create feature branch for login page
# Creates branch, explains workflow
```

### Scenario 3: "I committed to wrong branch"
```bash
/git/undo I committed to main instead of feature branch
# Shows how to fix safely
```

### Scenario 4: "Merge conflict!"
```bash
/git/conflicts resolve merge conflict in src/app.js
# Step-by-step resolution guide
```

### Scenario 5: "How do we collaborate?"
```bash
/git/workflows what workflow should our team use
# Explains GitHub Flow, Git Flow, etc.
```

## ⚡ Power User Tips

### Save Time with Stash
```bash
/git/advanced stash my changes
# Save work without committing
```

### Apply Single Commit
```bash
/git/advanced cherry-pick commit from another branch
# Apply specific commit
```

### Work on Multiple Branches
```bash
/git/advanced work on two branches simultaneously
# Learn about worktrees
```

## 🛠️ First-Time Git Setup

If Git isn't configured yet:

```bash
# Ask the skill
/git/basics configure git

# Or manually:
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## 📚 Next Steps

Once you're comfortable:

1. **Explore Sub-Skills**
   - Each covers a specific area in depth
   - Browse `/git/[topic]`

2. **Learn Team Workflows**
   - `/git/workflows` - GitHub Flow, Git Flow
   - `/git/remote` - Collaboration patterns

3. **Master Advanced Features**
   - `/git/advanced` - Stash, hooks, worktrees
   - `/git/history` - Code archaeology

## 🎯 Success Checklist

After this quick start, you should be able to:

- ✅ Ask Git questions with `/git`
- ✅ Navigate to specific sub-skills
- ✅ Make your first commit
- ✅ Create and merge branches
- ✅ Undo mistakes safely
- ✅ Resolve conflicts
- ✅ Push to remote repository

## 💬 Getting Help

### Ask the Skill
```bash
# Any Git question works
/git [your question]

# Examples:
/git how do I merge branches
/git what's a rebase
/git undo my changes
```

### Explore Sub-Skills
```bash
# See all patterns for a topic
/git/basics
/git/branching
/git/history
```

## 🚦 Quick Command Reference

```bash
# Status
git status

# Basic workflow
git add .
git commit -m "message"
git push

# Branching
git switch -c branch-name
git merge branch-name

# Undo
git restore --staged file
git restore file
git commit --amend

# Info
git log --oneline
git diff
```

## 🎉 You're Ready!

That's it! You now know how to:
- Use the Git skill suite
- Find answers to Git questions
- Navigate sub-skills
- Perform common operations

**Start with your first question:**
```bash
/git how do I [what you want to do]
```

Happy Git-ing! 🚀

---

**Quick Links:**
- Full documentation: `README.md`
- Installation guide: `INSTALLATION.md`
- Architecture: `STRUCTURE.md`
