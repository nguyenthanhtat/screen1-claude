#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
generate_site.py — Doc SQLite tu crawler, tao Next.js website hoan chinh chay duoc local.

Usage:
    python generate_site.py --db crawl.sqlite --out ./my-site
    python generate_site.py --db crawl.sqlite --out ./my-site --site-name "My Website"

Output: Next.js project, chỉ cần:
    cd my-site && npm install && npm run dev
"""

import sqlite3
import json
import re
import shutil
import sys
import urllib.request
from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import urlparse, urljoin
from datetime import datetime


# ─── Helpers ─────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert URL path or title to a safe slug."""
    text = text.lower().strip("/")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = text.strip("-")
    return text or "page"


def safe_json(val) -> list | dict:
    if not val:
        return []
    try:
        return json.loads(val)
    except Exception:
        return []


def strip_html(html: str) -> str:
    """Very simple HTML stripper for display."""
    return re.sub(r"<[^>]+>", " ", html or "").strip()


def download_image(url: str, dest: Path) -> str | None:
    """Download image and return local path relative to /public. Returns None on fail."""
    try:
        parsed = urlparse(url)
        filename = Path(parsed.path).name
        if not filename or "." not in filename:
            return None
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext not in ("jpg", "jpeg", "png", "gif", "webp", "svg", "avif"):
            return None
        dest.mkdir(parents=True, exist_ok=True)
        local_path = dest / filename
        if not local_path.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                local_path.write_bytes(r.read())
        return f"/images/{filename}"
    except Exception:
        return None


# ─── Database ─────────────────────────────────────────────────────────────────

def load_pages(db_path: str) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT url, path, title, description, text, h1, h2_tags, h3_tags,
               og_tags, nav_links, html, depth
        FROM pages
        WHERE status_code = 200
        ORDER BY depth ASC, id ASC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def load_assets(db_path: str) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("""
            SELECT page_url, asset_url, asset_type, alt_text FROM assets
            WHERE asset_type = 'image'
        """).fetchall()
    except Exception:
        rows = []
    conn.close()
    return [dict(r) for r in rows]


# ─── Page Structuring ─────────────────────────────────────────────────────────

def build_page_data(pages: list[dict], base_domain: str) -> list[dict]:
    """Convert raw DB rows into structured page objects."""
    result = []
    seen_slugs = set()

    for p in pages:
        url_path = (p.get("path") or "").strip("/")
        if not url_path:
            slug = "home"
            is_home = True
        else:
            slug = slugify(url_path)
            is_home = False

        # Ensure unique slug
        original = slug
        counter = 2
        while slug in seen_slugs:
            slug = f"{original}-{counter}"
            counter += 1
        seen_slugs.add(slug)

        h2s = safe_json(p.get("h2_tags"))
        og = safe_json(p.get("og_tags"))
        og_image = og.get("og:image", "") if isinstance(og, dict) else ""

        # Extract first meaningful paragraph from text
        text = p.get("text") or ""
        paragraphs = [ln.strip() for ln in text.split("\n") if len(ln.strip()) > 80]
        excerpt = paragraphs[0][:280] if paragraphs else (p.get("description") or "")[:280]

        result.append({
            "slug": slug,
            "is_home": is_home,
            "url": p.get("url", ""),
            "path": url_path,
            "title": p.get("title") or p.get("h1") or slug.replace("-", " ").title(),
            "description": p.get("description") or excerpt[:160],
            "excerpt": excerpt,
            "h1": p.get("h1") or p.get("title") or "",
            "h2s": h2s if isinstance(h2s, list) else [],
            "og_image": og_image,
            "depth": p.get("depth", 0),
        })

    return result


# ─── File Writers ─────────────────────────────────────────────────────────────

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ {path}")


def generate_package_json(out: Path, site_name: str):
    content = json.dumps({
        "name": slugify(site_name) or "cloned-site",
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start"
        },
        "dependencies": {
            "next": "^15.0.0",
            "react": "^19.0.0",
            "react-dom": "^19.0.0",
            "lucide-react": "^0.469.0"
        },
        "devDependencies": {
            "@types/node": "^22.0.0",
            "@types/react": "^19.0.0",
            "@types/react-dom": "^19.0.0",
            "typescript": "^5.0.0",
            "tailwindcss": "^4.0.0",
            "@tailwindcss/postcss": "^4.0.0"
        }
    }, indent=2)
    write_file(out / "package.json", content)


