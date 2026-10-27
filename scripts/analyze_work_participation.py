"""Audit what working participation measures and compare transition stages.

All results are derivatives. The catalogue and previous slide decks are unchanged.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy import stats
import plotly.graph_objects as go
import plotly.io as pio
import markdown
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import analyze_societies as core

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/exploratory-analysis"
RAW = core.RAW
ST = ["zero_variant", "transition", "post_work"]
LABEL = dict(zip(ST, ["Трудовые", "Частичный переход", "Посттрудовые"]))
COLOR = dict(zip(ST, ["#7b8896", "#d69c46", "#277f75"]))
STATUS = np.array([r["post_work_assessment"]["status"] for r in RAW])
WORK = 100 * (1 - core.L)
LO = 100 * (1 - np.array([r["axis_assessment"]["nonworking"]["interval"][1] for r in RAW]))
HI = 100 * (1 - np.array([r["axis_assessment"]["nonworking"]["interval"][0] for r in RAW]))
WIDTH = HI - LO
N = len(RAW)
SEED = 20261023
RNG = np.random.default_rng(SEED)
SOURCE_HASH = hashlib.sha256((ROOT / "data/societies.json").read_bytes()).hexdigest()
RESIDENT_IDS = {r["id"] for r in core.read("research/scope-audit.json")["records"]}
def current_resident_scope(record):
    population = record['scope']['population'].lower()
    broad = re.search(r'\b(residents|citizens|inhabitants|colonists|settlers|passengers|world population|national population|human population|humanity|populace)\b', population)
    narrow = re.search(r'\b(one|single|sole|crew|household|child|children|captain|commander|commanders|operators|technicians|owner|owners|factory|employees|staff|workers|researchers|prisoners|clones|elite)\b', population)
    return bool(broad and not narrow)


RESIDENT = np.array([current_resident_scope(r) for r in RAW])
NO_PROXY = np.array([not r["scope"].get("human_population_proxy", False) for r in RAW])


def summarize(mask):
    a = WORK[mask]
    g = core.GI[mask]
    local_w = 1 / np.bincount(g, minlength=len(core.GROUPS))[g]
    return dict(n=len(a), groups=len(np.unique(g)), mean=float(a.mean()),
                median=float(np.median(a)), q25=float(np.quantile(a, .25)),
                q75=float(np.quantile(a, .75)), minimum=float(a.min()), maximum=float(a.max()),
                group_balanced_mean=float(np.average(a, weights=local_w)),
                at_least_half=int(np.sum(a >= 50 - 1e-8)),
                strictly_more_than_half=int(np.sum(a > 50 + 1e-8)),
                at_most_10=int(np.sum(a <= 10 + 1e-8)), at_most_5=int(np.sum(a <= 5 + 1e-8)),
                exactly_zero=int(np.sum(np.isclose(a, 0))), exactly_100=int(np.sum(np.isclose(a, 100))),
                editorial_mean_min=float(LO[mask].mean()), editorial_mean_max=float(HI[mask].mean()),
                median_interval_width=float(np.median(WIDTH[mask])))


def interval(values):
    return dict(low=float(np.quantile(values, .025)), high=float(np.quantile(values, .975)))


def model(mask, adjusted=False):
    x = np.column_stack([(STATUS[mask] == st).astype(float) for st in ST[1:]])
    names = ["partial_vs_work_based", "post_work_vs_work_based"]
    if adjusted:
        media = [m for m in core.MEDIA if 15 <= core.MED[m][mask].sum() < mask.sum()]
        x = np.column_stack([x, *[core.MED[m][mask] for m in media]])
        names += ["medium_" + m for m in media]
    g = core.GI[mask]
    weights = 1 / np.bincount(g, minlength=len(core.GROUPS))[g]
    return core.public(core.fit(WORK[mask], x, names, weights, g))


def f(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def pct(n, total):
    return f(100 * n / total) + "%"


def main():
    assert Counter(STATUS) == Counter(zero_variant=345, transition=75, post_work=470)
    assert np.all((0 <= LO) & (LO <= WORK + 1e-8) & (WORK <= HI + 1e-8) & (HI <= 100))
    summary = {s: summarize(STATUS == s) for s in ST}
    sensitivity = {}
    for name, mask in {
        "all": np.ones(N, bool), "resident_scope": RESIDENT,
        "resident_nonproxy": RESIDENT & NO_PROXY,
        "exclude_exact_endpoints": (WORK > 0) & (WORK < 100),
        "exclude_largest_10_groups": ~np.isin(core.GI, np.argsort(core.COUNTS)[-10:]),
    }.items():
        cells = {s: summarize(mask & (STATUS == s)) for s in ST}
        sensitivity[name] = dict(stages=cells, post_minus_work_based=cells[ST[2]]["mean"] - cells[ST[0]]["mean"])

    # Bootstrap recognition groups together, retaining all their societies/stages.
    group_n = np.zeros((len(core.GROUPS), 3))
    group_sum = np.zeros_like(group_n)
    for j, st in enumerate(ST):
        ix = STATUS == st
        np.add.at(group_n[:, j], core.GI[ix], 1)
        np.add.at(group_sum[:, j], core.GI[ix], WORK[ix])
    multiplicity = RNG.multinomial(len(core.GROUPS), np.full(len(core.GROUPS), 1 / len(core.GROUPS)), size=5000)
    boot_means = (multiplicity @ group_sum) / (multiplicity @ group_n)
    paired = []
    for gi, gid in enumerate(core.GROUPS):
        if group_n[gi, 0] and group_n[gi, 2]:
            d = group_sum[gi, 2] / group_n[gi, 2] - group_sum[gi, 0] / group_n[gi, 0]
            paired.append(dict(group_id=gid, group=next(r["popularity_assessment"]["subject"] for r in RAW if r["popularity_assessment"]["subject_id"] == gid),
                               work_based_n=int(group_n[gi, 0]), post_work_n=int(group_n[gi, 2]), difference=float(d)))
    pd = np.array([r["difference"] for r in paired])
    paired_boot = RNG.choice(pd, (5000, len(pd)), replace=True).mean(axis=1)
    within = dict(groups=len(pd), mean=float(pd.mean()), median=float(np.median(pd)),
                  lower=int(np.sum(pd < -1e-8)), higher=int(np.sum(pd > 1e-8)), ties=int(np.sum(abs(pd) <= 1e-8)),
                  bootstrap_replicates=5000, **interval(paired_boot))
    binary = STATUS != "transition"
    u = stats.mannwhitneyu(WORK[STATUS == "zero_variant"], WORK[STATUS == "post_work"], alternative="two-sided").statistic
    auc = float(u / (345 * 470))
    # This is a descriptive ranking probability, not a held-out classifier score.
    grand = WORK.mean()
    eta2 = float(sum(summary[s]["n"] * (summary[s]["mean"] - grand)**2 for s in ST) / np.sum((WORK-grand)**2))
    bounds = [summary[ST[2]]["editorial_mean_min"] - summary[ST[0]]["editorial_mean_max"],
              summary[ST[2]]["editorial_mean_max"] - summary[ST[0]]["editorial_mean_min"]]
    models = {"group_balanced": model(np.ones(N, bool)),
              "group_balanced_media": model(np.ones(N, bool), True),
              "resident_group_balanced_media": model(RESIDENT, True)}
    quality = dict(confidence=Counter(r["axis_assessment"]["nonworking"]["confidence"] for r in RAW),
                   median_interval_width=float(np.median(WIDTH)), interval_at_least_50pp=int(np.sum(WIDTH >= 50-1e-8)),
                   interval_allows_both_endpoints=int(np.sum((LO == 0) & (HI == 100))),
                   explicit_participation_definitions=sum(bool(r.get("participation_definition")) for r in RAW),
                   nonempty_reported_labor_statistics=sum(bool(r.get("reported_labor_statistics")) for r in RAW),
                   reported_statistic_items=sum(len(r.get("reported_labor_statistics") or []) for r in RAW),
                   five_percentage_point_grid=int(np.sum(np.isclose(WORK / 5, np.round(WORK / 5)))),
                   exact_zero_working=int(np.sum(WORK == 0)), exact_all_working=int(np.sum(WORK == 100)))
    out = dict(input_sha256=SOURCE_HASH, seed=SEED, n=N, stage_order=ST,
               formula="working_percent = 100 * (1 - axis.nonworking)", stages=summary,
               raw_post_minus_work_based=dict(beta=summary[ST[2]]["mean"] - summary[ST[0]]["mean"],
                                              **interval(boot_means[:, 2]-boot_means[:, 0])),
               stage_mean_bootstrap={st: interval(boot_means[:, j]) for j, st in enumerate(ST)},
               ranking_probability_work_based_higher=auc, one_way_eta_squared=eta2,
               within_recognition_groups=within, sensitivity=sensitivity, models=models, quality=quality,
               resident_scope_filter=dict(n=int(RESIDENT.sum()), rule='Current scope.population: broad resident/citizen/inhabitant/colonist/settler/passenger/population words, conservatively excluding narrow role/household/child/singleton wording. No canon or demographic verification.',
                                          old_audit_date='2026-10-17',old_audit_ids_not_reused=True,
                                          old_ids_no_longer_passing=int(sum(r['id'] in RESIDENT_IDS and not RESIDENT[i] for i,r in enumerate(RAW)))),
               editorial_box_bounds_post_minus_work_based=bounds,
               caveat="All percentages concern scoped persons and editorial participation, not population-weighted rates, time, output or necessary production staffing. Bootstrap uncertainty holds scores fixed; editorial interval bounds are neither confidence intervals nor posterior probabilities.")
    core.save("working-participation-analysis.json", out)
    core.csvwrite("working-participation-by-stage.csv", [dict(stage=s, **summary[s]) for s in ST])
    core.csvwrite("working-participation-paired-groups.csv", paired)

    audit = []
    for i, r in enumerate(RAW):
        flags = []
        if np.isclose(WORK[i], 0): flags.append("exact_zero_working_single_person_reviewed")
        if np.isclose(WORK[i], 100): flags.append("all_scoped_people_work")
        if WORK[i] <= 5 + 1e-8: flags.append("working_at_most_5_percent_reviewed")
        if WIDTH[i] >= 50 - 1e-8: flags.append("interval_at_least_50pp")
        if LO[i] == 0 and HI[i] == 100: flags.append("interval_allows_zero_and_100")
        if not RESIDENT[i]: flags.append("outside_conservative_resident_filter")
        audit.append(dict(id=r["id"], name=r["name"], stage=STATUS[i], working_percent=float(WORK[i]),
                          working_min=float(LO[i]), working_max=float(HI[i]), confidence=r["axis_assessment"]["nonworking"]["confidence"],
                          population=r["scope"]["population"], resident_filter=bool(RESIDENT[i]), person_proxy=not bool(NO_PROXY[i]),
                          basis=r["axis_assessment"]["nonworking"]["basis"],
                          production_dependence=r["post_work_assessment"]["production_dependence"],
                          wage_dependence=r["post_work_assessment"]["wage_dependence"],
                          participation_definition=r.get("participation_definition"), reported_labor_statistics=r.get("reported_labor_statistics"),
                          source_ids=r["axis_assessment"]["nonworking"]["source_ids"], review_flags=flags))
    core.csvwrite("working-participation-record-audit.csv", audit)
    low = [r for r in audit if r["working_percent"] <= 5 + 1e-8]
    core.save("working-participation-low-work-cases.json", [RAW[i] for i in range(N) if WORK[i] <= 5 + 1e-8])

    figures = {}
    fig = go.Figure()
    for st in ST:
        ix = np.flatnonzero(STATUS == st)
        fig.add_trace(go.Box(x=[LABEL[st]]*len(ix), y=WORK[ix], name=LABEL[st], marker_color=COLOR[st],
                             boxpoints="all", jitter=.42, pointpos=0, marker_size=4, fillcolor=COLOR[st], opacity=.7,
                             customdata=[[RAW[i]["name"], RAW[i]["scope"]["population"], LO[i], HI[i]] for i in ix],
                             hovertemplate="%{customdata[0]}<br>Работает: %{y:.1f}%<br>Редакторский диапазон: %{customdata[2]:.0f}–%{customdata[3]:.0f}%<br>%{customdata[1]}<extra></extra>"))
    fig.update_layout(showlegend=False)
    figures["working-distribution"] = fig
    fig = go.Figure()
    bins = [(0, 10, "0–10%"), (10, 25, ">10–25%"), (25, 50, ">25–50%"), (50, 75, ">50–75%"), (75, 100, ">75–100%")]
    bin_rows = []
    for lo, hi, label in bins:
        vals=[]
        for st in ST:
            m=(STATUS==st) & (WORK<=hi+1e-8) & ((WORK>=lo-1e-8) if lo==0 else (WORK>lo+1e-8))
            vals.append(100*m.sum()/summary[st]["n"])
            bin_rows.append(dict(stage=st,working_band=label,n=int(m.sum()),share=float(vals[-1]/100)))
        fig.add_bar(name=label,x=[LABEL[s] for s in ST],y=vals,text=[f(v)+"%" if v>=4 else "" for v in vals],textposition="inside")
    fig.update_layout(barmode="stack",colorway=["#9c5d91","#6874b5","#5c9d85","#277f75","#ad654d"])
    figures["working-bands"] = fig
    core.csvwrite("working-participation-bands.csv", bin_rows)
    fig=go.Figure()
    for st in ST:
        v=np.sort(WORK[STATUS==st])
        fig.add_scatter(x=v,y=np.arange(1,len(v)+1)/len(v)*100,mode="lines",line=dict(color=COLOR[st],width=3),name=LABEL[st],
                        hovertemplate="Работает ≤ %{x:.1f}%<br>Доля обществ: %{y:.1f}%<extra>%{fullData.name}</extra>")
    figures["working-ecdf"] = fig
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=[r["working_percent"] for r in low],y=[r["name"] for r in low],mode="markers",marker=dict(color="#277f75",size=9),
                             error_x=dict(type="data",symmetric=False,array=[r["working_max"]-r["working_percent"] for r in low],arrayminus=[r["working_percent"]-r["working_min"] for r in low]),
                             customdata=[[r["population"],r["basis"]] for r in low],hovertemplate="%{y}<br>Центральная оценка: %{x:.0f}%<br>%{customdata[0]}<br>%{customdata[1]}<extra></extra>"))
    figures["working-low-cases"] = fig
    for name, fig in figures.items():
        fig.update_layout(template="plotly_white",font=dict(family="Arial",size=15,color="#23343a"),
                          height=700 if name=="working-low-cases" else 500,
                          margin=dict(l=80 if name!="working-low-cases" else 380,r=35,t=35,b=75),legend=dict(orientation="h",y=-.2))
        if name in {"working-distribution","working-bands"}:fig.update_yaxes(title="Доля людей, %" if name=="working-distribution" else "Доля обществ, %",range=[-3,103])
        else:fig.update_xaxes(title="Доля работающих, %",range=[-2,102])
        if name=="working-ecdf":fig.update_yaxes(title="Накопленная доля обществ, %",range=[0,100])
        if name=="working-low-cases":fig.update_yaxes(autorange="reversed",tickfont=dict(size=12))
        (OUT/("chart-"+name+".json")).write_text(pio.to_json(fig),encoding="utf8")

    # A standalone scientific figure complements the interactive report.
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'svg.fonttype':'none'})
    static, ax = plt.subplots(figsize=(13, 7.4), dpi=150)
    static.subplots_adjust(left=.24,right=.97,top=.79,bottom=.29)
    jitter = np.random.default_rng(SEED)
    for j, st in enumerate(ST):
        yy=3-j; vv=WORK[STATUS==st]
        bp=ax.boxplot([vv],positions=[yy],vert=False,widths=.4,whis=(0,100),showfliers=False,patch_artist=True,
                      boxprops=dict(facecolor=COLOR[st],edgecolor=COLOR[st],alpha=.3),medianprops=dict(color='#23343a',linewidth=2),
                      whiskerprops=dict(color=COLOR[st]),capprops=dict(color=COLOR[st]))
        ax.scatter(vv,yy+jitter.uniform(-.24,.24,len(vv)),s=13,color=COLOR[st],alpha=.35,linewidths=0)
        ax.scatter([vv.mean()],[yy],marker='D',s=70,color='#23343a',zorder=5)
        ax.annotate(f(vv.mean())+'%',(vv.mean(),yy),xytext=(0,28),textcoords='offset points',ha='center',fontweight='bold',color='#23343a')
    ax.set_yticks([3,2,1],[LABEL[s]+'\nn = '+str(summary[s]['n']) for s in ST]);ax.set_ylim(.4,3.7)
    ax.set_xlim(-2,102);ax.set_xticks(range(0,101,10));ax.set_xlabel('Доля работающих в выбранном населении, %',labelpad=12)
    ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
    for sp in ax.spines.values():sp.set_visible(False)
    ax.tick_params(axis='y',length=0,pad=16)
    static.text(.045,.93,'Работа и стадия посттрудового перехода',fontsize=23,fontweight='bold',color='#23343a')
    static.text(.045,.87,'В центральной разметке участие ниже после перехода, но распределения перекрываются.',fontsize=13,color='#60747a')
    static.text(.045,.115,'Ромб — среднее. Полоса — 25–75-й процентили, линия — медиана. Усы — минимум и максимум.\nКаждая точка — одна запись, независимо от численности её населения.',fontsize=11,color='#60747a',linespacing=1.6)
    static.text(.045,.035,'886 из 890 оценок имеют низкую уверенность. Участие включает добровольную деятельность и заботу.\nИсточник: data/societies.json. Аудит 23.10.2026.',fontsize=11,color='#60747a',linespacing=1.5)
    static.savefig(OUT/'working-participation-distribution.png',facecolor='white')
    static.savefig(OUT/'working-participation-distribution.svg',facecolor='white')
    plt.close(static)

    sections=[]
    sections.append(dict(key="working-audit",markdown=f"""## Аудит доли работающих: что означает показатель

