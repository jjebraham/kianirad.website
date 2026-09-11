#!/usr/bin/env python3
"""
build_i18n.py — regenerate the static tr/ and fa/ page copies from the
English root pages of kianirad.website.

Why this exists
---------------
The site is static and has no framework. assets/site.js exposes a global
KR object with a BASE string dictionary (rail/nav/footer) and an i18n
engine; every English page additionally defines window.PAGE_STRINGS
({en:{}, tr:{}, fa:{}}) inline BEFORE site.js loads. At runtime KR merges
BASE + PAGE_STRINGS and rewrites elements marked with:

    data-i18n="key"              -> textContent = t(key)
    data-i18n-html="key"         -> innerHTML   = t(key)
    data-i18n-attr="attr:key"    -> setAttribute(attr, t(key))

For SEO and no-JS robustness the tr/ and fa/ directories hold pre-rendered
static copies with the target language already baked into the HTML. This
script regenerates those copies so they never drift from the English
source pages. It is the ONLY writer of tr/*.html and fa/*.html (except
tr/klinikler-icin-telegram-botu.html, which is a hand-written TR-only
landing page and is not touched here).

What the script does, per page and per language (tr, fa)
--------------------------------------------------------
1. Reads the English root page.
2. Extracts the merged string dictionaries. If `node` is on PATH it evals
   the page's inline PAGE_STRINGS block plus assets/site.js in a stubbed
   sandbox and asks KR.t() for every key referenced in the HTML (this
   mirrors the real merge + en-fallback semantics exactly). Without node
   it falls back to a tolerant JS-object-literal parser in pure Python.
3. Rewrites the HTML (offset-based, via html.parser — inline scripts and
   everything not explicitly touched are preserved byte-for-byte):
     - <html lang="tr"> (dir="ltr") / <html lang="fa" dir="rtl">, plus the
       data-static-lang="tr|fa" marker that tells site.js not to consult
       localStorage for the language.
     - Bakes t(key) into every data-i18n / data-i18n-html element and every
       data-i18n-attr attribute.
     - Translates <title>, meta description, og:title, og:description,
       twitter:title and twitter:description using the META dictionary
       below (pages do not carry meta strings in PAGE_STRINGS, so the
       translations live here; they are derived from each page's English
       meta and were seeded from the owner-maintained tr/fa copies).
     - Sets a per-language canonical URL and a complete reciprocal
       hreflang set (en, tr, fa, x-default -> en). If the source page has
       the <!-- i18n-hreflang:start/end --> markers the block is replaced
       wholesale; otherwise existing hreflang links are removed and a
       marked block is inserted after the canonical link.
     - Sets og:locale (tr_TR / fa_IR) and og:locale:alternate for the
       other two locales; sets og:url to the per-language canonical.
     - Rewrites relative asset/image references (href/src="assets/..." or
       "images/...") to ../... so they resolve from the subdirectory. Root-absolute
       paths (/favicon.ico, /privacy.html, /cdn-cgi/...) are intentionally
       left untouched, matching the owner's hand-maintained copies.
4. Writes tr/<page> and fa/<page>.

Idempotent: input is always the EN root page, output only tr//fa/.
Re-run it after any edit to the English pages.

Usage:  python3 build_i18n.py            # regenerate everything
        python3 build_i18n.py --check    # report drift, write nothing
Stdlib only.
"""

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://www.kianirad.website"

# English root pages that get static tr/fa copies. Missing files are
# skipped with a warning so the script survives partial repo states.
PAGES = [
    "index.html",
    "projects.html",
    "consultancy.html",
    "about.html",
    "contact.html",
    "privacy.html",
    "status.html",
]

LANGS = {
    "tr": {"dir": "ltr", "locale": "tr_TR", "alternates": ["en_US", "fa_IR"]},
    "fa": {"dir": "rtl", "locale": "fa_IR", "alternates": ["en_US", "tr_TR"]},
}

