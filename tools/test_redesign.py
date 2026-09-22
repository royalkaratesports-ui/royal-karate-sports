"""The owner's replacement-template contract, not a hero color override."""
from pathlib import Path
import unittest
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]

class RedesignTest(unittest.TestCase):
    def test_main_coach_leads_first_screen(self):
        with sync_playwright() as pw:
            b=pw.chromium.launch(); p=b.new_page(viewport={'width':1440,'height':1000})
            p.goto((ROOT/'index.html').as_uri()); p.evaluate('document.fonts.ready')
            self.assertIn('Akash Shinde',p.locator('h1').inner_text())
            hero=p.locator('.home-hero')
            self.assertIn('Founder & Head Coach',hero.inner_text())
            portrait=hero.locator('img[src="assets/akash-kishor-shinde.webp"]')
            self.assertEqual(portrait.count(),1)
            box=portrait.bounding_box()
            self.assertGreaterEqual(box['width'],350)
            self.assertLess(box['y'],250)
            self.assertEqual(portrait.evaluate('(e)=>getComputedStyle(e).objectFit'),'contain')
            for width in (320,390,768,1440):
                p.set_viewport_size({'width':width,'height':900})
                self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),width)
                self.assertEqual(hero.evaluate('(e)=>parseFloat(getComputedStyle(e).borderBottomWidth)'),0)
            b.close()

    def test_direct_contact_is_visible_before_portrait_on_mobile(self):
        with sync_playwright() as pw:
            b=pw.chromium.launch(); p=b.new_page(viewport={'width':390,'height':844})
            p.goto((ROOT/'contact.html').as_uri());p.evaluate('document.fonts.ready')
            phone=p.locator('main a[href^="tel:"]')
            self.assertLess(phone.bounding_box()['y'],760)
            portrait=p.locator('.contact-person')
            self.assertLess(phone.bounding_box()['y'],portrait.bounding_box()['y'])
            p.set_viewport_size({'width':1440,'height':900})
            self.assertLess(phone.bounding_box()['y'],800)
            b.close()

    def test_mobile_profile_places_coach_photo_before_long_biography(self):
        with sync_playwright() as pw:
            b=pw.chromium.launch();p=b.new_page(viewport={'width':390,'height':844})
            p.goto((ROOT/'about-akash-shinde.html').as_uri())
            self.assertLess(p.locator('.profile-portrait').bounding_box()['y'],p.locator('.profile-lede').bounding_box()['y'])
            b.close()

    def test_all_routes_use_only_new_design_system(self):
        for file in ROOT.glob('*.html'):
            with self.subTest(file=file.name):
                s=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
                self.assertIn('royal-design',s.body.get('class',[]))
                self.assertEqual([x['href'] for x in s.select('link[rel="stylesheet"]')],['royal.css','royal-pages.css'])
                self.assertIn('Founder & Head Coach',s.footer.get_text(' ',strip=True))

if __name__=='__main__':unittest.main(verbosity=2)