**В текущей разметке посттрудовые общества в среднем имеют меньше работающих, но процент нельзя читать как измеренную занятость или человеческий вклад в выпуск.** Формула: `working_percent = 100 × (1 − axis.nonworking)`.

В числителе предполагаются люди или явно указанные разумные личности с регулярной полезной деятельностью либо назначенной ролью. Включены добровольная наука, творчество, забота, услуги и обязательные задания, даже технически ненужные. В знаменателе — население из `scope.population`: в одних случаях все жители вместе с детьми, в других только экипаж, цифровые личности или один человек. Единого периода наблюдения, минимального числа часов и операционального критерия «полезности» нет. Учёба для себя, отдых и пассивное содержание тела автоматически работой не считаются; полезная деятельность внутри симуляции может считаться.

Нужно различать четыре величины:

| Показатель | Какой вопрос он отвечает | Что есть в базе |
|---|---|---|
| Участие в деятельности | Какая доля людей делает регулярную полезную работу или выполняет назначения? | `axis.nonworking`, редакторская оценка |
| Обязательность работы для получения благ | Нужно ли работать, чтобы иметь доступ к содержанию? | `wage_dependence`, `allocation_mechanisms`, статус перехода |
| Необходимая производственная занятость | Сколько людей нужно для выпуска и поддержания системы? | Чаще качественное `production_dependence`, редкие отдельные числа |
| Доля выпуска, произведённого людьми | Какой вклад люди вносят в совокупное производство? | Единой числовой переменной нет |

