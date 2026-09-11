#!/usr/bin/env python3
"""Inject the shared UI v2 and Kimi progressive enhancement assets into public HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def asset_prefix(path: Path) -> str:
    return "../assets" if path.parent.name in {"tr", "fa"} else "assets"


def inject(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n?<!-- ui-v2-css:start -->.*?<!-- ui-v2-css:end -->\n?", "\n", text, flags=re.S)
    text = re.sub(r"\n?<!-- ui-v2-js:start -->.*?<!-- ui-v2-js:end -->\n?", "\n", text, flags=re.S)

    prefix = asset_prefix(path)
    css = (
        '<!-- ui-v2-css:start -->\n'
        f'<link rel="stylesheet" href="{prefix}/ui-v2.css">\n'
        f'<link rel="stylesheet" href="{prefix}/kimi-effects.css">\n'
        '<!-- ui-v2-css:end -->'
    )
    js = (
        '<!-- ui-v2-js:start -->\n'
        f'<script src="{prefix}/ui-v2.js"></script>\n'
        f'<script src="{prefix}/kimi-effects.js"></script>\n'
        '<!-- ui-v2-js:end -->'
    )

    site_css_pattern = re.compile(r'<link rel="stylesheet" href="(?:\.\./)?assets/site\.css">')
    match = site_css_pattern.search(text)
    if match:
        text = text[:match.end()] + "\n" + css + text[match.end():]
    else:
        text = text.replace("</head>", css + "\n</head>", 1)

    text = text.replace("</body>", js + "\n</body>", 1)
    path.write_text(text, encoding="utf-8")
    print(f"UI v2: {path.relative_to(ROOT)}")


def main() -> None:
    paths = sorted(ROOT.glob("*.html"))
    paths += sorted((ROOT / "tr").glob("*.html")) if (ROOT / "tr").exists() else []
    paths += sorted((ROOT / "fa").glob("*.html")) if (ROOT / "fa").exists() else []
    for path in paths:
        inject(path)


if __name__ == "__main__":
    main()