# ---------------------------------------------------------------------------
# META: per-page, per-language translations of the head metadata.
# Derived from each page's English <title>/meta description/og tags and
# seeded from the owner-maintained tr/fa copies (so regeneration does not
# degrade the existing translations). og values fall back to the plain
# title/description when not given.
# ---------------------------------------------------------------------------
META = {
    "index.html": {
        "tr": {
            "title": "Hadi Kianirad — Backend, Telegram botları ve otomasyon, İstanbul",
            "description": "İstanbul merkezli Python backend, Telegram botu ve yapay zekâ otomasyonu. Üretimde çalışan 14+ sistem; Türkçe, İngilizce ve Farsça.",
            "og_title": "Hadi Kianirad — Backend, botlar ve otomasyon",
            "og_description": "İşletmeler için Python backend, Telegram botları ve yapay zekâ otomasyonu. Çalışmaya devam eden sistemler.",
        },
        "fa": {
            "title": "هادی کیانی‌راد — بک‌اند، ربات تلگرام و اتوماسیون | استانبول",
            "description": "طراحی و توسعه‌ی بک‌اند پایتون، ربات تلگرام و اتوماسیون هوش مصنوعی برای کسب‌وکارها؛ بیش از ۱۴ سیستم فعال، به فارسی، ترکی و انگلیسی.",
            "og_title": "هادی کیانی‌راد — بک‌اند، ربات تلگرام و اتوماسیون | استانبول",
            "og_description": "بک‌اند، ربات تلگرام و اتوماسیون برای کسب‌وکارهایی که می‌خواهند سیستم‌هایشان شبانه‌روز کار کند.",
        },
    },
    "projects.html": {
        "tr": {
            "title": "Projeler | Hadi Kianirad",
            "description": "Hadi Kianirad'ın canlı sistemleri: gerçek zamanlı veri platformları, Telegram botları, exchange operasyonları ve doğrulama araçları.",
            "og_description": "Canlı sistemler: gerçek zamanlı veri, Telegram botları, exchange operasyonları, doğrulama ve üretim mesajlaşması.",
        },
        "fa": {
            "title": "پروژه‌ها | هادی کیانی‌راد",
            "description": "پروژه‌ها و سیستم‌های فعال هادی کیانی‌راد؛ از پلتفرم داده و ربات تلگرام تا عملیات صرافی، احراز هویت و وب‌سایت چندزبانه.",
            "og_description": "نمونه‌هایی از سیستم‌های واقعی در حال کار؛ داده، ربات تلگرام، فین‌تک، احراز هویت و ابزارهای عملیاتی.",
        },
    },
    "consultancy.html": {
        "tr": {
            "title": "Otomasyon Danışmanlığı | Hadi Kianirad",
            "description": "Tekrarlayan işleri azaltmak için Python, Telegram ve yapay zekâ otomasyonu danışmanlığı. Kapsam ve sabit fiyat iş başlamadan önce yazılı olarak belirlenir.",
            "og_description": "Ekibinizin zamanını alan tekrar eden işi bulun, doğru otomasyonu kurun ve sonucu haftalık çalışan sürümlerle görün.",
        },
        "fa": {
            "title": "مشاوره‌ی اتوماسیون | هادی کیانی‌راد",
            "description": "مشاوره و اجرای اتوماسیون با پایتون، ربات تلگرام و هوش مصنوعی برای کم‌کردن کارهای تکراری؛ محدوده و قیمت پیش از شروع مشخص می‌شود.",
            "og_description": "کار تکراری‌ای را که وقت تیم‌تان را می‌گیرد پیدا کنید، اول همان را خودکار کنید و نتیجه را قبل از بزرگ‌تر کردن پروژه ببینید.",
        },
    },
    "about.html": {
        "tr": {
            "title": "Hakkımda | Hadi Kianirad",
            "description": "İstanbul'da çalışan backend ve otomasyon mühendisi Hadi Kianirad: Python, sistem yönetimi, Telegram botları ve üretim sistemleri.",
            "og_description": "Hadi Kianirad'ın backend, otomasyon, Python ve üretim sistemleri geçmişi.",
        },
        "fa": {
            "title": "درباره من | هادی کیانی‌راد",
            "description": "هادی کیانی‌راد، مهندس بک‌اند و اتوماسیون در استانبول؛ با تجربه‌ی Python، مدیریت سیستم، ربات تلگرام و نگهداری سیستم‌های واقعی.",
            "og_description": "درباره‌ی تجربه‌ی هادی کیانی‌راد در بک‌اند، اتوماسیون، Python و ساخت و نگهداری سیستم‌های واقعی.",
        },
    },
    "contact.html": {
        "tr": {
            "title": "İletişim | Hadi Kianirad",
            "description": "Backend, Telegram botu veya yapay zekâ otomasyonu projenizi Hadi Kianirad ile görüşün. Türkçe, İngilizce veya Farsça iletişim kurun.",
            "og_description": "İşletmenizin zamanını alan işi anlatın; Türkçe, İngilizce veya Farsça iletişim kurun.",
        },
        "fa": {
            "title": "تماس | هادی کیانی‌راد",
            "description": "برای پروژه‌ی بک‌اند، ربات تلگرام، وب‌سایت یا اتوماسیون هوش مصنوعی با هادی کیانی‌راد تماس بگیرید؛ به فارسی، انگلیسی یا ترکی.",
            "og_description": "کاری را که هر هفته وقت‌تان را می‌گیرد توضیح دهید؛ به فارسی، انگلیسی یا ترکی.",
        },
    },
    "privacy.html": {
        "tr": {
            "title": "Gizlilik ve KVKK | Hadi Kianirad",
            "description": "kianirad.website iletişim formunda hangi bilgilerin işlendiği, nereye gönderildiği ve KVKK kapsamındaki haklarınız.",
            "og_description": "kianirad.website iletişim taleplerini ve kişisel verileri nasıl işler.",
        },
        "fa": {
            "title": "حریم خصوصی | هادی کیانی‌راد",
            "description": "توضیح روشن درباره‌ی اطلاعاتی که فرم تماس kianirad.website دریافت می‌کند، نحوه‌ی استفاده از آن و حقوق شما درباره‌ی داده‌های شخصی.",
            "og_description": "نحوه‌ی دریافت، استفاده و نگهداری اطلاعات تماس و درخواست‌های حریم خصوصی در kianirad.website.",
        },
    },
    "status.html": {
        "tr": {
            "title": "Sistem Durumu | Hadi Kianirad",
            "description": "Hadi Kianirad'ın bakımını üstlendiği üretim sistemlerinin güncel durumu ve son kontrol zamanı.",
            "og_description": "Canlı üretim sistemlerinin durumu ve son kontrol zamanı.",
        },
        "fa": {
            "title": "وضعیت سرویس‌ها | هادی کیانی‌راد",
            "description": "صفحه‌ی وضعیت عمومی سرویس‌ها در حال راه‌اندازی است؛ تا اتصال و تأیید بررسی‌های واقعی، آمار خودکار آپ‌تایم منتشر نمی‌شود.",
            "og_description": "وضعیت عمومی سرویس‌ها در حال راه‌اندازی است و فعلاً آمار خودکار آپ‌تایم منتشر نمی‌شود.",
        },
    },
}

