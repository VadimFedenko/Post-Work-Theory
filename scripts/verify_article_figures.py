"""Check the minimal inline figures and article embedding."""
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'research/article-infographics'


def main():
    article=(ROOT/'article.md').read_text('utf8')
    manifest=json.loads((AUDIT/'manifest.json').read_text('utf8'))
    assert manifest['input_sha256']==hashlib.sha256((ROOT/'data/societies.json').read_bytes()).hexdigest()
    assert len(manifest['figures'])==8
    assert article.count('](reference.png)')==1
    assert article.count('<summary>English</summary>')==4
    assert not re.search(r'research/article-infographics|Методика и данные|SVG RU|SVG EN|редакторская разметка',article,re.I)
    assert not any(x in article for x in ['01-infrastructure','03-six-regimes','04-elite-guarantees-examples','05-work-postwork-matrices','06-regime-dystopia'])
    forbidden=['источник','source:','data/societies','редакторск','editorial','субъективн','subjective','18 selected','18 выбранных','Продвинутые технологии','Advanced technology still','У трудовых миров','One regime dominates','Стадия описывает','У трудовых обществ уклад','Два вопроса','Two questions','545 post-work','545 посттрудовых']
    for fig in manifest['figures']:
        assert article.count('('+fig['png']+')')==1
        with Image.open(ROOT/fig['png']) as im:assert im.size==(fig['width'],fig['height'])
        svg=ET.parse(ROOT/fig['svg'])
        text=' '.join(t.text or '' for t in svg.findall('.//{http://www.w3.org/2000/svg}text'))
        assert not any(s.lower() in text.lower() for s in forbidden),(fig['png'],text)
        assert not re.search(r'[CD]:[\\/]',text)
        if fig['lang']=='en':assert not re.search('[А-Яа-яЁё]',text)
        if fig['key']=='06-guarantees':
            assert '58%' in text and '14%' in text
            assert len(svg.findall('.//{http://www.w3.org/2000/svg}rect'))==2
        if fig['key']=='05-regime-composition':
            assert all(str(n) in text for n in [345,75,470])
            assert ('65,5%' if fig['lang']=='ru' else '65.5%') in text
        if fig['key']=='02-technology-work':
            assert ('Ромб — медиана обществ' if fig['lang']=='ru' else 'Diamond: median') in text

    rendered=BeautifulSoup((AUDIT/'article-preview.html').read_text('utf8'),'html.parser')
    images=[i for i in rendered.find_all('img') if i.get('src','').startswith('assets/infographics/article/') or i.get('src')=='reference.png']
    assert len(images)==9
    assert len([i for i in images if i.find_parent('details')])==4
    assert not any(i.get('src','').endswith('01-infrastructure-ru.png') for i in rendered.find_all('img'))
    collisions=[]
    for f in json.loads((AUDIT/'.build/text-geometry.json').read_text('utf8')):
        for i,a in enumerate(f['texts']):
            for b in f['texts'][i+1:]:
                if a['text']==b['text'] and a['bbox']==b['bbox']:continue
                x,y,w,h=a['bbox'];xx,yy,ww,hh=b['bbox']
                area=max(0,min(x+w,xx+ww)-max(x,xx))*max(0,min(y+h,yy+hh)-max(y,yy))
                if area>5:collisions.append({'file':f['file'],'a':a['text'],'b':b['text'],'area':area})
    assert not collisions,collisions
    result={'generated_images':8,'original_reference':True,'article_placements':5,'languages':['ru','en'],
            'no_generated_titles_sources_or_commentary':True,'article_has_no_methodology_links':True,
            'guarantees_percentages':[r['percent'] for r in manifest['guarantees']],'text_collisions':collisions}
    (AUDIT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
