from pathlib import Path
import json,unittest,zipfile,hashlib,tempfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT.parent/'Royal-Karate-Sports-v19.zip'

class AchievementsReleaseTests(unittest.TestCase):
 def test_connected_archive_preserves_sources_and_reader(self):
  self.assertTrue(ARCHIVE.exists(),'Updated website archive not packaged')
  inputs=json.loads((ROOT/'tools/achievements-inputs.json').read_text())
  with zipfile.ZipFile(ARCHIVE) as z:
   self.assertIsNone(z.testzip())
   for name in inputs:
    rel='assets/achievements/originals/'+name
    self.assertEqual(hashlib.sha256(z.read('royal-karate-sports/'+rel)).digest(),hashlib.sha256((ROOT/rel).read_bytes()).digest())
   with tempfile.TemporaryDirectory() as tmp:
    z.extractall(tmp);site=Path(tmp)/'royal-karate-sports'
    with sync_playwright() as pw:
     browser=pw.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844});errors=[]
     page.on('pageerror',lambda e:errors.append(str(e)))
     page.goto((site/'index.html').as_uri())
     page.locator('.menu-toggle').click()
     page.locator('#mobile-menu').get_by_text('Trending',exact=True).click()
     page.locator('#mobile-menu').get_by_role('link',name='Achievements',exact=True).click()
     self.assertTrue(page.url.endswith('/achievements.html'))
     self.assertEqual(page.locator('.achievement-card').count(),20)
     self.assertEqual(page.locator('.achievements-opening').evaluate('(e)=>getComputedStyle(e).display'),'grid')
     page.locator('[data-ach-filter="community"]').click()
     self.assertEqual(page.locator('.achievement-card:visible').count(),3)
     page.locator('.achievement-card:visible [data-ach-open]').first.click()
     page.locator('#achievement-full').evaluate('(i)=>i.decode()')
     self.assertTrue(page.locator('#achievement-full').evaluate('(i)=>i.naturalWidth>0'))
     page.keyboard.press('Escape')
     page.get_by_role('link',name='Explore press coverage',exact=True).click()
     self.assertTrue(page.url.endswith('/media.html'))
     self.assertFalse(errors,errors);browser.close()

if __name__=='__main__':unittest.main(verbosity=2)
