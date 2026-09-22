from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
IG = 'https://www.instagram.com/royalsportsmartialartsacademy/'
FB = 'https://www.facebook.com/vishal.kadam09/about'
JD = 'justdial.com'

class FooterTest(unittest.TestCase):
    def test_footer_has_phone_email_and_social_logos_not_justdial(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 390, 'height': 844})
            for file in sorted(ROOT.glob('*.html')):
                page.goto(file.as_uri())
                footer = page.locator('footer')
                self.assertIn('8898329666', footer.inner_text(), file.name)
                self.assertIn('always4u.06@gmail.com', footer.inner_text(), file.name)
                ig = footer.locator(f'a[href="{IG}"]')
                fb = footer.locator(f'a[href="{FB}"]')
                self.assertEqual(ig.count(), 1, file.name)
                self.assertEqual(fb.count(), 1, file.name)
                self.assertGreaterEqual(ig.locator('svg').count(), 1, file.name)
                self.assertGreaterEqual(fb.locator('svg').count(), 1, file.name)
                self.assertIn('Instagram', ig.get_attribute('aria-label') or '')
                self.assertIn('Facebook', fb.get_attribute('aria-label') or '')
                box = ig.bounding_box()
                self.assertGreaterEqual(box['height'], 44)
                self.assertGreaterEqual(box['width'], 44)
                self.assertNotIn(JD, footer.inner_html())
            page.goto((ROOT / 'contact.html').as_uri())
            self.assertNotIn(JD, page.locator('main').inner_html())
            self.assertNotIn(JD, page.locator('footer').inner_html())
            browser.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
