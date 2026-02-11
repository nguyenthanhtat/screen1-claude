# Git Basics

**Parent Skill:** `/git`
**Path:** `/git/basics`

## Purpose
Master Git fundamentals including repository initialization, commits, basic workflows, and .gitignore configuration. This is the foundation for all Git operations.

## When to Use

**Trigger automatically when:**
- User mentions: init, clone, commit, add, status, push, pull, .gitignore
- First-time Git setup
- Basic commit workflow questions
- Configuration issues
- New repository creation

**Chat commands:**
```bash
/git/basics initialize new repository
/git/basics help me commit my changes
/git/basics create .gitignore for Node.js project
/git/basics configure git with my name and email
/git/basics what's the basic workflow
```

## Requirements

<critical>
- Git 2.30+ installed (`git --version`)
- User name and email configured
- Write access to repository directory
- For remote operations: SSH keys or HTTPS credentials
</critical>

## Verification
```bash
# Check Git installation
git --version

# Check configuration
git config --global --list

# Test repository access
git status
```

---

## Critical Rules

<critical>
1. ALWAYS configure user.name and user.email before first commit
2. ALWAYS run `git status` before commits to review what's being committed
3. NEVER commit secrets, credentials, or sensitive data
4. ALWAYS use .gitignore for generated files and dependencies
5. NEVER use `git add .` blindly - know what you're staging
6. ALWAYS write meaningful commit messages (not "fix" or "update")
</critical>

---

## Basic Workflow

### The Three States of Files

```
Working Directory → Staging Area (Index) → Repository (History)
     (modified)         (staged)              (committed)
         ↓                  ↓                      ↓
    git add           git commit              git push
```

---

## Patterns

### Pattern 1: Initialize New Repository

**Problem:** Starting a new project with Git version control

```bash
# ❌ BAD: Initialize in wrong directory
cd /
git init  # Don't do this!

# ✅ GOOD: Initialize in project directory
cd ~/projects/my-app
git init
git add .
git commit -m "Initial commit"
```

**With remote:**
```bash
# Create repository on GitHub first, then:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

**Impact:** Proper project structure and remote tracking from the start

**When to use:**
- Starting new project from scratch
- Adding Git to existing project
- Converting local folder to Git repository

---

### Pattern 2: Clone Existing Repository

**Problem:** Get a copy of an existing repository

```bash
# ❌ BAD: Clone without understanding destination
git clone https://github.com/user/repo.git
cd repo  # Which repo directory am I in?

# ✅ GOOD: Clone with explicit directory name
git clone https://github.com/user/repo.git my-project
cd my-project

# ✅ EVEN BETTER: Clone with SSH (for push access)
git clone git@github.com:user/repo.git my-project
cd my-project
git config user.name "Your Name"
git config user.email "you@example.com"
```

**Clone specific branch:**
```bash
# Clone only main branch (faster)
git clone --branch main --single-branch https://github.com/user/repo.git

# Clone with shallow history (save space)
git clone --depth 1 https://github.com/user/repo.git
```

**Impact:** Faster setup with proper configuration

**When to use:**
- Contributing to existing project
- Forking open source repository
- Deploying code to server

---

### Pattern 3: Basic Commit Workflow

**Problem:** Save changes to repository history

```bash
# ❌ BAD: Commit everything blindly
git add .
git commit -m "update"  # Meaningless message

# ✅ GOOD: Review, stage selectively, write clear message
git status                           # See what changed
git diff                             # Review changes
git add src/app.js                   # Stage specific files
git add tests/app.test.js
git status                           # Verify staged changes
git commit -m "feat: add user authentication

Implement JWT-based authentication with:
- Login endpoint with email/password
- Token generation and validation
- Protected routes middleware

Fixes #123"
```

**Interactive staging:**
```bash
# Stage parts of a file (not the whole file)
git add -p src/app.js  # Interactive patch mode
# Select 'y' for hunks you want to stage

# Review what will be committed
git diff --staged
```

**Impact:** Clean, reviewable commit history

**When to use:**
- Every time you complete a logical unit of work
- Before switching branches
- At end of coding session

---

### Pattern 4: Conventional Commit Messages

**Problem:** Inconsistent, unclear commit history

```bash
# ❌ BAD: Vague messages
git commit -m "fix"
git commit -m "update code"
git commit -m "changes"

