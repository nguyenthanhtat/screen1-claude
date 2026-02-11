# Git Conflicts

**Parent Skill:** `/git`
**Path:** `/git/conflicts`

## Purpose
Master conflict resolution for merge and rebase operations, understand conflict markers, use resolution strategies, and prevent conflicts through best practices.

## When to Use

**Trigger automatically when:**
- User mentions: conflict, merge conflict, rebase conflict, <<<<<<, resolve, merge failed
- After merge/rebase shows conflicts
- CONFLICT message appears
- Files show conflict markers
- Stuck in merge/rebase state

**Chat commands:**
```bash
/git/conflicts help me resolve this merge conflict
/git/conflicts what do the conflict markers mean
/git/conflicts use theirs for all conflicts
/git/conflicts abort this merge
/git/conflicts prevent conflicts in the future
```

## Requirements

<critical>
- Repository in conflicted state OR understanding conflict prevention
- Text editor or merge tool
- Understanding of both conflicting versions
- For complex conflicts: Communication with code author
</critical>

## Verification
```bash
# Check if in conflict state
git status

# See conflicted files
git diff --name-only --diff-filter=U

# See conflict markers
git diff --check
```

---

## Critical Rules

<critical>
1. NEVER commit with unresolved conflict markers (<<<<<<, ======, >>>>>>)
2. ALWAYS test code after resolving conflicts
3. UNDERSTAND both versions before choosing resolution
4. COMMUNICATE with teammate if resolving their changes
5. ABORT merge/rebase if resolution unclear (ask for help)
6. ALWAYS pull before push to minimize conflicts
</critical>

---

## Conflict Workflow

```
Attempt merge/rebase → Conflict! → Resolve → Stage → Complete

States:
1. Normal work
2. Conflict detected
3. Manually resolve (edit files)
4. Stage resolved files (git add)
5. Continue or commit
```

---

## Patterns

### Pattern 1: Understand Conflict Markers

**Problem:** Decipher what conflict markers mean

```bash
# File with conflict looks like:
<<<<<<< HEAD (Current Change)
const API_URL = "https://api.prod.com";
=======
const API_URL = "https://api.staging.com";
>>>>>>> feature-branch (Incoming Change)
```

**Breakdown:**
```
<<<<<<< HEAD
[Your current code]
=======
[Incoming code being merged]
>>>>>>> branch-name
```

**Visual representation:**
```javascript
// ❌ File with conflict (DO NOT COMMIT THIS!)
function greet(name) {
<<<<<<< HEAD
  return `Hello, ${name}!`;
=======
  return `Hi ${name}`;
>>>>>>> feature-greeting
}

// ✅ After resolution (clean, working code)
function greet(name) {
  return `Hello, ${name}!`;  // Chose current change
}

// ✅ Or combined both
function greet(name) {
  return `Hello, ${name}! Welcome!`;  // Merged both ideas
}
```

**Impact:** Understanding is first step to resolution

**When to use:**
- Every conflict resolution
- Teaching teammates
- Understanding merge tools

---

### Pattern 2: Resolve Merge Conflicts

**Problem:** Two branches modified same lines

```bash
# ❌ BAD: Panic and force one version
git checkout --theirs .  # Without understanding!
git add .
git commit

# ✅ GOOD: Understand and resolve carefully
# Step 1: See what conflicts
git status
# both modified: src/app.js
# both modified: README.md

# Step 2: Open conflicted file
code src/app.js

# Step 3: Find conflict markers
# <<<<<<< HEAD
# Current changes
# =======
# Incoming changes
# >>>>>>> feature-branch

# Step 4: Manually edit to keep what's needed
# Remove markers, keep correct code

# Step 5: Save and stage
git add src/app.js

# Step 6: Verify no conflicts remain
git diff --check

# Step 7: Continue merge
git commit  # Or git merge --continue
```

**Real example:**
```javascript
// Original (both branches started here):
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Your change (HEAD):
function calculateTotal(items) {
  // Added tax calculation
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal * 1.10; // 10% tax
}

// Their change (feature-branch):
function calculateTotal(items) {
  // Added discount support
  return items.reduce((sum, item) => sum + item.price - item.discount, 0);
}

// Conflict:
function calculateTotal(items) {
<<<<<<< HEAD
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal * 1.10; // 10% tax
=======
  return items.reduce((sum, item) => sum + item.price - item.discount, 0);
>>>>>>> feature-branch
}

// ✅ GOOD resolution (combine both features):
function calculateTotal(items) {
  const subtotal = items.reduce((sum, item) =>
    sum + item.price - (item.discount || 0), 0
  );
  return subtotal * 1.10; // 10% tax
}
```

