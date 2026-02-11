# Git Remote

**Parent Skill:** `/git`
**Path:** `/git/remote`

## Purpose
Master remote repository operations including adding remotes, fetching, pulling, pushing, managing multiple remotes (origin/upstream), and syncing forks.

## When to Use

**Trigger automatically when:**
- User mentions: remote, fetch, push, pull, origin, upstream, fork, sync
- Pushing code to GitHub/GitLab
- Syncing with team repository
- Managing multiple remotes
- Fork synchronization

**Chat commands:**
```bash
/git/remote push my branch to GitHub
/git/remote sync my fork with upstream
/git/remote what's the difference between fetch and pull
/git/remote add upstream repository
/git/remote force push safely
```

## Requirements

<critical>
- Git repository with at least one commit
- Remote repository access (GitHub, GitLab, Bitbucket)
- Authentication configured (SSH keys or HTTPS credentials)
- Network connectivity
- Push access for push operations
</critical>

## Verification
```bash
# Check remote configuration
git remote -v

# Test authentication
git ls-remote origin

# Check tracking branches
git branch -vv
```

---

## Critical Rules

<critical>
1. ALWAYS pull before push to avoid conflicts
2. NEVER force push to shared/main branches
3. ALWAYS use --force-with-lease instead of --force
4. NEVER commit credentials or secrets before pushing
5. ALWAYS verify remote URL before pushing
6. Use SSH for push access, HTTPS for read-only
</critical>

---

## Remote Workflow

```
Local Repository ←→ Remote Repository (origin)
                 ↑
                 └─→ Upstream Repository (for forks)

Commands:
fetch: Download changes (don't merge)
pull:  Download and merge (fetch + merge)
push:  Upload local commits
```

---

## Patterns

### Pattern 1: Add and Remove Remotes

**Problem:** Connect local repository to remote hosting

```bash
# ❌ BAD: Add remote without verification
git remote add origin https://github.com/user/repo.git
# Typo in URL? Won't know until push fails!

# ✅ GOOD: Add remote and verify
git remote add origin git@github.com:user/repo.git
git remote -v  # Verify URL
git ls-remote origin  # Test connection

# ✅ BETTER: Add with immediate fetch
git remote add origin git@github.com:user/repo.git
git fetch origin
```

**Remove remote:**
```bash
# Remove remote
git remote remove origin

# Or rename
git remote rename origin old-origin

# Update remote URL
git remote set-url origin git@github.com:user/new-repo.git
```

**Multiple remotes:**
```bash
# Add origin (your fork)
git remote add origin git@github.com:you/repo.git

# Add upstream (original repository)
git remote add upstream git@github.com:original/repo.git

# Verify
git remote -v
# origin    git@github.com:you/repo.git (fetch)
# origin    git@github.com:you/repo.git (push)
# upstream  git@github.com:original/repo.git (fetch)
# upstream  git@github.com:original/repo.git (push)
```

**Impact:** Proper remote configuration prevents errors

**When to use:**
- Cloning repository
- Forking projects
- Changing remote URLs
- Adding team repositories

---

### Pattern 2: Fetch vs Pull

**Problem:** Understand when to use fetch vs pull

```bash
# ❌ BAD: Pull without knowing what's coming
git pull  # Automatically merges! May cause conflicts

# ✅ GOOD: Fetch first, review, then merge
git fetch origin

# See what's new
git log HEAD..origin/main
git diff HEAD..origin/main

# Then decide to merge
git merge origin/main

# Or rebase
git rebase origin/main
```

**Fetch workflow:**
```bash
# Fetch all branches from origin
git fetch origin

# Fetch specific branch
git fetch origin main

# Fetch all remotes
git fetch --all

# Prune deleted branches
git fetch --prune
git fetch -p  # Short form
```

**Pull workflow:**
```bash
# Pull with merge (default)
git pull origin main

# Pull with rebase (cleaner history)
git pull --rebase origin main

# Pull current branch
git pull  # If upstream tracking set
```

