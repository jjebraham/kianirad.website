# Kianirad.website

Business portfolio for Hadi Kianirad, built as a lightweight multi-page static HTML/CSS/JavaScript site.

## Production architecture

There is **no npm/Vite production build step** and no application server for the public site. HTML, `assets/`, images and root metadata files are deployed directly to the Nginx document root behind Cloudflare.

Production URL: `https://www.kianirad.website/`

The apex host must redirect permanently to `www`.

## Public pages

- `index.html` — home, services, proof, interactive bot demo, process and project estimator
- `projects.html` — selected live projects
- `consultancy.html` — consultancy offering, process and FAQ
- `about.html` — background and working style
- `contact.html` — Telegram, email, GitHub and enquiry form
- `privacy.html` — plain-language privacy/KVKK information
- `status.html` — static public status snapshot; populated only with systems approved for public reporting
- `plans-pricing.html` — redirects to the estimator and remains `noindex`
- `tr/klinikler-icin-telegram-botu.html` — Turkish clinic landing page

Static Turkish and Persian copies of the core pages live under `tr/` and `fa/`.

Shared front-end assets:

- `assets/site.css` — base design system
- `assets/site.js` — shared configuration, languages, theme and contact helpers
- `assets/ui-v2.css` — progressive premium visual layer
- `assets/ui-v2.js` — vanilla process section, marquee, count-up and scroll reveals

`assets/site.js` is the single source of truth for contact details, prices, language switching, theme switching and shared navigation/footer strings.

## Contact configuration

Current contact configuration in `assets/site.js`:

- Email: `kianirad2020@gmail.com`
- Telegram: `@amirkiaaani`
- GitHub: `jjebraham`

The contact form falls back to a pre-filled email while `formEndpoint` is blank. The optional Telegram-forwarding FastAPI service is documented under `server/`. Never put its bot token or chat ID in Git.

## Static generation

`build_i18n.py` reads the existing `BASE` dictionary in `assets/site.js` and each page's `PAGE_STRINGS`. It generates baked `/tr/` and `/fa/` pages, self-canonicals and reciprocal `hreflang` tags without hand-copying translations.

`build_seo.py` localizes the generated Turkish/Persian head metadata and builds `FAQPage` JSON-LD directly from the visible Consultancy FAQ.

`build_ui.py` wires the shared UI v2 stylesheet and progressive enhancement script into the public HTML pages.

`build_sitemap.py` rebuilds `sitemap.xml` from the public files that actually exist.

GitHub Actions runs the generation pipeline automatically when source pages, translations, SEO rules or UI assets change and commits generated pages back to `main`.

Manual regeneration is also possible:

```bash
python3 build_i18n.py
python3 build_seo.py
python3 build_ui.py
python3 build_sitemap.py
```

## Local preview

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

## Production deploy

Pull `main`, then sync only public files to the Nginx document root. Do **not** run `npm install` or `npm run build`.

```bash
cd /home/kianirad2020/kianirad.website
git pull --ff-only

sudo rsync -a --delete \
  --exclude='.git/' \
  --exclude='.github/' \
  --exclude='.gitignore' \
  --exclude='README.md' \
  --exclude='server/' \
  --exclude='build_i18n.py' \
  --exclude='build_seo.py' \
  --exclude='build_ui.py' \
  --exclude='build_sitemap.py' \
  --exclude='status.json' \
  ./ /var/www/kianirad-react-dist/

sudo nginx -t && sudo systemctl reload nginx
```

After deploying:

1. Purge Cloudflare cache.
2. Check EN, TR and FA in a private window.
3. Check light and dark themes.
4. Confirm Persian pages are RTL even with JavaScript disabled.
5. Confirm the browser console is free of errors.
6. Confirm `/assets/site.js`, `/assets/ui-v2.css`, `/assets/ui-v2.js`, `/favicon.ico`, `/og-image.png`, `/robots.txt` and `/sitemap.xml` return HTTP 200.
7. Confirm `/tr/` and `/fa/` return HTTP 200.
8. Confirm the apex host redirects to `https://www.kianirad.website/` with HTTP 301.
9. Confirm an unknown URL returns the styled `404.html` with an actual HTTP 404 status.
10. Confirm Turkish/Persian `<title>` and social metadata are localized.