# ---------------------------------------------------------------------------
# Static-only baked-content overrides.
# Some baked fragments intentionally differ from the runtime dictionary
# value. Example: privacy.html "rights2" carries a Cloudflare-obfuscated
# email link in the static HTML (nice for no-JS readers and scrapers),
# while the PAGE_STRINGS value (which KR.t() would apply at runtime) uses
# the plain address. Keyed by (page, language, i18n key); the value is
# baked verbatim as the element's static inner HTML.
# ---------------------------------------------------------------------------
BAKE_OVERRIDES = {
    ("privacy.html", "tr", "rights2"): """Gizlilik talebi için <a href="mailto:kianirad2020@gmail.com">kianirad2020@gmail.com</a> adresine yazın ve hangi bilgi veya başvurudan söz ettiğinizi belirtin. Doğru kişiye yanıt verdiğimden emin olmak için yeterli bilgi istemem gerekebilir.""",
    ("privacy.html", "fa", "rights2"): """برای درخواست مربوط به حریم خصوصی به <a href="mailto:kianirad2020@gmail.com">kianirad2020@gmail.com</a> ایمیل بزنید و توضیح دهید درخواست‌تان مربوط به کدام اطلاعات یا پیام است. ممکن است برای اطمینان از اینکه پاسخ را به شخص درست می‌دهم، اطلاعات بیشتری برای تأیید هویت از شما بخواهم.""",
}

