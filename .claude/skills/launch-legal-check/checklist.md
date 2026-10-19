# Website and app launch checklist: legal and privacy

Run this before shipping any website, landing page, form or app, and again after big changes. It comes from
the six legal risks in AI-built apps (video notes by @adilet.fndr, https://www.instagram.com/p/DdyqycEINNe/) plus the privacy points we hit on real projects.

**This is a technical review, not legal advice.** Laws differ by country (UAE PDPL, EU GDPR, US federal and state rules).
Mark anything uncertain for the client's lawyer.

For each item, record **Done / Fixed / Not applicable (and why) / Open**, with evidence (file and line, or what you tested).

## The six risks from the notes

| # | Area | Check | Typical fix |
| --- | --- | --- | --- |
| 1 | Children's privacy (COPPA, under 13) | Does the site have sign-up or accounts, or target children? | Age gate on sign-up; state the audience in the privacy policy |
| 2 | Externally hosted fonts | Does any font load from Google Fonts, Typekit or another CDN? Check the theme AND plugins, in the rendered page's network requests. | Self-host the fonts (woff2 in the project); remove the third-party font links |
| 3 | Session replay | Is Hotjar, Microsoft Clarity, FullStory, LogRocket, Smartlook or Mouseflow installed (theme, plugin, tag manager)? | Remove it, or load it only after consent, with input masking on every field |
| 4 | Marketing email (CAN-SPAM and similar) | Which emails does the site send? Transactional (reply to a request) or marketing (newsletter, promotions)? | Marketing: unsubscribe link plus the sender's postal address, separate opt-in. Transactional: sender identified |
| 5 | Subscription renewals | Is there a checkout with recurring billing? | Renewal terms, price and cancellation shown next to the subscribe button |
| 6 | User uploads and copyright (DMCA) | Can users upload files, post comments or submit content? | Takedown process and contact; a DMCA agent if the service is US-facing |

## Also check on every build

| Area | Check |
| --- | --- |
| Cookie and storage consent | No analytics, ads or attribution identifiers stored (cookies, localStorage) before the visitor consents through the cookie banner |
| Forms | A required privacy-policy consent tick box, enforced on the server too; a privacy policy link that opens in a new tab; only the fields you need |
| Privacy policy | Exists, is linked in the footer and on forms, and names what is collected and why |
| Secrets | No passwords, API keys or app passwords in theme or repo files; put them in server config (e.g. `wp-config.php`) |
| Claims | No invented testimonials, client logos, results or prices on the page |

## How to report

Write a short report next to the project, named `legal-check-YYYY-MM-DD.md`: the table above with a status and evidence per
row, what was fixed, and what is open or needs a lawyer.
