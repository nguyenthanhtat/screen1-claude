# Git Advanced

**Parent Skill:** `/git`
**Path:** `/git/advanced`

## Purpose
Master advanced Git features including stash, cherry-pick, submodules, hooks, worktrees, sparse checkout, and Git attributes for power users.

## When to Use

**Trigger automatically when:**
- User mentions: stash, cherry-pick, submodule, hook, worktree, sparse, filter-branch, LFS
- Need to save work without committing
- Apply specific commits across branches
- Manage dependencies as submodules
- Automate Git operations
- Work on multiple branches simultaneously

**Chat commands:**
```bash
/git/advanced save my work without committing
/git/advanced apply commit from another branch
/git/advanced set up git hooks
/git/advanced work on multiple branches at once
/git/advanced manage large files in git
```

## Requirements

<critical>
- Git 2.30+ installed
- Repository access
- For hooks: Script execution permissions
- For submodules: Access to submodule repositories
- For LFS: Git LFS extension installed
- For worktrees: Disk space for multiple working directories
</critical>

## Verification
```bash
# Check Git version
git --version

# Check if Git LFS installed
git lfs --version

# Check hooks directory
ls -la .git/hooks/

# Check worktrees
git worktree list
```

---

## Critical Rules

<critical>
1. ALWAYS test hooks before committing
2. NEVER commit .git/hooks/ (use templates instead)
3. ALWAYS document submodule usage in README
4. Be cautious with filter-branch (destructive)
5. ALWAYS backup before advanced operations
6. Consider alternatives before using filter-branch
</critical>

---

## Patterns

### Pattern 1: Stash (Save Work Without Committing)

**Problem:** Need to switch context but not ready to commit

```bash
# ❌ BAD: Commit unfinished work
git add .
git commit -m "WIP"  # Clutters history

# ✅ GOOD: Use stash
git stash
git stash push -m "Work in progress on login feature"
```

**Basic stash workflow:**
```bash
# Save current changes
git stash

# Or with message
git stash push -m "Login feature work"

# List stashes
git stash list
# stash@{0}: On main: Login feature work
# stash@{1}: On main: Dashboard updates

# Apply latest stash
git stash pop  # Apply and remove from stash list

# Apply without removing
git stash apply

# Apply specific stash
git stash apply stash@{1}

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

**Advanced stash:**
```bash
# Stash only staged changes
git stash push --staged

# Stash including untracked files
git stash push -u

# Stash including ignored files
git stash push -a

