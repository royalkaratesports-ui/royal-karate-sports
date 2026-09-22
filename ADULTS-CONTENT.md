# Adult Batches

## Content
Owner supplied: advanced Shotokan, basic-to-extreme fitness, six-month belt gradation exams, weight-loss/weight-gain CrossFit workouts, karate meditation and street-fighting/self-defence training; five fitness/lifestyle benefits. These replace the previous generic adult placeholder.

Copy clarifies rather than guarantees results: conditioning intensity is adapted; body-composition goals depend on nutrition and recovery; mental composure is not medical treatment; street-fighting content is presented as street safety, de-escalation, escape and responsible self-defence. CrossFit-style describes functional conditioning, not a claim of official affiliation. No belt promotion, weight result or competition result is guaranteed. No times, prices, ranks or qualifications invented. Regular training remains free under supplied academy policy, with adult availability per centre requiring confirmation.

## Photographs
Five owner-supplied photos are preserved full-frame and optimized as WebP. Exact attachment names and dimensions are recorded by the asset provenance pipeline and in tools/test_adults.py. Three small JPGs are displayed as a mixed-age academy archive, not as evidence of adult-only classes or specific tournament results. The two larger attached PNGs supply the hero and practice photo. Do not identify people from photographs. Retain permission from participants/guardians before public launch.

## Design
Primary surface: Decide/Learn. Royal's ink/paper/vermilion palette, Barlow Condensed headings and Manrope body type remain unchanged. Distinct adult layout: dark editorial headline and enquiry beside it, full-width uncropped training photo, ruled curriculum, six-month grading band, benefits/practice photo, asymmetrical academy archive and useful FAQs. Mobile is single-column with the existing navigation and sticky trial shortcut. Ten-tell audit: 0/10; no feature tile grid, fake metrics, gradients or decorative icons.

## Build and verification
Edit tools/adults_content.py and adults.css; rebuild with tools/build.py. tools/test_adults.py checks supplied features, benefits, five photographs at four viewport widths, belt-exam FAQ and adult enquiry preselection. Existing regression tests and viewport/accessibility checks cover the rest of the site. ZIP extraction smoke test verifies the adult page's assets, CSS and enquiry path. Frontend-only enquiry prepares a local draft; no booking is sent. No deployment changes.
