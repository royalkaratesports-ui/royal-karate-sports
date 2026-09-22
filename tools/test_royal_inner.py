"""Inner redesign contract. Does not run the builder or write site files."""
import importlib.util
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


class InnerOpeningTests(unittest.TestCase):
    def test_profile_is_recomposed_with_a_prominent_founder(self):
        module = Path(__file__).with_name('royal_inner.py')
        self.assertTrue(module.exists(), 'Missing inner-page transformer')
        spec = importlib.util.spec_from_file_location('royal_inner', module)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        source = BeautifulSoup((ROOT / 'about-akash-shinde.html').read_text(encoding='utf-8'), 'html.parser').main.decode_contents()
        result = BeautifulSoup(mod.adapt_page('about-akash-shinde.html', source), 'html.parser')
        opening = result.select_one('.r-opening')
        self.assertIsNotNone(opening)
        self.assertIn('Founder & Head Coach', opening.get_text(' ', strip=True))
        self.assertIsNotNone(opening.select_one('.r-opening-copy .profile-lede'))
        self.assertIsNotNone(opening.select_one('img[src="assets/akash-kishor-shinde.webp"]'))
        self.assertIsNotNone(result.select_one('nav[aria-label="Breadcrumb"]'))
        self.assertIsNotNone(result.select_one('#mission'))


ROUTES = (
    'about-akash-shinde.html', 'sensei.html', 'academy.html', 'instructors.html',
    'kids-batches.html', 'adult-batches.html', 'programs.html', 'seminars.html',
    'competition.html', 'locations.html', 'contact.html', 'media.html',
    'achievements.html', 'events.html', 'gallery.html', 'information.html',
)


def source(name):
    return BeautifulSoup((ROOT / name).read_text(encoding='utf-8'), 'html.parser').main.decode_contents()


def transform(name):
    from royal_inner import adapt_page
    return BeautifulSoup(adapt_page(name, source(name)), 'html.parser')


