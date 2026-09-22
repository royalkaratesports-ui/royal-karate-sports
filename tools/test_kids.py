from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

class KidsTest(unittest.TestCase):
    def test_kids_page_explains_supplied_program_and_enrollment(self):
        with sync_playwright() as p:
            b=p.chromium.launch();page=b.new_page()
            page.goto((ROOT/'kids-batches.html').as_uri())
            text=page.locator('main').text_content()
            for phrase in ['Personal attention to each and every student','Basic to advanced karate and fitness training','Belt gradation exams every 5 months','Pure traditional and sports karate training','Training for national and international competitions','Training Benefits','Improves concentration','Improves confidence','Personality development','Improves body conditioning','Develops health and focus']:
                self.assertIn(phrase,text)
            self.assertNotIn('A proposed introduction',text)
            self.assertNotIn('illustrative stock',text)
            self.assertEqual(page.locator('main img').count(),3)
            expected={'kids-line-practice.webp':(480,640),'kids-group-training.webp':(554,554),'kids-first-steps.webp':(1200,1600)}
            for width in [1440,768,390,320]:
                page.set_viewport_size({'width':width,'height':900})
                for img in page.locator('main img').all():
                    img.scroll_into_view_if_needed();img.evaluate('(i)=>i.decode()')
                    data=img.evaluate('(i)=>({src:i.src.split("/").pop(),w:i.clientWidth,h:i.clientHeight,nw:i.naturalWidth,nh:i.naturalHeight})')
                    self.assertEqual((data['nw'],data['nh']),expected[data['src']])
                    self.assertAlmostEqual(data['w']/data['h'],data['nw']/data['nh'],delta=.01)
                self.assertFalse(page.evaluate('document.documentElement.scrollWidth>innerWidth'))
            page.get_by_text('When are the belt exams?',exact=True).click()
            self.assertTrue(page.get_by_text('Belt gradation exams are held every 5 months.',exact=False).is_visible())
            page.locator('main').get_by_role('link',name='Enquire for your child',exact=True).first.click()
            self.assertIn('contact.html',page.url)
            self.assertEqual(page.locator('#contact-topic').input_value(),'regular-classes')
            b.close()

if __name__=='__main__':unittest.main(verbosity=2)
