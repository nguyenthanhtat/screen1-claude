# Git Skill Suite

## Purpose
Comprehensive Git expertise covering all workflows, from basic commits to advanced operations, conflict resolution, and team collaboration patterns.

## Version
- **Version:** 1.0.0
- **Last Updated:** 2025-02-11
- **Git Version:** 2.30+
- **Compatibility:** All major Git hosting platforms (GitHub, GitLab, Bitbucket)

## How to Use This Skill

### Direct Sub-Skill Access
Use skill paths to access specific functionality:
- `/git/basics` - Repository setup, commits, and fundamental workflows
- `/git/branching` - Branch management, merging, and rebasing
- `/git/history` - Commit history, diffs, and code archaeology
- `/git/remote` - Remote repository operations and syncing
- `/git/conflicts` - Merge and rebase conflict resolution
- `/git/undo` - Undo changes and recover lost work
- `/git/workflows` - Team workflows (GitHub Flow, Git Flow, etc.)
- `/git/advanced` - Stash, cherry-pick, hooks, and power features

### Chat Command Examples
```bash
# Basic operations
/git/basics help me commit my changes with a good message

# Branching
/git/branching create feature branch and merge to main

# Conflict resolution
/git/conflicts resolve merge conflict in src/app.js

# History inspection
/git/history find when this bug was introduced

# Undo mistakes
/git/undo I accidentally committed to main, help me undo

# Remote operations
/git/remote sync my fork with upstream

# Team workflows
/git/workflows setup GitHub Flow for our team

# Advanced features
/git/advanced use stash to switch contexts quickly
```

## Auto-Routing (Claude Decides)

If you just use `/git`, Claude will analyze your request and automatically route to the appropriate sub-skill.

**Examples:**
- "How do I commit my changes?" → routes to `/basics`
- "Create a new branch" → routes to `/branching`
- "I have a merge conflict" → routes to `/conflicts`
- "View commit history" → routes to `/history`
- "Undo last commit" → routes to `/undo`
- "Push to GitHub" → routes to `/remote`
- "What's GitHub Flow?" → routes to `/workflows`
- "Save work without committing" → routes to `/advanced`

## Decision Tree

```
User Request Analysis:
│
├─ Keywords: init, clone, commit, add, status, push, pull, .gitignore
│  → /basics
│
├─ Keywords: branch, checkout, merge, rebase, delete branch, switch
│  → /branching
│
├─ Keywords: log, diff, show, blame, bisect, history, who changed
│  → /history
│
├─ Keywords: remote, fetch, upstream, origin, fork, sync
│  → /remote
│
├─ Keywords: conflict, merge conflict, rebase conflict, <<<<<<, resolve
│  → /conflicts
│
├─ Keywords: undo, reset, revert, restore, reflog, recover, amend
│  → /undo
│
├─ Keywords: workflow, github flow, git flow, trunk-based, PR, pull request
│  → /workflows
│
└─ Keywords: stash, cherry-pick, hook, submodule, worktree, filter-branch
   → /advanced
```

## Requirements (Global)

<critical>
All sub-skills require:
- Git 2.30+ installed (`git --version`)
- Git configured with user.name and user.email
- Repository access (local or remote)
- For remote operations: SSH keys or HTTPS credentials configured
</critical>

### Quick Setup Verification
```bash
# Check Git version
git --version

# Check configuration
git config --list

# Verify you can authenticate
git ls-remote https://github.com/user/repo
```

## Sub-Skills Overview

### 1. Basics
**Focus:** Repository fundamentals and daily workflows
**Common tasks:**
- Initialize new repository
- Clone existing repository
- Stage and commit changes
- Push and pull from remote
- Create .gitignore files
- Configure Git settings

**Key commands:** init, clone, add, commit, push, pull, status

---

### 2. Branching
**Focus:** Branch management and integration
**Common tasks:**
- Create and switch branches
- Merge branches (fast-forward and three-way)
- Rebase for linear history
- Delete local and remote branches
- Track remote branches
- Interactive rebase for cleanup

**Key commands:** branch, checkout, switch, merge, rebase

---

### 3. History
**Focus:** Commit history and code archaeology
**Common tasks:**
- View commit history with filters
- Compare changes between commits
- Find who changed a line (blame)
- Binary search for bug introduction (bisect)
- Search commit messages
- Visualize branch history

**Key commands:** log, diff, show, blame, bisect

---

### 4. Remote
**Focus:** Remote repository operations
**Common tasks:**
- Add and remove remotes
- Fetch vs pull (when to use each)
- Push with upstream tracking
- Manage multiple remotes (origin, upstream)
- Force push safely
- Sync fork with upstream

**Key commands:** remote, fetch, pull, push

---

### 5. Conflicts
**Focus:** Conflict resolution strategies
**Common tasks:**
- Understand conflict markers
- Resolve merge conflicts
- Resolve rebase conflicts
- Use merge tools
- Accept theirs/ours strategy
- Prevent conflicts (pull before push)

**Key commands:** merge, rebase, mergetool, checkout --ours/--theirs

---

### 6. Undo
**Focus:** Reversing changes and recovery
**Common tasks:**
- Undo staged changes
- Undo working directory changes
- Amend last commit
- Reset commits (soft, mixed, hard)
- Revert commits (safe for public history)
- Recover deleted commits with reflog

**Key commands:** restore, reset, revert, reflog, amend

---

### 7. Workflows
**Focus:** Team collaboration patterns
**Common tasks:**
- GitHub Flow (feature branches + PRs)
- Git Flow (release branches)
- Trunk-Based Development
- Forking workflow (open source)
- Pull request best practices
- Code review workflows

