# Planning Questions — Web Crawler

Trước khi bắt đầu crawl, xác định rõ các thông tin sau để chọn đúng tool và cấu hình.

## Câu hỏi bắt buộc

| # | Câu hỏi | Ảnh hưởng |
|---|---------|-----------|
| 1 | URL gốc cần crawl là gì? | Xác định base domain và scope |
| 2 | Website có dùng JavaScript (React, Vue, Next.js)? | → Playwright vs httpx |
| 3 | Mục tiêu cuối: lưu DB, hay tạo website chạy được? | → Chỉ crawl, hoặc crawl + generate |
| 4 | Bao nhiêu trang? (ước tính) | Chọn max_depth và max_pages |
| 5 | Cần ảnh tải về local không? | → `--download-images` flag |

## Câu hỏi nâng cao

| # | Câu hỏi | Mặc định |
|---|---------|---------|
| 6 | Màu chủ đạo của site gốc? | `#2563eb` |
| 7 | Tên website hiển thị? | Lấy từ domain |
| 8 | Cần tôn trọng robots.txt không? | Có (mặc định) |
| 9 | Delay giữa requests? | 1.5–2.0 giây |
| 10 | Giới hạn số trang tối đa? | 500 trang |

## Decision Tree

```
Website mục tiêu
├── Tĩnh (HTML thuần, WordPress, PHP)
│   └── → crawler.py (httpx + BS4)
└── Có JS (React, Vue, Next.js, SPA)
    └── → crawler_playwright.py

Mục tiêu output
├── Chỉ cần data/DB
│   └── → Dừng sau bước 4
└── Muốn website chạy được local
    └── → Thêm bước 5: generate_site.py
```

## Gợi ý depth theo loại site

| Loại site | depth khuyên dùng |
|-----------|------------------|
| Landing page đơn giản | 1 |
| Blog / News site | 2 |
| E-commerce nhỏ | 2–3 |
| Portal lớn | 3 (giới hạn max_pages=200) |
| Documentation site | 3–4 |
