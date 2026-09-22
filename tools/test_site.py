from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class SiteTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=sync_playwright().start(); cls.browser=cls.p.chromium.launch()
 @classmethod
 def tearDownClass(cls):
  cls.browser.close(); cls.p.stop()
 def setUp(self):
  self.page=self.browser.new_page(viewport={'width':1440,'height':1000})
 def tearDown(self): self.page.close()
 def open(self,name='index.html'):
  self.assertTrue((ROOT/name).exists(),f'{name} must exist')
  self.page.goto((ROOT/name).as_uri())
 def test_mobile_menu_opens_and_closes_with_escape(self):
  self.page.set_viewport_size({'width':390,'height':844})
  self.open()
  self.page.get_by_role('button',name='Open navigation').click()
  self.assertTrue(self.page.locator('#mobile-menu').is_visible())
  self.page.keyboard.press('Escape')
  self.assertFalse(self.page.locator('#mobile-menu').is_visible())
  self.assertTrue(self.page.get_by_role('button',name='Open navigation').evaluate('(el)=>el===document.activeElement'))
 def test_program_selection_updates_image_copy_and_destination(self):
  self.open()
  self.page.locator('#tab-adults').click()
  self.assertEqual(self.page.locator('#tab-adults').get_attribute('aria-selected'),'true')
  self.assertEqual('assets/adults-class-practice.webp',self.page.locator('#program-image').get_attribute('src'))
  self.assertIn('adults',self.page.locator('#program-link').get_attribute('href'))
  self.assertIn('ADULT',self.page.locator('#program-tag').inner_text().upper())
  self.page.keyboard.press('ArrowRight')
  self.assertEqual(self.page.locator('#tab-sport').get_attribute('aria-selected'),'true')
  self.page.keyboard.press('Home')
  self.assertEqual(self.page.locator('#tab-kids').get_attribute('aria-selected'),'true')
 def test_gallery_can_filter_and_enlarge_a_photo(self):
  self.open('gallery.html')
  self.page.get_by_role('button',name='Young learners',exact=True).click()
  self.assertEqual(self.page.locator('.gallery-grid figure:visible').count(),3)
  self.assertIn('3 photographs',self.page.locator('#gallery-count').inner_text())
  source=self.page.locator('.gallery-grid figure:visible .photo-button').first
  expected=source.get_attribute('data-photo')
  source.click()
  self.assertTrue(self.page.locator('.lightbox').is_visible())
  self.assertEqual(self.page.locator('.lightbox img').get_attribute('src'),expected)
  self.page.keyboard.press('Escape')
  self.assertFalse(self.page.locator('.lightbox').is_visible())
  self.assertTrue(source.evaluate('(el)=>el===document.activeElement'))
 def test_homepage_has_clear_trial_path(self):
  self.open()
  self.assertIn('Akash Shinde',self.page.locator('h1').inner_text())
  self.page.locator('.hero .button').first.click()
  self.assertIn('contact.html',self.page.url)
  self.assertEqual(self.page.locator('#contact-topic').input_value(),'regular-classes')
if __name__=='__main__': unittest.main(verbosity=2)
