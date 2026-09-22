"""Responsive/accessibility/link audit of every generated simple-theme page."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification'
files=sorted(ROOT.glob('*.html'))
report={'pages':[p.name for p in files],'checks':[],'errors':[],'broken_links':[],'accessibility':[]}
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    page=browser.new_page(reduced_motion='reduce')
    for file in files:
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(file.as_uri())
        page.evaluate("async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>{i.loading='eager';return i.decode().catch(()=>{})}))}")
        for href in page.locator('a[href]').evaluate_all('(es)=>es.map(e=>e.getAttribute("href"))'):
            url=urlsplit(href)
            if url.scheme or url.netloc:continue
            target=(file.parent/unquote(url.path)) if url.path else file
            if not target.exists():report['broken_links'].append({'page':file.name,'href':href})
            elif url.fragment and target.suffix=='.html':
                from html.parser import HTMLParser
                class IDs(HTMLParser):
                    def __init__(self):super().__init__();self.ids=set()
                    def handle_starttag(self,tag,attrs):self.ids.update(v for k,v in attrs if k=='id')
                parser=IDs();parser.feed(target.read_text(encoding='utf-8'))
                if unquote(url.fragment) not in parser.ids:report['broken_links'].append({'page':file.name,'href':href,'error':'missing anchor'})
        bad=page.locator('img[src]').evaluate_all('(es)=>es.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute("src"))')
        if bad:report['errors'].append({'page':file.name,'images':bad})
        page.add_script_tag(path=str(ROOT/'tools/axe.min.js'))
        for width in (320,390,768,1024,1440):
            page.set_viewport_size({'width':width,'height':900 if width>760 else 844})
            overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth')
            report['checks'].append({'page':file.name,'width':width,'overflow':overflow})
            if width in (390,1440):
                result=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
                report['accessibility'].append({'page':file.name,'width':width,'violations':[{'id':v['id'],'nodes':[{'target':n['target'],'summary':n.get('failureSummary')} for n in v['nodes']]} for v in result['violations']]})
                if file.name in ['index.html','contact.html','events.html','achievements.html','about-akash-shinde.html','kids-batches.html']:
                    for img in page.locator('main img:visible').all():img.scroll_into_view_if_needed()
                    page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                    page.screenshot(path=str(OUT/f'simple-{file.stem}-{width}.png'),full_page=True)
                    page.screenshot(path=str(OUT/f'simple-{file.stem}-top-{width}.png'))
        if errors:report['errors'].append({'page':file.name,'javascript':errors})
        (OUT/'simple-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    browser.close()
print(json.dumps({'pages':len(report['pages']),'responsive_checks':len(report['checks']),'overflows':[x for x in report['checks'] if x['overflow']],'errors':report['errors'],'broken_links':report['broken_links'],'accessibility_violations':[x for x in report['accessibility'] if x['violations']]},indent=2))
assert not any(x['overflow'] for x in report['checks'])
assert not report['errors'] and not report['broken_links']
assert not any(x['violations'] for x in report['accessibility'])
