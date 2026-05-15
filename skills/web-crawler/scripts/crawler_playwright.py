#!/usr/bin/env python3
"""
Web Crawler với Playwright - dành cho website có JavaScript (React, Vue, Next.js)

Cần cài:
    pip install playwright aiosqlite beautifulsoup4 lxml
    playwright install chromium

Usage:
    python crawler_playwright.py --url https://example.com --depth 2
"""

import asyncio
import hashlib
import json
import re
import sqlite3
from argparse import ArgumentParser
from collections import deque
from datetime import datetime
from urllib.parse import urljoin, urlparse, urldefrag

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

DEFAULT_VIEWPORT = {"width": 1280, "height": 800}

SCHEMA = """
CREATE TABLE IF NOT EXISTS pages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT UNIQUE NOT NULL,
    url_hash    TEXT UNIQUE NOT NULL,
    domain      TEXT NOT NULL,
    path        TEXT,
    title       TEXT,
    description TEXT,
    html        TEXT,
    text        TEXT,
    h1          TEXT,
    h2_tags     TEXT,
    screenshot  BLOB,
    status_code INTEGER,
    depth       INTEGER DEFAULT 0,
    crawled_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_url TEXT NOT NULL,
    to_url TEXT NOT NULL,
    anchor_text TEXT,
    is_internal BOOLEAN DEFAULT 1,
    UNIQUE(from_url, to_url)
);
CREATE INDEX IF NOT EXISTS idx_pages_domain ON pages(domain);
"""


def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def extract_data(url: str, html: str, depth: int, base_domain: str, screenshot: bytes = None) -> dict:
    soup = BeautifulSoup(html, "lxml")
    parsed = urlparse(url)

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = soup.find("title")
    title = title.get_text(strip=True) if title else ""

    desc = soup.find("meta", attrs={"name": re.compile("description", re.I)})
    description = desc.get("content", "").strip() if desc else ""

    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""
    h2_tags = json.dumps([h.get_text(strip=True) for h in soup.find_all("h2")[:20]])

    text = soup.get_text(separator="\n", strip=True)
    text = re.sub(r"\n{3,}", "\n\n", text)

    links = []
    for a in soup.find_all("a", href=True):
        href, _ = urldefrag(a["href"])
        if not href or href.startswith(("javascript:", "mailto:", "#")):
            continue
        abs_url = urljoin(url, href)
        link_domain = urlparse(abs_url).netloc
        links.append({
            "url": abs_url,
            "text": a.get_text(strip=True)[:200],
            "internal": link_domain == base_domain
        })

    return {
        "url": url,
        "url_hash": url_hash(url),
        "domain": parsed.netloc,
        "path": parsed.path,
        "title": title,
        "description": description,
        "html": html,
        "text": text,
        "h1": h1_text,
        "h2_tags": h2_tags,
        "screenshot": screenshot,
        "depth": depth,
        "links": links,
    }


async def crawl_playwright(start_url: str, max_depth: int, db_path: str,
                            delay: float = 2.0, max_pages: int = 5000,
                            take_screenshots: bool = False):
    conn = init_db(db_path)
    visited = set()
    queue = deque([(start_url, 0)])
    base_domain = urlparse(start_url).netloc
    page_count = 0

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=DEFAULT_VIEWPORT,
            user_agent="Mozilla/5.0 (compatible; WebCrawler/1.0)",
            ignore_https_errors=True,
        )
        page = await context.new_page()

        # Block unnecessary resources để tăng tốc
        await page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,otf}", lambda r: r.abort())

        while queue and page_count < max_pages:
            url, depth = queue.popleft()

            if url in visited or urlparse(url).netloc != base_domain:
                continue
            visited.add(url)

            try:
                print(f"[{page_count+1}] depth={depth} {url}")

                response = await page.goto(url, wait_until="networkidle", timeout=30000)
                status_code = response.status if response else 0

                # Đợi JS render xong
                await page.wait_for_timeout(1000)

                # Scroll để trigger lazy loading
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(500)

                html = await page.content()
                screenshot = None
                if take_screenshots:
                    screenshot = await page.screenshot(full_page=True)

                data = extract_data(url, html, depth, base_domain, screenshot)
                data["status_code"] = status_code

                # Save to DB
                conn.execute("""
                    INSERT OR REPLACE INTO pages
                    (url, url_hash, domain, path, title, description, html, text,
                     h1, h2_tags, screenshot, status_code, depth, crawled_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["url"], data["url_hash"], data["domain"], data.get("path"),
                    data.get("title"), data.get("description"), data.get("html"),
                    data.get("text"), data.get("h1"), data.get("h2_tags"),
                    data.get("screenshot"), data.get("status_code"),
                    data.get("depth"), datetime.now().isoformat()
                ))

                for link in data["links"]:
                    try:
                        conn.execute(
                            "INSERT OR IGNORE INTO links (from_url, to_url, anchor_text, is_internal) VALUES (?, ?, ?, ?)",
                            (url, link["url"], link.get("text", ""), link.get("internal", True))
                        )
                    except Exception:
                        pass
                conn.commit()

                page_count += 1

                if depth < max_depth:
                    for link in data["links"]:
                        if link["internal"] and link["url"] not in visited:
                            queue.append((link["url"], depth + 1))

                await asyncio.sleep(delay)

            except Exception as e:
                print(f"[ERROR] {url}: {e}")
                continue

        await browser.close()

    conn.close()
    print(f"\nDone! Crawled {page_count} pages → {db_path}")


def main():
    parser = ArgumentParser(description="Playwright Crawler cho JS/SPA websites")
    parser.add_argument("--url", required=True)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--db", default="crawl_playwright.sqlite")
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--max-pages", type=int, default=5000)
    parser.add_argument("--screenshots", action="store_true", help="Chụp screenshot mỗi trang")
    args = parser.parse_args()

    asyncio.run(crawl_playwright(
        start_url=args.url,
        max_depth=args.depth,
        db_path=args.db,
        delay=args.delay,
        max_pages=args.max_pages,
        take_screenshots=args.screenshots,
    ))


if __name__ == "__main__":
    main()