class AllInnerRoutesTests(unittest.TestCase):
    def test_all_sixteen_routes_have_real_compositions(self):
        self.assertEqual(len(ROUTES), 16)
        for name in ROUTES:
            with self.subTest(route=name):
                page = transform(name)
                self.assertIsNotNone(page.select_one('.r-content[data-r-adapted]'))
                self.assertIsNotNone(page.select_one('.r-opening h1'))
                self.assertIsNotNone(page.select_one('.r-opening-copy'))
                self.assertIsNotNone(page.select_one('nav[aria-label="Breadcrumb"]'))
                self.assertIsNotNone(page.select_one('.r-jump a[href^="#"]'))
                self.assertEqual(len(page.select('h1')), 1)

    def test_inner_styles_are_standalone_and_cover_interaction_states(self):
        target = ROOT / 'royal-pages.css'
        self.assertTrue(target.exists(), 'Missing standalone inner stylesheet')
        css = target.read_text(encoding='utf-8')
        self.assertNotIn('simple-design', css)
        for text in ['.r-page', '.is-zoomed', '[hidden]', 'object-fit: contain', 'max-width: 900px', 'max-width: 600px', 'min-height: 44px', '.contact-field', '.r-coach-lead']:
            self.assertIn(text, css)
        self.assertNotIn('object-fit: cover', css)

    def test_index_and_repeated_transform_are_noops(self):
        from royal_inner import adapt_page
        sentinel = '<section id="tab"><h1>Do not change</h1></section>'
        self.assertEqual(adapt_page('index.html', sentinel), sentinel)
        for name in ROUTES:
            first = adapt_page(name, source(name))
            self.assertEqual(adapt_page(name, first), first)

    def test_every_id_route_and_interaction_attribute_survives(self):
        from collections import Counter
        for name in ROUTES:
            before = BeautifulSoup(source(name), 'html.parser')
            after = transform(name)
            with self.subTest(route=name):
                old_ids = {n['id'] for n in before.select('[id]')}
                ids = [n['id'] for n in after.select('[id]')]
                self.assertTrue(old_ids <= set(ids))
                self.assertEqual(len(ids), len(set(ids)))
                old_links = Counter(n['href'] for n in before.select('[href]'))
                links = Counter(n['href'] for n in after.select('[href]'))
                self.assertFalse(old_links - links)
                def hooks(page):
                    return Counter((n.name, k, str(v)) for n in page.find_all(True) for k,v in n.attrs.items() if k.startswith('data-') and not k.startswith('data-r-'))
                self.assertEqual(hooks(before), hooks(after))
                for a in after.select('.r-jump a'):
                    self.assertIsNotNone(after.find(id=a['href'][1:]))

    def test_archive_collections_and_local_form_are_untouched(self):
        for name,selector,count in [('media.html','.press-grid figure',23),('achievements.html','.achievement-card',20),('events.html','.event-photo',7),('gallery.html','.gallery-grid figure',9)]:
            page = transform(name)
            self.assertEqual(len(page.select(selector)), count)
        before = BeautifulSoup(source('contact.html'), 'html.parser')
        after = transform('contact.html')
        self.assertEqual(str(before.select_one('#contact-form')), str(after.select_one('#contact-form')))
        self.assertEqual(str(before.select_one('#contact-review')), str(after.select_one('#contact-review')))
        self.assertTrue(after.select_one('#contact-fields').has_attr('disabled'))
        self.assertIn('UNSENT', after.get_text())
        self.assertEqual([n['href'] for n in before.select('a[href^="tel:"], a[href^="mailto:"]')], [n['href'] for n in after.select('a[href^="tel:"], a[href^="mailto:"]')])
        self.assertFalse(after.select('a[href*="instagram"],a[href*="facebook"],a[href*="justdial"]'))

    def test_founder_is_first_then_all_real_coaches(self):
        import json
        page = transform('instructors.html')
        lead = page.select_one('.r-coach-lead')
        self.assertIsNotNone(lead)
        self.assertIn('Akash Kishor Shinde', lead.get_text())
        self.assertIn('Founder & Head Coach', lead.get_text())
        manifest = json.loads((ROOT / 'tools/coaches-manifest.json').read_text(encoding='utf-8'))
        names = [n.get_text(strip=True) for n in page.select('.r-coaches h3')]
        self.assertEqual(names, [i['name'] for i in manifest['items']])
        for route in ['academy.html','contact.html']:
            self.assertIn('Founder & Head Coach', transform(route).get_text(' ', strip=True))
        self.assertFalse(page.select('img[src*="7045600"]'))

    def test_programmes_locations_seminars_have_owned_photos(self):
        for name in ['programs.html','locations.html','competition.html','seminars.html']:
            self.assertFalse(transform(name).select('img[src^="assets/704"]'))
        self.assertEqual(len(transform('programs.html').select('.r-program-grid > section')),4)
        self.assertEqual(len(transform('locations.html').select('.r-centre-cards > article')),2)
        self.assertEqual(len(transform('information.html').select('.r-information-section')),6)


import os


