"""Inventory supplied media, retain originals, deduplicate identical pixels."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path.home()/'Downloads'/'Dr shinde'
names=json.loads((ROOT/'tools/media-inputs.json').read_text())
assert len(names)==26 and len(set(names))==26
out=ROOT/'assets/press';out.mkdir(exist_ok=True)
items=[];seen={}
for n in names:
    source=SOURCE/n
    image=ImageOps.exif_transpose(Image.open(source)).convert('RGB')
    pixels=hashlib.sha256(str(image.size).encode()+image.tobytes()).hexdigest()
    if pixels in seen:
        seen[pixels]['sources'].append(n)
        continue
    id=f'press-{len(items)+1:02d}'
    row={'id':id,'sources':[n],'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pixels_sha256':pixels,'width':image.width,'height':image.height,'original':f'assets/press/{id}.jpg','thumbnail':f'assets/press/{id}.webp'}
    shutil.copyfile(source,ROOT/row['original'])
    thumb=ImageOps.contain(image,(700,850));thumb.save(ROOT/row['thumbnail'],quality=88,method=6)
    items.append(row);seen[pixels]=row
manifest={'input_count':len(names),'unique_count':len(items),'duplicate_count':len(names)-len(items),'items':items}
(ROOT/'tools/media-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for batch in range(0,len(items),6):
    sheet=Image.new('RGB',(1000,1170),'#e6e6e1');draw=ImageDraw.Draw(sheet)
    for k,row in enumerate(items[batch:batch+6]):
        im=ImageOps.exif_transpose(Image.open(ROOT/row['original'])).convert('RGB');thumb=ImageOps.contain(im,(475,345))
        x=(k%2)*500;y=(k//2)*390
        sheet.paste(thumb,(x+(500-thumb.width)//2,y+28))
        draw.text((x+12,y+7),row['id']+' | '+str(im.size),fill='black')
    sheet.save(ROOT/'verification'/f'press-sheet-{batch//6+1}.jpg')
print(json.dumps({'input_count':len(names),'unique_count':len(items),'duplicates':[x['sources'] for x in items if len(x['sources'])>1],'sheets':(len(items)+5)//6},indent=2))
