"""Create a reproducible report extension and interactive stage comparisons."""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research'/'exploratory-analysis'
Z=json.loads((OUT/'transition-analysis.json').read_text(encoding='utf8'))
ST=Z['stage_order']
LABEL=['Трудовые','Частичный переход','Посттрудовые']
STC=['#7b8896','#d69c46','#277f75']
RC=['#d69c46','#ad654d','#277f75','#5c9d85','#6874b5','#9c5d91']
RL=['1 · Элиты + гарантии','2 · Элиты без гарантий','3 · Распределённый + гарантии','4 · Активы без гарантий','5 · Система + гарантии','6 · Система без гарантий']
ML={'book':'Книги','short_story':'Рассказы','anime':'Аниме','manga':'Манга','game':'Игры','tv':'Телевидение','movie':'Кино','comic':'Комиксы','cartoon':'Мультфильмы','tabletop':'Настольные игры','web_fiction':'Веб-проза'}
def f(v,d=2):return f'{v:.{d}f}'.replace('.',',')
def p(v):return f(v*100,1)+'%'
def co(model,term):return next(c for c in Z['models'][model]['coefficients'] if c['term']==term)
def ci(c):return f"{f(c['beta'])} [{f(c['low'])}; {f(c['high'])}]"
def test(model,term):return next(c for c in Z['tests'] if c['model']==model and c['term']==term)
sections=[];figures={};order={}
def add(key,md,plots=()):sections.append(dict(key=key,markdown=md.strip()));order[key]=list(plots)

add('transitions',f'''
## 11. Три стадии перехода и шесть укладов

[Открыть 9 слайдов](presentation/index.html) · [Скачать редактируемую презентацию](presentation/post-work-stages-v2.pptx)

Стадия перехода — самостоятельное поле `post_work_assessment.status`, которое разделяет прежнюю объединённую группу из 545 записей. Термин «посттрудовые» ниже относится только к 470 записям `post_work`; 75 `transition` рассматриваются отдельно.

| Стадия | Обществ | Доля базы | Групп узнаваемости |
|---|---:|---:|---:|
'''+ '\n'.join(f"| {label} | {Z['stages'][st]['n']} | {p(Z['stages'][st]['n']/890)} | {Z['stages'][st]['groups']} |" for st,label in zip(ST,LABEL))+'''

На круговых диаграммах нулевые варианты распределены по координатам так же, как в обновлённом графике медиа. Остальные общества сохраняют редакторские уклады 1–6. Это изображение устройства трудовых обществ, а не признание их перехода состоявшимся. Диаграммы одинакового размера сравнивают доли внутри стадии; размеры групп указаны явно.

| Уклад | Трудовые, n = 345 | Частичный переход, n = 75 | Посттрудовые, n = 470 |
|---|---:|---:|---:|
'''+ '\n'.join('| '+RL[k-1]+' | '+' | '.join(p(next(r for r in Z['regimes'] if r['stage']==st and r['regime']==k)['share'])+' ('+str(next(r for r in Z['regimes'] if r['stage']==st and r['regime']==k)['n'])+')' for st in ST)+' |' for k in range(1,7))+'''

Самый заметный сдвиг — доля элит без гарантий: **65,5% / 38,7% / 17,0%**. Полный переход представлен сразу несколькими устройствами: элиты с гарантиями 24,5%, распределённый контроль с гарантиями 24,7%, автономные системы с гарантиями 18,9%. Одна экономическая стадия не определяет единственного политического уклада.

Для проверки применена и единая классификация по координатам ко всем 890 обществам. Общая картина сохраняется: элиты без гарантий 65,5% / 36,0% / 18,3%; распределённый контроль с гарантиями 3,2% / 12,0% / 25,7%. Значит, крупные различия не возникают только из сочетания ручной и геометрической классификаций. Полные данные находятся в `transition-regime-counts.csv`.
''',['transition-pies'])

