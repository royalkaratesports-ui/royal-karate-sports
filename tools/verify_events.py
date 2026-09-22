from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'verification'
report={'responsive':[],'accessibility':[],'errors':[],'external_requests':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch();page=browser.new_page()
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.on('request',lambda r:report['external_requests'].append(r.url) if r.url.startswith('http') else None)
 for width in [320,390,540,768,1024,1440,1920]:
  page.set_viewport_size({'width':width,'height':844 if width<760 else 960})
  page.goto((ROOT/'events.html').as_uri());page.evaluate('document.fonts.ready')
  page.locator('.events-content img').evaluate_all('els=>Promise.all(els.map(i=>{i.loading="eager";return Promise.race([i.decode(),new Promise((_,r)=>setTimeout(()=>r(new Error("decode timeout")),5000))])}))')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  assert page.locator('.events-content img').evaluate_all('els=>els.every(i=>Math.abs(i.getBoundingClientRect().width/i.getBoundingClientRect().height-i.naturalWidth/i.naturalHeight)<0.03)')
  for a in page.locator('.events-section-nav a').all():
   a.click();assert page.url.endswith(a.get_attribute('href'))
  for d in page.locator('.events-activity-list details').all():
   d.evaluate('e=>e.open=true');assert d.locator('p').is_visible()
  page.locator('.events-activity-list details').evaluate_all('els=>els.forEach((e,i)=>e.open=i===0)')
  if width in [390,1440]:
   for image in page.locator('.events-content img').all():image.scroll_into_view_if_needed()
   page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/f'events-{width}.png'))
   page.screenshot(path=str(OUT/f'events-full-{width}.png'),full_page=True)
   page.locator('#signature-camps').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'events-camps-{width}.png'))
   page.locator('#event-gallery').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'events-gallery-{width}.png'))
  page.locator('[data-event-open]').first.click();page.locator('#event-full').evaluate('i=>i.decode()')
  assert page.locator('#event-viewer').evaluate('e=>e.scrollWidth<=e.clientWidth'),width
  assert page.locator('.event-viewer-controls').evaluate('e=>e.getBoundingClientRect().bottom<=innerHeight'),width
  if width in [390,1440]:page.screenshot(path=str(OUT/f'events-viewer-{width}.png'))
  page.keyboard.press('Escape')
  report['responsive'].append({'width':width,'overflow':False,'uncropped_images':True,'viewer_controls_visible':True})
  if width in [390,1440]:
   page.add_script_tag(path=str(ROOT/'tools/axe.min.js'))
   for state in ['page','activities','viewer','menu']:
    if state=='activities':page.locator('.events-activity-list details').evaluate_all('els=>els.forEach(e=>e.open=true)')
    if state=='viewer':page.locator('[data-event-open]').first.click()
    if state=='menu':
     page.set_viewport_size({'width':390,'height':844});page.locator('.menu-toggle').click()
    v=page.evaluate('async()=>{const r=await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}});return r.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))}')
    report['accessibility'].append({'width':width,'state':state,'violations':v})
    if state in ['viewer','menu']:page.keyboard.press('Escape')
 context=browser.new_context(java_script_enabled=False)
 p=context.new_page();p.goto((ROOT/'events.html').as_uri());assert p.locator('.event-photo').count()==7
 p.locator('[data-event-open]').first.click();assert '/originals/' in p.url
 report['no_js_gallery']='passed';browser.close()
(OUT/'events-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert not report['errors'];assert not report['external_requests'];assert not any(x['violations'] for x in report['accessibility'])
