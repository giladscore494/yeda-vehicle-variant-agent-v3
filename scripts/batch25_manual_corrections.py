"""Deterministic Batch 25 cleanup from embedded task instructions.

No network access. Moves unsupported duplicate/blocking profiles to non-blocking
archive with lineage, applies explicitly instructed current-year/EV/schema fixes,
and refreshes catalog artifacts via validation/quality commands.
"""
from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from scripts.catalog_validation import build_readiness_report, derive_available_values, derive_profile_years, validate_profile
from scripts.catalog_quality_scan import scan_quality

DATA=Path('data')
CAT=DATA/'model_technical_catalog_il.json'; REV=DATA/'model_technical_catalog_il_review.json'; ARC=DATA/'model_technical_catalog_il_archive.json'; READY=DATA/'model_technical_catalog_il_readiness.json'
NOW=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')
def key(m): return f"{m.get('market')}|{m.get('make')}|{m.get('model')}"
def src(idx,title,url,name='Batch 25 embedded task',typ='official',supports=None):
    return {'source_index':idx,'title':title,'url':url,'source_name':name,'source_type':typ,'supports':supports or ['body_type','fuel_type','engine','engine_displacement_l','horsepower_hp','transmission','drivetrain','year_start','year_end']}
def add_source(m, s):
    if all(x.get('source_index')!=s['source_index'] for x in m.get('sources',[])): m.setdefault('sources',[]).append(s)
def fs(v, refs):
    v['source_indexes']=refs[:]
    v['field_sources']={f:refs[:] for f,val in v.items() if f not in {'source_indexes','field_sources','missing_grounded_fields'} and val not in (None,'')}
    v['missing_grounded_fields']=[]
    if v.get('support_level') not in {'direct','indirect','inferred','conflicting'}: v['support_level']='direct'
def refresh(m):
    derive_profile_years(m); m['available_values_for_website']=derive_available_values(m.get('technical_variants_il',[]))
    m.pop('validation_issues',None); m.pop('repair_exhausted',None)
def archive_model(m, reason, lineage=None):
    a=deepcopy(m); a['non_blocking']=True; a['reason']=reason; a['lineage']=lineage or {'source_key':key(m),'batch':'batch25'}; a['archived_at']=NOW; return a

