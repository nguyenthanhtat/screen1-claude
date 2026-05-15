# Database Schema cho Web Crawler

## SQLite Schema (dùng cho project nhỏ/local)

```sql
-- Bảng chính: các trang đã crawl
CREATE TABLE pages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT UNIQUE NOT NULL,
    url_hash    TEXT UNIQUE NOT NULL,     -- MD5/SHA256 của URL để dedup
    domain      TEXT NOT NULL,
    path        TEXT,
    title       TEXT,
    description TEXT,                     -- meta description
    keywords    TEXT,                     -- meta keywords
    html        TEXT,                     -- raw HTML
    text        TEXT,                     -- plain text đã extract
    status_code INTEGER,
    content_type TEXT,
    language    TEXT,
    depth       INTEGER DEFAULT 0,        -- độ sâu từ URL gốc
    crawled_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME,
    is_indexed  BOOLEAN DEFAULT FALSE
);

-- Bảng links: quan hệ giữa các trang
CREATE TABLE links (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    from_url    TEXT NOT NULL,
    to_url      TEXT NOT NULL,
    anchor_text TEXT,
    is_internal BOOLEAN DEFAULT TRUE,
    rel         TEXT,                     -- nofollow, noopener, etc.
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(from_url, to_url)
);

-- Bảng assets: hình ảnh, CSS, JS, file
CREATE TABLE assets (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    page_url     TEXT NOT NULL,
    asset_url    TEXT NOT NULL,
    asset_type   TEXT,                    -- image, css, js, font, video
    local_path   TEXT,                    -- đường dẫn file đã download
    file_size    INTEGER,
    mime_type    TEXT,
    alt_text     TEXT,                    -- cho hình ảnh
    downloaded   BOOLEAN DEFAULT FALSE,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(page_url, asset_url)
);

-- Bảng queue: URL đang chờ crawl
CREATE TABLE crawl_queue (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT UNIQUE NOT NULL,
    priority    INTEGER DEFAULT 0,
    depth       INTEGER DEFAULT 0,
    status      TEXT DEFAULT 'pending',  -- pending, processing, done, failed
    retries     INTEGER DEFAULT 0,
    error       TEXT,
    added_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME
);

-- Bảng metadata cấu trúc web
CREATE TABLE site_structure (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT UNIQUE NOT NULL,
    h1          TEXT,
    h2_tags     TEXT,                    -- JSON array
    h3_tags     TEXT,                    -- JSON array
    nav_links   TEXT,                    -- JSON array
    schema_org  TEXT,                    -- JSON-LD data
    og_tags     TEXT,                    -- Open Graph JSON
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_pages_domain ON pages(domain);
CREATE INDEX idx_pages_depth ON pages(depth);
CREATE INDEX idx_pages_crawled ON pages(crawled_at);
CREATE INDEX idx_links_from ON links(from_url);
CREATE INDEX idx_links_to ON links(to_url);
CREATE INDEX idx_queue_status ON crawl_queue(status, priority);
```

---

## PostgreSQL Schema (production)

```sql
-- Thêm full-text search support
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE pages (
    id          SERIAL PRIMARY KEY,
    url         TEXT UNIQUE NOT NULL,
    url_hash    CHAR(64) UNIQUE NOT NULL,
    domain      TEXT NOT NULL,
    path        TEXT,
    title       TEXT,
    description TEXT,
    keywords    TEXT,
    html        TEXT,
    text        TEXT,
    text_search TSVECTOR,               -- full-text search vector
    status_code SMALLINT,
    content_type TEXT,
    language    CHAR(5),
    depth       SMALLINT DEFAULT 0,
    metadata    JSONB,                  -- flexible extra data
    crawled_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ
);

-- Full-text search index
CREATE INDEX idx_pages_text_search ON pages USING GIN(text_search);
CREATE INDEX idx_pages_metadata ON pages USING GIN(metadata);
CREATE INDEX idx_pages_domain ON pages(domain);

-- Trigger cập nhật text_search tự động
CREATE OR REPLACE FUNCTION update_text_search()
RETURNS TRIGGER AS $$
BEGIN
    NEW.text_search = to_tsvector('english', 
        COALESCE(NEW.title, '') || ' ' || 
        COALESCE(NEW.description, '') || ' ' ||
        COALESCE(NEW.text, '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER pages_text_search_update
    BEFORE INSERT OR UPDATE ON pages
    FOR EACH ROW EXECUTE FUNCTION update_text_search();
```

---

## MongoDB Schema (flexible)

```javascript
// Collection: pages
{
  _id: ObjectId,
  url: String,          // unique
  url_hash: String,     // unique index
  domain: String,
  title: String,
  description: String,
  html: String,
  text: String,
  headings: {
    h1: [String],
    h2: [String],
    h3: [String]
  },
  meta: {
    keywords: String,
    og: Object,         // Open Graph tags
    schema: Object,     // JSON-LD
    canonical: String
  },
  links: {
    internal: [String],
    external: [String]
  },
  assets: {
    images: [{ url: String, alt: String, local: String }],
    css: [String],
    js: [String]
  },
  status_code: Number,
  depth: Number,
  language: String,
  crawled_at: Date,
  updated_at: Date
}

// Indexes
db.pages.createIndex({ url: 1 }, { unique: true })
db.pages.createIndex({ domain: 1 })
db.pages.createIndex({ depth: 1 })
db.pages.createIndex({ title: "text", text: "text" })  // text search
```

---

## Query Mẫu

```sql
-- Lấy tất cả trang theo domain
SELECT url, title, depth FROM pages WHERE domain = 'example.com' ORDER BY depth;

-- Tìm kiếm full-text (PostgreSQL)
SELECT url, title, ts_headline('english', text, q) as snippet
FROM pages, to_tsquery('english', 'keyword') q
WHERE text_search @@ q
ORDER BY ts_rank(text_search, q) DESC;

-- Lấy cấu trúc link graph
SELECT from_url, to_url, anchor_text FROM links WHERE is_internal = TRUE;

-- Trang chưa có hình ảnh
SELECT p.url FROM pages p
LEFT JOIN assets a ON p.url = a.page_url AND a.asset_type = 'image'
WHERE a.id IS NULL;

-- Thống kê theo depth
SELECT depth, COUNT(*) as page_count FROM pages GROUP BY depth ORDER BY depth;
```
