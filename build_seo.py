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
        "status.html": (
            "Sistem Durumu | Hadi Kianirad",
            "Hadi Kianirad'ın bakımını üstlendiği üretim sistemlerinin güncel durumu ve son kontrol zamanı.",
            "Sistem Durumu | Hadi Kianirad",
            "Canlı üretim sistemlerinin durumu ve son kontrol zamanı.",
        ),
    },
    "fa": {
        "index.html": (
            "هادی کیانی‌راد — بک‌اند، ربات تلگرام و اتوماسیون | استانبول",
            "طراحی و توسعه‌ی بک‌اند پایتون، ربات تلگرام و اتوماسیون هوش مصنوعی برای کسب‌وکارها؛ بیش از ۱۴ سیستم فعال، به فارسی، ترکی و انگلیسی.",
            "هادی کیانی‌راد — بک‌اند، ربات تلگرام و اتوماسیون | استانبول",
            "بک‌اند، ربات تلگرام و اتوماسیون برای کسب‌وکارهایی که می‌خواهند سیستم‌هایشان شبانه‌روز کار کند.",
        ),
        "projects.html": (
            "پروژه‌ها | هادی کیانی‌راد",
            "پروژه‌ها و سیستم‌های فعال هادی کیانی‌راد؛ از پلتفرم داده و ربات تلگرام تا عملیات صرافی، احراز هویت و وب‌سایت چندزبانه.",
            "پروژه‌ها | هادی کیانی‌راد",
            "نمونه‌هایی از سیستم‌های واقعی در حال کار؛ داده، ربات تلگرام، فین‌تک، احراز هویت و ابزارهای عملیاتی.",
        ),
        "consultancy.html": (
            "مشاوره‌ی اتوماسیون | هادی کیانی‌راد",
            "مشاوره و اجرای اتوماسیون با پایتون، ربات تلگرام و هوش مصنوعی برای کم‌کردن کارهای تکراری؛ محدوده و قیمت پیش از شروع مشخص می‌شود.",
            "مشاوره‌ی اتوماسیون | هادی کیانی‌راد",
            "کار تکراری‌ای را که وقت تیم‌تان را می‌گیرد پیدا کنید، اول همان را خودکار کنید و نتیجه را قبل از بزرگ‌تر کردن پروژه ببینید.",
        ),
        "about.html": (
            "درباره من | هادی کیانی‌راد",
            "هادی کیانی‌راد، مهندس بک‌اند و اتوماسیون در استانبول؛ با تجربه‌ی Python، مدیریت سیستم، ربات تلگرام و نگهداری سیستم‌های واقعی.",
            "درباره من | هادی کیانی‌راد",
            "درباره‌ی تجربه‌ی هادی کیانی‌راد در بک‌اند، اتوماسیون، Python و ساخت و نگهداری سیستم‌های واقعی.",
        ),
        "contact.html": (
            "تماس | هادی کیانی‌راد",
            "برای پروژه‌ی بک‌اند، ربات تلگرام، وب‌سایت یا اتوماسیون هوش مصنوعی با هادی کیانی‌راد تماس بگیرید؛ به فارسی، انگلیسی یا ترکی.",
            "تماس | هادی کیانی‌راد",
            "کاری را که هر هفته وقت‌تان را می‌گیرد توضیح دهید؛ به فارسی، انگلیسی یا ترکی.",
        ),
        "privacy.html": (
            "حریم خصوصی | هادی کیانی‌راد",
            "توضیح روشن درباره‌ی اطلاعاتی که فرم تماس kianirad.website دریافت می‌کند، نحوه‌ی استفاده از آن و حقوق شما درباره‌ی داده‌های شخصی.",
            "حریم خصوصی | هادی کیانی‌راد",
            "نحوه‌ی دریافت، استفاده و نگهداری اطلاعات تماس و درخواست‌های حریم خصوصی در kianirad.website.",
        ),
        "status.html": (
            "وضعیت سرویس‌ها | هادی کیانی‌راد",
            "صفحه‌ی وضعیت عمومی سرویس‌ها در حال راه‌اندازی است؛ تا اتصال و تأیید بررسی‌های واقعی، آمار خودکار آپ‌تایم منتشر نمی‌شود.",
            "وضعیت سرویس‌ها | هادی کیانی‌راد",
            "وضعیت عمومی سرویس‌ها در حال راه‌اندازی است و فعلاً آمار خودکار آپ‌تایم منتشر نمی‌شود.",
        ),
    },
}

