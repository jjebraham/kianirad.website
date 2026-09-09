#!/usr/bin/env python3
"""Regenerate sitemap.xml from the site's deployable public HTML files."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
BASE = "https://www.kianirad.website"
CORE = ["index.html", "projects.html", "consultancy.html", "about.html", "contact.html"]
EXTRA = ["privacy.html", "status.html"]


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return BASE + "/"
    if rel in {"tr/index.html", "fa/index.html"}:
        return BASE + "/" + rel.split("/", 1)[0] + "/"
    return BASE + "/" + rel


def main():
    candidates = [ROOT / name for name in CORE + EXTRA]
    for lang in ("tr", "fa"):
        candidates.extend(ROOT / lang / name for name in CORE)
    candidates.append(ROOT / "tr" / "klinikler-icin-telegram-botu.html")

    paths = []
    seen = set()
    for p in candidates:
        if p.exists() and p.is_file():
            url = url_for(p)
            if url not in seen:
                seen.add(url)
                paths.append((url, p))

    rows = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, p in paths:
        stamp = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).date().isoformat()
        rows.append("  <url>")
        rows.append(f"    <loc>{escape(url)}</loc>")
        rows.append(f"    <lastmod>{stamp}</lastmod>")
        rows.append("  </url>")
    rows.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"wrote sitemap.xml with {len(paths)} URLs")


if __name__ == "__main__":
    main()