# Stash specific files
git stash push -m "Config changes" config/*.json

# Interactive stash (choose hunks)
git stash push -p
```

**View stash contents:**
```bash
# See what's in stash
git stash show

# Detailed diff
git stash show -p

# Specific stash
git stash show stash@{1} -p
```

**Stash workflow example:**
```bash
# Working on feature
# ... editing files ...

# Urgent bug fix needed!
git stash push -m "Feature work"

# Fix bug
git checkout -b hotfix/urgent
# ... fix bug ...
git commit -m "fix: urgent bug"

# Back to feature
git checkout feature-branch
git stash pop  # Resume work
```

**Impact:** Context switching without committing

**When to use:**
- Switch branches with uncommitted changes
- Pull with local changes
- Temporarily save experimental work
- Apply changes across branches

---

### Pattern 2: Cherry-Pick (Apply Specific Commits)

**Problem:** Need commit from another branch without full merge

```bash
# ❌ BAD: Merge entire branch for one commit
git merge feature-branch  # Brings all commits!

# ✅ GOOD: Cherry-pick specific commit
git cherry-pick abc1234  # Only this commit
```

**Basic cherry-pick:**
```bash
# Apply commit from another branch
git checkout main
git cherry-pick abc1234

# New commit created on main with same changes
```

**Cherry-pick multiple commits:**
```bash
# Multiple commits
git cherry-pick abc1234 def5678 ghi9012

# Range of commits (exclusive start)
git cherry-pick abc1234..def5678

# Range including start commit
git cherry-pick abc1234^..def5678
```

**Cherry-pick with modifications:**
```bash
# Cherry-pick without committing (review first)
git cherry-pick abc1234 --no-commit

# Review changes
git status
git diff

# Then commit
git commit

# Edit commit message during cherry-pick
git cherry-pick abc1234 -e

# Change author
git cherry-pick abc1234 --reset-author
```

**Handle conflicts:**
```bash
# Cherry-pick causes conflict
git cherry-pick abc1234
# CONFLICT!

# Resolve conflict
git add resolved-file.js

# Continue cherry-pick
git cherry-pick --continue

# Or abort
git cherry-pick --abort
```

**Use cases:**
```bash
# Backport bug fix to release branch
git checkout release/v1.0
git cherry-pick bug-fix-commit

# Apply hotfix to multiple branches
git checkout main
git cherry-pick hotfix-commit
git checkout develop
git cherry-pick hotfix-commit

# Extract commit from merged PR
git cherry-pick feature-commit
```

**Impact:** Selective commit application

**When to use:**
- Backporting fixes
- Applying hotfixes across branches
- Extracting specific features
- Fixing commits on wrong branch

---

### Pattern 3: Submodules (Manage Dependencies)

**Problem:** Include external repository in your project

```bash
# ❌ BAD: Copy files from other repo
# Loses Git history and updates

# ✅ GOOD: Use submodule
git submodule add https://github.com/user/library.git libs/library
```

**Add submodule:**
```bash
# Add submodule
git submodule add https://github.com/user/library.git vendor/library

# Creates:
# - vendor/library/ (submodule content)
# - .gitmodules (submodule configuration)

# Commit submodule
git add .gitmodules vendor/library
git commit -m "chore: add library submodule"
git push
```

**Clone repository with submodules:**
```bash
# Method 1: Clone and initialize
git clone https://github.com/user/main-repo.git
cd main-repo
git submodule init
git submodule update

# Method 2: Clone with recursive
git clone --recursive https://github.com/user/main-repo.git

# Method 3: Initialize after clone
git clone https://github.com/user/main-repo.git
cd main-repo
git submodule update --init --recursive
```

**Update submodules:**
```bash
# Update all submodules to latest
git submodule update --remote

# Update specific submodule
git submodule update --remote vendor/library

# Commit updated submodule references
git add vendor/library
git commit -m "chore: update library submodule"
```

**Work within submodule:**
```bash
# Enter submodule
cd vendor/library

# It's a normal Git repository
git checkout main
git pull origin main

# Make changes (if you have write access)
git add .
git commit -m "fix: update library"
git push origin main

# Go back to main repo
cd ../..

# Commit new submodule reference
git add vendor/library
git commit -m "chore: update library to latest commit"
```

**Remove submodule:**
```bash
# Remove submodule (Git 2.13+)
git submodule deinit vendor/library
git rm vendor/library
git commit -m "chore: remove library submodule"

# Manual removal (older Git)
git submodule deinit vendor/library
git rm vendor/library
rm -rf .git/modules/vendor/library
git commit -m "chore: remove library submodule"
```

**Impact:** Manage external dependencies with Git

**When to use:**
- Shared libraries across projects
- Third-party dependencies
- Monorepo alternative
- Version-controlled dependencies

**Alternatives to consider:**
- Package managers (npm, pip, Maven) - Usually better
- Git subtree (simpler than submodules)
- Vendor directories (copy files)

---

### Pattern 4: Git Hooks (Automate Operations)

**Problem:** Automate checks before commit/push

```bash
# ❌ BAD: Manually remember to run tests
# Forget to run tests, push broken code

# ✅ GOOD: Automate with hooks
# Tests run automatically before push
```

**Available hooks:**
```
Client-side:
- pre-commit: Before commit created
- prepare-commit-msg: Before commit message editor
- commit-msg: After commit message entered
- post-commit: After commit created
- pre-push: Before push to remote
- post-checkout: After checkout
- post-merge: After merge

Server-side:
- pre-receive: Before push accepted
- update: Once per branch pushed
- post-receive: After push accepted
```

**Create hook:**
```bash
# Hooks location
ls .git/hooks/
# pre-commit.sample
# pre-push.sample
# ...

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Run linter
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Linting failed. Please fix errors."
  exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
  echo "❌ Tests failed. Please fix tests."
  exit 1
fi

echo "✅ All checks passed!"
exit 0
EOF

# Make executable
chmod +x .git/hooks/pre-commit
```

**Pre-commit hook (prevent bad commits):**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Prevent commits to main
branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
if [ "$branch" = "main" ]; then
  echo "❌ Cannot commit directly to main branch!"
  echo "Create a feature branch: git checkout -b feature/name"
  exit 1
fi

# Check for debugging code
if git diff --cached | grep -E "console\.log|debugger"; then
  echo "❌ Remove console.log or debugger statements"
  exit 1
fi

# Check for secrets
if git diff --cached | grep -iE "password|secret|api_key|token"; then
  echo "⚠️  Warning: Possible secret in commit"
  echo "Review changes carefully"
  # Uncomment to block:
  # exit 1
fi

exit 0
```

**Commit-msg hook (enforce message format):**
```bash
#!/bin/bash
# .git/hooks/commit-msg

# Enforce conventional commits
commit_msg=$(cat "$1")

if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"; then
  echo "❌ Invalid commit message format!"
  echo "Use: <type>: <description>"
  echo "Types: feat, fix, docs, style, refactor, test, chore"
  echo ""
  echo "Examples:"
  echo "  feat: add user authentication"
  echo "  fix: resolve login bug"
  exit 1
fi

exit 0
```

**Pre-push hook (prevent broken push):**
```bash
#!/bin/bash
# .git/hooks/pre-push

# Run full test suite
echo "Running tests before push..."
npm test

if [ $? -ne 0 ]; then
  echo "❌ Tests failed. Push aborted."
  exit 1
fi

echo "✅ Tests passed. Pushing..."
exit 0
```

**Share hooks with team:**
```bash
# Hooks aren't committed (.git/hooks/)
# Share via templates

# Create hooks directory in repo
mkdir -p .githooks

# Add hooks
cp my-pre-commit-hook .githooks/pre-commit

# Configure Git to use this directory
git config core.hooksPath .githooks

# Commit hooks directory
git add .githooks
git commit -m "chore: add Git hooks"

# Team members configure:
git config core.hooksPath .githooks
chmod +x .githooks/*
```

**Tools for hooks:**
```bash
# Husky (Node.js)
npm install -D husky
npx husky install
npx husky add .husky/pre-commit "npm test"

# Pre-commit framework (Python)
pip install pre-commit
pre-commit install
```

**Impact:** Automated quality checks

**When to use:**
- Enforce code standards
- Run tests automatically
- Prevent common mistakes
- Standardize commit messages

---

### Pattern 5: Worktrees (Multiple Working Directories)

**Problem:** Work on multiple branches simultaneously

```bash
# ❌ BAD: Clone repo multiple times
git clone repo.git repo-feature1
git clone repo.git repo-feature2
# Wastes disk space, separate repos

# ✅ GOOD: Use worktrees
git worktree add ../repo-feature1 feature1
git worktree add ../repo-feature2 feature2
# Shares .git directory
```

**Create worktree:**
```bash
# Main repo structure
/project/main/  (main branch)

# Add worktree for feature
cd /project/main
git worktree add ../feature1 feature1

# Now you have:
/project/main/     (main branch)
/project/feature1/ (feature1 branch)

# Both share same .git!
```

**Worktree workflow:**
```bash
# Work on main branch
cd /project/main
# ... work on main ...

# Switch to feature branch (different directory!)
cd /project/feature1
# ... work on feature ...

# Both are active simultaneously!
# No need to stash or commit unfinished work
```

**List worktrees:**
```bash
git worktree list
# /project/main      abc1234 [main]
# /project/feature1  def5678 [feature1]
# /project/hotfix    ghi9012 [hotfix/urgent]
```

**Remove worktree:**
```bash
# Remove worktree
git worktree remove ../feature1

# Or delete directory and prune
rm -rf ../feature1
git worktree prune
```

**Create worktree with new branch:**
```bash
# Create new branch and worktree
git worktree add ../feature2 -b feature2

# Create from specific commit
git worktree add ../hotfix -b hotfix abc1234
```

**Use cases:**
```bash
# Scenario 1: Code review while developing
# Main work
cd /project/feature-login
# ... developing ...

# Quick code review in separate worktree
cd /project
git worktree add ../review-pr-123 pr-123
cd ../review-pr-123
# Review code
cd ../feature-login
# Continue work

# Scenario 2: Run tests on different branch
cd /project/main
git worktree add ../test-branch feature-branch
cd ../test-branch
npm test  # Tests run while you continue working on main

# Scenario 3: Hotfix while feature in progress
cd /project/feature
# Urgent bug!
cd /project
git worktree add ../hotfix -b hotfix/urgent
cd ../hotfix
# Fix bug
git push origin hotfix/urgent
cd ../feature
# Resume feature work
```

**Impact:** Parallel work on multiple branches

**When to use:**
- Code review without losing work
- Run tests on different branch
- Work on hotfix while feature in progress
- Compare implementations

---

### Pattern 6: Sparse Checkout (Partial Clone)

**Problem:** Repository too large, only need some files

```bash
# ❌ BAD: Clone entire monorepo
git clone huge-monorepo.git
# Downloads 10GB for 100MB you need

# ✅ GOOD: Sparse checkout
git clone --filter=blob:none --sparse huge-monorepo.git
cd huge-monorepo
git sparse-checkout set packages/my-app
# Only downloads files you need
```

**Enable sparse checkout:**
```bash
# Clone with sparse checkout
git clone --filter=blob:none --sparse <repo-url>
cd repo

# Set which directories to include
git sparse-checkout set packages/app
git sparse-checkout add packages/shared

# List current sparse checkout
git sparse-checkout list
```

**Patterns:**
```bash
# Include specific directories
git sparse-checkout set src/components tests/unit

# Include with patterns
git sparse-checkout set "*.js" "*.json"

# Cone mode (recommended, faster)
git sparse-checkout init --cone
git sparse-checkout set packages/my-app

# Disable sparse checkout
git sparse-checkout disable
```

**Partial clone:**
```bash
# Clone without full history
git clone --depth 1 <repo-url>  # Only latest commit

# Clone without blobs (download on checkout)
git clone --filter=blob:none <repo-url>

# Clone without trees
git clone --filter=tree:0 <repo-url>

# Fetch more history later
git fetch --unshallow
```

**Impact:** Faster clones for large repositories

**When to use:**
- Large monorepos
- Only need subset of files
- CI/CD optimization
- Slow network connections

---

### Pattern 7: Git Attributes and LFS

**Problem:** Handle large files or custom merge strategies

**Git LFS (Large File Storage):**
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.mp4"
git lfs track "*.zip"

# Creates .gitattributes
cat .gitattributes
# *.psd filter=lfs diff=lfs merge=lfs -text
# *.mp4 filter=lfs diff=lfs merge=lfs -text

# Add and commit
git add .gitattributes
git commit -m "chore: track large files with LFS"

# Add large file (automatically uses LFS)
git add design.psd
git commit -m "chore: add design file"
git push

# Clone with LFS
git lfs clone <repo-url>
```

**Git attributes (.gitattributes):**
```bash
# Line ending normalization
* text=auto
*.sh text eol=lf
*.bat text eol=crlf

# Language detection
*.js linguist-language=JavaScript
docs/* linguist-documentation

# Diff drivers
*.json diff=json
*.md diff=markdown

# Merge strategies
package-lock.json merge=ours
database.sql merge=union

# Binary files
*.png binary
*.jpg binary
*.gif binary

# Export ignore (not in archive)
.gitattributes export-ignore
.gitignore export-ignore
tests/ export-ignore
```

**Custom merge driver:**
```bash
# .gitattributes
package-lock.json merge=npm-merge

# .git/config or .gitconfig
[merge "npm-merge"]
  name = automatically merge npm lock files
  driver = npx npm-merge-driver merge %A %O %B %P
```

**Impact:** Handle large files and custom strategies

**When to use:**
- Large binary files (images, videos)
- Generated files (package-lock.json)
- Platform-specific line endings
- Custom merge strategies

---

### Pattern 8: Filter-Branch and History Rewriting

**Problem:** Remove sensitive data or reduce repository size

```bash
# ⚠️  DANGEROUS: Rewrites entire history

# ❌ BAD: filter-branch (deprecated)
git filter-branch --tree-filter 'rm -f secret.txt' HEAD

# ✅ GOOD: Use BFG Repo-Cleaner (faster, safer)
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

java -jar bfg.jar --delete-files secret.txt repo.git
```

**Remove file from history (BFG):**
```bash
# Clone mirror
git clone --mirror https://github.com/user/repo.git

# Remove file
java -jar bfg.jar --delete-files secret.txt repo.git

# Clean up
cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (⚠️  destructive)
git push
```

**Remove large files:**
```bash
# Remove files over 100MB
java -jar bfg.jar --strip-blobs-bigger-than 100M repo.git

# Remove specific large file
java -jar bfg.jar --delete-files large-file.zip repo.git
```

**Replace text in history:**
```bash
# Remove passwords/secrets
java -jar bfg.jar --replace-text passwords.txt repo.git

# passwords.txt contains:
# PASSWORD1
# SECRET_API_KEY
```

**Modern alternative (git filter-repo):**
```bash
# Install: pip install git-filter-repo

# Remove file
git filter-repo --path secret.txt --invert-paths

# Remove directory
git filter-repo --path vendor/ --invert-paths

# Rename author
git filter-repo --name-callback '
  return name.replace(b"Old Name", b"New Name")
'
```

**Impact:** Clean repository history

**When to use:**
- Remove committed secrets (then rotate secrets!)
- Reduce repository size
- Fix authorship across history
- Clean up before open sourcing

**Critical notes:**
- ⚠️  Rewrites ALL commit hashes
- ⚠️  Team must re-clone repository
- ⚠️  Coordinate with entire team
- ⚠️  Have backup before running
- ✅  Rotate secrets after removal

---

## Common Workflows

### Context Switching with Stash
```bash
# Working on feature
# ... editing files ...

# Urgent bug fix needed
git stash push -m "Feature work"
git checkout -b hotfix/urgent
# Fix bug, commit, push
git checkout feature-branch
git stash pop
```

### Backporting Bug Fix
```bash
# Fixed bug on main
git log --oneline -5
# abc1234 fix: resolve login bug

# Apply to release branch
git checkout release/v1.0
git cherry-pick abc1234
git push origin release/v1.0
```

### Working with Submodules
```bash
# Clone project with submodules
git clone --recursive project.git

# Update submodules
git submodule update --remote

# Work in submodule
cd vendor/library
git checkout main
git pull
cd ../..
git add vendor/library
git commit -m "chore: update library"
```

---

## Best Practices

1. **Stash with messages** - Always name stashes
2. **Cherry-pick carefully** - Can create duplicate commits
3. **Document submodules** - README should explain them
4. **Share hooks** - Use .githooks directory
5. **Clean up worktrees** - Remove when done
6. **Backup before filter-branch** - Irreversible operation
7. **Use LFS early** - Add before committing large files
8. **Test hooks** - Ensure they don't break workflow

## Related Sub-Skills

- Basic Git operations? → `/git/basics`
- Branch management? → `/git/branching`
- Undo operations? → `/git/undo`
- Remote operations? → `/git/remote`

## Quick Command Reference

```bash
# Stash
git stash push -m "message"          # Save work
git stash list                       # List stashes
git stash pop                        # Apply and remove
git stash apply stash@{0}            # Apply specific

# Cherry-pick
git cherry-pick abc1234              # Apply commit
git cherry-pick abc..def             # Range

# Submodules
git submodule add <url> <path>       # Add submodule
git submodule update --init          # Initialize
git submodule update --remote        # Update

# Hooks
chmod +x .git/hooks/pre-commit       # Make executable
git config core.hooksPath .githooks  # Custom hooks dir

# Worktrees
git worktree add <path> <branch>     # Create worktree
git worktree list                    # List worktrees
git worktree remove <path>           # Remove worktree

# Sparse checkout
git sparse-checkout set <path>       # Set sparse
git sparse-checkout list             # List paths

# LFS
git lfs install                      # Install LFS
git lfs track "*.psd"                # Track files
git lfs ls-files                     # List LFS files
```

---

**Last Updated:** 2025-02-11
**Version:** 1.0.0
