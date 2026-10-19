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

## 1.3.2 (5 Oct 2026): link preview + meta description
Live PageSpeed (1.3.1) flagged "Document does not have a meta description", and the link-preview picture had stopped showing.
The theme's SEO module outputs both, but it switches itself off when an SEO plugin (Yoast / Rank Math / All in One SEO) is active.
If that plugin has no description or image set, the page ends up with neither.
- New gap-fill (end of `partials/seo.php`): with one of those plugins active, the theme supplies the description and the social card
  (`social-card-business-systems-2026.png`, 1200×630) only where the plugin left them empty. It never overrides plugin values.
- Search descriptions and the Organization schema reworded to lead with Odoo (diplomatic positioning).

## 1.3.3 (5 Oct 2026): Agentic Browsing 3/3
Live PageSpeed after 1.3.2: mobile 88, desktop 96, Agentic Browsing 2/3. The failing check, "Accessibility tree is not well-formed",
was a single empty link in the Complianz cookie banner (`a.cmplz-link.cookie-statement` with no text, because no Cookie Policy
document is assigned in Complianz).
- `main.js` hides consent-banner document links that have no text, and shows them again if the plugin fills the text in later.
  The proper fix is still to generate the Cookie Policy in Complianz (Wizard → Documents).
- New `/llms.txt` (llmstxt.org): a Markdown guide to the site for AI agents, built from the page meta map
  (published pages only, plus the latest 10 posts). Lighthouse audits it once it exists (needs an H1, links, and at least 50 characters).
Tested locally: axe (link-name, heading-order, landmark-one-main) reports no violations with a mocked Complianz banner; llms.txt renders.

## 1.3.4 (5 Oct 2026)
After 1.3.3, the client reported mobile 78 and Agentic Browsing still 2/3. The Cookie Policy was already generated by Complianz.
- CSS now hides an empty consent-banner document link from first paint (`a.cmplz-link:empty`), independent of JS timing.
  Verified with axe with `main.js` blocked: no link-name violation.
- The live report still has to confirm which agentic check fails and whether 1.3.3/1.3.4 is actually being served (cache).