def generate_next_config(out: Path, base_domain: str):
    content = f'''import type {{ NextConfig }} from "next";

const nextConfig: NextConfig = {{
  images: {{
    remotePatterns: [
      {{ protocol: "https", hostname: "{base_domain}" }},
    ],
    unoptimized: true,
  }},
}};

export default nextConfig;
'''
    write_file(out / "next.config.ts", content)


def generate_tsconfig(out: Path):
    content = json.dumps({
        "compilerOptions": {
            "target": "ES2017",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
            "paths": {"@/*": ["./src/*"]}
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }, indent=2)
    write_file(out / "tsconfig.json", content)


def generate_postcss(out: Path):
    content = '''export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
'''
    write_file(out / "postcss.config.mjs", content)


def generate_globals_css(out: Path, primary_color: str = "#2563eb"):
    content = f'''@import "tailwindcss";

:root {{
  --primary: {primary_color};
  --primary-dark: color-mix(in srgb, {primary_color} 80%, black);
  --dark: #0f172a;
  --gray: #64748b;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; color: var(--dark); background: #fff; }}

@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.fade-up {{ animation: fadeUp 0.5s ease forwards; }}

/* Prose styles for content */
.prose h2 {{ font-size: 1.5rem; font-weight: 700; margin: 1.5rem 0 0.75rem; color: var(--dark); }}
.prose h3 {{ font-size: 1.2rem; font-weight: 600; margin: 1.25rem 0 0.5rem; }}
.prose p {{ line-height: 1.75; margin-bottom: 1rem; color: #374151; }}
.prose ul {{ list-style: disc; padding-left: 1.5rem; margin-bottom: 1rem; }}
.prose li {{ margin-bottom: 0.25rem; line-height: 1.6; color: #374151; }}
'''
    write_file(out / "src" / "app" / "globals.css", content)


def generate_data_ts(out: Path, pages: list[dict], site_name: str, base_url: str):
    """Generate src/lib/data.ts with all page data."""
    pages_json = json.dumps(pages, ensure_ascii=False, indent=2)
    content = f'''// Auto-generated by generate_site.py
// Source: {base_url}
// Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

export interface Page {{
  slug: string;
  is_home: boolean;
  url: string;
  path: string;
  title: string;
  description: string;
  excerpt: string;
  h1: string;
  h2s: string[];
  og_image: string;
  depth: number;
}}

export const siteName = {json.dumps(site_name)};
export const baseUrl = {json.dumps(base_url)};

export const pages: Page[] = {pages_json};

export const homePage = pages.find(p => p.is_home) ?? pages[0];
export const navPages = pages.filter(p => !p.is_home && p.depth <= 1).slice(0, 8);
'''
    write_file(out / "src" / "lib" / "data.ts", content)


def generate_layout(out: Path, site_name: str, primary: str = "#2563eb"):
    content = f'''"use client";
import {{ useState, useEffect }} from "react";
import Link from "next/link";
import {{ Menu, X }} from "lucide-react";
import {{ navPages, siteName }} from "@/lib/data";
import "./globals.css";

export default function RootLayout({{ children }}: {{ children: React.ReactNode }}) {{
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {{
    const fn = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", fn);
    return () => window.removeEventListener("scroll", fn);
  }}, []);

  return (
    <html lang="vi">
      <body>
        {{/* ── Header ── */}}
        <header className={{`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${{
          scrolled ? "bg-white shadow-md" : "bg-white/95 backdrop-blur"
        }}`}}>
          <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <Link href="/" className="font-black text-xl tracking-tight" style={{{{ color: "{primary}" }}}}>
              {{siteName}}
            </Link>

            {{/* Desktop nav */}}
            <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-700">
              <Link href="/" className="hover:text-blue-600 transition-colors">Trang chủ</Link>
              {{navPages.map(p => (
                <Link key={{p.slug}} href={{`/${{p.slug}}`}}
                  className="hover:text-blue-600 transition-colors line-clamp-1 max-w-[120px]">
                  {{p.title}}
                </Link>
              ))}}
            </div>

            {{/* Mobile toggle */}}
            <button className="md:hidden p-2 text-slate-700" onClick={{() => setOpen(!open)}}>
              {{open ? <X size={{22}} /> : <Menu size={{22}} />}}
            </button>
          </nav>

          {{/* Mobile menu */}}
          {{open && (
            <div className="md:hidden bg-white border-t px-4 pb-4 shadow-lg">
              <Link href="/" className="block py-3 border-b text-sm font-medium"
                onClick={{() => setOpen(false)}}>Trang chủ</Link>
              {{navPages.map(p => (
                <Link key={{p.slug}} href={{`/${{p.slug}}`}}
                  className="block py-3 border-b text-sm text-slate-700"
                  onClick={{() => setOpen(false)}}>
                  {{p.title}}
                </Link>
              ))}}
            </div>
          )}}
        </header>

        <main className="pt-16">{{children}}</main>

        {{/* ── Footer ── */}}
        <footer className="bg-slate-900 text-slate-300 mt-20">
          <div className="max-w-7xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <p className="font-black text-xl text-white mb-2">{{siteName}}</p>
              <p className="text-sm text-slate-400">Website được tạo tự động.</p>
            </div>
            <div>
              <h3 className="font-bold text-white text-sm uppercase tracking-wider mb-4">Trang</h3>
              <ul className="space-y-2">
                {{navPages.slice(0, 6).map(p => (
                  <li key={{p.slug}}>
                    <Link href={{`/${{p.slug}}`}} className="text-sm hover:text-white transition-colors">
                      {{p.title}}
                    </Link>
                  </li>
                ))}}
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white text-sm uppercase tracking-wider mb-4">Thông tin</h3>
              <p className="text-sm text-slate-400">© {{new Date().getFullYear()}} {{siteName}}</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}}
'''
    write_file(out / "src" / "app" / "layout.tsx", content)


def generate_homepage(out: Path, home: dict, all_pages: list[dict], primary: str):
    non_home = [p for p in all_pages if not p["is_home"]][:12]
    cards_jsx = ""
    for p in non_home:
        img_part = ""
        if p.get("og_image"):
            img_part = f'''
              <div className="h-40 bg-slate-100 overflow-hidden">
                <img src="{{}}" alt={{"{p['title']}"}} className="w-full h-full object-cover" />
              </div>'''

        cards_jsx += f'''
          <Link href="/{p['slug']}"
            className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col">
            {img_part}
            <div className="p-5 flex-1 flex flex-col">
              <h3 className="font-bold text-slate-800 mb-2 line-clamp-2 text-base">{p['title']}</h3>
              <p className="text-sm text-slate-500 flex-1 line-clamp-3">{p['excerpt'][:200]}</p>
              <span className="mt-4 text-sm font-semibold" style={{{{ color: "{primary}" }}}}>
                Xem thêm →
              </span>
            </div>
          </Link>'''

    content = f'''import Link from "next/link";
import {{ pages, homePage, siteName }} from "@/lib/data";

export const metadata = {{
  title: `${{homePage?.title}} | ${{siteName}}`,
  description: homePage?.description,
}};

export default function HomePage() {{
  const nonHome = pages.filter(p => !p.is_home).slice(0, 12);

  return (
    <div>
      {{/* Hero */}}
      <section className="bg-gradient-to-br from-slate-900 to-slate-700 text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black leading-tight mb-4 fade-up">
            {{homePage?.h1 || homePage?.title || siteName}}
          </h1>
          <p className="text-lg text-slate-300 max-w-2xl mx-auto mb-8">
            {{homePage?.description}}
          </p>
          {{nonHome[0] && (
            <Link href={{`/${{nonHome[0].slug}}`}}
              className="inline-block px-8 py-3.5 rounded-full font-bold text-sm transition-colors"
              style={{{{ backgroundColor: "{primary}", color: "#fff" }}}}>
              Khám phá ngay
            </Link>
          )}}
        </div>
      </section>

      {{/* Page grid */}}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-2xl font-black text-slate-800 mb-8 text-center">Nội dung</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {{nonHome.map(p => (
            <Link key={{p.slug}} href={{`/${{p.slug}}`}}
              className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col">
              <div className="p-5 flex-1 flex flex-col">
                <h3 className="font-bold text-slate-800 mb-2 line-clamp-2 text-base">{{p.title}}</h3>
                <p className="text-sm text-slate-500 flex-1 line-clamp-3">{{p.excerpt}}</p>
                <span className="mt-4 text-sm font-semibold" style={{{{ color: "{primary}" }}}}>
                  Xem thêm →
                </span>
              </div>
            </Link>
          ))}}
        </div>
      </section>
    </div>
  );
}}
'''
    write_file(out / "src" / "app" / "page.tsx", content)


def generate_content_pages(out: Path, pages: list[dict], primary: str):
    """Generate [slug]/page.tsx as SSG."""
    # Static params list
    non_home = [p for p in pages if not p["is_home"]]

    params_list = json.dumps([{"slug": p["slug"]} for p in non_home], indent=4)
    pages_json = json.dumps(non_home, ensure_ascii=False, indent=2)

    content = f'''import {{ notFound }} from "next/navigation";
import Link from "next/link";
import {{ pages, siteName }} from "@/lib/data";

export async function generateStaticParams() {{
  return pages.filter(p => !p.is_home).map(p => ({{ slug: p.slug }}));
}}

export async function generateMetadata({{ params }}: {{ params: Promise<{{ slug: string }}> }}) {{
  const {{ slug }} = await params;
  const page = pages.find(p => p.slug === slug);
  if (!page) return {{}};
  return {{
    title: `${{page.title}} | ${{siteName}}`,
    description: page.description,
  }};
}}

export default async function ContentPage({{ params }}: {{ params: Promise<{{ slug: string }}> }}) {{
  const {{ slug }} = await params;
  const page = pages.find(p => p.slug === slug);
  if (!page) notFound();

  const related = pages.filter(p => !p.is_home && p.slug !== slug).slice(0, 4);

  return (
    <div className="min-h-screen bg-slate-50">
      {{/* Breadcrumb */}}
      <div className="bg-white border-b px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center gap-2 text-sm text-slate-500">
          <Link href="/" className="hover:text-blue-600 transition-colors">Trang chủ</Link>
          <span>›</span>
          <span className="text-slate-800 font-medium">{{page.title}}</span>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">

          {{/* Main */}}
          <article className="lg:col-span-2">
            {{/* Hero card */}}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 sm:p-10 mb-8">
              <h1 className="text-2xl sm:text-3xl font-black text-slate-900 mb-4 leading-tight">
                {{page.h1 || page.title}}
              </h1>
              {{page.description && (
                <p className="text-slate-500 text-base mb-6 border-l-4 pl-4"
                   style={{{{ borderColor: "{primary}" }}}}>
                  {{page.description}}
                </p>
              )}}

              {{/* H2 headings as content outline */}}
              {{page.h2s.length > 0 && (
                <div className="prose">
                  {{page.h2s.map((h2, i) => (
                    <h2 key={{i}}>{{h2}}</h2>
                  ))}}
                </div>
              )}}

              {{/* Excerpt */}}
              {{page.excerpt && (
                <div className="mt-6 prose">
                  <p>{{page.excerpt}}</p>
                </div>
              )}}

              {{/* Source link */}}
              <div className="mt-8 pt-6 border-t border-slate-100">
                <a href={{page.url}} target="_blank" rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-sm font-medium transition-colors"
                  style={{{{ color: "{primary}" }}}}>
                  Xem trang gốc →
                </a>
              </div>
            </div>
          </article>

          {{/* Sidebar */}}
          <aside className="lg:col-span-1">
            <div className="sticky top-20 space-y-6">
              {{/* Related pages */}}
              {{related.length > 0 && (
                <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
                  <h3 className="font-bold text-slate-800 mb-4 text-sm uppercase tracking-wide">
                    Trang liên quan
                  </h3>
                  <ul className="space-y-3">
                    {{related.map(r => (
                      <li key={{r.slug}}>
                        <Link href={{`/${{r.slug}}`}}
                          className="text-sm hover:text-blue-600 transition-colors font-medium block leading-snug">
                          {{r.title}}
                        </Link>
                        <p className="text-xs text-slate-400 mt-0.5 line-clamp-2">{{r.excerpt}}</p>
                      </li>
                    ))}}
                  </ul>
                </div>
              )}}

              {{/* Back home */}}
              <Link href="/"
                className="flex items-center justify-center gap-2 w-full py-3 rounded-xl text-white text-sm font-semibold transition-colors"
                style={{{{ backgroundColor: "{primary}" }}}}>
                ← Về trang chủ
              </Link>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}}
'''
    write_file(out / "src" / "app" / "[slug]" / "page.tsx", content)


def generate_not_found(out: Path):
    content = '''export default function NotFound() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-6xl font-black text-slate-200 mb-4">404</h1>
      <p className="text-xl font-bold text-slate-700 mb-2">Không tìm thấy trang</p>
      <p className="text-slate-500 mb-8">Trang bạn tìm kiếm không tồn tại.</p>
      <a href="/" className="bg-blue-600 text-white px-6 py-3 rounded-full font-semibold text-sm hover:bg-blue-700 transition-colors">
        Về trang chủ
      </a>
    </div>
  );
}
'''
    write_file(out / "src" / "app" / "not-found.tsx", content)


def generate_readme(out: Path, site_name: str, base_url: str, page_count: int):
    content = f'''# {site_name}

Website được tạo tự động từ {base_url}
Số trang: {page_count}
Tạo lúc: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Chạy local

```bash
npm install
npm run dev
```

Mở http://localhost:3000

## Build production

```bash
npm run build
npm start
```

## Stack
- Next.js 15 (App Router, SSG)
- Tailwind CSS v4
- TypeScript
'''
    write_file(out / "README.md", content)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = ArgumentParser(description="Tạo Next.js website từ SQLite crawl data")
    parser.add_argument("--db", required=True, help="File SQLite (output của crawler)")
    parser.add_argument("--out", required=True, help="Thư mục output")
    parser.add_argument("--site-name", default="", help="Tên website")
    parser.add_argument("--primary-color", default="#2563eb", help="Màu chủ đạo (hex)")
    parser.add_argument("--download-images", action="store_true", help="Tải ảnh về local")
    args = parser.parse_args()

    db_path = args.db
    out = Path(args.out)
    primary = args.primary_color

    print(f"\n🔍 Đọc database: {db_path}")
    raw_pages = load_pages(db_path)
    if not raw_pages:
        print("❌ Không có trang nào trong database (status_code=200)")
        sys.exit(1)

    base_url = raw_pages[0]["url"]
    base_domain = urlparse(base_url).netloc
    site_name = args.site_name or base_domain

    print(f"📦 Domain: {base_domain}")
    print(f"📄 Số trang: {len(raw_pages)}")

    pages = build_page_data(raw_pages, base_domain)
    home = next((p for p in pages if p["is_home"]), pages[0])

    # Download images nếu cần
    if args.download_images:
        print("\n🖼 Tải ảnh...")
        assets = load_assets(db_path)
        img_dir = out / "public" / "images"
        downloaded = 0
        for asset in assets:
            local = download_image(asset["asset_url"], img_dir)
            if local:
                downloaded += 1
        print(f"  ✓ {downloaded} ảnh")

    print(f"\n🏗 Tạo Next.js project: {out}")

    # Generate all files
    generate_package_json(out, site_name)
    generate_next_config(out, base_domain)
    generate_tsconfig(out)
    generate_postcss(out)
    generate_globals_css(out, primary)
    generate_data_ts(out, pages, site_name, base_url)
    generate_layout(out, site_name, primary)
    generate_homepage(out, home, pages, primary)
    generate_content_pages(out, pages, primary)
    generate_not_found(out)
    generate_readme(out, site_name, base_url, len(pages))

    # public folder placeholder
    (out / "public").mkdir(exist_ok=True)

    print(f"""
✅ Xong! Website đã được tạo tại: {out}

Chạy local:
  cd {out}
  npm install
  npm run dev

→ http://localhost:3000
""")


if __name__ == "__main__":
    main()
