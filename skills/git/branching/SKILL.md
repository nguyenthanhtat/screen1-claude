# Git Branching

**Parent Skill:** `/git`
**Path:** `/git/branching`

## Purpose
Master branch management including creating, merging, rebasing, and organizing branches for clean workflows. Learn merge strategies, interactive rebase, and branch naming conventions.

## When to Use

**Trigger automatically when:**
- User mentions: branch, checkout, merge, rebase, switch, delete branch
- Creating new features
- Integrating changes
- Cleaning up branch history
- Branch organization questions

**Chat commands:**
```bash
/git/branching create new feature branch
/git/branching merge feature into main
/git/branching rebase my branch on main
/git/branching delete old branches
/git/branching interactive rebase to clean history
```

## Requirements

<critical>
- Git 2.30+ installed
- Repository with at least one commit
- Understanding of current branch
- For remote branches: Push access configured
</critical>

## Verification
```bash
# Check current branch
git branch --show-current

# List all branches
git branch -a

# Check if branch exists
git rev-parse --verify feature-branch
```

---

## Critical Rules

<critical>
1. ALWAYS commit or stash changes before switching branches
2. NEVER delete branches with unmerged changes (without confirmation)
3. ALWAYS pull before merging to avoid conflicts
4. NEVER rebase public/shared branches (only rebase your own branches)
5. ALWAYS verify you're on the correct branch before making commits
6. Use meaningful branch names (feature/*, fix/*, etc.)
</critical>

---

## Branching Workflow

```
main (production)
  ├── feature/user-auth
  ├── feature/dashboard
  └── fix/login-bug

Workflow:
1. Create branch from main
2. Make commits on branch
3. Merge or rebase to integrate
4. Delete branch after merge
```

---

## Patterns

### Pattern 1: Create and Switch Branches

**Problem:** Start working on a new feature without affecting main code

```bash
# ❌ BAD: Old syntax, easy to make mistakes
git branch feature-login
git checkout feature-login  # Two commands

# Or worse:
git checkout -b feature-login  # Creates locally only

# ✅ GOOD: Modern syntax (Git 2.23+)
git switch -c feature-login
# or
git switch --create feature-login

# ✅ BETTER: Create from specific branch
git switch -c feature-login main  # Create from main

# Create from remote branch
git switch -c local-name origin/remote-branch
```

**Switch to existing branch:**
```bash
# Old way
git checkout feature-login

# New way (clearer)
git switch feature-login

# Create branch from specific commit
git switch -c fix-bug abc1234
```

**Impact:** Clean separation of features, safe experimentation

**When to use:**
- Starting new feature
- Creating hotfix
- Experimenting with changes
- Every time you start a new unit of work

---

### Pattern 2: Merge Branches

**Problem:** Integrate feature branch changes into main branch

**Fast-Forward Merge** (when possible):
```bash
# ❌ BAD: Merge without updating main first
git switch main
git merge feature-login  # May create conflicts

# ✅ GOOD: Update main first, then merge
git switch main
git pull origin main           # Get latest changes
git merge feature-login        # Fast-forward if possible

# If fast-forward:
# main:     A---B---C
#                    \
# feature:            D---E
# After merge:
# main:     A---B---C---D---E
```

**Three-Way Merge** (when branches diverged):
```bash
# ✅ GOOD: Merge with commit message
git switch main
git pull origin main
git merge feature-login -m "feat: merge user login feature

Includes:
- JWT authentication
- Login form validation
- Session management"

# Creates merge commit:
# main:     A---B---C-------F (merge commit)
#                    \     /
# feature:            D---E
```

**Merge strategies:**
```bash
# No fast-forward (always create merge commit)
git merge --no-ff feature-login

# Squash all commits (cleaner history)
git merge --squash feature-login
git commit -m "feat: add login feature"

# Abort merge if conflicts
git merge --abort
```

**Impact:** Integrate work while preserving history

**When to use:**
- Feature complete and tested
- Ready to deploy
- Integrating release branches
- Merging pull requests

---

### Pattern 3: Rebase for Linear History

**Problem:** Keep clean, linear commit history without merge commits

```bash
# ❌ BAD: Merge creates messy history
git switch feature-login
git merge main  # Creates merge commit on feature branch

# ✅ GOOD: Rebase feature on top of main
git switch feature-login
git fetch origin main
git rebase origin/main

# Before rebase:
# main:     A---B---C---F
# feature:  A---B---D---E
#
# After rebase:
# main:     A---B---C---F
# feature:              D'---E' (commits rewritten)
```

**Handling rebase conflicts:**
```bash
git rebase main
# CONFLICT in file.js

# Fix conflicts in file.js
git add file.js
git rebase --continue

# Or skip this commit
git rebase --skip

# Or abort rebase
git rebase --abort
```

**Rebase vs Merge decision:**
```bash
# Use REBASE when:
# - Working on your own feature branch
# - Want linear history
# - Before creating pull request

# Use MERGE when:
# - Integrating to main/shared branch
# - Want to preserve exact history
# - Multiple people working on branch
```

**Impact:** Cleaner, linear history that's easier to understand

**When to use:**
- Before creating pull request
- Updating feature branch with main
- Cleaning up local commits
- Never on public/shared branches

---

### Pattern 4: Interactive Rebase (Clean Up Commits)

**Problem:** Multiple messy commits before merging

```bash
# ❌ BAD: Merge with messy commits
# Commit history:
# - "fix typo"
# - "fix another typo"
# - "actually fix it"
# - "add feature"

# ✅ GOOD: Interactive rebase to clean up
git rebase -i HEAD~4  # Last 4 commits

# Editor opens with:
# pick abc1234 add feature
# pick def5678 fix typo
# pick ghi9012 fix another typo
# pick jkl3456 actually fix it

# Change to:
# pick abc1234 add feature
# fixup def5678 fix typo
# fixup ghi9012 fix another typo
# fixup jkl3456 actually fix it

# Result: One clean commit!
```

**Interactive rebase commands:**
```bash
# p, pick = use commit
# r, reword = use commit, edit message
# e, edit = use commit, stop to amend
# s, squash = combine with previous, edit message
# f, fixup = combine with previous, discard message
# d, drop = remove commit
```

**Reorder commits:**
```bash
git rebase -i HEAD~5

# Change order in editor:
# pick aaa commit 3
# pick bbb commit 1
# pick ccc commit 2
# Commits will be reordered
```

**Split a commit:**
```bash
git rebase -i HEAD~3
# Change 'pick' to 'edit' for commit to split

# When rebase stops:
git reset HEAD^        # Undo the commit
git add file1.js
git commit -m "feat: add file1"
git add file2.js
git commit -m "feat: add file2"
git rebase --continue
```

**Impact:** Clean, professional commit history for pull requests

**When to use:**
- Before creating PR
- Fixing commit messages
- Combining multiple "WIP" commits
- Reordering commits logically

---

### Pattern 5: Delete Branches

**Problem:** Clean up old branches after merging

```bash
# ❌ BAD: Delete without checking merge status
git branch -D feature-login  # Force delete, may lose work!

# ✅ GOOD: Safe delete (merged branches only)
git branch -d feature-login  # Errors if not merged

# If you see: "error: The branch 'feature-login' is not fully merged"
# Check if really merged:
git branch --merged main
git branch --no-merged main

# If safe to delete:
git branch -D feature-login  # Force delete
```

**Delete remote branch:**
```bash
# Delete local branch
git branch -d feature-login

# Delete remote branch
git push origin --delete feature-login

# Or (older syntax):
git push origin :feature-login
```

**Bulk cleanup:**
```bash
# Delete all merged branches
git branch --merged main | grep -v "\* main" | xargs -n 1 git branch -d

# Prune remote tracking branches (deleted on remote)
git fetch --prune

# Or
git remote prune origin
```

**Impact:** Keep repository organized, avoid confusion

**When to use:**
- After feature merged to main
- After PR merged and closed
- Cleaning up old experiments
- Regular repository maintenance

---

### Pattern 6: Branch Naming Conventions

**Problem:** Inconsistent branch names cause confusion

```bash
# ❌ BAD: Vague, inconsistent names
git switch -c fix
git switch -c new-stuff
git switch -c test123

# ✅ GOOD: Descriptive, conventional names
git switch -c feature/user-authentication
git switch -c fix/login-validation-bug
git switch -c hotfix/security-patch-CVE-2024-001
git switch -c docs/api-documentation
git switch -c refactor/extract-auth-service
```

**Naming patterns:**
```bash
# Features
feature/user-profile
feature/payment-integration
feat/dashboard-analytics

# Bug fixes
fix/null-pointer-in-login
bugfix/email-validation
fix/issue-123

# Hotfixes (urgent production fixes)
hotfix/critical-security-patch
hotfix/payment-failure

# Documentation
docs/api-endpoints
docs/readme-update

# Refactoring
refactor/extract-validation
refactor/optimize-queries

# Experiments
experiment/new-ui-framework
spike/performance-optimization
```

**With issue numbers:**
```bash
git switch -c feature/123-add-user-auth
git switch -c fix/456-email-validation
```

**Impact:** Clear organization, easier collaboration

**When to use:**
- Creating any branch
- Team collaborations
- Open source projects
- Automated workflows

---

### Pattern 7: Track Remote Branches

**Problem:** Work with branches from remote repository

```bash
# ❌ BAD: Manually create and track
git branch feature-login
git push origin feature-login
git branch --set-upstream-to=origin/feature-login

# ✅ GOOD: Create and push with tracking
git switch -c feature-login
git push -u origin feature-login
# -u sets upstream tracking

# Now you can use:
git pull    # Pulls from origin/feature-login
git push    # Pushes to origin/feature-login
```

**Checkout remote branch:**
```bash
# See all remote branches
git branch -r

# Create local branch tracking remote
git switch feature-from-teammate
# Git automatically creates local branch from origin/feature-from-teammate

# Or explicit:
git switch -c local-name origin/remote-branch
```

**Update remote tracking:**
```bash
# See tracking status
git branch -vv

# Set upstream for existing branch
git branch --set-upstream-to=origin/main main

# Push and set upstream
git push -u origin current-branch
```

**Impact:** Seamless collaboration with team

**When to use:**
- Sharing feature branches
- Collaborating on same branch
- Code review workflows

---

### Pattern 8: Merge Strategies

**Problem:** Choose appropriate merge strategy for situation

**Strategy 1: Fast-Forward (default)**
```bash
# When feature branch is ahead of main
git merge feature-login

# Only if main hasn't changed:
# main:     A---B
# feature:  A---B---C---D
# Result:   A---B---C---D (main moves forward)
```

**Strategy 2: No-Fast-Forward (preserve branch)**
```bash
# Always create merge commit (shows feature was a branch)
git merge --no-ff feature-login

# main:     A---B-------E (merge commit)
#                \     /
# feature:        C---D
```

**Strategy 3: Squash Merge (single commit)**
```bash
# Combine all feature commits into one
git merge --squash feature-login
git commit -m "feat: add complete login feature"

# All changes from feature applied, but as one commit
# Good for: messy feature branches, keeping main clean
```

**Strategy 4: Rebase and Merge**
```bash
# On feature branch
git rebase main
git switch main
git merge feature-login  # Fast-forward

# Result: Linear history
```

**Strategy 5: Ours/Theirs (conflict resolution)**
```bash
# Take all changes from current branch
git merge -X ours feature-branch

# Take all changes from merging branch
git merge -X theirs feature-branch

# Use with caution!
```

**Decision matrix:**
```
Use FAST-FORWARD when:
- Simple feature, main unchanged
- Want minimal commit overhead

Use NO-FF when:
- Want to preserve branch context
- Important to see feature as unit
- GitHub/GitLab default

Use SQUASH when:
- Feature has messy commits
- Want single commit per feature
- Keep main branch clean

Use REBASE then MERGE when:
- Want linear history
- Feature branch is private
- Clean commit history
```

**Impact:** Appropriate history for your workflow

**When to use:**
- Integrating features
- Release management
- Different team workflows

---

## Common Workflows

### Feature Branch Workflow
```bash
# Create feature branch
git switch -c feature/user-login

# Make commits
git add src/auth.js
git commit -m "feat: add login endpoint"

# Update with main
git fetch origin main
git rebase origin/main

# Push feature branch
git push -u origin feature/user-login

# Create PR on GitHub
# After PR approved:
git switch main
git pull origin main
# PR was merged, delete local branch
git branch -d feature/user-login
```

### Hotfix Workflow
```bash
# Create hotfix from main
git switch main
git pull origin main
git switch -c hotfix/critical-bug

# Fix and commit
git add src/fix.js
git commit -m "fix: resolve critical security issue"

# Merge to main
git switch main
git merge --no-ff hotfix/critical-bug
git push origin main

# Merge to develop (if using Git Flow)
git switch develop
git merge --no-ff hotfix/critical-bug

# Delete hotfix branch
git branch -d hotfix/critical-bug
```

### Experiment Workflow
```bash
# Create experiment branch
git switch -c experiment/new-architecture

# Make experimental changes
# ... lots of commits ...

# If successful:
git switch main
git merge --squash experiment/new-architecture
git commit -m "refactor: new architecture implementation"

# If failed:
git switch main
git branch -D experiment/new-architecture  # Delete without merging
```

---

## Troubleshooting

### Can't switch branches (uncommitted changes)
```bash
# Error: "Please commit your changes or stash them"

# Option 1: Commit changes
git add .
git commit -m "WIP: work in progress"

# Option 2: Stash changes
git stash
git switch other-branch
# Later:
git switch back
git stash pop
```

### Accidentally committed to wrong branch
```bash
# Committed to main instead of feature branch
git switch -c feature-branch  # Create branch from current state
git switch main
git reset --hard HEAD~1        # Undo commit on main
git switch feature-branch      # Commit is now on feature branch
```

### Need to rename branch
```bash
# Rename local branch
git branch -m old-name new-name

# If on the branch:
git branch -m new-name

# Rename remote branch:
git push origin :old-name new-name
git push origin -u new-name
```

### Merge conflict
```bash
# During merge
git merge feature-branch
# CONFLICT...

# See conflicted files
git status

# Resolve conflicts, then:
git add resolved-file.js
git commit  # Complete merge

# Or abort:
git merge --abort
```

---

## Best Practices

1. **Branch early, branch often** - Create branch for every feature/fix
2. **One purpose per branch** - Don't mix features
3. **Keep branches short-lived** - Merge or delete within days
4. **Update from main frequently** - Avoid large conflicts
5. **Clean up after merge** - Delete merged branches
6. **Use meaningful names** - Follow naming conventions
7. **Rebase before PR** - Clean up commits
8. **Don't rebase public branches** - Only rebase your own branches

## Related Sub-Skills

- Need to resolve conflicts? → `/git/conflicts`
- Need to undo branch changes? → `/git/undo`
- Need to push branch to remote? → `/git/remote`
- Setting up workflow? → `/git/workflows`

## Quick Command Reference

```bash
# Create branch
git switch -c branch-name              # Create and switch
git switch -c new-branch main          # Create from main

# Switch branch
git switch branch-name                 # Switch to branch
git switch -                           # Switch to previous branch

# List branches
git branch                             # Local branches
git branch -r                          # Remote branches
git branch -a                          # All branches

# Merge
git merge branch-name                  # Merge branch
git merge --no-ff branch-name          # No fast-forward
git merge --squash branch-name         # Squash merge

# Rebase
git rebase main                        # Rebase on main
git rebase -i HEAD~3                   # Interactive rebase

# Delete
git branch -d branch-name              # Delete merged branch
git branch -D branch-name              # Force delete
git push origin --delete branch-name   # Delete remote branch

# Info
git branch --show-current              # Current branch name
git branch -vv                         # Tracking info
```

---

**Last Updated:** 2025-02-11
**Version:** 1.0.0
