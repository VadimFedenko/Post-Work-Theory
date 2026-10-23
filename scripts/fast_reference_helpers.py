"""Serialization for the faster reference pass; all substantive claims remain supplied by each batch."""
from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

def cited_sources(prefix, rows):
    return [source(prefix+key,title,author,url,kind,'Bounded accessible or explicitly indexed reference passage',claim,limits)
            for key,title,author,url,kind,claim,limits in rows]

def scoped_record(cid, rid, name, work, society, media, continuity, period, population,
                  exclusions, description, axes, bounds, bases, refs, regime, proxy=False,
                  zero=False, locator='Bounded named-society economic and story sections', alternatives=None):
    return record(rid,cid,name,work,society,media,scope(continuity,period,population,exclusions,proxy=proxy),description,
                  dict(zip(['guarantees','control','nonworking'],axes)),
                  {k:assessment(v,b,'low',why,refs) for k,v,b,why in zip(['guarantees','control','nonworking'],axes,bounds,bases)},
                  0 if zero else regime,refs,[evidence(bases[0],refs,locator,'labeled_reference_and_interpretation')],
                  ['Reference-led provisional assessment; source limitations and editorial uncertainty remain explicit.',bases[1],bases[2]],
                  record_type='zero_variant' if zero else 'post_work',analogy=[regime] if zero else None,alternatives=alternatives)

def short_disposition(cid, status, reason, refs, analysis, **extra):
    return decision(cid,status,reason,refs,analysis=analysis,
                    follow_up='Keep the disposition and continue the queue; reopen only if a clear short reference becomes readily available.',**extra)
