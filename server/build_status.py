#!/usr/bin/env python3
"""Generate status.html from root status.json.

The browser never polls. A cron job or monitoring process writes status.json and then
runs this script. Only systems present in status.json are rendered publicly.
"""
from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "status.json"
OUT = ROOT / "status.html"


def esc(value):
    return html.escape(str(value or ""), quote=True)


def load_data():
    if not DATA.exists():
        return None, "Status data has not been published yet."
    try:
        payload = json.loads(DATA.read_text(encoding="utf-8"))
    except Exception:
        return None, "Status data is temporarily unavailable."
    if not isinstance(payload, dict) or not isinstance(payload.get("systems", []), list):
        return None, "Status data is temporarily unavailable."
    return payload, None


def build():
    payload, error = load_data()
    systems = [] if error else payload.get("systems", [])
    checked_at = "Not available" if error else payload.get("checked_at") or "Not available"

    rows = []
    for item in systems:
        if not isinstance(item, dict) or not item.get("name"):
            continue
        state = str(item.get("state", "unknown")).lower()
        if state not in {"up", "down", "degraded", "unknown"}:
            state = "unknown"
        label = {"up":"Operational","down":"Down","degraded":"Degraded","unknown":"Unknown"}[state]
        url = item.get("url")
        name = esc(item["name"])
        name_html = f'<a href="{esc(url)}" rel="noopener">{name}</a>' if url else name
        when = esc(item.get("checked_at") or checked_at)
        rows.append(
            f'<div class="item"><div><h3>{name_html}</h3><p>Last checked: {when}</p></div>'
            f'<div class="stack">{esc(label)}</div></div>'
        )

    if error:
        body = f'<p class="lede">{esc(error)} The page remains readable even when the monitoring data is missing.</p>'
    elif not rows:
        body = '<p class="lede">No production systems have been selected for public status reporting yet.</p>'
    else:
        body = '<div class="build">' + "".join(rows) + '</div>'

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    document = f'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Status | Hadi Kianirad</title>
<meta name="description" content="Public operating status for selected systems maintained by Hadi Kianirad.">
<link rel="canonical" href="https://www.kianirad.website/status.html">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23137F72'/%3E%3Ctext x='32' y='44' text-anchor='middle' font-family='Arial,sans-serif' font-size='40' font-weight='800' fill='white'%3EK%3C/text%3E%3C/svg%3E">
<link rel="alternate icon" href="/favicon.ico">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="shell">
  <aside class="rail"><div><a class="mark" href="index.html">Hadi Kianirad<span>Systems that keep running</span></a><p class="role">Backend and automation engineer. Istanbul.</p></div><nav class="railnav"><a href="index.html">Home</a><a href="projects.html">Projects</a><a href="contact.html">Contact</a></nav></aside>
  <main id="main">
    <section class="pagehead"><h1 class="pagetitle">System status</h1><p class="lede">A static snapshot generated from monitoring data. This page does not poll production systems from your browser.</p></section>
    <section><h2>Selected public systems</h2>{body}</section>
    <section><h2>Snapshot details</h2><div class="prose"><p>Monitoring data timestamp: {esc(checked_at)}</p><p>Page generated: {esc(generated)}</p></div></section>
  </main>
</div>
<footer><span>Kiani Limited Liability Company · Istanbul · English, Türkçe, فارسی</span><span dir="ltr"> · ©2026</span> · <a href="/privacy.html">Privacy</a></footer>
</body>
</html>'''
    OUT.write_text(document, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
