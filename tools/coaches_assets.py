"""Ingest the three owner-identified coaches without altering originals."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path.home()/'Pictures/Downloads'
INPUTS=[('Amar Dabade.webp','amar-dabade'),('Mayur Dilawar.webp','mayur-dilawar'),('साहिल हेगडकर.webp','sahil-hegadkar')]
items=[]
for filename,slug in INPUTS:
    original=ROOT/'assets/coaches/originals'/filename
    display=ROOT/'assets/coaches'/f'{slug}.webp'
    original.parent.mkdir(parents=True,exist_ok=True)
    if not original.exists():shutil.copy2(SOURCE/filename,original)
    image=Image.open(original).convert('RGB')
    bounds=(0,0,*image.size)
    if slug=='sahil-hegadkar':
        # The supplied square image has blank white side margins. Retain
        # every photographic pixel; no face, body or equipment is cropped.
        mask=ImageChops.difference(image,Image.new('RGB',image.size,'white')).convert('L').point(lambda p:255 if p>12 else 0)
        left,top,right,bottom=mask.getbbox()
        bounds=(max(0,left-2),0,min(image.width,right+2),image.height)
        image=image.crop(bounds)
        image.save(display,'WEBP',quality=95,method=6)
    else:shutil.copy2(original,display)
    items.append({'name':Path(filename).stem,'source':filename,'original':original.relative_to(ROOT).as_posix(),'display':display.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'width':image.width,'height':image.height,'display_crop':list(bounds)})
manifest={'supplied_count':len(INPUTS),'displayed_count':len(items),'identity_source':'Names and coach roles supplied by the website owner. No qualifications or ranks inferred.','items':items}
(ROOT/'tools/coaches-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'preserved':len(items),'display_files':[x['display'] for x in items],'dimensions':[[x['width'],x['height']] for x in items]},indent=2))