## 1.4.0 (17 Oct 2026): contact form redesign (taste-skill pass)
Client: Google Ads are running but no one fills the form; the page felt dark and uninviting. Built on the client's live 1.3.4
(which had their own `tolx_name` field fix and SMTP lead mail; synced into the repo with the SMTP password removed).
- **The form is in the first screen,** on a light panel (#F4F4F5) beside a large headline: "Tell us what's hard to track."
  The old hero, "What to expect" strip and five contact cards are gone; their content moved into "What happens next"
  (a real ordered list) and "Rather talk now?" (WhatsApp, phone, email) under the headline, plus the Odoo Ready Partner badge.
- **Shorter and friendlier:** topic chips ("What should we look at first?", multi-select) replace the dropdown; only name and email
  are required; company, phone and message are marked optional; "How did you hear about us?" was removed (the ad source is now
  captured automatically). The button reads "Request my discovery call". Readable sentence-case labels, 17px inputs, 52px+ tap targets.
- **Inline validation** for name and email, one submit only ("Sending…"), and values and chips are kept after a server error.
  After a failed send, the page scrolls to the form (clear of the fixed nav).
- **Ad attribution:** `main.js` stores utm_* / gclid / gbraid / wbraid from the landing URL for 30 days (this browser only).
  The enquiry carries them in a hidden `tracking` field and sets `source` = `google-ads` for paid Google clicks. The lead email
  shows them as "Came from (ad / campaign)".
- **Conversion event:** a successful enquiry fires GA4 `generate_lead` (via the site's gtag), so it can be imported into Google Ads.
- New topic value `einvoicing` ("Invoicing and e-invoicing"), which ties into the e-invoicing video.
- Taste-skill inspector: the contact page went from 15 FAIL to 7. The remaining 7 come from site-wide brand elements
  (monospace breadcrumbs and footer labels, the gold glow on the nav "Book a Call" button, nav/footer hairlines, no photography),
  kept for consistency with the rest of the site.

**Before uploading 1.4.0:** the theme no longer contains the Gmail app password. Add it to `wp-config.php` first:
`define('TOLX_SMTP_PASS', 'xxxx xxxx xxxx xxxx');` (a NEW app password; the old one was shared in a zip and should be revoked).

## 1.4.1 (17 Oct 2026): form back on brand, highlighted
Client: "it should be on brand but more highlighted" (the light panel read as off-brand).
- The form panel is dark (#131316) with a gold-tinted edge, led by a solid gold header: "Book your discovery call / Takes two
  minutes. We reply within one business day." Picked topic chips turn gold, inputs are dark with a gold focus ring, and the
  button is flat gold.
- Tighter spacing, and the breadcrumb moved into the left column: the whole form including the button fits in the first
  screen at 1440×900 and larger (fields visible but the button just below at 1366×768).
- Email sending (`partials/leads.php`) is unchanged from the live site apart from the password placeholder and the two
  lead-email labels ("Source", "Came from (ad / campaign)").

## 1.4.2 (17 Oct 2026): topic picker
Client: the topic chips "can be better" (ragged pill cloud, "Not sure yet" orphaned).
- Replaced with a grid of equal option tiles: two columns on desktop, one on phones, "Not sure yet" full width. Each tile has a
  gold line icon and a one-line label; when picked, the icon turns into a gold tick box and the tile gets a gold edge and tint.
  The legend now says "Pick any that apply".
- Shorter labels so every tile stays on one line: Orders & follow-ups · Stock & sales · E-invoicing & VAT · Team tasks &
  approvals · Reports & dashboards · Website & marketing · Not sure yet. The lead email shows the same labels.
- The submit button still fits in the first screen at 1440×900.

## 1.4.3 (17 Oct 2026): required privacy consent
Client: the visitor must tick that they agree to the privacy policy, or the form must not send.
- A required tick box above the button: "I agree to the privacy policy and to TOLX contacting me about my enquiry."
  The privacy policy link opens in a new tab, so the form isn't lost.
- Enforced twice: the browser blocks the send and shows "Please tick the box to agree to our privacy policy.", and the server
  refuses any submission without it (so it also holds if JavaScript is off or the form is posted directly).
- The saved enquiry and the lead email record it: "Consent: Agreed to the privacy policy (date and time, UTC)".
- Because of the extra line, the button now sits about 60px below the first screen at 1440×900 (the tick box and all fields are visible).

## 1.4.4 (17 Oct 2026): minimal form, first on the page
Client: "the form [should] be minimalistic but also appear first in the page, the client do not need to scroll to find it".
- Fields cut to: name, work email, phone or WhatsApp (optional), "What should we look at first?" as one compact dropdown
  (optional), the privacy tick box, and the button. The topic tiles, company and message fields were removed.
- On phones and tablets the form now comes first, right under the nav; the headline, next steps and contact options follow it.
  On desktop the form stays at the top right beside the headline.
- Measured (button bottom vs screen height), all visible with no scrolling: 1440×900, 1366×768, 1920×1080, 768×1024,
  390×844 (iPhone), 360×740 (Android), 375×667 (iPhone SE, with tighter spacing on short phones).
- Unchanged: required privacy consent (browser + server), inline validation, values kept after an error, ad attribution, the
  GA4 generate_lead event, and email sending.

## 1.4.5 (17 Oct 2026): caching
Client: the new form only showed in the browser they installed from (logged in); other browsers kept the old page.
That is the page cache: logged-in admins bypass it, visitors get the saved copy.
- Contact and scorecard pages are now never page-cached (`DONOTCACHEPAGE`, LiteSpeed no-cache, no-cache headers). A cached
  form carries an expired security token, so after about a day every visitor's submission failed with "Security check
  failed". This may have cost real enquiries from the ads.
- When a new theme version goes live, the theme clears the page caches once (LiteSpeed, WP Rocket, W3 Total Cache,
  WP Super Cache, Autoptimize). A CDN (Hostinger CDN or Cloudflare) still needs flushing in its own panel.

## 1.4.6 (19 Oct 2026): launch legal check
Audit against the six legal risks in AI-built apps (see `legal-check-2026-10-19.md`).
- Ad attribution is now stored only after marketing consent in Complianz, and erased when consent is withdrawn. Without consent,
  the click id is still used for an enquiry made on the landing page itself, but nothing is stored.
- The enquiry confirmation email names the sender (TOLX, Dubai, United Arab Emirates, tolx.ae).
