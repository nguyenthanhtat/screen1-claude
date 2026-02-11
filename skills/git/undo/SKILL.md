# Git Undo

**Parent Skill:** `/git`
**Path:** `/git/undo`

## Purpose
Master undoing changes at every stage: unstage files, discard working changes, amend commits, reset history, revert safely, and recover lost commits with reflog.

## When to Use

**Trigger automatically when:**
- User mentions: undo, reset, revert, restore, reflog, recover, amend, rollback
- Made mistake in commit
- Need to unstage files
- Want to discard changes
- Recover deleted commits
- Fix commit history

**Chat commands:**
```bash
/git/undo unstage this file
/git/undo discard my local changes
/git/undo fix my last commit message
/git/undo undo last commit but keep changes
/git/undo recover deleted commit
```

## Requirements

<critical>
- Git repository with commit history (for most operations)
- Understanding of Git states (working/staging/committed)
- For recovery: Commits not garbage collected yet
- CAUTION: Some operations destructive and irreversible
</critical>

## Verification
```bash
# Check current state
git status

# See commit history
git log --oneline -5

# Check reflog (for recovery)
git reflog
```

---

## Critical Rules

<critical>
1. NEVER use `git reset --hard` without backup if unsure
2. NEVER force push reset to shared branches
3. ALWAYS verify what will be affected before undo
4. Use `git revert` for public history (not reset)
5. ALWAYS check `git status` before major undo operations
6. Reflog expires after 90 days - recover deleted commits ASAP
</critical>

---

## Undo Workflow

```
File States & Undo Commands:

Working Directory → Staging → Repository
   (modified)       (staged)   (committed)
       ↓               ↓            ↓
 git restore      git restore   git reset
                   --staged    or git revert

Recovery: git reflog (for any deleted commits)
```

---

## Patterns

### Pattern 1: Unstage Files (Restore --staged)

**Problem:** Staged file by mistake

```bash
# ❌ BAD: Old confusing syntax
git reset HEAD file.js  # Works but unclear

# ✅ GOOD: Modern, clear syntax (Git 2.23+)
git restore --staged file.js

# Unstage all files
git restore --staged .

# Unstage specific files
git restore --staged src/app.js src/utils.js
```

**Before and after:**
```bash
# Accidentally staged everything
git add .
git status
# Changes to be committed:
#   modified: src/app.js
#   modified: .env  # Oops! Secret file!

# Unstage .env
git restore --staged .env

git status
# Changes to be committed:
#   modified: src/app.js
# Changes not staged:
#   modified: .env  # Back to unstaged
```

**Old vs new syntax:**
```bash
# Old way (still works)
git reset HEAD file.js

# New way (clearer intent)
git restore --staged file.js

# Both do same thing: unstage file
```

**Impact:** Remove file from staging without losing changes

**When to use:**
- Staged wrong file
- Want to commit files separately
- Accidentally staged secrets
- Reviewing what to commit

---

### Pattern 2: Discard Working Directory Changes (Restore)

**Problem:** Don't want local modifications

```bash
# ❌ DANGEROUS: Old confusing syntax
git checkout -- file.js  # Confusing with branch checkout

# ✅ GOOD: Modern, clear syntax
git restore file.js

# Discard all changes
git restore .

# Discard specific files
git restore src/app.js src/utils.js

# Interactive discard (choose hunks)
git restore -p file.js
```

**Warning - This is destructive!**
```bash
# Before restore
git status
# Changes not staged for commit:
#   modified: src/app.js  # Hours of work!

# ❌ DANGER: Lost forever if not staged!
git restore src/app.js

# After restore: changes gone!
git status
# nothing to commit, working tree clean

# CANNOT UNDO THIS! Changes lost!
```

**Safe workflow:**
```bash
# Save changes first (just in case)
git stash

# Or commit to temporary branch
git checkout -b backup-$(date +%Y%m%d-%H%M%S)
git add .
git commit -m "Backup before restore"
git checkout original-branch

# Then restore if still needed
git restore file.js
```

**Restore from specific commit:**
```bash
# Restore file from specific commit
git restore --source=abc1234 file.js

# Restore from main branch
git restore --source=main file.js

# Restore file to staged state
git restore --staged --worktree file.js
```

**Impact:** Clean working directory, but changes lost

