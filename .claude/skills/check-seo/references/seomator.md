# Seomator CLI Reference

## Installation
```bash
npm install -g @seomator/seo-audit
npx playwright install chromium  # optional, for Core Web Vitals
```

## Key Commands
```bash
seomator init                          # create seomator.toml config
seomator audit <url>                   # audit with console output
seomator audit <url> --format llm      # token-optimized XML for AI (use this)
seomator audit <url> --format json     # full JSON output
seomator audit <url> --format html     # HTML report
seomator audit <url> --format markdown # Markdown report
```

## Always use `--format llm`
- 50-70% smaller than JSON
- XML structured for AI parsing
- Includes severity, category, score, and fix hints

## XML Output Schema
```xml
<audit url="https://example.com" score="67" grade="D">
  <category name="Core SEO" score="45" weight="0.12">
    <issue id="meta-description" severity="critical" score="0">
      <title>Missing meta description</title>
      <description>No meta description found. Add one (120-160 chars).</description>
      <impact>high</impact>
    </issue>
    <issue id="title-length" severity="warning" score="50">
      <title>Title tag too long</title>
      <description>Title is 87 chars. Recommended max: 60.</description>
      <impact>medium</impact>
    </issue>
  </category>
</audit>
```

## Scoring System
| Score | Grade | Meaning |
|---|---|---|
| 90-100 | A | Excellent |
| 80-89 | B | Good |
| 70-79 | C | Average |
| 50-69 | D | Poor |
| 0-49 | F | Critical |

## Severity Levels
- `critical` — Fix immediately, major SEO impact
- `warning` — Should fix, moderate impact
- `info` — Nice to have, minor impact

## 20 Audit Categories
1. Core (title, description, canonical) — 12% weight
2. Performance (CWV, CSS/JS) — 12%
3. Links (internal/external) — 8%
4. Images (alt text, formats) — 8%
5. Security (HTTPS, headers) — 8%
6. Technical SEO — 7%
7. Crawlability (robots, sitemap) — 7%
8. Structured Data (schema) — 6%
9. JavaScript Rendering — 6%
10. Accessibility — 6%
11. Content — 5%
12. Social (OG, Twitter) — 5%
13. E-E-A-T — 4%
14. URL Structure — 4%
15. Redirects — 3%
16. Mobile — 3%
17. Internationalization — 2%
18. HTML Validation — 2%
19. AI/GEO Readiness — 1%
20. Legal Compliance — 1%