По описанной методике числа назначали вручную по сюжету и масштабу населения, затем превращали `nonworking` в процент дополнением до 100. Это не подсчёт работников по списку персонажей и не статистика из переписи. У **{quality['confidence']['low']} из 890 оценок низкая уверенность**, у остальных четырёх средняя. Медианная ширина сохранённого диапазона составляет **{f(quality['median_interval_width'],0)} п.п.** У {quality['interval_at_least_50pp']} записей ширина не менее 50 п.п.; {quality['interval_allows_both_endpoints']} допускают одновременно 0 и 100% работающих. На сетке с шагом 5 п.п. лежат {quality['five_percentage_point_grid']} записей. Внешняя точность вида «70%» гораздо выше точности оснований.

Непустой `reported_labor_statistics` есть только у {quality['nonempty_reported_labor_statistics']} записей, всего {quality['reported_statistic_items']} числа. Они описывают другие величины: безработицу, необходимый производственный персонал или получение гарантированного дохода. Явного отдельного `participation_definition` лишь три, хотя общее определение дано в README и развёрнуто в индивидуальных основаниях.

История подтверждает риск подмены понятий: в `research/revisions/revision-053.json` у жителей Terrafoam из «Манны» уже исправляли вывод из безработицы. Раньше ставили 99% неработающих, затем 80%, поскольку забота, взаимопомощь и добровольное творчество тоже считаются работой. Это исправление смысла оценки, а не новая перепись. Текущие 20% работающих остаются иллюстративным сценарием. Иначе можно правильно описать почти полное замещение оплачиваемых должностей, но неправильно объявить людей бездеятельными.

