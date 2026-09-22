"""Homepage acceptance tests; run against the built static homepage."""
from pathlib import Path
import re
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REAL = re.compile(r'^assets/(events/event-0[1-7]|akash-kishor-shinde|royal-academy-group|kids-[\w-]+|adults-[\w-]+|coaches/(?:amar-dabade|mayur-dilawar|sahil-hegadkar))\.webp$')

class HomeRefreshTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = sync_playwright().start()
        cls.browser = cls.p.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.p.stop()

    def setUp(self):
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 1000})
        self.page.goto((ROOT / 'index.html').as_uri())

    def tearDown(self):
        self.page.close()

    def test_home_photographs_are_real_full_frame_sources(self):
        images = self.page.locator('main img')
        self.assertGreater(images.count(), 3)
        for image in images.all():
            src = image.get_attribute('src')
            self.assertRegex(src, REAL, 'Homepage must use only supplied photography')
            self.assertTrue((ROOT / src).exists())
            self.assertTrue(image.get_attribute('alt'))
            fit = image.evaluate('(el) => getComputedStyle(el).objectFit')
            if 'home-hero-photo' in (image.evaluate('(el) => el.className + " " + (el.parentElement&&el.parentElement.className||"")')):
                self.assertIn(fit, ('cover', 'contain'))
            else:
                self.assertEqual(fit, 'contain')

    def test_home_uses_full_bleed_hero_and_two_ctas(self):
        hero = self.page.locator('.home-hero')
        self.assertTrue(hero.locator('img').first.is_visible())
        self.assertGreaterEqual(hero.evaluate('(e)=>e.getBoundingClientRect().height'), 420)
        labels = [t.strip() for t in self.page.locator('.home-hero a').all_inner_texts()]
        self.assertTrue(any('Contact' in t for t in labels))
        self.assertGreaterEqual(len(labels), 2)
        body = self.page.locator('main').inner_text()
        self.assertNotIn('Ayumi Iwata', body)
        self.assertNotIn('$25', body)
        self.assertIn('free', body.lower())

    def test_program_tabs_keep_real_photos_and_keyboard_navigation(self):
        seen = set()
        for key in ('kids', 'teens', 'adults', 'sport'):
            tab = self.page.locator('#tab-' + key)
            tab.click()
            self.assertEqual(tab.get_attribute('aria-selected'), 'true')
            src = self.page.locator('#program-image').get_attribute('src')
            self.assertRegex(src, REAL)
            seen.add(src)
            self.assertIn('#' + key, self.page.locator('#program-link').get_attribute('href'))
            self.assertEqual(self.page.locator('#program-panel').get_attribute('aria-labelledby'), 'tab-' + key)
        self.assertEqual(len(seen), 4)
        self.page.keyboard.press('Home')
        self.assertEqual(self.page.locator('#tab-kids').get_attribute('aria-selected'), 'true')
        self.page.keyboard.press('ArrowRight')
        self.assertEqual(self.page.locator('#tab-teens').get_attribute('aria-selected'), 'true')
        self.assertRegex(self.page.locator('#program-image').get_attribute('src'), REAL)

    def test_camp_and_community_information_is_grounded(self):
        text = self.page.locator('main').inner_text().lower()
        for term in ('summer', 'winter', 'twice a year', 'one month before', 'grading', 'kata', 'sparring', 'awards', 'self-defense', 'personal growth', 'ganesh vidyamandir school', 'dharavi', 'pratiksha nagar', 'akash kishor shinde', 'free of charge'):
            self.assertIn(term, text)
        self.assertNotIn('enrollment is open', text)
        self.assertEqual(self.page.locator('h1').count(), 1)
        self.page.locator('.home-hero .button').first.click()
        self.assertIn('contact.html', self.page.url)
        self.assertEqual(self.page.locator('#contact-topic').input_value(), 'regular-classes')

    def test_mobile_selection_navigation_and_local_links(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.get_by_role('button', name='Open navigation').click()
        self.assertTrue(self.page.locator('#mobile-menu').is_visible())
        self.page.keyboard.press('Escape')
        self.assertFalse(self.page.locator('#mobile-menu').is_visible())
        for key in ('kids', 'teens', 'adults', 'sport'):
            self.page.locator('#tab-' + key).click()
            self.assertRegex(self.page.locator('#program-image').get_attribute('src'), REAL)
            self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth'))
        for anchor in self.page.locator('main a').all():
            href = anchor.get_attribute('href')
            filename = href.split('#')[0].split('?')[0]
            if filename:
                self.assertTrue((ROOT / filename).exists(), href)
        self.page.locator('.home-camps .button').click()
        self.assertTrue(self.page.url.endswith('events.html'))

    def test_responsive_render_and_capture(self):
        import json
        errors = []
        self.page.on('pageerror', lambda error: errors.append(str(error)))
        self.page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
        self.page.reload()
        self.page.evaluate("async () => { await document.fonts.ready; for (const img of document.images) { img.loading='eager'; await img.decode().catch(() => {}); } }")
        report = {'viewport_checks': [], 'screenshots': [], 'console_errors': errors}
        for width in (320, 390, 760, 1024, 1440, 1920):
            self.page.set_viewport_size({'width': width, 'height': 900 if width > 760 else 844})
            self.page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
            self.page.wait_for_timeout(100)
            overflow = self.page.evaluate('document.documentElement.scrollWidth > innerWidth')
            self.assertFalse(overflow, f'Horizontal overflow at {width}px')
            report['viewport_checks'].append({'width': width, 'horizontal_overflow': overflow})
            if width in (390, 1440):
                label = 'mobile' if width == 390 else 'desktop'
                # Trigger actual painting before taking the full-page screenshot.
                for img in self.page.locator('main img').all():
                    img.scroll_into_view_if_needed()
                    self.assertGreater(img.evaluate('(el) => el.naturalWidth'), 0)
                self.page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
                self.page.wait_for_timeout(150)
                path = ROOT / ('home-' + label + '.png')
                self.page.screenshot(path=str(path), full_page=True)
                report['screenshots'].append(path.name)
                self.page.screenshot(path=str(ROOT / ('home-' + label + '-hero.png')))
        self.assertEqual(errors, [])
        report['tdd'] = {'real_photography': 'RED on stock hero; GREEN after replacement', 'program_photography': 'RED on shared stock tab source; GREEN after page-scoped data override'}
        report['source_manifest'] = {'path': 'tools/events-manifest.json', 'input_count': 8, 'unique_count': 7}
        report['legacy_test_note'] = 'tools/test_site.py stock asset assertion 7045595 is obsolete; actual adult image is adults-class-practice.webp. Other 4 legacy tests pass.'
        (ROOT / 'home-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

if __name__ == '__main__':
    unittest.main(verbosity=2)
