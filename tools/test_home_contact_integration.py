from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

class HomeContactIntegrationTest(unittest.TestCase):
 def test_new_home_and_contact_are_connected_on_mobile(self):
  with sync_playwright() as pw:
   browser=pw.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844})
   page.goto((ROOT/'index.html').as_uri())
   self.assertIn('home-refresh',page.locator('body').get_attribute('class'))
   page.locator('.menu-toggle').click()
   page.locator('#mobile-menu').get_by_role('link',name='Contact',exact=True).click()
   self.assertTrue(page.url.endswith('/contact.html'))
   self.assertIn('contact-refresh',page.locator('body').get_attribute('class'))
   self.assertEqual(page.locator('main form').count(),1)
   text=page.locator('main').text_content()
   for phrase in ['Ganesh Vidyamandir','Pratiksha Nagar']:
    self.assertIn(phrase,text)
   page.locator('.menu-toggle').click()
   page.locator('#mobile-menu').get_by_text('Trending',exact=True).click()
   page.locator('#mobile-menu').get_by_role('link',name='Events',exact=True).click()
   self.assertIn('Summer Karate Camp',page.locator('main').text_content())
   self.assertEqual(page.locator('.event-photo').count(),7)
   browser.close()

if __name__=='__main__':unittest.main(verbosity=2)
