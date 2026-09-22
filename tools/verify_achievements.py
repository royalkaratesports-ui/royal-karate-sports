from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification';OUT.mkdir(exist_ok=True)
report={'widths':[],'accessibility':[],'errors':[],'external_requests':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch()
 page=browser.new_page()
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.on('request',lambda r:report['external_requests'].append(r.url) if r.url.startswith('http') else None)
 for width in [320,390,540,768,1024,1440,1920]:
  page.set_viewport_size({'width':width,'height':900 if width>760 else 844})
  page.goto((ROOT/'achievements.html').as_uri());page.evaluate('document.fonts.ready')
  page.locator('.achievements-content img').evaluate_all('els=>els.forEach(i=>i.loading="eager")')
  page.locator('.achievements-content img').evaluate_all('els=>Promise.all(els.map(i=>Promise.race([i.decode(),new Promise((_,r)=>setTimeout(()=>r(new Error("decode timed out")),5000))])))')
  for category in ['all','awards','competition','community','moments']:
   page.locator(f'[data-ach-filter="{category}"]').click()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,category)
  page.locator('[data-ach-filter="all"]').click();page.evaluate('scrollTo(0,0)')
  report['widths'].append({'width':width,'overflow':False})
  if width in [390,1440]:
   page.screenshot(path=str(OUT/f'achievements-{width}.png'))
   page.locator('#achievement-archive').scroll_into_view_if_needed()
   page.screenshot(path=str(OUT/f'achievements-gallery-{width}.png'))
   page.locator('[data-ach-filter="awards"]').click()
   page.locator('.achievement-card:visible [data-ach-open]').first.click()
   page.locator('#achievement-full').evaluate('i=>i.decode()')
   page.screenshot(path=str(OUT/f'achievements-reader-{width}.png'))
   page.keyboard.press('Escape')
   page.add_script_tag(path=str(ROOT/'tools/axe.min.js'))
   for state in ['awards','competition','community','moments','all','viewer']:
    if state=='viewer':page.locator('.achievement-card:visible [data-ach-open]').first.click()
    else:page.locator(f'[data-ach-filter="{state}"]').click()
    result=page.evaluate('async()=>{const r=await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}});return r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))}')
    report['accessibility'].append({'width':width,'state':state,'violations':result})
   page.keyboard.press('Escape')
  # Actual reader traverses the filtered collection, with correct images and originals.
  for category in ['awards','competition','community','moments']:
   page.locator(f'[data-ach-filter="{category}"]').click()
   links=page.locator('.achievement-card:visible [data-ach-open]')
   expected=links.evaluate_all('els=>els.map(e=>({image:e.dataset.view,original:e.getAttribute("href")}))')
   links.first.click()
   for entry in expected:
    assert page.locator('#achievement-full').get_attribute('src')==entry['image']
    assert page.locator('#achievement-original').get_attribute('href')==entry['original']
    page.locator('#achievement-full').evaluate('i=>i.decode()')
    page.locator('[data-ach-next]').click()
   page.keyboard.press('Escape')
 context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
 nojs=context.new_page();nojs.goto((ROOT/'achievements.html').as_uri())
 assert nojs.locator('.achievement-card').count()==20
 nojs.locator('.achievement-card [data-ach-open]').first.click()
 assert '/originals/' in nojs.url
 report['no_js_original_access']='passed'
 assert not report['errors'],report['errors'];assert not report['external_requests'],report['external_requests']
 browser.close()
(OUT/'achievements-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert not any(x['violations'] for x in report['accessibility'])
