# check-seo

Audit any website's SEO, suggest prioritized fixes, then auto-apply fixes to the local codebase.

## When to use
Triggered by: "check SEO", "audit SEO", "fix SEO", "my SEO score", "audit https://...", "improve SEO"

## Prerequisites

Check and install if missing:
```bash
seomator --version 2>/dev/null || npm install -g @seomator/seo-audit
```

For Core Web Vitals (optional):
```bash
npx playwright install chromium
```

## Phase 1 — Audit

Run the audit with LLM-optimized output:
```bash
seomator audit <url> --format llm
```

Parse the XML output to extract:
- Overall score (0-100) and grade (A-F)
- Per-category scores and weights
- All issues with severity: `critical`, `warning`, `info`

Display a summary table:
```
Overall: 67/100 (D)

Category         Score  Issues
Core SEO          45    3 critical, 2 warnings
Performance       72    1 critical, 4 warnings
Security          88    0 critical, 1 warning
...
```

## Phase 2 — Suggest

Group all issues by severity and show the top 10 prioritized by impact:

```
CRITICAL (fix these first):
1. [Core SEO] Missing meta description — affects click-through rate
2. [Core SEO] Title tag too long (87 chars, max 60) — truncated in SERPs
3. [Performance] No image lazy loading — hurts LCP score
...

WARNINGS:
4. [Security] Missing X-Frame-Options header
...
```

Ask the user:
> "Found X critical issues and Y warnings. Fix all critical issues automatically? (yes/no/select)"

If "select", list issues numbered so user can pick which to fix.

## Phase 3 — Detect Stack

From the project root, detect the tech stack:

```bash
# Check for framework config files
ls next.config.* 2>/dev/null && echo "nextjs"
ls nuxt.config.* 2>/dev/null && echo "nuxt"
ls vite.config.* 2>/dev/null && echo "vite"
find . -name "*.html" -maxdepth 3 | head -5
```

Detection rules:
- `next.config.*` OR `src/app/layout.tsx` OR `pages/_app.tsx` → **Next.js**
- `nuxt.config.*` → **Nuxt**
- `vite.config.*` + `index.html` → **Vue SPA**
- `*.html` files, no framework → **Plain HTML**
- Unknown → treat as Plain HTML

Load the appropriate fix map from `references/fix-maps.md`.

## Phase 4 — Fix

For each approved issue:

1. Find the target file using the fix map (see `references/fix-maps.md`)
2. Show the planned edit:
   ```
   File: src/app/layout.tsx
   Adding: description to metadata export
   ```
3. Apply the fix with Edit tool
4. Confirm the fix was applied correctly

**Rules:**
- Never fix what cannot be confidently mapped to a file
- Always show before/after for each edit
- If a file doesn't exist and needs to be created, create it
- Group unmappable issues into a "Manual Fixes" section at the end

## Phase 5 — Verify

Re-run the audit after all fixes:
```bash
seomator audit <url> --format llm
```

Show score delta:
```
Before: 67/100 (D)
After:  84/100 (B)  ▲ +17 points

Fixed: 8 issues
Remaining manual fixes: 3 issues (see below)
```

## Manual Fixes Report

For issues that couldn't be auto-fixed, provide specific instructions:
```
MANUAL FIXES REQUIRED:
1. [Performance] Enable server-side compression (gzip/brotli)
   → Configure in your hosting provider or server (nginx/vercel.json)
   → Expected impact: +5-8 points

2. [Crawlability] Submit sitemap to Google Search Console
   → https://search.google.com/search-console
```

## Reference Files
- `references/seomator.md` — CLI flags, XML output schema, scoring system
- `references/fix-maps.md` — Issue-to-file mapping for each stack
