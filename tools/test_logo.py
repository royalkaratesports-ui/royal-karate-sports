"""Owner logo replaces the concept monogram everywhere, including icons."""
from pathlib import Path
import json,hashlib,unittest
from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

class LogoTest(unittest.TestCase):
    def test_all_pages_use_owner_logo_in_every_brand_placement(self):
        pages=sorted(ROOT.glob('*.html'))
        self.assertEqual(len(pages),17)
        for file in pages:
            with self.subTest(page=file.name):
                soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
                brands=soup.select('a.brand')
                self.assertEqual(len(brands),3)
                for brand in brands:
                    self.assertEqual(len(brand.select('img.brand-logo')),1)
                    self.assertEqual(brand.img['src'],'assets/brand/royal-logo.png')
                    self.assertEqual(brand['href'],'index.html')
                    self.assertIn('logo',brand.img['alt'].lower())
                    self.assertFalse(brand.select('svg'))
                self.assertEqual(soup.select_one('link[rel="icon"]')['href'],'assets/brand/favicon.png')
                self.assertEqual(soup.select_one('link[rel="apple-touch-icon"]')['href'],'assets/brand/apple-touch-icon.png')

    def test_logo_has_real_transparency_and_preserved_original(self):
        manifest=ROOT/'tools/logo-manifest.json'
        self.assertTrue(manifest.exists(),'Owner logo assets and provenance must exist')
        data=json.loads(manifest.read_text(encoding='utf-8'))
        self.assertEqual(hashlib.sha256((ROOT/data['original']).read_bytes()).hexdigest(),data['sha256'])
        im=Image.open(ROOT/'assets/brand/royal-logo.png').convert('RGBA')
        self.assertEqual(im.size,(512,512))
        self.assertEqual(im.getpixel((0,0))[3],0)
        self.assertEqual(im.getpixel((256,256))[3],255)
        self.assertTrue((ROOT/'assets/brand/favicon.png').exists())

    def test_responsive_brand_and_mobile_menu(self):
        with sync_playwright() as pw:
            b=pw.chromium.launch();p=b.new_page()
            p.goto((ROOT/'index.html').as_uri());p.evaluate('document.fonts.ready')
            for width in (320,390,768,1440):
                p.set_viewport_size({'width':width,'height':900})
                logo=p.locator('.site-header .brand-logo')
                self.assertEqual(logo.count(),1)
                self.assertTrue(logo.is_visible())
                self.assertGreaterEqual(logo.bounding_box()['height'],60)
                self.assertEqual(logo.evaluate('(i)=>getComputedStyle(i).objectFit'),'contain')
                self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),width)
            p.set_viewport_size({'width':390,'height':844})
            p.locator('.menu-toggle').click()
            self.assertTrue(p.locator('#mobile-menu .brand-logo').is_visible())
            p.keyboard.press('Escape')
            b.close()

if __name__=='__main__':unittest.main(verbosity=2)
