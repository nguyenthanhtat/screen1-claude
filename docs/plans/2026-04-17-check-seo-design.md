# check-seo Skill Design
Date: 2026-04-17

## Goal
A Claude Code skill that audits any website's SEO using `@seomator/seo-audit`, suggests prioritized fixes, then auto-applies fixes to the local codebase.

## Three-Phase Flow

```
Phase 1: AUDIT   → seomator audit <url> --format llm → parse XML
Phase 2: SUGGEST → group by severity, show score + top issues
Phase 3: FIX     → detect stack → map issues to files → edit → re-audit
```

## Stack Detection
| Signal | Stack |
|---|---|
| `next.config.*` or `src/app/layout.tsx` | Next.js |
| `nuxt.config.*` | Nuxt |
| `*.html`, no framework config | Plain HTML |
| `vite.config.*` + `index.html` | Vue SPA |
| fallback | HTML editing |

## Issue → File Mapping
| Issue | Next.js | HTML |
|---|---|---|
| Missing title | `layout.tsx` metadata | `<title>` in `<head>` |
| Missing meta description | `layout.tsx` metadata | `<meta name="description">` |
| Missing canonical | `metadata.alternates.canonical` | `<link rel="canonical">` |
| Missing OG tags | `metadata.openGraph` | `<meta property="og:*">` |
| Missing schema | JsonLd component | `<script type="application/ld+json">` |
| Missing alt text | `<Image alt="">` in components | `<img alt="">` |
| Missing robots.txt | `app/robots.ts` | `robots.txt` |
| Missing sitemap | `app/sitemap.ts` | `sitemap.xml` |

## Rules
- Only fix issues that map confidently to a file
- Show before/after for every edit
- Unfixable issues go into a manual-fixes report
- Re-run audit after fixes to show score delta

## Skill Files
```
.claude/skills/check-seo/
├── SKILL.md
└── references/
    ├── seomator.md
    └── fix-maps.md
```

## Prerequisites
- Node.js 18+
- `npm install -g @seomator/seo-audit`
- Playwright Chromium (optional, for Core Web Vitals)
