"""Inventory exact attachments; preserve originals and deduplicate decoded pixels."""
from pathlib import Path
from PIL import Image,ImageOps
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('C:/Users/Yantra 12/Downloads/Dr shinde')

def inventory():
 names=json.loads((ROOT/'tools/achievements-inputs.json').read_text())
 dest=ROOT/'assets/achievements/originals';dest.mkdir(parents=True,exist_ok=True)
 items=[];seen={}
 for index,name in enumerate(names,1):
  source=SOURCE/name;shutil.copy2(source,dest/name)
  im=ImageOps.exif_transpose(Image.open(source)).convert('RGB')
  digest=hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()
  if digest in seen:
   seen[digest]['sources'].append(name);continue
  item={'id':f'achievement-{index:02d}','sources':[name],'original':f'assets/achievements/originals/{name}','width':im.width,'height':im.height,'pixel_hash':digest,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
  seen[digest]=item;items.append(item)
 data={'input_count':len(names),'unique_count':len(items),'items':items}
 (ROOT/'tools/achievements-manifest.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
 print(json.dumps({'inputs':len(names),'unique':len(items),'duplicates':[x['sources'] for x in items if len(x['sources'])>1]}))
 return data

if __name__=='__main__':inventory()