**When to use:**
- Experimental changes failed
- Want to start over
- Undo local edits
- Match repository state

---

### Pattern 3: Amend Last Commit

**Problem:** Typo in commit message or forgot to include file

```bash
# ❌ BAD: Create new commit for minor fix
git commit -m "Add user authentification"  # Typo!
git commit -m "Fix typo in commit message"  # Messy history

# ✅ GOOD: Amend last commit
git commit -m "Add user authentification"  # Typo!
# Fix: Amend instead
git commit --amend -m "Add user authentication"
```

**Forgot to include file:**
```bash
# Made commit
git commit -m "Add user authentication"

# Oops, forgot a file!
git add src/forgot-this.js

# Add to last commit
git commit --amend --no-edit
# --no-edit keeps same message
```

**Change last commit message:**
```bash
# Change message interactively
git commit --amend
# Editor opens, change message, save

# Change message inline
git commit --amend -m "New commit message"
```

**After amend:**
```bash
# If already pushed (careful!)
git push --force-with-lease origin feature-branch

# If NOT pushed yet:
git push -u origin feature-branch
```

**Amend author:**
```bash
# Change last commit author
git commit --amend --author="Name <email@example.com>"

# Use configured user
git commit --amend --reset-author
```

**Impact:** Clean up last commit without extra commits

**When to use:**
- Typo in commit message
- Forgot to include file
- Wrong author
- Before pushing (safe)
- After pushing own branch (with force-with-lease)

---

### Pattern 4: Reset (Soft, Mixed, Hard)

**Problem:** Undo commits with different levels

```bash
# Three types of reset:
# --soft:  Undo commit, keep staged
# --mixed: Undo commit, unstage (default)
# --hard:  Undo commit, discard changes
```

**Soft reset (keep changes staged):**
```bash
# Undo last commit, keep changes in staging
git reset --soft HEAD~1

# Before:
# Commit: abc1234 "Add feature"
# Status: Working directory clean

# After:
# Commit: def5678 (previous commit)
# Status: All changes from abc1234 are staged

# Use case: Redo commit with different message
git reset --soft HEAD~1
git commit -m "Better commit message"
```

**Mixed reset (unstage changes):**
```bash
# Undo last commit, unstage changes (default)
git reset HEAD~1
# Same as:
git reset --mixed HEAD~1

# Before:
# Commit: abc1234 "Add feature"

# After:
# Commit: def5678
# Status: Changes from abc1234 are unstaged

# Use case: Reorganize changes into multiple commits
git reset HEAD~1
git add src/feature-a.js
git commit -m "Add feature A"
git add src/feature-b.js
git commit -m "Add feature B"
```

**Hard reset (discard everything):**
```bash
# ❌ DANGER: Undo commit AND discard changes
git reset --hard HEAD~1

# Before:
# Commit: abc1234 "Add feature"

# After:
# Commit: def5678
# Status: All changes from abc1234 GONE!

# ⚠️ CANNOT UNDO! (unless using reflog)
```

**Reset to specific commit:**
```bash
# Reset to specific commit hash
git reset --hard abc1234

# Reset to remote state
git reset --hard origin/main

# Reset to 5 commits ago
git reset --hard HEAD~5
```

**Impact:** Undo commits with control over what's kept

**When to use:**
- Reorganize commits (soft/mixed)
- Undo commits on private branch
- Start over from specific point (hard)
- Never on public branches!

---

### Pattern 5: Revert (Safe Public Undo)

**Problem:** Undo commit that's already pushed/shared

```bash
# ❌ BAD: Reset public branch
git reset --hard HEAD~1
git push --force origin main  # Breaks others' work!

# ✅ GOOD: Revert (creates new commit)
git revert HEAD

# Creates new commit that undoes changes
# Commit history:
# abc1234 - Add feature
# def5678 - Revert "Add feature"  ← New commit
```

**Revert specific commit:**
```bash
# Revert by hash
git revert abc1234

# Revert with custom message
git revert abc1234 -m "Revert feature due to bug #123"

# Revert without auto-commit (review first)
git revert abc1234 --no-commit
git status  # Review changes
git commit -m "Revert feature - found security issue"
```

**Revert multiple commits:**
```bash
# Revert range (inclusive)
git revert abc1234..def5678

# Revert each commit individually
git revert HEAD~3..HEAD

# Revert last 3 commits
git revert HEAD~3 HEAD~2 HEAD~1
```

