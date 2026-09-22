from pathlib import Path
from PIL import Image,ImageOps
import json,hashlib,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else Path('C:/Users/Yantra 12/Downloads/Dr shinde')
names=json.loads((ROOT/'tools/events-inputs.json').read_text())
folder=ROOT/'assets/events';(folder/'originals').mkdir(parents=True,exist_ok=True)
labels=[('Together at an academy gathering','A large group of karate students and adults posing indoors.'),('Certificates, medals and shared progress','Karate practitioners seated and standing on mats, holding certificates and wearing medals.'),('An outdoor presentation','A group outside a building with people at the centre holding a document.'),('A moment with the team','Karate practitioners wearing medals posing outdoors alongside two adults.'),('The wider academy community','A wide group photograph of karate students in uniform and adults at an indoor gathering.'),('Celebrating young practitioners','Young karate practitioners wearing medals posing with adults in front of a white backdrop.'),('The people around the practice','A line of adults posing indoors in front of an event banner.'),('Celebrating young practitioners','Young karate practitioners wearing medals posing with adults in front of a white backdrop.')]
items=[];seen={}
for i,(name,label) in enumerate(zip(names,labels),1):
 source=SOURCE/name
 if not source.exists():
  candidates=list(SOURCE.rglob(name))
  if len(candidates)!=1:raise FileNotFoundError(f'Expected one source for {name}; found {len(candidates)}')
  source=candidates[0]
 dest=folder/'originals'/name
 if source.resolve()!=dest.resolve():shutil.copy2(source,dest)
 sha=hashlib.sha256(dest.read_bytes()).hexdigest()
 im=ImageOps.exif_transpose(Image.open(dest)).convert('RGB')
 pixels=hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()
 if pixels in seen:
  seen[pixels]['sources'].append(name);seen[pixels]['source_hashes'][name]=sha;continue
 asset=f'assets/events/event-{i:02d}.webp';im.save(ROOT/asset,quality=92,method=6)
 item={'id':f'event-{i:02d}','sources':[name],'source_hashes':{name:sha},'pixel_hash':pixels,'image':asset,'original':f'assets/events/originals/{name}','width':im.width,'height':im.height,'title':label[0],'alt':label[1]}
 seen[pixels]=item;items.append(item)
data={'input_count':len(names),'unique_count':len(items),'items':items}
(ROOT/'tools/events-manifest.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps({'inputs':len(names),'unique':len(items),'duplicates':[x['sources'] for x in items if len(x['sources'])>1]}))
