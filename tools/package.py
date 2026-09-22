from pathlib import Path
import zipfile,json,hashlib,tempfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
photos=sorted((ROOT/'assets').glob('*.webp'))
lines=['# Asset provenance','','## Photographs','','The numbered images are illustrative stock imagery, not Royal Karate Sports people, premises, competition results or endorsements. The named Akash Kishor Shinde portrait, royal-academy-group photograph and kids-*/adults-* photographs are user-supplied, listed separately below. Stock photographs were downloaded from the public Pexels image CDN and resized/re-encoded to WebP locally. Source photo pages and applicable license must be checked before public launch. No competitor imagery is included.','','Pexels license reference: https://www.pexels.com/license/','','| Local file | Source page | Original image |','|---|---|---|']
for p in photos:
 i=p.stem
 if i.isdigit():lines.append(f'| assets/{p.name} | https://www.pexels.com/photo/{i}/ | https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg |')
 elif i.startswith('adults-'):
  supplied={'adults-archive-group':'165dcd72-eb3e-4909-b93c-afbb82a3395f (1).jpg','adults-archive-athletes':'1906aaa2-9cf1-4675-92c1-ec9e9e225623.jpg','adults-archive-community':'4701ceed-3cee-4954-b21c-d39b556f96e7.jpg','adults-shotokan':'image_477f72.png','adults-class-practice':'image_7a03e6.png'}
  lines.append(f'| assets/{p.name} | User-supplied adult-page photograph (not stock) | Original attachment {supplied[i]}; full frame retained |')
 elif i.startswith('kids-'):
  supplied={'kids-line-practice':'image_83292b.png','kids-group-training':'image_1cf642.png','kids-first-steps':'image_1d053d.png'}
  lines.append(f'| assets/{p.name} | User-supplied kids training photo (not stock) | Original attachment {supplied[i]}; full frame retained |')
 elif i=='royal-academy-group':lines.append(f'| assets/{p.name} | User-supplied academy group photo (not stock) | Original attachment f304aa50-489d-46d8-a0cf-82d5b89b6604_2ddf2b.jpg; full frame retained |')
 else:lines.append(f'| assets/{p.name} | User-supplied Akash Kishor Shinde portrait (not stock) | Original attachment 91a62ceb-3186-44c5-bdb2-038f38c6f20e.jpg; full frame retained |')
press_manifest=json.loads((ROOT/'tools/media-manifest.json').read_text(encoding='utf-8'))
lines+=['','## Media archive','','26 supplied files; 23 unique images after exact pixel deduplication. Originals are retained byte-for-byte; WebP thumbnails are derived. No authenticity or government recognition is implied by inclusion. See tools/media-manifest.json for hashes and duplicate provenance.','']
for item in press_manifest['items']:
 lines.append('- '+item['original']+' — '+', '.join(item['sources']))
lines+=['','## Fonts','','- Barlow Condensed Bold: https://github.com/google/fonts/tree/main/ofl/barlowcondensed — assets/display.ttf, static weight 700.','- Manrope variable: https://github.com/google/fonts/tree/main/ofl/manrope — assets/body.ttf, variable weights.','- SIL Open Font License texts are bundled as assets/barlowcondensed-OFL.txt and assets/manrope-OFL.txt.','','## Brand mark','','Owner-supplied Royal Sports & Martial Arts Academy logo. Latest maroon/white attachment image_438c6f.png is used in the header, mobile menu, footer and browser icons. Only its exterior baked checkerboard was removed; lettering, figure and inner white field remain intact. Both supplied original versions are preserved in assets/brand/originals/. See tools/logo-manifest.json for the source hash and treatment.','','## Research only','','- Nike: https://www.nike.com/','- Equinox: https://www.equinox.com/','- Evolve: https://evolve-mma.com/','- Content taxonomy only: https://championskarateclub.com/']
achievement_manifest=json.loads((ROOT/'tools/achievements-manifest.json').read_text())
lines+=['','## Achievements archive','','21 supplied attachments; 20 unique images. All 21 byte-preserved originals are bundled under assets/achievements/originals/. Display copies rotate four sideways scans without cropping. See tools/achievements-labels.json and ACHIEVEMENTS-CONTENT.md for caption evidence; inclusion is not independent award verification.','']
for item in achievement_manifest['items']:
 lines.append('- '+item['display']+' — '+', '.join(item['sources']))
events_manifest=json.loads((ROOT/'tools/events-manifest.json').read_text())
lines+=['','## Events archive','','8 user-supplied files, 7 unique full-frame photographs. Original files are preserved byte-for-byte in assets/events/originals/. No dates or camp seasons are inferred from photos. See EVENTS-CONTENT.md.','']
for item in events_manifest['items']:
 lines.append('- '+item['image']+' — '+', '.join(item['sources']))
coach_manifest=json.loads((ROOT/'tools/coaches-manifest.json').read_text(encoding='utf-8'))
lines+=['','## Coaching team','','The owner supplied these photos and identified the coach names from their filenames. No qualifications or ranks are inferred. Originals are byte-preserved. Only blank white side margins were trimmed from the Sahil display copy; photographic content is retained.','']
for item in coach_manifest['items']:
 lines.append('- '+item['display']+' — '+item['name']+'; original: '+item['original'])