**Impact:** Correct code that combines both changes

**When to use:**
- Every merge conflict
- After pull with conflicts
- Merging feature branches

---

### Pattern 3: Resolve Rebase Conflicts

**Problem:** Conflicts during rebase

```bash
# ❌ BAD: Abort at first sign of conflict
git rebase main
# CONFLICT!
git rebase --abort  # Gives up immediately

# ✅ GOOD: Resolve conflicts commit by commit
git rebase main
# CONFLICT in src/app.js

# Step 1: See which commit is being applied
git status
# rebase in progress; onto abc1234
# You are currently rebasing branch 'feature' on 'abc1234'
# (fix conflicts and run "git rebase --continue")

# Step 2: See what commit caused conflict
git log --oneline HEAD..main

# Step 3: Resolve conflict (same as merge)
code src/app.js
# ... edit file, remove markers ...

# Step 4: Stage resolved file
git add src/app.js

# Step 5: Continue rebase
git rebase --continue

# May have more conflicts for next commits
# Repeat until done
```

**Rebase conflict workflow:**
```bash
git rebase main
# Applying: feat: add feature A
# CONFLICT!

# Resolve conflict
git add file.js
git rebase --continue

# Applying: feat: add feature B
# CONFLICT!

# Resolve conflict
git add file.js
git rebase --continue

# Success!
```

**Skip or abort:**
```bash
# Skip this commit (if no longer needed)
git rebase --skip

# Abort entire rebase
git rebase --abort

# Edit commit during rebase
git rebase --edit-todo
```

**Impact:** Clean rebase with resolved conflicts

**When to use:**
- Rebasing feature on main
- Interactive rebase conflicts
- Updating old branches

---

### Pattern 4: Use Merge Tool

**Problem:** Manual editing is tedious for complex conflicts

```bash
# ❌ BAD: Try to resolve complex conflicts manually
# 50 conflicts across 20 files!

# ✅ GOOD: Use merge tool
git mergetool

# Launches configured tool (e.g., VS Code, meld, kdiff3)
# Shows 3-way merge:
# - Left: Your version
# - Middle: Base (common ancestor)
# - Right: Their version
# - Bottom: Result

# Or specify tool:
git mergetool --tool=vimdiff
git mergetool --tool=code
```

**Configure merge tool:**
```bash
# VS Code
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait --merge $REMOTE $LOCAL $BASE $MERGED'

# Meld (Linux)
git config --global merge.tool meld

# Kdiff3
git config --global merge.tool kdiff3

# Disable backup files (.orig)
git config --global mergetool.keepBackup false
```

**Using merge tool:**
```bash
# Start merge that has conflicts
git merge feature-branch
# CONFLICT!

# Launch merge tool for all conflicts
git mergetool

# Tool opens each conflicted file
# Resolve in tool, save, close
# Tool automatically stages resolved files

# Verify resolution
git diff --staged

# Complete merge
git commit
```

**Impact:** Faster, visual conflict resolution

**When to use:**
- Multiple conflicts
- Complex 3-way merges
- Binary file conflicts
- Prefer visual tools

---

### Pattern 5: Accept Theirs/Ours Strategy

**Problem:** Know entire file should use one version

```bash
# ❌ BAD: Manually edit every conflict in file
# File has 20 conflicts, all should use same version

# ✅ GOOD: Accept all from one side
# During merge/rebase conflict:

# Accept all current changes (ours)
git checkout --ours path/to/file.js
git add path/to/file.js

# Accept all incoming changes (theirs)
git checkout --theirs path/to/file.js
git add path/to/file.js

# ✅ BETTER: Use merge strategy upfront
# Merge with strategy (prefer ours for conflicts)
git merge -X ours feature-branch

# Merge with strategy (prefer theirs for conflicts)
git merge -X theirs feature-branch
```

**For specific files:**
```bash
# Merge mostly works, but config files use ours
git merge feature-branch
# CONFLICT in config files

# Use ours for config
git checkout --ours config/*.json
git add config/

# Manually resolve code conflicts
# ...

git commit
```

**Rebase with strategy:**
```bash
# Rebase, preferring our version on conflicts
git rebase -X ours main

# Note: In rebase, "ours" and "theirs" are swapped!
# - "ours" = main (being rebased onto)
# - "theirs" = your branch (being replayed)
```

