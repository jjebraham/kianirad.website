# Kianirad.website

Business portfolio for Hadi Kianirad, built as a lightweight multi-page static HTML/CSS/JavaScript site.

## Production architecture

There is **no production build step** and no application server. The source HTML, `assets/`, images and root metadata files are deployed directly to the web root and served by Nginx behind Cloudflare.

Production URL: `https://www.kianirad.website/`

The apex host should redirect permanently to `www`.

## Pages

- `index.html` — home, services, proof, interactive bot demo and project estimator
- `projects.html` — selected live projects
- `consultancy.html` — consultancy offering, process and FAQ
- `about.html` — background and working style
- `contact.html` — Telegram, email, GitHub and enquiry form
- `plans-pricing.html` — redirects to the estimator on the home page and should remain `noindex`

Shared front-end assets live in:

- `assets/site.css`
- `assets/site.js`

`assets/site.js` is the single source of truth for contact details, prices, language switching, theme switching and shared navigation/footer strings.

## Contact configuration

Current contact configuration in `assets/site.js`:

- Email: `kianirad2020@gmail.com`
- Telegram: `@amirkiaaani`
- GitHub: `jjebraham`

The contact form falls back to a pre-filled email while `formEndpoint` is blank. Do not put secrets in this repository.

## Local preview

Any simple static HTTP server is sufficient, for example:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

## Deploy

Pull the repository, then copy the static site files directly to the configured Nginx document root. Do **not** run `npm install` or `npm run build` for production deployment.

After deploying:

1. Purge the Cloudflare cache.
2. Check EN, TR and FA in a private window.
3. Check light and dark themes.
4. Confirm Persian switches the page to RTL.
5. Confirm the browser console is free of errors.
6. Confirm `/assets/site.js`, `/favicon.ico`, `/og-image.png`, `/robots.txt` and `/sitemap.xml` return HTTP 200.
7. Confirm the apex host redirects to `https://www.kianirad.website/` with HTTP 301.
