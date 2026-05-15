# Xử lý dữ liệu sau khi crawl

## Query dữ liệu từ SQLite

```python
import sqlite3
import json

conn = sqlite3.connect("crawl.sqlite")
conn.row_factory = sqlite3.Row  # access by column name

# 1. Xem tổng quan
cursor = conn.execute("""
    SELECT 
        COUNT(*) as total_pages,
        COUNT(DISTINCT domain) as domains,
        AVG(length(text)) as avg_text_len,
        MIN(crawled_at), MAX(crawled_at)
    FROM pages
""")
print(dict(cursor.fetchone()))

# 2. Lấy tất cả trang theo depth
pages = conn.execute(
    "SELECT url, title, depth FROM pages ORDER BY depth, url"
).fetchall()

# 3. Tìm kiếm trong nội dung (SQLite FTS5)
# Nếu muốn full-text search mạnh hơn, dùng PostgreSQL
results = conn.execute(
    "SELECT url, title FROM pages WHERE text LIKE ?", ("%từ_khóa%",)
).fetchall()

# 4. Lấy cấu trúc navigation
for page in conn.execute("SELECT url, nav_links FROM pages WHERE nav_links IS NOT NULL"):
    nav = json.loads(page["nav_links"])
    print(f"{page['url']}: {len(nav)} nav items")

# 5. Phân tích link graph
internal_links = conn.execute("""
    SELECT from_url, to_url, anchor_text 
    FROM links 
    WHERE is_internal = 1
    ORDER BY from_url
""").fetchall()

# 6. Trang có nhiều link nhất (hub pages)
hubs = conn.execute("""
    SELECT from_url, COUNT(*) as link_count
    FROM links WHERE is_internal = 1
    GROUP BY from_url
    ORDER BY link_count DESC
    LIMIT 20
""").fetchall()

# 7. Trang được link nhiều nhất (authority pages)
authorities = conn.execute("""
    SELECT to_url, COUNT(*) as inbound
    FROM links WHERE is_internal = 1
    GROUP BY to_url
    ORDER BY inbound DESC
    LIMIT 20
""").fetchall()
```

---

## Export dữ liệu

```python
import csv
import json

# Export CSV
with open("pages.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["url", "title", "description", "depth", "text_length"])
    for row in conn.execute("SELECT url, title, description, depth, length(text) FROM pages"):
        writer.writerow(row)

# Export JSON
pages = []
for row in conn.execute("SELECT url, title, description, text, depth FROM pages"):
    pages.append({
        "url": row[0],
        "title": row[1],
        "description": row[2],
        "text": row[3][:500],  # preview
        "depth": row[4]
    })

with open("pages.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)
```

---

## Visualize link graph

```python
# pip install networkx matplotlib
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
for row in conn.execute("SELECT from_url, to_url FROM links WHERE is_internal = 1"):
    G.add_edge(row[0], row[1])

print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
print(f"PageRank top 10:")
pr = nx.pagerank(G)
for url, score in sorted(pr.items(), key=lambda x: -x[1])[:10]:
    print(f"  {score:.4f} {url}")

# Vẽ graph (chỉ dùng cho site nhỏ)
plt.figure(figsize=(20, 20))
nx.draw(G, with_labels=False, node_size=50, alpha=0.7)
plt.savefig("link_graph.png", dpi=150)
```

---

## Tạo sitemap từ dữ liệu crawl

```python
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

for row in conn.execute("SELECT url, crawled_at FROM pages ORDER BY depth"):
    url_el = SubElement(urlset, "url")
    SubElement(url_el, "loc").text = row[0]
    SubElement(url_el, "lastmod").text = row[1][:10]

with open("sitemap.xml", "wb") as f:
    f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write(tostring(urlset, encoding="unicode").encode())
```

---

## Index vào Elasticsearch (search nhanh)

```python
# pip install elasticsearch
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://localhost:9200")

def generate_docs():
    for row in conn.execute("SELECT url, title, description, text, crawled_at FROM pages"):
        yield {
            "_index": "web_pages",
            "_id": row[0],
            "_source": {
                "url": row[0],
                "title": row[1],
                "description": row[2],
                "content": row[3],
                "crawled_at": row[4],
            }
        }

helpers.bulk(es, generate_docs())

# Search
results = es.search(index="web_pages", body={
    "query": {
        "multi_match": {
            "query": "từ khóa tìm kiếm",
            "fields": ["title^3", "description^2", "content"]
        }
    },
    "highlight": {
        "fields": {"content": {}}
    }
})
```
