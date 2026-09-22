"""Photo-led team section with owner-supplied coach names only."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]

def build_coaches(founder):
    manifest=json.loads((ROOT/'tools/coaches-manifest.json').read_text(encoding='utf-8'))
    cards=[]
    for person in manifest['items']:
        name=escape(person['name'])
        language=' lang="mr"' if person['name']=='साहिल हेगडकर' else ''
        cards.append(f'''<article class="coach-card"><figure class="coach-photo"><img src="{escape(person['display'])}" width="{person['width']}" height="{person['height']}" loading="lazy" decoding="async" alt="{name} — coach at Royal Sports Academy"></figure><div class="coach-caption"><h3 class="coach-name"{language}>{name}</h3><p>Coach</p></div></article>''')
    return '''<section class="home-team section" id="our-team" aria-labelledby="team-title"><div class="wrap"><header class="team-heading"><h2 id="team-title">Your professional coaches</h2></header><div class="coaches-grid">'''+''.join(cards)+'''</div>'''+founder+'''</div></section>'''
