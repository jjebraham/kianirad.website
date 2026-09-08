# Kianirad.website

Personal portfolio for Hadi Kianirad, built as a lightweight multi-page HTML/CSS/JavaScript site with Vite.

## Pages

- `index.html` — home, services, proof, interactive demo and project estimator
- `projects.html` — selected live projects
- `consultancy.html` — consultancy offering and process
- `about.html` — background and working style
- `contact.html` — Telegram, email, GitHub and enquiry form
- `plans-pricing.html` — redirects to the estimator on the home page

Shared front-end assets live in `assets/site.css` and `assets/site.js`.

## Contact configuration

The main contact details are defined once in `assets/site.js`:

- Email: `kianirad2020@gmail.com`
- Telegram: `@amirkiaaani`
- GitHub: `jjebraham`

The contact form currently opens a pre-filled email. A POST endpoint can be added later by setting `formEndpoint` in `assets/site.js`.

## Run locally

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

Vite outputs the production site to `dist/`. Deploy the contents of `dist/` to the server document root.
