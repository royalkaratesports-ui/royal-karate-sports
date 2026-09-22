# Inner-page audit and redesign

## Integration

Public entry point: `tools/royal_inner.py::adapt_page(name: str, body: str) -> str`.

```python
from royal_inner import adapt_page
body = adapt_page(name, simplify_content(name, body))
# Pass body to the parent's shared shell.
```

- `index.html` returns the original input byte-for-byte. Unknown routes are also unchanged.
- All 16 inner routes are exported in `INNER_ROUTES`, including `sensei.html`.
- The transform is idempotent via `.r-content[data-r-adapted]`.
- No filesystem writes, builder execution or asset generation occur inside the transform.
- Parent shell: `body.royal-design.r-page` plus original page-kind class; load `royal.css` then `royal-pages.css`, and no previous stylesheets.
- Keep `site.js` and the existing global gallery `.lightbox` shell. Route-specific scripts remain in the transformed fragment.
- Base assumptions verified against the parent's actual `royal.css`: Manrope/font face, provided colour/spacing tokens, `.wrap`, `.section`, headings, buttons, `.text-link`, `.icon-button`, `.faq-list` / `.contact-answers`, inputs, header/footer and the gallery lightbox.
- All inner CSS is `.r-page`-scoped. No legacy theme dependency or decorative section rules. Actual input/filter/reader control boundaries remain.

## What was audited

Read `verification/redesign-audit.json`, the complete inner content modules, shared builder/category module, heading simplifier, coaches manifest/content, current rendered inner mains, old page styles, base/theme styles, and `site.js`, `contact.js`, `media.js`, `achievements.js`, `events.js`.

The original pages repeated long divider-lined splits; the instructor page still used a stock instructor while real coach assets existed; Akash's Contact photograph was a small thumbnail. Archive views depended on CSS that would disappear when legacy styles were removed.

## Route-by-route result

| Route | New composition |
| --- | --- |
| `about-akash-shinde.html` | Large full-frame portrait beside joined biography; Founder & Head Coach above the name; mission statement and card-based recognition/values. |
| `sensei.html` | Same full profile transformation and preserved alias route. |
| `academy.html` | Real group photograph moved into opening; philosophy becomes a separate reading spread; substantial founder/head-coach feature promoted before the academy story. |
| `instructors.html` | Real Akash lead portrait and name first, coaching approach beside it, then three secondary coach cards from the manifest. |
| `kids-batches.html` | Clear opening, at-a-glance cards, visible curriculum grid, separate assessment note, benefits and parent guide. |
| `adult-batches.html` | Intro and academy practice photo composed together; curriculum cards, assessment section, qualified benefits and full-frame archive strip. |
| `programs.html` | Four anchored programme cards in a comparison grid; real academy photographs and detailed programme links; draft/availability caveat visible before selection. |
| `seminars.html` | Proposed-offering caveat promoted to opening beside explicitly non-seminar academy photograph; scope cards below. |
| `competition.html` | Real training-led opening; kata/kumite groups; archive image and confirmation caveat together, with link to actual supplied achievements. |
| `locations.html` | Real archive photograph explicitly does not identify a venue; two named centre cards, separate confirmation/accessibility/timetable information. |
| `contact.html` | Full-sized Akash identity/portrait in opening; direct phone/email section ahead of centres and local draft form. |
| `media.html` | Scan-led opening, reading jumps, context/caveats before all 23 archive items, complete filter/reader/zoom CSS. |
| `achievements.html` | Document-led opening, context before all 20 records, consistent scan cards and keyboard/zoom reader. |
| `events.html` | Clear season cards, activity accordions, full-frame 7-photo collection with source caveat first, enrollment confirmation panel. |
| `gallery.html` | Stock-image disclaimer before filtering; all 9 illustrative items retained; working shared lightbox. |
| `information.html` | Six independently navigable reading chapters; typography/photography statements updated for this actual redesign. |

Every inner route now has a breadcrumb and small in-page navigation. Existing IDs and links are retained, with stable additional section IDs only where missing.

## Factual and interaction preservation

