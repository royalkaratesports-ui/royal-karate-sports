# Achievement image content review

Reviewed all 21 supplied images using the three numbered contact sheets, with individual views for documents requiring closer inspection. Captions and alt text are in `tools/achievements-labels.json`, keyed by exact original filename.

## Verified inventory

- 21 source labels: 5 awards, 5 competition, 4 community, 7 moments.
- Images 10 and 18 are byte-identical and decoded-pixel-identical (1125 × 1600). Keep both source records, display one gallery item.
- 20 distinct gallery images: 5 awards, 5 competition, 3 community, 7 moments. These are image counts, not counts of separate achievements or awards.
- PIL upright rotations: image 4 `90`, image 13 `90`, image 14 `-90`, image 16 `90`; all others `0`. Positive PIL angles are counterclockwise. Use `expand=True` to avoid clipping.
- JSON validation confirms all 21 exact input filenames, all five required fields, allowed categories and allowed rotation values.

## Content boundaries and uncertainties

- Photographs are labelled by observable scenes and legible event backdrops. No person is identified from their face; no official capacity, meeting purpose or location is inferred.
- Award titles describe what the supplied certificates or plaques say. They are not independent authentication of the awards, issuers or biographies.
- Emblems, registration statements and flags are not evidence of a government-conferred award. The Bharat Bhushan materials and Indian Sports Award document are not presented as government awards.
- Bharat Bhushan Samman 2022 is represented by a certificate, an event photo and a plaque. Do not count these three images as three different awards.
- Competition documents are not used to assert medals, results, ranks or placings. Handwritten entries are deliberately omitted where unnecessary or uncertain.
- Image 13 is a Mumbai Fire Brigade training record, not an award. Its handwritten name and date are omitted.
- Image 14 receives a broad inter-school sports competition label; small-print event details, season and handwritten result are omitted.
- Image 16 acknowledges an integrity pledge by Royal Sports and Martial Arts Academy. It is not an award, accreditation or official endorsement.
- Images 10/18 acknowledge contributions to a youth-club sports event, not a competition victory.
- Image 20 uses the broad legible wording “National Sports Award”; the smaller award prefix and date are omitted rather than treated as certain.
- Where a name is transcribed from an award document, retain its visible spelling, “Akash Kishor Shinde”. No attempt is made to harmonise document spelling with other biography text.
- Dates appear in titles only when clearly legible in the image. Event seasons are copied as event seasons, not silently converted to award dates.
