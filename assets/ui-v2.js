/* Kianirad UI v2 — progressive enhancement, no external animation library. */
(function () {
  "use strict";

  var reduce = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var TECH = ["Python","FastAPI","aiogram","Telegram Bot API","Postgres","SQLite","Docker","GCP","DigitalOcean","LLM APIs","Webhooks","Nginx"];

  var PROCESS = {
    en: {
      h: "How we work",
      d: "A small, visible process: understand the task, agree the risk, build in the open, then keep it healthy.",
      steps: [
        ["Discover","A 20-minute call to identify the repetitive job and whether software should solve it."],
        ["Fixed quote","Scope, price, responsibilities and boundaries are written down before work starts."],
        ["Build","You see a working version every week, not just a status report."],
        ["Launch & care","Handover, monitoring, backups and optional maintenance after launch."]
      ],
      tech: "Technology stack"
    },
    tr: {
      h: "Nasıl çalışıyoruz",
      d: "Küçük ve görünür bir süreç: işi anlayın, riski netleştirin, açık şekilde geliştirin ve sonrasında sistemi sağlıklı tutun.",
      steps: [
        ["Keşif","20 dakikalık görüşmede tekrarlanan işi ve yazılımın gerçekten çözüm olup olmadığını netleştiririz."],
        ["Sabit teklif","Kapsam, fiyat, sorumluluklar ve sınırlar işe başlamadan önce yazılı hâle gelir."],
        ["Geliştirme","Durum raporu yerine her hafta çalışan bir sürüm görürsünüz."],
        ["Yayın ve bakım","Devir, izleme, yedekleme ve isterseniz yayın sonrası bakım."]
      ],
      tech: "Teknoloji yığını"
    },
    fa: {
      h: "چطور با هم کار می‌کنیم",
      d: "فرایندی کوتاه و شفاف: مسئله را بفهمیم، ریسک را مشخص کنیم، جلوی چشم شما بسازیم و بعد از انتشار سالم نگهش داریم.",
      steps: [
        ["شناخت","در یک گفت‌وگوی ۲۰ دقیقه‌ای کار تکراری و این‌که آیا واقعاً باید با نرم‌افزار حل شود را مشخص می‌کنیم."],
        ["قیمت ثابت","محدوده، قیمت، مسئولیت‌ها و مرزهای کار قبل از شروع به‌صورت مکتوب مشخص می‌شود."],
        ["ساخت","هر هفته یک نسخه‌ی قابل استفاده می‌بینید، نه فقط گزارش وضعیت."],
        ["انتشار و نگهداری","تحویل کامل، پایش، پشتیبان‌گیری و در صورت نیاز نگهداری پس از انتشار."]
      ],
      tech: "فناوری‌ها"
    }
  };

  function lang() {
    var l = (window.KR && KR.lang) || document.documentElement.lang || "en";
    return PROCESS[l] ? l : "en";
  }

  function renderProcess() {
    var section = document.getElementById("process-v2");
    if (!section) return;
    var t = PROCESS[lang()];
    section.querySelector("h2").textContent = t.h;
    section.querySelector(".lede").textContent = t.d;
    section.querySelectorAll(".process-card").forEach(function (card, i) {
      card.querySelector(".n").textContent = String(i + 1).padStart(2, "0");
      card.querySelector("h3").textContent = t.steps[i][0];
      card.querySelector("p").textContent = t.steps[i][1];
    });
    var marquee = document.querySelector(".tech-marquee-wrap");
    if (marquee) marquee.setAttribute("aria-label", t.tech);
  }

  function addProcessAndMarquee() {
    var proof = document.getElementById("proof");
    var scope = document.getElementById("scope");
    var build = document.getElementById("build");
    if (!proof || !scope || !build) return;

    if (!document.querySelector(".tech-marquee-wrap")) {
      var wrap = document.createElement("div");
      wrap.className = "tech-marquee-wrap";
      wrap.setAttribute("role", "region");
      var track = document.createElement("div");
      track.className = "tech-marquee";
      track.setAttribute("aria-hidden", "true");
      TECH.concat(TECH).forEach(function (name) {
        var span = document.createElement("span");
        span.textContent = name;
        track.appendChild(span);
      });
      wrap.appendChild(track);
      build.parentNode.insertBefore(wrap, build);
    }

    if (!document.getElementById("process-v2")) {
      var section = document.createElement("section");
      section.id = "process-v2";
      section.className = "process-v2";
      var h = document.createElement("h2");
      var d = document.createElement("p");
      d.className = "lede";
      var grid = document.createElement("div");
      grid.className = "process-grid";
      for (var i = 0; i < 4; i++) {
        var card = document.createElement("article");
        card.className = "process-card";
        card.innerHTML = '<span class="n"></span><h3></h3><p></p>';
        grid.appendChild(card);
      }
      section.appendChild(h);
      section.appendChild(d);
      section.appendChild(grid);
      scope.parentNode.insertBefore(section, scope);
    }

    renderProcess();
    if (window.KR && KR.onChange) KR.onChange(renderProcess);
  }

  function localizedNumber(value) {
    var l = lang();
    var locale = l === "fa" ? "fa-IR" : (l === "tr" ? "tr-TR" : "en-US");
    return new Intl.NumberFormat(locale, {maximumFractionDigits:0}).format(value);
  }

  function animateStat(el) {
    if (el.dataset.krCounted === "1") return;
    var raw = el.textContent.trim();
    var m = raw.match(/^([~≈]?)([\d,]+)(\+?)$/);
    if (!m) return;
    var target = Number(m[2].replace(/,/g, ""));
    if (!Number.isFinite(target)) return;
    el.dataset.krCounted = "1";
    var prefix = m[1] || "";
    var suffix = m[3] || "";
    if (reduce) {
      el.textContent = prefix + localizedNumber(target) + suffix;
      return;
    }
    var start = performance.now();
    var duration = 950;
    function frame(now) {
      var p = Math.min(1, (now - start) / duration);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + localizedNumber(Math.round(target * eased)) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function initCounts() {
    var stats = Array.prototype.slice.call(document.querySelectorAll(".fig b"));
    if (!stats.length) return;
    if (reduce || !("IntersectionObserver" in window)) {
      stats.forEach(animateStat);
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        animateStat(entry.target);
        observer.unobserve(entry.target);
      });
    }, {threshold:.55});
    stats.forEach(function (el) { observer.observe(el); });
  }

  function initReveal() {
    // Reveal motion is a homepage enhancement only. Content pages such as Contact
    // must remain visible even if IntersectionObserver is unavailable or misbehaves.
    if (!document.getElementById("proof") || !document.getElementById("scope")) return;

    var nodes = Array.prototype.slice.call(document.querySelectorAll(
      "main > section:not(.hero), .case, .build .item, .process-card"
    ));
    if (!nodes.length || reduce || !("IntersectionObserver" in window)) return;

    var observer;
    try {
      observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      }, {rootMargin:"0px 0px -7% 0px", threshold:.08});
    } catch (e) {
      return;
    }

    nodes.forEach(function (el) {
      el.classList.add("kr-reveal");
      observer.observe(el);
    });

    // Fail open: animations must never be able to leave real content invisible.
    window.setTimeout(function () {
      nodes.forEach(function (el) { el.classList.add("is-visible"); });
    }, 1600);
  }

  function start() {
    addProcessAndMarquee();
    initCounts();
    initReveal();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, {once:true});
  } else {
    start();
  }
})();