(ROOT/'ASSETS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
files = sorted(ROOT.glob('*.html')) + [ROOT/'royal.css', ROOT/'royal-pages.css']
files += sorted(ROOT.glob('*.js')) + sorted(ROOT.glob('*.md'))
files += [ROOT/name for name in ('requirements-dev.txt','.gitignore','.gitattributes','.nojekyll')]
files += [p for p in (ROOT/'assets').rglob('*') if p.is_file()]
files += sorted((ROOT/'tools').glob('*.py')) + sorted((ROOT/'tools').glob('*.json')) + [ROOT/'tools/axe.min.js']
files += [ROOT/'verification/report.json', ROOT/'verification/accessibility.json', ROOT/'verification/redesign-audit.json', ROOT/'verification/redesign-suite-final.log', ROOT/'verification/inner-audit.md', ROOT/'verification/logo-report.json', ROOT/'verification/logo-suite.log']
files=sorted(set(files))
manifest={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(ROOT/'verification/package-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
files.append(ROOT/'verification/package-manifest.json')
archive=ROOT.parent/'Royal-Karate-Sports-v19.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,'royal-karate-sports/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 with tempfile.TemporaryDirectory() as tmp:
  z.extractall(tmp);extracted=Path(tmp)/'royal-karate-sports'
  for name,digest in manifest.items():assert hashlib.sha256((extracted/name).read_bytes()).hexdigest()==digest
  with sync_playwright() as pw:
   b=pw.chromium.launch();s=b.new_page();errors=[];s.on('pageerror',lambda e:errors.append(str(e)))
   s.goto((extracted/'index.html').as_uri())
   assert s.locator('a.brand img.brand-logo').count()==3
   for logo in s.locator('a.brand img.brand-logo').all():
    logo.evaluate('(i)=>i.decode()');assert logo.evaluate('(i)=>i.naturalWidth===512')
   s.locator('#tab-adults').click();assert 'adults-class-practice' in s.locator('#program-image').get_attribute('src')
   s.locator('#program-link').click();assert s.url.endswith('programs.html#adults')
   s.locator('#adults .button').click();assert s.locator('#contact-topic').input_value()=='regular-classes'
   s.goto((extracted/'about-akash-shinde.html').as_uri());s.evaluate('document.fonts.ready')
   portrait=s.locator('.profile-portrait img');portrait.evaluate('(i)=>i.decode()')
   assert portrait.evaluate('(i)=>i.naturalWidth===720&&i.naturalHeight===960')
   assert 'Akash Kishor Shinde' in s.title()
   assert s.locator('.profile-hero').evaluate('(e)=>getComputedStyle(e).display')=='grid'
   assert 'Free Karate Training.' in s.locator('main').text_content()
   s.goto((extracted/'academy.html').as_uri());s.evaluate('document.fonts.ready')
   assert 'About Royal Sports Academy' in s.title()
   group=s.locator('.academy-opening img');group.evaluate('(i)=>i.decode()')
   assert group.get_attribute('src')=='assets/royal-academy-group.webp'
   assert group.evaluate('(i)=>i.naturalWidth===960&&i.naturalHeight===720')
   assert s.locator('.academy-opening').evaluate('(e)=>getComputedStyle(e).display')=='grid'
   assert 'nomination record rather than receipt of a Padma Award' in s.locator('main').text_content()
   s.locator('main').get_by_role('link',name='Read Akash Shinde’s full profile').click()
   assert s.url.endswith('about-akash-shinde.html')
   s.goto((extracted/'kids-batches.html').as_uri());s.evaluate('document.fonts.ready')
   assert s.locator('main img').count()==3
   for image in s.locator('main img').all():
    image.evaluate('(i)=>{i.loading="eager";return Promise.race([i.decode(),new Promise((_,reject)=>setTimeout(()=>reject(new Error("Image decode timeout: "+i.src)),5000))])}');assert image.evaluate('(i)=>i.naturalWidth>0')
   assert s.locator('.kids-hero').evaluate('(e)=>getComputedStyle(e).display')=='grid'
   s.locator('main').get_by_role('link',name='Enquire for your child',exact=True).first.click()
   assert s.locator('#contact-topic').input_value()=='regular-classes'
   s.goto((extracted/'adult-batches.html').as_uri());s.evaluate('document.fonts.ready')
   assert s.locator('main img').count()==5
   for image in s.locator('main img').all():
    image.evaluate('(i)=>{i.loading="eager";return Promise.race([i.decode(),new Promise((_,reject)=>setTimeout(()=>reject(new Error("Image decode timeout: "+i.src)),5000))])}');assert image.evaluate('(i)=>i.naturalWidth>0')
   assert s.locator('.adults-hero').evaluate('(e)=>getComputedStyle(e).display')=='grid'
   s.locator('main').get_by_role('link',name='Enquire for adult training',exact=True).first.click()
   assert s.locator('#contact-topic').input_value()=='regular-classes'
   s.goto((extracted/'media.html').as_uri());s.evaluate('document.fonts.ready')
   assert s.locator('.press-grid figure').count()==press_manifest['unique_count']
   for image in s.locator('.press-grid img').all():
    image.evaluate('(i)=>{i.loading="eager";return Promise.race([i.decode(),new Promise((_,r)=>setTimeout(()=>r(new Error("decode timeout")),5000))])}')
   s.locator('[data-media-filter="records"]').click()
   s.locator('.press-grid figure:visible [data-press-open]').first.click()
   assert s.locator('#press-viewer').is_visible()
   s.locator('#press-viewer-image').evaluate('(i)=>i.decode()')
   s.locator('[data-press-zoom]').click();assert s.locator('[data-press-zoom]').get_attribute('aria-pressed')=='true'
   s.keyboard.press('Escape');assert not s.locator('#press-viewer').is_visible()
   assert not errors;b.close()
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'packaged_files':len(files),'pages':len(list(ROOT.glob('*.html'))),'photographs':len(photos),'archive_integrity':'passed','extracted_navigation_and_program_preselection':'passed'},indent=2))
