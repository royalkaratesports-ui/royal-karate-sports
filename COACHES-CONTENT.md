# Coaching team — content and imagery

The website owner supplied three images and confirmed that these are coaches, with their names taken from the filenames:

- `Amar Dabade.webp` → **Amar Dabade**
- `Mayur Dilawar.webp` → **Mayur Dilawar**
- `साहिल हेगडकर.webp` → **साहिल हेगडकर**

The Home section is titled **Your professional coaches**. It uses only the supplied names, photographs and generic Coach role. No biography, belt rank, certificate, years of experience, specialty, achievements, contact details or social profiles have been inferred from appearance or imagery.

All original files are preserved byte-for-byte under `assets/coaches/originals/`. Their acquisition SHA-256 hashes, exact source names and display paths are recorded in `tools/coaches-manifest.json`. Amar and Mayur display copies retain the original WebP bytes. Sahil's display copy removes only the supplied blank white side margins; the full photographic content is retained. All images use `object-fit:contain` and are not cropped to faces or altered by AI.

Placement: Home → programmes → coaching team and founder → seasonal camps → FAQs. The existing founder biography and portrait are retained in a compact block below the coaches.

The team uses actual photographs and plain name captions, not outlined cards, badges or invented social buttons. Mobile shows a readable vertical list. Marathi text is preserved in Unicode with an appropriate local fallback font.

Edit `tools/coaches_content.py` for section markup and `simple.css` for final appearance. Run `tools/coaches_assets.py` only to regenerate display assets from preserved originals. Normal builds do not require the original Pictures/Downloads paths.
