"""Compare all three labour-transition stages without altering the catalogue."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy import stats

import analyze_societies as core

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"research"/"exploratory-analysis"
RAW=core.RAW
STAGES=["zero_variant","transition","post_work"]
LABELS={"zero_variant":"Переход не состоялся","transition":"Частичный переход","post_work":"Переход состоялся"}
ST=np.array([r["post_work_assessment"]["status"] for r in RAW])
GI=core.GI
W=core.W
U,P,S,C,L=core.U,core.P,core.S,core.C,core.L


def region(r):
    base=3 if r["axis"]["control"]>1/3 else 5 if r["axis"]["control"]<=-1/3 else 1
    return base+(0 if r["axis"]["guarantees"]<0 else 1)


REG=np.array([r["regime_primary"] or region(r) for r in RAW])
GEO=np.array([region(r) for r in RAW])
SEC=S>0
MEDIA=[m for m in core.MEDIA if core.MED[m].sum()>=15]
MX=np.column_stack([core.MED[m] for m in MEDIA]).astype(float)
T=(ST=="transition").astype(float)
F=(ST=="post_work").astype(float)


def summary(mask):
    ix=np.flatnonzero(mask)
    if not len(ix):return {"n":0,"groups":0}
    y=U[ix]
    w=1/np.bincount(GI[ix],minlength=len(core.GROUPS))[GI[ix]]
    res=core.summary(mask)
    res.update(mean_security=core.avg(S[ix]),mean_control=core.avg(C[ix]),
               median_nonworking=float(np.median(L[ix])),share_majority_working=float(np.mean(L[ix]<=.5)),
               no_one_works_share=float(np.mean(L[ix]>=.95)),
               secure_share=float(np.mean(SEC[ix])),mean_abs_utopia=float(np.mean(abs(y))),
               std_utopia=float(np.std(y,ddof=1)),central_share=float(np.mean((y>-.5)&(y<.5))),
               population_proxy_share=float(np.mean([RAW[i]["scope"].get("human_population_proxy",False) for i in ix])),
               group_balanced_secure=core.avg(SEC[ix],w),group_balanced_nonworking=core.avg(L[ix],w),
               group_balanced_strong_utopia=core.avg(y>=.5,w),group_balanced_mean_abs_utopia=core.avg(abs(y),w))
    return res


def save_csv(name,rows):core.csvwrite(name,rows)
def save(name,value):core.save(name,value)


def main():
    assert Counter(ST)==Counter(zero_variant=345,transition=75,post_work=470)
    by_stage={st:summary(ST==st) for st in STAGES}
    regime_rows=[]
    for st in STAGES:
        for k in range(1,7):
            mask=ST==st
            regime_rows.append(dict(stage=st,regime=k,n=int(np.sum(mask&(REG==k))),share=float(np.mean(REG[mask]==k)),
                                   all_coordinate_n=int(np.sum(mask&(GEO==k))),all_coordinate_share=float(np.mean(GEO[mask]==k))))
    save_csv("transition-regime-counts.csv",regime_rows)
    media_rows=[]
    for m in MEDIA:
        for st in STAGES:
            mask=core.MED[m]&(ST==st)
            media_rows.append(dict(medium=m,stage=st,media_n=int(core.MED[m].sum()),share_in_medium=float(mask.sum()/core.MED[m].sum()),**summary(mask)))
    save_csv("transition-media-counts.csv",media_rows)
    security_rows=[]
    for st in STAGES:
        for sec in [False,True]:
            mask=(ST==st)&(SEC==sec)
            security_rows.append(dict(stage=st,has_guarantees=sec,**summary(mask)))
    save_csv("transition-security-counts.csv",security_rows)
    control_rows=[]
    for st in STAGES:
        for fam,ks in [("elite",[1,2]),("distributed",[3,4]),("autonomous",[5,6])]:
            control_rows.append(dict(stage=st,control_family=fam,**summary((ST==st)&np.isin(REG,ks))))
    save_csv("transition-control-counts.csv",control_rows)
    alloc=[]
    for st in STAGES:
        for k in sorted(set(core.CODE)):
            alloc.append(dict(stage=st,manual_code=k,n=int(np.sum((ST==st)&(core.CODE==k)))))
    save_csv("transition-allocation-counts.csv",alloc)
    models={}
    all_tests=[]
    def run_model(name,y,x,names,weights=W,groups=GI,intercept=True):
        m=core.fit(y,x,names,weights,groups,intercept=intercept)
        models[name]=core.public(m)
        for c in m["coefficients"]:
            if c["term"] in ["partial_transition","full_transition"]:
                all_tests.append(dict(model=name,**c))
        if "partial_transition" in m["_names"] and "full_transition" in m["_names"]:
            ct=core.contrast(m,{"full_transition":1,"partial_transition":-1})
            models[name]["full_minus_partial"]=ct
            all_tests.append(dict(model=name,term="full_minus_partial",**ct))
        return m
    stage_x=np.column_stack([T,F])
    media_x=np.column_stack([T,F,P,MX])
    media_names=["partial_transition","full_transition","popularity"]+["media_"+m for m in MEDIA]
    full_x=np.column_stack([T,F,S,C,C*C,L,P,MX])
    full_names=["partial_transition","full_transition","security","control","control_squared","nonworking","popularity"]+["media_"+m for m in MEDIA]
    run_model("utopia_raw",U,stage_x,["partial_transition","full_transition"])
    run_model("utopia_media_adjusted",U,media_x,media_names)
    run_model("utopia_structural_adjusted",U,full_x,full_names)
    interaction=run_model("utopia_security_interaction",U,np.column_stack([full_x,T*S,F*S]),full_names+["partial_x_security","full_x_security"])
    for c in interaction['coefficients']:
        if c['term'].endswith('_x_security'):all_tests.append(dict(model='utopia_security_interaction',**c))
    # Saved intervals are editorial scenarios, not statistical confidence bounds.
    intervals={axis:np.array([r['axis_assessment'][axis]['interval'] for r in RAW]) for axis in ['guarantees','control','nonworking']}
    rng=np.random.default_rng(20261022)
    scenario=[]
    for _ in range(500):
        ss=-rng.uniform(*intervals['guarantees'].T);cc=rng.uniform(*intervals['control'].T);ll=rng.uniform(*intervals['nonworking'].T)
        xx=np.column_stack([np.ones(len(RAW)),T,F,ss,cc,cc*cc,ll,P,MX])
        bb=np.linalg.lstsq(xx*np.sqrt(W[:,None]),U*np.sqrt(W),rcond=None)[0]
        scenario.append([bb[1],bb[2],bb[2]-bb[1]])
    scenario=np.array(scenario)
    coordinate_scenarios=dict(replicates=500,assumption='Independent uniform draws within saved axis intervals; utopia and popularity fixed; not posterior probabilities or confidence intervals',
        coefficients={name:dict(median=float(np.median(scenario[:,j])),low=float(np.quantile(scenario[:,j],.025)),high=float(np.quantile(scenario[:,j],.975)),positive_share=float(np.mean(scenario[:,j]>0))) for j,name in enumerate(['partial_vs_zero','full_vs_zero','full_vs_partial'])})
    for name,y in [("extremity",abs(U)),("strong_dystopia",(U<=-.5).astype(float)),("strong_utopia",(U>=.5).astype(float)),
                   ("secure",SEC.astype(float)),("nonworking",L),("popularity",P)]:
        xx=np.column_stack([stage_x,MX])
        names=["partial_transition","full_transition"]+["media_"+m for m in MEDIA]
        run_model(name+"_media_adjusted",y,xx,names)
    # U comparisons within recognition groups. Some are distinct states rather than timelines.
    xy=np.column_stack([T,F,S,C,C*C,L])
    wy=U.copy();wx=xy.copy()
    for g in range(len(core.GROUPS)):
        mask=GI==g;wy[mask]-=np.mean(wy[mask]);wx[mask]-=np.mean(wx[mask],axis=0)
    active=core.COUNTS[GI]>1
    run_model("within_group_stages_only",wy[active],wx[active,:2],["partial_transition","full_transition"],W[active],GI[active],False)
    run_model("within_group_structural",wy[active],wx[active],["partial_transition","full_transition","security","control","control_squared","nonworking"],W[active],GI[active],False)
    resident_ids={r["id"] for r in core.read("research/scope-audit.json")["records"]}
    masks={
        "resident_scope":np.array([r["id"] in resident_ids for r in RAW]),
        "no_proxy":np.array([not r["scope"].get("human_population_proxy",False) for r in RAW]),
        "no_projection_or_configurable":np.array([not r["scope"].get("projection_status") and not r["scope"].get("player_configurable") for r in RAW]),
        "exclude_largest_10_groups":~np.isin(GI,np.argsort(core.COUNTS)[-10:]),
    }
    for label,mask in masks.items():
        wi=1/np.bincount(GI[mask],minlength=len(core.GROUPS))[GI[mask]]
        run_model("sensitivity_"+label,U[mask],full_x[mask],full_names,wi,GI[mask])
    for r,q in zip(all_tests,core.bh([r["p"] for r in all_tests])):r["q_BH"]=float(q)
    save_csv("transition-tests.csv",all_tests)
    group_rows=[]
    comparisons={}
    for g,gid in enumerate(core.GROUPS):
        mask=GI==g;stages={st:U[mask&(ST==st)] for st in STAGES}
        if sum(len(v)>0 for v in stages.values())<2:continue
        row=dict(group_id=gid,subject=next(r["popularity_assessment"]["subject"] for r,k in zip(RAW,mask) if k))
        for st,vals in stages.items():
            row[st+"_n"]=len(vals)
            row[st+"_utopia"]=float(vals.mean()) if len(vals) else None
        group_rows.append(row)
    for a,b in [("post_work","zero_variant"),("transition","zero_variant"),("post_work","transition")]:
        diffs=[r[a+"_utopia"]-r[b+"_utopia"] for r in group_rows if r[a+"_n"] and r[b+"_n"]]
        arr=np.array(diffs)
        rng=np.random.default_rng(20261022)
        boots=np.array([rng.choice(arr,len(arr),replace=True).mean() for _ in range(5000)])
        comparisons[a+"_minus_"+b]=dict(groups=len(arr),mean_difference=float(arr.mean()),median_difference=float(np.median(arr)),positive_groups=int(np.sum(arr>0)),negative_groups=int(np.sum(arr<0)),ties=int(np.sum(arr==0)),low=float(np.quantile(boots,.025)),high=float(np.quantile(boots,.975)))
    save_csv("transition-interesting-groups.csv",group_rows)
    # Dates remain a provisional saved-metadata subset.
    dated_records={r["id"]:r for r in csv.DictReader((OUT/"analysis-records.csv").open(encoding="utf-8-sig"))}
    chronological=[]
    for label,lo,hi in [("before_1950",1800,1949),("1950_1979",1950,1979),("1980_1999",1980,1999),("2000_2009",2000,2009),("2010_2026",2010,2026)]:
        mask=np.array([bool(dated_records[r["id"]]["publication_year"]) and lo<=int(dated_records[r["id"]]["publication_year"] or 0)<=hi for r in RAW])
        for st in STAGES:
            chronological.append(dict(era=label,stage=st,n=int(np.sum(mask&(ST==st))),era_n=int(mask.sum()),share=float(np.mean(ST[mask]==st))))
    save_csv("transition-chronology.csv",chronological)
    # Record-level export preserves the original status and regime.
    records=[]
    for i,r in enumerate(RAW):
        records.append(dict(id=r["id"],name=r["name"],work=r["work"],group=r["popularity_assessment"]["subject_id"],
                            stage=ST[i],original_regime=r["regime_primary"],chart_regime=int(REG[i]),coordinate_region=int(GEO[i]),
                            media=r["media"],utopia=float(U[i]),security=float(S[i]),control=float(C[i]),nonworking=float(L[i]),popularity=float(P[i])))
    save_csv("transition-records.csv",records)
    result=dict(stage_order=STAGES,labels=LABELS,stages=by_stage,regimes=regime_rows,media=media_rows,security=security_rows,control=control_rows,
                models=models,tests=all_tests,paired_groups=comparisons,chronology=chronological,coordinate_scenarios=coordinate_scenarios,
                input_sha256=hashlib.sha256((ROOT/"data/societies.json").read_bytes()).hexdigest(),
                method="Three saved post_work_assessment.status categories. Chart regimes preserve 1-6; only regime 0 uses guarantee split at 0 and control splits +/-1/3. Full coordinate classification is a sensitivity check. Inverse recognition-group size weights, CR1 group-clustered errors, BH within new test family. No temporal or causal transition effect inferred.")
    save("transition-analysis.json",result)
    print(json.dumps(dict(stages={st:dict(n=v['n'],utopia=v['mean_utopia'],std=v['std_utopia'],extremity=v['mean_abs_utopia'],nonworking=v['mean_nonworking'],secure=v['secure_share']) for st,v in by_stage.items()},paired=comparisons),ensure_ascii=False,indent=2))


if __name__=="__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
