---
name: web-crawler
description: "Crawl và clone hoàn toàn một website, tạo Next.js website chạy được local. Use when: user muốn clone/mirror website, scrape dữ liệu, copy cấu trúc trang web, tạo website từ site có sẵn, crawl content để phân tích."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# Web Crawler → Website Generator Skill

Skill này crawl một website và tạo ra **Next.js website hoàn chỉnh chạy được local**, với layout responsive cao cấp cho cả PC và mobile.

## Trigger Scenarios

- "Crawl website X lấy toàn bộ nội dung"
- "Clone/copy website X"
- "Tạo website local từ site X"
- "Scrape dữ liệu từ trang X"
- "Mirror website để dùng offline"

---

## Workflow Đầy Đủ (6 bước)

### Bước 1 — Xác định yêu cầu

Hỏi user (xem chi tiết tại [references/planning-questions.md](references/planning-questions.md)):
- URL gốc cần crawl
- Website có dùng JavaScript không? (→ chọn crawler)
- Màu chủ đạo của site gốc? (hex color)
- Tên website?

---

### Bước 2 — Chọn crawler phù hợp

| Website | Crawler |
|---------|---------|
| Tĩnh (HTML, WordPress, PHP) | `scripts/crawler.py` |
| Có JS (React, Vue, Next.js) | `scripts/crawler_playwright.py` |

---

### Bước 3 — Cài môi trường

```bash
pip install httpx beautifulsoup4 playwright aiosqlite lxml
playwright install chromium
```

---

### Bước 4 — Chạy crawler

```bash
# Website tĩnh
python scripts/crawler.py --url https://example.com --depth 2 --db site.sqlite

# Website có JavaScript (React, Vue, SPA)
python scripts/crawler_playwright.py --url https://example.com --depth 2 --db site.sqlite
```

**Tham số quan trọng:**
- `--depth 2` — đủ cho hầu hết site (depth 1 = chỉ trang chủ)
- `--max-pages 200` — giới hạn nếu site lớn
- `--delay 2.0` — tránh bị block

---

### Bước 5 — Generate website

```bash
python scripts/generate_site.py \
  --db site.sqlite \
  --out ./output-site \
  --site-name "Tên Website" \
  --primary-color "#BB162B" \
  --download-images
```

Script này tạo **Next.js project hoàn chỉnh** gồm:
- `package.json` — dependencies (Next.js 15, Tailwind v4, TypeScript)
- `src/lib/data.ts` — toàn bộ data từ crawl
- `src/app/layout.tsx` — responsive header/footer với mobile menu
- `src/app/page.tsx` — homepage với hero + page grid
- `src/app/[slug]/page.tsx` — content pages với sidebar
- `src/app/globals.css` — Tailwind v4 + custom animations

---

### Bước 6 — Chạy local

```bash
cd output-site
npm install
npm run dev
# → http://localhost:3000
```

---

## Output Features

### Layout PC (≥1024px)
- Fixed header với dropdown navigation
- 2-col layout: main content + sticky sidebar
- Page grid 3 cột ở homepage

### Layout Mobile (<768px)
- Hamburger menu với slide-down drawer
- Single column layout
- Touch-friendly buttons (min 44px tap target)
- Breadcrumb navigation

### UX
- Smooth scroll, fade-up animations
- Sticky sidebar (related pages)
- 404 not-found page
- SEO metadata tự động (title, description)
- Static Generation (SSG) — nhanh, không cần server

---

## Core Principles

1. **Luôn kiểm tra robots.txt** trước khi crawl
2. **Rate limiting**: delay 1.5–2s giữa requests
3. **Deduplication**: URL hash để tránh crawl trùng
4. **Error handling**: retry với exponential backoff
5. **Responsive first**: mobile layout là ưu tiên
6. **Respect scope**: chỉ crawl domain mục tiêu

---

## Files

| File | Mô tả |
|------|-------|
| `scripts/crawler.py` | Crawler cho site tĩnh (httpx + BS4) |
| `scripts/crawler_playwright.py` | Crawler cho JS/SPA (Playwright) |
| `scripts/generate_site.py` | **Tạo Next.js website từ SQLite** |
| `references/planning-questions.md` | Câu hỏi cần hỏi trước khi bắt đầu |
| `references/tech-stack.md` | So sánh tool crawl |
| `references/database-schema.md` | Schema SQLite |
| `references/data-processing.md` | Query và xử lý dữ liệu |

---

## Ví dụ hoàn chỉnh — Clone kia-hcm.com

```bash
# 1. Crawl (site WordPress có lazy loading → dùng Playwright)
python scripts/crawler_playwright.py \
  --url https://kia-hcm.com \
  --depth 2 \
  --db kia.sqlite \
  --delay 2.0

# 2. Generate Next.js site
python scripts/generate_site.py \
  --db kia.sqlite \
  --out ./kia-local \
  --site-name "KIA HCM" \
  --primary-color "#BB162B" \
  --download-images

# 3. Chạy
cd kia-local && npm install && npm run dev
```