add('transition-polarity',f'''
## 12. Частичный и полный переход имеют одинаковое среднее, но разные хвосты

| Показатель | Трудовые | Частичный переход | Посттрудовые |
|---|---:|---:|---:|
'''+ '\n'.join('| '+name+' | '+' | '.join(fmt(Z['stages'][st][key]) for st in ST)+' |' for name,key,fmt in [
('Средняя U','mean_utopia',f),('Средняя U при равном весе групп','group_balanced_utopia',f),('Сильные дистопии, U ≤ −0,5','strong_dystopia_share',p),('Промежуточная зона, −0,5 < U < +0,5','central_share',p),('Сильные утопии, U ≥ +0,5','strong_utopia_share',p),('Средняя абсолютная U','mean_abs_utopia',f),('Стандартное отклонение U','std_utopia',f)])+f'''

У частичного перехода и посттрудовых обществ средняя оценка почти одинакова: **−0,119 и −0,115**. Однако у посттрудовых сильных утопий почти в пять раз больше: **18,9% против 4,0%**. Сильных дистопий тоже больше: **33,2% против 22,7%**. У трудовых обществ доля сильных утопий составляет только 1,4%.

Разница полного и частичного перехода сохраняется в моделях с поправкой на медиа и одинаковым суммарным весом групп: сильных утопий больше на {p(Z['models']['strong_utopia_media_adjusted']['full_minus_partial']['beta'])}, сильных дистопий — на {p(Z['models']['strong_dystopia_media_adjusted']['full_minus_partial']['beta'])}. q составляет {f(test('strong_utopia_media_adjusted','full_minus_partial')['q_BH'],4)} и {f(test('strong_dystopia_media_adjusted','full_minus_partial')['q_BH'],4)} соответственно.

Разведочная гипотеза: состоявшийся переход чаще соседствует с радикально различными устройствами жизни, а частичные переходы в каталоге чаще описаны как смешанные случаи. Это не доказательство, что сам переход вызывает поляризацию: центральная U может означать как умеренные условия, так и недостаточно подробный лор. Кроме того, по абсолютной U трудовые общества столь же экстремальны, как посттрудовые, но гораздо чаще на отрицательной стороне шкалы.
''',['transition-polarity'])

add('transition-security',f'''
## 13. Обеспечение и стадия перехода разделяют разные вопросы

Для сравнения трёх стадий используется один критерий: исходная `axis.guarantees < 0`. Это координатная половина карты с более сильными гарантиями, а не новый факт о правовой универсальности обеспечения.

| Стадия | Доля с гарантиями | U с гарантиями | U без гарантий |
|---|---:|---:|---:|
'''+ '\n'.join('| '+label+' | '+p(Z['stages'][st]['secure_share'])+' | '+f(next(r for r in Z['security'] if r['stage']==st and r['has_guarantees'])['mean_utopia'])+' | '+f(next(r for r in Z['security'] if r['stage']==st and not r['has_guarantees'])['mean_utopia'])+' |' for st,label in zip(ST,LABEL))+'''

Гарантии гораздо чаще встречаются после полного перехода: **67,0%** против **8,4%** у трудовых обществ. Но у **155 посттрудовых обществ без гарантий средняя U = −0,64**, ниже, чем у 316 трудовых без гарантий (−0,51). Это интересный кандидат на дальнейший разбор: исчезновение главенства заработка может сочетаться и с универсальным доступом, и с исключением из распределения.

Нельзя считать разницу −0,64 против −0,51 последствием перехода. В ячейках различаются контроль, население, насилие и другие условия. Взаимодействия стадии с непрерывной обеспеченностью проверены в `utopia_security_interaction`; они не подтверждают простую формулу «обеспечение всегда имеет более сильную связь с U именно после полного перехода».
''',['transition-security'])

add('transition-work','''
## 14. Посттрудовое общество часто остаётся обществом работающих людей

| Показатель | Трудовые | Частичный переход | Посттрудовые |
|---|---:|---:|---:|
'''+ '\n'.join('| '+name+' | '+' | '.join(fmt(Z['stages'][st][key]) for st in ST)+' |' for name,key,fmt in [
('Средняя доля неработающих','mean_nonworking',p),('Медианная доля неработающих','median_nonworking',p),('Обществ, где работает не менее половины населения','share_majority_working',p)])+'''

В **341 из 470 посттрудовых обществ (72,6%)** по разметке работает хотя бы половина рассматриваемого населения. Только **11 из 470** имеют оценку неработающих 95% и выше. Поэтому «переход состоялся» нельзя заменять условием «почти никто не работает».

Примеры из базы: Культура сочетает незарплатный доступ с добровольной деятельностью; Aria даёт высокий U в работающей экономике; человекоподобные и синтетические личности тоже учитываются как участники полезного труда. Доля прокси человекоподобного населения различается между стадиями: 28,1% / 36,0% / 48,7%. Это дополнительная причина читать доли участия как сравнительные редакторские сценарии, а не статистику занятости обычных людей.
''',['transition-work'])

