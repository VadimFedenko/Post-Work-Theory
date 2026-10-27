"""Build Russian Markdown and a self-contained Plotly HTML research report."""
from __future__ import annotations

import csv
import hashlib
import html
import json
import sys
import textwrap
from pathlib import Path

import markdown
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

if hasattr(sys.stdout,"reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "exploratory-analysis"


def rd(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def f(x, n=2):
    return f"{x:.{n}f}".replace(".", ",")


def pct(x):
    return f(x * 100, 1) + "%"


def coef(model, term):
    return next(c for c in model["coefficients"] if c["term"] == term)


def ci(c):
    return f"{f(c['beta'])} [{f(c['low'])}; {f(c['high'])}]"


AUDIT=rd("audit.json")
SUM=rd("group-summaries.json")
MODELS=rd("models.json")
TESTS=rd("exploratory-tests.json")
REG={int(r["category"]):r for r in SUM if r["dimension"]=="regime"}
MEDIA={r["category"]:r for r in SUM if r["dimension"]=="media"}
CV=rd("cross-validation.json")
TIME=rd("chronology.json")
FA=rd("factor-analysis.json")
PCA=rd("pca.json")
CON=rd("factorial-contrasts.json")
NONLIN=rd("nonworking-nonlinearity.json")
RECOG=rd("recognition-analysis.json")
RAW=json.loads((ROOT/"data/societies.json").read_text(encoding="utf-8"))["societies"]
LABELS={0:"0 · Трудовая зависимость сохраняется",1:"1 · Элиты + гарантии",2:"2 · Элиты без гарантий",3:"3 · Распределённая власть + гарантии",4:"4 · Распределённые активы без гарантий",5:"5 · Автономная система + гарантии",6:"6 · Автономная система без гарантий"}
ML={"book":"Книги","anime":"Аниме","tv":"Телевидение","game":"Игры","movie":"Кино","comic":"Комиксы","cartoon":"Мультфильмы","short_story":"Рассказы","tabletop":"Настольные игры","web_fiction":"Веб-проза","manga":"Манга"}
COLORS={0:"#7b8896",1:"#d69c46",2:"#ad654d",3:"#277f75",4:"#5c9d85",5:"#6874b5",6:"#9c5d91"}


def composition_regime(record):
    """Reassign only regime 0 to the coordinate regions used by Atlas.tsx.

    The map splits guarantees at 0 and control into three equal horizontal
    bands. Boundary points belong to the right/lower region, as in setRegionAt.
    This is a chart projection, not a change to the source post-work status.
    """
    if record["regime_primary"] != 0:
        return record["regime_primary"]
    g=record["axis"]["guarantees"]
    c=record["axis"]["control"]
    base=3 if c > 1/3 else 5 if c <= -1/3 else 1
    return base + (0 if g < 0 else 1)


COMPOSITION_REGIMES={r["id"]:composition_regime(r) for r in RAW}
ZERO_ASSIGNMENTS=[dict(id=r["id"],name=r["name"],work=r["work"],media=";".join(r["media"]),original_regime=0,chart_regime=COMPOSITION_REGIMES[r["id"]],guarantees=r["axis"]["guarantees"],control=r["axis"]["control"]) for r in RAW if r["regime_primary"]==0]
with (OUT/"zero-regime-coordinate-assignments.csv").open("w",encoding="utf-8-sig",newline="") as fh:
    writer=csv.DictWriter(fh,fieldnames=list(ZERO_ASSIGNMENTS[0]))
    writer.writeheader();writer.writerows(ZERO_ASSIGNMENTS)
COMPOSITION_NOTE="На этом графике все 345 нулевых вариантов распределены между укладами 1–6 по координатам: гарантии < 0 — с гарантиями; контроль > ⅓ — распределённый, контроль ≤ −⅓ — автономная система, между ними — элиты. Остальные записи сохраняют исходный уклад."


def qval(family, term):
    return next(r["q_BH"] for r in TESTS if r["family"]==family and r["term"]==term)


sections=[]
def add(key, text):
    sections.append((key,text.strip()))


add("intro",f"""
# Что связано с утопией в собранных мирах

Исследовательский анализ базы на 22 октября 2026 года. **890 обществ · 674 значения названия произведения · 496 групп узнаваемости.**

Самый устойчивый результат — сочетание материальных гарантий и распределённой власти связано с более благополучными мирами. Автономное управление само по себе не связано с худшим результатом, чем власть элит. Видимая мрачность отдельных медиа и привлекательность «общества без работы» во многом меняются после учёта устройства общества.

Это исследование **редакторских оценок в отобранном каталоге**, а не случайной выборки всей фантастики. Оно показывает связи внутри базы; причинность и частоты во всей литературе из него не следуют. Все оценки утопичности и популярности имеют низкую заявленную уверенность. Материальная безопасность входит и в определение гарантий, и в оценку утопичности: часть их сильной связи ожидаема из самой методики разметки.

Шкала утопичности: −1 — сильная дистопия, +1 — сильная утопия. Здесь «отрицательная оценка» означает U < 0, «выраженная дистопия» — U ≤ −0,5, «выраженная утопия» — U ≥ +0,5. Порог ±0,5 выбран для описания хвостов шкалы и не является границей из первичной разметки.
""")

add("regimes",f"""
## 1. Самый благополучный уклад — распределённая власть с гарантиями

| Уклад | Обществ | Средняя U | U < 0 | U ≤ −0,5 | Средняя U при равном весе групп |
|---|---:|---:|---:|---:|---:|
"""+"\n".join(f"| {LABELS[k]} | {REG[k]['n']} | {f(REG[k]['mean_utopia'])} | {pct(REG[k]['negative_share'])} | {pct(REG[k]['strong_dystopia_share'])} | {f(REG[k]['group_balanced_utopia'])} |" for k in [3,5,4,1,0,6,2])+f"""

У распределённой власти с гарантиями **7 отрицательных оценок из 128 и ни одной оценки ≤ −0,5**. Это не отсутствие любых проблем: есть Wyst (−0,40), The Million (−0,45) и общество Эдо в Star Trek (−0,35).

В модели только для 545 посттрудовых обществ/переходов, при учёте медиа, узнаваемости и участия в работе, распределённая власть с гарантиями выше власти элит с гарантиями на **{ci(CON['distributed_vs_elite_with_guarantees'])}**, а автономной системы с гарантиями — на **{ci(CON['distributed_vs_autonomous_with_guarantees'])}**. Здесь и далее квадратные скобки — 95%-ные интервалы статистической модели с кластеризацией по группам, а не интервалы достоверности самой редакторской разметки.
""")

add("security",f"""
## 2. Гарантии связаны с улучшением при любом типе власти

Корреляция Спирмена между отсутствием гарантий и утопичностью по 890 обществам равна **−0,750**. Если поменять знак оси, чтобы положительное значение означало обеспеченность, связь становится положительной. При равном весе 496 групп ранговая связь составляет **+0,741**, а интервал группового бутстрэпа — примерно [0,700; 0,777]. Это взвешенная корреляция общих средних рангов, поэтому она немного отличается от обычного Спирмена по усреднённым группам.

| Кто контролирует систему | Разница «с гарантиями — без» в средней U | Скорректированная разница и 95%-ный интервал |
|---|---:|---:|
| Элиты | {f(REG[1]['mean_utopia']-REG[2]['mean_utopia'])} | {ci(CON['guarantee_effect_elite'])} |
| Распределённая власть/активы | {f(REG[3]['mean_utopia']-REG[4]['mean_utopia'])} | {ci(CON['guarantee_effect_distributed'])} |
| Автономная система | {f(REG[5]['mean_utopia']-REG[6]['mean_utopia'])} | {ci(CON['guarantee_effect_autonomous'])} |

Для трёх скорректированных различий q < 0,001 после поправки на множественные проверки. Взаимодействия «тип власти × наличие гарантий» отдельно неубедительны: данные совместимы с сопоставимым положительным различием во всех трёх семействах. У распределённых активов без гарантий всего 21 запись; эту ячейку следует читать осторожнее остальных.

Одна только обеспеченность даёт R² ≈ **{f(CV['security_only'])}** в проверке с отложенными группами. Структурная модель добавляет распределение власти, участие в работе, посттрудовой статус и узнаваемость и достигает **{f(CV['structural'])}**. Это качество воспроизведения оценок внутри каталога, а не проверка теории на независимой разметке.
""")

add("ai",f"""
## 3. Самостоятельная система не выглядит хуже элит; распределённая власть выглядит лучше обеих

С гарантиями: элиты **{f(REG[1]['mean_utopia'])}**, автономные системы **+{f(REG[5]['mean_utopia'])}**. Без гарантий: элиты **{f(REG[2]['mean_utopia'])}**, автономные системы **{f(REG[6]['mean_utopia'])}**. Простая гипотеза «чем больше власть у самой системы, тем хуже мир» не описывает эту таблицу.

С поправками автономная система отличается от элит с гарантиями на **{ci(CON['autonomous_vs_elite_with_guarantees'])}**. Это слабый сигнал: p = 0,044, но q = **{f(qval('factorial_contrast','autonomous_vs_elite_with_guarantees'),3)}**, поэтому утверждать превосходство автономного управления нельзя. Без гарантий разница **{ci(CON['autonomous_vs_elite_without_guarantees'])}** также неубедительна.

Более надёжен положительный результат распределённого контроля. Ось контроля нельзя читать как простую линейную шкалу авторитаризма: −1 означает решающую автономию системы, 0 — концентрацию у элит, +1 — широко распределённую власть. Поэтому модели включают и квадрат этой координаты, а отдельная факторная модель сравнивает три семейства напрямую.

«Автономная система» здесь — функциональная категория базы, а не чистая выборка программных ИИ: например, у Сивиллы отдельно оговорены человеческие мозги. Сравниваются уже существующие состояния обществ. Данных о контролируемой передаче власти от людей к ИИ в одном и том же обществе здесь нет.
""")

add("leisure",f"""
## 4. Отсутствие работы не даёт простого линейного преимущества

Здесь измеряется участие в широкой деятельности, включая неоплачиваемую заботу и добровольные проекты. Доля неработающих не равна доле досуга или человеческому вкладу в выпуск. [Подробный аудит измерения и всех крайних случаев](#working-audit) показывает ограничения процентов и неодинаковые знаменатели.

Без поправок доля неработающих положительно связана с утопичностью: обычный Спирмен **+0,355**, взвешенная ранговая связь **+0,334**. Линейный коэффициент в модели с одним предиктором — **{ci(coef(MODELS['nonworking_only'],'nonworking'))}**. Прибавка 10 процентных пунктов соответствует примерно +0,073 к U.

После учёта обеспечения, контроля, статуса, медиа и узнаваемости линейный коэффициент становится **{ci(coef(MODELS['full_group_balanced'],'nonworking'))}** — практически нулевым. Удаление этого члена даже немного улучшает проверку на отложенных группах: R² {f(CV['without_nonworking'],3)} вместо {f(CV['structural_and_media'],3)}.

Это не доказывает отсутствия любой связи. Более гибкая модель с квадратом доли неработающих и её взаимодействиями с обеспечением/контролем обнаруживает **нелинейность**: совместная проверка четырёх членов даёт q = **{f(qval('flexible_omnibus','all_nonworking_terms'),4)}**. R² на отложенных группах составляет {f(NONLIN['cv_r2'],3)}; без всех членов участия, но с взаимодействием обеспечения и контроля — {f(NONLIN['cv_no_nonworking_terms'],3)}. Дополнительный выигрыш невелик, около одного процентного пункта.

В обществах с сильными гарантиями (исходная ось guarantees ≤ −0,5) средняя U составляет +0,50 при 20–40% неработающих (n = 39), +0,39 при 40–60% (n = 79), +0,12 при 60–80% (n = 43) и около 0,00 при 80–100% (n = 26). Это описательные, нескорректированные подгруппы; границы выбраны для наглядности.

Возможная интерпретация — некоторые сюжеты различают свободную полезную деятельность и полную зависимость/пассивность. Но это **гипотеза для дальнейшей проверки**, а не вывод о пользе обязательного труда. 886 из 890 оценок участия имеют низкую уверенность; медианная ширина их редакторского интервала — 0,75. В подвыборке без человекоподобных прокси интервал одной из нелинейных разниц включает ноль. Нельзя выводить из этой модели «оптимальную занятость».
""")

media_table="\n".join(f"| {ML[m]} | {MEDIA[m]['n']} | {MEDIA[m]['groups']} | {f(MEDIA[m]['mean_utopia'])} | {pct(MEDIA[m]['negative_share'])} | {pct(MEDIA[m]['strong_dystopia_share'])} |" for m in ["book","short_story","anime","manga","movie","tv","game","comic","cartoon","tabletop","web_fiction"])
anime_con=next(c for c in rd("media-contrasts.json") if c["medium"]=="anime")
game_con=next(c for c in rd("media-contrasts.json") if c["medium"]=="game")
add("media",f"""
## 5. В каталоге аниме мрачнее книг; после учёта устройства общества разница исчезает

| Медиа | Обществ | Групп | Средняя U | U < 0 | U ≤ −0,5 |
|---|---:|---:|---:|---:|---:|
{media_table}

У аниме отрицательных оценок **74,0%**, у книг **51,7%**: разница 22,3 процентного пункта. Выраженных дистопий соответственно 47,9% и 34,5%, разница 13,4 пункта. Телевидение имеет ещё большую долю отрицательных оценок — **80,6%**. Медиа являются пересекающимися тегами: аниме-фильм может входить сразу в несколько строк.

Но состав укладов очень различается. Распределённая власть с гарантиями встречается у **23,2% книжных записей и только у 2,7% аниме-записей**. У аниме чаще сохранённая трудовая зависимость, власть элит и автономные системы без гарантий.

В модели медиа с равным весом групп разница аниме с книгами до структурных поправок составляет {ci(anime_con['unadjusted'])}. После поправок — **{ci(anime_con['adjusted'])}**; q = {f(qval('media_vs_book','anime'),3)}. В строгом сравнении непересекающихся аниме и прозы результат тот же: +0,081 [−0,028; +0,189]. Утверждение о самостоятельной «дистопичности формата аниме» не подтверждается.

Добавление всех медиа к структурной модели почти не улучшает подгонку и немного ухудшает групповую проверку: R² {f(CV['structural'],3)} → {f(CV['structural_and_media'],3)}. Это согласуется с объяснением через состав обществ, но не является доказательством причинного механизма.

Небольшая дополнительная находка: игры после тех же поправок оказываются выше книг на **{ci(game_con['adjusted'])}**, q = {f(qval('media_vs_book','game'),3)}. Это вторичный результат. У игр есть выбираемые ветки и финалы, а многие координаты неуверенны; общую гипотезу о «более оптимистичном игровом устройстве общества» ещё нужно проверять.

**Обновление графика состава укладов.** {COMPOSITION_NOTE} Переназначение относится к этому графику; таблицы и статистические модели выше используют исходную классификацию базы.
""")

add("selection",f"""
## 6. «Веб-фантастика оптимистична» — пример ловушки состава выборки

У веб-прозы средняя U = **+0,39**, а у телевидения −0,47. Однако **23 из 29 веб-записей принадлежат Orion’s Arm**. После равного взвешивания шести групп веб-прозы средняя снижается до **+0,14**. У телевидения 108 обществ относятся всего к 30 группам; отдельные длинные франшизы тоже получают много карточек.

Следовательно, визуально большая разница между колонками не превращается автоматически в свойство медиа. Веб-проза здесь — особенно слабое основание для обобщения: шесть групп дают мало независимых наблюдений.

Узнаваемость тоже назначена произведению/группе, а не конкретному обществу. Нельзя считать одинаковую популярность десятка миров одной франшизы десятью независимыми подтверждениями.
""")

add("popularity",f"""
## 7. Более известные произведения кажутся мрачнее, но независимая связь неустойчива

На уровне обществ популярность и U имеют Спирмена **−0,188**. На уровне 496 групп, где у каждой группы одна строка, узнаваемость и средняя U связаны слабее: **−0,160**.

Если одновременно учитывать медиа и среднюю абсолютную U, связь средней U с популярностью становится почти нулевой: коэффициент **{ci(coef(RECOG['model'],'mean_utopia'))}**, p = 0,500. Это согласуется с тем, что более массовые экранные медиа в этом каталоге одновременно представлены более мрачными обществами.

Гипотеза «крайности популярнее» имеет только слабый сигнал. Средняя абсолютная U связана с узнаваемостью на уровне Спирмена **+0,119**; скорректированный коэффициент {ci(coef(RECOG['model'],'mean_abs_utopia'))}. Без поправки p = 0,043, после множественных сравнений q = **{f(qval('popularity','mean_abs_utopia'),3)}**. Этого недостаточно для уверенного вывода, что радикальные утопии/дистопии популярнее.

Популярность — редакторская оценка международной узнаваемости на одну дату. Это не продажи, аудитория, качество или исторический ряд интереса публики. Поэтому даже идеальные даты публикации не позволят по этой переменной установить, «становятся ли крайности популярнее с течением времени».
""")

era_names={"before_1950":"До 1950","1950_1979":"1950–1979","1980_1999":"1980–1999","2000_2009":"2000–2009","2010_2026":"2010–2026"}
era_table="\n".join(f"| {era_names[r['era']]} | {r['n']} | {f(r['mean_utopia'])} | {pct(r['strong_dystopia_share'])} | {pct(r['strong_utopia_share'])} |" for r in TIME['eras'])
ut=coef(TIME['models']['utopia_medium_adjusted'],'decade')
ex=coef(TIME['models']['extremity_medium_adjusted'],'decade')
add("history",f"""
## 8. Историческое усиление крайностей не подтверждается на доступном поднаборе

В основном экспорте **нет года выхода**. Из сохранённых введений Wikipedia и метаданных точно совпавших сериалов TVmaze получен предварительный датированный поднабор: **{AUDIT['dates_rows']} общества, {AUDIT['dates_works']} названия, {TIME['groups']} групп**. Это {pct(AUDIT['dates_rows']/890)} записей, а не вся база. Даты и фрагменты-основания сохранены в `publication-dates.csv`.

| Период | Обществ | Средняя U | U ≤ −0,5 | U ≥ +0,5 |
|---|---:|---:|---:|---:|
{era_table}

Для последних лет средняя действительно более отрицательная, но ряд не монотонен. В модели с равным весом групп и поправкой на медиа изменение U за десятилетие — **{ci(ut)}**, p = {f(ut['p'],3)}. Изменение абсолютной U — **{ci(ex)}**, p = {f(ex['p'],3)}. Для долей сильных дистопий и сильных утопий убедительного линейного тренда также нет.

Эти нулевые результаты не доказывают отсутствия исторических изменений. Поднабор неполон, датировка не прошла сплошную библиографическую проверку, а дата начала сериала не всегда совпадает с датой эпизода, где появилось общество. Варианты медиа под одним названием, манга/комиксы с неоднозначной сериализацией и конфликтующие даты исключались. Годы из Open Library и Steam не использованы автоматически: они могут относиться к переводу, переизданию или порту. Для City дата сборника всё равно не датирует каждую отдельную историю — такие ограничения нельзя исправить одной регрессией.

Чтобы ответить именно про изменение популярности, потребуется исторический показатель аудитории/продаж/упоминаний с поправкой на объём выпуска каждого медиа и время, прошедшее с релиза.
""")

add("factors",f"""
## 9. Факторный анализ различает обеспечение/досуг и агентность/благополучие

Проведены два разных анализа, которые не следует смешивать.

**Главные компоненты только трёх структурных координат**, без утопичности и популярности: первая компонента объясняет **52,6%** разброса, вторая — **30,9%**, третья — 16,5%. Первая сильнее всего связана с обеспечением и долей неработающих; вторая — с распределением контроля. То есть экономическая обеспеченность и устройство власти образуют различимые направления, а не одну шкалу.

**Разведочный факторный анализ пяти параметров** — обеспечение, контроль, доля неработающих, U и популярность. Использована одна усреднённая строка на группу (n = 496), стандартизация, оценка максимальным правдоподобием, два фактора с вращением varimax.

| Параметр | Фактор 1 | Фактор 2 |
|---|---:|---:|
| Обеспечение | 0,50 | 0,77 |
| Распределённый контроль | 0,45 | 0,02 |
| Доля неработающих | 0,12 | 0,56 |
| Утопичность | 0,85 | 0,36 |
| Популярность | −0,16 | −0,04 |

Первый фактор можно условно прочитать как **агентность и благополучие**, второй — как **обеспечение и освобождение от работы**. Популярность почти не входит в них: около 97% её стандартизированной дисперсии модель оставляет специфической.

Пригодность данных для факторизации умеренная: KMO = **{f(FA['KMO'],3)}**. Пять переменных и два фактора оставляют очень мало свободы для содержательной проверки структуры. U уже включена в факторизацию, поэтому высокий её вес не является независимым объяснением благополучия. Это полезное описание совместного варьирования, а не обнаружение двух объективных законов фантастики.
""")

add("cases",f"""
## 10. Внутри одной вселенной часто есть противоположные ответы

Из **173 групп с несколькими обществами у 98** присутствуют и положительные, и отрицательные оценки. У **38** есть одновременно U ≤ −0,5 и U ≥ +0,5. Это число относится к группам узнаваемости, которые лишь приближённо соответствуют вселенным/франшизам.

Поэтому Manna, Star Trek, Fallout или другая большая серия плохо описываются одним словом «утопия»/«дистопия». Например, в Manna австралийский проект имеет U = +0,85, американские комплексы — −0,65.

В модели различий **внутри группы** связь обеспечения с U сохраняется: коэффициент **{ci(coef(MODELS['within_group_fixed_effects'],'security'))}**. Сохраняются и члены распределения контроля. Такие сравнения устраняют постоянные особенности группы, хотя разные общества внутри неё всё ещё могут отличаться по множеству неучтённых причин.

Интереснее всего для дальнейшей содержательной работы отклонения от простой структурной модели:

| Общество | U | Что не улавливают три координаты полностью |
|---|---:|---|
| With Folded Hands, после захвата | −0,75 | Забота и обеспечение сочетаются с подавлением самостоятельной деятельности |
| Brave New World, исходный роман | −0,60 | Комфорт сочетается с кастами, обусловливанием и ограниченным выбором |
| Fantastic Planet, цивилизация драгов | −0,90 | Благополучие доминирующей группы связано с подчинением других разумных существ |
| Neuromancer, бодрствующий анклав Тессье–Эшпул | −0,85 | Изобилие узкой элиты не описывает цену и исключения системы |
| The Talos Principle 2, New Jerusalem до Машины | +0,45 | Кооперация и самостоятельная деятельность дают положительный результат при сохраняющейся необходимости работы |
| Aria, сервисная экономика Аквы | +0,75 | Полезная работа совместима с высоким благополучием |

Это разбор сохранённых обоснований разметки, а не независимая повторная проверка сюжетов. Все 14 случаев с сильным обеспечением и U ≤ −0,5, а также наибольшие остатки модели находятся в `interesting-cases.csv`. Перспективное расширение базы — отдельно разметить свободу выхода, принуждение, классовую/видовую исключённость и условность поддержки по независимому протоколу, не выводя эти признаки из уже назначенной U.
""")

sens=rd("sensitivity.json")
add("methods",f"""
## Методика, устойчивость и ограничения

**Единица анализа.** Общество, население, период или выбранная ветка. Основной массив содержит 890 записей; 345 нулевых вариантов сохранены как сравнение, 545 относятся к посттрудовым обществам/переходам. 29 дополнительных записей из другой схемы просмотрены по составу и исключены из совместной статистики: у них нет сопоставимого полного слоя U/популярности. Исторические пакеты, ревизии и копии экспорта не добавлялись как новые наблюдения.

**Направление осей.** Для анализа создана производная `security = −axis.guarantees`: больше означает лучшее обеспечение. Исходные данные не менялись. `control` и `nonworking` сохранены. Коды укладов — категории; корреляция с номером уклада не вычислялась. Признаки `manual_code`, `allocation_mechanisms`, производство и зарплатная зависимость проверены по распределению. В актуальной версии они во многом задаются одним ручным кодом, поэтому включать их как независимые факторы одновременно означало бы многократно учитывать одну и ту же разметку.

**Вес и ошибки.** Основные регрессии — взвешенные наименьшие квадраты с весом 1 / число обществ данной группы в выбранном поднаборе. Суммарный вес каждой представленной группы одинаков. Стандартные ошибки CR1 кластеризованы по `popularity_assessment.subject_id`, интервалы используют t-распределение с G−1 степенями свободы. Группы узнаваемости не являются универсальным идентификатором франшизы. Для 496 отдельных групп популярности применяется по одной строке на группу и такая же робастная оценка ошибок. Численные шкалы трактуются как условно интервальные для регрессий; отдельно проверены ранговые связи.

**Модель.** Базовые предикторы: обеспечение, контроль, квадрат контроля, доля неработающих, посттрудовой флаг, популярность и пересекающиеся индикаторы медиа с ≥15 записями. Посттрудовая факторная модель сравнивает наличие гарантий и три семейства контроля с взаимодействиями. Показаны также модель различий внутри группы, нелинейная модель участия, компонентный и факторный анализ. Это разведочный поиск, а не заранее зарегистрированный тест единственной гипотезы.

**Множественные проверки.** Поправка Benjamini–Hochberg применена общей семьёй к {len(TESTS)} опубликованным тестам коэффициентов, контрастов и исторических трендов. q < 0,05 отмечает относительно устойчивый сигнал в этой семье, но не устраняет систематические ошибки отбора/разметки. Доверительные интервалы не скорректированы на множественность. Описательные таблицы и бутстрэп корреляций служат картой данных, а не отдельной серией доказательств.

**Предсказательная проверка.** Пять разбиений GroupKFold: все общества группы остаются в одном разбиении. Утопичность не использована для построения структурных компонент или предикторов. Состав моделей выбран разведочно на этой базе; оценка R² не является окончательной внешней валидацией.

| Проверка основной модели | Обществ | Коэффициент обеспечения |
|---|---:|---:|
| Вся база, равный вес групп | 890 | {f(coef(MODELS['full_group_balanced'],'security')['beta'])} |
"""+"\n".join(f"| {label} | {r['n']} | {f(r['coefficients']['security'])} |" for label,r in zip(["Консервативный охват населения","Без прокси человекоподобного населения","Без проекций и настраиваемых веток","Без десяти крупнейших групп","Только посттрудовые общества/переходы"],sens))+f"""

**Неопределённость координат.** Выполнены 500 искусственных сценариев: каждая координата независимо и равномерно варьировалась в сохранённом редакторском интервале, а U и популярность фиксировались. Во всех этих сценариях коэффициенты обеспечения и направления контроля сохраняют положительный знак; линейный коэффициент неработающих меняет знак примерно поровну. Это тест чувствительности к конкретному допущению, а не вероятностная модель истинных координат: интервалы не являются доверительными, ошибки могут быть зависимыми. Посттрудовой коэффициент в этих сценариях меняет содержательный вывод, поэтому не вынесен как самостоятельная находка. Нелинейные результаты участия не прошли полноценную проверку неопределённости самой U.

**Главное ограничение.** Обеспечение, контроль и U интерпретировались по пересекающимся текстам одним редакторским процессом. Высокая корреляция может отражать и свойства выбранных вымышленных обществ, и согласованность ценностной схемы разметки. Низкие p/q не делают субъективные числа точными и не превращают каталог в репрезентативную выборку всей фантастики.

## Файлы и воспроизведение

- `report.html` — автономный интерактивный отчёт; Plotly включён внутрь, доступ к сети не нужен.
- `analysis-records.csv` — все 890 производных строк и использованные веса.
- `group-summaries.csv`, `correlations.csv`, `recognition-groups.csv` — полные описательные результаты.
- `zero-regime-coordinate-assignments.csv`, `media-regime-composition-reassigned.csv` — переносы нулевых вариантов по координатам и обновлённые доли для графика состава укладов.
- `transition-analysis.json`, `transition-records.csv`, `transition-tests.csv` — отдельный анализ трёх стадий перехода, все строки и проверки.
- `presentation/post-work-stages-v2.pptx` — девять редактируемых слайдов со сравнением трёх стадий.
- `models.json`, `factorial-contrasts.json`, `media-contrasts.json`, `exploratory-tests.csv` — оценки моделей, интервалы, p и q.
- `publication-dates.csv`, `publication-date-rejections.json`, `chronology.json` — датировка, источники и причины исключений.
- `interesting-cases.csv` — случаи для содержательной проверки с ID, обоснованием и ссылками на реестр источников.
- `pca.json`, `factor-analysis.json`, `sensitivity.json`, `nonlinear-sensitivity.json`, `editorial-interval-scenarios.json` — дополнительные проверки.
- `provenance.json` — контрольные суммы входных файлов, версия numpy и seed {20261022}.

Из корня проекта: `python scripts/analyze_societies.py`, `python scripts/analyze_transition_stages.py`, `python scripts/write_transition_report.py`, затем `python scripts/write_society_analysis_report.py`. Анализ использует numpy, scipy, scikit-learn; отчёт — Plotly и Python-Markdown. Запуск проверен на установленном Python 3.10. Источники и первичные оценки сохранены без изменений.
""")


def style(fig, title, height=470):
    wrapped="<br>".join(textwrap.wrap(title,width=46))
    fig.update_layout(title=dict(text=wrapped,x=0,font=dict(size=17)),height=height+35,
        font=dict(family="Arial, sans-serif",size=13,color="#23343a"),paper_bgcolor="white",plot_bgcolor="white",
        margin=dict(l=70,r=30,t=100,b=110),legend=dict(orientation="h",y=-.22,x=0,font=dict(size=11)),hoverlabel=dict(bgcolor="white"))
    fig.update_xaxes(gridcolor="#e5ebed",zerolinecolor="#bfcbd0")
    fig.update_yaxes(gridcolor="#e5ebed",zerolinecolor="#bfcbd0")
    return fig


figures={}
order=[2,6,0,1,4,5,3]
SHORT={0:"0 · Трудовая зависимость",1:"1 · Элиты + гарантии",2:"2 · Элиты без гарантий",3:"3 · Распределённый + гарантии",4:"4 · Активы без гарантий",5:"5 · Система + гарантии",6:"6 · Система без гарантий"}
fig=go.Figure()
for metric,label,color in [("mean_utopia","Каждое общество — один голос","#2f7d79"),("group_balanced_utopia","Равный вес групп внутри уклада","#a9bdb9")]:
    fig.add_bar(y=[SHORT[k] for k in order],x=[REG[k][metric] for k in order],orientation="h",name=label,marker_color=color,
        customdata=[[REG[k]["n"],REG[k]["groups"]] for k in order],hovertemplate="%{y}<br>Средняя U: %{x:.3f}<br>Обществ: %{customdata[0]} · групп: %{customdata[1]}<extra>%{fullData.name}</extra>")
fig.update_layout(barmode="group");fig.update_xaxes(range=[-1,1],title="Средняя утопичность U");fig.update_yaxes(autorange="reversed")
figures["regimes"]=style(fig,"Уклад связан с оценкой сильнее, чем формат произведения",540)

fig=go.Figure()
for fam,ks,color in [("Элиты",[2,1],COLORS[1]),("Распределённая власть / активы",[4,3],COLORS[3]),("Автономная система",[6,5],COLORS[5])]:
    fig.add_scatter(x=["Без гарантий","С гарантиями"],y=[REG[k]["mean_utopia"] for k in ks],mode="lines+markers",name=fam,marker=dict(size=12,color=color),line=dict(width=3,color=color),
        customdata=[[REG[k]["n"]] for k in ks],hovertemplate="%{x}<br>U = %{y:.3f}<br>n = %{customdata[0]}<extra>%{fullData.name}</extra>")
fig.update_yaxes(range=[-.85,.65],title="Средняя U (без поправок)")
figures["security"]=style(fig,"Гарантии связаны с более высокой U во всех трёх семействах",450)

ms=["book","short_story","anime","movie","tv","game","comic","web_fiction"]
fig=go.Figure()
fig.add_bar(x=[ML[m] for m in ms],y=[MEDIA[m]["negative_share"]*100 for m in ms],marker_color="#a66b61",name="Отрицательная оценка U < 0",customdata=[[MEDIA[m]["n"],MEDIA[m]["groups"]] for m in ms],hovertemplate="%{x}: %{y:.1f}%<br>n = %{customdata[0]} · групп = %{customdata[1]}<extra></extra>")
fig.update_yaxes(range=[0,100],title="% обществ с отрицательной оценкой")
figures["media"]=style(fig,"Доли в отобранном каталоге; теги медиа могут пересекаться",450)

fig=go.Figure()
mcons=rd("media-contrasts.json")
sel=[m for m in mcons if m["medium"] in ["anime","game","movie","tv","comic"]]
for field,label,col in [("unadjusted","Только медиа; равный вес групп","#9c635c"),("adjusted","С учётом устройства общества","#2f7d79")]:
    fig.add_scatter(y=[ML[c["medium"]] for c in sel],x=[c[field]["beta"] for c in sel],mode="markers",name=label,marker=dict(size=10,color=col),error_x=dict(type="data",symmetric=False,array=[c[field]["high"]-c[field]["beta"] for c in sel],arrayminus=[c[field]["beta"]-c[field]["low"] for c in sel],color=col),hovertemplate="%{y}: %{x:.3f}<extra>%{fullData.name}</extra>")
fig.update_xaxes(title="Разница с книгами по U · 95%-ные интервалы модели",range=[-.5,.35]);fig.update_yaxes(autorange="reversed")
figures["media_adjustment"]=style(fig,"После поправок мрачность формата перестаёт быть устойчивым объяснением",430)

fig=go.Figure()
low=[0,.2,.4,.6,.8];high=[.2,.4,.6,.8,1.01]
for secure,label,color in [(False,"Остальные общества","#9c635c"),(True,"Сильные гарантии (security ≥ 0,5)","#2f7d79")]:
    means,ns=[],[]
    for lo,hi in zip(low,high):
        rs=[r for r in RAW if lo<=r["axis"]["nonworking"]<hi and (-r["axis"]["guarantees"]>=.5)==secure]
        means.append(np.mean([r["utopia_score"] for r in rs]));ns.append(len(rs))
    fig.add_scatter(x=["0–20%","20–40%","40–60%","60–80%","80–100%"],y=means,mode="lines+markers",name=label,marker=dict(size=10,color=color),line=dict(color=color,width=3),customdata=ns,hovertemplate="Неработающие: %{x}<br>Средняя U: %{y:.3f}<br>n = %{customdata}<extra>%{fullData.name}</extra>")
fig.update_xaxes(title="Доля неработающих, %")
fig.update_yaxes(title="Средняя U",range=[-.8,.8])
figures["leisure"]=style(fig,"Связь с неучастием в работе неодинакова на разных участках шкалы",470)

fig=go.Figure()
composition_media=["book","anime","game","tv","web_fiction"]
composition_rows=[]
for k in range(1,7):
    shares=[];counts=[]
    for m in composition_media:
        records=[r for r in RAW if m in r["media"]]
        count=sum(COMPOSITION_REGIMES[r["id"]]==k for r in records)
        reassigned=sum(r["regime_primary"]==0 and COMPOSITION_REGIMES[r["id"]]==k for r in records)
        shares.append(count/len(records)*100);counts.append([count,len(records),reassigned])
        composition_rows.append(dict(medium=m,regime=k,n=count,total=len(records),reassigned_from_zero=reassigned,share=count/len(records)))
    fig.add_bar(y=[ML[m] for m in composition_media],x=shares,orientation="h",name=SHORT[k],legendgroup=str(k),marker_color=COLORS[k],customdata=counts,hovertemplate=f"%{{y}}<br>{LABELS[k]}: %{{x:.1f}}%<br>%{{customdata[0]}} из %{{customdata[1]}} обществ<br>Из нулевого варианта: %{{customdata[2]}}<extra></extra>")
with (OUT/"media-regime-composition-reassigned.csv").open("w",encoding="utf-8-sig",newline="") as fh:
    writer=csv.DictWriter(fh,fieldnames=list(composition_rows[0]))
    writer.writeheader();writer.writerows(composition_rows)
assert len(ZERO_ASSIGNMENTS)==345
assert all(COMPOSITION_REGIMES[r["id"]] in range(1,7) for r in RAW)
assert all(COMPOSITION_REGIMES[r["id"]]==r["regime_primary"] for r in RAW if r["regime_primary"]!=0)
assert all(abs(sum(r["share"] for r in composition_rows if r["medium"]==m)-1)<1e-12 for m in composition_media)
fig.update_layout(barmode="stack");fig.update_xaxes(range=[0,100],title="Доля обществ каждого уклада, %");fig.update_yaxes(autorange="reversed")
figures["composition"]=style(fig,"Разные медиа содержат разные наборы общественных укладов",550)

fig=go.Figure()
for key,label,color in [("strong_dystopia_share","U ≤ −0,5","#a66b61"),("strong_utopia_share","U ≥ +0,5","#2f7d79")]:
    fig.add_bar(x=[era_names[r["era"]] for r in TIME["eras"]],y=[r[key]*100 for r in TIME["eras"]],name=label,marker_color=color,customdata=[r["n"] for r in TIME["eras"]],hovertemplate="%{x}: %{y:.1f}%<br>n = %{customdata}<extra>%{fullData.name}</extra>")
fig.update_layout(barmode="group");fig.update_yaxes(range=[0,65],title="Доля обществ, %")
figures["history"]=style(fig,f"Датированный поднабор: {AUDIT['dates_rows']} из 890 обществ; линейный тренд неубедителен",450)

fa_load=FA["models"][1]["loadings"]
fig=go.Figure(go.Heatmap(z=fa_load,x=["Фактор 1","Фактор 2"],y=["Обеспечение","Распределение контроля","Доля неработающих","Утопичность","Популярность"],zmin=-1,zmax=1,colorscale=[[0,"#9c635c"],[.5,"#f7f9f8"],[1,"#2f7d79"]],text=np.array(fa_load).round(2),texttemplate="%{text}",hovertemplate="%{y} · %{x}: %{z:.3f}<extra></extra>",colorbar=dict(title="Нагрузка")))
fig.update_yaxes(autorange="reversed")
figures["factors"]=style(fig,"Разведочная факторизация: благополучие/агентность и обеспечение/досуг",430)

group_rows=list(csv.DictReader((OUT/"recognition-groups.csv").open(encoding="utf-8-sig")))
fig=go.Figure(go.Scatter(x=[float(r["mean_utopia"]) for r in group_rows],y=[float(r["popularity"]) for r in group_rows],text=[r["subject"] for r in group_rows],customdata=[r["n"] for r in group_rows],mode="markers",marker=dict(size=7,color="#536e80",opacity=.5),hovertemplate="%{text}<br>Средняя U: %{x:.2f}<br>Узнаваемость: %{y:.2f}<br>Обществ в группе: %{customdata}<extra></extra>"))
fig.update_xaxes(title="Средняя утопичность обществ группы",range=[-1.05,1.05]);fig.update_yaxes(title="Редакторская узнаваемость группы",range=[0,1.05])
figures["popularity"]=style(fig,"496 групп: слабая сырая связь с популярностью требует поправок",460)

transition_fragment=None
if (OUT/"transition-report-fragment.json").exists():
    transition_fragment=rd("transition-report-fragment.json")
    expected=rd("transition-analysis.json")["input_sha256"]
    assert hashlib.sha256((ROOT/"data/societies.json").read_bytes()).hexdigest()==expected,"Rerun the stage analysis after catalogue changes"
    insertion=next(i for i,(key,_) in enumerate(sections) if key=="methods")
    sections[insertion:insertion]=[(r["key"],r["markdown"]) for r in transition_fragment["sections"]]
    for key,name in transition_fragment["figure_files"].items():
        figures[key]=pio.from_json((OUT/name).read_text(encoding="utf-8"))
working_fragment=None
if (OUT/"working-report-fragment.json").exists():
    working_fragment=rd("working-report-fragment.json")
    assert hashlib.sha256((ROOT/"data/societies.json").read_bytes()).hexdigest()==working_fragment["input_sha256"],"Rerun the participation audit after catalogue changes"
    insertion=next(i for i,(key,_) in enumerate(sections) if key=="methods")
    sections[insertion:insertion]=[(r["key"],r["markdown"]) for r in working_fragment["sections"]]
    for key,name in working_fragment["figure_files"].items():
        figures[key]=pio.from_json((OUT/name).read_text(encoding="utf-8"))
md="\n\n".join(text for _,text in sections)+"\n"
(OUT/"report.md").write_text(md,encoding="utf-8")
body=[]
plot_order={"regimes":["regimes"],"security":["security"],"leisure":["leisure"],"media":["media","composition","media_adjustment"],"popularity":["popularity"],"history":["history"],"factors":["factors"]}
if transition_fragment:plot_order.update(transition_fragment["plot_order"])
if working_fragment:plot_order.update(working_fragment["plot_order"])
js_added=False
for key,text in sections:
    body.append('<section id="'+key+'">'+markdown.markdown(text,extensions=["tables","fenced_code"])+"</section>")
    for plot_key in plot_order.get(key,[]):
        fig=figures[plot_key]
        # Both JSON and JS embedded locally. No remote scripts, fonts, or data.
        block=pio.to_html(fig,full_html=False,include_plotlyjs=not js_added,config=dict(responsive=True,displaylogo=False,toImageButtonOptions=dict(format="svg",filename="societies-"+plot_key)),div_id="plot-"+plot_key)
        js_added=True
        body.append('<div class="chart">'+block+"</div>")
        if plot_key=="composition":
            body.append('<p class="chart-note">'+html.escape(COMPOSITION_NOTE)+'</p>')
for key,fig in figures.items():
    (OUT/("chart-"+key+".json")).write_text(pio.to_json(fig),encoding="utf-8")
css="""
:root{color-scheme:light;--ink:#23343a;--teal:#2f7d79;--muted:#61717a}
*{box-sizing:border-box}body{margin:0;background:#eef2f1;color:var(--ink);font:16px/1.72 'Segoe UI',Arial,sans-serif}
header{background:#183e40;color:#f8fcfa;padding:34px max(24px,calc((100vw - 1100px)/2));border-bottom:5px solid #d2b076}
header small{letter-spacing:.13em;text-transform:uppercase;color:#c8dcd7}header p{margin:8px 0 0;max-width:760px}
main{max-width:1160px;margin:auto;padding:24px 24px 60px}section{background:white;padding:28px 38px;margin:0 0 20px;border-radius:9px;box-shadow:0 3px 18px #153f3a08}
h1{font-size:34px;line-height:1.2;max-width:850px}h2{font-size:25px;line-height:1.3;margin:5px 0 22px}p{margin:0 0 16px}strong{font-weight:650}a{color:#226d68}
table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.5;margin:24px 0;display:block;overflow:auto}thead{background:#e9f1ef}th,td{padding:11px 13px;text-align:left;border-bottom:1px solid #dfe7e5}th{font-weight:650}tbody tr:nth-child(even){background:#f8faf9}td:not(:first-child){font-variant-numeric:tabular-nums}
code{background:#eff3f2;padding:2px 5px;border-radius:4px;font-size:.88em;overflow-wrap:anywhere}li{margin:6px 0}.chart{background:white;padding:14px 24px 24px;border-radius:9px;margin:0 0 24px;overflow:hidden}
.nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 22px}.nav a{text-decoration:none;background:white;padding:6px 12px;border-radius:6px;font-size:14px;color:#275d59}
.chart-note{font-size:14px;color:#52666a;padding:0 24px 20px;margin:-8px 0 16px}
.foot{color:var(--muted);font-size:13px;margin:28px 0}ul{padding-left:25px}section p:last-child{margin-bottom:0}
@media(max-width:700px){main{padding:16px 10px}section{padding:22px 18px}.chart{padding:5px}h1{font-size:28px}h2{font-size:22px}body{font-size:15px}header{padding:22px}table{font-size:12px}}
@media print{body{background:white}header,.nav,.modebar{display:none}section{box-shadow:none;padding:12px 0;break-inside:avoid}.chart{break-inside:avoid}main{max-width:none;padding:0}}
"""
nav='<nav class="nav">'+''.join('<a href="#'+key+'">'+title+'</a>' for key,title in [("transitions","Три стадии перехода"),("working-audit","Аудит доли работающих"),("regimes","Уклады"),("ai","Автономные системы"),("leisure","Работа и досуг"),("media","Медиа"),("popularity","Популярность"),("history","История"),("factors","Факторы"),("cases","Примеры"),("methods","Методика")])+"</nav>"
page='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Общества, гарантии и утопичность — исследование 890 записей</title><style>'+css+'</style></head><body><header><small>Исследовательский отчёт · 22.10.2026</small><p>Корреляции, многомерные модели и осторожные гипотезы по каталогу вымышленных обществ</p></header><main>'+nav+''.join(body)+'<p class="foot">Производные данные и код находятся рядом с отчётом. Исходные 890 записей не изменены. Интерактивные графики работают без подключения к сети.</p></main></body></html>'
(OUT/"report.html").write_text(page,encoding="utf-8")
print(json.dumps(dict(markdown=str(OUT/"report.md"),html=str(OUT/"report.html"),sections=len(sections),charts=len(figures),html_bytes=len(page.encode("utf-8"))),ensure_ascii=False))