# ---------------------------------------------------------------------------
# Translated application/ld+json blocks. The owner hand-translated the
# FAQPage JSON-LD on the tr/fa consultancy pages; those translations live
# here so regeneration keeps them. A block is only swapped in when the
# English source block still matches the recorded sha256 — if the EN
# structured data changes, the script keeps the English block and prints a
# warning instead of silently serving stale structured data.
# ---------------------------------------------------------------------------
JSONLD = {
    ("consultancy.html", "tr"): {
        "sha256": "c8017f2c0031e2a05115c48f287800167f15bb3e16e14df45c717a7bf8348c83",
        "block": """
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Ya otomasyon işe yaramazsa?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Kapsam, “çalışıyor”un ne demek olduğu dâhil, başlamadan önce yazılı olarak sabitlenir. Bunu karşılamayan bir şey teslim edersem masrafı bana ait olmak üzere düzeltirim. Yapmayacağım şey, kontrolümde olmayan bir ticari sonucu vaat etmek: yazılımın doğru cevap verdiğini garanti ederim, pazarınızın daha çok satın alacağını değil."
      }
    },
    {
      "@type": "Question",
      "name": "Yapılan iş bana mı ait olur?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evet. Son ödemeyle birlikte kod, veri ve hesaplar sizindir. Barındırmanızı rehin tutmam ve ayrılırsanız başka bir geliştiriciye sorunsuz devrederim."
      }
    },
    {
      "@type": "Question",
      "name": "Verimi bir şeyi eğitmek için kullanır mısınız?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Hayır. İçeriğiniz yalnızca kendi sisteminizi yapılandırmak için kullanılır. Proje müşteri verisi içeriyorsa, başlamadan önce hangi üçüncü taraf servislerin bu veriye dokunduğunu tek tek söylerim; kararı siz verirsiniz."
      }
    },
    {
      "@type": "Question",
      "name": "Faturalama nasıl, hangi para biriminde?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "USD veya EUR üzerinden sabit fiyat, iki taksitte faturalanır. Türkiye'deki müşteriler lira olarak faturalandırılabilir. Bakım paketleri aylık faturalanır."
      }
    },
    {
      "@type": "Question",
      "name": "Neleri almıyorsunuz?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sizin bütçenizle öğreneceğim işleri, native mobil uygulamaları ve sizin tarafınızda karar verebilecek kimsenin olmadığı projeleri. Vasat bir işi yavaşça teslim etmektense sizi daha uygun birine yönlendirmeyi tercih ederim."
      }
    }
  ]
}
""",
    },
    ("consultancy.html", "fa"): {
        "sha256": "c8017f2c0031e2a05115c48f287800167f15bb3e16e14df45c717a7bf8348c83",
        "block": """
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "اگر اتوماسیون درست کار نکند چه؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "قبل از شروع، دقیقاً و مکتوب مشخص می‌کنیم «درست کار کردن» یعنی چه. اگر چیزی تحویل بدهم که با آن توافق مطابقت نداشته باشد، با هزینه‌ی خودم اصلاحش می‌کنم. چیزی که تضمین نمی‌کنم نتیجه‌ای تجاری است که در کنترل من نیست؛ می‌توانم درست کار کردن نرم‌افزار را تضمین کنم، نه اینکه بازار حتماً بیشتر بخرد."
      }
    },
    {
      "@type": "Question",
      "name": "کد و سیستمی که می‌سازید در نهایت مال من است؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "بله. بعد از پرداخت نهایی، کد، داده‌ها و حساب‌ها برای شماست. شما را با میزبانی یا دسترسی‌ها به خودم وابسته نمی‌کنم و اگر بخواهید با برنامه‌نویس دیگری ادامه بدهید، سیستم را بدون دردسر تحویل می‌دهم."
      }
    },
    {
      "@type": "Question",
      "name": "از داده‌های من برای آموزش مدل استفاده می‌کنید؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "نه. محتوای شما فقط برای راه‌اندازی و تنظیم سیستم خودتان استفاده می‌شود. اگر پروژه شامل داده‌ی مشتری باشد، قبل از شروع دقیقاً می‌گویم کدام سرویس‌های شخص ثالث به آن داده دسترسی خواهند داشت تا خودتان تصمیم بگیرید."
      }
    },
    {
      "@type": "Question",
      "name": "فاکتور را چطور و با چه ارزی صادر می‌کنید؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "قیمت پروژه از قبل مشخص می‌شود و معمولاً به دلار یا یورو، در دو بخش، فاکتور می‌شود. برای مشتریان داخل ترکیه امکان فاکتور به لیر هم وجود دارد. هزینه‌ی نگهداری به‌صورت ماهانه محاسبه می‌شود."
      }
    },
    {
      "@type": "Question",
      "name": "چه پروژه‌هایی را قبول نمی‌کنید؟",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "پروژه‌ای را که لازم باشد با بودجه‌ی شما تازه یاد بگیرم قبول نمی‌کنم؛ همین‌طور اپلیکیشن موبایل نیتیو و پروژه‌ای که در سمت شما کسی اختیار تصمیم‌گیری ندارد. اگر فرد مناسب‌تری برای کار وجود داشته باشد، ترجیح می‌دهم معرفی‌اش کنم تا اینکه کاری را که مناسب من نیست با کیفیت متوسط تحویل بدهم."
      }
    }
  ]
}
""",
    },
}


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


# ---------------------------------------------------------------------------
# Escaping helpers (match the owner's existing output style)
# ---------------------------------------------------------------------------
def esc_text(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_attr(s):
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace("'", "&#x27;"))


# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------
def page_url(lang, page):
    """Canonical URL for a page in a language. index.html maps to the root."""
    path = "" if page == "index.html" else page
    if lang == "en":
        return SITE + "/" + path
    return SITE + "/" + lang + "/" + path


def hreflang_block(page):
    lines = ["<!-- i18n-hreflang:start -->"]
    for code in ("en", "tr", "fa"):
        lines.append('<link rel="alternate" hreflang="%s" href="%s">'
                     % (code, page_url(code, page)))
    lines.append('<link rel="alternate" hreflang="x-default" href="%s">'
                 % page_url("en", page))
    lines.append("<!-- i18n-hreflang:end -->")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Dictionary extraction
# ---------------------------------------------------------------------------
def extract_page_strings_src(html):
    """Return the JS source of the inline `window.PAGE_STRINGS = {...};`
    assignment, or None if the page has none."""
    m = re.search(r"window\.PAGE_STRINGS\s*=", html)
    if not m:
        return None
    i = html.index("{", m.end())
    depth = 0
    in_str = None
    esc = False
    j = i
    while j < len(html):
        c = html[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_str:
                in_str = None
        else:
            if c in "\"'`":
                in_str = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return html[m.start():j + 1] + ";"
        j += 1
    raise ValueError("unbalanced PAGE_STRINGS literal")


def keys_used_in_html(html):
    keys = set(re.findall(r'data-i18n(?:-html)?="([^"]+)"', html))
    for pair in re.findall(r'data-i18n-attr="([^"]+)"', html):
        for p in pair.split(","):
            if ":" in p:
                keys.add(p.split(":", 1)[1].strip())
    return sorted(keys)


NODE_HARNESS = r"""
// Sandboxed harness: stub just enough browser surface for site.js to load,
// then dump t(key) for every requested key in every requested language.
const fs = require("fs");
var window = {};
var document = {
  readyState: "loading",
  addEventListener: function () {},
  documentElement: { setAttribute: function () {} },
  querySelectorAll: function () { return []; }
};
var navigator = {};
var location = { pathname: "/", protocol: "https:", search: "", hash: "" };
var localStorage = { getItem: function () { return null; }, setItem: function () {} };

const pageSrc = fs.readFileSync(process.argv[2], "utf8");   // PAGE_STRINGS block
const siteSrc = fs.readFileSync(process.argv[3], "utf8");   // assets/site.js
const keys = JSON.parse(fs.readFileSync(process.argv[4], "utf8"));
const langs = JSON.parse(process.argv[5]);

if (pageSrc) { eval(pageSrc); }
eval(siteSrc + "\nglobalThis.__KR = KR;");

const out = {};
langs.forEach(function (L) {
  __KR.setLang(L);
  out[L] = {};
  keys.forEach(function (k) { out[L][k] = __KR.t(k); });
});
process.stdout.write(JSON.stringify(out));
"""


def dicts_via_node(page_strings_src, site_js_path, keys, langs):
    node = shutil.which("node")
    if not node:
        return None
    try:
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "harness.js").write_text(NODE_HARNESS, encoding="utf-8")
            (td / "page.js").write_text(page_strings_src or "", encoding="utf-8")
            (td / "keys.json").write_text(json.dumps(keys), encoding="utf-8")
            proc = subprocess.run(
                [node, str(td / "harness.js"), str(td / "page.js"),
                 str(site_js_path), str(td / "keys.json"), json.dumps(langs)],
                capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip())
        return json.loads(proc.stdout)
    except Exception as exc:  # fall through to the Python parser
        print("  ! node harness failed (%s); using Python fallback parser" % exc,
              file=sys.stderr)
        return None


# --- tolerant JS object-literal parser (fallback when node is absent) ------
def _skip_ws(src, i):
    while i < len(src):
        if src[i] in " \t\r\n":
            i += 1
        elif src.startswith("//", i):
            i = src.find("\n", i)
            if i == -1:
                return len(src)
        elif src.startswith("/*", i):
            i = src.index("*/", i) + 2
        else:
            break
    return i


def _parse_js_string(src, i):
    quote = src[i]
    i += 1
    out = []
    while i < len(src):
        c = src[i]
        if c == "\\":
            nxt = src[i + 1]
            if nxt == "u":
                out.append(chr(int(src[i + 2:i + 6], 16)))
                i += 6
                continue
            if nxt == "x":
                out.append(chr(int(src[i + 2:i + 4], 16)))
                i += 4
                continue
            out.append({"n": "\n", "t": "\t", "r": "\r", "b": "\b",
                        "f": "\f", "v": "\v", "0": "\0"}.get(nxt, nxt))
            i += 2
            continue
        if c == quote:
            return "".join(out), i + 1
        out.append(c)
        i += 1
    raise ValueError("unterminated string in JS literal")


