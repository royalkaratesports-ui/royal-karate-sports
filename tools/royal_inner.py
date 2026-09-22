"""Content-preserving inner compositions for Royal's navy/cream design.

Public handle: adapt_page(name: str, body: str) -> str. Call AFTER
simplify_content. Pure fragment transform; never runs the builder or writes assets.
The shell must use body.royal-design.r-page and royal.css + royal-pages.css.
"""
from pathlib import Path
import json
import re
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
INNER_ROUTES = (
    'about-akash-shinde.html', 'sensei.html', 'academy.html', 'instructors.html',
    'kids-batches.html', 'adult-batches.html', 'programs.html', 'seminars.html',
    'competition.html', 'locations.html', 'contact.html', 'media.html',
    'achievements.html', 'events.html', 'gallery.html', 'information.html',
)
OPENINGS = '.profile-hero, .academy-opening, .kids-hero, .adults-hero, .contact-heading, .media-intro, .achievements-opening, .events-hero, .page-hero'


def _classes(node, *names):
    if node is not None:
        node['class'] = list(dict.fromkeys(node.get('class', []) + list(names)))


def _element(soup, tag, text=None, **attrs):
    node = soup.new_tag(tag, attrs=attrs)
    if text is not None:
        node.string = text
    return node


def _fragment(html):
    return BeautifulSoup(html, 'html.parser').find()


def _move_all(source, target):
    for node in list(source.contents):
        target.append(node.extract())


def _role(soup, target):
    target.insert(0, _element(soup, 'p', 'Founder & Head Coach', **{'class': 'r-role'}))


def _replace_photo(soup, figure, src, alt, caption):
    """Replace only non-interactive stock photographs, never archive records."""
    img = figure.find('img')
    img['src'], img['alt'] = src, alt
    img.attrs.pop('width', None)
    img.attrs.pop('height', None)
    figcaption = figure.find('figcaption')
    if figcaption:
        figcaption.string = caption
    else:
        figure.append(_element(soup, 'figcaption', caption))
    _classes(figure, 'r-supplied-photo')


def _opening(soup, name):
    opening = soup.select_one(OPENINGS)
    _classes(opening, 'wrap', 'r-opening')
    # Old full-width/wrapper combinations are flattened, not duplicated.
    inner = opening.find('div', class_='wrap', recursive=False)
    if inner:
        inner.unwrap()
    copy = _element(soup, 'div', **{'class': 'r-opening-copy'})
    figures = opening.find_all('figure', recursive=False)
    if name == 'adult-batches.html':
        heading = opening.select_one('.adults-hero-heading')
        _move_all(heading, copy)
        heading.decompose()
    else:
        for node in list(opening.contents):
            if node not in figures:
                copy.append(node.extract())
    opening.insert(0, copy)
    for figure in figures:
        _classes(figure, 'r-opening-figure')
    return opening, copy


def _profile(soup, opening, copy):
    _classes(opening, 'r-profile-opening')
    # Bring the entire biography beside the portrait, not three grid fragments.
    lede = copy.select_one('.profile-lede')
    if lede is None:
        lede = soup.select_one('.profile-lede')
        copy.append(lede.extract())
    heading = copy.select_one('.profile-heading')
    _role(soup, heading)
    close = soup.select_one('.profile-closing h2')
    close.string = 'Train. Learn. Grow.'
    label = soup.select_one('.recognition-discipline')
    label.string = 'Karate'


def _academy(soup, opening, copy):
    intro = copy.select_one('.academy-opening-copy').extract()
    intro.name = 'section'
    _classes(intro, 'wrap', 'r-academy-introduction')
    intro['id'] = 'academy-purpose'
    opening.insert_after(intro)
    group = soup.select_one('.academy-story-grid figure').extract()
    _classes(group, 'r-opening-figure')
    opening.append(group)
    copy.append(_element(soup, 'p', 'Free regular karate training. No paid classes. No training fees.', **{'class': 'r-lead'}))
    copy.append(_fragment('<a class="button" href="#founder">Meet our founder &amp; head coach <span aria-hidden="true">↗</span></a>'))
    founder = soup.select_one('#founder').extract()
    intro.insert_after(founder)
    founder.select_one('.eyebrow').string = 'Founder & Head Coach'
    _classes(founder, 'r-founder-feature')
    _classes(soup.select_one('#our-story'), 'r-story-reading')