# ✅ GOOD: Conventional Commits format
git commit -m "feat: add user registration form"
git commit -m "fix: resolve null pointer in login handler"
git commit -m "docs: update API documentation"
git commit -m "refactor: extract validation to separate module"
git commit -m "test: add unit tests for auth service"
git commit -m "chore: update dependencies"
```

**Commit types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, semicolons)
- `refactor`: Code restructuring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Maintenance (dependencies, config)
- `perf`: Performance improvement
- `ci`: CI/CD changes

**With scope:**
```bash
git commit -m "feat(auth): add password reset flow"
git commit -m "fix(ui): correct button alignment on mobile"
```

**Impact:** Automated changelog generation, clearer project history

**When to use:**
- All commits in professional projects
- Open source contributions
- Team collaboration

---

### Pattern 5: Working with .gitignore

**Problem:** Prevent committing unnecessary or sensitive files

```bash
# ❌ BAD: No .gitignore, commit everything
git add .
git commit -m "add project"  # Includes node_modules/, .env, etc.

# ✅ GOOD: Create .gitignore first
# Create .gitignore file
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
vendor/

# Environment variables
.env
.env.local

# Build output
dist/
build/
*.log

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
EOF

git add .gitignore
git commit -m "chore: add .gitignore"
git add .
git commit -m "feat: initial project setup"
```

**Language-specific .gitignore templates:**

**Node.js:**
```bash
# .gitignore for Node.js
node_modules/
npm-debug.log
.env
dist/
coverage/
```

**Python:**
```bash
# .gitignore for Python
__pycache__/
*.py[cod]
venv/
.env
*.egg-info/
dist/
```

**Already committed sensitive file:**
```bash
# ❌ WRONG: Just add to .gitignore
echo ".env" >> .gitignore  # File still in history!

# ✅ RIGHT: Remove from Git but keep locally
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "chore: remove .env from tracking"

# If already pushed to remote, you need to:
# 1. Rotate the secrets (they're compromised!)
# 2. Use git filter-branch or BFG Repo-Cleaner to remove from history
```

**Impact:** Prevent security issues and reduce repository size

**When to use:**
- Immediately when starting new project
- Before first commit
- When adding new tools that generate files

---

### Pattern 6: Git Configuration

**Problem:** Proper Git setup for smooth workflow

```bash
# ❌ BAD: No configuration, commits with wrong identity
git commit -m "update"  # Uses wrong name/email

# ✅ GOOD: Configure before first commit
# Global configuration (all repositories)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Local configuration (this repository only)
git config user.name "Your Work Name"
git config user.email "you@company.com"

# Useful global settings
git config --global core.editor "code --wait"  # VS Code as editor
git config --global init.defaultBranch main    # Use 'main' instead of 'master'
git config --global pull.rebase false          # Merge on pull (default)
git config --global core.autocrlf input        # Line endings (Mac/Linux)
# git config --global core.autocrlf true       # Line endings (Windows)

# View all configuration
git config --list

# View specific config
git config user.email
```

**SSH key setup (for GitHub/GitLab):**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "you@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard (add to GitHub)
cat ~/.ssh/id_ed25519.pub

# Test connection
ssh -T git@github.com
```

**Impact:** Correct attribution and smooth remote operations

**When to use:**
- First time using Git
- New computer or user account
- Working with multiple Git identities

---

### Pattern 7: Checking Repository Status

**Problem:** Understanding current state of repository

```bash
# ❌ BAD: Make changes without checking status
git add .
git commit -m "stuff"

# ✅ GOOD: Regular status checks
git status                    # Full status

# Short status (more concise)
git status -s
# M  modified file
# A  added file
# D  deleted file
# ?? untracked file
# MM file modified, staged, then modified again

# See what changed (not yet staged)
git diff

# See what will be committed (staged)
git diff --staged

# See all changes
git diff HEAD
```

**Detailed inspection:**
```bash
# List all files Git is tracking
git ls-files

# See ignored files
git status --ignored

# See branch information
git status -sb  # Short with branch info
```