Все 890 оснований выгружены в [таблицу аудита](working-participation-record-audit.csv). Числа в основной базе не изменены. Прочитаны основания всех крайних случаев до 5% работающих; это проверка разметки, а не полный повторный просмотр произведений.
"""))
    table="| Показатель | Трудовые | Частичный переход | Посттрудовые |\n|---|---:|---:|---:|\n"
    for label,key in [("Обществ","n"),("Средняя доля работающих","mean"),("Медиана","median"),("25-й процентиль","q25"),("75-й процентиль","q75"),("Средняя при равном весе групп внутри стадии","group_balanced_mean"),("Работает не менее половины: число обществ","at_least_half"),("Работает не более 10%: число обществ","at_most_10"),("Ровно 0%: число записей","exactly_zero"),("Ровно 100%: число записей","exactly_100")]:
        table+="| "+label+" | "+" | ".join(str(summary[s][key]) if isinstance(summary[s][key],int) else f(summary[s][key])+"%" for s in ST)+" |\n"
    diff=out['raw_post_minus_work_based']
    adj=next(c for c in models['group_balanced_media']['coefficients'] if c['term']=='post_work_vs_work_based')
    sens_table="| Подвыборка | Трудовые: среднее | Посттрудовые: среднее | Разница, п.п. |\n|---|---:|---:|---:|\n"
    for key,title in [("resident_scope","Консервативный фильтр постоянных жителей"),("resident_nonproxy","Тот же фильтр без прокси населения"),("exclude_exact_endpoints","Без точных 0 и 100%"),("exclude_largest_10_groups","Без 10 крупнейших групп")]:
        a=sensitivity[key];sens_table+=f"| {title} | {f(a['stages'][ST[0]]['mean'])}% (n={a['stages'][ST[0]]['n']}) | {f(a['stages'][ST[2]]['mean'])}% (n={a['stages'][ST[2]]['n']}) | {f(a['post_minus_work_based'])} |\n"
    sections.append(dict(key="working-stage-link",markdown=f"""## Связь участия со стадией перехода