**Configure default pull behavior:**
```bash
# Use merge (creates merge commit)
git config pull.rebase false

# Use rebase (linear history)
git config pull.rebase true

# Fail if can't fast-forward (safest)
git config pull.ff only
```

**Impact:** Control over when and how changes are integrated

**When to use:**
- **Fetch**: When you want to review changes first
- **Pull**: When you trust the changes (e.g., your own other branch)

---

### Pattern 3: Push to Remote

**Problem:** Upload local commits to remote repository

```bash
# ❌ BAD: Push without setting upstream
git push  # Error: no upstream branch

# ✅ GOOD: Push and set upstream tracking
git push -u origin feature-branch
# Now 'git push' works without arguments

# ✅ BETTER: Verify before push
git log origin/main..HEAD  # See what will be pushed
git diff origin/main..HEAD  # Review changes
git push -u origin feature-branch
```

**First push to new repository:**
```bash
# After initial commit
git branch -M main  # Rename to main
git remote add origin git@github.com:user/repo.git
git push -u origin main

# Now clone other computer and push works with:
git push
```

**Push different branch:**
```bash
# Push local branch to remote with different name
git push origin local-branch:remote-branch

# Push to different remote
git push upstream feature-branch
```

**Delete remote branch:**
```bash
# Delete remote branch
git push origin --delete feature-branch

# Old syntax (still works)
git push origin :feature-branch
```

**Impact:** Share work with team and backup code

**When to use:**
- Sharing feature branch
- Backing up work
- After completing feature
- End of work day

---

### Pattern 4: Track Remote Branches

**Problem:** Keep local branch in sync with remote

```bash
# ❌ BAD: Manual tracking
git branch feature-branch
git push origin feature-branch
# No tracking relationship!

# ✅ GOOD: Push with upstream tracking
git push -u origin feature-branch
# or
git push --set-upstream origin feature-branch

# Now these work:
git pull  # Pulls from origin/feature-branch
git push  # Pushes to origin/feature-branch
```

**Check tracking status:**
```bash
# See tracking info
git branch -vv
# * main        abc1234 [origin/main] Latest commit
#   feature     def5678 [origin/feature: ahead 2] Feature work

# Ahead/behind status
git status -sb
# ## main...origin/main [ahead 1, behind 2]
```

**Set tracking after creation:**
```bash
# Branch already exists
git branch --set-upstream-to=origin/main main

# Or
git branch -u origin/main main
```

**Checkout and track remote branch:**
```bash
# See remote branches
git branch -r

# Checkout remote branch (creates local tracking branch)
git switch feature-from-teammate
# Git automatically creates local branch tracking origin/feature-from-teammate

# Or explicit
git switch -c local-name origin/remote-branch
```

**Impact:** Simplified push/pull workflow

**When to use:**
- Creating feature branches
- Collaborating on branches
- Team workflows

---

### Pattern 5: Multiple Remotes (Origin & Upstream)

**Problem:** Manage fork and upstream repository

```bash
# ❌ BAD: Only origin configured
git remote -v
# origin  git@github.com:you/repo.git (fetch)
# origin  git@github.com:you/repo.git (push)
# Can't sync with upstream!

# ✅ GOOD: Both origin and upstream
# Fork on GitHub, then:
git clone git@github.com:you/repo.git
cd repo
git remote add upstream git@github.com:original/repo.git

git remote -v
# origin    git@github.com:you/repo.git (fetch)
# origin    git@github.com:you/repo.git (push)
# upstream  git@github.com:original/repo.git (fetch)
# upstream  git@github.com:original/repo.git (push)
```

**Workflow with fork:**
```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main  # or rebase
git push origin main

# Create feature from upstream
git fetch upstream
git checkout -b feature-x upstream/main

# Work on feature
git add .
git commit -m "feat: add feature"

# Push to your fork
git push -u origin feature-x

# Create PR from your fork to upstream
```