**When to use strategies:**
```
Use --ours when:
- Config files should keep your settings
- Database migrations (yours are newer)
- You're sure your version is correct

Use --theirs when:
- Auto-generated files (package-lock.json)
- Taking upstream's version
- You're sure their version is correct

Use with CAUTION:
- Never blindly apply without understanding
- Communicate with code author
- Test thoroughly after
```

**Impact:** Quick resolution for clear-cut conflicts

**When to use:**
- Config files
- Generated files
- Database migrations
- Clear ownership of changes

---

### Pattern 6: Prevent Conflicts

**Problem:** Conflicts are disruptive, prevent when possible

```bash
# ❌ BAD: Rarely sync with main
git checkout -b feature
# ... 2 weeks of work ...
git merge main
# 50 conflicts!

# ✅ GOOD: Sync regularly
git checkout -b feature
# ... daily work ...
git fetch origin
git rebase origin/main
# Small conflicts, easy to resolve

# Repeat daily or after significant main changes
```

**Best practices to prevent conflicts:**
```bash
# 1. Pull before starting work
git checkout main
git pull origin main
git checkout -b feature

# 2. Pull/rebase frequently
git fetch origin
git rebase origin/main  # Daily

# 3. Keep branches short-lived
git checkout -b feature
# ... 1-3 days of work ...
git push # Create PR
# Merge quickly

# 4. Communicate with team
# "I'm working on auth.js this week"
# Others avoid editing same file

# 5. Use .gitattributes for files that conflict
# package-lock.json merge=ours
echo "package-lock.json merge=ours" >> .gitattributes
```

**Automatic conflict markers:**
```bash
# For files that always conflict (like CHANGELOG)
# Tell Git to use union merge (keep both versions)
echo "CHANGELOG.md merge=union" >> .gitattributes

# For binary files
echo "*.png binary" >> .gitattributes
echo "*.jpg binary" >> .gitattributes
```

**Impact:** Fewer, smaller conflicts

**When to use:**
- Always! Prevention is best
- Team collaboration
- Long-running branches

---

### Pattern 7: Abort Merge/Rebase

**Problem:** Resolution too complex, need to reconsider

```bash
# ❌ BAD: Try to force resolution without understanding
# Make guesses, commit broken code

# ✅ GOOD: Abort and reconsider
# During merge
git merge feature-branch
# CONFLICT! Too complex!

git merge --abort  # Returns to pre-merge state

# During rebase
git rebase main
# CONFLICT! Too complex!

git rebase --abort  # Returns to pre-rebase state

# ✅ BETTER: Abort, communicate, then retry
git merge --abort

# Talk to teammate who made conflicting changes
# Understand their approach
# Agree on resolution strategy

# Retry with knowledge
git merge feature-branch
# Resolve with understanding
```

**When to abort:**
```
Abort when:
- Unsure which version is correct
- Need to communicate with code author
- Too many conflicts (>20 files)
- Conflict involves critical security code
- Time-sensitive: will return to it later
- Tests would definitely fail

Don't abort when:
- Just a few simple conflicts
- You understand both versions
- Clear which version is correct
- In the middle of good progress
```

**After abort:**
```bash
# Aborted merge, what now?

# Option 1: Use different merge strategy
git merge -X ours feature-branch

# Option 2: Rebase instead of merge
git checkout feature-branch
git rebase main
git checkout main
git merge feature-branch

# Option 3: Squash merge
git merge --squash feature-branch
git commit

# Option 4: Ask author to rebase their branch first
# (They resolve conflicts on their branch)
```

**Impact:** Avoid broken commits from rushed resolution

**When to use:**
- Uncertainty about resolution
- Too complex to resolve now
- Need to consult with team

---

### Pattern 8: Complex Conflict Resolution

**Problem:** Conflicts involve multiple people's work

```bash
# ❌ BAD: Resolve alone without consultation
git merge team-branch
# 30 files conflict
# Guess at resolutions
git commit

# ✅ GOOD: Systematic approach
# Step 1: Assess scope
git merge team-branch
git status | grep "both modified" | wc -l
# 30 conflicts!

# Step 2: Abort and plan
git merge --abort

# Step 3: Communicate
# Team meeting or Slack:
# "I'm merging team-branch to main"
# "30 conflicts in auth.js, database.js, api.js"
# "Who can help resolve?"

# Step 4: Pair programming for resolution
# Screen share or pair station

# Step 5: Merge with team present
git merge team-branch

# Step 6: Resolve each file with author input
# auth.js conflicts → auth expert helps
# database.js conflicts → database expert helps

# Step 7: Test thoroughly
npm test
npm run integration-tests

# Step 8: Commit with documentation
git commit -m "Merge team-branch into main

Resolved conflicts in:
- auth.js: Combined OAuth and JWT approaches (with @alice)
- database.js: Merged schema changes (with @bob)
- api.js: Kept REST, removed GraphQL experiment

Tested:
- All unit tests pass
- Integration tests pass
- Manual testing completed"
```

