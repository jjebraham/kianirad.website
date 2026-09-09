#!/usr/bin/env python3
"""Generate static /tr/ and /fa/ copies from the site's existing JS dictionaries.

No third-party Python packages are required. The parser intentionally supports the
small JavaScript-literal subset used by assets/site.js and PAGE_STRINGS.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANGS = ("en", "tr", "fa")
PAGES = (
    "index.html",
    "projects.html",
    "consultancy.html",
    "about.html",
    "contact.html",
    "privacy.html",
)
BASE_URL = "https://www.kianirad.website"


class JSParser:
    def __init__(self, text: str):
        self.s = text
        self.i = 0

    def ws(self):
        while self.i < len(self.s):
            if self.s[self.i].isspace():
                self.i += 1
                continue
            if self.s.startswith("//", self.i):
                j = self.s.find("\n", self.i)
                self.i = len(self.s) if j < 0 else j + 1
                continue
            if self.s.startswith("/*", self.i):
                j = self.s.find("*/", self.i + 2)
                self.i = len(self.s) if j < 0 else j + 2
                continue
            break

    def value(self):
        self.ws()
        if self.i >= len(self.s):
            raise ValueError("unexpected end of JS literal")
        c = self.s[self.i]
        if c == "{":
            return self.obj()
        if c == "[":
            return self.arr()
        if c in "\"'":
            return self.string()
        if c.isdigit() or c in "+-":
            return self.number()
        ident = self.ident()
        return {"true": True, "false": False, "null": None}.get(ident, ident)

    def ident(self):
        self.ws()
        m = re.match(r"[A-Za-z_$][\w$-]*", self.s[self.i:])
        if not m:
            raise ValueError(f"expected identifier near {self.s[self.i:self.i+30]!r}")
        self.i += len(m.group(0))
        return m.group(0)

    def string(self):
        quote = self.s[self.i]
        self.i += 1
        out = []
        while self.i < len(self.s):
            c = self.s[self.i]
            self.i += 1
            if c == quote:
                return "".join(out)
            if c != "\\":
                out.append(c)
                continue
            if self.i >= len(self.s):
                break
            e = self.s[self.i]
            self.i += 1
            mapping = {"n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f", "v": "\v"}
            if e == "u" and self.i + 4 <= len(self.s):
                code = self.s[self.i:self.i+4]
                if re.fullmatch(r"[0-9a-fA-F]{4}", code):
                    out.append(chr(int(code, 16)))
                    self.i += 4
                    continue
            if e == "x" and self.i + 2 <= len(self.s):
                code = self.s[self.i:self.i+2]
                if re.fullmatch(r"[0-9a-fA-F]{2}", code):
                    out.append(chr(int(code, 16)))
                    self.i += 2
                    continue
            out.append(mapping.get(e, e))
        raise ValueError("unterminated string")

    def number(self):
        self.ws()
        m = re.match(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", self.s[self.i:])
        if not m:
            raise ValueError("bad number")
        token = m.group(0)
        self.i += len(token)
        return float(token) if "." in token else int(token)

    def obj(self):
        out = {}
        self.i += 1
        while True:
            self.ws()
            if self.s[self.i] == "}":
                self.i += 1
                return out
            key = self.string() if self.s[self.i] in "\"'" else self.ident()
            self.ws()
            if self.s[self.i] != ":":
                raise ValueError("expected colon")
            self.i += 1
            out[key] = self.value()
            self.ws()
            if self.s[self.i] == ",":
                self.i += 1
                continue
            if self.s[self.i] == "}":
                self.i += 1
                return out
            raise ValueError("expected comma or object end")

    def arr(self):
        out = []
        self.i += 1
        while True:
            self.ws()
            if self.s[self.i] == "]":
                self.i += 1
                return out
            out.append(self.value())
            self.ws()
            if self.s[self.i] == ",":
                self.i += 1
                continue
            if self.s[self.i] == "]":
                self.i += 1
                return out
            raise ValueError("expected comma or array end")


def balanced_object(text: str, marker: str) -> str:
    pos = text.find(marker)
    if pos < 0:
        raise ValueError(f"marker not found: {marker}")
    start = text.find("{", pos)
    if start < 0:
        raise ValueError(f"object not found after: {marker}")
    depth = 0
    quote = None
    escaped = False
    i = start
    while i < len(text):
        c = text[i]
        if quote:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == quote:
                quote = None
        else:
            if c in "\"'":
                quote = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i+1]
        i += 1
    raise ValueError(f"unterminated object after: {marker}")


def parse_object(text: str, marker: str) -> dict:
    return JSParser(balanced_object(text, marker)).value()


def page_url(lang: str, name: str) -> str:
    if name == "index.html":
        return BASE_URL + ("/" if lang == "en" else f"/{lang}/")
    return BASE_URL + (f"/{name}" if lang == "en" else f"/{lang}/{name}")


def hreflang_block(name: str) -> str:
    return "\n".join([
        "<!-- i18n-hreflang:start -->",
        f'<link rel="alternate" hreflang="en" href="{page_url("en", name)}">',
        f'<link rel="alternate" hreflang="tr" href="{page_url("tr", name)}">',
        f'<link rel="alternate" hreflang="fa" href="{page_url("fa", name)}">',
        f'<link rel="alternate" hreflang="x-default" href="{page_url("en", name)}">',
        "<!-- i18n-hreflang:end -->",
    ])


def replace_hreflang(src: str, name: str) -> str:
    src = re.sub(r"\n?<!-- i18n-hreflang:start -->.*?<!-- i18n-hreflang:end -->\n?", "\n", src, flags=re.S)
    block = hreflang_block(name)
    canonical = re.search(r'<link rel="canonical"[^>]*>', src)
    if not canonical:
        raise ValueError(f"canonical missing in {name}")
    return src[:canonical.start()] + block + "\n" + src[canonical.start():]


def replace_canonical(src: str, url: str) -> str:
    return re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{url}">', src, count=1)


def ensure_privacy_link(src: str) -> str:
    """Keep Privacy crawlable/no-JS while site.js still owns the translation at runtime."""
    if 'class="privacy-link"' in src:
        return src
    replacement = ' · <a class="privacy-link" href="/privacy.html" data-i18n="navPrivacy">Privacy</a></footer>'
    return re.sub(r'</footer>', replacement, src, count=1)


def bake_text(src: str, key: str, value: str, html_mode: bool = False) -> str:
    attr = "data-i18n-html" if html_mode else "data-i18n"
    escaped = value if html_mode else html.escape(value, quote=False)
    pattern = re.compile(
        rf'(<(?P<tag>[A-Za-z0-9]+)\b[^>]*\b{attr}="{re.escape(key)}"[^>]*>)(.*?)(</(?P=tag)>)',
        re.S,
    )
    return pattern.sub(lambda m: m.group(1) + escaped + m.group(4), src)


def bake_attr(src: str, key: str, value: str):
    pattern = re.compile(rf'<(?P<tag>[A-Za-z0-9]+)\b(?P<attrs>[^>]*\bdata-i18n-attr="(?P<spec>[^"]*:{re.escape(key)})"[^>]*)>')
    def repl(m):
        tag = m.group(0)
        spec = m.group("spec")
        attr_name = spec.split(":", 1)[0]
        safe = html.escape(value, quote=True)
        if re.search(rf'\b{re.escape(attr_name)}="[^"]*"', tag):
            return re.sub(rf'\b{re.escape(attr_name)}="[^"]*"', f'{attr_name}="{safe}"', tag)
        return tag[:-1] + f' {attr_name}="{safe}">'
    return pattern.sub(repl, src)


def bake(src: str, strings: dict) -> str:
    for key, value in strings.items():
        if not isinstance(value, str):
            continue
        src = bake_text(src, key, value, html_mode=True)
        src = bake_text(src, key, value, html_mode=False)
        src = bake_attr(src, key, value)
    return src


def set_html_language(src: str, lang: str) -> str:
    direction = "rtl" if lang == "fa" else "ltr"
    return re.sub(
        r'<html\b[^>]*>',
        f'<html lang="{lang}" dir="{direction}" data-static-lang="{lang}">',
        src,
        count=1,
    )


def adjust_paths(src: str) -> str:
    src = src.replace('href="assets/', 'href="../assets/')
    src = src.replace('src="assets/', 'src="../assets/')
    return src


def build():
    site_js = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
    base = parse_object(site_js, "var BASE =")

    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            print(f"skip missing: {name}")
            continue
        source = ensure_privacy_link(path.read_text(encoding="utf-8"))
        page_strings = parse_object(source, "window.PAGE_STRINGS")

        # Keep reciprocal hreflang tags and a static Privacy link on the English source page too.
        english = replace_hreflang(source, name)
        english = replace_canonical(english, page_url("en", name))
        path.write_text(english, encoding="utf-8")

        for lang in ("tr", "fa"):
            strings = {}
            strings.update(base.get(lang, {}))
            strings.update(page_strings.get(lang, {}))
            out = bake(source, strings)
            out = replace_hreflang(out, name)
            out = replace_canonical(out, page_url(lang, name))
            out = set_html_language(out, lang)
            out = adjust_paths(out)
            dest = ROOT / lang / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(out, encoding="utf-8")
            print(f"wrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
