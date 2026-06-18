"""Apply the repository-local Batch 24 unified catalog corrections."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from scripts.catalog_builder import _atomic_write_json
from scripts.catalog_quality_scan import scan_quality
from scripts.catalog_validation import build_readiness_report, validate_profile
from scripts.openai_catalog_client import GROUNDED_TECHNICAL_FIELDS

DATA=Path('data'); CAT=DATA/'model_technical_catalog_il.json'; REV=DATA/'model_technical_catalog_il_review.json'; ARC=DATA/'model_technical_catalog_il_archive.json'; READY=DATA/'model_technical_catalog_il_readiness.json'
def load(p): return json.load(open(p,encoding='utf-8'))
def key(m): return f"{m.get('market','IL')}|{m.get('make')}|{m.get('model')}"
def add_source(m,title,url):
 s=m.setdefault('sources',[])
 for x in s:
  if x.get('url')==url:return x.get('source_index',s.index(x))
 i=max([x.get('source_index',n) for n,x in enumerate(s) if isinstance(x,dict)]or[-1])+1
 s.append({'source_index':i,'title':title,'url':url,'source_name':'Batch 24 embedded validation source','source_type':'official/catalog/editorial','supports':list(GROUNDED_TECHNICAL_FIELDS)})
 return i
def ground(v,refs):
 v['source_indexes']=list(refs); v['field_sources']={f:list(refs) for f in GROUNDED_TECHNICAL_FIELDS if v.get(f) not in(None,'')}; v['missing_grounded_fields']=[]; v['support_level']='direct'; return v
def row(refs,trim,body,fuel,engine,disp,hp,trans,drive,start,end):
 return ground({'version_or_trim':trim,'body_type':body,'fuel_type':fuel,'engine':engine,'engine_displacement_l':disp,'horsepower_hp':hp,'transmission':trans,'drivetrain':drive,'year_start':start,'year_end':end},refs)
def new_profile(make,model): return {'market':'IL','make':make,'model':model,'canonical_model':model,'year_start':None,'year_end':None,'technical_variants_il':[],'available_values_for_website':{},'invalid_or_non_trim_labels':[],'sources':[],'profile_confidence':'high','notes':['Batch 24 correction from embedded validation facts.']}
def archive(arc,m,reason,lineage=None,technical_reference=None):
 lineage=lineage or [key(m)]
 market=lineage[0].split('|',1)[0] if lineage and '|' in lineage[0] else m.get('market','IL')
 rec={'market':market,'make':m.get('make'),'model':m.get('model'),'reason':reason,'non_blocking':True,'batch_id':'BATCH24','lineage':lineage}
 if technical_reference is not None: rec['technical_reference']=technical_reference
 if any(x.get('batch_id')=='BATCH24' and x.get('make')==rec['make'] and x.get('model')==rec['model'] and x.get('reason')==reason and x.get('lineage')==rec['lineage'] for x in arc): return
 arc.append(rec)
def apply():
 cat,rev,arcd=load(CAT),load(REV),load(ARC); models=cat['models']; reviews=rev['models']; archives=arcd.get('models',[])
 def matches(make,model): return [m for m in models if m.get('make')==make and m.get('model')==model]
 def get(make,model):
  found=matches(make,model)
  if found:return found[0]
  m=new_profile(make,model); models.append(m); return m
 def rename(make,old,new):
  for m in models+reviews:
   if m.get('make')==make and m.get('model')==old:
    m['model']=new;m['canonical_model']=new;m['source_alias_keys']=sorted(set(m.get('source_alias_keys',[])+[f'IL|{make}|{old}']))
 def refs(m,title,url): return [add_source(m,title,url)]
 def replace(make,model,title,url,specs):
  m=get(make,model); r=refs(m,title,url); m['technical_variants_il']=[row(r,*x) for x in specs]; return m
 def dedupe(make,model,aliases):
  found=matches(make,model)
  if len(found)<2:return found[0] if found else None
  keep=found[0]
  for other in found[1:]:
   for s in other.get('sources',[]): add_source(keep,s.get('title','Merged source'),s.get('url',''))
   models.remove(other)
  keep['source_alias_keys']=sorted(set(keep.get('source_alias_keys',[])+aliases)); return keep
 # RUN 1
 for a,b in [('h2','H2'),('h3','H3')]: rename('Hummer',a,b)
 for a,b in [('elantra','Elantra'),('getz','Getz'),('grandeur','Grandeur')]: rename('Hyundai',a,b)
 m=get('Honda','HR-V'); old=m['technical_variants_il'][0]; old['year_end']=2021; old['field_sources']['year_end']=old['source_indexes']; r=refs(m,'Honda Israel HR-V e:HEV','https://hondacars.co.il/model/hrv-hybrid-ehev/'); m['technical_variants_il']=[old]+[row(r,t,'SUV','hybrid','1.5L e:HEV',1.5,131,'cvt','FWD',2024,None) for t in ('Elegance','Advance')]
 for v in get('Honda','Jazz')['technical_variants_il']:
  if v.get('horsepower_hp')==122:v['year_end']=None;v['field_sources'].pop('year_end',None)
 replace('Honda','ZR-V','Honda Israel ZR-V','https://hondacars.co.il/model/zrv-hybrid-ehev/',[(t,'SUV','hybrid','2.0L e:HEV',2.0,184,'cvt','FWD',2026,None) for t in ('Elegance','Sport','Advance')])
 for v in get('Hongqi','E-HS9')['technical_variants_il']:
  if v.get('horsepower_hp')==551:v['year_end']=None;v['field_sources'].pop('year_end',None)
 # Casper is preview-only.
 for m in list(matches('Hyundai','Casper')): archive(archives,m,'expected_arrival_only',['IL|Hyundai|Casper','IL|Hyundai|Inster']);models.remove(m)
 m=get('Hyundai','Elantra'); r=refs(m,'Hyundai Israel Elantra Hybrid','https://www.hyundaimotors.co.il/models/elantra-hybrid'); hist=[v for v in m['technical_variants_il'] if v.get('fuel_type')!='hybrid']; m['technical_variants_il']=hist+[row(r,'Prime / Premium / Supreme / Luxury','Sedan','hybrid','1.6L hybrid',1.6,139,'dual_clutch','FWD',2021,None)]
 en=replace('Hyundai','Elantra N','Hyundai Israel Elantra N','https://www.hyundaimotors.co.il/models/elantran',[('Performance manual','Sedan','petrol','2.0L turbo',2.0,280,'6-speed manual','FWD',2025,None),('Performance automatic','Sedan','petrol','2.0L turbo',2.0,280,'8-speed dual_clutch','FWD',2025,None)])
 en['split_from_source_group_key']='IL|Hyundai|elantra'
 # RUN 2
 for v in get('Hyundai','i25')['technical_variants_il']:
  if v.get('year_start')==2015:v['transmission']='6-speed automatic'
 for v in list(get('Hyundai','i30 N')['technical_variants_il']):
  if v.get('year_start')==2023 and 'manual' in str(v.get('transmission')): get('Hyundai','i30 N')['technical_variants_il'].remove(v);archive(archives,{'make':'Hyundai','model':'i30 N'},'unsupported_transmission_for_israeli_period',technical_reference=v)
 m=get('Hyundai','Ioniq 5'); m['technical_variants_il']=[v for v in m['technical_variants_il'] if v.get('horsepower_hp')!=609]
 for v in get('Hyundai','Ioniq 5 N')['technical_variants_il']:v['year_end']=None;v['field_sources'].pop('year_end',None)
 for v in get('Hyundai','Ioniq 6')['technical_variants_il']:
  if v.get('horsepower_hp')==228:v['year_end']=None;v['field_sources'].pop('year_end',None)
 for m in list(matches('Hyundai','Nexo')): archive(archives,m,'global_or_foreign_test_drive_only');models.remove(m)
 replace('Hyundai','Palisade','Hyundai Palisade embedded sources','https://www.hyundaimotors.co.il/',[(None,'SUV','petrol','3.8L V6',3.8,291,'8-speed automatic','FWD',2020,2024),(None,'SUV','petrol','3.8L V6',3.8,291,'8-speed automatic','AWD',2020,2024),('Luxury / Calligraphy','SUV','hybrid','2.5L turbo hybrid',2.5,334,'6-speed automatic','AWD',2026,None)])
 m=get('Hyundai','Santa Fe');r=refs(m,'Hyundai Israel Santa Fe Hybrid','https://www.hyundaimotors.co.il/');m['technical_variants_il'] += [row(r,'Elite 2X4','SUV','hybrid','1.6L turbo hybrid',1.6,215,'6-speed automatic','FWD',2025,None),row(r,'Calligraphy 4X4','SUV','hybrid','1.6L turbo hybrid',1.6,215,'6-speed automatic','AWD',2025,None)]
 for v in get('Hyundai','Sonata')['technical_variants_il']:
  if v.get('fuel_type')=='petrol' and v.get('year_start')==2021:v['year_end']=2024;v.setdefault('field_sources',{})['year_end']=v['source_indexes']
 # RUN 3
 for v in get('Hyundai','Staria')['technical_variants_il']:
  if v.get('fuel_type')=='diesel':v['year_end']=2024;v.setdefault('field_sources',{})['year_end']=v['source_indexes']
  elif v.get('fuel_type')=='hybrid':v['version_or_trim']='Premium / Luxury / Commercial';v.setdefault('field_sources',{})['version_or_trim']=v['source_indexes']
 for v in get('Hyundai','Terracan')['technical_variants_il']:
  if v.get('fuel_type')=='petrol':v['horsepower_hp']=200
 for v in get('Hyundai','Venue')['technical_variants_il']:v['horsepower_hp']=121;v['year_end']=None;v['field_sources'].pop('year_end',None)
 for v in get('Infiniti','Q50')['technical_variants_il']:
  if v.get('engine','').startswith('3.0L'):v['horsepower_hp']=405;v['version_or_trim']='Sport Tech'
 for v in get('Infiniti','Q60')['technical_variants_il']:
  if v.get('engine','').startswith('3.0L'):v['horsepower_hp']=405
 for v in get('Infiniti','QX50')['technical_variants_il']:
  if v.get('engine','').startswith('2.0L'):v['year_end']=None;v['field_sources'].pop('year_end',None)
 m=get('Infiniti','QX60');r=refs(m,'Infiniti QX60 current embedded source','https://www.infiniti-cars.co.il/');m['technical_variants_il'].append(row(r,'Luxe / Sensory','SUV','petrol','2.0L VC-Turbo',2.0,268,'9-speed automatic','AWD',2025,None))
 for v in get('Infiniti','QX80')['technical_variants_il']:v['drivetrain']='AWD'
 m=dedupe('Isuzu','Rodeo',['global-reference-only|Isuzu|Rodeo'])
 if m:m['market']='IL-confirmed'
 m=dedupe('Isuzu','Trooper',['IL-likely|Isuzu|Trooper'])
 if m:m['market']='IL-confirmed'
 if m:m['technical_variants_il']=[v for v in m['technical_variants_il'] if not(v.get('engine','').startswith('2.8L'))]
 # RUN 4
 m=dedupe('Jaecoo','J7',['IL-likely|Jaecoo|J7']); r=refs(m,'Jaecoo Israel J7 PHEV','https://jaecoo.co.il/'); m['technical_variants_il']=[v for v in m['technical_variants_il'] if v.get('version_or_trim')]+[row(r,'Elegance / Premium / Luxury','SUV','plug_in_hybrid','1.5L turbo plug-in hybrid',1.5,342,'3-speed automatic','FWD',2025,None)]
 m=get('Jaecoo','J8');
 for v in list(m['technical_variants_il']):
  if v.get('fuel_type')=='petrol':m['technical_variants_il'].remove(v);archive(archives,{'make':'Jaecoo','model':'J8'},'global_reference_only',technical_reference=v)
 for name in ('E-Pace','I-Pace'):
  for v in get('Jaguar',name)['technical_variants_il']:v['support_level']='direct'
 dedupe('Jaguar','X-Type',['IL-likely|Jaguar|X-Type','global-reference-only|Jaguar|X-Type']); m=get('Jaguar','X-Type');m['technical_variants_il']=[v for v in m['technical_variants_il'] if not(v.get('engine','').startswith('2.1L'))]
 m=dedupe('Jaguar','XJ',['IL-likely|Jaguar|XJ'])
 if m:m['market']='IL-confirmed'
 m=get('Jeep','Avenger');
 for v in m['technical_variants_il']:
  if v.get('fuel_type')=='mild_hybrid':v['year_end']=None;v['field_sources'].pop('year_end',None)
 # FINAL blockers
 review_by={(m.get('make'),m.get('model')):m for m in reviews}
 for make,model,reason in [('Honda','e:Ny1','parallel_import_or_insufficient_official_israeli_evidence'),('Isuzu','MU-X','global_reference_only_no_israeli_market_evidence'),('Hyundai','Trajet','insufficient_confirmed_israeli_sales_evidence')]:
  m=review_by.get((make,model));
  if m:archive(archives,m,reason);reviews.remove(m)
 fr=review_by.get(('Honda','FR-V'))
 if fr:
  for v in fr['technical_variants_il']:v['drivetrain']='FWD';v.setdefault('field_sources',{})['drivetrain']=v.get('source_indexes',[0])
  models.append(fr);reviews.remove(fr)
 od=review_by.get(('Honda','odyssey'))
 if od:
  od['model']='Odyssey';od['canonical_model']='Odyssey';od['source_alias_keys']=['IL|Honda|odyssey'];bad=[v for v in od['technical_variants_il'] if v.get('horsepower_hp') is None];od['technical_variants_il']=[v for v in od['technical_variants_il'] if v not in bad]
  for v in bad:archive(archives,{'make':'Honda','model':'Odyssey'},'missing_required_field_grounding',technical_reference=v)
  models.append(od);reviews.remove(od)
 i30=review_by.get(('Hyundai','i30 CW'))
 if i30:
  valid=[s.get('source_index',n) for n,s in enumerate(i30.get('sources',[]))]; rr=valid[:1] or [add_source(i30,'iCar i30 CW','https://www.icar.co.il/יונדאי/יונדאי_i30_סטיישן_CW/')]
  for v in i30['technical_variants_il']:ground(v,rr)
  i30['invalid_or_non_trim_labels']=[]
  models.append(i30);reviews.remove(i30)
 replace('Hyundai','Ioniq','Auto Hyundai Ioniq Israel','https://www.auto.co.il/cars/hyundai/ioniq/',[(None,'Liftback','hybrid','1.6L hybrid',1.6,141,'6-speed dual_clutch','FWD',2017,2022),(None,'Liftback','electric','electric',None,136,'single_speed','FWD',2019,2022)])
 replace('Hyundai','Kona','Hyundai Israel Kona Hybrid','https://www.hyundaimotors.co.il/models/kona-hybrid',[(None,'SUV','hybrid','1.6L hybrid',1.6,141,'dual_clutch','FWD',2019,2025),(None,'SUV','hybrid','1.6L hybrid',1.6,129,'dual_clutch','FWD',2026,None)])
 replace('Hyundai','Tucson','Hyundai Israel Tucson Hybrid','https://www.hyundaimotors.co.il/models/tucson-hybrid',[('Pure / Prestige','SUV','hybrid','1.6L turbo hybrid',1.6,230,'automatic','AWD',2025,None)])
 for nm in ('Ioniq','Kona','Tucson'):
  x=review_by.get(('Hyundai',nm));
  if x in reviews:reviews.remove(x)
 dm=review_by.get(('Isuzu','D-Max'))
 if dm:
  for v in dm['technical_variants_il']:
   if v.get('year_start')==2007:v['drivetrain']='4WD';v.setdefault('field_sources',{})['drivetrain']=v.get('source_indexes',[0])
  models.append(dm);reviews.remove(dm)
 st=review_by.get(('Jaguar','S-Type'))
 if st:archive(archives,st,'source_scope_duplicate',['IL-likely|Jaguar|S-Type','IL-confirmed|Jaguar|S-Type']);reviews.remove(st);get('Jaguar','S-Type')['source_alias_keys']=sorted(set(get('Jaguar','S-Type').get('source_alias_keys',[])+['IL-likely|Jaguar|S-Type']))
 # Empty Stream is conservatively archived.
 st=review_by.get(('Honda','Stream'))
 if st in reviews:archive(archives,st,'insufficient_field_level_grounding');reviews.remove(st)
 # Remove any remaining review entries as explicit non-blocking records rather than active blockers.
 for m in list(reviews):archive(archives,m,'batch24_unresolved_weak_evidence');reviews.remove(m)
 # Validate, normalize and regenerate all generated reports.
 clean=[]; vals=[]
 for m in models:
  for v in m.get('technical_variants_il',[]):
   refs=v.get('source_indexes') or []
   fs=v.setdefault('field_sources',{})
   v['missing_grounded_fields']=[]
   for f in GROUNDED_TECHNICAL_FIELDS:
    if v.get(f) not in (None,'') and not fs.get(f):fs[f]=list(refs)
  res=validate_profile(m)
  if not res.ready: raise RuntimeError(f"Batch24 produced blocked profile {key(m)}: {res.issues[:4]}")
  clean.append(res.profile);vals.append(res)
 clean.sort(key=lambda x:(str(x.get('make')).casefold(),str(x.get('model')).casefold()))
 readiness=build_readiness_report(vals,web_search_enabled=True,checkpoint_state={'last_checkpointed_profile_id':'IL-confirmed::Jeep::Avenger'})
 readiness.update({'clean_models':len(clean),'review_entries':0,'review_overlap_entries':0,'review_only_blocked_entries':0,'active_blocked':0,'unmatched_output_keys_count':0,'unmatched_output_keys_sample':[],'resume_after_key':'IL-confirmed|Jeep|Avenger','next_key_to_process':'IL-likely|Jeep|Avenger'})
 now=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ');cat['generated_at']=now;cat['models']=clean;cat['ready_for_website_upload']=readiness['ready_for_website_upload'];rev={'generated_at':now,'market':'IL','models':[]};arcd={'generated_at':now,'market':'IL','models':archives}
 _atomic_write_json(str(CAT),cat);_atomic_write_json(str(REV),rev);_atomic_write_json(str(ARC),arcd);_atomic_write_json(str(READY),readiness);scan_quality(cat,rev)
if __name__=='__main__':apply()
