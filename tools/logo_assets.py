"""Prepare the supplied logo; remove only the exterior baked checkerboard.
Run with the latest supplied PNG path for initial ingestion, then without args.
The original artwork and internal white field are retained byte-for-byte in originals/.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import hashlib,json,shutil,sys,base64
ROOT=Path(__file__).resolve().parents[1]


def build_logo(source=None):
    folder=ROOT/'assets/brand';original=folder/'originals/royal-logo-owner.png'
    original.parent.mkdir(parents=True,exist_ok=True)
    if source:shutil.copy2(source,original)
    image=Image.open(original).convert('RGBA')
    # The opaque checkerboard is outside a continuous maroon outline. Trace its
    # outer row envelope; never remove white pixels inside the enclosed emblem.
    edges=[]
    for y in range(image.height):
        xs=[]
        for x in range(image.width):
            r,g,b,a=image.getpixel((x,y))
            if r-g>18 and r-b>18 and r>g*1.3 and r>b*1.3:xs.append(x)
        if xs:edges.append((min(xs),max(xs),y))
    if len(edges)<image.height*.8:raise ValueError('Unexpected outline; review the source before masking')
    polygon=[(left,y) for left,right,y in edges]+[(right,y) for left,right,y in reversed(edges)]
    mask=Image.new('L',image.size,0);ImageDraw.Draw(mask).polygon(polygon,fill=255)
    mask=mask.filter(ImageFilter.MaxFilter(3))
    image.putalpha(mask);bounds=mask.getbbox();image=image.crop(bounds)
    side=max(image.size)+8
    square=Image.new('RGBA',(side,side),(0,0,0,0));square.alpha_composite(image,((side-image.width)//2,(side-image.height)//2))
    for filename,size in [('royal-logo.png',512),('favicon.png',64),('apple-touch-icon.png',180)]:
        square.resize((size,size),Image.Resampling.LANCZOS).save(folder/filename,optimize=True)
    icon= square.resize((64,64),Image.Resampling.LANCZOS)
    icon.save(folder/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64)])
    # Keep the old favicon URL as a compatibility alias, with the NEW artwork.
    data=base64.b64encode((folder/'favicon.png').read_bytes()).decode('ascii')
    (ROOT/'assets/favicon.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><image width="64" height="64" href="data:image/png;base64,{data}"/></svg>',encoding='utf-8')
    manifest={'original':str(original.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'source_filename':'image_438c6f.png','source_size':list(Image.open(original).size),'exterior_bounds':list(bounds),'display':'assets/brand/royal-logo.png','treatment':'Only exterior baked checkerboard removed using the existing maroon outline. Lettering, figure, colors and inner white field unchanged. Uniform scaling, no distortion.'}
    (ROOT/'tools/logo-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':build_logo(sys.argv[1] if len(sys.argv)>1 else None)
