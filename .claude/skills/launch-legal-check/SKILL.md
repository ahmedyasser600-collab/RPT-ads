---
name: launch-legal-check
description: Pre-launch legal and privacy review for websites, landing pages, web forms and apps. Use whenever you build, change or ship a site, page, form, sign-up, checkout, email template or tracking/analytics code, before reporting the work as done, and whenever the user asks whether a site is compliant, GDPR/PDPL-safe or ready to launch. Covers age gates (COPPA), externally hosted fonts, session replay, marketing email (CAN-SPAM), subscription renewal disclosure, user uploads (DMCA), cookie/storage consent, form consent, privacy policy and secrets in code.
---

# Launch legal check

1. Read `docs/website-launch-legal-checklist.md` in this repo; it is the checklist.
2. Inspect the real code, and where possible the rendered page (its network requests and storage), for every row. Use grep for
   font hosts, tracker names, `localStorage`/`document.cookie`, sign-up or upload handlers, mail functions and checkout code.
   Look in theme/app code and note which plugins or tag managers could add more.
3. Fix what is in your scope (self-host fonts, gate storage on consent, require the form consent tick box, remove secrets).
   Test each fix.
4. Write `legal-check-YYYY-MM-DD.md` next to the project: status plus evidence per row, fixes made, and open items.
5. In your reply, give the user the open items in plain words. Say clearly that this is a technical review, not legal advice,
   and name anything that needs a lawyer.

Never claim a row passes without having checked it. If something can only be checked on the live site (plugins, a CDN,
tag-manager tags) and you cannot reach it, mark it Open and tell the user how to check it.
