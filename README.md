# KIANIRAD Web Design & Development

Personal portfolio website rebuilt as a plain HTML/CSS/JS multi-page site (Vite),
matching the design of the previous Wix version
(https://ahkr19003.wixsite.com/kiani-development/).

## Pages

| File                | Page                                   |
|---------------------|----------------------------------------|
| `index.html`        | Home — hero + "Inspiring Design" gallery |
| `plans-pricing.html`| Plans & Pricing — Basic / Pro / Exclusive |
| `projects.html`     | Recent Projects                        |
| `about.html`        | About (BIO)                            |
| `contact.html`      | Contact + form                         |
| `consultancy.html`  | Consultancy + appointment form         |

Shared assets: `styles.css`, `script.js`, images in `public/images/`.

## Run locally

```bash
npm install
npm run dev        # http://localhost:5173
```

## Build & deploy

```bash
npm run build      # outputs static files to dist/
```

Upload the **contents of `dist/`** to your web server document root.
(A ready-made `dist/` is included — you can upload it directly without building.)

## Notes

- **Buy Now buttons** link to the Contact page (no payment provider wired up).
- **Contact / appointment forms** use the free [FormSubmit](https://formsubmit.co)
  service and send to `kianirad2020@gmail.com`. The first submission triggers a
  one-time activation email from FormSubmit — click the confirmation link in it
  once, and the forms will work from then on. No server-side code needed.
- The footer year updates automatically via `script.js`.
- Fonts: [Jost](https://fonts.google.com/specimen/Jost) (Google Fonts, headings)
  + Helvetica/Arial (body), matching the Wix look.