**Revert merge commit:**
```bash
# Merge commits have two parents
# Must specify which parent to revert to

# -m 1: Keep first parent (usually main)
git revert -m 1 merge-commit-hash

# Example:
git revert -m 1 HEAD  # Revert last merge
```

**Impact:** Safe undo for public history

**When to use:**
- Undo commit on main/shared branch
- Production hotfix (revert bad deploy)
- Preserve history (audit trail)
- Safe collaborative undo

---

### Pattern 6: Recover Deleted Commits (Reflog)

**Problem:** Accidentally deleted commits, need recovery

```bash
# ❌ PANIC: "I lost my work!"
git reset --hard HEAD~5  # Deleted 5 commits!
git log  # Commits are gone!

# ✅ SOLUTION: Reflog saves you!
git reflog
# abc1234 HEAD@{0}: reset: moving to HEAD~5
# def5678 HEAD@{1}: commit: Feature work  ← Lost commit!
# ghi9012 HEAD@{2}: commit: More work     ← Lost commit!

# Recover to specific state
git reset --hard HEAD@{1}
# or
git reset --hard def5678

# Commits recovered!
```

**View reflog:**
```bash
# See all operations
git reflog

# See last 10
git reflog -10

# See specific branch reflog
git reflog show feature-branch

# See with dates
git reflog --date=relative
git reflog --date=iso
```

**Recover deleted branch:**
```bash
# Deleted branch
git branch -D feature-branch
# Error: branch deleted!

# Find last commit
git reflog | grep feature-branch
# abc1234 HEAD@{5}: checkout: moving from feature-branch to main

# Recreate branch
git branch feature-branch abc1234
git checkout feature-branch
# Branch recovered!
```

**Reflog for specific operations:**
```bash
# Find when file was deleted
git reflog -- path/to/file.js

# Find all commits
git reflog show --all

# Find specific commit message
git reflog | grep "important feature"
```

**Impact:** Recover "lost" commits and branches

**When to use:**
- Accidentally reset
- Deleted branch
- Lost commits after rebase
- Any "oops" moment
- Within 90 days (default reflog expiry)

---

### Pattern 7: Undo Pushed Commits

**Problem:** Pushed commits that need to be undone

```bash
# ❌ BAD: Reset and force push
git reset --hard HEAD~3
git push --force origin main  # Dangerous for team!

# ✅ GOOD: Revert pushed commits
git revert HEAD~3..HEAD
git push origin main

# Or revert individually
git revert HEAD
git revert HEAD~1
git revert HEAD~2
git push origin main
```

**For your own branch:**
```bash
# If it's your feature branch (not shared)
git reset --hard HEAD~2
git push --force-with-lease origin feature-branch

# Safe because:
# 1. Your branch only
# 2. Not sharing with others
# 3. Using --force-with-lease
```

**For shared branch (proper procedure):**
```bash
# Step 1: Communicate with team
# "I'm reverting commits abc-def on main"

# Step 2: Revert commits
git revert abc1234..def5678

# Step 3: Push
git push origin main

# Step 4: Tell team to pull
# "Pull latest main, bad commits reverted"
```

**Emergency rollback:**
```bash
# Production is broken, must rollback NOW

# Option 1: Revert merge
git revert -m 1 HEAD  # Revert last merge
git push origin main

# Option 2: Revert to specific commit
git revert --no-commit HEAD~5..HEAD
git commit -m "Emergency rollback to stable version"
git push origin main

# Option 3: Create tag, then revert
git tag broken-version
git revert -m 1 HEAD
git push origin main
git push origin broken-version  # For investigation later
```

**Impact:** Safe undo even after pushing

**When to use:**
- Bug found in production
- Reverting bad merge
- Undoing public commits
- Team collaboration

---

### Pattern 8: Reset vs Revert Decision Guide

**Problem:** Which undo method to use?

**Decision tree:**
```
Is commit pushed/shared?
├─ No → Use RESET (clean history)
│   ├─ Want to keep changes? → git reset --soft HEAD~1
│   ├─ Want to unstage? → git reset HEAD~1
│   └─ Want to discard? → git reset --hard HEAD~1
│
└─ Yes → Use REVERT (safe public undo)
    ├─ Single commit → git revert abc1234
    ├─ Multiple commits → git revert abc1234..def5678
    └─ Merge commit → git revert -m 1 merge-hash
```