def _parse_js_object(src, i):
    """Parse a JS object literal with string/number/bool/nested-object values."""
    i = _skip_ws(src, i)
    assert src[i] == "{", "expected '{' at %d" % i
    i += 1
    obj = {}
    while True:
        i = _skip_ws(src, i)
        if src[i] == "}":
            return obj, i + 1
        if src[i] in "\"'":
            key, i = _parse_js_string(src, i)
        else:
            m = re.match(r"[A-Za-z_$][\w$]*", src[i:])
            key = m.group(0)
            i += m.end()
        i = _skip_ws(src, i)
        assert src[i] == ":"
        i = _skip_ws(src, i + 1)
        if src[i] in "\"'`":
            val, i = _parse_js_string(src, i)
        elif src[i] == "{":
            val, i = _parse_js_object(src, i)
        else:
            m = re.match(r"[^,}\n]+", src[i:])
            raw = m.group(0).strip()
            try:
                val = int(raw)
            except ValueError:
                try:
                    val = float(raw)
                except ValueError:
                    val = raw
            i += m.end()
        obj[key] = val
        i = _skip_ws(src, i)
        if src[i] == ",":
            i += 1


def dicts_via_python(page_strings_src, site_js_path, keys, langs):
    site_src = Path(site_js_path).read_text(encoding="utf-8")
    m = re.search(r"var\s+BASE\s*=", site_src)
    if not m:
        raise RuntimeError("could not locate BASE dictionary in site.js")
    base, _ = _parse_js_object(site_src, site_src.index("{", m.end()))
    page = {}
    if page_strings_src:
        i = page_strings_src.index("{")
        page, _ = _parse_js_object(page_strings_src, i)
    out = {}
    for L in langs:
        merged = dict(base.get(L, {}))
        merged.update(page.get(L, {}))
        en = dict(base.get("en", {}))
        en.update(page.get("en", {}))
        out[L] = {}
        for k in keys:
            v = merged.get(k)
            if v is None:
                v = en.get(k, "")
            out[L][k] = str(v)
    return out


def get_translations(html, keys, langs):
    """Return {lang: {key: text}} for the keys the page actually uses."""
    page_src = extract_page_strings_src(html)
    site_js = ROOT / "assets" / "site.js"
    dicts = dicts_via_node(page_src, site_js, keys, langs)
    if dicts is None:
        dicts = dicts_via_python(page_src, site_js, keys, langs)
    return dicts


# ---------------------------------------------------------------------------
# Tag-text attribute helpers (operate on the raw start-tag text)
# ---------------------------------------------------------------------------
_ATTR_RE = r'(\s%s\s*=\s*)("[^"]*"|\'[^\']*\'|[^\s>]+)'


def set_attr(tag_text, name, value):
    rx = re.compile(_ATTR_RE % re.escape(name))
    if rx.search(tag_text):
        return rx.sub(lambda m: '%s"%s"' % (m.group(1), esc_attr(value)),
                      tag_text, count=1)
    # insert before the closing > or />
    insert = ' %s="%s"' % (name, esc_attr(value))
    if tag_text.rstrip().endswith("/>"):
        idx = tag_text.rfind("/>")
        return tag_text[:idx] + insert + tag_text[idx:]
    idx = tag_text.rfind(">")
    return tag_text[:idx] + insert + tag_text[idx:]


def get_attr(tag_text, name):
    m = re.search(_ATTR_RE % re.escape(name), tag_text)
    if not m:
        return None
    raw = m.group(2)
    if raw[:1] in "\"'":
        raw = raw[1:-1]
    return raw


def del_attr(tag_text, name):
    return re.sub(_ATTR_RE % re.escape(name), "", tag_text, count=1)


