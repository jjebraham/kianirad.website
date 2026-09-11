/* ============================================================
   Kianirad — shared site script
   EDIT ONLY THE CONFIG BLOCK BELOW. Everything else is machinery.
   ============================================================ */

var KR = (function () {
  "use strict";

  /* ---------- 1. CONFIG — your details and prices live here ---------- */
  var CONFIG = {
    email: "kianirad2020@gmail.com",   // <-- your real email
    telegram: "amirkiaaani",             // <-- your real Telegram username, no @
    github: "jjebraham",

    // TODO: set the real Cal.com/Calendly URL here when JJ supplies it.
    // While blank, "Book a 20-minute call" links keep their contact.html fallback.
    bookingUrl: "",

    // Leave blank ("") and the contact form opens a pre-filled email instead.
    // Put a URL here (your own FastAPI endpoint, Formspree, Web3Forms...) to POST instead.
    formEndpoint: "",

    // TODO: paste the analytics script URL here once a provider is chosen
    // (Cloudflare Web Analytics beacon, Plausible, GoatCounter...).
    // Blank = nothing is loaded. Some providers also need data-* attributes;
    // add them in loadAnalytics() below if so.
    analyticsScript: "",

    // Project price ranges in USD, and rough weeks of work.
    // Change these numbers once; every language and page updates.
    prices: {
      site:  { lo: 900,  hi: 2500, weeks: 3 },
      api:   { lo: 2500, hi: 8000, weeks: 6 },
      bot:   { lo: 1200, hi: 3500, weeks: 4 },
      ai:    { lo: 1500, hi: 5000, weeks: 5 },
      multi: { lo: 400,  hi: 1200, weeks: 1 },
      care:  { monthlyLo: 120, monthlyHi: 400 }
    }
  };

  /* ---------- 2. Shared strings (rail, nav, footer) ---------- */
  var BASE = {
    en: {
      markSub: "Systems that keep running",
      role: "Backend and automation engineer. Istanbul.",
      pulse: "14+ systems in production",
      navHome: "Home",
      navBuild: "What I build",
      navProjects: "Projects",
      navConsult: "Consultancy",
      navAbout: "About",
      navContact: "Contact",
      navPrivacy: "Privacy",
      ctaMain: "Book a 20-minute call",
      foot: "Kiani Limited Liability Company · Istanbul · English, Türkçe, فارسی"
    },
    tr: {
      markSub: "Çalışmaya devam eden sistemler",
      role: "Backend ve otomasyon mühendisi. İstanbul.",
      pulse: "14+ sistem canlıda",
      navHome: "Ana sayfa",
      navBuild: "Neler yapıyorum",
      navProjects: "Projeler",
      navConsult: "Danışmanlık",
      navAbout: "Hakkımda",
      navContact: "İletişim",
      navPrivacy: "Gizlilik",
      ctaMain: "20 dakikalık görüşme ayarla",
      foot: "Kiani Limited Liability Company · İstanbul · English, Türkçe, فارسی"
    },
    fa: {
      markSub: "سیستم‌هایی که از کار نمی‌افتند",
      role: "مهندس بک‌اند و اتوماسیون. استانبول.",
      pulse: "بیش از ۱۴ سیستم در حال اجرا",
      navHome: "خانه",
      navBuild: "چه می‌سازم",
      navProjects: "پروژه‌ها",
      navConsult: "مشاوره",
      navAbout: "درباره من",
      navContact: "تماس",
      navPrivacy: "حریم خصوصی",
      ctaMain: "رزرو گفت‌وگوی ۲۰ دقیقه‌ای",
      foot: "شرکت کیانی · استانبول · English, Türkçe, فارسی"
    }
  };

  /* ---------- 3. Machinery ---------- */
  var LANGS = ["en", "tr", "fa"];
  var CORE_PAGES = ["/", "/index.html", "/projects.html", "/consultancy.html", "/about.html", "/contact.html", "/privacy.html", "/status.html"];
  var dict = {};
  var lang = "en";
  var listeners = [];
  var reduce = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  // merge page-specific strings (set as window.PAGE_STRINGS before this file loads)
  (function merge() {
    var page = window.PAGE_STRINGS || {};
    LANGS.forEach(function (L) {
      dict[L] = {};
      var src = [BASE[L] || {}, page[L] || {}];
      src.forEach(function (o) {
        Object.keys(o).forEach(function (k) { dict[L][k] = o[k]; });
      });
    });
  })();

  function t(key) {
    return (dict[lang] && dict[lang][key] !== undefined) ? dict[lang][key] : (dict.en[key] || "");
  }

  var FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"; // ۰۱۲۳۴۵۶۷۸۹

  // Locale-aware number formatting: FA gets Persian digits with the ٬
  // thousands separator, TR gets tr-TR grouping, EN gets en-US grouping.
  function fmtNum(n) {
    var grouped = Number(n).toLocaleString(lang === "tr" ? "tr-TR" : "en-US");
    if (lang !== "fa") return grouped;
    return grouped.replace(/,/g, "٬").replace(/\d/g, function (d) {
      return FA_DIGITS.charAt(Number(d));
    });
  }

  function money(n) { return "$" + fmtNum(n); }

  function prefersDark() {
    return !!(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
  }

  function languagePath(next) {
    if (LANGS.indexOf(next) === -1) return null;
    var path = location.pathname || "/";
    path = path.replace(/^\/(?:tr|fa)(?=\/)/, "");
    if (!path) path = "/";
    if (CORE_PAGES.indexOf(path) === -1) return null;
    if (path === "/index.html") path = "/";
    if (next === "en") return path;
    return path === "/" ? "/" + next + "/" : "/" + next + path;
  }

  function fillConfigSlots() {
    document.querySelectorAll("[data-kr]").forEach(function (el) {
      var k = el.getAttribute("data-kr");
      var text = "", href = "";

      if (k === "email") {
        text = CONFIG.email;
        href = "mailto:" + CONFIG.email;
      } else if (k === "telegram") {
        text = "@" + CONFIG.telegram;
        href = "https://t.me/" + CONFIG.telegram;
      } else if (k === "github") {
        text = "github.com/" + CONFIG.github;
        href = "https://github.com/" + CONFIG.github;
      } else {
        return;
      }

      if (el.tagName === "A") el.href = href;

      // If the element wraps a .v value span, write into that and leave the rest alone.
      var slot = el.querySelector(".v");
      if (slot) slot.textContent = text;
      else el.textContent = text;
    });
  }

  function fillBookingLinks() {
    if (!CONFIG.bookingUrl) return;
    document.querySelectorAll('a[data-i18n="ctaMain"]').forEach(function (a) {
      a.href = CONFIG.bookingUrl;
      a.target = "_blank";
      a.rel = "noopener";
    });
  }

  // Inject the analytics script only when CONFIG.analyticsScript is set.
  // TODO: if the chosen provider needs extra data-* attributes, add them here.
  function loadAnalytics() {
    if (!CONFIG.analyticsScript) return;
    var s = document.createElement("script");
    s.defer = true;
    s.src = CONFIG.analyticsScript;
    document.head.appendChild(s);
  }

  function ensurePrivacyLink() {
    document.querySelectorAll("footer").forEach(function (footer) {
      if (footer.querySelector(".privacy-link")) return;
      footer.appendChild(document.createTextNode(" · "));
      var link = document.createElement("a");
      link.className = "privacy-link";
      link.href = "/privacy.html";
      link.setAttribute("data-i18n", "navPrivacy");
      link.textContent = BASE.en.navPrivacy;
      footer.appendChild(link);
    });
  }

  function apply(next) {
    if (LANGS.indexOf(next) === -1) next = "en";
    lang = next;
    document.documentElement.lang = lang;
    document.documentElement.dir = (lang === "fa") ? "rtl" : "ltr";

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var v = t(el.getAttribute("data-i18n"));
      if (v) el.textContent = v;
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var v = t(el.getAttribute("data-i18n-html"));
      if (v) el.innerHTML = v;
    });
    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      // format: "placeholder:keyName"
      var pair = el.getAttribute("data-i18n-attr").split(":");
      var v = t(pair[1]);
      if (v) el.setAttribute(pair[0], v);
    });

    document.querySelectorAll(".lang [data-lang]").forEach(function (b) {
      var active = b.getAttribute("data-lang") === lang;
      b.setAttribute("aria-pressed", String(active));
      if (active) b.setAttribute("aria-current", "page");
      else b.removeAttribute("aria-current");
    });

    listeners.forEach(function (fn) { try { fn(lang); } catch (e) { console.error(e); } });
    try { localStorage.setItem("kr-lang", lang); } catch (e) {}
  }

  function setTheme(theme) {
    if (theme !== "dark" && theme !== "light") theme = prefersDark() ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", theme);
    document.documentElement.style.colorScheme = theme;
    var b = document.getElementById("themebtn");
    if (b) {
      b.textContent = (theme === "dark") ? "☀" : "☾";
      b.setAttribute("aria-pressed", String(theme === "dark"));
      b.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
      b.title = b.getAttribute("aria-label");
    }
    try { localStorage.setItem("kr-theme", theme); } catch (e) {}
  }

  function markCurrentNav() {
    var here = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    document.querySelectorAll(".railnav a").forEach(function (a) {
      var target = (a.getAttribute("href") || "").split("#")[0].split("/").pop().toLowerCase();
      if (target && target === here) a.setAttribute("aria-current", "page");
    });
  }

  function init() {
    document.querySelectorAll(".lang [data-lang]").forEach(function (b) {
      b.addEventListener("click", function (event) {
        var next = b.getAttribute("data-lang");
        var target = languagePath(next);
        if (target && location.protocol !== "file:" && location.pathname !== target) {
          if (event && event.preventDefault) event.preventDefault();
          try { localStorage.setItem("kr-lang", next); } catch (e) {}
          location.assign(target + location.search + location.hash);
          return;
        }
        apply(next);
      });
    });

    var tb = document.getElementById("themebtn");
    if (tb) {
      tb.addEventListener("click", function () {
        var cur = document.documentElement.getAttribute("data-theme");
        if (!cur) cur = prefersDark() ? "dark" : "light";
        setTheme(cur === "dark" ? "light" : "dark");
      });
    }

    try {
      var savedTheme = localStorage.getItem("kr-theme");
      setTheme(savedTheme || (prefersDark() ? "dark" : "light"));
    } catch (e) {
      setTheme(prefersDark() ? "dark" : "light");
    }

    ensurePrivacyLink();
    fillConfigSlots();
    fillBookingLinks();
    loadAnalytics();
    markCurrentNav();

    var staticLang = document.documentElement.getAttribute("data-static-lang");
    var savedLang = staticLang || "en";
    if (!staticLang) {
      try { savedLang = localStorage.getItem("kr-lang") || "en"; } catch (e) {}
    }
    apply(savedLang);
  }

  var api = {
    config: CONFIG,
    t: t,
    money: money,
    fmtNum: fmtNum,
    reduce: reduce,
    get lang() { return lang; },
    onChange: function (fn) { listeners.push(fn); },
    setLang: apply
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  return api;
})();
