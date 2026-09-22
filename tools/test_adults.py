from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

class AdultsTest(unittest.TestCase):
    def test_supplied_adult_program_photos_and_enquiry(self):
        with sync_playwright() as p:
            b=p.chromium.launch();page=b.new_page()
            page.goto((ROOT/'adult-batches.html').as_uri())
            text=page.locator('main').text_content()
            for phrase in ['Advanced Shotokan karate training','Basic to extreme physical fitness training','Belt gradation exams every 6 months','Weight loss and weight gain','CrossFit-style','Karate meditation training','Street-safety and self-defence training','Training Benefits','Body fitness and health','Personality and self-presentation','Mental stability and composure','Weight management','A happier, active lifestyle']:
                self.assertIn(phrase,text)
            self.assertNotIn('proposed adult pathway',text)
            self.assertEqual(page.locator('main img').count(),5)
            expected={'adults-shotokan.webp':(1728,780),'adults-class-practice.webp':(1280,1229),'adults-archive-group.webp':(544,183),'adults-archive-athletes.webp':(458,270),'adults-archive-community.webp':(522,171)}
            for width in [1440,768,390,320]:
                page.set_viewport_size({'width':width,'height':900})
                for img in page.locator('main img').all():
                    img.scroll_into_view_if_needed();img.evaluate('(i)=>i.decode()')
                    data=img.evaluate('(i)=>({src:i.src.split("/").pop(),w:i.clientWidth,h:i.clientHeight,nw:i.naturalWidth,nh:i.naturalHeight})')
                    self.assertEqual((data['nw'],data['nh']),expected[data['src']])
                    self.assertAlmostEqual(data['w']/data['h'],data['nw']/data['nh'],delta=.03)
                self.assertFalse(page.evaluate('document.documentElement.scrollWidth>innerWidth'))
            page.get_by_text('When are adult belt exams held?',exact=True).click()
            self.assertTrue(page.get_by_text('Adult belt gradation exams are held every 6 months.',exact=False).is_visible())
            page.locator('main').get_by_role('link',name='Enquire for adult training',exact=True).first.click()
            self.assertIn('contact.html',page.url)
            self.assertEqual(page.locator('#contact-topic').input_value(),'regular-classes')
            b.close()

if __name__=='__main__':unittest.main(verbosity=2)