LOCALE = {"tr": "tr_TR", "fa": "fa_IR"}

HOME_FAQ = {
    "tr": [
        ("Tipik bir proje ne kadar sürer?", "Bir web sitesi yaklaşık üç hafta, bir bot dört, daha büyük backend'ler altı hafta sürer. Takvimi teklifle birlikte yazılı alırsınız."),
        ("Ödemeler nasıl işliyor?", "Yarısı başta, yarısı teslimde. İşe başlamadan sabit fiyat anlaşılır — rakam oynamaz."),
        ("Türkçe ve Farsça çalışıyor musunuz?", "Evet — düzgün sağdan sola düzen dâhil. Bu sayfa zaten demosu: kenar çubuğundan dili değiştirin."),
        ("Yayından sonra ne oluyor?", "Kalmaya devam ederim: izleme, yedekleme, güvenlik güncellemeleri. Aylık bakım planı, istediğinizde iptal."),
        ("Proje bana uygun değilse?", "İlk görüşmede açıkça söylerim ve sizi daha iyi bir yere yönlendiririm. O görüşme size hiçbir şeye mal olmaz."),
    ],
    "fa": [
        ("یک پروژه معمولاً چقدر زمان می‌برد؟", "یک وب‌سایت حدود ۳ هفته، یک ربات حدود ۴ هفته و بک‌اندهای بزرگ‌تر حدود ۶ هفته. زمان‌بندی را همراه با پیشنهاد قیمت، مکتوب دریافت می‌کنید."),
        ("پرداخت به چه شکل است؟", "نصف مبلغ اول کار و نصف موقع تحویل. قیمت قبل از شروع مشخص می‌شود و وسط پروژه بدون توافق تغییر نمی‌کند."),
        ("فارسی و ترکی هم کار می‌کنید؟", "بله، از جمله چیدمان درست راست‌به‌چپ. همین صفحه نمونه‌اش است؛ زبان را از کنار صفحه عوض کنید."),
        ("بعد از راه‌اندازی چه می‌شود؟", "می‌مانم: پایش، بک‌آپ و به‌روزرسانی‌های امنیتی. نگهداری ماهانه است و هر وقت بخواهید می‌توانید لغوش کنید."),
        ("اگر پروژه‌ام مناسب شما نباشد چه؟", "همان تماس اول صریح می‌گویم و اگر بتوانم مسیر یا فرد مناسب‌تری پیشنهاد می‌کنم. آن تماس هم رایگان است."),
    ],
}


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


def localize_home_faq_schema(path: Path, lang: str) -> None:
    """Keep homepage FAQ structured data in the same language as the visible FAQ."""
    text = path.read_text(encoding="utf-8")
    entities = [
        {
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": answer},
        }
        for question, answer in HOME_FAQ[lang]
    ]
    payload = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    block = (
        "<!-- FAQPage structured data. Mirrors the localized visible FAQ in assets/kimi-effects.js. -->\n"
        '<script type="application/ld+json">\n'
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n</script>"
    )
    pattern = r"<!-- FAQPage structured data\..*?</script>"
    if not re.search(pattern, text, flags=re.S):
        raise ValueError(f"homepage FAQ schema block not found in {path}")
    text = re.sub(pattern, block, text, count=1, flags=re.S)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for lang, pages in SEO.items():
        for filename, data in pages.items():
            path = ROOT / lang / filename
            if path.exists():
                localize_head(path, lang, data)
                print(f"localized head: {path.relative_to(ROOT)}")
        homepage = ROOT / lang / "index.html"
        if homepage.exists():
            localize_home_faq_schema(homepage, lang)
            print(f"homepage FAQ schema: {homepage.relative_to(ROOT)}")

    for path in (ROOT / "consultancy.html", ROOT / "tr" / "consultancy.html", ROOT / "fa" / "consultancy.html"):
        faq_schema(path)
        print(f"FAQ schema: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
