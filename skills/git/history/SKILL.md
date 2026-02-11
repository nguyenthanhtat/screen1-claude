# Git History

**Parent Skill:** `/git`
**Path:** `/git/history`

## Purpose
Explore commit history, compare changes, perform code archaeology, and find when bugs were introduced. Master log viewing, diffs, blame, bisect, and history filtering.

## When to Use

**Trigger automatically when:**
- User mentions: log, diff, show, blame, bisect, history, who changed, when was
- Investigating bugs
- Code review preparation
- Finding when changes were made
- Understanding code evolution

**Chat commands:**
```bash
/git/history show me recent commits
/git/history find when this bug was introduced
/git/history who changed this line
/git/history compare branches
/git/history search commit messages for "auth"
```

## Requirements

<critical>
- Git repository with commit history
- Read access to repository
- For bisect: Working test case
- For blame: File must exist in history
</critical>

## Verification
```bash
# Check repository has commits
git log --oneline -5

# Check file history exists
git log -- path/to/file.js
```

---

## Critical Rules

<critical>
1. ALWAYS use relative time or commit ranges for large repositories
2. NEVER run `git log` without limits on huge repositories
3. ALWAYS save bisect session progress (can resume later)
4. Use `git log --follow` to track file renames
5. For diffs, specify what you're comparing explicitly
</critical>

---

## Patterns

### Pattern 1: View Commit History

**Problem:** Understand what changes were made and when

```bash
# ❌ BAD: Default log is overwhelming
git log  # Shows full commit messages, can be thousands of lines

# ✅ GOOD: Concise, readable format
git log --oneline -10

# ✅ BETTER: Custom format with author and date
git log --oneline --graph --decorate --all -20

# ✅ BEST: Alias for common format
git config --global alias.lg "log --oneline --graph --decorate --all"
git lg -20
```

**Pretty formatting:**
```bash
# One line per commit
git log --oneline
# abc1234 feat: add user authentication
# def5678 fix: resolve login bug

# With graph (show branches)
git log --oneline --graph
# * abc1234 feat: add user auth
# * def5678 fix: resolve login bug
# |\
# | * ghi9012 feat: add dashboard
# |/
# * jkl3456 Initial commit

# Custom format
git log --pretty=format:"%h - %an, %ar : %s"
# abc1234 - John Doe, 2 hours ago : feat: add user auth

# With stats
git log --stat -3
# Shows files changed and line counts
```

**Time-based filtering:**
```bash
# Commits from last week
git log --since="1 week ago"

# Commits from specific date range
git log --since="2024-01-01" --until="2024-02-01"

# Commits from last 3 days
git log --since="3 days ago"

# Commits from specific time
git log --since="2024-02-01 10:00" --until="2024-02-01 18:00"
```

**Impact:** Quickly understand project evolution

**When to use:**
- Code review preparation
- Understanding recent changes
- Writing changelogs
- Investigating project timeline

---

### Pattern 2: Compare Changes (Diff)

**Problem:** See what changed between commits, branches, or states

```bash
# ❌ BAD: Unclear what's being compared
git diff  # Compares working directory to staging?

# ✅ GOOD: Explicit comparisons
# Unstaged changes (working directory vs staging)
git diff

# Staged changes (staging vs last commit)
git diff --staged
# or
git diff --cached

# All changes (working directory vs last commit)
git diff HEAD

# Specific file
git diff HEAD -- src/app.js
```

**Compare commits:**
```bash
# Compare two commits
git diff abc1234 def5678

# Compare commit to HEAD
git diff abc1234 HEAD

# Compare with parent
git diff HEAD^ HEAD
git diff HEAD~1 HEAD

# Show what commit changed
git show abc1234
```

**Compare branches:**
```bash
# Changes from main to feature branch
git diff main..feature-branch

# Changes that will be merged
git diff main...feature-branch  # Three dots!

# Files changed between branches
git diff --name-only main..feature-branch

# Stat summary
git diff --stat main..feature-branch
```

