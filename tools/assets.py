from pathlib import Path
import requests, concurrent.futures, json
from PIL import Image, ImageOps, ImageDraw
root=Path(__file__).resolve().parents[1]
(root/'assets').mkdir(exist_ok=True)
ids=[7045397,7045393,7045395,7045587,7045595,7045588,7045606,7045453,7045456,7045466,7045473,7045484]
def get(i):
 try:
  r=requests.get(f'https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg?auto=compress&cs=tinysrgb&w=1600',timeout=30); r.raise_for_status()
  p=root/'assets'/f'{i}.jpg'; p.write_bytes(r.content)
  im=Image.open(p); return i,im.size
 except Exception as e:return i,str(e)
results=list(concurrent.futures.ThreadPoolExecutor(8).map(get,ids)); print(results)
sheet=Image.new('RGB',(1200,900),'white'); d=ImageDraw.Draw(sheet)
for n,(i,status) in enumerate(results):
 try:
  im=Image.open(root/'assets'/f'{i}.jpg'); im=ImageOps.fit(im,(300,260)); x=n%4*300;y=n//4*300;sheet.paste(im,(x,y));d.text((x+8,y+270),str(i),fill='black')
 except:pass
sheet.save(root/'contact-sheet.jpg')
