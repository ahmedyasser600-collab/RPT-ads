# TOLX website: launch legal check, 19 Oct 2026

Theme 1.4.6, checked against `docs/website-launch-legal-checklist.md` (six risks from
[the video notes](../../docs/notes/video-notes-app-launch-risks.md), plus our standing checks).
I checked the theme code and tested in a local copy. The live site (plugins, CDN, Google tag) could not be reached
from the build environment, so its rows are marked "check live".
**Technical review, not legal advice.**

## The six risks

| # | Area | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Children's privacy / age gate | **Not applicable** | No sign-up or accounts anywhere in the theme. The only forms are the B2B contact form and scorecard (name, work email, company). The audience is businesses, not children. |
| 2 | Externally hosted fonts | **Done** (since 1.3.1) | Chakra Petch and Share Tech Mono are self-hosted in `tolx/assets/fonts/` (woff2); no `fonts.googleapis`/`gstatic` reference in the theme. Live PageSpeed after 1.3.1 showed no Google Fonts requests. **Check live:** that no plugin adds its own Google Fonts. |
| 3 | Session replay | **Done** in the theme | No Hotjar, Clarity, FullStory, LogRocket, Smartlook or Mouseflow code in the theme. **Check live:** Site Kit / Google Tag Manager tags, and the Hostinger `embed.js` (Hostinger Reach) seen in PageSpeed, for any recording tool. |
| 4 | Marketing email | **Done** (transactional only) | The site sends: the team notification, the visitor's enquiry confirmation (with brochure) and the scorecard summary. All are replies to a request, not marketing. Sender identification added to the confirmation (TOLX, Dubai, United Arab Emirates, tolx.ae). The form consent covers "contacting me about my enquiry" only. **If newsletters start** (e.g. Hostinger Reach), they need a separate opt-in, an unsubscribe link and a postal address. |
| 5 | Subscription renewals | **Not applicable** | No checkout, payments or subscriptions on the site. |
| 6 | User uploads / DMCA | **Not applicable** | No file uploads, and no comment template in `single.php`, so no user-posted content. TOLX is UAE-based; a DMCA agent only matters for a US-facing service hosting user content. |

## Standing checks

| Area | Status | Evidence |
| --- | --- | --- |
| Cookie / storage consent | **Fixed in 1.4.6** | The ad attribution added in 1.4.0 saved the Google click id and campaign tags in `localStorage` without consent. It now only stores them after **marketing consent** in Complianz (`cmplz_has_consent('marketing')`), and erases them if consent is withdrawn. Without consent the click id is still used for an enquiry on the landing page itself, without storing anything. Tested: no consent → nothing stored; consent → remembered; withdrawn → erased. **Check live:** the Google tag (Site Kit) follows Complianz consent (Consent Mode). |
| Form consent | **Done** (1.4.3) | Required privacy-policy tick box, enforced in the browser and on the server, stored with a timestamp on each enquiry. |
| Privacy policy | **Done** | `/privacy-policy/` page template exists, linked in the footer and on the form (opens in a new tab). The client should keep it accurate for what the form and analytics collect (UAE PDPL). |
| Secrets | **Fixed** (1.4.0) | The Gmail app password was removed from `partials/leads.php`; it belongs in `wp-config.php`. **Open:** revoke the old app password, which was shared in a zip and in chat. |
| Claims | **Done** | No invented testimonials, client logos, results or prices. |

## Open items for the client
1. Revoke the old Gmail app password and put the new one in `wp-config.php`.
2. On the live site, check plugins and Google Tag Manager for session-replay tools and extra Google Fonts. Confirm what the Hostinger `embed.js` script does, and remove it if it's unused.
3. Confirm in Complianz that the Google tag only fires after statistics/marketing consent.
4. If you start sending newsletters, add an opt-in, an unsubscribe link and your postal address.