**Diff output options:**
```bash
# Side-by-side diff (if terminal supports)
git diff --color-words

# Show only file names
git diff --name-only

# Show with stats
git diff --stat

# Ignore whitespace
git diff -w

# Specific function/class (Git is smart!)
git diff -L :functionName:file.js
```

**Impact:** Understand exactly what changed

**When to use:**
- Before committing (review changes)
- Code review
- Comparing branches before merge
- Understanding specific changes

---

### Pattern 3: Show Commit Details

**Problem:** See complete details of specific commit

```bash
# ❌ BAD: Just hash or log
git log abc1234
# Too much output

# ✅ GOOD: Show specific commit
git show abc1234

# ✅ BETTER: Show with stat summary
git show --stat abc1234

# Show only changed files
git show --name-only abc1234

# Show specific file from commit
git show abc1234:src/app.js
```

**View file at specific commit:**
```bash
# See file content from commit
git show abc1234:path/to/file.js

# Save file version to disk
git show abc1234:src/app.js > app-old.js

# Compare file between commits
git diff abc1234:src/app.js def5678:src/app.js
```

**Show multiple commits:**
```bash
# Show last 3 commits with details
git show HEAD~3 HEAD~2 HEAD~1

# Show range
git log -p abc1234..def5678  # -p shows patches (diffs)
```

**Impact:** Deep dive into specific changes

**When to use:**
- Investigating bug fix
- Understanding old code
- Code archaeology
- Reverting specific changes

---

### Pattern 4: Find Who Changed Line (Blame)

**Problem:** Find who last modified each line of file

```bash
# ❌ BAD: Blame without context
git blame file.js
# Overwhelming output

# ✅ GOOD: Blame with line numbers and author
git blame -L 10,20 src/app.js
# Shows lines 10-20 only

# ✅ BETTER: Ignore whitespace changes
git blame -w src/app.js

# Show email and date
git blame -e --date=short src/app.js
```

**Advanced blame:**
```bash
# Ignore specific commit (like reformatting)
git blame --ignore-rev abc1234 src/app.js

# Ignore all commits in file
git blame --ignore-revs-file .git-blame-ignore-revs src/app.js

# Show original line numbers (track through renames)
git blame -C -C src/app.js

# Interactive blame (show commit details)
git blame -L 50,60 src/app.js
# Copy commit hash
git show abc1234
```

**Find deleted code:**
```bash
# Find when line was deleted
git log -S "function oldFunction" -- src/app.js

# Show commits that added or removed string
git log -G "regex pattern" -- src/app.js
```

**Impact:** Understand code history and authorship

**When to use:**
- Bug investigation
- Understanding design decisions
- Code review context
- Finding subject matter expert

---

### Pattern 5: Binary Search for Bugs (Bisect)

**Problem:** Find commit that introduced a bug

```bash
# ❌ BAD: Manually check each commit
git log --oneline
git checkout abc1234
# Test...
git checkout def5678
# Test...
# This takes forever!

# ✅ GOOD: Binary search with bisect
git bisect start
git bisect bad                 # Current commit is bad
git bisect good abc1234        # This old commit was good

# Git checks out middle commit
# Test it
npm test

# If test passes:
git bisect good

# If test fails:
git bisect bad

# Repeat until Git finds the culprit commit
# Git will tell you: "abc1234 is the first bad commit"

# End bisect
git bisect reset
```

**Automated bisect:**
```bash
# Let Git automatically test
git bisect start HEAD abc1234
git bisect run npm test

# Git will automatically:
# 1. Check out commit
# 2. Run npm test
# 3. Mark good (exit 0) or bad (exit 1)
# 4. Continue until found

# Works with any command that returns exit code
git bisect run ./test.sh
git bisect run python -m pytest
```