**Comparison table:**

| Operation | Reset | Revert |
|-----------|-------|--------|
| Changes history | Yes | No |
| Creates new commit | No | Yes |
| Safe for public branches | ❌ No | ✅ Yes |
| Removes from history | ✅ Yes | ❌ No |
| Undoes specific commit | ❌ Harder | ✅ Easy |
| Can recover with reflog | ✅ Yes | N/A |

**Examples:**

```bash
# Local experiment failed
git reset --hard HEAD~5  # OK: Not pushed

# Production bug
git revert HEAD  # CORRECT: Already pushed

# Reorganize commits before PR
git reset --soft HEAD~3  # OK: Your branch
git commit  # Combine into one commit

# Undo commit on main
git revert abc1234  # CORRECT: Shared branch
```

**Impact:** Choose correct undo method

**When to use:**
- Reset: Private branches, local work
- Revert: Public branches, shared work

---

## Common Workflows

### Fix Commit Message Typo
```bash
git commit -m "Add authentification"  # Typo!
git commit --amend -m "Add authentication"
git push --force-with-lease origin feature-branch
```

### Reorganize Last 3 Commits
```bash
git reset --soft HEAD~3
# All changes now staged
git add src/feature-a.js
git commit -m "Add feature A"
git add src/feature-b.js
git commit -m "Add feature B"
git push --force-with-lease origin feature-branch
```

### Recover Deleted Branch
```bash
git branch -D feature-branch  # Oops!
git reflog | grep feature-branch
# Find commit: abc1234
git checkout -b feature-branch abc1234
```

### Revert Production Bug
```bash
git checkout main
git pull origin main
git revert abc1234  # Bad commit
git push origin main
```

### Undo Local Uncommitted Changes
```bash
# Save first (optional)
git stash

# Discard all changes
git restore .

# Or specific file
git restore src/app.js
```

---

## Troubleshooting

### Amend after push
```bash
# Error: Updates were rejected

# If your branch only:
git push --force-with-lease origin feature-branch

# If shared:
# Don't amend! Create new commit instead
```

### Can't find commit in reflog
```bash
# Reflog expires after 90 days

# Check if still exists
git fsck --lost-found

# Recover from lost+found
ls .git/lost-found/commit/
git show <hash>
git branch recovered-branch <hash>
```

### Reset wrong commit
```bash
# Used reset but meant different commit
git reflog
# Find pre-reset state
git reset --hard HEAD@{1}
```

### Revert created conflict
```bash
# Revert may conflict with newer changes
git revert abc1234
# CONFLICT!

# Resolve conflict
git add resolved-file.js
git revert --continue
```

---

## Best Practices

1. **Check status first** - Always `git status` before major undo
2. **Prefer revert for public** - Use revert on shared branches
3. **Reset for private only** - Only reset on your own branches
4. **Backup before hard reset** - Create branch or stash
5. **Amend before push** - OK to amend local commits
6. **Force-with-lease** - Safer than --force
7. **Reflog expires** - Recover within 90 days
8. **Communicate** - Tell team about major undos

## Related Sub-Skills

- Made changes after undo? → `/git/basics`
- Need to redo after reset? → `/git/history`
- Pushed after undo? → `/git/remote`
- Conflicts after revert? → `/git/conflicts`

## Quick Command Reference

```bash
# Unstage
git restore --staged file.js         # Unstage file
git restore --staged .                # Unstage all

# Discard changes
git restore file.js                   # Discard file changes
git restore .                         # Discard all changes

# Amend
git commit --amend                    # Change last commit
git commit --amend --no-edit          # Add to last commit

# Reset
git reset --soft HEAD~1               # Undo commit, keep staged
git reset HEAD~1                      # Undo commit, unstage
git reset --hard HEAD~1               # Undo commit, discard

# Revert
git revert HEAD                       # Revert last commit
git revert abc1234                    # Revert specific commit
git revert -m 1 merge-hash            # Revert merge

# Recover
git reflog                            # View reflog
git reset --hard HEAD@{1}             # Recover from reflog
git branch recovered abc1234          # Recover deleted branch
```

---

**Last Updated:** 2025-02-11
**Version:** 1.0.0
