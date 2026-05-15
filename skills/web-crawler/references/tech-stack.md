# Tech Stack So Sánh cho Web Crawling

## 1. httpx + BeautifulSoup4 (Khuyên dùng cho starter)

**Khi nào dùng:** Website tĩnh, HTML đơn giản, không cần JS rendering

**Ưu điểm:**
- Async nhanh, nhẹ
- Dễ dùng, ít setup
- Phù hợp với hầu hết blog, tin tức, e-commerce đơn giản

**Nhược điểm:**
- Không render JavaScript → không lấy được nội dung SPA (React/Vue/Angular)
- Cần tự xử lý pagination, session, cookies

```bash
pip install httpx beautifulsoup4 lxml aiosqlite
```

---

## 2. Playwright (Khuyên dùng cho SPA/JS-heavy sites)

**Khi nào dùng:** React, Vue, Angular, Next.js, lazy-loading content, infinite scroll

**Ưu điểm:**
- Render JavaScript đầy đủ như browser thật
- Hỗ trợ screenshot, PDF
- Xử lý được AJAX, fetch, WebSocket
- Có thể click, scroll, fill form

**Nhược điểm:**
- Chậm hơn httpx (~5-10x)
- Dùng nhiều RAM hơn
- Setup phức tạp hơn

```bash
pip install playwright
playwright install chromium
```

---

## 3. Scrapy (Khuyên dùng cho crawl quy mô lớn)

**Khi nào dùng:** Crawl hàng nghìn trang, cần pipeline phức tạp, team project

**Ưu điểm:**
- Framework chuyên nghiệp, production-ready
- Built-in middleware (retry, throttle, proxy, cookies)
- Dễ scale, có Scrapy Cloud
- Có scrapy-playwright để xử lý JS

**Nhược điểm:**
- Learning curve cao
- Overkill cho project nhỏ

```bash
pip install scrapy scrapy-playwright
```

---

## 4. wget / httrack (Clone toàn bộ site)

**Khi nào dùng:** Muốn mirror website hoàn toàn để dùng offline

**wget:**
```bash
wget --mirror --convert-links --adjust-extension \
     --page-requisites --no-parent \
     -e robots=off \
     https://example.com
```

**httrack:**
```bash
httrack https://example.com -O ./cloned -%v
```

**Ưu điểm:**
- Không cần code, chạy ngay
- Download cả CSS, JS, hình ảnh

**Nhược điểm:**
- Không lưu vào database
- Không render JavaScript

---

## 5. Database Choice

| Database | Khi nào dùng | Cài đặt |
|----------|-------------|---------|
| **SQLite** | Project nhỏ, local, ≤1M rows | Built-in Python |
| **PostgreSQL** | Production, team, full-text search | `pip install asyncpg` |
| **MongoDB** | Dữ liệu không có schema cố định | `pip install motor` |
| **Elasticsearch** | Cần search nhanh trong content | `pip install elasticsearch` |

---

## Recommendation Matrix

```
Website tĩnh + nhỏ    → httpx + BS4 + SQLite
Website tĩnh + lớn    → Scrapy + SQLite/Postgres
Website JS + nhỏ      → Playwright + SQLite
Website JS + lớn      → Scrapy + playwright plugin + Postgres
Clone offline         → wget --mirror hoặc httrack
Cần search content    → bất kỳ crawler + Elasticsearch
```
