# Royal Sports Academy — coach-led redesign

## Product and information architecture

A static, multi-page academy website for families, new karate students and returning practitioners in Mumbai. The primary conversion is a real phone/email conversation with the academy; the Contact form is explicitly an unsent local draft. There is no booking backend, dashboard, payment service or verified timetable.

17 routes are retained (including the legacy `sensei.html` alias). The source route/heading/image audit is `verification/redesign-audit.json`. Original biography, training policies, programme details, team names and archive provenance remain the content source of truth.

## Why the previous template was replaced

The previous build layered site, per-page and simplified themes, with repeated divider rules and conflicting header/hero treatments. Akash Kishor Shinde appeared below the other coaches on the homepage. These are composition and hierarchy problems, not a color-tuning task.

The replacement makes Akash **Founder & Head Coach**, with the largest person image and his name in the opening headline. Secondary coaches remain in a later supporting-team section. Generic stock-instructor presentation must not displace him.

## Surface and composition

Primary surface: Decide / Learn. Archives are Explore; Contact is Configure.

- Solid cream navigation, consistently legible on every route.
- Midnight-blue split hero: meaningful copy left, full-frame head-coach portrait right. No text overlay on a crowded training photograph, no separating decorative rules.
- Interactive programme selector with one shared, real-photo panel.
- Community/centres editorial split, supporting coaches, seasonal camps and FAQs.
- Inner-page compositions use reading columns, photo stages, section navigation and browsable archives instead of endless identical cards.
- Content separation comes from space and surface changes. Fine separators may be used for header/footer structure; repeated section rules are avoided. Fields and selected controls retain visible boundaries.

## Tokens

| Role | Value |
|---|---|
| Ink / navy | `#142b3c` |
| Paper / cream | `#f6f3ed` |
| Surface | `#ffffff` |
| Muted text | `#526372` |
| Link / deep teal | `#244e58` |
| Action / gold | `#e2b86b` with navy text |
| Functional border | `#c7ced1` |
| Major radius | `12px` |
| Section rhythm | `clamp(48px,6vw,80px)` |
| Content width | `1240px` maximum |

Typography: locally hosted variable Manrope, with Nirmala UI fallback for the supplied Marathi coach name. Sentence-case headings, strong weight, comfortable line height. Body 17px desktop / 16px mobile. No condensed uppercase display slogans.

## Implementation

`tools/build.py` remains the canonical builder. It calls the content modules, the heading-copy formatter, the inner-layout adapter (`tools/royal_inner.py`) and shared shell (`tools/royal_shell.py`). Homepage composition lives in `tools/home_content.py`.

Only `royal.css` and `royal-pages.css` are loaded. Legacy styles are not a dependency. Standalone Contact/Home refresh commands use the canonical pipeline so they cannot silently restore rejected layouts.

`site.js` owns menu, tab and stock gallery interactions. Archive-specific readers and the safe Contact draft script are retained. Removed enrollment routes do not return.

## Photography and factual boundaries

Supplied photographs remain full frame using contain, not head/face crops. Biography name is Akash Kishor Shinde; supplied direct-contact display spelling is retained separately. Children receive neutral descriptive alt text.

Regular karate training is free. Centres are Ganesh Vidyamandir School, Dharavi, and Pratiksha Nagar, Mumbai. No invented schedules, ranks, medal counts, testimonials or partnerships. Padma Awards 2023 nomination wording is not upgraded to receipt of an award. Archive inclusion is not independent authentication.

Phone/email stay on Contact and footer. Facebook/Instagram are icon links in footer; no Justdial or duplicated social rows in Contact main.

## Responsive and interaction contract

Mobile: stacked composition, readable headings, 44px-or-larger main controls, modal navigation with focus restoration. No fixed action bar obscures content. Full keyboard tab operation; Escape closes menus and viewers. Native details retain no-JavaScript FAQ access. Reduced-motion preference is respected.

Contact remains disabled if JavaScript fails. Review/download actions do not send a message, persist browser data or reserve a place. User strings are rendered as text.

## Verification evidence

Run `python tools/build.py`, `python tools/verify_redesign.py`, `python tools/accessibility.py`, `python tools/package.py` and the unittest suite. `verification/report.json` and `verification/accessibility.json` record actual outcomes; this document does not substitute for those reports. Final ZIP is tested after extraction under file://, so the site also opens without a development server.
