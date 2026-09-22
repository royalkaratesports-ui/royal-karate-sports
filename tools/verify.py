from pathlib import Path
import json,re
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification'; OUT.mkdir(exist_ok=True)
issues=[]; results=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 for width,height in [(1440,1000),(768,1024),(390,844),(320,740)]:
  for file in sorted(ROOT.glob('*.html')):
   page=browser.new_page(viewport={'width':width,'height':height})
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   page.goto(file.as_uri());page.evaluate('document.fonts.ready');page.wait_for_timeout(60)
   page.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
   page.wait_for_function("Array.from(document.images).every(i=>i.complete)")
   page.evaluate("Promise.all(Array.from(document.images).map(i=>i.decode().catch(()=>{})))")
   page.evaluate("document.documentElement.style.scrollBehavior='auto'")
   for y in range(0,page.evaluate("document.body.scrollHeight"),height):
    page.evaluate("y=>window.scrollTo(0,y)",y);page.wait_for_timeout(40)
   page.evaluate("window.scrollTo(0,0)");page.wait_for_timeout(100)
   data=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth,h1:document.querySelectorAll('h1').length,badImages:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),fonts:document.fonts.check('700 20px Barlow')&&document.fonts.check('400 16px Manrope')})''')
   row={'page':file.name,'width':width,**data,'errors':errors};results.append(row)
   if data['overflow'] or data['h1']!=1 or data['badImages'] or errors or not data['fonts']:issues.append(row)
   if width in [1440,390] and file.name in ['index.html','trial.html','gallery.html','locations.html','about-akash-shinde.html','academy.html','kids-batches.html','adult-batches.html','media.html']:
    page.screenshot(path=str(OUT/f'{file.stem}-{width}.png'),full_page=True)
    if file.name=='index.html':page.screenshot(path=str(OUT/f'hero-{width}.png'))
   page.close()
 browser.close()
for file in ROOT.glob('*.html'):
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 for el in soup.select('[href],[src]'):
  ref=el.get('href') or el.get('src');parsed=urlsplit(ref)
  if parsed.scheme or ref.startswith('//'):continue
  target=ROOT/unquote(parsed.path) if parsed.path else file
  if not target.exists():issues.append({'page':file.name,'missing':ref})
  elif parsed.fragment and target.suffix=='.html':
   ts=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
   if not ts.find(id=parsed.fragment):issues.append({'page':file.name,'missingFragment':ref})
report={'viewports_checked':len(results),'pages':len(list(ROOT.glob('*.html'))),'issues':issues,'results':results}
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'viewports_checked':len(results),'pages':report['pages'],'issues':issues},indent=2))
assert not issues
