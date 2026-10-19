# Video notes: Six legal risks in AI-built apps

- **Creator:** @adilet.fndr
- **Source:** https://www.instagram.com/p/DdyqycEINNe/
- **Notes prepared:** 19 October 2026
- **Coverage:** Summary of the video's accompanying Instagram caption. Audio was not transcribed; these are not timestamped or verbatim video notes.

## Main idea

The creator argues that an app can face legal exposure before it earns revenue. The post highlights six areas that developers may overlook when building quickly with AI, and suggests using a coding assistant to inspect them.

## The six points

| Area | Risk described by the creator | Fix proposed in the post |
| --- | --- | --- |
| Children's privacy | Signup without age checks may expose an app to COPPA issues involving children under 13. | Add an age gate to signup. |
| Externally hosted fonts | Loading Google Fonts from Google's servers sends visitor IP addresses to a third party; the post cites a Munich GDPR case. | Self-host fonts. |
| Session replay | Recording interactions and keystrokes may create privacy or wiretapping issues, with California's CIPA cited. | Disable session replay, or add consent and input masking. |
| Marketing email | Launch emails without an unsubscribe mechanism or postal address may create CAN-SPAM issues. | Include an unsubscribe link and postal address in marketing emails. |
| Subscription renewals | Poorly disclosed renewal terms at checkout may create problems under California subscription rules. | Display renewal terms next to the subscription button. |
| User-uploaded content | The creator links the absence of a registered DMCA agent to losing safe-harbor protection for user uploads. | Review DMCA agent registration. |

## Monetary examples mentioned

These are **unverified claims from the caption**, recorded for completeness rather than confirmed penalty guidance:

- COPPA: up to approximately **$53,000 per child under 13**.
- Google Fonts: **€100 awarded to one visitor** in the cited Munich case.
- CIPA/session replay: **$5,000 per session**.
- CAN-SPAM: up to approximately **$53,000 per email**.
- California subscription renewals: the creator says improperly disclosed renewals can be treated as gifts requiring refunds.
- DMCA: the creator mentions a **$6 registration fee** and copyright exposure of up to **$150,000 per image**.

The rhetorical emphasis is on repeated exposure: per visitor, session, email, or item of content.

## Suggested AI workflow — paraphrased from the caption

Ask a coding assistant to review the app's signup age checks, external font loading, session recording, marketing email templates, subscription disclosures, and DMCA agent registration needs. The creator proposes using the assistant to make technical changes and explain the registration process.

## Takeaway

Treat these six areas as prompts for a pre-launch review. The caption mixes different jurisdictions and simplifies legal requirements; it does not establish that every listed rule or monetary amount applies to every app. The creator also recommends consulting a lawyer about the specific situation. An AI-generated code change alone is not proof of legal compliance.

## Review checklist derived from the post

- [ ] Examine signup and the intended age range of users.
- [ ] Check whether fonts load from third-party servers.
- [ ] Identify session-replay tools and what they record.
- [ ] Inspect marketing emails for unsubscribe and sender-address details.
- [ ] Check the placement and clarity of subscription renewal information.
- [ ] Determine whether the app accepts user uploads and review its copyright process.

*These notes summarize the source; no independent legal fact-check was performed.*
