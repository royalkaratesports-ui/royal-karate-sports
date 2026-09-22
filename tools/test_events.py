from pathlib import Path
import unittest,json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

class EventsTest(unittest.TestCase):
 def test_all_eight_supplied_photos_are_preserved(self):
  manifest=ROOT/'tools/events-manifest.json'
  self.assertTrue(manifest.exists(),'Events photo inventory missing')
  data=json.loads(manifest.read_text())
  names=json.loads((ROOT/'tools/events-inputs.json').read_text())
  self.assertEqual(len(names),8)
  self.assertEqual(sorted(names),sorted(n for x in data['items'] for n in x['sources']))
  self.assertEqual(len(data['items']),len(set(x['pixel_hash'] for x in data['items'])))
  for item in data['items']:
   for name in item['sources']:
    self.assertEqual(hashlib.sha256((ROOT/'assets/events/originals'/name).read_bytes()).hexdigest(),item['source_hashes'][name])

 def test_camp_content_real_gallery_and_navigation(self):
  data=json.loads((ROOT/'tools/events-manifest.json').read_text())
  with sync_playwright() as pw:
   browser=pw.chromium.launch();page=browser.new_page();page.goto((ROOT/'events.html').as_uri())
   text=page.locator('main').text_content()
   for phrase in ['Events &','Summer Karate Camp','Winter Karate Camp','Twice a year','Belt Grading & Level-Ups','Tournaments & Competitions','Awards & Prize Distribution','Real-World Self-Defense','Personal Growth & Discipline','one month before']:
    self.assertIn(phrase,text)
   self.assertNotIn('CALENDAR AWAITING',text)
   self.assertNotIn('protect themselves in any situation',text)
   self.assertEqual(page.locator('.event-photo').count(),data['unique_count'])
   self.assertTrue(all('/events/' in x for x in page.locator('.events-content img').evaluate_all('(els)=>els.map(e=>e.getAttribute("src"))')))
   self.assertEqual(set(page.locator('.event-photo [data-event-open]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))')),{x['original'] for x in data['items']})
   page.get_by_role('link',name='Enquire about camps',exact=True).click();self.assertTrue(page.url.endswith('/contact.html'))
   browser.close()

 def test_photo_viewer_and_camp_activity_controls(self):
  with sync_playwright() as pw:
   browser=pw.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844});page.set_default_timeout(4000)
   page.goto((ROOT/'events.html').as_uri())
   page.get_by_text('Real-World Self-Defense',exact=True).click()
   self.assertTrue(page.get_by_text('Practical self-defense training develops',exact=False).is_visible())
   first=page.locator('[data-event-open]').first;first.click()
   self.assertTrue(page.locator('#event-viewer').is_visible())
   links=page.locator('[data-event-open]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))')
   for i,href in enumerate(links):
    self.assertEqual(page.locator('#event-original').get_attribute('href'),href)
    self.assertEqual(page.locator('#event-position').inner_text(),f'{i+1} / {len(links)}')
    page.locator('#event-full').evaluate('(i)=>i.decode()')
    page.keyboard.press('ArrowRight')
   self.assertEqual(page.locator('#event-original').get_attribute('href'),links[0])
   self.assertNotIn('stock',page.locator('#event-viewer').inner_text().lower())
   page.keyboard.press('Escape');self.assertFalse(page.locator('#event-viewer').is_visible())
   self.assertTrue(first.evaluate('(e)=>document.activeElement===e'))
   browser.close()

 def test_release_contains_events_and_connected_mobile_navigation(self):
  import zipfile,tempfile
  archive=ROOT.parent/'Royal-Karate-Sports-v19.zip'
  self.assertTrue(archive.exists(),'Updated Events website ZIP missing')
  with zipfile.ZipFile(archive) as z:
   self.assertIsNone(z.testzip())
   manifest=json.loads((ROOT/'tools/events-manifest.json').read_text())
   for item in manifest['items']:
    for name,sha in item['source_hashes'].items():
     self.assertEqual(hashlib.sha256(z.read('royal-karate-sports/assets/events/originals/'+name)).hexdigest(),sha)
   with tempfile.TemporaryDirectory() as tmp:
    z.extractall(tmp);site=Path(tmp)/'royal-karate-sports'
    with sync_playwright() as pw:
     browser=pw.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844});errors=[]
     page.on('pageerror',lambda e:errors.append(str(e)))
     page.goto((site/'index.html').as_uri());page.locator('.menu-toggle').click()
     page.locator('#mobile-menu').get_by_text('Trending',exact=True).click()
     page.locator('#mobile-menu').get_by_role('link',name='Events',exact=True).click()
     self.assertTrue(page.url.endswith('/events.html'))
     self.assertEqual(page.locator('.event-photo').count(),7)
     self.assertEqual(page.locator('.events-hero').evaluate('e=>getComputedStyle(e).display'),'grid')
     page.locator('[data-event-open]').first.click();self.assertTrue(page.locator('#event-viewer').is_visible())
     page.locator('#event-full').evaluate('i=>i.decode()');page.keyboard.press('Escape')
     self.assertFalse(errors);browser.close()

if __name__=='__main__':unittest.main(verbosity=2)