def _instructors(soup, opening, copy):
    lead = soup.select_one('.editorial-split')
    _classes(lead, 'r-coach-lead')
    lead['id'] = lead.get('id', 'lead-coach')
    figure = lead.find('figure')
    _replace_photo(soup, figure, 'assets/akash-kishor-shinde.webp',
                   'Akash Kishor Shinde, founder and head coach of Royal Sports Academy',
                   'Akash Kishor Shinde · Photograph supplied by the academy')
    text = lead.find('div', recursive=False)
    _role(soup, text)
    text.insert(1, _element(soup, 'h2', 'Akash Kishor Shinde'))
    approach = text.find_all('h2')[-1]
    approach.name = 'h3'
    note = text.select_one('.content-note')
    for string in list(note.find_all(string=True)):
        if 'The training photograph above is illustrative stock imagery' in string:
            string.replace_with(str(string).replace(' The training photograph above is illustrative stock imagery, not Akash’s portrait.', ''))
    manifest = json.loads((ROOT / 'tools/coaches-manifest.json').read_text(encoding='utf-8'))
    team = _element(soup, 'section', **{'class': 'wrap section r-team-section', 'id': 'coaching-team'})
    team.append(_element(soup, 'h2', 'The coaching team'))
    team.append(_element(soup, 'p', 'The coaches supporting the practice at Royal Sports Academy. Names and coach roles supplied by the academy.'))
    grid = _element(soup, 'div', **{'class': 'r-coaches'})
    for person in manifest['items']:
        card = _element(soup, 'article', **{'class': 'r-coach-card'})
        figure = _element(soup, 'figure')
        # The Sahil display derivative is cropped: use the existing original.
        crop = person.get('display_crop', [])
        src = person['original'] if crop and any(crop[:2]) else person['display']
        figure.append(_element(soup, 'img', src=src, alt=f"{person['name']} — coach at Royal Sports Academy", loading='lazy', decoding='async'))
        card.append(figure)
        heading = _element(soup, 'h3', person['name'])
        if person['name'] == 'साहिल हेगडकर':
            heading['lang'] = 'mr'
        card.append(heading)
        card.append(_element(soup, 'p', 'Coach'))
        grid.append(card)
    team.append(grid)
    lead.insert_after(team)


def _contact(soup, opening, copy):
    _classes(opening, 'r-contact-opening')
    person = soup.select_one('.contact-person').extract()
    _classes(person, 'r-opening-figure')
    _role(soup, person.find('figcaption'))
    opening.append(person)
    channels = soup.select_one('.contact-channels').extract()
    _classes(channels, 'r-contact-direct')
    channels['id'] = 'direct-contact'
    copy.append(channels)
    copy.append(copy.select_one('.contact-jump').extract())
    _classes(soup.select_one('.contact-information'), 'r-centre-information')


def _programs(soup, opening, copy):
    sections = soup.select('.program-detail')
    grid = _element(soup, 'div', **{'class': 'r-program-grid'})
    sections[0].insert_before(grid)
    photos = [
        ('assets/kids-group-training.webp', 'Children practising punches together on training mats', 'Kids training · Academy-supplied photograph'),
        ('assets/adults-class-practice.webp', 'Mixed-age karate class standing in formation', 'Academy archive · Mixed-age class, not a separate teen batch'),
        ('assets/adults-shotokan.webp', 'Karate practitioners practising punches together in a hall', 'Karate practice · Academy-supplied photograph'),
        ('assets/adults-archive-athletes.webp', 'Karate practitioners with medals alongside adults', 'Academy archive · No event or result is inferred'),
    ]
    for section, (src, alt, caption) in zip(sections, photos):
        grid.append(section.extract())
        _replace_photo(soup, section.find('figure'), src, alt, caption)
    for key, href, label in [('kids','kids-batches.html','Explore kids training'), ('adults','adult-batches.html','Explore adult training'), ('sport','competition.html','About kata & kumite')]:
        node = soup.select_one(f'#{key} .detail-copy')
        node.append(_element(soup, 'a', label, href=href, **{'class': 'text-link'}))
    note = soup.select_one('.page-note').extract()
    _classes(note, 'r-notice')
    copy.append(note)


