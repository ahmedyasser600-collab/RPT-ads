# TOLX website theme (WordPress)

`tolx/` is the TOLX WordPress theme. The client supplied version 1.2.0 (5 Oct 2026); every later change is in git history.
To install, zip the `tolx/` folder and upload it under Appearance → Themes. Pages and posts live in WordPress, not in this folder.

## 1.3.0 (5 Oct 2026): futuristic polish + UX fixes
Same brand: black and gold, Chakra Petch / Share Tech Mono, the same logo, page structure and content.
Most of the visual work is one block at the end of `style.css` ("V3 — FUTURE LAYER").

**Look**
- Home hero: drifting gold aurora, animated perspective grid floor with a glowing horizon, rising gold particles.
- Hero "Operations Layer" panel: rotating gold edge, slow scan sweep, a data packet moving from Discovery to Go Live.
- Cards: cursor-follow gold spotlight, HUD corner marks, glow edge and lift on hover (mouse only, not touch).
- Glass nav with a glowing hairline once scrolled, gold underline on hover, gold scroll-progress line at the top.
- Gold-gradient buttons with a light sweep; glass ghost buttons; gold-gradient accent words in headlines.
- Faint grid floor and a stronger glow on inner page heroes; glowing seams between sections; blur-in reveals.
- All motion stops for visitors with "reduce motion" turned on.

**UX**
- Secondary text `#71717A` → `#A1A1AA` (4.1:1 → 7.8:1 contrast, passes WCAG AA).
- Mobile type: body copy 15–16px (was 12–13px), labels 10.5px (was 9px), bigger footer tap targets.
- Preloader shows only on the first page view of a session and clears after ~0.45 s (it used to wait for every image plus 0.8 s, up to 3 s).
- Hero: "Book a Discovery Call" is now the main button, plus a "Prefer WhatsApp?" link. Floating WhatsApp button on every page except Contact (which has its own).
- The flip word no longer leaves a blank gap between words.
- Tighter section spacing.
- Fixed sideways scrolling on phones (fleet page and any page with an image placeholder).

**Positioning: Odoo-first** (client, 5 Oct 2026: "we are Odoo partner so we wanna implement Odoo, but we also can implement other
solutions if Odoo doesn't fit"). Copy updated on the home hero, the home Odoo section ("Odoo first. The right fit, always."), the CTA block,
the footer, About, Odoo Partnership ("Odoo-first, never Odoo-only.") and the Odoo implementation SEO description.

Install: upload `dist/tolx-theme-1.3.0.zip` under Appearance → Themes → Add New → Upload, then activate. Pages, posts and Customizer images are kept.
Checked locally with a WordPress stub: every page template renders without PHP errors, there is no sideways scroll at 390px, and there are no JS errors.
Not checked: the live site with real images and plugins. Please look over the site after installing.

### Positioning copy, revised (5 Oct 2026)
Client: "we are Odoo partner, we do not rub it in their face that we are not Odoo only, need to be more diplomatic."
Headlines and the hero now just lead with Odoo ("Built on Odoo. *Implemented around your business.*", "Odoo, implemented around
how you work."). Alternatives are no longer mentioned in headlines, the hero, the CTA or the footer. The home Odoo section keeps
one soft line: "our advice always starts from what your operation needs". The original advisory paragraphs on the Odoo guide
pages (when Odoo isn't a fit) are unchanged from 1.2.0.

## 1.3.1 (5 Oct 2026): speed + accessibility
Live PageSpeed before this (1.3.0, mobile): Performance 77 (FCP 3.4 s, LCP 4.3 s), Accessibility 95, SEO 92. Desktop 95.
- **Fonts self-hosted** (`tolx/assets/fonts`, woff2, OFL licence included). Removes the render-blocking Google Fonts
  stylesheet plus two extra connections. The weights the hero needs (300, 700) are preloaded, with `font-display: swap`.
- **Preloader removed.** It covered the page on every first visit, which is exactly what PageSpeed measures.
- **The hero paints immediately.** Its text no longer waits for JavaScript to fade in (the hero paragraph is the mobile LCP element).
  The operations panel animates in with pure CSS.
- **Minified CSS:** `style.min.css` (58 KB vs 85 KB) is served automatically, but only when it is newer than `style.css`.
  After editing `style.css`, run `./build.sh`; until then WordPress falls back to `style.css`, so nothing breaks.
- `main.js` is deferred. The hero headline's width measurement now runs after load. Hero animations pause when the hero is off screen.
  The aurora's blur filter was removed (expensive to repaint).
- Accessibility: a `<main>` landmark, a skip link, and heading order fixed (card and footer titles changed from h4 to h3, same styling).
Local Lighthouse (mobile, Moto G emulation, no plugins): Performance 95 → 96, FCP 2.4 → 2.0 s, Accessibility 96 → 100.
The live score also depends on hosting and plugins. See the delivery notes for page caching and the cookie banner.
