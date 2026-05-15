#!/usr/bin/env python3
"""
Web Crawler - httpx + BeautifulSoup4 + SQLite
Dùng cho website tĩnh (không cần JS rendering)

Usage:
    python crawler.py --url https://example.com --depth 2 --db data.sqlite
    python crawler.py --url https://example.com --depth 3 --delay 2.0
"""

import asyncio
import hashlib
import json
import re
import sqlite3
import time
from argparse import ArgumentParser
from collections import deque
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag

import httpx
from bs4 import BeautifulSoup

# ─── Config ───────────────────────────────────────────────────────────────────

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WebCrawler/1.0; +https://github.com/web-crawler)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
}

# ─── Database ─────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS pages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT UNIQUE NOT NULL,
    url_hash    TEXT UNIQUE NOT NULL,
    domain      TEXT NOT NULL,
    path        TEXT,
    title       TEXT,
    description TEXT,
    keywords    TEXT,
    html        TEXT,
    text        TEXT,
    h1          TEXT,
    h2_tags     TEXT,
    h3_tags     TEXT,
    og_tags     TEXT,
    schema_org  TEXT,
    nav_links   TEXT,
    status_code INTEGER,
    content_type TEXT,
    language    TEXT,
    depth       INTEGER DEFAULT 0,
    crawled_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS links (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    from_url    TEXT NOT NULL,
    to_url      TEXT NOT NULL,
    anchor_text TEXT,
    is_internal BOOLEAN DEFAULT 1,
    UNIQUE(from_url, to_url)
);

CREATE TABLE IF NOT EXISTS assets (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    page_url    TEXT NOT NULL,
    asset_url   TEXT NOT NULL,
    asset_type  TEXT,
    alt_text    TEXT,
    UNIQUE(page_url, asset_url)
);

CREATE INDEX IF NOT EXISTS idx_pages_domain ON pages(domain);
CREATE INDEX IF NOT EXISTS idx_pages_depth ON pages(depth);
CREATE INDEX IF NOT EXISTS idx_links_from ON links(from_url);
"""

def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def save_page(conn: sqlite3.Connection, data: dict):
    conn.execute("""
        INSERT OR REPLACE INTO pages
        (url, url_hash, domain, path, title, description, keywords,
         html, text, h1, h2_tags, h3_tags, og_tags, schema_org, nav_links,
         status_code, content_type, language, depth, crawled_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["url"], data["url_hash"], data["domain"], data.get("path"),
        data.get("title"), data.get("description"), data.get("keywords"),
        data.get("html"), data.get("text"),
        data.get("h1"), data.get("h2_tags"), data.get("h3_tags"),
        data.get("og_tags"), data.get("schema_org"), data.get("nav_links"),
        data.get("status_code"), data.get("content_type"),
        data.get("language"), data.get("depth"),
        datetime.now().isoformat()
    ))
    conn.commit()


def save_links(conn: sqlite3.Connection, from_url: str, links: list):
    for link in links:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO links (from_url, to_url, anchor_text, is_internal) VALUES (?, ?, ?, ?)",
                (from_url, link["url"], link.get("text", ""), link.get("internal", True))
            )
        except Exception:
            pass
    conn.commit()


def save_assets(conn: sqlite3.Connection, page_url: str, assets: list):
    for asset in assets:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO assets (page_url, asset_url, asset_type, alt_text) VALUES (?, ?, ?, ?)",
                (page_url, asset["url"], asset.get("type"), asset.get("alt"))
            )
        except Exception:
            pass
    conn.commit()


# ─── Parsing ──────────────────────────────────────────────────────────────────