@unittest.skipUnless(os.environ.get('ROYAL_BROWSER_TEST') == '1', 'Set ROYAL_BROWSER_TEST=1 for Chromium + real styles/scripts')
class InnerBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        from urllib.parse import unquote, urlsplit
        import mimetypes
        from royal_inner import adapt_page
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()
        cls.context = cls.browser.new_context(reduced_motion='reduce')
        cls.bodies = {name: adapt_page(name, source(name)) for name in ROUTES}
        def serve(route):
            name = unquote(urlsplit(route.request.url).path.lstrip('/'))
            if name in cls.bodies:
                old = BeautifulSoup((ROOT / name).read_text(encoding='utf-8'), 'html.parser')
                lightbox = old.select_one('.lightbox')
                html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Royal inner verification</title><link rel="stylesheet" href="royal.css"><link rel="stylesheet" href="royal-pages.css"><script src="site.js" defer></script></head><body class="royal-design r-page"><main id="main">' + cls.bodies[name] + '</main>' + (str(lightbox) if lightbox else '') + '</body></html>'
                route.fulfill(status=200, body=html, content_type='text/html; charset=utf-8')
            else:
                file = ROOT / name
                if file.is_file() and ROOT in file.resolve().parents:
                    route.fulfill(status=200, body=file.read_bytes(), content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
                else:
                    route.fulfill(status=404, body='Not found')
        cls.serve = staticmethod(serve)
        cls.context.route('https://royal.test/**', serve)
        cls.page = cls.context.new_page()
        cls.errors = []
        cls.page.on('pageerror', lambda e: cls.errors.append(str(e)))

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def open_page(self, name):
        self.page.goto('https://royal.test/' + name)
        self.page.evaluate("async()=>{await document.fonts.ready; await Promise.all([...document.images].filter(i=>i.hasAttribute('src')).map(i=>{i.loading='eager';return i.decode().catch(()=>{})}));}")

    def test_all_routes_at_five_widths_and_real_images(self):
        for name in ROUTES:
            self.open_page(name)
            broken = self.page.locator('main img[src]').evaluate_all('(es)=>es.filter(i=>!i.naturalWidth).map(i=>i.src)')
            self.assertEqual(broken, [], name)
            for width in (320,390,600,900,1440):
                self.page.set_viewport_size({'width':width,'height':1000})
                with self.subTest(route=name, width=width):
                    self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth'), 'horizontal overflow')
                    small = self.page.locator('main button:visible,main summary:visible,.r-jump a:visible').evaluate_all('(es)=>es.filter(e=>e.getBoundingClientRect().height<43.5).map(e=>({text:e.textContent,h:e.getBoundingClientRect().height}))')
                    self.assertEqual(small, [], 'control smaller than 44px')
                    crop = self.page.locator('main img[src]').evaluate_all('(es)=>es.filter(i=>getComputedStyle(i).objectFit!=="contain").map(i=>i.src)')
                    self.assertEqual(crop, [])
        self.assertEqual(self.errors, [])

    def test_accessibility_and_optional_visual_captures(self):
        for name in ROUTES:
            self.open_page(name)
            self.page.add_script_tag(path=str(ROOT / 'tools/axe.min.js'))
            for width in (390,1440):
                self.page.set_viewport_size({'width':width,'height':1000})
                result = self.page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
                violations = [{'id':v['id'],'targets':[n['target'] for n in v['nodes']]} for v in result['violations']]
                with self.subTest(route=name, width=width):
                    self.assertEqual(violations, [])
                directory = os.environ.get('ROYAL_SCREENSHOT_DIR')
                if directory and name in ['about-akash-shinde.html','academy.html','instructors.html','programs.html','contact.html','events.html','media.html']:
                    output = Path(directory)
                    output.mkdir(parents=True, exist_ok=True)
                    self.page.screenshot(path=str(output / f'{name[:-5]}-{width}.png'))

    def test_editorial_spacing_and_button_palette(self):
        self.page.set_viewport_size({'width':1440,'height':1000})
        self.open_page('academy.html')
        columns = self.page.locator('.r-academy-introduction > :not(:first-child)').evaluate_all('(es)=>es.map(e=>getComputedStyle(e).gridColumnStart)')
        self.assertEqual(set(columns), {'2'})
        self.open_page('events.html')
        self.assertEqual(self.page.locator('.events-hero-photo figcaption span').evaluate('e=>getComputedStyle(e).display'), 'block')
        colors = self.page.locator('.r-opening .button').evaluate('e=>({bg:getComputedStyle(e).backgroundColor,ink:getComputedStyle(e).color})')
        self.assertEqual(colors, {'bg':'rgb(226, 184, 107)', 'ink':'rgb(20, 43, 60)'})

    def test_archive_filters_readers_keyboard_and_zoom(self):
        for name, grid, filter_attr, category_attr, open_attr, viewer, zoom, stage, next_button in [
            ('media.html','.press-grid figure','data-media-filter','data-media-category','data-press-open','#press-viewer','[data-press-zoom]','.press-image-stage','[data-press-next]'),
            ('achievements.html','.achievement-card','data-ach-filter','data-ach-category','data-ach-open','#achievement-viewer','[data-ach-zoom]','.achievement-stage','[data-ach-next]'),
        ]:
            self.open_page(name)
            categories = self.page.locator('['+filter_attr+']').evaluate_all('(es)=>es.map(e=>e.getAttribute("'+filter_attr+'"))')
            for category in categories:
                self.page.locator('['+filter_attr+'="'+category+'"]').click()
                expected = self.page.locator(grid).count() if category=='all' else self.page.locator(grid+'['+category_attr+'="'+category+'"]').count()
                self.assertEqual(self.page.locator(grid+':visible').count(), expected)
            self.page.locator('['+filter_attr+'="all"]').click()
            opener = self.page.locator(grid+' ['+open_attr+']').first
            opener.click()
            self.assertTrue(self.page.locator(viewer).is_visible())
            self.page.locator(zoom).click()
            self.assertTrue(self.page.locator(stage).evaluate('e=>e.scrollWidth>e.clientWidth'))
            self.page.locator(zoom).click()
            self.page.locator(next_button).focus()
            self.page.keyboard.press('ArrowRight')
            self.page.keyboard.press('Escape')
            self.assertFalse(self.page.locator(viewer).is_visible())
            self.assertTrue(opener.evaluate('e=>e===document.activeElement'))
        self.open_page('events.html')
        self.page.locator('[data-event-open]').first.click()
        self.page.keyboard.press('ArrowRight')
        self.assertIn('2 / 7', self.page.locator('#event-position').inner_text())
        self.page.keyboard.press('Escape')
        self.assertFalse(self.page.locator('#event-viewer').is_visible())
        self.open_page('gallery.html')
        self.page.locator('[data-filter="junior"]').click()
        self.assertEqual(self.page.locator('.gallery-grid figure:visible').count(),3)
        self.page.locator('[data-photo]:visible').first.click()
        self.assertTrue(self.page.locator('.lightbox').is_visible())
        self.page.keyboard.press('Escape')

    def test_contact_is_an_unsent_editable_download(self):
        self.open_page('contact.html?enquiry=regular-classes')
        self.page.locator('#contact-name').fill('Verification only')
        self.page.locator('#contact-message').fill('Please confirm the class time.')
        self.page.locator('#contact-review-button').click()
        self.assertTrue(self.page.locator('#contact-review').is_visible())
        self.assertIn('UNSENT ENQUIRY DRAFT', self.page.locator('#contact-draft').inner_text())
        with self.page.expect_download() as download:
            self.page.locator('#contact-download').click()
        self.assertEqual(download.value.suggested_filename, 'royal-karate-enquiry-UNSENT.txt')
        self.page.locator('#contact-edit').click()
        self.assertFalse(self.page.locator('#contact-review').is_visible())
        self.assertTrue(self.page.locator('#contact-download').is_disabled())
        self.assertEqual(self.page.evaluate('localStorage.length'),0)
        context = self.browser.new_context(java_script_enabled=False)
        context.route('https://royal.test/**', self.serve)
        page = context.new_page()
        page.goto('https://royal.test/contact.html')
        self.assertIsNotNone(page.locator('#contact-fields').get_attribute('disabled'))
        self.assertTrue(page.locator('#contact-name').is_disabled())
        self.assertTrue(page.locator('#contact-review-button').is_disabled())
        context.close()


if __name__ == '__main__':
    unittest.main()
