from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]

class AcademyTest(unittest.TestCase):
    def test_supplied_group_photo_is_uncropped_on_desktop_and_mobile(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for width in [1440, 390, 320]:
                page = browser.new_page(viewport={'width': width, 'height': 900})
                page.goto((ROOT / 'academy.html').as_uri())
                photo = page.locator('.academy-opening img')
                self.assertEqual(photo.get_attribute('src'), 'assets/royal-academy-group.webp')
                photo.scroll_into_view_if_needed()
                photo.evaluate('(i)=>i.decode()')
                metrics = photo.evaluate('(i)=>({w:i.clientWidth,h:i.clientHeight,nw:i.naturalWidth,nh:i.naturalHeight})')
                self.assertEqual((metrics['nw'], metrics['nh']), (960, 720))
                self.assertAlmostEqual(metrics['w']/metrics['h'], 960/720, delta=.01)
                self.assertNotIn('Stock', page.locator('.academy-opening figcaption').inner_text())
                self.assertFalse(page.evaluate('document.documentElement.scrollWidth>innerWidth'))
                page.close()
            browser.close()

    def test_supplied_academy_story_and_founder_link(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((ROOT / 'academy.html').as_uri())
            self.assertIn('Royal Sports Academy', page.title())
            text = page.locator('main').text_content()
            for phrase in ['Martial Arts Training With a Purpose', 'Our Story', '100% Free Karate Training', 'No Monthly Fees. No Paid Classes.', 'Our Training Centres', 'Ganesh Vidyamandir School', 'Pratiksha Nagar', 'What We Teach', 'From Training to Competition', 'Founder & Head Coach', 'Our Mission', 'Our Vision', 'Why Royal Sports Academy?', 'Open to Opportunity, Not Income', '2023', 'nomination record rather than receipt of a Padma Award', 'Mumbai Zonal Inter School TEBMA Martial Arts Championship 2016–17', '23rd WFSKO Open Asian / International Karate Championship in 2018']:
                self.assertIn(phrase, text)
            self.assertNotIn('Proposed academy philosophy', text)
            self.assertNotIn('being shaped around', text)
            page.locator('main').get_by_role('link', name='Read Akash Shinde’s full profile').click()
            self.assertTrue(page.url.endswith('about-akash-shinde.html'))
            browser.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