**Bisect with build script:**
```bash
# Create test script
cat > test.sh << 'EOF'
#!/bin/bash
npm install
npm run build
npm test
exit $?
EOF

chmod +x test.sh

git bisect start HEAD v1.0.0
git bisect run ./test.sh
```

**Skip commits (if build broken):**
```bash
git bisect start
git bisect bad
git bisect good abc1234

# Current commit can't be tested
git bisect skip

# Skip range
git bisect skip abc1234..def5678
```

**Impact:** Find bug introduction 10x faster than manual search

**When to use:**
- Regression testing
- Bug appeared between releases
- Code worked before, broken now
- Large commit history to search

---

### Pattern 6: Search Commit Messages

**Problem:** Find commits related to specific feature or bug

```bash
# ❌ BAD: Search all commits with grep
git log | grep "auth"
# Misses context

# ✅ GOOD: Search commit messages
git log --grep="auth"

# Case insensitive
git log --grep="auth" -i

# Multiple patterns (OR)
git log --grep="auth" --grep="login"

# Multiple patterns (AND)
git log --grep="auth" --grep="login" --all-match

# Regular expressions
git log --grep="fix.*auth" -E
```

**Search commit content:**
```bash
# Find commits that added/removed string
git log -S "functionName"

# With patches showing context
git log -S "functionName" -p

# Regular expression in content
git log -G "function.*Auth"

# Find commits affecting specific file
git log -- src/auth.js

# Combination: message and file
git log --grep="fix" -- src/auth.js
```

**Impact:** Quickly find relevant commits

**When to use:**
- Finding when feature was added
- Locating bug fix
- Code review
- Understanding feature history

---

### Pattern 7: Filter History by File/Author/Date

**Problem:** View commits for specific context

**Filter by file:**
```bash
# ❌ BAD: All commits, then search
git log > all.txt
# Search in editor

# ✅ GOOD: Filter by file path
git log -- src/auth.js

# Follow file through renames
git log --follow -- src/auth.js

# Multiple files
git log -- src/auth.js src/user.js

# Directory
git log -- src/components/
```

**Filter by author:**
```bash
# Specific author
git log --author="John Doe"

# Partial match
git log --author="John"

# Multiple authors
git log --author="John\|Jane"

# Exclude author
git log --author="^(?!John).*$"

# With stats
git log --author="John" --stat
```

**Filter by date:**
```bash
# Since date
git log --since="2024-01-01"

# Until date
git log --until="2024-02-01"

# Date range
git log --since="2024-01-01" --until="2024-02-01"

# Relative dates
git log --since="2 weeks ago"
git log --since="yesterday"
git log --since="1 month ago"
```

**Combine filters:**
```bash
# Author + date + file
git log --author="John" --since="1 week ago" -- src/auth.js

# Author + message
git log --author="John" --grep="fix"

# Multiple filters
git log --author="John" --since="2024-01-01" --grep="auth" -- src/
```

**Impact:** Narrow down to exact commits needed

**When to use:**
- Reviewing teammate's work
- File history investigation
- Preparing changelog
- Audit and compliance

---

### Pattern 8: Visualize Branch History

**Problem:** Understand complex branch structure

```bash
# ❌ BAD: Linear log
git log --oneline
# Can't see branches

# ✅ GOOD: Graph view
git log --graph --oneline --all

# ✅ BETTER: With decorations and colors
git log --graph --oneline --decorate --all --color

# ✅ BEST: Custom format with details
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --all
```

**Create alias:**
```bash
git config --global alias.tree "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --all"

# Now use:
git tree
git tree -20  # Last 20 commits
```

**Branch-specific views:**
```bash
# Show only current branch
git log --graph --oneline

# Show all branches
git log --graph --oneline --all

# Show specific branches
git log --graph --oneline main develop feature-branch

# Show branch divergence
git log --graph --oneline main..feature-branch
```

