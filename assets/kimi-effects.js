/* Kianirad — Kimi visual interaction layer.
   Loaded after ui-v2.js; adds only the visual/interaction features that are not in the reliability layer. */
(function () {
  "use strict";

  var reduce = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  var PRINCIPLES = {
  "en": {
    "h": "Principles",
    "cards": [
      [
        "Fixed price before work",
        "Agreed in writing. It doesn't change mid-project."
      ],
      [
        "Half up front, half on delivery",
        "You never pay for something you haven't seen."
      ],
      [
        "You own the code and the docs",
        "Repositories, credentials and documentation are yours from day one."
      ],
      [
        "I stay after launch",
        "Monitoring, backups, and a human who answers."
      ]
    ]
  },
  "tr": {
    "h": "İlkeler",
    "cards": [
      [
        "İşe başlamadan sabit fiyat",
        "Yazılı olarak anlaşılır. Proje ortasında değişmez."
      ],
      [
        "Yarısı başta, yarısı teslimde",
        "Görmediğiniz bir şey için asla ödeme yapmazsınız."
      ],
      [
        "Kod ve dokümanlar sizindir",
        "Depolar, erişim bilgileri ve dokümantasyon ilk günden sizin."
      ],
      [
        "Yayından sonra da kalırım",
        "İzleme, yedekleme ve cevap veren bir insan."
      ]
    ]
  },
  "fa": {
    "h": "اصول همکاری",
    "cards": [
      [
        "قیمت از قبل مشخص است",
        "قبل از شروع مکتوب توافق می‌کنیم و وسط پروژه بدون توافق تغییر نمی‌کند."
      ],
      [
        "نصف اول، نصف موقع تحویل",
        "نصف دوم را وقتی می‌پردازید که نتیجه‌ی کار را دیده‌اید."
      ],
      [
        "کد و مستندات برای شماست",
        "مخزن کد، دسترسی‌ها و مستندات از روز اول برای شماست."
      ],
      [
        "بعد از راه‌اندازی هم هستم",
        "پایش، بک‌آپ و یک آدم واقعی که جواب می‌دهد."
      ]
    ]
  }
};

  var FAQS = {
  "en": {
    "h": "Common questions, straight answers",
    "items": [
      [
        "How long does a typical project take?",
        "A website is about three weeks, a bot around four, larger backends six. You get the timeline in writing with the quote."
      ],
      [
        "How do payments work?",
        "Half up front, half on delivery. Fixed price agreed before work starts — the number doesn't move."
      ],
      [
        "Do you work in Turkish and Persian?",
        "Yes — including proper right-to-left layout. This page is the demo: switch language in the sidebar."
      ],
      [
        "What happens after launch?",
        "I stay: monitoring, backups, security updates. Monthly care plan, cancel any time."
      ],
      [
        "What if my project isn't a fit?",
        "I'll say so on the first call and point you somewhere better. That call costs you nothing."
      ]
    ]
  },
  "tr": {
    "h": "Sık sorulan sorular, net cevaplar",
    "items": [
      [
        "Tipik bir proje ne kadar sürer?",
        "Bir web sitesi yaklaşık üç hafta, bir bot dört, daha büyük backend'ler altı hafta sürer. Takvimi teklifle birlikte yazılı alırsınız."
      ],
      [
        "Ödemeler nasıl işliyor?",
        "Yarısı başta, yarısı teslimde. İşe başlamadan sabit fiyat anlaşılır — rakam oynamaz."
      ],
      [
        "Türkçe ve Farsça çalışıyor musunuz?",
        "Evet — düzgün sağdan sola düzen dâhil. Bu sayfa zaten demosu: kenar çubuğundan dili değiştirin."
      ],
      [
        "Yayından sonra ne oluyor?",
        "Kalmaya devam ederim: izleme, yedekleme, güvenlik güncellemeleri. Aylık bakım planı, istediğinizde iptal."
      ],
      [
        "Proje bana uygun değilse?",
        "İlk görüşmede açıkça söylerim ve sizi daha iyi bir yere yönlendiririm. O görüşme size hiçbir şeye mal olmaz."
      ]
    ]
  },
  "fa": {
    "h": "سؤال‌های رایج، جواب‌های روشن",
    "items": [
      [
        "یک پروژه معمولاً چقدر زمان می‌برد؟",
        "یک وب‌سایت حدود ۳ هفته، یک ربات حدود ۴ هفته و بک‌اندهای بزرگ‌تر حدود ۶ هفته. زمان‌بندی را همراه با پیشنهاد قیمت، مکتوب دریافت می‌کنید."
      ],
      [
        "پرداخت به چه شکل است؟",
        "نصف مبلغ اول کار و نصف موقع تحویل. قیمت قبل از شروع مشخص می‌شود و وسط پروژه بدون توافق تغییر نمی‌کند."
      ],
      [
        "فارسی و ترکی هم کار می‌کنید؟",
        "بله، از جمله چیدمان درست راست‌به‌چپ. همین صفحه نمونه‌اش است؛ زبان را از کنار صفحه عوض کنید."
      ],
      [
        "بعد از راه‌اندازی چه می‌شود؟",
        "می‌مانم: پایش، بک‌آپ و به‌روزرسانی‌های امنیتی. نگهداری ماهانه است و هر وقت بخواهید می‌توانید لغوش کنید."
      ],
      [
        "اگر پروژه‌ام مناسب شما نباشد چه؟",
        "همان تماس اول صریح می‌گویم و اگر بتوانم مسیر یا فرد مناسب‌تری پیشنهاد می‌کنم. آن تماس هم رایگان است."
      ]
    ]
  }
};

  var UI = {
  "en": {
    "backTop": "Back to top"
  },
  "tr": {
    "backTop": "Yukarı dön"
  },
  "fa": {
    "backTop": "برگشت به بالا"
  }
};

  function lang() {
    var l = (window.KR && KR.lang) || document.documentElement.lang || "en";
    return PRINCIPLES[l] ? l : "en";
  }

  function isHomepage() {
    return !!(document.getElementById("proof") && document.getElementById("scope"));
  }

  /* ---------- Principles strip (homepage) ---------- */
  function renderPrinciples() {
    var section = document.getElementById("principles-v2");
    if (!section) return;
    var t = PRINCIPLES[lang()];
    section.querySelector("h2").textContent = t.h;
    section.querySelectorAll(".principle-card").forEach(function (card, i) {
      card.querySelector("h3").textContent = t.cards[i][0];
      card.querySelector("p").textContent = t.cards[i][1];
    });
  }

  function addPrinciples() {
    if (!isHomepage() || document.getElementById("principles-v2")) return;
    var scope = document.getElementById("scope");
    var section = document.createElement("section");
    section.id = "principles-v2";
    section.className = "principles-v2";
    var h = document.createElement("h2");
    var grid = document.createElement("div");
    grid.className = "principles-grid";
    for (var i = 0; i < 4; i++) {
      var card = document.createElement("article");
      card.className = "principle-card";
      card.innerHTML = "<h3></h3><p></p>";
      grid.appendChild(card);
    }
    section.appendChild(h);
    section.appendChild(grid);
    scope.parentNode.insertBefore(section, scope);
    renderPrinciples();
    if (window.KR && KR.onChange) KR.onChange(renderPrinciples);
  }

  /* ---------- FAQ accordion (homepage) ---------- */
  function renderFaq() {
    var section = document.getElementById("faq-v2");
    if (!section) return;
    var t = FAQS[lang()];
    section.querySelector("h2").textContent = t.h;
    section.querySelectorAll(".faq-item").forEach(function (item, i) {
      item.querySelector(".faq-q .faq-q-text").textContent = t.items[i][0];
      item.querySelector(".faq-a-inner").textContent = t.items[i][1];
    });
  }

  function addFaq() {
    if (!isHomepage() || document.getElementById("faq-v2")) return;
    var scope = document.getElementById("scope");
    var section = document.createElement("section");
    section.id = "faq-v2";
    section.className = "faq-v2";
    section.appendChild(document.createElement("h2"));
    var list = document.createElement("div");
    list.className = "faq-list";
    for (var i = 0; i < 5; i++) {
      var item = document.createElement("div");
      item.className = "faq-item";
      var q = document.createElement("button");
      q.type = "button";
      q.className = "faq-q";
      q.setAttribute("aria-expanded", "false");
      q.innerHTML = '<span class="faq-q-text"></span><span class="faq-icon" aria-hidden="true"></span>';
      var panel = document.createElement("div");
      panel.className = "faq-a";
      panel.setAttribute("role", "region");
      var inner = document.createElement("div");
      inner.className = "faq-a-inner";
      panel.appendChild(inner);
      q.addEventListener("click", function () {
        var btn = this;
        var it = btn.parentNode;
        var isOpen = it.classList.contains("open");
        list.querySelectorAll(".faq-item.open").forEach(function (o) {
          o.classList.remove("open");
          o.querySelector(".faq-q").setAttribute("aria-expanded", "false");
          o.querySelector(".faq-a").style.maxHeight = "0px";
        });
        if (!isOpen) {
          it.classList.add("open");
          btn.setAttribute("aria-expanded", "true");
          var p = it.querySelector(".faq-a");
          p.style.maxHeight = p.scrollHeight + "px";
        }
      });
      item.appendChild(q);
      item.appendChild(panel);
      list.appendChild(item);
    }
    section.appendChild(list);
    scope.parentNode.insertBefore(section, scope.nextSibling);
    renderFaq();
    if (window.KR && KR.onChange) KR.onChange(renderFaq);
  }

  /* ---------- Scroll-spy (all pages) ---------- */
  function initScrollSpy() {
    if (!("IntersectionObserver" in window)) return;
    var sections = Array.prototype.slice.call(document.querySelectorAll("main section[id]"));
    if (!sections.length) return;
    var pairs = [];
    sections.forEach(function (s) {
      var link = document.querySelector('.railnav a[href*="#' + s.id + '"]');
      if (link) pairs.push({section: s, link: link});
    });
    if (!pairs.length) return;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        pairs.forEach(function (p) { p.link.classList.remove("active"); });
        var hit = pairs.filter(function (p) { return p.section === entry.target; })[0];
        if (hit) hit.link.classList.add("active");
      });
    }, {rootMargin: "-35% 0px -55% 0px", threshold: 0});
    pairs.forEach(function (p) { observer.observe(p.section); });
  }

  /* ---------- Pointer effects: magnetic buttons, spotlight, card tilt ---------- */
  function initPointerFx() {
    if (reduce) return;
    if (!window.matchMedia || !window.matchMedia("(pointer:fine)").matches) return;

    if (!document.querySelector(".cursor-spot")) {
      var spot = document.createElement("div");
      spot.className = "cursor-spot";
      spot.setAttribute("aria-hidden", "true");
      document.body.appendChild(spot);
      var raf = null, sx = 0, sy = 0;
      document.addEventListener("pointermove", function (e) {
        sx = e.clientX; sy = e.clientY;
        if (raf) return;
        raf = requestAnimationFrame(function () {
          spot.style.transform = "translate(" + sx + "px," + sy + "px)";
          raf = null;
        });
      }, {passive: true});
    }

    document.querySelectorAll(".btn").forEach(function (btn) {
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
        var dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
        btn.style.translate = (dx * 4).toFixed(1) + "px " + (dy * 4).toFixed(1) + "px";
      });
      btn.addEventListener("pointerleave", function () {
        btn.style.translate = "0px 0px";
      });
    });

    document.querySelectorAll(".case").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        var rx = ((e.clientY - r.top) / r.height - 0.5) * -5;
        var ry = ((e.clientX - r.left) / r.width - 0.5) * 5;
        card.style.transform = "perspective(700px) rotateX(" + rx.toFixed(2) + "deg) rotateY(" + ry.toFixed(2) + "deg)";
      });
      card.addEventListener("pointerleave", function () {
        card.style.transform = "";
      });
    });
  }

  /* ---------- Particle constellation hero canvas (homepage) ---------- */
  function initParticles() {
    if (reduce || !isHomepage()) return;
    var hero = document.querySelector(".hero");
    if (!hero || hero.querySelector(".hero-canvas")) return;
    var canvas = document.createElement("canvas");
    canvas.className = "hero-canvas";
    canvas.setAttribute("aria-hidden", "true");
    hero.insertBefore(canvas, hero.firstChild);
    var ctx = canvas.getContext("2d");
    if (!ctx) { canvas.remove(); return; }

    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = 0, H = 0, parts = [], running = false, rafId = null;
    var colDot = "rgba(0,0,0,.35)", colLine = "rgba(0,0,0,.12)";

    function readColors() {
      var cs = getComputedStyle(document.documentElement);
      var ink = cs.getPropertyValue("--ink").trim() || "#12233F";
      var accent = cs.getPropertyValue("--accent").trim() || "#137F72";
      colDot = "color-mix(in srgb, " + ink + " 32%, transparent)";
      colLine = "color-mix(in srgb, " + accent + " 20%, transparent)";
    }

    function resize() {
      var r = hero.getBoundingClientRect();
      W = Math.max(1, Math.round(r.width));
      H = Math.max(1, Math.round(r.height));
      canvas.width = W * dpr;
      canvas.height = H * dpr;
      canvas.style.width = W + "px";
      canvas.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(70, Math.max(40, (W * H) / 22000)));
      parts = [];
      for (var i = 0; i < n; i++) {
        parts.push({
          x: Math.random() * W, y: Math.random() * H,
          vx: (Math.random() - 0.5) * 0.22, vy: (Math.random() - 0.5) * 0.22,
          r: 1 + Math.random() * 1.6
        });
      }
    }

    var LINK = 130;
    function frame() {
      if (!running) return;
      ctx.clearRect(0, 0, W, H);
      var i, j, p, q, dx, dy, d;
      for (i = 0; i < parts.length; i++) {
        p = parts[i];
        p.x += p.vx; p.y += p.vy;
        if (p.x < -10) p.x = W + 10; else if (p.x > W + 10) p.x = -10;
        if (p.y < -10) p.y = H + 10; else if (p.y > H + 10) p.y = -10;
      }
      ctx.strokeStyle = colLine;
      ctx.lineWidth = 1;
      for (i = 0; i < parts.length; i++) {
        for (j = i + 1; j < parts.length; j++) {
          p = parts[i]; q = parts[j];
          dx = p.x - q.x; dy = p.y - q.y;
          d = dx * dx + dy * dy;
          if (d < LINK * LINK) {
            ctx.globalAlpha = 1 - Math.sqrt(d) / LINK;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.stroke();
          }
        }
      }
      ctx.globalAlpha = 1;
      ctx.fillStyle = colDot;
      for (i = 0; i < parts.length; i++) {
        p = parts[i];
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      }
      rafId = requestAnimationFrame(frame);
    }

    function play() {
      if (running || document.hidden || !inView) return;
      running = true;
      rafId = requestAnimationFrame(frame);
    }
    function stop() {
      running = false;
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
    }

    var inView = true;
    readColors();
    resize();

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        if (inView) play(); else stop();
      }, {threshold: 0}).observe(hero);
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else play();
    });
    if ("MutationObserver" in window) {
      new MutationObserver(function () { readColors(); })
        .observe(document.documentElement, {attributes: true, attributeFilter: ["data-theme"]});
    }
    var rzT = null;
    window.addEventListener("resize", function () {
      clearTimeout(rzT);
      rzT = setTimeout(function () { resize(); }, 160);
    });
    play();
  }

  /* ---------- Word-by-word hero headline reveal (homepage) ---------- */
  function splitHeadline() {
    if (reduce || !isHomepage()) return;
    var h = document.querySelector(".hero h1.display");
    if (!h) return;
    var text = h.textContent.replace(/\s+/g, " ").trim();
    if (!text) return;
    h.textContent = "";
    var words = text.split(" ");
    words.forEach(function (w, i) {
      var wrap = document.createElement("span");
      wrap.className = "hw-wrap";
      var inner = document.createElement("span");
      inner.className = "hw";
      inner.textContent = w;
      inner.style.transitionDelay = (i * 45) + "ms";
      wrap.appendChild(inner);
      h.appendChild(wrap);
      if (i < words.length - 1) h.appendChild(document.createTextNode(" "));
    });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { h.classList.add("hw-in"); });
    });
  }

  function initHeadline() {
    if (reduce || !isHomepage()) return;
    splitHeadline();
    if (window.KR && KR.onChange) KR.onChange(function () {
      var h = document.querySelector(".hero h1.display");
      if (h) h.classList.remove("hw-in");
      splitHeadline();
    });
  }

  /* ---------- Sticky mobile CTA + back-to-top (all pages) ---------- */
  function addFloatingCtas() {
    if (document.querySelector(".mobile-cta") || document.querySelector(".back-top")) return;
    var ctaText = (window.KR && KR.t("ctaMain")) || "Book a 20-minute call";

    var bar = document.createElement("div");
    bar.className = "mobile-cta";
    var link = document.createElement("a");
    link.className = "btn mobile-cta-btn";
    link.href = "contact.html";
    link.textContent = ctaText;
    bar.appendChild(link);
    document.body.appendChild(bar);

    var top = document.createElement("button");
    top.type = "button";
    top.className = "back-top";
    top.setAttribute("aria-label", UI[lang()].backTop);
    top.title = UI[lang()].backTop;
    top.innerHTML = '<span aria-hidden="true">↑</span>';
    top.addEventListener("click", function () {
      window.scrollTo({top: 0, behavior: reduce ? "auto" : "smooth"});
    });
    document.body.appendChild(top);

    if (window.KR && KR.onChange) KR.onChange(function () {
      link.textContent = (window.KR && KR.t("ctaMain")) || "Book a 20-minute call";
      var t = UI[lang()].backTop;
      top.setAttribute("aria-label", t);
      top.title = t;
    });

    var narrow = window.matchMedia ? window.matchMedia("(max-width:1019px)") : {matches:false};
    var contactVisible = false;

    function update() {
      var past = window.scrollY > window.innerHeight * 0.8;
      var showBar = narrow.matches && past && !contactVisible;
      bar.classList.toggle("show", showBar);
      document.body.classList.toggle("has-mobile-cta", showBar);
      top.classList.toggle("show", window.scrollY > 600);
      top.classList.toggle("above-cta", showBar);
    }

    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { update(); ticking = false; });
    }, {passive: true});
    if (narrow.addEventListener) narrow.addEventListener("change", update);
    else if (narrow.addListener) narrow.addListener(update);

    if ("IntersectionObserver" in window) {
      var contacts = document.querySelectorAll('main section[id*="contact"], main form, main .form, main [id*="form"]');
      if (contacts.length) {
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) contactVisible = true;
            else {
              contactVisible = Array.prototype.some.call(contacts, function (el) {
                var r = el.getBoundingClientRect();
                return r.top < window.innerHeight && r.bottom > 0;
              });
            }
          });
          update();
        }, {threshold: 0.05});
        contacts.forEach(function (el) { io.observe(el); });
      }
    }
    update();
  }

  function start() {
    addPrinciples();
    addFaq();
    initScrollSpy();
    initPointerFx();
    initParticles();
    initHeadline();
    addFloatingCtas();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, {once:true});
  } else {
    start();
  }
})();