{table}

Разница посттрудовых с трудовыми составляет **{f(diff['beta'])} п.п.** Кластерный bootstrap по 496 группам узнаваемости даёт диапазон [{f(diff['low'])}; {f(diff['high'])}] п.п. при фиксированных редакторских баллах. Доля межстадийного разброса в общем разбросе оценок, η², равна {f(eta2,3)}. В случайной паре из трудового и посттрудового обществ первое имеет более высокий балл участия с вероятностью **{f(100*auc)}%**, учитывая половину равенств. Это описание перекрытия распределений в каталоге, не проверка классификатора на новых произведениях.

После равного веса групп и поправки на пересекающиеся теги медиа разница составляет **{f(adj['beta'])} п.п.**, 95%-ный кластерный интервал [{f(adj['low'])}; {f(adj['high'])}]. В {within['groups']} группах представлены обе стадии: посттрудовые имеют меньшую среднюю долю работающих в {within['lower']} группах, большую в {within['higher']}, равную в {within['ties']}. Средняя парная разница {f(within['mean'])} п.п., bootstrap [{f(within['low'])}; {f(within['high'])}]. Эти пары могут сравнивать разные населения и периоды; это не наблюдение единого общества до и после реформы.

**341 из 470 посттрудовых обществ, или 72,6%, сохраняют участие не менее половины населения.** В 23 посттрудовых записях работают все лица выбранного населения. Поэтому наличие работы не определяет стадию: статус описывает зависимость доступа к благам от труда, а участие — деятельность людей. Даже одинаковый процент может означать принудительную работу, службу или добровольные занятия.