media=['book','short_story','anime','manga','movie','tv','game','comic','tabletop','web_fiction']
add('transition-media','''
## 15. Медиа различаются и стадиями перехода, и благополучием внутри стадии

| Медиа | Всего | Трудовые | Частичный переход | Посттрудовые |
|---|---:|---:|---:|---:|
'''+ '\n'.join('| '+ML[m]+' | '+str(next(r for r in Z['media'] if r['medium']==m)['media_n'])+' | '+' | '.join(p(next(r for r in Z['media'] if r['medium']==m and r['stage']==st)['share_in_medium']) for st in ST)+' |' for m in media)+'''

У аниме полный переход встречается в **45,2%** записей, у книг — в **52,2%**. Этот разрыв меньше, чем разрыв в исходных долях дистопий. При сопоставлении мрачности медиа нужно учитывать и экономическую стадию, и устройство общества внутри неё.

У веб-прозы полный переход занимает 93,1%, но снова срабатывает состав коллекции: 23 из 29 записей относятся к Orion’s Arm. У манги доля трудовых обществ 66,7%, однако всего 18 записей, а состоявшихся переходов только четыре. Теги пересекаются; строки таблицы не складываются в 890.

На тепловой карте ниже каждая ячейка показывает среднюю U и число обществ. Малые ячейки помогают найти примеры для чтения, но не дают устойчивых межмедийных оценок.
''',['transition-media','transition-media-utopia'])

pair=Z['paired_groups']['post_work_minus_zero_variant']
cond=Z['models']['utopia_structural_adjusted']
add('transition-models',f'''
## 16. Сравнение внутри франшиз и чувствительность к поправкам

**84 группы** содержат и трудовые, и посттрудовые общества. В **60** средняя U посттрудовых выше, в **23** ниже, в одной равна. Средняя разница при равном весе таких пар групп составляет **+{f(pair['mean_difference'])}**, интервал группового бутстрэпа [ +{f(pair['low'])}; +{f(pair['high'])} ]. Это сопоставление разных обществ/состояний внутри групп, а не наблюдение за одной политикой до и после её внедрения.

| Модель | Частичный минус трудовые | Полный минус трудовые |
|---|---:|---:|
'''+ '\n'.join('| '+name+' | '+ci(co(key,'partial_transition'))+' | '+ci(co(key,'full_transition'))+' |' for name,key in [
('Только стадия, равный вес групп','utopia_raw'),('Также медиа и узнаваемость','utopia_media_adjusted'),('Также гарантии, контроль и участие','utopia_structural_adjusted')])+f'''

В модели с центральными координатами полный переход получает условный коэффициент **{ci(co('utopia_structural_adjusted','full_transition'))}**. Однако при сравнении внутри групп и тех же поправках интервал включает ноль: {ci(co('within_group_structural','full_transition'))}.

Ещё существеннее неопределённость координат. В 500 искусственных сценариях независимого равномерного варьирования осей внутри сохранённых редакторских интервалов медианный коэффициент полного перехода относительно трудовых составляет **+{f(Z['coordinate_scenarios']['coefficients']['full_vs_zero']['median'])}**, то есть меняет знак по сравнению с центральными оценками. Эти сценарии не являются вероятностной моделью истинных значений, но показывают, что отрицательный условный коэффициент нельзя выносить как устойчивый вывод о вреде перехода.

Иными словами, общие различия стадий хорошо видны, но разложение на «самостоятельный эффект перехода» и «эффект институтов» здесь зависит от модели ошибок и совместного процесса разметки. Полные коэффициенты и отдельная поправка BH по новым тестам сохранены в `transition-tests.csv`.
''',['transition-paired'])