**Configure push/fetch separately:**
```bash
# Fetch from upstream, push to origin
git config remote.upstream.pushurl "DISABLE"

# Or set different URLs
git remote set-url --push upstream DISABLE
```

**Impact:** Proper fork workflow for open source

**When to use:**
- Contributing to open source
- Working with forked repositories
- Team members with forks

---

### Pattern 6: Force Push Safely

**Problem:** Need to force push after rebase/amend

```bash
# ❌ DANGEROUS: Force push
git push --force
# Can overwrite teammate's work!

# ✅ GOOD: Force with lease
git push --force-with-lease
# Fails if remote branch changed since last fetch

# ✅ BETTER: Force with lease on specific branch
git push --force-with-lease origin feature-branch
```

**When force push is OK:**
```bash
# After interactive rebase on YOUR branch
git rebase -i HEAD~3
git push --force-with-lease origin feature-branch

# After amending last commit
git commit --amend
git push --force-with-lease

# After fixing commits in PR
git rebase -i upstream/main
git push --force-with-lease origin pr-branch
```

**When force push is NOT OK:**
```bash
# ❌ NEVER force push to:
# - main or master branch
# - develop or release branches
# - Any branch others are using
# - Public branches

# If you must (emergency):
# 1. Communicate with team first!
# 2. Make sure everyone has pushed their work
# 3. Use --force-with-lease
# 4. Tell team to reset: git fetch && git reset --hard origin/main
```

**Safer alternatives:**
```bash
# Instead of force push, use revert
git revert HEAD
git push

# Or create new branch
git switch -c fixed-feature-branch
git push -u origin fixed-feature-branch
```

**Impact:** Prevent data loss from overwrites

**When to use:**
- After rebasing your feature branch
- After amending your commits
- Cleaning up PR before merge
- NEVER on shared branches

---

### Pattern 7: Sync Fork with Upstream

**Problem:** Keep forked repository up to date

```bash
# ❌ BAD: Manually download and push
# Download zip from upstream
# Extract and copy files
# Commit and push
# This loses Git history!

# ✅ GOOD: Proper sync workflow
# One-time setup
git remote add upstream git@github.com:original/repo.git

# Sync workflow (do regularly)
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# ✅ BETTER: Sync with rebase (cleaner)
git fetch upstream
git checkout main
git rebase upstream/main
git push --force-with-lease origin main
# Only if no one else uses your fork's main!
```

**Sync feature branch:**
```bash
# Update your feature with upstream changes
git fetch upstream
git checkout feature-branch
git rebase upstream/main
git push --force-with-lease origin feature-branch
```

**GitHub web UI sync:**
```bash
# Can also use "Sync fork" button on GitHub
# Then locally:
git checkout main
git pull origin main
```

**Automated sync:**
```bash
# Create alias
git config alias.sync-fork '!git fetch upstream && git checkout main && git merge upstream/main && git push origin main'

# Use:
git sync-fork
```

**Impact:** Stay current with upstream project

**When to use:**
- Before starting new feature
- Regularly (weekly/monthly)
- Before creating pull request
- Resolving merge conflicts

---

### Pattern 8: Remote Branch Management

**Problem:** Manage remote branches efficiently

```bash
# ❌ BAD: Let remote branches accumulate
git branch -r
# origin/feature-1
# origin/feature-2
# ... 50 old branches ...

# ✅ GOOD: Regular cleanup
# See merged branches
git branch -r --merged main

# Delete remote branches (after PR merged)
git push origin --delete feature-1
git push origin --delete feature-2

# Prune local references to deleted remote branches
git fetch --prune
# or
git remote prune origin
```

**Bulk operations:**
```bash
# List all remote branches
git ls-remote --heads origin

# Delete multiple remote branches
git push origin --delete branch1 branch2 branch3

# Prune and show what was removed
git fetch --prune --verbose
```

**Protected branches:**
```bash
# Some branches can't be deleted (GitHub/GitLab settings)
# main, develop usually protected

# Check branch protection (GitHub CLI)
gh api repos/:owner/:repo/branches/main/protection
```

