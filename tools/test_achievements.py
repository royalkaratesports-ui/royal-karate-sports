from pathlib import Path
import unittest,json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

class AchievementsTests(unittest.TestCase):
 def test_all_supplied_files_preserved_and_unique_images_inventoried(self):
  manifest=ROOT/'tools/achievements-manifest.json'
  self.assertTrue(manifest.exists(),'Achievements inventory not built')
  data=json.loads(manifest.read_text())
  inputs=json.loads((ROOT/'tools/achievements-inputs.json').read_text())
  self.assertEqual(len(inputs),21)
  self.assertEqual(sorted(inputs),sorted(n for x in data['items'] for n in x['sources']))
  self.assertEqual(len(data['items']),len(set(x['pixel_hash'] for x in data['items'])))
  for item in data['items']:
   for name in item['sources']:
    copy=ROOT/'assets/achievements/originals'/name
    # Compare to the acquisition hash, not a mutable Downloads location.
    self.assertEqual(hashlib.sha256(copy.read_bytes()).hexdigest(),item['sha256'])

 def test_page_shows_every_unique_attachment_without_stock(self):
  data=json.loads((ROOT/'tools/achievements-manifest.json').read_text())
  with sync_playwright() as pw:
   browser=pw.chromium.launch();page=browser.new_page()
   page.goto((ROOT/'achievements.html').as_uri())
   self.assertEqual(page.locator('.achievement-card').count(),data['unique_count'])
   self.assertEqual(page.locator('h1').count(),1)
   self.assertNotIn('No verified tournament results',page.locator('main').inner_text())
   hrefs=page.locator('.achievement-card [data-ach-open]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))')
   self.assertEqual(set(hrefs),{x['original'] for x in data['items']})
   self.assertTrue(all('/achievements/' in x for x in page.locator('.achievements-content img').evaluate_all('(els)=>els.map(e=>e.getAttribute("src"))')))
   browser.close()

 def test_filter_reader_zoom_navigation_and_focus(self):
  data=json.loads((ROOT/'tools/achievements-manifest.json').read_text())
  labels=json.loads((ROOT/'tools/achievements-labels.json').read_text(encoding='utf-8'))
  with sync_playwright() as pw:
   browser=pw.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844});page.set_default_timeout(4000)
   page.goto((ROOT/'achievements.html').as_uri())
   for category in ['awards','competition','community','moments','all']:
    page.locator(f'[data-ach-filter="{category}"]').click()
    expected=sum(category=='all' or labels[x['sources'][0]]['category']==category for x in data['items'])
    self.assertEqual(page.locator('.achievement-card:visible').count(),expected)
    self.assertEqual(page.locator('#achievements-count').inner_text(),f'{expected} archive items')
   page.locator('[data-ach-filter="competition"]').click()
   opener=page.locator('.achievement-card:visible [data-ach-open]').first
   opener.click();self.assertTrue(page.locator('#achievement-viewer').is_visible())
   self.assertEqual(page.locator('#achievement-original').get_attribute('href'),opener.get_attribute('href'))
   self.assertNotIn('stock',page.locator('#achievement-viewer').inner_text().lower())
   old=page.locator('#achievement-full').get_attribute('src')
   page.locator('[data-ach-zoom]').click()
   self.assertEqual(page.locator('[data-ach-zoom]').get_attribute('aria-pressed'),'true')
   self.assertTrue(page.locator('.achievement-stage').evaluate('(e)=>e.scrollWidth>e.clientWidth'))
   page.keyboard.press('ArrowRight')
   self.assertNotEqual(page.locator('#achievement-full').get_attribute('src'),old)
   self.assertEqual(page.locator('[data-ach-zoom]').get_attribute('aria-pressed'),'false')
   page.keyboard.press('Escape');self.assertFalse(page.locator('#achievement-viewer').is_visible())
   self.assertTrue(opener.evaluate('(e)=>document.activeElement===e'))
   browser.close()

if __name__=='__main__':unittest.main(verbosity=2)