def _editorial(soup, name, opening, copy):
    selector = '.location-photo' if name == 'locations.html' else '.editorial-split > figure'
    figure = soup.select_one(selector).extract()
    if name == 'seminars.html':
        src, alt, caption = ('assets/adults-class-practice.webp', 'A mixed-age academy class in formation', 'Academy training archive · Not a seminar photograph')
        note = soup.select_one('.content-note').extract()
        _classes(note, 'r-notice')
        copy.append(note)
        _classes(soup.select_one('.editorial-split'), 'r-seminar-outline')
    elif name == 'locations.html':
        src, alt, caption = ('assets/royal-academy-group.webp', 'Academy students and adults in a group photograph', 'Academy-supplied photograph · The venue is not identified')
        panel = soup.select_one('.location-panel')
        cards = _element(soup, 'div', **{'class': 'r-centre-cards'})
        for title, locality in [('Ganesh Vidyamandir School', 'Dharavi, Mumbai'), ('Pratiksha Nagar', 'Mumbai')]:
            card = _element(soup, 'article')
            card.append(_element(soup, 'h3', title))
            card.append(_element(soup, 'p', locality))
            card.append(_element(soup, 'p', 'Free regular karate training', **{'class': 'r-free'}))
            cards.append(card)
        panel.select_one('.location-meta').insert_before(cards)
        small = panel.select_one('.small')
        small.string = 'Please do not travel until Royal has confirmed your venue and class. The academy archive photograph does not identify either training centre.'
    else:
        src, alt, caption = ('assets/adults-shotokan.webp', 'Karate practitioners working on punching techniques together in a hall', 'Academy training photograph · Not a tournament result')
        other = soup.select_one('.competition-image')
        _replace_photo(soup, other, 'assets/adults-archive-athletes.webp', 'Karate practitioners with medals alongside adults', 'Academy archive photograph · Event and results not specified')
        empty = soup.select_one('.results-empty')
        empty.find('h3').string = 'Confirmed results, not invented counts'
        empty.find('p').string = 'No independently verified tournament results have been provided. The supplied certificates and photographs can be explored in the achievement archive; event names, dates, athlete permissions and results require confirmation. No medal counts are invented.'
        empty.append(_element(soup, 'a', 'Explore the supplied achievement archive', href='achievements.html', **{'class': 'text-link'}))
        _classes(empty, 'r-results-note')
        lower = empty.parent
        if lower.find(class_='eyebrow', recursive=False):
            empty.insert(0, lower.find(class_='eyebrow', recursive=False).extract())
        soup.select_one('.competition > .wrap').append(empty.extract())
        if not lower.find(True):
            lower.decompose()
    _replace_photo(soup, figure, src, alt, caption)
    _classes(figure, 'r-opening-figure')
    opening.append(figure)


def _information(soup):
    prose = soup.select_one('.prose')
    _classes(prose, 'r-information')
    section = None
    for node in list(prose.contents):
        if isinstance(node, Tag) and node.name == 'h2':
            section = _element(soup, 'section', **{'class': 'r-information-section'})
            prose.append(section)
        if section is not None:
            section.append(node.extract())
    for paragraph in prose.find_all('p'):
        if paragraph.get_text().startswith('Barlow Condensed and Manrope'):
            paragraph.string = 'Manrope is locally hosted from Google Fonts and used for headings and body text. Manrope and the retained Barlow Condensed font asset are distributed under the SIL Open Font License. License files are included with the website package.'
        if 'Other training photographs depict stock models' in paragraph.get_text():
            for string in list(paragraph.find_all(string=True)):
                string.replace_with(str(string).replace('Other training photographs depict stock models and studios, not Royal Karate Sports students, staff or facilities.', 'The Photo gallery contains explicitly illustrative stock models and studios, not Royal Karate Sports students, staff or facilities. Other academy photographs, coach portraits, event images and archive scans were supplied by the owner.'))


def _navigation(soup, content, opening, name):
    title = opening.h1.get_text(' ', strip=True)
    breadcrumb = _element(soup, 'nav', **{'class': 'wrap r-breadcrumb', 'aria-label': 'Breadcrumb'})
    breadcrumb.append(_element(soup, 'a', 'Home', href='index.html'))
    breadcrumb.append(_element(soup, 'span', title, **{'aria-current': 'page'}))
    content.insert(0, breadcrumb)
    existing = soup.select_one('.profile-jump, .academy-section-nav, .events-section-nav')
    jump = existing or _element(soup, 'nav', **{'class': 'wrap'})
    jump.name = 'nav'
    _classes(jump, 'r-jump')
    jump['aria-label'] = 'On this page'
    if existing:
        jump.extract()
    targets = []
    for heading in content.select('h2'):
        if heading.find_parent('dialog') or heading.find_parent(id='contact-review'):
            continue
        section = heading.find_parent('section')
        if section is None or section == opening or section.find_parent('section') == opening:
            continue
        if section not in targets:
            targets.append(section)
    existing_links = {a.get('href') for a in jump.find_all('a')}
    # Keep all original navigation; add only a few high-value reading jumps.
    for i, section in enumerate(targets):
        if not section.get('id'):
            stem = re.sub('[^a-z0-9]+', '-', section.h2.get_text(' ', strip=True).lower()).strip('-')
            candidate = 'r-' + (stem or str(i))
            while soup.find(id=candidate):
                candidate += '-section'
            section['id'] = candidate
        href = '#' + section['id']
        if not existing and len(jump.find_all('a')) < 5 and href not in existing_links:
            label = section.h2.get_text(' ', strip=True)
            jump.append(_element(soup, 'a', label, href=href))
    if not jump.find('a'):
        target = soup.select_one('.gallery-grid')
        if target:
            target['id'] = target.get('id', 'photo-collection')
            jump.append(_element(soup, 'a', 'Browse photographs', href='#' + target['id']))
    opening.insert_after(jump)