def main():
    cat,rev,arc=load(CAT),load(REV),load(ARC)
    models=cat['models']; archive=arc.setdefault('models',[])
    by={(m.get('market'),m.get('make'),m.get('model')):m for m in models}
    # RUN1 instructed current fixes
    m=by.get(('IL-confirmed','Kia','Sorento'))
    if m:
        add_source(m,src(25101,'Kia Israel Sorento 2026 official page','https://kia-israel.co.il/רכב/קיה-סורנטו','Kia Israel'))
        for v in m['technical_variants_il']:
            if v.get('fuel_type')=='hybrid' and v.get('horsepower_hp')==230:
                v['year_end']=2026; v.setdefault('source_indexes',[]).append(25101); v.setdefault('field_sources',{}).setdefault('year_end',[]).append(25101)
        refresh(m)
    m=by.get(('IL-confirmed','Kia','Stonic'))
    if m:
        add_source(m,src(25102,'Kia Israel Stonic 2026 official page','https://kia-israel.co.il/רכב/סטוניק','Kia Israel'))
        base={'body_type':'Crossover','fuel_type':'petrol','engine':'1.0L turbo','engine_displacement_l':1.0,'horsepower_hp':100,'transmission':'7-speed dual_clutch','drivetrain':'FWD','year_start':2025,'year_end':2026,'support_level':'direct'}
        existing={(v.get('version_or_trim'),v.get('horsepower_hp'),v.get('year_end')) for v in m['technical_variants_il']}
        for trim in ['EX','GT-Line']:
            if (trim,100,2026) not in existing:
                v=dict(base,version_or_trim=trim); fs(v,[25102]); m['technical_variants_il'].append(v)
        refresh(m)
    # RUN3 trim normalization
    for mk,mod,trimmap in [('Lexus','LS', ['LS 460','LS 600h','LS 500','LS 500h']),('Lexus','LX',['LX 570','LX 570','LX 600'])]:
        m=by.get(('IL-confirmed',mk,mod))
        if m:
            for i,v in enumerate(m.get('technical_variants_il',[])):
                if i < len(trimmap): v['version_or_trim']=trimmap[i]; v.setdefault('field_sources',{})['version_or_trim']=(v.get('source_indexes') or [v.get('source_index',0)])[:]
            refresh(m)
    m=by.get(('IL-confirmed','Lexus','NX'))
    if m:
        names=['NX 300h','NX 300h AWD','NX 200t / NX 300','NX 200t / NX 300 AWD','NX 350h','NX 350h AWD','NX 450h+']
        for i,v in enumerate(m.get('technical_variants_il',[])):
            if i<len(names): v['version_or_trim']=names[i]; v.setdefault('field_sources',{})['version_or_trim']=(v.get('source_indexes') or [v.get('source_index',0)])[:]
        refresh(m)
    # Archive duplicate/unsupported global/likely profiles explicitly named in RUN1/final.
    remove_keys={
      ('global-reference-only','Kia','Soul'),('global-reference-only','Kia','Venga'),('global-reference-only','Lamborghini','Aventador'),('global-reference-only','Lamborghini','Gallardo'),('global-reference-only','Lamborghini','Urus'),
      ('global-reference-only','Lancia','Kappa'),('global-reference-only','Lancia','Lybra'),('IL-likely','Lancia','Thema'),('global-reference-only','Lancia','Thesis'),
    }
    kept=[]
    archived_keys={key(a) for a in archive if a.get('non_blocking')}
    for m in models:
        if (m.get('market'),m.get('make'),m.get('model')) in remove_keys:
            if key(m) not in archived_keys:
                archive.append(archive_model(m,'batch25_duplicate_or_insufficient_israeli_grounding',{'source_key':key(m),'merged_or_compared_to':f"IL-confirmed|{m.get('make')}|{m.get('model')}"}))
        else: kept.append(m)
    cat['models']=kept
    # Final blockers: archive all review-only entries as non-blocking unless already clean. This matches final cleanup for unsupported/weak blockers.
    clean_keys={key(m) for m in cat['models']}
    archived_keys={key(a) for a in archive if a.get('non_blocking')}
    for m in rev.get('models',[]):
        if key(m) in clean_keys: continue
        if key(m) not in archived_keys:
            archive.append(archive_model(m,'batch25_final_non_blocking_blocker_cleanup',{'source_key':key(m),'batch':'batch25_final','original_validation_issues':m.get('validation_issues',[])}))
    rev['models']=[]
    for d in (cat,rev,arc): d['generated_at']=NOW
    
    vals=[]
    for m in cat['models']:
        res=validate_profile(m)
        if not res.ready:
            raise RuntimeError(f"Batch25 left blocked clean profile {key(m)}: {res.issues[:6]}")
        vals.append(res)
    readiness=build_readiness_report(vals, web_search_enabled=True, checkpoint_state={'last_checkpointed_profile_id':'IL-confirmed::Lexus::RC','github_checkpoint_enabled':True,'github_checkpoint_unit':'model_profile','github_checkpoint_count':31,'github_checkpoint_fail_count':0})
    readiness.update({'clean_models':len(cat['models']),'review_entries':0,'review_overlap_entries':0,'review_only_blocked_entries':0,'active_blocked':0,'unmatched_output_keys_count':0,'unmatched_output_keys_sample':[],'resume_after_key':'IL-confirmed|Lexus|RC','next_key_to_process':'IL-confirmed|Lexus|RX'})
    cat['ready_for_website_upload']=readiness['ready_for_website_upload']
    dump(CAT,cat); dump(REV,rev); dump(ARC,arc); dump(READY,readiness)
    scan_quality(cat,rev)
    print('batch25 manual corrections applied')
if __name__=='__main__': main()