# ---------------------------------------------------------------------------
# The HTML rewriter
# ---------------------------------------------------------------------------
class PageRewriter(HTMLParser):
    """Offset-based rewriter: records (start, end, replacement) edits and
    leaves everything else byte-identical to the English source."""

    def __init__(self, html, page, lang, trans, meta):
        super().__init__(convert_charrefs=False)
        self.src = html
        self.page = page
        self.lang = lang
        self.info = LANGS[lang]
        self.trans = trans          # {key: translated text}
        self.meta = meta            # {title, description, og_title, og_description}
        self.overrides = {k: v for (p, l, k), v in BAKE_OVERRIDES.items()
                          if p == page and l == lang}
        self.edits = []             # (start, end, replacement)
        self.line_starts = [0]
        for m in re.finditer("\n", html):
            self.line_starts.append(m.end())
        self.pending = None         # open data-i18n element being tracked
        self.warnings = []
        self._og_locale_seen = False
        self._locale_alts = iter(self.info["alternates"])
        self.canonical_url = page_url(lang, page)
        self._canonical_tag_end = None
        self._hreflang_tags = []    # (start, end) of stray hreflang links

    # -- position helpers ---------------------------------------------------
    def off(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def t(self, key):
        v = self.trans.get(key, "")
        if v == "":
            self.warnings.append("missing translation for key %r (%s)" %
                                 (key, self.lang))
        return v

    # -- tag handlers -------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        self._starttag(tag, self_closing=False)

    def handle_startendtag(self, tag, attrs):
        self._starttag(tag, self_closing=True)

    def _starttag(self, tag, self_closing):
        raw = self.get_starttag_text()
        start = self.off()
        end = start + len(raw)

        # If we are inside a data-i18n element, only track nesting depth.
        if self.pending is not None:
            if tag == self.pending["tag"] and not self_closing \
                    and tag not in VOID_TAGS:
                self.pending["depth"] += 1
            return

        new = raw

        if tag == "html":
            new = set_attr(new, "lang", self.lang)
            new = set_attr(new, "dir", self.info["dir"])
            new = set_attr(new, "data-static-lang", self.lang)

        elif tag == "title":
            self.pending = {"tag": "title", "content_start": end,
                            "value": esc_text(self.meta["title"]), "depth": 1}

        elif tag == "meta":
            name = get_attr(raw, "name")
            prop = get_attr(raw, "property")
            if name == "description":
                new = set_attr(new, "content", self.meta["description"])
            elif name == "twitter:title":
                new = set_attr(new, "content", self.meta["og_title"])
            elif name == "twitter:description":
                new = set_attr(new, "content", self.meta["og_description"])
            elif prop == "og:title":
                new = set_attr(new, "content", self.meta["og_title"])
            elif prop == "og:description":
                new = set_attr(new, "content", self.meta["og_description"])
            elif prop == "og:url":
                new = set_attr(new, "content", self.canonical_url)
            elif prop == "og:locale":
                new = set_attr(new, "content", self.info["locale"])
                self._og_locale_seen = True
                alts = "\n" + "\n".join(
                    '<meta property="og:locale:alternate" content="%s">' % a
                    for a in self.info["alternates"])
                self.edits.append((end, end, alts))
            elif prop == "og:locale:alternate":
                # Source already has alternates: rewrite in canonical order,
                # drop extras so reruns and hand edits stay consistent.
                try:
                    alt = next(self._locale_alts)
                    new = set_attr(new, "content", alt)
                except StopIteration:
                    new = ""

        elif tag == "link":
            rel = (get_attr(raw, "rel") or "").lower()
            if rel == "canonical":
                new = set_attr(new, "href", self.canonical_url)
                self._canonical_tag_end = end
            elif "alternate" in rel and get_attr(raw, "hreflang"):
                # Only reached when the marked block is absent; the caller
                # decided to strip stray hreflang links and insert a block.
                if not self._markers_present:
                    self._hreflang_tags.append((start, end))
                    return

        # data-i18n* baking
        if new != "" and tag not in ("html", "meta", "link", "title"):
            i18n = get_attr(raw, "data-i18n")
            i18n_html = get_attr(raw, "data-i18n-html")
            i18n_attr = get_attr(raw, "data-i18n-attr")
            if i18n_attr:
                for pair in i18n_attr.split(","):
                    if ":" in pair:
                        attr, key = pair.split(":", 1)
                        new = set_attr(new, attr.strip(), self.t(key.strip()))
            key, is_html = (i18n_html, True) if i18n_html else (i18n, False)
            if key and not self_closing and tag not in VOID_TAGS:
                override = self.overrides.get(key)
                if override is not None:
                    val = override  # verbatim static-only baked HTML
                else:
                    val = self.t(key)
                    if not is_html:
                        val = esc_text(val)
                self.pending = {"tag": tag, "content_start": end,
                                "value": val, "depth": 1}

        # relative asset paths must keep working from tr//fa/ subdirectories
        if new:
            for a in ("href", "src"):
                v = get_attr(new, a)
                if v and (v.startswith("assets/") or v.startswith("images/")):
                    new = set_attr(new, a, "../" + v)

        if new != raw:
            self.edits.append((start, end, new))

    def handle_endtag(self, tag):
        if self.pending is not None and tag == self.pending["tag"]:
            self.pending["depth"] -= 1
            if self.pending["depth"] == 0:
                self.edits.append((self.pending["content_start"], self.off(),
                                   self.pending["value"]))
                self.pending = None

    # -- driver ---------------------------------------------------------------
    _markers_present = True

    def render(self):
        self._markers_present = (
            "<!-- i18n-hreflang:start -->" in self.src
            and "<!-- i18n-hreflang:end -->" in self.src)
        self.feed(self.src)
        self.close()
        if self.pending is not None:
            self.warnings.append("unclosed data-i18n element <%s>" %
                                 self.pending["tag"])

        # hreflang handling
        if self._markers_present:
            pass  # handled by regex in build_page()
        elif self._hreflang_tags:
            for (s, e) in self._hreflang_tags:
                self.edits.append((s, e, ""))
            if self._canonical_tag_end:
                self.edits.append((self._canonical_tag_end,
                                   self._canonical_tag_end,
                                   "\n" + hreflang_block(self.page)))

        out = self.src
        for (s, e, repl) in sorted(self.edits, key=lambda x: x[0],
                                   reverse=True):
            out = out[:s] + repl + out[e:]
        return out


def apply_jsonld(page, lang, out):
    """Swap in the translated JSON-LD block for (page, lang), but only when
    the English source block still matches the recorded sha256 — a changed
    English block keeps English structured data plus a loud warning rather
    than silently serving a stale translation."""
    entry = JSONLD.get((page, lang))
    if not entry:
        return out
    matched = []

    def repl(m):
        if hashlib.sha256(m.group(2).encode()).hexdigest() == entry["sha256"]:
            matched.append(True)
            return m.group(1) + entry["block"] + m.group(3)
        return m.group(0)

    out = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',
                 repl, out, flags=re.S)
    if not matched:
        print("  ! %s [%s]: English JSON-LD changed; kept English structured "
              "data (TODO: retranslate and update JSONLD)" % (page, lang),
              file=sys.stderr)
    return out


