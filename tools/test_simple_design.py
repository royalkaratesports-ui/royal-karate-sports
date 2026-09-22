"""Acceptance checks for the owner's simple, readable redesign."""
from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]

class SimpleDesignTest(unittest.TestCase):
    def test_current_release_excludes_removed_pages_and_runs_offline(self):
        import zipfile,tempfile
        archive=ROOT.parent/'Royal-Karate-Sports-v19.zip'
        self.assertTrue(archive.exists())
        with zipfile.ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            self.assertNotIn('royal-karate-sports/trial.html',z.namelist())
            self.assertNotIn('royal-karate-sports/enroll-now.html',z.namelist())
            self.assertEqual(z.read('royal-karate-sports/royal.css'),(ROOT/'royal.css').read_bytes())
            with tempfile.TemporaryDirectory() as tmp:
                z.extractall(tmp)
                site=Path(tmp)/'royal-karate-sports'
                self.assertEqual(len(list(site.glob('*.html'))),len(list(ROOT.glob('*.html'))))
                with sync_playwright() as pw:
                    browser=pw.chromium.launch()
                    page=browser.new_page(viewport={'width':390,'height':844},accept_downloads=True)
                    page.goto((site/'index.html').as_uri())
                    page.locator('.home-hero .button').first.click()
                    self.assertEqual(page.locator('#contact-topic').input_value(),'regular-classes')
                    page.fill('#contact-name','Release check')
                    page.fill('#contact-message','What are the class timings?')
                    page.locator('#contact-review-button').click()
                    with page.expect_download() as download:
                        page.locator('#contact-download').click()
                    self.assertIn('UNSENT',Path(download.value.path()).read_text(encoding='utf-8'))
                    self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'),390)
                    browser.close()

    def test_trial_and_enrollment_pages_are_removed(self):
        self.assertFalse((ROOT/'trial.html').exists())
        self.assertFalse((ROOT/'enroll-now.html').exists())
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            page=browser.new_page()
            for file in sorted(ROOT.glob('*.html')):
                page.goto(file.as_uri())
                links=page.locator('a').evaluate_all('(es)=>es.map(e=>e.getAttribute("href")||"")')
                self.assertFalse(any('trial.html' in h or 'enroll-now.html' in h for h in links), file.name)
                self.assertNotIn('Enroll Now', page.locator('body').inner_text())
                self.assertNotIn('Plan your trial', page.locator('body').inner_text())
            page.goto((ROOT/'index.html').as_uri())
            for selector in ['.home-access','.home-faq','.home-seasons>div','.faq-list details']:
                for node in page.locator(selector).all():
                    self.assertEqual(node.evaluate('(e)=>parseFloat(getComputedStyle(e).borderTopWidth)'),0,selector)
            page.locator('.home-hero .button').first.click()
            self.assertIn('contact.html',page.url)
            self.assertTrue(page.locator('#contact-form').is_visible())
            browser.close()

    def test_home_and_contact_use_direct_compact_copy(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto((ROOT/'index.html').as_uri())
            self.assertIn('Akash Shinde', page.locator('h1').inner_text())
            self.assertLessEqual(page.locator('main > section').count(), 6)
            self.assertEqual(page.locator('.home-start').count(), 0)
            page.goto((ROOT/'contact.html').as_uri())
            self.assertEqual(page.locator('h1').inner_text(), 'Contact Royal Karate Sports')
            browser.close()

    def test_readable_heading_system_on_every_page(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            for file in sorted(ROOT.glob('*.html')):
                for width in (320, 390, 1440):
                    with self.subTest(page=file.name, width=width):
                        page.set_viewport_size({'width':width,'height':900})
                        page.goto(file.as_uri())
                        h1 = page.locator('main h1')
                        self.assertEqual(h1.count(), 1)
                        style = h1.evaluate('(e)=>{const s=getComputedStyle(e);return {font:s.fontFamily,size:parseFloat(s.fontSize),line:parseFloat(s.lineHeight),transform:s.textTransform}}')
                        if file.name == 'index.html':
                            self.assertTrue('Barlow' in style['font'] or 'Manrope' in style['font'])
                            self.assertLessEqual(style['size'], 120 if width >= 768 else 72)
                        else:
                            self.assertIn('Manrope', style['font'])
                            self.assertEqual(style['transform'], 'none')
                            cap = 40 if width == 390 else 64
                            self.assertLessEqual(style['size'], cap)
                            self.assertGreaterEqual(style['line']/style['size'],1.12)
                        self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'),width)
            browser.close()

if __name__ == '__main__': unittest.main(verbosity=2)