**Mirror repository:**
```bash
# Clone with all branches
git clone --mirror git@github.com:user/repo.git

# Push to different remote
cd repo.git
git push --mirror git@gitlab.com:user/repo.git
```

**Impact:** Clean, organized remote repository

**When to use:**
- After PRs merged
- Regular maintenance
- Repository cleanup
- Migrating repositories

---

## Common Workflows

### Daily Team Collaboration
```bash
# Start of day
git fetch origin
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature-new
# ... work ...
git push -u origin feature-new

# Later: Sync with main
git fetch origin
git rebase origin/main
git push --force-with-lease origin feature-new

# After PR merged
git checkout main
git pull origin main
git branch -d feature-new
git push origin --delete feature-new
```

### Open Source Contribution
```bash
# One-time setup
git clone git@github.com:you/forked-repo.git
cd forked-repo
git remote add upstream git@github.com:original/repo.git

# Before starting work
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Create feature
git checkout -b feature-contribution
# ... work ...
git push -u origin feature-contribution

# Create PR on GitHub from your fork
```

### Deploy to Production
```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Tag release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Push to production remote
git push production main
```

---

## Troubleshooting

### Push rejected (non-fast-forward)
```bash
# Error: Updates were rejected

# Option 1: Pull and merge
git pull origin main
git push origin main

# Option 2: Pull with rebase
git pull --rebase origin main
git push origin main

# Option 3: Check if you should force push
git push --force-with-lease origin feature-branch
```

### Authentication failed
```bash
# HTTPS credentials
git config credential.helper store
git pull  # Will prompt for password once

# SSH key issues
ssh -T git@github.com  # Test SSH
ssh-add ~/.ssh/id_ed25519  # Add key to agent

# Switch from HTTPS to SSH
git remote set-url origin git@github.com:user/repo.git
```

### Wrong remote URL
```bash
# Check current URL
git remote -v

# Update URL
git remote set-url origin git@github.com:correct-user/repo.git

# Verify
git remote -v
git ls-remote origin
```

### Lost tracking branch
```bash
# Re-establish tracking
git branch --set-upstream-to=origin/main main

# Or delete and recreate
git branch -d feature
git fetch origin
git checkout feature  # Auto-tracks origin/feature
```

---

## Best Practices

1. **Pull before push** - Always fetch/pull before pushing
2. **Use SSH for push** - More secure than HTTPS
3. **Verify remotes** - Check remote URLs are correct
4. **Fetch regularly** - Stay aware of team changes
5. **Clean up branches** - Delete merged branches
6. **Force push carefully** - Use --force-with-lease only on your branches
7. **Tag releases** - Use tags for version milestones
8. **Sync forks regularly** - Keep upstream in sync

## Related Sub-Skills

- Need to handle push conflicts? → `/git/conflicts`
- Need to undo pushed commits? → `/git/undo`
- Setting up team workflow? → `/git/workflows`
- Managing branches? → `/git/branching`

## Quick Command Reference

```bash
# Remotes
git remote add origin <url>              # Add remote
git remote -v                            # List remotes
git remote remove origin                 # Remove remote

# Fetch/Pull
git fetch origin                         # Download changes
git pull origin main                     # Fetch and merge
git pull --rebase                        # Pull with rebase

# Push
git push -u origin branch                # Push with tracking
git push --force-with-lease              # Safe force push
git push origin --delete branch          # Delete remote branch

# Tracking
git branch -vv                           # Show tracking
git branch -u origin/main                # Set upstream

# Multiple remotes
git remote add upstream <url>            # Add upstream
git fetch upstream                       # Fetch from upstream
git merge upstream/main                  # Merge upstream

# Cleanup
git fetch --prune                        # Remove stale references
git remote prune origin                  # Prune remote
```

---

**Last Updated:** 2025-02-11
**Version:** 1.0.0