**Patterns:** Feature branches, release management, hotfixes

---

### 8. Advanced
**Focus:** Power user features
**Common tasks:**
- Stash uncommitted changes
- Cherry-pick specific commits
- Manage submodules
- Create and use Git hooks
- Use worktrees for parallel work
- Sparse checkout for large repos

**Key commands:** stash, cherry-pick, submodule, worktree, hook

---

## Workflow Integration

### For Team Development

```bash
# Step 1: Clone repository and setup
/git/basics clone team repository and configure settings

# Step 2: Create feature branch
/git/branching create feature branch from main

# Step 3: Make changes and commit
/git/basics commit changes with conventional commit message

# Step 4: Sync with remote
/git/remote pull latest changes from main

# Step 5: Resolve any conflicts
/git/conflicts resolve merge conflicts if any

# Step 6: Push feature branch
/git/remote push feature branch to origin

# Step 7: Review history before PR
/git/history review my commits before creating pull request

# Step 8: Follow team workflow
/git/workflows create pull request following GitHub Flow
```

### For Solo Projects

```bash
# Initialize project
/git/basics setup new repository with .gitignore

# Regular workflow
/git/basics commit and push changes

# Undo mistakes
/git/undo fix commit message or undo changes

# Experiment safely
/git/branching create experimental branch

# Save work in progress
/git/advanced stash changes to switch context
```

### For Open Source Contribution

```bash
# Step 1: Fork and clone
/git/remote setup fork with upstream remote

# Step 2: Create feature branch
/git/branching create feature branch from upstream/main

# Step 3: Make changes
/git/basics commit changes following project guidelines

# Step 4: Sync with upstream
/git/remote sync fork with upstream

# Step 5: Clean up commits
/git/branching interactive rebase to squash commits

# Step 6: Submit PR
/git/workflows follow project contribution workflow
```

## Quick Reference

| Task | Sub-Skill | Command Example |
|------|-----------|-----------------|
| First commit | basics | `/git/basics initialize repository and make first commit` |
| Create branch | branching | `/git/branching create feature branch for login page` |
| Merge conflict | conflicts | `/git/conflicts resolve conflict in package.json` |
| View history | history | `/git/history show commits from last week` |
| Undo commit | undo | `/git/undo undo last commit but keep changes` |
| Push to GitHub | remote | `/git/remote push branch to GitHub` |
| GitHub Flow | workflows | `/git/workflows explain GitHub Flow process` |
| Save WIP | advanced | `/git/advanced stash changes and switch branch` |

## Common Scenarios

### "I'm new to Git"
Start with `/git/basics` to learn fundamental concepts:
- What is a repository?
- How to make commits
- Basic workflow (add → commit → push)
- Setting up .gitignore

### "I need to work on a feature"
Use `/git/branching` for branch workflows:
- Create feature branch
- Make commits on branch
- Merge back to main
- Delete feature branch

### "I made a mistake"
Use `/git/undo` to fix problems:
- Uncommit changes
- Unstage files
- Discard local changes
- Recover deleted commits

### "I have conflicts"
Use `/git/conflicts` to resolve:
- Understand conflict markers
- Choose correct version
- Test after resolution
- Complete merge/rebase

### "We need a team workflow"
Use `/git/workflows` for patterns:
- Choose workflow (GitHub Flow, Git Flow, etc.)
- Set up branch protection
- Define PR process
- Establish code review standards

## Installation

Copy this entire folder to your Claude skills directory:

```bash
# Option 1: User skills (recommended)
cp -r skills/git ~/.claude/skills/git

# Option 2: Windows PowerShell
Copy-Item -Recurse skills/git $env:USERPROFILE\.claude\skills\git
```

Then configure in your `.claude` file:
```yaml
skills:
  - ~/.claude/skills/git
```

## Best Practices

### Commit Messages
- Use conventional commits: `feat:`, `fix:`, `docs:`, etc.
- First line: brief summary (50 chars or less)
- Blank line, then detailed explanation if needed
- Reference issue numbers: `Fixes #123`

### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `hotfix/description` - Urgent production fixes
- `docs/description` - Documentation changes

### Git Hygiene
- Pull before push to avoid conflicts
- Commit frequently with meaningful messages
- Use .gitignore to exclude generated files
- Never commit secrets or credentials
- Keep commits focused (one logical change per commit)

### Remote Operations
- Always review changes before pushing
- Use `git fetch` first to see what's new
- Avoid force push to shared branches
- Use `--force-with-lease` if force push is necessary

## Related Documentation

- Official Git: https://git-scm.com/doc
- Pro Git Book: https://git-scm.com/book/en/v2
- GitHub Docs: https://docs.github.com
- GitLab Docs: https://docs.gitlab.com
- Atlassian Git Tutorials: https://www.atlassian.com/git/tutorials

## Changelog

### 1.0.0 (2025-02-11)
- Initial Git skill suite release
- 8 sub-skills covering all major Git operations
- Support for GitHub Flow, Git Flow, and trunk-based development
- Comprehensive conflict resolution patterns
- Advanced features (stash, cherry-pick, hooks, worktrees)

## Support

For Git issues or questions:
1. Use the appropriate sub-skill for your specific need
2. Check Git documentation with `git help <command>`
3. Review error messages carefully - Git provides helpful hints
4. Use `/git/troubleshooting` patterns in relevant sub-skills

## License

Free to use and modify for personal/commercial projects.
