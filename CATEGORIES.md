# Reference-matched categories

The user requested the same page categories as championskarateclub.com, not the competitor’s visual design. The source’s live `#menu-main-menu` was inspected as HTML. Its structure is recorded in verification/reference-menu.json.

## Main navigation

| Source category | Royal category | Royal destination |
|---|---|---|
| HOME | Home | index.html |
| ABOUT US | About Us | Expandable category |
| PROGRAMMES | Programmes | Expandable category |
| TRENDING | Trending | Expandable category |
| CONTACT | Contact | contact.html |
| ENROLL NOW | Removed at owner request | No enrollment page |

## Sub-pages

| Group | Source sub-page | Royal sub-page | Royal destination |
|---|---|---|---|
| About Us | About Sensei Santosh Mohite | About Akash Shinde | about-akash-shinde.html |
| About Us | About Champion’s Karate Club | About Royal Sports Academy | academy.html |
| About Us | Instructors | Instructors | instructors.html |
| Programmes | Kids Batches | Kids Batches | kids-batches.html |
| Programmes | Adult Batches | Adult Batches | adult-batches.html |
| Programmes | Seminars | Seminars | seminars.html |
| Trending | Media | Media | media.html |
| Trending | Events | Events | events.html |
| Trending | Achievements | Achievements | achievements.html |

The competitor’s Sensei identity is not reused or attributed to Royal. Akash Kishor Shinde’s biography and portrait are now provided by the owner. The legacy sensei.html route retains the updated profile. The competitor’s seminars link points to `/corporate-batches/`; Royal uses a descriptive `seminars.html` route and original copy. Media and Gallery are not treated as equivalent: Media has its own press/video publication status and a link to the photo journal. Events includes upcoming and past-event publication status. Contact includes training-centre status without copying the competitor’s phone, email, addresses or maps.

Additional pages (programme overview, sport karate, photo gallery, locations and preview information) remain accessible through contextual links. The trial and enrollment pages have been removed; class enquiry links lead to Contact.

## Visual and interaction rules

Use the current simple design described in SIMPLE-DESIGN.md: readable sentence-case typography, real supplied photos and whitespace instead of decorative divider rules. Desktop category disclosure is native HTML details/summary with clear keyboard controls, exclusive opening, outside-click dismissal and Escape focus restoration. Mobile categories expand inside the existing full-screen menu. Each sub-page is a working local page, not a dead `#` link.

Akash’s supplied biography, free-training policy and two location names are now included. Press archives are included. Phone and email are published on Contact as supplied. Instagram and Facebook appear as footer logos. Class schedules and a live enquiry service still require confirmation and setup.