**Visual tools:**
```bash
# Use gitk (GUI tool)
gitk --all

# Or tig (terminal tool)
tig

# Or GitHub/GitLab web interface
```

**Impact:** Understand branch relationships visually

**When to use:**
- Complex branch structures
- Before merging
- Understanding team workflow
- Debugging merge issues

---

## Common Workflows

### Bug Investigation Workflow
```bash
# 1. Find when bug appeared
git bisect start HEAD v1.0.0
git bisect run npm test

# 2. Found commit abc1234
git show abc1234

# 3. Who wrote it?
git blame src/buggy-file.js

# 4. What was the context?
git log --oneline abc1234~5..abc1234

# 5. Related changes?
git log --grep="feature-name" --since="1 month ago"
```

### Code Review Preparation
```bash
# 1. See all commits in PR
git log --oneline main..feature-branch

# 2. See detailed changes
git diff main...feature-branch

# 3. Review each commit
git log -p main..feature-branch

# 4. Check specific file changes
git log --follow -- src/important-file.js
```

### Changelog Generation
```bash
# Get commits since last release
git log --oneline v1.0.0..HEAD

# Group by type
git log --oneline --grep="feat:" v1.0.0..HEAD
git log --oneline --grep="fix:" v1.0.0..HEAD

# With authors
git log --pretty=format:"- %s (%an)" v1.0.0..HEAD

# Export to file
git log --pretty=format:"- %s" v1.0.0..HEAD > CHANGELOG.md
```

---

## Troubleshooting

### Log is too long
```bash
# Limit number of commits
git log -10

# Use pager
git log | less

# Export to file
git log > log.txt
```

### Can't find commit
```bash
# Search all branches
git log --all --grep="search term"

# Search reflog (even deleted commits)
git reflog | grep "search term"

# Search by date
git log --all --since="when I remember working on it"
```

### Blame shows wrong author
```bash
# Blame shows reformatting commit
# Create .git-blame-ignore-revs
echo "abc1234" >> .git-blame-ignore-revs
git blame --ignore-revs-file .git-blame-ignore-revs file.js

# Or configure globally
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

### Bisect stuck
```bash
# Skip problematic commits
git bisect skip

# Abort and start over
git bisect reset
git bisect start

# Resume from saved state
git bisect log > bisect-log.txt
# Git automatically resumes from saved state
```

---

## Best Practices

1. **Use limits** - Always limit git log output (`-10`, `--since`, etc.)
2. **Specific comparisons** - Be explicit with diff comparisons
3. **Follow renames** - Use `--follow` for file history
4. **Automate bisect** - Write test scripts for bisect run
5. **Create aliases** - Save complex log formats as aliases
6. **Use graphical view** - Visual tools for complex branches
7. **Document bisect** - Save bisect results in commit/issue

## Related Sub-Skills

- Need to undo changes? → `/git/undo`
- Need to compare branches? → `/git/branching`
- Investigating merge conflicts? → `/git/conflicts`
- Understanding team workflow? → `/git/workflows`

## Quick Command Reference

```bash
# View history
git log --oneline -10                    # Recent commits
git log --graph --all                    # Branch graph
git log --since="1 week ago"             # Time filter

# Compare
git diff                                 # Unstaged changes
git diff --staged                        # Staged changes
git diff main..feature                   # Branch comparison

# Show commit
git show abc1234                         # Commit details
git show abc1234:file.js                 # File at commit

# Blame
git blame file.js                        # Who changed what
git blame -L 10,20 file.js              # Specific lines

# Bisect
git bisect start HEAD v1.0.0            # Start bisect
git bisect good/bad                      # Mark commits
git bisect reset                         # End bisect

# Search
git log --grep="search"                  # Search messages
git log -S "code"                        # Search content
git log -- file.js                       # File history

# Filter
git log --author="John"                  # By author
git log --since="date"                   # By date
```

---

**Last Updated:** 2025-02-11
**Version:** 1.0.0
