"""All-route viewport, assets, links and render evidence for the new template."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification'/'redesign';OUT.mkdir(parents=True,exist_ok=True)
PAGES=sorted(ROOT.glob('*.html'))
EXPECTED={x['route'] for x in json.loads((ROOT/'verification/redesign-audit.json').read_text(encoding='utf-8'))}
assert {x.name for x in PAGES}==EXPECTED,'Route set changed unexpectedly'
issues=[]; rows=[]

def save():
    report={'pages':len(PAGES),'viewports_checked':len(rows),'issues':issues,'results':rows}
    (ROOT/'verification/report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

with sync_playwright() as pw:
    browser=pw.chromium.launch()
    for file in PAGES:
        for width in (320,390,768,1024,1440):
            page=browser.new_page(viewport={'width':width,'height':900 if width>760 else 844},reduced_motion='reduce')
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
            try:
                page.goto(file.as_uri());page.evaluate('document.fonts.ready')
                page.evaluate("async()=>{for(const i of document.querySelectorAll('img[src]')){i.loading='eager';await Promise.race([i.decode().catch(()=>{}),new Promise(r=>setTimeout(r,5000))]);}}")
                data=page.evaluate("""()=>({overflow:document.documentElement.scrollWidth>innerWidth,h1:document.querySelectorAll('h1').length,badImages:[...document.querySelectorAll('img[src]')].filter(i=>!i.naturalWidth).map(i=>i.getAttribute('src')),font:document.fonts.check('700 20px Manrope')})""")
                row={'page':file.name,'width':width,**data,'errors':errors};rows.append(row)
                if data['overflow'] or data['h1']!=1 or data['badImages'] or errors or not data['font']:issues.append(row)
                if width in (390,1440):
                    for img in page.locator('main img[src]').all():
                        if img.is_visible():img.scroll_into_view_if_needed()
                    page.evaluate("scrollTo({top:0,behavior:'instant'})");page.wait_for_timeout(60)
                    page.screenshot(path=str(OUT/f'{file.stem}-{width}-full.png'),full_page=True)
                    page.screenshot(path=str(OUT/f'{file.stem}-{width}-top.png'))
            except Exception as e:
                issues.append({'page':file.name,'width':width,'exception':str(e)})
            page.close()
            save()
    browser.close()
for file in PAGES:
    soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
    ids=[x['id'] for x in soup.select('[id]')]
    if len(ids)!=len(set(ids)):issues.append({'page':file.name,'duplicateIds':True})
    for el in soup.select('[href],[src]'):
        ref=el.get('href') or el.get('src')
        parsed=urlsplit(ref)
        if parsed.scheme or ref.startswith('//'):continue
        target=ROOT/unquote(parsed.path) if parsed.path else file
        if not target.exists():issues.append({'page':file.name,'missing':ref})
        elif parsed.fragment and target.suffix=='.html':
            ts=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
            if not ts.find(id=parsed.fragment):issues.append({'page':file.name,'missingFragment':ref})
save()
print(json.dumps({'pages':len(PAGES),'viewports_checked':len(rows),'issues':issues},indent=2))
assert len(rows)==len(PAGES)*5
assert not issues
