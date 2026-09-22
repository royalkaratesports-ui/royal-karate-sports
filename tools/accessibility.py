from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
report=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':950})
  for file in sorted(root.glob('*.html')):
   page.goto(file.as_uri());page.evaluate('document.fonts.ready')
   page.add_script_tag(path=str(root/'tools/axe.min.js'))
   result=page.evaluate("axe.run(document, {runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
   violations=[{'id':v['id'],'impact':v['impact'],'nodes':[{'target':n['target'],'summary':n['failureSummary']} for n in v['nodes']]} for v in result['violations']]
   report.append({'page':file.name,'width':width,'violations':violations})
  page.close()
 b.close()
(root/'verification/accessibility.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
errors=[r for r in report if r['violations']]
print(json.dumps({'checks':len(report),'violations':errors},indent=2))
assert not errors
