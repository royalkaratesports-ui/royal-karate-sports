import unittest,json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
GROUPS={'About Us':[('About Akash Shinde','about-akash-shinde.html'),('About Royal Sports Academy','academy.html'),('Instructors','instructors.html')],'Programmes':[('Kids Batches','kids-batches.html'),('Adult Batches','adult-batches.html'),('Seminars','seminars.html')],'Trending':[('Media','media.html'),('Events','events.html'),('Achievements','achievements.html')]}
class CategoryTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=sync_playwright().start();cls.b=cls.p.chromium.launch()
 @classmethod
 def tearDownClass(cls):cls.b.close();cls.p.stop()
 def test_desktop_dropdown_dismisses_with_escape_and_outside_click(self):
  page=self.b.new_page(viewport={'width':1440,'height':1000})
  page.goto((ROOT/'index.html').as_uri())
  summary=page.locator('.desktop-nav summary',has_text='Programmes')
  summary.focus();page.keyboard.press('Enter')
  self.assertTrue(page.locator('.desktop-nav').get_by_role('link',name='Kids Batches').is_visible())
  page.keyboard.press('Tab');page.keyboard.press('Escape')
  self.assertEqual(page.locator('.desktop-nav .nav-group[open]').count(),0)
  self.assertTrue(summary.evaluate('(e)=>e===document.activeElement'))
  summary.click();page.locator('h1').click()
  self.assertEqual(page.locator('.desktop-nav .nav-group[open]').count(),0)
  page.close()
 def test_mobile_categories_match_desktop(self):
  page=self.b.new_page(viewport={'width':390,'height':844})
  for group,items in GROUPS.items():
   for label,target in items:
    page.goto((ROOT/'index.html').as_uri())
    page.get_by_role('button',name='Open navigation').click()
    page.locator('#mobile-menu summary',has_text=group).click()
    page.locator('#mobile-menu').get_by_role('link',name=label,exact=True).click()
    self.assertTrue(page.url.endswith(target))
    self.assertFalse(page.locator('#mobile-menu').is_visible())
  page.close()
 def test_reference_categories_have_working_royal_pages(self):
  page=self.b.new_page(viewport={'width':1440,'height':1000})
  page.goto((ROOT/'index.html').as_uri())
  self.assertEqual(page.locator('.desktop-nav > .nav-group > summary').all_text_contents(),list(GROUPS))
  self.assertEqual(page.locator('.desktop-nav > a').all_text_contents(),['Home','Contact'])
  self.assertEqual(page.locator('.header-cta').count(),0)
  for group,items in GROUPS.items():
   for label,target in items:
    page.goto((ROOT/'index.html').as_uri())
    page.locator('.desktop-nav summary',has_text=group).click()
    anchor=page.locator('.desktop-nav').get_by_role('link',name=label,exact=True)
    self.assertTrue(anchor.is_visible())
    self.assertEqual(anchor.get_attribute('href'),target)
    anchor.click()
    self.assertTrue(page.url.endswith(target))
    self.assertEqual(page.locator('h1').count(),1)
    self.assertNotIn('Santosh Mohite',page.locator('main').inner_text())
  page.goto((ROOT/'index.html').as_uri());page.locator('.desktop-nav').get_by_role('link',name='Contact',exact=True).click()
  self.assertTrue(page.url.endswith('contact.html'))
  self.assertTrue(page.locator('#contact-form').is_visible())
  page.close()
if __name__=='__main__':unittest.main(verbosity=2)