add('transition-recognition',f'''
## 17. Популярность почти одинакова; историческая картина остаётся предварительной

Средняя узнаваемость при равном весе групп внутри стадии: **{f(Z['stages']['zero_variant']['group_balanced_popularity'])} / {f(Z['stages']['transition']['group_balanced_popularity'])} / {f(Z['stages']['post_work']['group_balanced_popularity'])}**. В моделях с поправками на медиа разницы с трудовыми малы и неубедительны: частичный переход {ci(co('popularity_media_adjusted','partial_transition'))}, полный {ci(co('popularity_media_adjusted','full_transition'))}.

Стадия экономики не даёт простого объяснения популярности произведения. Проверка использует зависимость обществ внутри групп, потому что один балл узнаваемости наследуют все общества группы.

Для датированного поднабора состав стадий по эпохам сохранён в `transition-chronology.csv`. Как и в прежнем анализе, даты предварительны и покрывают лишь 324 записи. По ним можно исследовать структуру именно этого поднабора, но нельзя установить исторические предпочтения публики или объяснять современные жанры без поправки на неполноту каталога.

Перспективные гипотезы для дальнейшей независимой разметки: различаются ли переходы через расширение прав и через вытеснение людей из распределения; когда добровольная полезная деятельность сочетается с правом отказаться; насколько комфорт одной группы зависит от эксплуатации другой; отличается ли отсутствие информации о переходном обществе от умеренности его устройства. Эти гипотезы не следует проверять признаками, автоматически извлечёнными из уже назначенного балла U.
''',['transition-recognition','transition-chronology'])


def style(fig,title,height=500):
    import textwrap
    fig.update_layout(title=dict(text='<br>'.join(textwrap.wrap(title,47)),x=0,font=dict(size=17)),height=height,
        font=dict(family='Arial, sans-serif',size=13,color='#23343a'),paper_bgcolor='white',plot_bgcolor='white',
        margin=dict(l=75,r=30,t=100,b=115),legend=dict(orientation='h',x=0,y=-.25,font=dict(size=11)))
    fig.update_xaxes(gridcolor='#e2e9e7');fig.update_yaxes(gridcolor='#e2e9e7')
    return fig

fig=make_subplots(rows=1,cols=3,specs=[[{'type':'domain'}]*3],subplot_titles=[f'{la}<br>n = {Z["stages"][st]["n"]}' for st,la in zip(ST,LABEL)],horizontal_spacing=.035)
for j,st in enumerate(ST):
    rows=[r for r in Z['regimes'] if r['stage']==st]
    fig.add_trace(go.Pie(labels=RL,values=[r['n'] for r in rows],marker=dict(colors=RC,line=dict(color='white',width=1)),sort=False,textinfo='percent',textfont=dict(size=12),hovertemplate='%{label}<br>%{value} обществ (%{percent})<extra></extra>',showlegend=j==0),row=1,col=j+1)
figures['transition-pies']=style(fig,'Шесть укладов внутри каждой из трёх стадий',530)

fig=go.Figure()
for key,label,color in [('strong_dystopia_share','U ≤ −0,5','#ad654d'),('central_share','Промежуточная зона','#d7e0df'),('strong_utopia_share','U ≥ +0,5','#277f75')]:
    fig.add_bar(y=LABEL,x=[Z['stages'][st][key]*100 for st in ST],name=label,marker_color=color,orientation='h',hovertemplate='%{y}: %{x:.1f}%<extra>%{fullData.name}</extra>')
fig.update_layout(barmode='stack');fig.update_xaxes(range=[0,100],title='Доля обществ, %');fig.update_yaxes(autorange='reversed')
figures['transition-polarity']=style(fig,'Похожие средние оценки скрывают разную долю крайних исходов',450)

fig=go.Figure()
for sec,label,color in [(False,'Без гарантий','#ad654d'),(True,'С гарантиями','#277f75')]:
    rows=[next(r for r in Z['security'] if r['stage']==st and r['has_guarantees']==sec) for st in ST]
    fig.add_bar(x=LABEL,y=[r['mean_utopia'] for r in rows],customdata=[r['n'] for r in rows],name=label,marker_color=color,hovertemplate='%{x}<br>Средняя U %{y:.3f}<br>n = %{customdata}<extra>%{fullData.name}</extra>')
fig.update_yaxes(range=[-.8,.4],title='Средняя U');figures['transition-security']=style(fig,'Обеспечение различает благополучие при всех стадиях',450)

fig=go.Figure()
for key,label,color in [('mean_nonworking','Средняя доля неработающих','#6874b5'),('share_majority_working','Обществ, где работает хотя бы половина','#277f75')]:
    fig.add_bar(x=LABEL,y=[Z['stages'][st][key]*100 for st in ST],name=label,marker_color=color,hovertemplate='%{x}: %{y:.1f}%<extra>%{fullData.name}</extra>')