**Impact:** Prevent accidental commits and understand repository state

**When to use:**
- Before every `git add`
- Before every `git commit`
- After making changes
- When unsure about file state

---

### Pattern 8: Push and Pull

**Problem:** Sync local changes with remote repository

```bash
# ❌ BAD: Push without pull, no upstream tracking
git push  # May fail if remote has changes

# ✅ GOOD: Pull before push
git pull                      # Get latest changes
# Resolve conflicts if any
git push

# First push to new branch (set upstream)
git push -u origin feature-branch
# Subsequent pushes
git push

# Pull with rebase (cleaner history)
git pull --rebase
```

**Understanding push/pull:**
```bash
# Fetch (download changes, don't merge)
git fetch origin

# See what's new on remote
git log HEAD..origin/main

# Then merge manually
git merge origin/main

# Or pull (fetch + merge)
git pull origin main

# Push all branches
git push --all

# Push and set upstream
git push --set-upstream origin main
```

**Force push (dangerous!):**
```bash
# ❌ DANGEROUS: Can overwrite others' work
git push --force

# ✅ SAFER: Force with lease (fails if remote changed)
git push --force-with-lease

# Only use force push on:
# - Your own feature branches
# - After interactive rebase
# - When you're 100% sure
```

**Impact:** Keep local and remote in sync

**When to use:**
- After completing feature
- Before starting work (pull)
- Sharing work with team
- Backing up work to remote

---

## Common Workflows

### Daily Development Workflow
```bash
# Start of day
git pull                              # Get latest changes

# Make changes
# ... edit files ...

git status                            # See what changed
git diff                              # Review changes
git add src/feature.js                # Stage specific files
git commit -m "feat: add new feature" # Commit with message

# End of day
git pull                              # Check for remote changes
git push                              # Push your work
```

### Feature Development Workflow
```bash
git checkout -b feature-login         # Create feature branch
# ... make changes ...
git add .
git commit -m "feat: implement login"
git push -u origin feature-login      # Push feature branch
# Create pull request on GitHub
```

### Quick Fix Workflow
```bash
# ... editing files ...
git add -p                            # Interactively stage changes
git commit -m "fix: typo in docs"
git push
```

---

## Troubleshooting

### Forgot to configure name/email
```bash
# Error: "Please tell me who you are"
git config user.name "Your Name"
git config user.email "you@example.com"

# Fix last commit's author
git commit --amend --reset-author --no-edit
```

### Accidentally staged wrong files
```bash
# Unstage specific file
git reset HEAD file.txt

# Unstage all
git reset HEAD
```

### Want to see what's about to be pushed
```bash
git log origin/main..HEAD
git diff origin/main..HEAD
```

### Commit message typo
```bash
git commit --amend -m "fix: corrected commit message"
# Only if not pushed yet!
```

---

## Best Practices

1. **Commit early, commit often** - Small, frequent commits are better than large ones
2. **Pull before push** - Always check for remote changes first
3. **Write clear messages** - Use conventional commits format
4. **Review before staging** - Use `git status` and `git diff`
5. **Use .gitignore** - Prevent committing unnecessary files
6. **Don't commit secrets** - Never commit passwords, API keys, or credentials
7. **One logical change per commit** - Don't mix unrelated changes

## Related Sub-Skills

- Need to create a branch? → `/git/branching`
- Made a mistake? → `/git/undo`
- Need to push to GitHub? → `/git/remote`
- Have conflicts? → `/git/conflicts`

## Quick Command Reference

```bash
# Setup
git init                              # Initialize repository
git clone <url>                       # Clone repository
git config user.name "Name"           # Set name

# Basic workflow
git status                            # Check status
git add <file>                        # Stage file
git commit -m "message"               # Commit
git push                              # Push to remote
git pull                              # Pull from remote

# Information
git diff                              # See unstaged changes
git diff --staged                     # See staged changes
git log                               # View commit history
git log --oneline                     # Compact history

# .gitignore
echo "node_modules/" >> .gitignore    # Add to .gitignore
git rm --cached <file>                # Untrack file
```

---

**Last Updated:** 2025-02-11
**Version:** 1.0.0
