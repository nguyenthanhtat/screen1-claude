# Git Skill Suite

Complete set of Git skills for Claude Code and Claude AI - from basics to advanced operations.

## 📦 What's Included

### Main Router Skill
- **SKILL.md** - Main entry point that routes to sub-skills based on your question

### 8 Sub-Skills

1. **basics/** - Repository setup, commits, .gitignore, and fundamental workflows
2. **branching/** - Branch management, merging, rebasing, and branch strategies
3. **history/** - Commit history, diffs, blame, bisect, and code archaeology
4. **remote/** - Remote operations, push/pull, multiple remotes, and fork syncing
5. **conflicts/** - Merge and rebase conflict resolution strategies
6. **undo/** - Undo changes, reset, revert, and reflog recovery
7. **workflows/** - GitHub Flow, Git Flow, trunk-based, PR best practices
8. **advanced/** - Stash, cherry-pick, hooks, submodules, worktrees, LFS

## 🚀 Installation

### Quick Install

```bash
# Copy to Claude skills directory
cp -r skills/git ~/.claude/skills/git
```

### Windows (PowerShell)

```powershell
Copy-Item -Recurse skills/git $env:USERPROFILE\.claude\skills\git
```

### Manual Installation

1. Create skills directory:
   ```bash
   mkdir -p ~/.claude/skills
   ```

2. Copy Git skill:
   ```bash
   cp -r skills/git ~/.claude/skills/git
   ```

3. Verify:
   ```bash
   ls ~/.claude/skills/git
   ```

## 📖 Usage

### Direct Sub-Skill Access

```bash
# Basic operations
/git/basics help me make my first commit
/git/basics create .gitignore for Node.js project

# Branch management
/git/branching create feature branch and merge to main
/git/branching interactive rebase to clean commits

# View history
/git/history show commits from last week
/git/history who changed this line

# Remote operations
/git/remote push my branch to GitHub
/git/remote sync my fork with upstream

# Resolve conflicts
/git/conflicts help me resolve merge conflict in app.js
/git/conflicts use theirs for all conflicts

# Undo changes
/git/undo fix my last commit message
/git/undo recover deleted commit

# Team workflows
/git/workflows explain GitHub Flow
/git/workflows set up pull request template

# Advanced features
/git/advanced save work without committing
/git/advanced cherry-pick commit to another branch
```

### Auto-Routing

Let Claude decide which sub-skill to use:

```bash
# Claude automatically routes to the right skill
/git how do I commit my changes?
/git I have a merge conflict
/git undo my last commit
/git what's GitHub Flow?
```

## 🎯 Quick Start Scenarios

### New to Git?
```bash
# Start here
/git/basics initialize repository and make first commit
/git/basics what's the basic workflow
/git/basics create .gitignore
```

### Working on a Team?
```bash
# Collaboration essentials
/git/workflows what workflow should we use
/git/branching create feature branch
/git/remote push to GitHub
/git/conflicts resolve merge conflict
```

### Made a Mistake?
```bash
# Undo operations
/git/undo unstage this file
/git/undo fix my commit message
/git/undo undo last commit but keep changes
/git/undo recover deleted branch
```

### Advanced User?
```bash
# Power features
/git/advanced stash my changes
/git/advanced cherry-pick commit
/git/advanced set up git hooks
/git/advanced work on multiple branches
```

## 🎓 Learning Path

### Beginner
1. `/git/basics` - Learn Git fundamentals
2. `/git/branching` - Understand branches
3. `/git/remote` - Push and pull
4. `/git/undo` - Fix mistakes

### Intermediate
1. `/git/workflows` - Team collaboration
2. `/git/conflicts` - Handle conflicts
3. `/git/history` - Inspect history
4. `/git/branching` - Advanced merging

### Advanced
1. `/git/advanced` - Stash, hooks, worktrees
2. `/git/workflows` - Choose team workflow
3. `/git/history` - Code archaeology
4. `/git/undo` - Complex recovery

## 🛠️ Common Use Cases

### Daily Development

```bash
# Morning routine
/git/basics pull latest changes
/git/branching create feature branch

# During development
/git/basics commit changes
/git/history check what changed

# End of day
/git/remote push my work
```

### Code Review

```bash
# Before creating PR
/git/history review my commits
/git/branching clean up commit history
/git/remote push to origin

# During review
/git/conflicts resolve feedback
/git/undo amend commit
```

### Hotfix Process

```bash
# Urgent production fix
/git/branching create hotfix branch
/git/basics commit fix
/git/remote push hotfix
/git/workflows merge hotfix to main and develop
```

### Open Source Contribution

```bash
# Fork workflow
/git/remote setup fork with upstream
/git/branching create feature branch
/git/basics make commits
/git/remote sync with upstream
/git/workflows create pull request
```

## 📋 Command Quick Reference

### Basics
```bash
git init                    # Initialize repository
git add <file>              # Stage changes
git commit -m "message"     # Commit
git push                    # Push to remote
git pull                    # Pull from remote
```

### Branching
```bash
git switch -c branch        # Create branch
git merge branch            # Merge branch
git rebase main             # Rebase on main
git branch -d branch        # Delete branch
```

### History
```bash
git log --oneline          # View commits
git diff                   # See changes
git blame file             # Who changed line
git bisect                 # Find bug introduction
```

### Undo
```bash
git restore --staged file  # Unstage
git restore file           # Discard changes
git commit --amend         # Fix last commit
git reset HEAD~1           # Undo commit
git revert HEAD            # Safe undo (public)
```

## 🏆 Best Practices

### For Teams
- ✅ Use pull requests for all changes
- ✅ Write meaningful commit messages
- ✅ Pull before push
- ✅ Keep branches short-lived
- ✅ Code review before merge
- ✅ Protect main branch

### For Solo Projects
- ✅ Commit frequently
- ✅ Write clear messages
- ✅ Use .gitignore
- ✅ Never commit secrets
- ✅ Push regularly (backup)

### For Open Source
- ✅ Fork the repository
- ✅ Follow contribution guidelines
- ✅ Keep fork synced
- ✅ One feature per PR
- ✅ Respect maintainer feedback

## 🔧 Configuration Tips

### First-Time Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

### Useful Aliases
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.lg "log --oneline --graph --all"
```

### SSH Setup (GitHub)
```bash
ssh-keygen -t ed25519 -C "you@example.com"
ssh-add ~/.ssh/id_ed25519
# Add public key to GitHub
```

## 📚 Additional Resources

### Official Documentation
- [Git Documentation](https://git-scm.com/doc)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [GitHub Docs](https://docs.github.com)

### Interactive Learning
- [Learn Git Branching](https://learngitbranching.js.org/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

### Tools
- [GitHub Desktop](https://desktop.github.com/) - GUI client
- [GitKraken](https://www.gitkraken.com/) - Visual Git client
- [tig](https://jonas.github.io/tig/) - Terminal Git interface

## 🤝 Contributing

Found an issue or want to improve this skill?

1. The skill files are in `skills/git/`
2. Each sub-skill has its own directory
3. Update relevant SKILL.md files
4. Test your changes
5. Submit improvements

## 📜 License

Free to use and modify for personal/commercial projects.

## 🆘 Getting Help

### Within Claude
```bash
# Ask for help on any Git topic
/git help me with [topic]

# Navigate to specific sub-skill
/git/basics
/git/branching
/git/conflicts
# ... etc
```

### Outside Claude
- Git documentation: `git help <command>`
- Stack Overflow: [git tag](https://stackoverflow.com/questions/tagged/git)
- GitHub Community: [community.github.com](https://github.community/)

## 📊 Version

- **Current Version:** 1.0.0
- **Last Updated:** 2025-02-11
- **Git Version Required:** 2.30+
- **Platforms:** All (Linux, macOS, Windows)

## 🎯 What Makes This Skill Suite Special

✨ **Comprehensive Coverage** - From basics to advanced operations
✨ **Real-World Patterns** - Actual workflows used by professionals
✨ **Best Practices** - Learn the right way from the start
✨ **Beginner Friendly** - Clear explanations with examples
✨ **Team Ready** - Collaboration workflows included
✨ **Regular Updates** - Kept current with Git best practices

---

**Ready to master Git?** Start with `/git/basics` or ask any Git question with `/git`!