- Regular training stays free. No paid classes or training fees introduced.
- Only Ganesh Vidyamandir School, Dharavi and Pratiksha Nagar, Mumbai are described as centres. Reused archive photos do not infer venue identity, age-specific batch identity, competition results or seminar history.
- Nomination-not-award cautions remain in academy and media content. No additional dates, ranks, awards or medal counts were created.
- All three secondary coach names remain exactly as in the manifest. Sahil's existing **original** asset is used because the manifest's display derivative has a crop; no source asset was changed.
- Akash is explicitly Founder & Head Coach on profile, academy, instructors and Contact.
- Contact phone/email hrefs and visible text are retained exactly. No Contact Facebook/Instagram/Justdial rows were added.
- Contact form, field attributes, disabled-without-JS state, review section, IDs, and script are unchanged. Draft `<pre>` has bounded scrolling and wraps at 320px.
- All original interaction `data-*` attributes and original link multiplicities survive the transform. All original IDs survive and no duplicate IDs are introduced.
- All archive items remain: 23 media + 20 achievements + 7 event photos + 9 illustrative gallery photos = 59 collection items. Featured duplicates outside collections remain unchanged.
- Archive reader selectors, `hidden`, `is-zoomed`, `locked`, `aria-pressed`, previous/next, original links, close controls and focus-return behavior are supported.
- The media reader's scroll region additionally becomes keyboard-focusable, like the existing achievement reader.
- Obsolete stock-photo and future-achievement-archive statements were updated where the corresponding content was actually replaced. Other factual copy remains in the document rather than being hidden or discarded.

## TDD and verification

1. Wrote profile transform test first; observed `FAIL: Missing inner-page transformer`.
2. Implemented profile tracer; observed pass.
3. Added all-route composition contracts; observed 18 missing-composition/real-coach/image failures; implemented remaining routes; passed.
4. Added standalone stylesheet contract; observed missing-stylesheet failure; implemented stylesheet; passed.
5. Real browser tests exposed undersized event activity controls. Reused the parent's FAQ control class; re-tested successfully.
6. Visual inspection exposed an academy intro grid placement issue and concatenated event caption. Added browser regression checks, observed failure, fixed composition CSS and gold-button palette, re-tested.

Latest executed command:

```bash
ROYAL_BROWSER_TEST=1 python -B tools/test_royal_inner.py -v
```

Actual result: **13 tests passed**, `Ran 13 tests in 15.639s`, `OK`.

The browser harness serves transformed HTML and existing real assets/scripts through an in-memory Playwright route; it loads only the actual `royal.css` and `royal-pages.css`. It does not build or alter generated site files.

Verified:

- All 16 routes at 320, 390, 600, 900 and 1440px: 80 responsive checks, no horizontal overflow.
- All inner image sources load; all computed inner image `object-fit` values are `contain`.
- All visible buttons, summaries and in-page jump controls have at least 44px height.
- 32 Axe scans: each route at 390 and 1440px, WCAG 2 A/AA + 2.1 AA tags, zero violations.
- Every media/achievement filter category matches actual visible-item counts.
- Media/achievement modal opening, zoom producing scrollable magnification, next/arrow keys, Escape and focus restoration.
- Event reader arrow navigation and Escape, gallery filters and lightbox.
- Contact query-topic prefilling, validation/review, UNSENT text, real `.txt` download event, edit invalidation, no localStorage, and disabled form controls without JavaScript.
- Homepage byte preservation, repeated-call idempotence, original IDs/links/data attributes, exact form serialization and archive counts.

Optional screenshots:

```bash
ROYAL_BROWSER_TEST=1 ROYAL_SCREENSHOT_DIR='C:/Users/Yantra 12/AppData/Local/Temp/royal-inner-visual' python -B tools/test_royal_inner.py -v
```

Temporary desktop/mobile captures were actually produced and visually inspected for profile, academy, instructors, Contact, programmes, events and media. They live outside the repository. These captures intentionally isolate main content; the parent must verify final integrated header/footer/navigation separately.

## Parent integration follow-up (resolved)

`contact.js` still contains this stale line in the downloaded draft:

> Official phone / WhatsApp and email have not yet been supplied for this preview.

The parent corrected this sentence in contact.js, added a failing regression, then verified the actual downloaded draft contains the supplied phone/email and remains UNSENT. Integrated checks also tightened section spacing, moved direct Contact channels before the portrait on mobile, retained natural image ratios, and moved the profile portrait before the long mobile biography.

## Files owned by this subtask

- `tools/royal_inner.py`
- `royal-pages.css`
- `tools/test_royal_inner.py`
- `verification/inner-audit.md`

No builder, shared shell, source content module, original CSS/JS, generated HTML or asset was modified by this subtask. Full site build, shared-shell integration and release verification remain parent-owned.
