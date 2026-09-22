"""Owner-supplied coach identities/photos and uncluttered presentation."""
from pathlib import Path
import hashlib,json,unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
NAMES=['Amar Dabade','Mayur Dilawar','साहिल हेगडकर']

class HomeTeamTest(unittest.TestCase):
    def test_release_contains_all_coaches_and_originals(self):
        import zipfile,tempfile
        archive=ROOT.parent/'Royal-Karate-Sports-v19.zip'
        self.assertTrue(archive.exists())
        manifest=json.loads((ROOT/'tools/coaches-manifest.json').read_text(encoding='utf-8'))
        with zipfile.ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            for item in manifest['items']:
                self.assertEqual(hashlib.sha256(z.read('royal-karate-sports/'+item['original'])).hexdigest(),item['sha256'])
                self.assertEqual(z.read('royal-karate-sports/'+item['display']),(ROOT/item['display']).read_bytes())
            with tempfile.TemporaryDirectory() as tmp:
                z.extractall(tmp)
                with sync_playwright() as pw:
                    browser=pw.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844})
                    page.goto((Path(tmp)/'royal-karate-sports/index.html').as_uri())
                    self.assertEqual(page.locator('.coach-name').all_text_contents(),NAMES)
                    for image in page.locator('.coach-photo img').all():
                        image.scroll_into_view_if_needed();image.evaluate('(i)=>i.decode()')
                        self.assertGreater(image.evaluate('(i)=>i.naturalWidth'),0)
                    browser.close()

    def test_remaining_decorative_rules_are_removed_but_inputs_keep_boundaries(self):
        with sync_playwright() as pw:
            browser=pw.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844})
            page.goto((ROOT/'index.html').as_uri());page.locator('.menu-toggle').click()
            for item in page.locator('#mobile-menu nav>a, #mobile-menu summary').all():
                self.assertEqual(item.evaluate('(e)=>parseFloat(getComputedStyle(e).borderBottomWidth)'),0)
            page.goto((ROOT/'contact.html').as_uri())
            self.assertEqual(page.locator('.contact-enquiry').evaluate('(e)=>parseFloat(getComputedStyle(e).borderTopWidth)'),0)
            self.assertGreaterEqual(page.locator('#contact-name').evaluate('(e)=>parseFloat(getComputedStyle(e).borderTopWidth)'),1)
            page.locator('#contact-name').focus()
            self.assertGreaterEqual(page.locator('#contact-name').evaluate('(e)=>parseFloat(getComputedStyle(e).outlineWidth)'),2)
            page.goto((ROOT/'achievements.html').as_uri())
            self.assertEqual(page.locator('.achievement-image').first.evaluate('(e)=>parseFloat(getComputedStyle(e).borderTopWidth)'),0)
            browser.close()

    def test_three_coaches_have_exact_supplied_names_and_preserved_sources(self):
        with sync_playwright() as pw:
            browser=pw.chromium.launch();page=browser.new_page()
            page.goto((ROOT/'index.html').as_uri())
            self.assertEqual(page.locator('#our-team .coach-name').all_text_contents(),NAMES)
            self.assertEqual(page.locator('#our-team .coach-photo img').count(),3)
            self.assertIn('Led by Akash.',page.locator('#our-team > .wrap > header h2').inner_text())
            manifest=json.loads((ROOT/'tools/coaches-manifest.json').read_text(encoding='utf-8'))
            self.assertEqual([x['name'] for x in manifest['items']],NAMES)
            for item,img in zip(manifest['items'],page.locator('#our-team .coach-photo img').all()):
                self.assertEqual(img.get_attribute('src'),item['display'])
                self.assertIn(item['name'],img.get_attribute('alt'))
                self.assertEqual(hashlib.sha256((ROOT/item['original']).read_bytes()).hexdigest(),item['sha256'])
            for width in (320,390,768,1024,1440):
                page.set_viewport_size({'width':width,'height':900})
                for img in page.locator('#our-team .coach-photo img').all():
                    img.scroll_into_view_if_needed();img.evaluate('(i)=>i.decode()')
                    self.assertGreater(img.evaluate('(i)=>i.naturalWidth'),0)
                    self.assertEqual(img.evaluate('(i)=>getComputedStyle(i).objectFit'),'contain')
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'),width)
                for card in page.locator('.coach-card').all():
                    self.assertEqual(card.evaluate('(e)=>getComputedStyle(e).boxShadow'),'none')
                    self.assertEqual(card.evaluate('(e)=>parseFloat(getComputedStyle(e).borderTopWidth)'),0)
            browser.close()

if __name__=='__main__':unittest.main(verbosity=2)