{sens_table}

Фильтр жителей заново применён к текущему `scope.population`: множественные жители, граждане и население, с консервативным исключением упоминаний отдельных лиц, экипажей, рабочих коллективов, детских групп и домохозяйств. Прошедшие строки явно отмечены в таблице аудита. Это текстовый фильтр, а не проверка демографии и лора, он может исключать подходящие общества. Список из `research/scope-audit.json` от 17.10.2026 не использован: после уточнений населения часть его записей стала одиночными случаями. Связь сохраняется без крайних оценок и в более сопоставимых подвыборках, поэтому её нельзя целиком объяснить тремя одиночными нулевыми случаями.

Однако bootstrap отражает только состав каталога при неизменных баллах. Если разрешить каждому баллу любое значение из его сохранённого редакторского диапазона, допустимая разница средних простирается от **{f(bounds[0])} до {f(bounds[1])} п.п.**, включая обратный знак. Это предельные комбинации допущений, не вероятностный интервал. Связь убедительна для центральной разметки, но не установлена независимо от способа её выставления. Поскольку статус и участие размечены по сходным сюжетным признакам, возможна общая ошибка оценивания.

Средние имеют равный вес обществ, а не жителей: один человек в отдельной записи и многомиллиардная цивилизация дают по одной строке. Нельзя читать 58,7% как долю всех людей во всех посттрудовых мирах.
"""))
    case_notes={
        'mudd-android-serviced-captivity':('Гарри Мадд, один человек','Центральный сценарий: андроиды содержат Мадда, постоянной полезной роли ему не приписали. Это не вывод обо всём человечестве Star Trek.'),
        'eden-sara-robot-upbringing':('Сара, один ребёнок','Роботы выращивают и содержат ребёнка. Учёбу саму по себе не сочли работой. Если учитывать регулярную помощь на ферме, двоичный балл меняется на 100% работающих.'),
        'aquila-rift-thom-sanctuary':('Том, один человек','Жизнь в поддерживаемой симуляции; постоянной полезной роли не установлено. Биологический опекун, неопределённость содержания и узость случая делают обобщение особенно слабым.'),
        'walle-axiom':('Пассажиры и капитан Axiom','Автоматическое обслуживание, преимущественно пассажирский досуг, минимальные обязанности капитана. 1% — округлённое предположение, не подсчёт.'),
        'with-folded-hands-two-rivers':('Жители Two Rivers в финале','Машинное обслуживание вытесняет занятия и самостоятельные решения. 1% — оценка почти полного вытеснения, не отсутствие любой человеческой активности.'),
        'comarre-sleeping-enclave':('Сознательные жители машинных снов','Частный опыт во сне при автоматическом содержании. Полезная совместная умственная деятельность считалась бы работой, но её доля не установлена.'),
        'solaria-foundation-earth':('Жители поздней Солярии','Оценка освобождения от рутинного труда; надзор за роботами остаётся возможным. Всё участие надёжно не посчитано.'),
        'last-question-late-humanity':('Поздние люди и их активные сознания','Автоматическое содержание тел. Возможные умственные проекты прямо оставляют неопределённость.'),
        'reynolds-looking-backward':('Будущая Америка Рейнольдса','2% необходимого производственного персонала и 98% получателей гарантированного дохода не дают доли всех деятельных людей. Переход к 5% работающих — редакторская поправка, не число автора.'),
        'doraemon-chamocha-before-revolt':('Жители Чамочи до переворота','Роботы выполняют производственные и сервисные функции. Доля добровольной науки и других занятий неизвестна.'),
        'horizon-eleuthia9-first-generation':('Первое поколение детей в колыбели','Преимущественно дети под машинной опекой, до исчерпания запасов. Это не полноценная возрастная структура цивилизации.'),
    }
    assert set(case_notes)=={r['id'] for r in low}
    cases="| Запись | Работающих | Сохранённый диапазон | Кого считали и что означает число |\n|---|---:|---:|---|\n"
    for row in sorted(low,key=lambda r:(r['working_percent'],r['id'])):
        who,note=case_notes[row['id']]
        cases+=f"| {row['name']} | {f(row['working_percent'],0)}% | {f(row['working_min'],0)}–{f(row['working_max'],0)}% | **{who}.** {note} |\n"
    sections.append(dict(key="working-zero-cases",markdown=f"""## Все нулевые и почти нулевые оценки