def build_page(page, lang, html, dicts):
    meta = dict(META.get(page, {}).get(lang, {}))
    if not meta.get("title"):
        # No dictionary entry: reuse the English head so nothing breaks,
        # and say so loudly. Add proper translations to META above.
        en_title = re.search(r"(?s)<title>(.*?)</title>", html)
        en_desc = re.search(r'<meta name="description" content="([^"]*)"', html)
        en_ogd = re.search(r'<meta property="og:description" content="([^"]*)"', html)
        meta = {
            "title": en_title.group(1) if en_title else "",
            "description": en_desc.group(1) if en_desc else "",
            "og_title": "",
            "og_description": en_ogd.group(1) if en_ogd else "",
        }
        print("  ! %s [%s]: no META entry, English meta reused (TODO: translate)"
              % (page, lang), file=sys.stderr)
    meta.setdefault("og_title", meta["title"])
    meta.setdefault("og_description", meta["description"])
    if not meta["og_title"]:
        meta["og_title"] = meta["title"]

    rw = PageRewriter(html, page, lang, dicts[lang], meta)
    out = rw.render()
    out = apply_jsonld(page, lang, out)

    if rw._markers_present:
        block = hreflang_block(page)
        out = re.sub(
            r"<!-- i18n-hreflang:start -->.*?<!-- i18n-hreflang:end -->",
            lambda _m: block, out, count=1, flags=re.S)

    for w in rw.warnings:
        print("  ! %s [%s]: %s" % (page, lang, w), file=sys.stderr)
    return out


def main():
    check_only = "--check" in sys.argv
    langs = list(LANGS)
    changed, drift = [], []
    for page in PAGES:
        src_path = ROOT / page
        if not src_path.exists():
            print("  ! %s missing, skipped" % page, file=sys.stderr)
            continue
        html = src_path.read_text(encoding="utf-8")
        keys = keys_used_in_html(html)
        dicts = get_translations(html, keys, langs)
        for lang in langs:
            out = build_page(page, lang, html, dicts)
            dest = ROOT / lang / page
            dest.parent.mkdir(exist_ok=True)
            if dest.exists() and dest.read_text(encoding="utf-8") == out:
                continue
            if check_only:
                drift.append("%s/%s" % (lang, page))
            else:
                dest.write_text(out, encoding="utf-8")
                changed.append("%s/%s" % (lang, page))
    if check_only:
        if drift:
            print("drift detected:")
            print("\n".join("  " + d for d in drift))
            return 1
        print("tr/ and fa/ are up to date")
        return 0
    print("wrote %d file(s):" % len(changed))
    print("\n".join("  " + c for c in changed) or "  (no changes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
