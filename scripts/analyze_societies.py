"""Reproducible exploratory analysis of the frozen society catalogue.

Run with Python 3.10, numpy, scipy, sklearn, plotly (no pandas required).
All outputs are derivatives; source classifications are never modified.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import re
import sys
import warnings
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats
from sklearn.decomposition import FactorAnalysis
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "exploratory-analysis"
OUT.mkdir(exist_ok=True)
SEED = 20261022
RNG = np.random.default_rng(SEED)


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save(name, value):
    def convert(x):
        if isinstance(x, np.ndarray):
            return x.tolist()
        if isinstance(x, np.generic):
            return x.item()
        raise TypeError(type(x).__name__)
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, default=convert, allow_nan=False) + "\n", encoding="utf-8")


def csvwrite(name, rows):
    if not rows:
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list, tuple)) else v for k, v in row.items()})


def norm(x):
    return re.sub(r"[^a-z0-9]", "", x.lower())


def recover_dates(records):
    """Use saved matched asset metadata only; no fuzzy title lookup or lore dates.

    A representative franchise cover is NOT a date for all episodes/novels.
    Exact normalized selected-title/work match is required. Conflicts are rejected.
    """
    manifest = read("research/images/manifest.json")["images"]
    ol, tv, steam, kitsu = defaultdict(list), {}, {}, {}
    for p in (ROOT / "research/images/cache").glob("*.json"):
        try:
            z = json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if isinstance(z, dict):
            for doc in z.get("docs", []):
                if isinstance(doc, dict) and doc.get("key") and doc.get("first_publish_year"):
                    ol[doc["key"]].append((doc["first_publish_year"], p.relative_to(ROOT).as_posix(), doc.get("title")))
            for key, value in z.items():
                if isinstance(value, dict) and value.get("success") and isinstance(value.get("data"), dict):
                    d = value["data"]
                    if d.get("release_date", {}).get("date"):
                        steam[key] = (d["release_date"]["date"], p.relative_to(ROOT).as_posix())
            for d in z.get("data", []) if isinstance(z.get("data"), list) else []:
                if isinstance(d, dict) and d.get("type") == "anime":
                    a = d.get("attributes", {})
                    if a.get("startDate"):
                        kitsu[str(d.get("id"))] = (a["startDate"], p.relative_to(ROOT).as_posix())
            if z.get("premiered") and z.get("url"):
                tv[z["url"].rstrip("/")] = (z["premiered"], p.relative_to(ROOT).as_posix(), z.get("name"))
        elif isinstance(z, list):
            for d in z:
                if isinstance(d, dict):
                    d = d.get("show", d)
                    if d.get("premiered") and d.get("url"):
                        tv[d["url"].rstrip("/")] = (d["premiered"], p.relative_to(ROOT).as_posix(), d.get("name"))
    candidates, rejected = defaultdict(list), []
    def intro_date(desc):
        pats = [
            r"\b(?:originally|first)\s+serialized\b[^.]{0,100}?\b((?:18|19|20)\d{2})\b",
            r"\bis\s+(?:a|an)\s+((?:18|19|20)\d{2})\b",
            r"\bfirst\s+published\b[^.]{0,110}?\b((?:18|19|20)\d{2})\b",
            r"\b(?:initial publication|originally appeared)\b[^.]{0,100}?\b((?:18|19|20)\d{2})\b",
            r"\bpublished\s+(?:in\s+|on\s+)?(?:[A-Za-z]+\s+\d{1,2},?\s+)?((?:18|19|20)\d{2})\b",
            r"\bfirst\s+(?:aired|released|broadcast)\s+in\s+((?:18|19|20)\d{2})\b",
        ]
        for pat in pats:
            match = re.search(pat, desc[:1300], flags=re.I)
            if match:
                return int(match[1]), match[0]
        return None

    # The image search retained thousands of introductions even if no cover was used.
    # These are much better date evidence than Open Library's sometimes edition-based
    # 'first_publish_year'. Never silently use catalogue years as original dates.
    wiki = read("research/images/wiki-pages.json")
    work_media = defaultdict(set)
    for r in records:
        work_media[r["work"]].update(r["media"])
    ambiguous = set()
    for work, media in work_media.items():
        if media & {"comic","manga","webcomic"}:
            ambiguous.add(work)
        elif media & {"book","short_story","web_fiction","play"} and media & {"movie","tv","anime","cartoon","game"}:
            ambiguous.add(work)
    for work in ambiguous:
        rejected.append(dict(work=work,reason="Multiple adaptation formats under one work label, or comic/manga serialization dates ambiguous"))
    for work, media in work_media.items():
        if work in ambiguous:
            continue
        for page in wiki.values():
            title = page.get("title", "")
            desc = page.get("extract", "")
            if not desc:
                continue
            bare = re.sub(r"\s*\((?:\d{4}\s+)?(?:novel|novella|short story|book|film|TV series|television series|manga|anime|video game|play|comics)\)$", "", title, flags=re.I)
            if norm(work) not in {norm(title),norm(bare)}:
                continue
            opening = desc[:350].lower()
            prose = bool(media & {"book","short_story","web_fiction","play"})
            screen = bool(media & {"movie","tv","anime","cartoon"})
            if prose and not screen and re.search(r"\b(?:film|television|anime|manga|comic|video game)\b", opening.split("based on")[0]):
                continue
            if screen and not prose and re.search(r"\b(?:novel|novella|short story|book)\b", opening.split("based on")[0]):
                continue
            date = intro_date(desc)
            if date:
                year,evidence=date
                candidates[work].append(dict(work=work,year=year,method="wikipedia_saved_exact_title_intro",local_source="research/images/wiki-pages.json#"+title,source_url=page.get("fullurl",page.get("canonicalurl","")),evidence=evidence,asset_id=None))
    for aid, image in manifest.items():
        sel = image.get("selection", {})
        title = sel.get("title", "")
        works = [w for w in image.get("works", []) if norm(w) == norm(title) and w not in ambiguous]
        if not works:
            continue
        values = []
        source = sel.get("source_page", "")
        key = re.search(r"/works/(OL\d+W)", sel.get("catalogue_page", ""))
        if key:
            hits = ol.get("/works/" + key[1], [])
            years = {int(v[0]) for v in hits}
            if len(years) == 1:
                yr, cache, _ = hits[0]
                rejected.append(dict(work=title,reason="Open Library first_publish_year may refer to edition/translation; not used as original-publication date without corroboration",year=int(yr),cache=cache))
        if source.rstrip("/") in tv:
            date, cache, _ = tv[source.rstrip("/")]
            values.append((int(date[:4]), "tvmaze_exact_show_premiered", cache, source, date))
        app = re.search(r"store\.steampowered\.com/app/(\d+)", source)
        if app and app[1] in steam:
            date, cache = steam[app[1]]
            # Steam can describe a later port; keep out of publication chronology.
            rejected.append({"work": title, "reason": "Steam platform date may be later port", "date": date, "cache": cache})
        desc = html.unescape(re.sub(r"<[^>]*>", " ", sel.get("description", "")))
        if "wikipedia" in sel.get("provider", ""):
            # Only explicit publication/release language or opening 'is a YEAR'.
            date = intro_date(desc)
            if date:
                year,evidence=date
                values.append((year, "wikipedia_saved_selected_intro", "research/images/manifest.json#" + aid, source, evidence))
        for work in works:
            for year, method, cache, url, evidence in values:
                if 1800 <= year <= 2026:
                    candidates[work].append(dict(work=work, year=year, method=method, local_source=cache, source_url=url, evidence=evidence, asset_id=aid))
    accepted = {}
    for work, values in candidates.items():
        if len({v["year"] for v in values}) == 1:
            accepted[work] = values[0]
        else:
            rejected.append({"work": work, "reason": "conflicting publication dates", "candidates": values})
    csvwrite("publication-dates.csv", list(accepted.values()))
    save("publication-date-rejections.json", rejected)
    return accepted


RAW = read("data/societies.json")["societies"]
N = len(RAW)
assert N == len({r["id"] for r in RAW})
GROUPS, GI = np.unique([r["popularity_assessment"]["subject_id"] for r in RAW], return_inverse=True)
COUNTS = np.bincount(GI)
W = 1 / COUNTS[GI]
U = np.array([r["utopia_score"] for r in RAW])
P = np.array([r["popularity_score"] for r in RAW])
S = -np.array([r["axis"]["guarantees"] for r in RAW])  # + means better security
C = np.array([r["axis"]["control"] for r in RAW])
L = np.array([r["axis"]["nonworking"] for r in RAW])
REG = np.array([r["regime_primary"] for r in RAW])
POST = REG > 0
CODE = np.array([r["post_work_assessment"]["manual_code"] for r in RAW])
MEDIA = sorted({m for r in RAW for m in r["media"]})
MED = {m: np.array([m in r["media"] for r in RAW]) for m in MEDIA}
FAMILY = np.array(["zero" if k == 0 else "elite" if k in (1, 2) else "distributed" if k in (3, 4) else "autonomous" for k in REG])
HAS = np.isin(REG, [1, 3, 5])


def avg(x, w=None):
    return float(np.average(x, weights=w))


def wcorr(x, y, w):
    dx, dy = x - avg(x, w), y - avg(y, w)
    return avg(dx * dy, w) / math.sqrt(avg(dx * dx, w) * avg(dy * dy, w))


def summary(mask):
    ix = np.flatnonzero(mask)
    if not len(ix):
        return {}
    w = W[ix]
    # Equal weight to represented groups *within this subset*, not globally.
    counts = np.bincount(GI[ix], minlength=len(GROUPS))
    local_w = 1 / counts[GI[ix]]
    return dict(n=len(ix), groups=int(np.unique(GI[ix]).size), mean_utopia=avg(U[ix]),
                median_utopia=float(np.median(U[ix])), negative_share=avg(U[ix] < 0),
                strong_dystopia_share=avg(U[ix] <= -.5), strong_utopia_share=avg(U[ix] >= .5),
                mean_popularity=avg(P[ix]), mean_nonworking=avg(L[ix]),
                group_balanced_utopia=avg(U[ix], local_w), group_balanced_negative=avg(U[ix] < 0, local_w),
                group_balanced_strong_dystopia=avg(U[ix] <= -.5, local_w),
                group_balanced_popularity=avg(P[ix], local_w))


def fit(y, X, names, weights, groups, intercept=True):
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    if intercept:
        X = np.column_stack([np.ones(len(y)), X])
        names = ["intercept"] + list(names)
    rank = np.linalg.matrix_rank(X * np.sqrt(weights[:, None]))
    if rank != X.shape[1]:
        raise ValueError(f"Rank deficient {rank}/{X.shape[1]}: {names}")
    bread = np.linalg.pinv(X.T @ (weights[:, None] * X))
    beta = bread @ X.T @ (weights * y)
    resid = y - X @ beta
    _, gi = np.unique(groups, return_inverse=True)
    g = gi.max() + 1
    score = np.zeros((g, X.shape[1]))
    np.add.at(score, gi, X * (weights * resid)[:, None])
    cov = bread @ (score.T @ score) @ bread
    cov *= g / (g - 1) * (len(y) - 1) / (len(y) - X.shape[1])
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    t = np.divide(beta, se, out=np.zeros_like(beta), where=se > 0)
    p = 2 * stats.t.sf(abs(t), df=g - 1)
    q = stats.t.ppf(.975, df=g - 1)
    r2 = 1 - avg(resid**2, weights) / avg((y - avg(y, weights))**2, weights)
    return dict(n=len(y), groups=int(g), rank=int(rank), r2=r2,
                coefficients=[dict(term=n, beta=b, se=s, low=b-q*s, high=b+q*s, p=pv) for n, b, s, pv in zip(names, beta, se, p)],
                _X=X, _beta=beta, _cov=cov, _resid=resid, _names=names)


def public(model):
    return {k: v for k, v in model.items() if not k.startswith("_")}


def contrast(model, terms):
    v = np.array([terms.get(n, 0) for n in model["_names"]])
    b = float(v @ model["_beta"])
    se = float(np.sqrt(v @ model["_cov"] @ v))
    q = stats.t.ppf(.975, model["groups"] - 1)
    return dict(beta=b, se=se, low=b-q*se, high=b+q*se, p=float(2*stats.t.sf(abs(b/se), model["groups"]-1)) if se else 1.)


def bh(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    qs = np.minimum.accumulate((p[order] * len(p) / np.arange(1, len(p)+1))[::-1])[::-1]
    out = np.empty(len(p)); out[order] = np.minimum(qs, 1)
    return out


def group_boot_corr(x, y, mask=None, b=2000):
    if mask is None:
        mask = np.ones(len(x), bool)
    x, y, gi = x[mask], y[mask], GI[mask]
    groups, gi = np.unique(gi, return_inverse=True)
    w = 1 / np.bincount(gi)[gi]
    x, y = stats.rankdata(x), stats.rankdata(y)
    # Weighted pooled midranks; bootstrap holds those ranks fixed.
    point = wcorr(x, y, w)
    out = []
    for _ in range(b):
        mult = RNG.multinomial(len(groups), np.full(len(groups), 1/len(groups)))
        out.append(wcorr(x, y, w * mult[gi]))
    lo, hi = np.quantile(out, [.025, .975])
    return dict(rho=point, low=float(lo), high=float(hi), bootstrap_replicates=b, groups=len(groups), n=len(x), rank_definition="pooled_midrank_then_inverse_group_size_weighting")


def cv_r2(y, X, weights, groups):
    pred = np.zeros(len(y))
    for train, test in GroupKFold(5).split(X, y, groups):
        xtr = np.column_stack([np.ones(len(train)), X[train]])
        xte = np.column_stack([np.ones(len(test)), X[test]])
        b = np.linalg.lstsq(xtr * np.sqrt(weights[train, None]), y[train] * np.sqrt(weights[train]), rcond=None)[0]
        pred[test] = xte @ b
    return 1 - avg((y-pred)**2, weights) / avg((y-avg(y,weights))**2, weights)


def core():
    dates = recover_dates(RAW)
    audit = dict(n=N, groups=len(GROUPS), exact_works=len({r["work"] for r in RAW}),
                 regime_counts=Counter(map(int, REG)), media_counts={m: int(x.sum()) for m, x in MED.items()},
                 utopia_confidence=Counter(r["utopia_assessment"]["confidence"] for r in RAW),
                 popularity_confidence=Counter(r["popularity_assessment"]["confidence"] for r in RAW),
                 dates_works=len(dates), dates_rows=sum(r["work"] in dates for r in RAW),
                 date_method_counts=Counter(v["method"] for v in dates.values()),
                 assessment_confidence={axis: Counter(r["axis_assessment"][axis]["confidence"] for r in RAW) for axis in ["guarantees", "control", "nonworking"]},
                 editorial_interval_median_width={axis: float(np.median([r["axis_assessment"][axis]["interval"][1]-r["axis_assessment"][axis]["interval"][0] for r in RAW])) for axis in ["guarantees", "control", "nonworking"]},
                 supplementary_count=len(read("data/comparisons.json")["comparisons"]))
    save("audit.json", audit)
    summary_rows = []
    for field, masks in [("regime", {str(k): REG == k for k in range(7)}), ("media", MED),
                         ("status", {k: np.array([r["post_work_assessment"]["status"] == k for r in RAW]) for k in ["post_work", "transition", "zero_variant"]}),
                         ("allocation", {k: CODE == k for k in sorted(set(CODE))})]:
        for label, mask in masks.items():
            summary_rows.append(dict(dimension=field, category=label, **summary(mask)))
    csvwrite("group-summaries.csv", summary_rows)
    save("group-summaries.json", summary_rows)
    axes = dict(security=S, control=C, nonworking=L, popularity=P, utopia=U)
    correlations = []
    for i, (a, x) in enumerate(axes.items()):
        for b, y in list(axes.items())[i+1:]:
            correlations.append(dict(x=a, y=b, raw_spearman=float(stats.spearmanr(x, y).statistic), **group_boot_corr(x, y)))
    save("correlations.json", correlations)
    csvwrite("correlations.csv", correlations)
    # Multi-label medium controls; omitted tiny media remain the reference mix.
    media_names = [m for m in MEDIA if MED[m].sum() >= 15]
    mx = np.column_stack([MED[m] for m in media_names]).astype(float)
    base_names = ["security", "control", "control_squared", "nonworking", "post_work", "popularity"]
    base_x = np.column_stack([S, C, C*C, L, POST, P])
    full_x = np.column_stack([base_x, mx])
    full_names = base_names + ["media_"+m for m in media_names]
    full = fit(U, full_x, full_names, W, GI)
    simple = fit(U, base_x, base_names, W, GI)
    rows_model = fit(U, full_x, full_names, np.ones(N), GI)
    models = {"structural_group_balanced": public(simple), "full_group_balanced": public(full), "full_equal_rows": public(rows_model)}
    cv = {"security_only": cv_r2(U, S[:,None], W, GI), "structural": cv_r2(U, base_x, W, GI), "structural_and_media": cv_r2(U, full_x, W, GI)}
    for name, inds in {"security": [0], "control": [1,2], "nonworking": [3], "post_work": [4], "popularity": [5], "media": list(range(6, full_x.shape[1]))}.items():
        keep = [j for j in range(full_x.shape[1]) if j not in inds]
        cv["without_"+name] = cv_r2(U, full_x[:, keep], W, GI)
    save("cross-validation.json", cv)
    # Do not conclude 'no association' from a linear leisure term alone.
    flex_x=np.column_stack([full_x,L*L,L*S,L*C,S*C])
    flex_names=full_names+["nonworking_squared","nonworking_x_security","nonworking_x_control","security_x_control"]
    flex=fit(U,flex_x,flex_names,W,GI)
    models["flexible_nonworking_and_interactions"]=public(flex)
    terms=["nonworking","nonworking_squared","nonworking_x_security","nonworking_x_control"]
    inds=[flex["_names"].index(t) for t in terms]
    bb=flex["_beta"][inds];cc=flex["_cov"][np.ix_(inds,inds)]
    wald=float(bb@np.linalg.pinv(cc)@bb)
    nonlinear=dict(terms=terms,cluster_wald_chi2=wald,df=len(terms),p=float(stats.chi2.sf(wald,len(terms))),cv_r2=cv_r2(U,flex_x,W,GI),linear_full_cv_r2=cv["structural_and_media"],
        cv_security_control_interaction=cv_r2(U,np.column_stack([full_x,S*C]),W,GI),
        cv_no_nonworking_terms=cv_r2(U,np.column_stack([full_x[:,[i for i,n in enumerate(full_names) if n!="nonworking"]],S*C]),W,GI))
    save("nonworking-nonlinearity.json",nonlinear)
    # Post-work-only factorial model: 2 guarantee states x 3 control families.
    ix = np.flatnonzero(POST)
    d = (FAMILY == "distributed").astype(float)
    a = (FAMILY == "autonomous").astype(float)
    h = HAS.astype(float)
    factorial_x = np.column_stack([h,d,a,h*d,h*a,L,P,mx])
    factorial_names = ["guarantees", "distributed", "autonomous", "guarantees_x_distributed", "guarantees_x_autonomous", "nonworking", "popularity"] + ["media_"+m for m in media_names]
    # Equal groups within post-work subset.
    wp = 1 / np.bincount(GI[ix], minlength=len(GROUPS))[GI[ix]]
    fm = fit(U[ix], factorial_x[ix], factorial_names, wp, GI[ix])
    models["post_work_factorial"] = public(fm)
    contrasts = {}
    for family, terms in [("elite", {"guarantees":1}), ("distributed", {"guarantees":1,"guarantees_x_distributed":1}), ("autonomous", {"guarantees":1,"guarantees_x_autonomous":1})]:
        contrasts["guarantee_effect_"+family] = contrast(fm, terms)
    contrasts["autonomous_vs_elite_with_guarantees"] = contrast(fm, {"autonomous":1,"guarantees_x_autonomous":1})
    contrasts["autonomous_vs_elite_without_guarantees"] = contrast(fm, {"autonomous":1})
    contrasts["distributed_vs_elite_with_guarantees"] = contrast(fm, {"distributed":1,"guarantees_x_distributed":1})
    contrasts["distributed_vs_autonomous_with_guarantees"] = contrast(fm, {"distributed":1,"guarantees_x_distributed":1,"autonomous":-1,"guarantees_x_autonomous":-1})
    save("factorial-contrasts.json", contrasts)
    # Media contrasts with and without economic controls. Multi-label, same weights.
    medium_only = fit(U, mx, ["media_"+m for m in media_names], W, GI)
    models["medium_only"] = public(medium_only)
    media_contrasts = []
    for m in media_names:
        if m != "book":
            media_contrasts.append(dict(medium=m, reference="book", unadjusted=contrast(medium_only,{"media_"+m:1,"media_book":-1}), adjusted=contrast(full,{"media_"+m:1,"media_book":-1})))
    save("media-contrasts.json", media_contrasts)
    # Strict nonoverlapping anime vs prose; a group may contribute to both categories.
    strict_anime = MED["anime"] & ~MED["book"] & ~MED["short_story"]
    strict_prose = (MED["book"] | MED["short_story"]) & ~MED["anime"] & ~MED["manga"] & ~MED["movie"] & ~MED["tv"] & ~MED["game"]
    strict = strict_anime | strict_prose
    si = np.flatnonzero(strict)
    swi = 1 / np.bincount(GI[si], minlength=len(GROUPS))[GI[si]]
    sx = np.column_stack([strict_anime.astype(float), S,C,C*C,L,POST,P])
    sm = fit(U[si], sx[si], ["anime_vs_prose","security","control","control_squared","nonworking","post_work","popularity"], swi, GI[si])
    models["strict_anime_vs_prose"] = public(sm)
    save("strict-media-summary.json", {"anime": summary(strict_anime), "prose": summary(strict_prose)})
    # Within-group differences remove all group-constant popularity effects.
    wx = np.column_stack([S,C,C*C,L,POST])
    wy = U.copy()
    for g in range(len(GROUPS)):
        sel = GI == g
        wy[sel] -= wy[sel].mean()
        wx[sel] -= wx[sel].mean(axis=0)
    active = COUNTS[GI] > 1
    wm = fit(wy[active], wx[active], ["security","control","control_squared","nonworking","post_work"], W[active], GI[active], intercept=False)
    models["within_group_fixed_effects"] = public(wm)
    # Nonworking: simple association vs multivariate association.
    models["nonworking_only"] = public(fit(U,L[:,None],["nonworking"],W,GI))
    # Scope sensitivity: pre-existing conservative resident-scope audit, projections/proxies excluded.
    resident_ids = {r["id"] for r in read("research/scope-audit.json")["records"]}
    mask_sets = {
        "resident_scope": np.array([r["id"] in resident_ids for r in RAW]),
        "no_population_proxy": np.array([not r["scope"].get("human_population_proxy",False) for r in RAW]),
        "no_projection_or_configurable": np.array([not r["scope"].get("player_configurable") and not r["scope"].get("projection_status") for r in RAW]),
        "exclude_largest_10_groups": ~np.isin(GI,np.argsort(COUNTS)[-10:]),
        "post_work_only_continuous": POST,
    }
    sensitivity = []
    nonlinear_sensitivity=[]
    for label, mask in mask_sets.items():
        xi = full_x[mask]
        names = full_names.copy()
        # Drop constant post_work in the post-work-only sample.
        keep = np.std(xi,axis=0)>1e-10
        xi=xi[:,keep]; names=[n for n,k in zip(names,keep) if k]
        wi=1/np.bincount(GI[mask],minlength=len(GROUPS))[GI[mask]]
        model=fit(U[mask],xi,names,wi,GI[mask])
        models[label]=public(model)
        sensitivity.append(dict(sample=label,n=int(mask.sum()),groups=model["groups"],r2=model["r2"],coefficients={v["term"]:v["beta"] for v in model["coefficients"]}))
        fxi=flex_x[mask];fkeep=np.std(fxi,axis=0)>1e-10
        fnames=[n for n,k in zip(flex_names,fkeep) if k]
        flex_sub=fit(U[mask],fxi[:,fkeep],fnames,wi,GI[mask])
        nonlinear_sensitivity.append(dict(sample=label,n=int(mask.sum()),coefficients={v["term"]:v["beta"] for v in flex_sub["coefficients"] if v["term"].startswith("nonworking") or v["term"]=="security_x_control"},
             delta_nonworking_30_to_80_at_security_06_control_0=contrast(flex_sub,{"nonworking":.5,"nonworking_squared":.55,"nonworking_x_security":.3})))
    save("sensitivity.json",sensitivity)
    save("nonlinear-sensitivity.json",nonlinear_sensitivity)
    # Editorial coordinate interval scenarios: neither statistical uncertainty nor CI.
    # Vary every coordinate independently and uniformly within its saved interval.
    intervals = {axis: np.array([r["axis_assessment"][axis]["interval"] for r in RAW]) for axis in ["guarantees","control","nonworking"]}
    scenario_betas = []
    for _ in range(500):
        sv,cvv,lv = [-RNG.uniform(*intervals["guarantees"].T), RNG.uniform(*intervals["control"].T), RNG.uniform(*intervals["nonworking"].T)]
        xx=np.column_stack([np.ones(N),sv,cvv,cvv*cvv,lv,POST,P,mx])
        b=np.linalg.lstsq(xx*np.sqrt(W[:,None]),U*np.sqrt(W),rcond=None)[0]
        scenario_betas.append(b)
    scenario_betas=np.array(scenario_betas)
    scenarios={name:dict(median=float(np.median(scenario_betas[:,j])),low=float(np.quantile(scenario_betas[:,j],.025)),high=float(np.quantile(scenario_betas[:,j],.975)),positive_share=float(np.mean(scenario_betas[:,j]>0))) for j,name in enumerate(["intercept"]+full_names)}
    save("editorial-interval-scenarios.json",dict(replicates=500,assumption="independent uniform coordinates inside editorial intervals; U and popularity held fixed; not a posterior or confidence interval",coefficients=scenarios))
    save("models.json", models)
    # Group-level recognition: one observation per group. No row pseudo-replication.
    group_rows=[]
    for g, gid in enumerate(GROUPS):
        mask=GI==g; rr=[r for r,k in zip(RAW,mask) if k]
        assert np.ptp(P[mask]) == 0
        row=dict(group_id=gid,subject=rr[0]["popularity_assessment"]["subject"],n=int(mask.sum()),popularity=float(P[mask][0]),
                 mean_utopia=avg(U[mask]),mean_abs_utopia=avg(abs(U[mask])),min_utopia=float(U[mask].min()),max_utopia=float(U[mask].max()),
                 utopia_range=float(np.ptp(U[mask])),strong_dystopia_share=avg(U[mask]<=-.5),strong_utopia_share=avg(U[mask]>=.5),negative_share=avg(U[mask]<0),
                 mean_security=avg(S[mask]),mean_control=avg(C[mask]),mean_nonworking=avg(L[mask]),mean_post_work=avg(POST[mask]))
        for m in media_names:row["media_"+m]=float(any(m in r["media"] for r in rr))
        group_rows.append(row)
    csvwrite("recognition-groups.csv",group_rows)
    gy=np.array([r["popularity"] for r in group_rows])
    ga=np.array([r["mean_abs_utopia"] for r in group_rows])
    gu=np.array([r["mean_utopia"] for r in group_rows])
    gmx=np.array([[r["media_"+m] for m in media_names] for r in group_rows])
    gm=fit(gy,np.column_stack([gu,ga,gmx]),["mean_utopia","mean_abs_utopia"]+["media_"+m for m in media_names],np.ones(len(GROUPS)),np.arange(len(GROUPS)))
    gp=dict(popularity_vs_mean_utopia=float(stats.spearmanr(gy,gu).statistic),popularity_vs_mean_absolute_utopia=float(stats.spearmanr(gy,ga).statistic),model=public(gm),
            multi_society_groups=sum(r["n"]>1 for r in group_rows),both_positive_and_negative=sum(r["min_utopia"]<0<r["max_utopia"] for r in group_rows),
            both_strong_extremes=sum(r["min_utopia"]<=-.5 and r["max_utopia"]>=.5 for r in group_rows))
    save("recognition-analysis.json",gp)
    # Compare media composition; these are associations, not a mediation proof.
    composition=[]
    for m in media_names:
        mask=MED[m]
        for k in range(7):composition.append(dict(medium=m,regime=k,n=int(np.sum(mask&(REG==k))),share=float(np.mean(REG[mask]==k))))
    csvwrite("media-regime-composition.csv",composition)
    # Principal components of the three institutions; supplementary outcomes are excluded.
    structural=np.column_stack([S,C,L]);mean=np.average(structural,axis=0,weights=W)
    sd=np.sqrt(np.average((structural-mean)**2,axis=0,weights=W));z=(structural-mean)/sd
    cov=z.T@(W[:,None]*z)/W.sum();eig,vec=np.linalg.eigh(cov);order=np.argsort(eig)[::-1];eig,vec=eig[order],vec[:,order]
    for j in range(3):
        if vec[np.argmax(abs(vec[:,j])),j]<0:vec[:,j]*=-1
    pcs=z@vec
    pca=dict(variables=["security","control","nonworking"],eigenvalues=eig,explained_variance=eig/eig.sum(),eigenvectors=vec,
             loadings=vec*np.sqrt(eig),utopia_supplementary_correlations=[wcorr(pcs[:,j],U,W) for j in range(3)],
             popularity_supplementary_correlations=[wcorr(pcs[:,j],P,W) for j in range(3)],group_balanced=True)
    save("pca.json",pca)
    # Literal exploratory factor analysis: five variables including U and P.
    # Keep one averaged observation per group to eliminate row pseudo-replication.
    fa_data=np.array([[avg(S[GI==g]),avg(C[GI==g]),avg(L[GI==g]),avg(U[GI==g]),avg(P[GI==g])] for g in range(len(GROUPS))])
    faz=(fa_data-fa_data.mean(0))/fa_data.std(0)
    corr=np.corrcoef(faz,rowvar=False);inv=np.linalg.inv(corr);partial=-inv/np.sqrt(np.outer(np.diag(inv),np.diag(inv)));np.fill_diagonal(partial,0)
    cc=corr.copy();np.fill_diagonal(cc,0);kmo=float(np.sum(cc**2)/(np.sum(cc**2)+np.sum(partial**2)))
    fa_results={"variables":["security","control","nonworking","utopia","popularity"],"n_groups":len(GROUPS),"KMO":kmo,"models":[]}
    for k in [1,2]:
        fa=FactorAnalysis(n_components=k,rotation="varimax" if k==2 else None,random_state=SEED,max_iter=2000).fit(faz)
        load=fa.components_.T
        for j in range(k):
            if load[np.argmax(abs(load[:,j])),j]<0:load[:,j]*=-1
        reproduced=load@load.T+np.diag(fa.noise_variance_)
        residual=np.cov(faz,rowvar=False,bias=True)-reproduced
        mask=~np.eye(5,dtype=bool)
        fa_results["models"].append(dict(factors=k,loadings=load,uniqueness=fa.noise_variance_,log_likelihood=float(fa.score(faz)*len(faz)),off_diagonal_rms=float(np.sqrt(np.mean(residual[mask]**2)))))
    save("factor-analysis.json",fa_results)
    # Chronology on the strict, saved-date subset; group-balanced, medium-adjusted.
    dated=np.array([r["work"] in dates for r in RAW]);di=np.flatnonzero(dated)
    years=np.array([dates[r["work"]]["year"] if r["work"] in dates else 0 for r in RAW])
    era_rows=[]
    for label,low,high in [("before_1950",1800,1949),("1950_1979",1950,1979),("1980_1999",1980,1999),("2000_2009",2000,2009),("2010_2026",2010,2026)]:
        mask=dated&(years>=low)&(years<=high)
        era_rows.append(dict(era=label,**summary(mask)))
    chronology=dict(n_dated=len(di),groups=len(np.unique(GI[di])),works=len(dates),eras=era_rows,
                    missing_summary=summary(~dated),dated_summary=summary(dated),models={})
    if len(di)>50:
        t=(years[di]-2000)/10
        wi=1/np.bincount(GI[di],minlength=len(GROUPS))[GI[di]]
        for outcome,y in [("utopia",U[di]),("extremity",abs(U[di])),("strong_dystopia",(U[di]<=-.5).astype(float)),("strong_utopia",(U[di]>=.5).astype(float))]:
            for adjustment,xx,names in [("unadjusted",t[:,None],["decade"]),("medium_adjusted",np.column_stack([t,mx[di]]),["decade"]+["media_"+m for m in media_names])]:
                keep=np.std(xx,axis=0)>1e-10
                xx=xx[:,keep];names=[n for n,k in zip(names,keep) if k]
                model=fit(y,xx,names,wi,GI[di])
                chronology["models"][outcome+"_"+adjustment]=public(model)
    save("chronology.json",chronology)
    # Multiple-comparison screen: related tests are descriptive, adjusted together.
    screen=[]
    for name,model in [("full",full),("factorial",fm),("popularity",gm),("flexible",flex)]:
        for c in model["coefficients"]:
            if c["term"]!="intercept":screen.append(dict(family=name,**c))
    for name,v in contrasts.items():screen.append(dict(family="factorial_contrast",term=name,**v))
    for c in media_contrasts:screen.append(dict(family="media_vs_book",term=c["medium"],**c["adjusted"]))
    for name,model in chronology["models"].items():
        term=next(c for c in model["coefficients"] if c["term"]=="decade");screen.append(dict(term,family="chronology",term=name))
    screen.append(dict(family="flexible_omnibus",term="all_nonworking_terms",p=nonlinear["p"]))
    for c,q in zip(screen,bh([v["p"] for v in screen])):c["q_BH"]=q
    csvwrite("exploratory-tests.csv",screen)
    save("exploratory-tests.json",screen)
    # Cases deserving reading, selected mechanically and with explicit IDs.
    case_rows=[]
    residual=full["_resid"]
    for category,ixs in [("worse_than_model",np.argsort(residual)[:15]),("better_than_model",np.argsort(residual)[-15:][::-1]),
                         ("secure_but_dystopian",np.flatnonzero((S>=.5)&(U<=-.5))), ("insecure_but_positive",np.flatnonzero((S<=-.3)&(U>=.2)))]:
        for i in ixs:
            r=RAW[i]
            case_rows.append(dict(category=category,id=r["id"],name=r["name"],work=r["work"],regime=int(REG[i]),utopia=float(U[i]),security=float(S[i]),control=float(C[i]),nonworking=float(L[i]),residual=float(residual[i]),basis=r["utopia_assessment"]["basis"],source_ids=r["source_ids"]))
    csvwrite("interesting-cases.csv",case_rows);save("interesting-cases.json",case_rows)
    rows=[]
    for i,r in enumerate(RAW):
        rows.append(dict(id=r["id"],name=r["name"],work=r["work"],group=r["popularity_assessment"]["subject_id"],media=r["media"],regime=int(REG[i]),control_family=FAMILY[i],security=float(S[i]),control=float(C[i]),nonworking=float(L[i]),utopia=float(U[i]),popularity=float(P[i]),group_weight=float(W[i]),publication_year=int(years[i]) if dated[i] else None))
    csvwrite("analysis-records.csv",rows)
    save("provenance.json",dict(seed=SEED,input_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ["data/societies.json","data/taxonomy.json","data/comparisons.json","research/images/manifest.json","research/scope-audit.json"]},method="Exploratory observational analysis of editorial ratings; WLS with inverse group size weights and group-clustered CR1 standard errors; two-sided t references; BH across reported exploratory regression tests; 5-fold GroupKFold prediction.",date="2026-10-22",numpy=np.__version__))
    print(json.dumps(dict(n=N,groups=len(GROUPS),dated_rows=len(di),dated_works=len(dates),full_model_r2=full["r2"],cv_r2=cv["structural_and_media"],fa_KMO=kmo),ensure_ascii=False,indent=2))


if __name__=="__main__":
    if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
    core()