**Ровно 0% работающих стоят у трёх записей. Каждая описывает одного человека, каждая имеет низкую уверенность и диапазон 0–100%.** Это не три надёжно установленных полностью праздных цивилизации. Знаменатель из одного человека делает показатель двоичным: при признании хотя бы одной постоянной полезной роли он превращается из 0% в 100%.

{cases}

Официальный [синопсис Eden от Netflix](https://media.netflix.com/en/only-on-netflix/80992783) подтверждает, что роботы тайно воспитывают одного ребёнка; он не измеряет долю её полезной деятельности. В [авторском введении Рейнольдса](https://www.everand.com/book/484777968/Equality-In-the-Year-2000) действительно нужны только 2% населения для производства потребления страны, а 98% получают гарантированный доход. Из этого не следует, что остальные не занимаются наукой, заботой, искусством и общественной жизнью. Эти два первичных источника повторно открыты 23.10.2026. Остальные описания в таблице — аудит сохранённых оснований, без заявления о новом полном просмотре произведений.

У противоположного края тоже есть проблема знаменателя: **69 записей имеют 100% работающих**, из них 23 посттрудовые. Например, в `pantheon-maddie-stellar-project` единственная активная жительница Мэдди занята исследовательским проектом; в `technobabylon-latha-welfare-household` творческие и активистские занятия Латы посчитали работой. Это полезные контрпримеры отождествлению работы с необходимостью зарабатывать, но не демографическая статистика общества.

Показателен и `matrix-pod-humanity`: разметка считает работающими 70% активных человеческих сознаний, включая деятельность внутри симуляции. Неподвижность тел и получение машинами биологической энергии не превращены в показатель праздности. Эта запись показывает, почему доля индустриального человеческого труда и доля деятельных личностей должны оставаться разными величинами.

Здесь есть и отдельный вопрос сопоставимости слоёв: в этой записи стадия перехода описывает физическое содержание тел, а участие — деятельность сознаний внутри симуляции. Без явной маркировки слоя такая пара показателей может выглядеть противоречиво. У ребёнка Сары незарплатная опека, в свою очередь, не устанавливает устройство экономики всех взрослых: зависимость ребёнка от содержания встречается и в обычном трудовом обществе. Одиночные кейсы требуют отдельной интерпретации даже при корректно указанном знаменателе.
"""))
    sections.append(dict(key="working-method-next",markdown="""## Как исправить измерение, не подменив его смысл

Текущий `axis.nonworking` по замыслу измеряет участие в широкой деятельности. Переименовать его во «вклад людей в производство» нельзя: это поменяет смысл данных. При этом точные проценты часто не подкреплены источниками, а неодинаковые знаменатели затрудняют сравнение.

Для следующей ревизии предлагается:

1. Сохранить существующие числа как `legacy_editorial_participation`, а основным результатом показывать качественную оценку и её основание. Числовое неизвестное хранить как `null`, без подстановки 0, 50 или нового выдуманного процента.
2. Для участия явно задать числитель, население, возрастной охват, период и правило регулярности. Разделить общие общества, рабочие коллективы и одиночные случаи. По умолчанию сравнивать сопоставимые постоянные населения; маленькие кейсы показывать отдельно. Это не требует удалять их из каталога.
3. Независимо разметить зависимость доступа к благам от работы и характер деятельности: работа по принуждению, работа ради заработка, добровольные проекты и забота. Один балл участия не различает эти условия.
4. Создать отдельное поле для необходимого человеческого персонала производства и поддержания системы. Число 2% у Рейнольдса относится сюда. Долю выпуска людей и долю рабочего времени при необходимости хранить отдельно, с единицами и знаменателем. `production_dependence` пока остаётся качественным свидетельством.
5. Помечать происхождение каждой величины: авторское число с совместимым определением, вывод из явного состава небольшой группы или редакторский сценарий. Три точных нуля вывести из агрегатов больших обществ и показывать как одиночные сценарии с неустановленным участием.

Проверка обнаружила прежде всего слабость количественной операционализации, а не необходимость механически повысить нулевые значения. Надёжный содержательный вывод уже доступен: работа может сохраняться после постзарплатного перехода, потому что доступ к жизни и фактическая деятельность людей описывают разные стороны общества.

Воспроизведение: `python scripts/analyze_work_participation.py`, затем `python scripts/write_society_analysis_report.py`. Машиночитаемые итоги: [JSON](working-participation-analysis.json), [сводка стадий](working-participation-by-stage.csv), [все записи](working-participation-record-audit.csv), [парные группы](working-participation-paired-groups.csv). Исходный файл, классификация обществ и прежние презентации не редактировались.
"""))
    plot_order={"working-stage-link":["working-distribution","working-bands","working-ecdf"],"working-zero-cases":["working-low-cases"]}
    fragment=dict(input_sha256=SOURCE_HASH,sections=sections,plot_order=plot_order,figure_files={name:"chart-"+name+".json" for name in figures})
    core.save("working-report-fragment.json", fragment)
    md="\n\n".join(s['markdown'] for s in sections)+"\n"
    (OUT/"working-participation.md").write_text(md,encoding="utf8")
    body=[];js=False
    for s in sections:
        body.append('<section id="'+s['key']+'">'+markdown.markdown(s['markdown'],extensions=['tables','fenced_code'])+'</section>')
        for key in plot_order.get(s['key'],[]):
            body.append(pio.to_html(figures[key],include_plotlyjs=not js,full_html=False,div_id='plot-'+key,config=dict(responsive=True,displaylogo=False)))
            js=True
    css="body{margin:0;background:#eef2f1;color:#23343a;font:17px/1.65 'Segoe UI',Arial,sans-serif}main{max-width:1200px;margin:30px auto;padding:0 24px}section{background:white;padding:28px 34px;margin-bottom:20px}h1,h2{line-height:1.3}h2{font-size:26px}table{border-collapse:collapse;display:block;overflow:auto;font-size:14px;margin:24px 0}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #dfe7e5}th{background:#e9f1ef}code{overflow-wrap:anywhere;font-size:.85em}a{color:#226d68}@media(max-width:700px){main{padding:0 8px}section{padding:20px 16px}}"
    (OUT/"working-participation.html").write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Аудит участия в работе</title><style>'+css+'</style><main><h1>Работа и посттрудовой переход: анализ и аудит измерения</h1>'+''.join(body)+'</main></html>',encoding='utf8')
    assert hashlib.sha256((ROOT/'data/societies.json').read_bytes()).hexdigest()==SOURCE_HASH
    core.save('working-participation-validation.json',dict(input_unchanged=True,n=N,stage_counts={s:summary[s]['n'] for s in ST},
               audit_rows=len(audit),low_cases=len(low),all_zero_cases_are_reviewed=True,band_counts_complete=all(sum(r['n'] for r in bin_rows if r['stage']==s)==summary[s]['n'] for s in ST),
               source_hash=SOURCE_HASH,bootstrap_replicates=5000,confidence_intervals_exclude_editorial_uncertainty=True))
    print(json.dumps(dict(stages=summary,quality=quality,raw_difference=diff,adjusted=adj,paired=within,editorial_bounds=bounds,resident=sensitivity['resident_scope']),ensure_ascii=False))


if __name__ == '__main__':
    main()