def parse_page(url: str, html: str, status_code: int,
               content_type: str, depth: int, base_domain: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    parsed = urlparse(url)

    # Remove scripts/styles for text extraction
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Basic metadata
    title = soup.find("title")
    title = title.get_text(strip=True) if title else ""

    desc_tag = soup.find("meta", attrs={"name": re.compile("description", re.I)})
    description = desc_tag.get("content", "").strip() if desc_tag else ""

    keywords_tag = soup.find("meta", attrs={"name": re.compile("keywords", re.I)})
    keywords = keywords_tag.get("content", "").strip() if keywords_tag else ""

    lang_tag = soup.find("html")
    language = lang_tag.get("lang", "") if lang_tag else ""

    # Headings
    h1 = soup.find("h1")
    h1 = h1.get_text(strip=True) if h1 else ""
    h2_tags = json.dumps([h.get_text(strip=True) for h in soup.find_all("h2")[:20]])
    h3_tags = json.dumps([h.get_text(strip=True) for h in soup.find_all("h3")[:30]])

    # Open Graph
    og = {}
    for tag in soup.find_all("meta", property=re.compile("^og:")):
        og[tag.get("property", "")] = tag.get("content", "")
    og_tags = json.dumps(og) if og else None

    # JSON-LD (Schema.org)
    schema_scripts = soup.find_all("script", type="application/ld+json")
    schema_data = []
    for s in schema_scripts:
        try:
            schema_data.append(json.loads(s.string))
        except Exception:
            pass
    schema_org = json.dumps(schema_data) if schema_data else None

    # Navigation links
    nav = soup.find("nav")
    nav_links = []
    if nav:
        for a in nav.find_all("a", href=True):
            href = urljoin(url, a["href"])
            nav_links.append({"url": href, "text": a.get_text(strip=True)})
    nav_links_json = json.dumps(nav_links) if nav_links else None

    # Plain text
    text = soup.get_text(separator="\n", strip=True)
    text = re.sub(r"\n{3,}", "\n\n", text)  # compress whitespace

    # Links
    links = []
    for a in soup.find_all("a", href=True):
        href, _ = urldefrag(a["href"])
        if not href or href.startswith(("javascript:", "mailto:", "tel:", "#")):
            continue
        abs_url = urljoin(url, href)
        link_domain = urlparse(abs_url).netloc
        is_internal = link_domain == base_domain
        links.append({
            "url": abs_url,
            "text": a.get_text(strip=True)[:200],
            "internal": is_internal
        })

    # Assets
    assets = []
    for img in soup.find_all("img", src=True):
        assets.append({
            "url": urljoin(url, img["src"]),
            "type": "image",
            "alt": img.get("alt", "")
        })
    for link_tag in soup.find_all("link", rel="stylesheet"):
        if link_tag.get("href"):
            assets.append({"url": urljoin(url, link_tag["href"]), "type": "css"})
    for script in soup.find_all("script", src=True):
        assets.append({"url": urljoin(url, script["src"]), "type": "js"})

    return {
        "url": url,
        "url_hash": url_hash(url),
        "domain": parsed.netloc,
        "path": parsed.path,
        "title": title,
        "description": description,
        "keywords": keywords,
        "html": html,
        "text": text,
        "h1": h1,
        "h2_tags": h2_tags,
        "h3_tags": h3_tags,
        "og_tags": og_tags,
        "schema_org": schema_org,
        "nav_links": nav_links_json,
        "status_code": status_code,
        "content_type": content_type,
        "language": language,
        "depth": depth,
        "links": links,
        "assets": assets,
    }


# ─── Crawler ──────────────────────────────────────────────────────────────────

async def crawl(start_url: str, max_depth: int, db_path: str,
                delay: float = 1.5, max_pages: int = 10000):
    conn = init_db(db_path)
    visited = set()
    queue = deque([(start_url, 0)])  # (url, depth)
    base_domain = urlparse(start_url).netloc

    # Check robots.txt
    robots_url = f"{urlparse(start_url).scheme}://{base_domain}/robots.txt"
    disallowed = set()
    try:
        async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=10) as client:
            r = await client.get(robots_url)
            if r.status_code == 200:
                for line in r.text.splitlines():
                    if line.lower().startswith("disallow:"):
                        path = line.split(":", 1)[1].strip()
                        if path:
                            disallowed.add(path)
                print(f"[robots.txt] {len(disallowed)} disallowed paths")
    except Exception:
        pass

    def is_allowed(url: str) -> bool:
        path = urlparse(url).path
        return not any(path.startswith(d) for d in disallowed if d != "/")

    async with httpx.AsyncClient(
        headers=DEFAULT_HEADERS,
        timeout=30,
        follow_redirects=True,
        limits=httpx.Limits(max_connections=5)
    ) as client:
        page_count = 0

        while queue and page_count < max_pages:
            url, depth = queue.popleft()

            # Dedup và scope check
            if url in visited:
                continue
            if urlparse(url).netloc != base_domain:
                continue
            if not is_allowed(url):
                print(f"[SKIP robots] {url}")
                continue

            visited.add(url)

            try:
                print(f"[{page_count+1}] depth={depth} {url}")
                resp = await client.get(url)
                content_type = resp.headers.get("content-type", "")

                if "text/html" not in content_type:
                    continue

                data = parse_page(url, resp.text, resp.status_code,
                                  content_type, depth, base_domain)
                save_page(conn, data)
                save_links(conn, url, data["links"])
                save_assets(conn, url, data["assets"])

                page_count += 1

                # Queue internal links nếu chưa đạt max depth
                if depth < max_depth:
                    for link in data["links"]:
                        if link["internal"] and link["url"] not in visited:
                            queue.append((link["url"], depth + 1))

                await asyncio.sleep(delay)

            except httpx.TimeoutException:
                print(f"[TIMEOUT] {url}")
            except Exception as e:
                print(f"[ERROR] {url}: {e}")

    conn.close()
    print(f"\nDone! Crawled {page_count} pages → {db_path}")
    return page_count


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = ArgumentParser(description="Web Crawler - lưu vào SQLite")
    parser.add_argument("--url", required=True, help="URL bắt đầu crawl")
    parser.add_argument("--depth", type=int, default=2, help="Độ sâu crawl (default: 2)")
    parser.add_argument("--db", default="crawl.sqlite", help="File SQLite output")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay giữa requests (giây)")
    parser.add_argument("--max-pages", type=int, default=10000, help="Số trang tối đa")
    args = parser.parse_args()

    asyncio.run(crawl(
        start_url=args.url,
        max_depth=args.depth,
        db_path=args.db,
        delay=args.delay,
        max_pages=args.max_pages,
    ))


if __name__ == "__main__":
    main()
