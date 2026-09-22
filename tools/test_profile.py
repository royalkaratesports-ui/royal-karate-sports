from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class ProfileTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.p=sync_playwright().start();cls.b=cls.p.chromium.launch()
 @classmethod
 def tearDownClass(cls):cls.b.close();cls.p.stop()
 def test_training_facts_are_consistent_across_the_site(self):
  page=self.b.new_page()
  page.goto((ROOT/'index.html').as_uri())
  page.get_by_text('Is regular karate training really free?',exact=True).click()
  answer=page.locator('details',has=page.get_by_text('Is regular karate training really free?',exact=True)).inner_text()
  self.assertIn('free',answer.lower())
  self.assertNotIn('not advertised as free',answer)
  for filename in ['locations.html','contact.html']:
   page.goto((ROOT/filename).as_uri())
   self.assertIn('Ganesh Vidyamandir School',page.locator('main').inner_text())
   self.assertIn('Dharavi',page.locator('main').inner_text())
   self.assertIn('Pratiksha Nagar',page.locator('main').inner_text())
  for file in ROOT.glob('*.html'):
   text=file.read_text(encoding='utf-8')
   for stale in ['About Our Sensei','Pricing has not been supplied','fees and class times are not yet connected','availability, fees','fee confirmation']:
    self.assertNotIn(stale,text,file.name)
  page.close()
 def test_akash_profile_has_supplied_story_photo_and_navigation(self):
  target=ROOT/'about-akash-shinde.html'
  self.assertTrue(target.exists(),'The named Akash Shinde profile must exist')
  page=self.b.new_page(viewport={'width':1440,'height':1000});page.goto(target.as_uri())
  self.assertIn('AKASH KISHOR SHINDE',' '.join(page.locator('h1').inner_text().upper().split()))
  body=page.locator('main').text_content()
  for text in ['Martial Arts With a Mission','No child should be denied','completely free of charge','Ganesh Vidyamandir School, Dharavi','Pratiksha Nagar, Mumbai','Self-discipline and confidence','Mumbai Zonal Inter School TEBMA Martial Arts Championship 2016–17','23rd WFSKO Open Asian/International Karate Championship in 2018','Indian Sports Award','2019','Bharat Bhushan Samman','2022','Our Mission','Our Vision','No Paid Classes.']:
   self.assertIn(text,body)
  self.assertNotIn('profile is awaiting verification',body)
  portrait=page.locator('main img').first
  self.assertIn('akash-kishor-shinde.webp',portrait.get_attribute('src'))
  self.assertTrue(portrait.evaluate('(e)=>e.complete&&e.naturalWidth>0'))
  page.locator('.desktop-nav summary',has_text='About Us').click()
  a=page.locator('.desktop-nav').get_by_role('link',name='About Akash Shinde',exact=True)
  self.assertEqual(a.get_attribute('href'),'about-akash-shinde.html')
  page.goto((ROOT/'sensei.html').as_uri())
  self.assertIn('AKASH KISHOR SHINDE',' '.join(page.locator('h1').inner_text().upper().split()))
  page.close()
if __name__=='__main__':unittest.main(verbosity=2)
