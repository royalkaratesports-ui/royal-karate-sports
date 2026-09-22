# Events & Camps — supplied content and imagery

## Page and facts

`events.html` replaces the earlier Events placeholder and is linked through Trending → Events on desktop/mobile and the shared footer. `tools/events_content.py` generates the page; `events.css` and `events.js` supply styling and the dedicated original-photo viewer.

The owner supplied the following camp information: camps twice yearly, Summer Karate Camp and Winter Karate Camp, belt grading, sparring/kata competitions, trophies/medals/certificates, practical self-defense, personal growth/discipline, and enrollment opening a month before each season. These are owner-supplied descriptions, not independently audited operations.

No exact camp dates, travel itinerary, venue, age limits, duration, fee or current enrollment status was provided. No dates or availability are invented. The camp enquiry points to the existing Contact page; this is a local frontend preview, not live registration. Existing free regular-karate-training wording is retained without making unsupported claims about camp arrangements.

The universal protection claim has been edited to practical awareness, avoidance, appropriate responses and seeking help; no guarantee of safety in every situation is made. Belt advancement is described as assessment-based, not automatic. Camp grading does not replace the previously supplied regular Kids/Adult Batches grading intervals.

## Photography

8 exact user-named files were inventoried in `tools/events-inputs.json`, with per-file acquisition hashes in `tools/events-manifest.json`. All 8 originals are retained byte-for-byte under `assets/events/originals/`. Seven unique full-frame WebP display copies are bundled.

`88371b85-bc79-428c-a92b-99ae3338219c.jpg` and `f304aa50-489d-46d8-a0cf-82d5b89b6604.jpg` have identical decoded pixels and share one displayed gallery item. Other similar views are retained rather than assumed identical. Gallery counts represent photographs, not events, seasons or participants.

Captions describe visible group gatherings, certificates, medals and presentations. No participant is identified from a face, and no photo is attributed to a summer/winter camp or specific date without evidence. No stock photography is used in the Events page body. Low-resolution archive photos retain their source quality; no generative enhancement, crop or invented detail was applied.

## Design and verification

Primary surface: Decide/Learn. A photo-led camp introduction, paired seasonal descriptions, native activity accordions, full-frame gallery and practical enrollment information extend the existing cream/carbon/vermilion brand. The initial copy audit flagged repeated paired slogans; gallery, season and enrollment headings were replaced with direct labels. Ten-point visual anti-slop score after review: 0/10; no tech gradients, icon tiles, decorative stats or centered stack. The photo gallery grid is appropriate for browsing real supplied images.

Tests cover exact inventory, owner-supplied content, all seven original images, keyboard photo navigation, accordion expansion, enquiry route and extracted ZIP navigation. `tools/verify_events.py` checks seven responsive widths, uncropped image ratios, viewer control visibility, no-JavaScript original access, external requests, page errors and axe WCAG A/AA states. Automated checks are not a full accessibility audit. Screenshots are in `verification/events-*.png`.