def _reading_compositions(soup):
    _classes(soup.select_one('.events-activity-list'), 'faq-list')
    # These transform lists into distinct content groups rather than restoring
    # the former long divider-lined editorial template.
    for selector in ['.kids-training-list', '.adult-training-list', '.recognition-list', '.academy-why dl']:
        _classes(soup.select_one(selector), 'r-card-grid')
    for selector in ['.kids-training', '.adults-programme']:
        node = soup.select_one(selector)
        if node:
            _classes(node, 'r-curriculum')
            first = node.find('div', recursive=False)
            _classes(first, 'r-section-intro')
    for selector in ['.profile-values-list', '.academy-skills']:
        _classes(soup.select_one(selector), 'r-skill-list')
    for selector in ['.media-gallery-heading', '.achievements-section-heading', '.events-section-heading', '.adult-archive-heading']:
        for node in soup.select(selector):
            _classes(node, 'r-section-heading')
    for selector in ['.media-intro', '.achievements-opening']:
        _classes(soup.select_one(selector), 'r-archive-opening')
    # Archive contextual notes move before the gallery so readers see the
    # verification caveats before browsing, without losing a single record.
    for grid_sel, note_sel in [('.press-grid','.media-archive-note'),('.achievements-grid','.achievement-archive-note'),('.events-gallery','.events-photo-note')]:
        grid = soup.select_one(grid_sel)
        notes = soup.select(note_sel)
        note = next((n for n in notes if not n.find_parent('noscript')), None)
        if grid and note:
            grid.insert_before(note.extract())
            _classes(note, 'r-archive-context')
    stage = soup.select_one('.press-image-stage')
    if stage:
        stage['tabindex'] = '0'
        stage['role'] = 'region'
        stage['aria-label'] = 'Document; scroll to pan when zoomed'
    if soup.select_one('.gallery-disclaimer'):
        disclaimer = soup.select_one('.gallery-disclaimer').extract()
        soup.select_one('.gallery-controls').insert_before(disclaimer)
        _classes(disclaimer, 'r-notice')
    for node in soup.select('.kids-overview span'):
        node.string = node.get_text().capitalize()
    # Exact form IDs, fields, scripts and archive interaction hooks are never
    # rewritten. Typographic changes only apply to non-interactive copy.


def adapt_page(name: str, body: str) -> str:
    """Return the redesign of one of 16 inner routes; index is unchanged."""
    if name == 'index.html' or name not in INNER_ROUTES:
        return body
    soup = BeautifulSoup(body, 'html.parser')
    if soup.select_one('[data-r-adapted]'):
        return body
    if soup.select_one(OPENINGS) is None:
        raise ValueError(f'{name}: expected an existing page opening')
    content = soup.find('article', recursive=False)
    if content is None:
        content = _element(soup, 'article')
        nodes = list(soup.contents)
        soup.append(content)
        for node in nodes:
            if isinstance(node, Tag) and node.name in ('dialog', 'script'):
                continue
            content.append(node.extract())
    _classes(content, 'r-content', 'r-' + name.removesuffix('.html'))
    content['data-r-adapted'] = name
    opening, copy = _opening(soup, name)
    if name in ('about-akash-shinde.html', 'sensei.html'):
        _profile(soup, opening, copy)
    elif name == 'academy.html':
        _academy(soup, opening, copy)
    elif name == 'instructors.html':
        _instructors(soup, opening, copy)
    elif name == 'contact.html':
        _contact(soup, opening, copy)
    elif name == 'programs.html':
        _programs(soup, opening, copy)
    elif name in ('locations.html', 'seminars.html', 'competition.html'):
        _editorial(soup, name, opening, copy)
    elif name == 'information.html':
        _information(soup)
    _reading_compositions(soup)
    _navigation(soup, content, opening, name)
    return str(soup)