fig.update_yaxes(range=[0,100],title='%');figures['transition-work']=style(fig,'Ослабление зарплатной зависимости сочетается с полезной работой',470)

ms=['book','anime','manga','movie','tv','game','comic','web_fiction']
fig=go.Figure()
for st,la,col in zip(ST,LABEL,STC):
    rows=[next(r for r in Z['media'] if r['medium']==m and r['stage']==st) for m in ms]
    fig.add_bar(y=[ML[m] for m in ms],x=[r['share_in_medium']*100 for r in rows],name=la,marker_color=col,orientation='h',customdata=[[r['n'],r['media_n']] for r in rows],hovertemplate='%{y}: %{x:.1f}%<br>%{customdata[0]} из %{customdata[1]}<extra>%{fullData.name}</extra>')
fig.update_layout(barmode='stack');fig.update_xaxes(range=[0,100],title='Доля обществ, %');fig.update_yaxes(autorange='reversed');figures['transition-media']=style(fig,'Три стадии в разных медиа',540)

zz=[];tt=[]
for m in ms:
    row=[next(r for r in Z['media'] if r['medium']==m and r['stage']==st) for st in ST]
    zz.append([r.get('mean_utopia') if r['n'] else None for r in row]);tt.append([f"{f(r['mean_utopia'])}<br>n = {r['n']}" if r['n'] else 'нет записей' for r in row])
fig=go.Figure(go.Heatmap(x=LABEL,y=[ML[m] for m in ms],z=zz,text=tt,texttemplate='%{text}',zmin=-1,zmax=1,colorscale=[[0,'#b56857'],[.5,'#f5f7f6'],[1,'#277f75']],hovertemplate='%{y}<br>%{x}<br>%{text}<extra></extra>',colorbar=dict(title='U')))
fig.update_yaxes(autorange='reversed');figures['transition-media-utopia']=style(fig,'Средняя U внутри каждой комбинации стадии и медиа',620)

fig=go.Figure(go.Bar(x=[pair['positive_groups'],pair['negative_groups'],pair['ties']],y=['Посттрудовые выше','Трудовые выше','Одинаковая средняя U'],orientation='h',marker_color=['#277f75','#ad654d','#7b8896'],text=[pair['positive_groups'],pair['negative_groups'],pair['ties']],textposition='outside',hovertemplate='%{y}: %{x} групп<extra></extra>'))
fig.update_xaxes(title='Количество сопоставимых групп');fig.update_yaxes(autorange='reversed');figures['transition-paired']=style(fig,'Внутри групп: чаще выше U у посттрудовых обществ',440)

fig=go.Figure(go.Bar(x=LABEL,y=[Z['stages'][st]['group_balanced_popularity'] for st in ST],marker_color=STC,hovertemplate='%{x}: %{y:.3f}<extra></extra>'))
fig.update_yaxes(range=[0,1],title='Средняя узнаваемость, равный вес групп');figures['transition-recognition']=style(fig,'Узнаваемость мало различается между стадиями',440)

eras=['before_1950','1950_1979','1980_1999','2000_2009','2010_2026'];eln=['До 1950','1950–1979','1980–1999','2000–2009','2010–2026']
fig=go.Figure()
for st,label,col in zip(ST,LABEL,STC):
    rows=[next(r for r in Z['chronology'] if r['era']==era and r['stage']==st) for era in eras]
    fig.add_bar(x=eln,y=[r['share']*100 for r in rows],name=label,marker_color=col,customdata=[[r['n'],r['era_n']] for r in rows],hovertemplate='%{x}: %{y:.1f}%<br>%{customdata[0]} из %{customdata[1]}<extra>%{fullData.name}</extra>')
fig.update_layout(barmode='stack');fig.update_yaxes(range=[0,100],title='Доля датированного поднабора, %');figures['transition-chronology']=style(fig,'Предварительный датированный поднабор, 324 общества',460)

for name,fig in figures.items():(OUT/('chart-'+name+'.json')).write_text(pio.to_json(fig),encoding='utf8')
fragment=dict(sections=sections,plot_order=order,figure_files={name:'chart-'+name+'.json' for name in figures})
(OUT/'transition-report-fragment.json').write_text(json.dumps(fragment,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(OUT/'transition-report.md').write_text('\n\n'.join(r['markdown'] for r in sections)+'\n',encoding='utf8')
print(json.dumps({'sections':len(sections),'charts':len(figures)},ensure_ascii=False))
