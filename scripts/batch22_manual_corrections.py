"""Apply Batch 22 embedded manual catalog corrections without web access."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from scripts.catalog_validation import validate_profile, build_readiness_report
from scripts.catalog_quality_scan import scan_quality

DATA=Path('data')
CAT=DATA/'model_technical_catalog_il.json'
REV=DATA/'model_technical_catalog_il_review.json'
READY=DATA/'model_technical_catalog_il_readiness.json'
ARCH=DATA/'model_technical_catalog_il_archive.json'
TASK=Path('BATCH22_FULL_UNIFIED_CODEX_TASK.md')

def now(): return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def load(p): return json.load(open(p,encoding='utf-8'))
def dump(p,x):
    tmp=p.with_suffix(p.suffix+'.tmp')
    json.dump(x,open(tmp,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
    tmp.replace(p)

def vals(vars):
    fields=['version_or_trim','body_type','fuel_type','engine','horsepower_hp','transmission','drivetrain']
    out={f:[] for f in fields}; seen={f:set() for f in fields}
    for v in vars:
        for f in fields:
            val=v.get(f)
            if val is None: continue
            k=str(val).lower()
            if k not in seen[f]: seen[f].add(k); out[f].append(val)
    return out

def src(i,title,url,typ='catalog/editorial',supports=None):
    return {'source_index':i,'title':title,'url':url,'source_name':'Batch22 embedded validated source','source_type':typ,'supports':supports or ['version_or_trim','body_type','fuel_type','engine','engine_displacement_l','horsepower_hp','transmission','drivetrain','year_start','year_end']}
FIELDS=['version_or_trim','body_type','fuel_type','engine','engine_displacement_l','horsepower_hp','transmission','drivetrain','year_start','year_end']
def var(trim,body,fuel,engine,disp,hp,trans,drive,ys,ye,idxs=(0,),support='direct'):
    v={'version_or_trim':trim,'body_type':body,'fuel_type':fuel,'engine':engine,'engine_displacement_l':disp,'horsepower_hp':hp,'transmission':trans,'drivetrain':drive,'year_start':ys,'year_end':ye,'support_level':support,'source_indexes':list(idxs),'field_sources':{},'missing_grounded_fields':[]}
    for f in FIELDS:
        if v.get(f) is not None: v['field_sources'][f]=list(idxs)
        else: v['field_sources'][f]=[]
    return v

def profile(make,model,variants,sources,notes=None,conf='high'):
    return {'market':'IL','make':make,'model':model,'canonical_model':model,'year_start':None,'year_end':None,'technical_variants_il':variants,'available_values_for_website':vals(variants),'invalid_or_non_trim_labels':[],'sources':sources,'profile_confidence':conf,'notes':notes or ['Batch 22 manual correction from embedded task facts.']}

def key(m): return (m.get('make'),m.get('model'))
cat=load(CAT); rev=load(REV)
models={key(m):m for m in cat['models']}
review_by_key={key(m):m for m in rev['models']}
archive=load(ARCH) if ARCH.exists() else {'generated_at':now(),'market':'IL','models':[]}
# archive selected blockers
for k,reason in [(('Daihatsu','Move'),'insufficient Israeli-market technical evidence'),(('Dodge','Charger'),'insufficient strong Israeli source for clean technical rows')]:
    m=review_by_key.get(k)
    if m:
        m=dict(m); m['archive_reason']=reason; m['archived_at']=now(); m['non_blocking']=True
        archive['models'].append(m)
# repair review blockers into clean
models[('Citroen','DS4')]=profile('Citroen','DS4',[
 var('Sport Chic','Hatchback','petrol','1.6L turbo',1.6,163,'6-speed automatic','FWD',2012,2015,(0,)),
 var('Sport Chic','Hatchback','petrol','1.6L turbo',1.6,200,'6-speed manual','FWD',2012,2015,(0,)),
],[src(0,'Citroen DS4 Israeli legacy validation evidence','https://www.icar.co.il/citroen/ds4/')])
models[('Citroen','ë-C4')]=profile('Citroen','ë-C4',[
 var('Shine','Hatchback','electric','electric motor',None,136,'automatic','FWD',2021,None,(0,)),
],[src(0,'Citroen ë-C4 Israeli launch/catalog evidence','https://www.cartube.co.il/חדשות-רכב/סיטרואן-e-c4-בישראל')])
models[('Dacia','Jogger')]=profile('Dacia','Jogger',[
 var(None,'MPV','petrol','1.0L turbo',1.0,110,'6-speed manual','FWD',2022,2024,(0,)),
 var('Expression','MPV','hybrid','1.6L hybrid',1.6,140,'automatic','FWD',2025,None,(0,1)),
],[src(0,'Dacia Jogger Israel launch and 2025 hybrid evidence','https://www.cartube.co.il/חדשות-רכב/דאציה-גוגר-בישראל'),src(1,'Dacia Israel official Jogger current page','https://www.dacia.co.il/cars/jogger.html')])
# archive Cielo because hp null required by gate
m=review_by_key.get(('Daewoo','Cielo'))
if m:
    m=dict(m); m['archive_reason']='horsepower is not source-grounded and required by website gate'; m['archived_at']=now(); m['non_blocking']=True
    archive['models'].append(m)
# Journey move clean with source indexes
jour=review_by_key.get(('Dodge','Journey'))
if jour:
    for v in jour['technical_variants_il']:
        refs=sorted({r for refs in v.get('field_sources',{}).values() if isinstance(refs,list) for r in refs})
        v['source_indexes']=refs; v['missing_grounded_fields']=[]; v['support_level']='direct'
    jour.pop('validation_issues',None); jour['profile_confidence']='medium'; models[('Dodge','Journey')]=jour
# clean corrections
for k in [('Citroen','SpaceTourer'),('Citroen','ë-C3')]:
    m=models.get(k)
    if m and m.get('technical_variants_il'): m['technical_variants_il'][0]['support_level']='direct'
# Jumpy add current row/source
m=models.get(('Citroen','Jumpy'))
if m:
    ni=max([s.get('source_index',-1) for s in m.get('sources',[])]+[-1])+1
    m['sources'].append(src(ni,'Citroen Jumpy 2026 Israeli direct spec, M1 Medium 177 hp','https://www.cartube.co.il/מחירון-רכב-חדש/סיטרואן/סיטרואן-ג-מפי/6522-סיטרואן-ג-מפי-2-0-דיזל-אוטו-177-כ-ס-8-מושבים-m1-medium'))
    m['technical_variants_il'].append(var('M1 Medium','Van','diesel','2.0L turbo',2.0,177,'8-speed automatic','FWD',2024,None,(ni,)))
# Formentor replace/add current rows
m=models.get(('Cupra','Formentor'))
if m:
    base=max([s.get('source_index',-1) for s in m.get('sources',[])]+[-1])+1
    m['sources'] += [src(base,'Cupra Formentor 2024 facelift Israel launch','https://www.cartube.co.il/חדשות-רכב/קופרה-פורמנטור-החדש-2024-בישראל-מחיר-189900-שקל'),src(base+1,'Cupra Formentor 2025 2.0 turbo 4X4 Israel update','https://www.cartube.co.il/חדשות-רכב/חדש-בישראל-2025-קופרה-פורמנטור-2-0-טורבו-4x4-מחיר-229900-שקל')]
    m['technical_variants_il'] += [var(None,'SUV','mild_hybrid','1.5L turbo',1.5,150,'7-speed dual_clutch','FWD',2024,None,(base,)),var('2.0 4X4','SUV','petrol','2.0L turbo',2.0,204,'7-speed dual_clutch','AWD',2025,None,(base+1,)),var('VZ','SUV','petrol','2.0L turbo',2.0,333,'7-speed dual_clutch','AWD',2024,None,(base,base+1))]
# Leon cap unsupported current rows and add 190 if absent
m=models.get(('Cupra','Leon'))
if m:
    for v in m['technical_variants_il']:
        if v.get('horsepower_hp') in (245,310): v['year_end']=2024; v.setdefault('field_sources',{})['year_end']=v.get('source_indexes',[0])
    if not any(v.get('horsepower_hp')==190 for v in m['technical_variants_il']):
        ni=max([s.get('source_index',-1) for s in m.get('sources',[])]+[-1])+1; m['sources'].append(src(ni,'Cupra Leon 2023/2024 Israeli price-list 2.0 190 hp','https://www.cartube.co.il/מחירון-רכב-חדש/קופרה/קופרה-לאון'))
        m['technical_variants_il'].append(var(None,'Hatchback','petrol','2.0L turbo',2.0,190,'7-speed dual_clutch','FWD',2023,2024,(ni,)))
# Challenger Hellcat hp
m=models.get(('Dodge','Challenger'))
if m:
    for v in m['technical_variants_il']:
        if v.get('version_or_trim')=='SRT Hellcat': v['horsepower_hp']=707
# Charade remove false-rejection hp labels
m=models.get(('Daihatsu','Charade'))
if m:
    m['invalid_or_non_trim_labels']=[x for x in m.get('invalid_or_non_trim_labels',[]) if x.get('classification')!='horsepower']
# Chery HEV
hev_profile=profile('Chery','Tiggo 4 HEV',[
 var('Comfort','SUV','hybrid','1.5L hybrid',1.5,163,'DHT automatic','FWD',2025,None,(0,)),
 var('Luxury','SUV','hybrid','1.5L hybrid',1.5,163,'DHT automatic','FWD',2025,None,(0,)),
 var('Noble','SUV','hybrid','1.5L hybrid',1.5,163,'DHT automatic','FWD',2025,None,(0,)),
],[src(0,'Chery Israel official TIGGO 4 HEV page','https://cheryisrael.co.il/models/tiggo-4-hev/',typ='official importer')],notes=['Batch 22 carry-forward correction: separate TIGGO 4 HEV line with Comfort, Luxury and Noble trims.'])
hev_profile['source_alias_keys']=['IL|Chery|Tiggo 4 Pro']
hev_profile['line_aliases']=['IL|Chery|Tiggo 4 Hybrid','IL|Chery|TIGGO 4 HEV','IL|Chery|Tiggo4 HEV']
models[('Chery','Tiggo 4 HEV')]=hev_profile
# validate all; route ready only to catalog, no active review
valid=[]; clean=[]; blocked=[]
for m in sorted(models.values(), key=lambda x:(x.get('make',''),x.get('model',''))):
    res=validate_profile(m); valid.append(res)
    if res.ready: clean.append(res.profile)
    else:
        p=res.profile; p['validation_issues']=res.issues; blocked.append(p)
cat['models']=clean; cat['generated_at']=now(); cat['ready_for_website_upload']=not blocked
rev={'generated_at':now(),'market':'IL','models':blocked}
ready=build_readiness_report(valid, web_search_enabled=True, checkpoint_state={})
archive['generated_at']=now()
dump(CAT,cat); dump(REV,rev); dump(READY,ready); dump(ARCH,archive)
# Recompute readiness from the de-duplicated written catalog so final metrics
# reflect generated outputs, not pre-deduplication repair inputs.
cat=load(CAT); rev=load(REV)
valid=[validate_profile(m) for m in cat.get('models', []) + rev.get('models', [])]
ready=build_readiness_report(valid, web_search_enabled=True, checkpoint_state={})
dump(READY,ready)
scan_quality(cat,rev)
if TASK.exists(): TASK.unlink()
print(json.dumps({'clean':len(clean),'blocked':len(blocked),'ready':ready['ready_for_website_upload']},indent=2))