**Conflict resolution checklist:**
```
Before resolving:
☐ Understand both versions
☐ Know why each change was made
☐ Consult with code authors if possible
☐ Have test cases ready

During resolution:
☐ Resolve conflicts systematically
☐ Test after each file
☐ Keep conflict markers removed
☐ Verify no unintended deletions

After resolution:
☐ All tests pass
☐ Code review (if major conflicts)
☐ Document resolution in commit message
☐ Deploy to staging first (for production merges)
```

**Impact:** Correct, well-tested conflict resolution

**When to use:**
- Large merges
- Critical code conflicts
- Team integration
- Release merges

---

## Common Workflows

### Daily Conflict Prevention
```bash
# Morning routine
git checkout main
git pull origin main

# Before starting feature
git checkout -b feature-new

# End of day (if branch not done)
git fetch origin
git rebase origin/main  # Keep up to date
git push --force-with-lease origin feature-new
```

### Resolving Merge Conflict
```bash
# Merge causes conflict
git merge feature-branch
# CONFLICT in src/app.js

# 1. Check what's conflicted
git status

# 2. Open file
code src/app.js

# 3. Find and resolve markers
# Remove <<<<<<, ======, >>>>>>
# Keep correct code

# 4. Test changes
npm test

# 5. Stage
git add src/app.js

# 6. Verify
git diff --check

# 7. Complete merge
git commit
```

### Resolving Rebase Conflict
```bash
# Rebase causes conflict
git rebase main
# CONFLICT in src/app.js

# 1. Resolve conflict
code src/app.js
# Edit file

# 2. Stage
git add src/app.js

# 3. Continue
git rebase --continue

# 4. May have more conflicts, repeat

# 5. When done, force push
git push --force-with-lease origin feature-branch
```

---

## Troubleshooting

### "Both modified" won't go away
```bash
# Resolved conflict but git status still shows conflict

# Make sure conflict markers are removed
grep -r "<<<<<<" src/
grep -r ">>>>>>" src/

# Check for whitespace issues
git diff --check

# Stage explicitly
git add -A
```

### Lost track of what to keep
```bash
# See original version
git show :1:file.js > file-base.js

# See your version
git show :2:file.js > file-ours.js

# See their version
git show :3:file.js > file-theirs.js

# Compare and decide
diff file-ours.js file-theirs.js
```

### Merge tool created .orig files
```bash
# Disable for future
git config --global mergetool.keepBackup false

# Delete existing
find . -name "*.orig" -delete
```

### Accidentally committed with markers
```bash
# If not pushed yet
git reset HEAD^
# Resolve properly
git add .
git commit

# If already pushed
git revert HEAD
# Create new commit with fix
```

---

## Best Practices

1. **Pull before push** - Prevent conflicts at source
2. **Sync frequently** - Small conflicts easier than large
3. **Keep branches short** - Less time to diverge
4. **Communicate** - Coordinate on shared files
5. **Test after resolution** - Ensure code works
6. **Document complex resolutions** - In commit message
7. **Use merge tools** - For complex conflicts
8. **Don't guess** - Ask if unsure

## Related Sub-Skills

- Need to undo conflict resolution? → `/git/undo`
- Need to push after rebase? → `/git/remote`
- Setting up merge strategies? → `/git/workflows`
- Understanding branch structure? → `/git/branching`

## Quick Command Reference

```bash
# During conflict
git status                               # See conflicted files
git diff                                 # See conflict markers

# Resolution
git add file.js                          # Mark resolved
git diff --check                         # Check no markers remain

# Strategies
git checkout --ours file.js              # Use our version
git checkout --theirs file.js            # Use their version
git mergetool                            # Launch merge tool

# Merge conflict
git merge --abort                        # Abort merge
git commit                               # Complete merge

# Rebase conflict
git rebase --abort                       # Abort rebase
git rebase --skip                        # Skip commit
git rebase --continue                    # Continue rebase

# Prevention
git pull --rebase                        # Rebase instead of merge
git fetch && git rebase origin/main      # Update branch
```

---

**Last Updated:** 2025-02-11
**Version:** 1.0.0
