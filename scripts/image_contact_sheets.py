"""Produce local visual QA sheets, never publish a site."""
import json, math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT=Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding='utf8')
m=json.loads((ROOT/'research/images/manifest.json').read_text(encoding='utf8'))
items=[x for x in m['images'].values() if x['status']=='prepared']
out=ROOT/'research/images/contact-sheets';out.mkdir(exist_ok=True,parents=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
index=[]
for page in range(math.ceil(len(items)/70)):
    batch=items[page*70:(page+1)*70]
    sheet=Image.new('RGB',(1400,7*220),(238,240,244));draw=ImageDraw.Draw(sheet)
    for cell,item in enumerate(batch):
        x=(cell%10)*140;y=(cell//10)*220
        im=Image.open(ROOT/item['local']['poster']);im=ImageOps.contain(im,(124,178))
        sheet.paste(im,(x+(140-im.width)//2,y))
        num=page*70+cell+1;title=item['selection']['title']
        label=f'{num}. {title}'
        draw.text((x+3,y+181),label[:23],fill=(0,0,0),font=font)
        draw.text((x+3,y+197),label[23:46],fill=(0,0,0),font=font)
        index.append({'number':num,'image_id':item['id'],'title':item['title'],'artwork_title':title,'sheet':page+1})
    path=out/f'covers-{page+1:02d}.jpg';sheet.save(path,quality=90)
    print(str(path))
(out/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
