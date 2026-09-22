# GitHub source and hosting

This is the complete v19 source, including all 17 generated pages, the current CSS and JavaScript, supplied assets, Python generators, provenance manifests and regression tests. It does not include credentials, Python caches, old rejected theme snapshots or scratch screenshots.

## Develop from a fresh download / clone

Run the commands in README.md. All generated pages and required local assets are committed, so no Python installation is needed simply to view or host the site.

## GitHub Pages (optional, not automatically enabled)

A repository upload is not a live website deployment. If the owner approves public hosting and asset rights, open repository **Settings → Pages**, select **Deploy from a branch**, then **main** and **/(root)**. GitHub will show the actual published URL after deployment. A public repository normally supports Pages on the free plan; private-repository Pages availability depends on the account plan. The `.nojekyll` file makes this a plain static site.

Do not set a custom domain until its DNS and ownership are confirmed. No `CNAME` is supplied. Search indexing is intentionally disabled pending production approval.

## Editing

- Shared branding/header/footer: `tools/royal_shell.py`
- Homepage: `tools/home_content.py`
- Inner-page composition: `tools/royal_inner.py`
- Factual page content: the corresponding `tools/*_content.py` modules
- Current styling: `royal.css`, `royal-pages.css`
- Interactions: `site.js`, `contact.js`, `media.js`, `events.js`, `achievements.js`
- Logo source and derivatives: `assets/brand/`; provenance: `tools/logo-manifest.json`

Always rebuild after changing generator content. Earlier theme files are deliberately not part of the current release.

## Asset import utilities

The complete display assets and preserved originals are already included. `tools/*_assets.py` and `tools/assets.py` are optional ingestion utilities, not part of the routine build. Some original ingestion manifests refer to the owner's local attachment filenames or input folders. Do not run them on a new computer without supplying the appropriate source directory. Routine build, tests and hosting use the bundled assets, not those external folders.

## Rights and privacy

This delivery does not grant a blanket open-source license over supplied photographs, people, logos, press clippings or third-party assets. See `ASSETS.md` and the included font licenses. Confirm permissions before changing a private repository to public or enabling public hosting. Contact details are owner-supplied public business contacts. The enquiry form only downloads an **UNSENT** local draft; it has no backend, analytics or stored submissions.
