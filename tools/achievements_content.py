"""Original academy archive, captions grounded in supplied photographs and documents."""
from pathlib import Path
from html import escape as esc
from PIL import Image,ImageOps
import json
ROOT=Path(__file__).resolve().parents[1]
CATEGORIES={'awards':'Awards & honours','competition':'Competition records','community':'Community & service','moments':'Memorable moments'}

def build_achievements(button,link):
 data=json.loads((ROOT/'tools/achievements-manifest.json').read_text())
 labels=json.loads((ROOT/'tools/achievements-labels.json').read_text(encoding='utf-8'))
 assert set(labels)=={n for i in data['items'] for n in i['sources']}
 for item in data['items']:
  label=labels[item['sources'][0]]
  im=ImageOps.exif_transpose(Image.open(ROOT/item['original'])).convert('RGB')
  if label.get('rotate',0):im=im.rotate(label['rotate'],expand=True)
  item['display']=f"assets/achievements/{item['id']}-full.webp"
  item['thumbnail']=f"assets/achievements/{item['id']}.webp"
  im.save(ROOT/item['display'],quality=94,method=6)
  im.thumbnail((820,820));im.save(ROOT/item['thumbnail'],quality=88,method=6)
  item['display_width'],item['display_height']=Image.open(ROOT/item['display']).size
 (ROOT/'tools/achievements-manifest.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
 by_id={x['id']:x for x in data['items']}
 def photo(item,featured=False):
  m=labels[item['sources'][0]];title=esc(m['title']);alt=esc(m['alt'])
  return f'''<a href="{item['original']}" class="achievement-image" data-ach-open data-view="{item['display']}" data-title="{title}" data-note="{alt}" aria-label="View: {title}"><img src="{item['thumbnail']}" alt="{alt}" width="{item['display_width']}" height="{item['display_height']}" {'fetchpriority="high"' if featured else 'loading="lazy"'} decoding="async"><span class="achievement-open">View full image <span aria-hidden="true">↗</span></span></a>'''
 figures=[]
 for item in data['items']:
  m=labels[item['sources'][0]]
  figures.append(f'''<figure class="achievement-card" id="{item['id']}" data-ach-category="{m['category']}">{photo(item)}<figcaption><span class="achievement-type">{CATEGORIES[m['category']]}</span><h3>{esc(m['title'])}</h3></figcaption></figure>''')
 filters=''.join(f'<button type="button" data-ach-filter="{k}" aria-pressed="false">{v}</button>' for k,v in CATEGORIES.items())
 return f'''<article class="achievements-content">
 <section class="wrap achievements-opening"><div class="achievements-heading"><span class="eyebrow red">Trending / Achievements</span><h1>Recognition.<br>With purpose.</h1><p class="achievements-name">Akash Kishor Shinde · Royal Sports Academy</p><p>Awards, sporting milestones and moments of appreciation. Explore the records and photographs behind the journey.</p><a class="text-link" href="#achievement-archive">Explore the archive <span aria-hidden="true">↓</span></a></div><figure class="achievements-lead">{photo(by_id['achievement-15'],True)}<figcaption><span>Bharat Bhushan Samman · 2022</span><span>From the academy archive</span></figcaption></figure></section>
 <div class="achievements-intro-line wrap"><p>On the mat. In the community. Along the way.</p><a href="about-akash-shinde.html">Meet Akash Shinde <span aria-hidden="true">↗</span></a></div>
 <section class="achievements-archive" id="achievement-archive"><div class="wrap section"><div class="achievements-section-heading"><div><span class="eyebrow red">Certificates, honours & photographs</span><h2>A record of<br>the journey.</h2></div><p>Browse by category. Open any image to see the full frame, read the details or explore the original document.</p></div><div class="achievements-toolbar"><div class="achievements-filters" role="group" aria-label="Filter achievements"><button type="button" data-ach-filter="all" aria-pressed="true">All achievements</button>{filters}</div><p id="achievements-count" role="status">{data['unique_count']} archive items</p></div><noscript><p class="achievement-archive-note">All items are shown below. Select an image to open the original.</p></noscript><div class="achievements-grid">{''.join(figures)}</div><p class="achievement-archive-note">From the academy’s supplied collection. Duplicate scans are shown once; originals are retained. Captions describe the visible material, not independent verification of an issuer or award status. Image clarity varies with the original.</p></div></section>
 <section class="wrap section achievements-purpose"><div><span class="eyebrow red">The work continues</span><h2>The purpose stays<br>the same.</h2></div><div><p>Recognition is one part of the story. Making karate accessible is the continuing commitment.</p><p>Royal Sports Academy provides free karate training at Ganesh Vidyamandir School, Dharavi, and at Pratiksha Nagar, Mumbai.</p><div class="achievements-related">{link('About the academy','academy.html')}{link('Explore press coverage','media.html')}</div></div></section></article>'''+VIEWER

VIEWER='''<dialog id="achievement-viewer" aria-labelledby="achievement-viewer-title"><div class="achievement-viewer-head"><div><span class="eyebrow">The achievement archive</span><h2 id="achievement-viewer-title">Archive image</h2></div><button type="button" class="icon-button" data-ach-close aria-label="Close image">×</button></div><div class="achievement-viewer-tools"><button type="button" data-ach-prev aria-label="Previous image">← Previous</button><button type="button" data-ach-next aria-label="Next image">Next →</button><button type="button" data-ach-zoom aria-pressed="false">Zoom in</button><a id="achievement-original" href="#achievement-archive" target="_blank" rel="noopener">Open original ↗</a></div><div class="achievement-stage" tabindex="0" role="region" aria-label="Image; scroll to pan when zoomed"><img id="achievement-full" alt=""></div><div class="achievement-viewer-foot"><p id="achievement-position" role="status"></p><p id="achievement-note"></p></div></dialog><script src="achievements.js" defer></script>'''
