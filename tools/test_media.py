from pathlib import Path
import json,unittest,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

class MediaTest(unittest.TestCase):
    def test_archive_filters_reader_zoom_and_keyboard(self):
        labels=json.loads((ROOT/'tools/media-labels.json').read_text(encoding='utf-8'))
        with sync_playwright() as p:
            b=p.chromium.launch();page=b.new_page(viewport={'width':390,'height':844})
            page.goto((ROOT/'media.html').as_uri())
            page.locator('[data-media-filter="records"]').click()
            expected=sum(x['category']=='records' for x in labels.values())
            self.assertEqual(page.locator('.press-grid figure:visible').count(),expected)
            self.assertEqual(page.locator('#press-count').inner_text(),f'{expected} archive items')
            first=page.locator('.press-grid figure:visible [data-press-open]').first
            first.click();self.assertTrue(page.locator('#press-viewer').is_visible())
            self.assertNotIn('stock',page.locator('#press-viewer').inner_text().lower())
            self.assertEqual(page.locator('#press-original').get_attribute('href'),first.get_attribute('href'))
            page.locator('[data-press-zoom]').click()
            self.assertEqual(page.locator('[data-press-zoom]').get_attribute('aria-pressed'),'true')
            self.assertTrue(page.locator('.press-image-stage').evaluate('(e)=>e.scrollWidth>e.clientWidth'))
            old=page.locator('#press-viewer-image').get_attribute('src')
            page.keyboard.press('ArrowRight')
            self.assertNotEqual(page.locator('#press-viewer-image').get_attribute('src'),old)
            page.keyboard.press('Escape');self.assertFalse(page.locator('#press-viewer').is_visible())
            self.assertTrue(first.evaluate('(a)=>a===document.activeElement'))
            for category in ['press','records','all']:
                page.locator(f'[data-media-filter="{category}"]').click()
                count=len(labels) if category=='all' else sum(x['category']==category for x in labels.values())
                self.assertEqual(page.locator('.press-grid figure:visible').count(),count)
            b.close()

    def test_media_content_and_complete_deduplicated_archive(self):
        manifest=json.loads((ROOT/'tools/media-manifest.json').read_text())
        self.assertEqual(manifest['input_count'],26)
        self.assertEqual(sum(len(x['sources']) for x in manifest['items']),26)
        self.assertEqual(len(manifest['items']),23)
        inputs=json.loads((ROOT/'tools/media-inputs.json').read_text())
        self.assertEqual(sorted(inputs),sorted(n for item in manifest['items'] for n in item['sources']))
        for item in manifest['items']:
            self.assertEqual(hashlib.sha256((ROOT/item['original']).read_bytes()).hexdigest(),item['sha256'])
        with sync_playwright() as p:
            b=p.chromium.launch();page=b.new_page();page.goto((ROOT/'media.html').as_uri())
            text=page.locator('main').text_content()
            for phrase in ['Media & Press','Media & press','Featured in the Media','Stories That Go Beyond Sports','Indian Sports Award 2019','Bharat Bhushan Samman 2022','nomination, not receipt of a Padma Award','Ganesh Vidyamandir School, Dharavi, Mumbai','Pratiksha Nagar, Mumbai','Media Gallery']:
                self.assertIn(phrase,text)
            self.assertEqual(page.locator('.press-grid figure').count(),23)
            self.assertEqual(set(page.locator('.press-grid [data-press-open]').evaluate_all('(a)=>a.map(x=>x.getAttribute("href"))')),set(x['original'] for x in manifest['items']))
            self.assertNotIn('Original clippings and publication details are still needed',text)
            b.close()

if __name__=='__main__':unittest.main(verbosity=2)
