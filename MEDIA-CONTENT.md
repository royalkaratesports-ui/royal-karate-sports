# Media & Press

## Source inventory
26 owner-supplied JPEG files were inventoried from the exact filenames in tools/media-inputs.json. SHA-256 of decoded, orientation-corrected pixels identifies 23 unique images and 3 duplicate copies. The duplicate groups and original filenames are retained in tools/media-manifest.json. The site renders each unique item once.

Original JPEGs in assets/press are copied byte-for-byte, with SHA-256 verification. Derived WebP thumbnails retain the full frame; the original files remain available in the reader and through Open original. No scan is cropped, rewritten or digitally reconstructed. Some text is limited by source quality.

## Content and claims
Page prose supplied by the owner covers free training, sporting achievements, community work, academy activity and recognition. The scans are documentary material supplied for display, not independent authentication of recognition claims or institutional status. The named Indian Sports Award 2019 and Bharat Bhushan Samman 2022 remain owner-supplied recognition descriptions. Do not conflate similarly named organizational recognitions with Government of India national sports honours.

Padma Awards 2023 is explicitly a nomination record, NOT receipt of a Padma Award. The Ministry nomination list is not among these scans and has not been independently checked in this implementation. No new dates, medal counts, titles, identities or government endorsements are inferred from faces or layouts. Publication names in captions are descriptive, not endorsement logos.

## Design and interaction
Primary surface: Explore. Preserve Royal's ink/warm-paper/vermilion identity, Barlow Condensed and Manrope, with an editorial introduction, featured clipping, archive-first gallery, ruled story sections and explicit nomination note. Categories follow actual supplied document types: press coverage and letters/records. No empty certificate, event or video filter is displayed. Three columns on desktop, two on tablet and one on mobile. No carousel or animated decoration hides documents.

The native-dialog reader supports previous/next, arrow keys, Escape, full-frame fit, zoom and Open original. Focus returns to the opener. Scans remain directly accessible as image links if JavaScript is disabled. The media reader is separate from the existing stock-photo lightbox; no stock disclaimer is applied to real scans. Gallery counts come from the actual inventory and filters.

Ten-tell audit: 0/10. No tech gradients, decorative statistics, glassmorphism, generic icon feature tiles or all-centred composition. The archive grid is the appropriate Explore layout, not a marketing feature grid.

## Editing and packaging
Edit tools/media_content.py, tools/media-labels.json, media.css and media.js. Build via tools/build.py. tools/media_assets.py reprocesses original attachments when available at the owner's supplied local path; packaging includes every original, thumbnail, manifest and source module. Runtime makes no remote request.

Before public launch retain publication/photo permissions, confirm any desired precise dates/transcriptions, and obtain the Ministry nomination source if that claim is to be independently linked. User-facing originals may contain names/signatures; review publication rights before deployment. No hosting or live-enrollment change has been made.
