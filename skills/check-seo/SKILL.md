---
name: check-seo
description: "Audit any website's SEO using @seomator/seo-audit, suggest prioritized fixes, then auto-apply fixes to the local codebase. Supports Next.js, plain HTML, Nuxt, and Vue."
---

# check-seo

Audit any website's SEO, suggest prioritized fixes, then auto-apply fixes to the local codebase.

## When to use
Triggered by: "check SEO", "audit SEO", "fix SEO", "my SEO score", "audit https://...", "improve SEO"

## Prerequisites

Check and install if missing:
```bash
seomator --version 2>/dev/null || npm install -g @seomator/seo-audit
```

For Core Web Vitals (optional — requires Chrome/Chromium):
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

## Phase 4 — Fix

For each approved issue, apply the correct fix based on stack:

### Next.js (App Router) fixes

**Missing title / description** → `src/app/layout.tsx`:
```tsx
export const metadata: Metadata = {
  title: 'Your Page Title (50-60 chars)',
  description: 'Your meta description (120-160 chars)',
}
```

**Missing canonical** → `src/app/layout.tsx`:
```tsx
export const metadata: Metadata = {
  alternates: { canonical: 'https://yourdomain.com' },
}
```

**Missing OG / Twitter tags** → `src/app/layout.tsx`:
```tsx
export const metadata: Metadata = {
  openGraph: {
    title: 'Your Title',
    description: 'Your description',
    url: 'https://yourdomain.com',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: { card: 'summary_large_image', title: 'Your Title', description: 'Your description', images: ['/og-image.png'] },
}
```

**Missing robots.txt** → create `src/app/robots.ts`:
```ts
import { MetadataRoute } from 'next'
export default function robots(): MetadataRoute.Robots {
  return { rules: { userAgent: '*', allow: '/' }, sitemap: 'https://yourdomain.com/sitemap.xml' }
}
```

**Missing sitemap** → create `src/app/sitemap.ts`:
```ts
import { MetadataRoute } from 'next'
export default function sitemap(): MetadataRoute.Sitemap {
  return [{ url: 'https://yourdomain.com', lastModified: new Date(), changeFrequency: 'monthly', priority: 1 }]
}
```

**Structured data** → add to `src/app/layout.tsx`:
```tsx
const jsonLd = { '@context': 'https://schema.org', '@type': 'WebSite', name: 'Your Site', url: 'https://yourdomain.com' }
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
```

**Missing alt text** → find all `<Image>` / `<img>` without `alt` prop, add descriptive alt text.

### Plain HTML fixes

Add to `<head>` in the relevant `.html` file:
```html
<title>Your Title (50-60 chars)</title>
<meta name="description" content="Your description (120-160 chars)">
<link rel="canonical" href="https://yourdomain.com/page">
<meta property="og:title" content="Your Title">
<meta property="og:description" content="Your description">
<meta property="og:image" content="https://yourdomain.com/og-image.png">
<meta property="og:url" content="https://yourdomain.com">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Your Site","url":"https://yourdomain.com"}</script>
```

**Missing robots.txt** → create `robots.txt`:
```
User-agent: *
Allow: /
Sitemap: https://yourdomain.com/sitemap.xml
```

### Nuxt 3 fixes

**Meta** → `nuxt.config.ts` or per-page `useSeoMeta()`:
```ts
useSeoMeta({ title: 'Your Title', description: 'Your description', ogTitle: 'Your Title', ogDescription: 'Your description', ogImage: '/og-image.png' })
```

### Issue ID → Fix Map

| seomator issue id | Action |
|---|---|
| `meta-description` | Add description metadata |
| `title-missing` | Add title metadata |
| `title-length` | Shorten title to 50-60 chars |
| `canonical-missing` | Add canonical link |
| `og-title`, `og-description`, `og-image` | Add Open Graph meta |
| `twitter-card` | Add Twitter card meta |
| `structured-data` | Add JSON-LD schema |
| `robots-txt` | Create robots.txt |
| `sitemap` | Create sitemap.xml |
| `image-alt` | Add alt attributes to images |
| `h1-missing` | Add single H1 to page |
| `h1-multiple` | Remove extra H1 tags |
| `https`, `gzip`, `core-web-vitals` | **Manual fix** — add to report |

**Rules:**
- Never fix what cannot be confidently mapped to a file
- Always show before/after for each edit
- If a needed file doesn't exist, create it
- Group unmappable issues into a "Manual Fixes" section

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

For issues that couldn't be auto-fixed:
```
MANUAL FIXES REQUIRED:
1. [Performance] Enable gzip/brotli compression
   → Configure in hosting provider (nginx, vercel.json, etc.)

2. [Crawlability] Submit sitemap to Google Search Console
   → https://search.google.com/search-console
```

## Seomator Reference

**Scoring:** 90-100=A, 80-89=B, 70-79=C, 50-69=D, 0-49=F

**20 Audit Categories (top by weight):**
Core SEO (12%), Performance (12%), Links (8%), Images (8%), Security (8%), Technical SEO (7%), Crawlability (7%), Structured Data (6%), JS Rendering (6%), Accessibility (6%), Content (5%), Social (5%), E-E-A-T (4%), URL Structure (4%), Redirects (3%), Mobile (3%), and more.

**Always use `--format llm`** — 50-70% smaller than JSON, structured XML optimized for AI parsing.
