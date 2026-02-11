# Git Workflows

**Parent Skill:** `/git`
**Path:** `/git/workflows`

## Purpose
Master team collaboration patterns including GitHub Flow, Git Flow, Trunk-Based Development, forking workflow, pull request best practices, and code review processes.

## When to Use

**Trigger automatically when:**
- User mentions: workflow, github flow, git flow, trunk-based, PR, pull request, code review, release, branching strategy
- Setting up team process
- Choosing Git strategy
- Creating pull requests
- Release management questions

**Chat commands:**
```bash
/git/workflows what's GitHub Flow
/git/workflows set up Git Flow for our team
/git/workflows create pull request checklist
/git/workflows how to do code reviews
/git/workflows choose workflow for startup
```

## Requirements

<critical>
- Git repository (local or remote)
- Team collaboration setup (GitHub/GitLab/Bitbucket)
- Understanding of branching basics
- For PRs: Remote repository access
- Team agreement on chosen workflow
</critical>

## Verification
```bash
# Check current branches
git branch -a

# Check remote configuration
git remote -v

# Check workflow documentation
ls .github/  # GitHub-specific files
cat .github/pull_request_template.md
```

---

## Critical Rules

<critical>
1. CHOOSE ONE workflow and stick to it (don't mix)
2. DOCUMENT your workflow in README or CONTRIBUTING.md
3. PROTECT main/production branches (require PRs)
4. REQUIRE code review before merge
5. AUTOMATE tests in CI/CD
6. NEVER commit directly to main/production
7. COMMUNICATE workflow to all team members
</critical>

---

## Workflows Comparison

```
GitHub Flow:      Simple, continuous deployment
Git Flow:         Structured, release-based
Trunk-Based:      Extreme simplicity, fast merges
Forking:          Open source contributions
```

---

## Patterns

### Pattern 1: GitHub Flow (Recommended for Most Teams)

**Philosophy:** Simple, branch-based workflow for continuous deployment

**Structure:**
```
main (always deployable)
 ├─ feature/user-login
 ├─ fix/email-validation
 └─ feature/dashboard
```

**Workflow:**
```bash
# 1. Start from main (always up to date)
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-profile

# 3. Make commits
git add src/profile.js
git commit -m "feat: add user profile page"
git add tests/profile.test.js
git commit -m "test: add profile page tests"

# 4. Push branch
git push -u origin feature/user-profile

# 5. Create Pull Request on GitHub
# - Add description
# - Request reviewers
# - Link to issue

# 6. Address review feedback
git add src/profile.js
git commit -m "fix: address review comments"
git push origin feature/user-profile

# 7. Merge PR (on GitHub)
# - Squash and merge (or merge commit)
# - Delete branch automatically

# 8. Update local
git checkout main
git pull origin main
git branch -d feature/user-profile
```

**Branch naming:**
```
feature/user-authentication
feature/payment-integration
fix/login-validation
fix/email-typo
hotfix/security-patch
docs/api-documentation
```

**Protection rules:**
```
main branch:
☐ Require pull request reviews (at least 1)
☐ Require status checks to pass
☐ Require branches to be up to date
☐ Enforce for administrators
☐ Restrict pushes (no direct commits)
```

**When to use:**
- Web applications with continuous deployment
- Small to medium teams (2-20 developers)
- Need simple, easy to understand workflow
- Deploy from main frequently

**Pros:**
✅ Simple to understand
✅ Continuous integration friendly
✅ Fast feedback loops
✅ Always deployable main branch

**Cons:**
❌ No support for multiple versions
❌ Hotfixes require same process as features
❌ Release timing less controlled

---

### Pattern 2: Git Flow (Complex, Release-Based)

**Philosophy:** Structured workflow for scheduled releases

**Structure:**
```
main (production)
 ├─ develop (integration branch)
 │   ├─ feature/user-login
 │   ├─ feature/dashboard
 │   └─ feature/reports
 ├─ release/v1.2.0
 └─ hotfix/critical-bug
```

**Branches:**
- **main**: Production, tagged releases
- **develop**: Integration, next release
- **feature/***: New features (from develop)
- **release/***: Release preparation (from develop)
- **hotfix/***: Production fixes (from main)

**Workflow:**

**Feature development:**
```bash
# 1. Start from develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/user-login

# 3. Develop feature
# ... commits ...

# 4. Finish feature
git checkout develop
git merge --no-ff feature/user-login
git branch -d feature/user-login
git push origin develop
```

**Release process:**
```bash
# 1. Create release branch from develop
git checkout develop
git checkout -b release/v1.2.0

# 2. Bump version, update changelog
echo "1.2.0" > VERSION
git add VERSION CHANGELOG.md
git commit -m "chore: bump version to 1.2.0"

# 3. Bug fixes on release branch
# ... minor fixes ...

# 4. Merge to main
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"

# 5. Merge back to develop
git checkout develop
git merge --no-ff release/v1.2.0

# 6. Delete release branch
git branch -d release/v1.2.0

# 7. Push everything
git push origin main develop --tags
```

**Hotfix process:**
```bash
# 1. Create hotfix from main
git checkout main
git checkout -b hotfix/security-patch

# 2. Fix bug
git commit -m "fix: security vulnerability CVE-2024-001"

# 3. Merge to main
git checkout main
git merge --no-ff hotfix/security-patch
git tag -a v1.2.1 -m "Hotfix security patch"

# 4. Merge to develop
git checkout develop
git merge --no-ff hotfix/security-patch

# 5. Delete hotfix branch
git branch -d hotfix/security-patch
git push origin main develop --tags
```

**When to use:**
- Desktop software with scheduled releases
- Mobile apps (app store releases)
- Products with multiple versions in production
- Large teams with defined release cycles

**Pros:**
✅ Clear separation of concerns
✅ Support multiple versions
✅ Organized release process
✅ Hotfix workflow defined

**Cons:**
❌ Complex to learn and maintain
❌ Overhead for small teams
❌ Slower than GitHub Flow
❌ Merge conflicts more common

---

### Pattern 3: Trunk-Based Development

**Philosophy:** Everyone commits to trunk (main), very short-lived branches

**Structure:**
```
main (trunk)
 ├─ short-lived-branch-1 (< 1 day)
 ├─ short-lived-branch-2 (< 1 day)
 └─ release branches (read-only)
```

**Workflow:**
```bash
# 1. Pull latest main
git checkout main
git pull origin main

# 2. Create tiny branch (optional)
git checkout -b add-login-button

# 3. Make small change (< 1 day of work)
git add src/LoginButton.js
git commit -m "feat: add login button component"

# 4. Immediately push and PR
git push -u origin add-login-button
# Create PR on GitHub

# 5. Quick review and merge (< 2 hours)
# Merge to main

# 6. Delete branch
git checkout main
git pull origin main
git branch -d add-login-button

# Alternative: Commit directly to main (very advanced teams)
git checkout main
git pull origin main
# ... make change ...
git commit -m "feat: add login button"
git push origin main
```

**Feature flags for large features:**
```javascript
// Use feature flags for incomplete features
function renderDashboard() {
  if (featureFlags.newDashboard) {
    return <NewDashboard />;  // Work in progress
  }
  return <OldDashboard />;  // Production stable
}
```

**Release branches:**
```bash
# Create release branch from main
git checkout -b release/v1.0.0 main

# Cherry-pick fixes to release branch
git cherry-pick abc1234

# Deploy from release branch
# Never merge release branch back to main
```

**When to use:**
- Experienced teams
- Strong CI/CD infrastructure
- Feature flags capability
- Fast-moving startups
- Monorepo setup

**Pros:**
✅ Maximum simplicity
✅ Fast integration
✅ Always up to date
✅ Minimal merge conflicts

**Cons:**
❌ Requires mature CI/CD
❌ Needs feature flags
❌ Risk of breaking main
❌ Requires discipline

---

### Pattern 4: Forking Workflow (Open Source)

**Philosophy:** Contributors fork repository, submit PRs from fork

**Structure:**
```
upstream (original)
 └─ main

origin (your fork)
 └─ main
     ├─ feature/fix-bug
     └─ feature/add-feature
```

**Workflow:**

**One-time setup:**
```bash
# 1. Fork on GitHub (web UI)
# Creates: github.com/you/repo

# 2. Clone your fork
git clone git@github.com:you/repo.git
cd repo

# 3. Add upstream
git remote add upstream git@github.com:original/repo.git

# 4. Verify remotes
git remote -v
# origin    git@github.com:you/repo.git (fetch)
# origin    git@github.com:you/repo.git (push)
# upstream  git@github.com:original/repo.git (fetch)
# upstream  git@github.com:original/repo.git (push)
```

**Contribution workflow:**
```bash
# 1. Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 2. Create feature branch from upstream
git checkout -b feature/fix-typo upstream/main

# 3. Make changes
git add README.md
git commit -m "docs: fix typo in installation instructions"

# 4. Push to your fork
git push -u origin feature/fix-typo

# 5. Create PR on GitHub
# From: you/repo feature/fix-typo
# To: original/repo main

# 6. Address review feedback
git add README.md
git commit -m "docs: apply review suggestions"
git push origin feature/fix-typo

# 7. After PR merged
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
git branch -d feature/fix-typo
```

**Keep fork synced:**
```bash
# Regular sync (weekly)
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Or with alias
git config alias.sync '!git fetch upstream && git checkout main && git merge upstream/main && git push origin main'
git sync
```

**When to use:**
- Open source projects
- External contributors
- No write access to main repo
- Large community projects

**Pros:**
✅ Isolates contributions
✅ Safe for untrusted contributors
✅ Clear separation of official/fork
✅ Standard for open source

**Cons:**
❌ More complex setup
❌ Extra sync overhead
❌ Confusing for beginners

---

### Pattern 5: Pull Request Best Practices

**Problem:** Create effective, reviewable pull requests

**PR checklist:**
```markdown
## PR Description Template

### What does this PR do?
Brief summary of changes

### Why?
Context: Which problem does this solve?

### How?
Implementation approach

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Screenshots (for UI changes)

### Checklist
- [ ] Code follows style guide
- [ ] Self-review completed
- [ ] No console.log or debug code
- [ ] Documentation updated
- [ ] Breaking changes documented
- [ ] No merge conflicts

### Related Issues
Fixes #123
Closes #456
```

**Good PR:**
```bash
# ✅ GOOD: Small, focused PR
git checkout -b fix/email-validation
# ... fix one thing ...
git commit -m "fix: validate email format on signup

- Add email regex validation
- Show error message for invalid emails
- Add unit tests

Fixes #123"
git push -u origin fix/email-validation
```

**Bad PR:**
```bash
# ❌ BAD: Large, unfocused PR
git checkout -b updates
# ... change 50 files ...
git commit -m "updates"  # Vague message
# PR: "Various updates and fixes"
# 2000 lines changed across 50 files
```

**PR size guidelines:**
- **Small**: < 200 lines (ideal)
- **Medium**: 200-400 lines (acceptable)
- **Large**: 400-1000 lines (needs justification)
- **Too large**: > 1000 lines (split into multiple PRs)

**Commit organization:**
```bash
# Option 1: Multiple logical commits
git commit -m "feat: add user model"
git commit -m "feat: add user API endpoints"
git commit -m "test: add user tests"
# Keep all commits, merge with merge commit

# Option 2: Squash before merge
# Multiple WIP commits
git commit -m "wip: user model"
git commit -m "fix typo"
git commit -m "more work"
# Squash and merge on GitHub: becomes 1 commit

# Option 3: Rebase and clean
git rebase -i origin/main
# Clean up commits before PR
```

**When to use:**
- Every feature or bug fix
- All team collaboration
- Code review culture

---

### Pattern 6: Code Review Workflows

**Problem:** Effective code review process

**Reviewer responsibilities:**
```markdown
## Code Review Checklist

### Functionality
- [ ] Code does what PR says it does
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] No obvious bugs

### Code Quality
- [ ] Readable and maintainable
- [ ] Follows project conventions
- [ ] No unnecessary complexity
- [ ] DRY principle followed

### Testing
- [ ] Tests added for new code
- [ ] Tests actually test the code
- [ ] Edge cases tested
- [ ] Tests are readable

### Security
- [ ] No security vulnerabilities
- [ ] Input validation present
- [ ] No hardcoded secrets
- [ ] Dependencies are safe

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No N+1 queries
- [ ] Caching where appropriate
```

**Review workflow:**
```bash
# 1. Checkout PR branch
gh pr checkout 123
# or
git fetch origin pull/123/head:pr-123
git checkout pr-123

# 2. Review changes
git diff main...pr-123
git log main..pr-123

# 3. Test locally
npm install
npm test
npm run dev  # Manual testing

# 4. Leave review on GitHub
# - Comment on specific lines
# - Request changes or approve
# - Add summary comment

# 5. Author addresses feedback
# (Author makes changes)

# 6. Re-review
git pull origin pr-123
npm test

# 7. Approve and merge
```

**Review comments style:**
```markdown
# ✅ GOOD: Constructive, specific
"Consider extracting this logic into a separate function for reusability."
"This could cause a race condition if multiple requests occur simultaneously. Can we add locking?"
"Great implementation! Suggestion: add error handling for the API call."

# ❌ BAD: Vague, negative
"This is wrong."
"I don't like this."
"Change this."
```

**When to use:**
- All pull requests
- Before merging to main
- Knowledge sharing
- Quality assurance

---

### Pattern 7: Release Management

**Problem:** Organize and track releases

**Semantic Versioning:**
```
Version: MAJOR.MINOR.PATCH

MAJOR: Breaking changes (1.0.0 → 2.0.0)
MINOR: New features (1.0.0 → 1.1.0)
PATCH: Bug fixes (1.0.0 → 1.0.1)

Examples:
v1.0.0 - Initial release
v1.1.0 - Add user profiles
v1.1.1 - Fix login bug
v2.0.0 - New API (breaking change)
```

**Release workflow:**
```bash
# 1. Update version
npm version minor  # Updates package.json and creates git tag
# or manually:
echo "1.2.0" > VERSION

# 2. Update CHANGELOG.md
cat >> CHANGELOG.md << EOF
## [1.2.0] - 2024-02-10
### Added
- User profile page
- Email notifications

### Fixed
- Login validation bug
- Mobile responsive issues
EOF

# 3. Commit and tag
git add VERSION CHANGELOG.md package.json
git commit -m "chore: release v1.2.0"
git tag -a v1.2.0 -m "Release version 1.2.0"

# 4. Push
git push origin main --tags

# 5. Create GitHub Release
gh release create v1.2.0 \
  --title "Version 1.2.0" \
  --notes-file CHANGELOG.md

# 6. Deploy
./deploy.sh production v1.2.0
```

**Automated changelog:**
```bash
# Generate from conventional commits
npx conventional-changelog -p angular -i CHANGELOG.md -s

# Or use tool
npm install -g auto-changelog
auto-changelog
```

**When to use:**
- Scheduled releases
- Version tracking
- Deployment process
- User communication

---

### Pattern 8: Monorepo vs Multi-Repo

**Monorepo (one repo for everything):**
```
repo/
  ├─ packages/
  │   ├─ web-app/
  │   ├─ mobile-app/
  │   ├─ api/
  │   └─ shared-lib/
  ├─ .git/
  └─ package.json
```

**Advantages:**
✅ Single source of truth
✅ Atomic changes across projects
✅ Easy code sharing
✅ Unified CI/CD

**Challenges:**
❌ Large repository size
❌ Slower git operations
❌ Complicated CI/CD
❌ Need tools (Lerna, Nx, Turborepo)

**Multi-repo (separate repos):**
```
web-app/.git
mobile-app/.git
api/.git
shared-lib/.git (published as package)
```

**Advantages:**
✅ Simple git operations
✅ Independent deployments
✅ Clear ownership
✅ Standard tools work

**Challenges:**
❌ Version coordination
❌ Cross-repo changes complex
❌ Code duplication risk
❌ Multiple PRs needed

**When to use:**
- Monorepo: Tightly coupled services, shared team
- Multi-repo: Independent services, separate teams

---

## Choosing a Workflow

**Decision guide:**

```
Team size and project type:
├─ Startup (2-5 devs, web app)
│   → GitHub Flow
│
├─ Small team (5-10 devs, continuous deployment)
│   → GitHub Flow or Trunk-Based
│
├─ Medium team (10-30 devs, scheduled releases)
│   → Git Flow
│
├─ Large team (30+ devs, multiple products)
│   → Trunk-Based with feature flags
│
└─ Open source project
    → Forking Workflow
```

---

## Best Practices

1. **Document workflow** - README or CONTRIBUTING.md
2. **Protect main branch** - Require PRs and reviews
3. **Automate testing** - CI/CD on all PRs
4. **Small PRs** - < 400 lines when possible
5. **Quick reviews** - < 24 hours turnaround
6. **Feature flags** - For large features
7. **Semantic versioning** - Clear version numbers
8. **Changelog** - Document changes

## Related Sub-Skills

- Need branch basics? → `/git/branching`
- Merge conflicts in workflow? → `/git/conflicts`
- Push/pull in workflow? → `/git/remote`
- Release tagging? → `/git/basics`

## Quick Reference

```bash
# GitHub Flow
git checkout main && git pull
git checkout -b feature/name
git push -u origin feature/name
# Create PR, review, merge

# Git Flow
git checkout develop
git checkout -b feature/name
# Develop, then:
git checkout develop && git merge feature/name

# Release
git checkout -b release/v1.0.0 develop
git checkout main && git merge release/v1.0.0
git tag v1.0.0

# Forking
git clone git@github.com:you/fork.git
git remote add upstream git@github.com:original/repo.git
git fetch upstream
git merge upstream/main
```

---

**Last Updated:** 2025-02-11
**Version:** 1.0.0
