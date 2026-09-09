#!/usr/bin/env python3
"""Post-process generated language pages for localized head metadata and FAQ schema."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SEO = {
    "tr": {
        "index.html": (
            "Hadi Kianirad — Backend, Telegram botları ve otomasyon, İstanbul",
            "İstanbul merkezli Python backend, Telegram botu ve yapay zekâ otomasyonu. Üretimde çalışan 14+ sistem; Türkçe, İngilizce ve Farsça.",
            "Hadi Kianirad — Backend, botlar ve otomasyon",
            "İşletmeler için Python backend, Telegram botları ve yapay zekâ otomasyonu. Çalışmaya devam eden sistemler.",
        ),
        "projects.html": (
            "Projeler | Hadi Kianirad",
            "Hadi Kianirad'ın canlı sistemleri: gerçek zamanlı veri platformları, Telegram botları, exchange operasyonları ve doğrulama araçları.",
            "Projeler | Hadi Kianirad",
            "Canlı sistemler: gerçek zamanlı veri, Telegram botları, exchange operasyonları, doğrulama ve üretim mesajlaşması.",
        ),
        "consultancy.html": (
            "Otomasyon Danışmanlığı | Hadi Kianirad",
            "Tekrarlayan işleri azaltmak için Python, Telegram ve yapay zekâ otomasyonu danışmanlığı. Kapsam ve sabit fiyat iş başlamadan önce yazılı olarak belirlenir.",
            "Otomasyon Danışmanlığı | Hadi Kianirad",
            "Ekibinizin zamanını alan tekrar eden işi bulun, doğru otomasyonu kurun ve sonucu haftalık çalışan sürümlerle görün.",
        ),
        "about.html": (
            "Hakkımda | Hadi Kianirad",
            "İstanbul'da çalışan backend ve otomasyon mühendisi Hadi Kianirad: Python, sistem yönetimi, Telegram botları ve üretim sistemleri.",
            "Hakkımda | Hadi Kianirad",
            "Hadi Kianirad'ın backend, otomasyon, Python ve üretim sistemleri geçmişi.",
        ),
        "contact.html": (
            "İletişim | Hadi Kianirad",
            "Backend, Telegram botu veya yapay zekâ otomasyonu projenizi Hadi Kianirad ile görüşün. Türkçe, İngilizce veya Farsça iletişim kurun.",
            "İletişim | Hadi Kianirad",
            "İşletmenizin zamanını alan işi anlatın; Türkçe, İngilizce veya Farsça iletişim kurun.",
        ),
        "privacy.html": (
            "Gizlilik ve KVKK | Hadi Kianirad",
            "kianirad.website iletişim formunda hangi bilgilerin işlendiği, nereye gönderildiği ve KVKK kapsamındaki haklarınız.",
            "Gizlilik ve KVKK | Hadi Kianirad",
            "kianirad.website iletişim taleplerini ve kişisel verileri nasıl işler.",
        ),
    },
    "fa": {
        "index.html": (
            "هادی کیانی‌راد — بک‌اند، ربات تلگرام و اتوماسیون در استانبول",
            "بک‌اند پایتون، ربات تلگرام و اتوماسیون هوش مصنوعی برای کسب‌وکارها؛ بیش از ۱۴ سیستم در حال اجرا، به فارسی، ترکی و انگلیسی.",
            "هادی کیانی‌راد — بک‌اند، ربات و اتوماسیون",
            "بک‌اند پایتون، ربات تلگرام و اتوماسیون هوش مصنوعی برای کسب‌وکارها؛ سیستم‌هایی که از کار نمی‌افتند.",
        ),
        "projects.html": (
            "پروژه‌ها | هادی کیانی‌راد",
            "سیستم‌های زنده ساخته‌شده توسط هادی کیانی‌راد: داده بلادرنگ، ربات تلگرام، عملیات صرافی و ابزارهای اعتبارسنجی.",
            "پروژه‌ها | هادی کیانی‌راد",
            "سیستم‌های واقعی در حال اجرا: داده بلادرنگ، ربات تلگرام، عملیات صرافی و ابزارهای تولیدی.",
        ),
        "consultancy.html": (
            "مشاوره اتوماسیون | هادی کیانی‌راد",
            "مشاوره برای حذف کارهای تکراری با پایتون، ربات تلگرام و اتوماسیون هوش مصنوعی؛ محدوده و قیمت ثابت پیش از شروع مکتوب می‌شود.",
            "مشاوره اتوماسیون | هادی کیانی‌راد",
            "کار تکراری‌ای را که وقت تیم شما را می‌گیرد پیدا کنید، اتوماسیون مناسب را بسازید و هر هفته نسخه‌ای قابل استفاده ببینید.",
        ),
        "about.html": (
            "درباره من | هادی کیانی‌راد",
            "هادی کیانی‌راد، مهندس بک‌اند و اتوماسیون در استانبول؛ با سابقه پایتون، مدیریت سیستم، ربات تلگرام و سامانه‌های تولیدی.",
            "درباره من | هادی کیانی‌راد",
            "سابقه هادی کیانی‌راد در بک‌اند، اتوماسیون، پایتون و سیستم‌های تولیدی.",
        ),
        "contact.html": (
            "تماس | هادی کیانی‌راد",
            "برای پروژه بک‌اند، ربات تلگرام یا اتوماسیون هوش مصنوعی با هادی کیانی‌راد تماس بگیرید؛ به فارسی، ترکی یا انگلیسی.",
            "تماس | هادی کیانی‌راد",
            "کاری را که وقت کسب‌وکار شما را می‌گیرد توضیح دهید؛ به فارسی، ترکی یا انگلیسی.",
        ),
        "privacy.html": (
            "حریم خصوصی | هادی کیانی‌راد",
            "توضیح ساده درباره اطلاعات فرم تماس kianirad.website، نحوه استفاده از آن و حقوق مرتبط با داده‌های شخصی.",
            "حریم خصوصی | هادی کیانی‌راد",
            "kianirad.website چگونه درخواست‌های تماس و اطلاعات شخصی را پردازش می‌کند.",
        ),
    },
}

LOCALE = {"tr": "tr_TR", "fa": "fa_IR"}


def replace_tag(text: str, pattern: str, replacement: str) -> str:
    if not re.search(pattern, text, flags=re.I | re.S):
        raise ValueError(f"head tag not found: {pattern}")
    return re.sub(pattern, replacement, text, count=1, flags=re.I | re.S)


def localize_head(path: Path, lang: str, data: tuple[str, str, str, str]) -> None:
    title, desc, social_title, social_desc = data
    text = path.read_text(encoding="utf-8")
    canonical = re.search(r'<link rel="canonical" href="([^"]+)">', text)
    canonical_url = canonical.group(1) if canonical else ""

    text = replace_tag(text, r"<title>.*?</title>", f"<title>{html.escape(title)}</title>")
    text = replace_tag(text, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc, quote=True)}">')
    text = replace_tag(text, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(social_title, quote=True)}">')
    text = replace_tag(text, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(social_desc, quote=True)}">')
    text = replace_tag(text, r'<meta property="og:locale" content="[^"]*">', f'<meta property="og:locale" content="{LOCALE[lang]}">')
    if canonical_url:
        text = replace_tag(text, r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{html.escape(canonical_url, quote=True)}">')
    text = replace_tag(text, r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{html.escape(social_title, quote=True)}">')
    text = replace_tag(text, r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{html.escape(social_desc, quote=True)}">')
    path.write_text(text, encoding="utf-8")


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(fragment).strip()


def faq_schema(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n?<!-- faq-schema:start -->.*?<!-- faq-schema:end -->\n?", "\n", text, flags=re.S)
    pairs = re.findall(
        r"<details>\s*<summary[^>]*>(.*?)</summary>\s*<p[^>]*>(.*?)</p>\s*</details>",
        text,
        flags=re.S | re.I,
    )
    if not pairs:
        raise ValueError(f"no FAQ details found in {path}")
    entities = [
        {
            "@type": "Question",
            "name": strip_tags(question),
            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(answer)},
        }
        for question, answer in pairs
    ]
    payload = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    block = (
        '<!-- faq-schema:start -->\n'
        '<script type="application/ld+json">\n'
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + '\n</script>\n'
        '<!-- faq-schema:end -->\n'
    )
    text = text.replace("</head>", block + "</head>", 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for lang, pages in SEO.items():
        for filename, data in pages.items():
            path = ROOT / lang / filename
            if path.exists():
                localize_head(path, lang, data)
                print(f"localized head: {path.relative_to(ROOT)}")
    for path in (ROOT / "consultancy.html", ROOT / "tr" / "consultancy.html", ROOT / "fa" / "consultancy.html"):
        faq_schema(path)
        print(f"FAQ schema: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
