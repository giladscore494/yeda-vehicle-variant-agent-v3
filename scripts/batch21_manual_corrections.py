from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.catalog_builder import CATALOG_OUTPUT_PATH, READINESS_OUTPUT_PATH, REVIEW_OUTPUT_PATH, _atomic_write_json, compute_resume_state
from scripts.catalog_quality_scan import scan_quality
from scripts.catalog_validation import build_readiness_report, derive_available_values, validate_profile
from scripts.openai_catalog_client import GROUNDED_TECHNICAL_FIELDS

DATA=Path('data')
CAT=DATA/'model_technical_catalog_il.json'; REV=DATA/'model_technical_catalog_il_review.json'; READY=DATA/'model_technical_catalog_il_readiness.json'

def load(p): return json.load(open(p,encoding='utf-8'))
def key(m): return f"{m.get('market','IL')}|{m.get('make')}|{m.get('model')}"

def src(profile, title, url, source_name='Batch21 verified source', source_type='catalog/editorial'):
    sources=profile.setdefault('sources',[])
    for s in sources:
        if s.get('url')==url: return s.get('source_index', sources.index(s))
    idx=max([s.get('source_index',i) for i,s in enumerate(sources) if isinstance(s,dict)] or [-1])+1
    sources.append({'source_index':idx,'title':title,'url':url,'source_name':source_name,'source_type':source_type,'supports':list(GROUNDED_TECHNICAL_FIELDS)})
    return idx

def make_row(profile, refs, **kw):
    row={
      'version_or_trim':kw.get('version_or_trim'), 'body_type':kw['body_type'], 'fuel_type':kw['fuel_type'],
      'engine':kw['engine'], 'engine_displacement_l':kw.get('engine_displacement_l'), 'horsepower_hp':kw['horsepower_hp'],
      'transmission':kw['transmission'], 'drivetrain':kw['drivetrain'], 'year_start':kw['year_start'], 'year_end':kw.get('year_end'),
      'support_level':kw.get('support_level','direct'), 'source_indexes':refs, 'field_sources':{}, 'missing_grounded_fields':[]}
    for f in GROUNDED_TECHNICAL_FIELDS:
        if row.get(f) not in (None,''):
            row['field_sources'][f]=refs
    return row

def profile(make, model, rows=None, urls=None):
    return {'market':'IL','make':make,'model':model,'canonical_model':model,'year_start':None,'year_end':None,'technical_variants_il':rows or [],'available_values_for_website':{},'invalid_or_non_trim_labels':[],'sources':urls or [],'profile_confidence':'high','notes':['Batch 21 manual correction from embedded validation facts.']}

def apply():
    cat=load(CAT); rev=load(REV)
    by={key(m):m for m in cat['models'] if isinstance(m,dict)}
    rby={key(m):m for m in rev.get('models',[]) if isinstance(m,dict)}
    def get(make,model):
        k=f'IL|{make}|{model}'
        if k not in by: by[k]=profile(make,model)
        return by[k]
    def refs(m,title,url): return [src(m,title,url)]
    def replace(make,model,title,url,row_specs):
        m=get(make,model); r=refs(m,title,url); m['technical_variants_il']=[make_row(m,r,**x) for x in row_specs]; return m

    # global casing
    for d in (by,rby):
        for m in d.values():
            if m.get('make')=='Bmw': m['make']='BMW'
            if m.get('model')=='z4 sdrive20i': m['model']='Z4 sDrive20i'; m['canonical_model']='Z4 sDrive20i'
    by={key(m):m for m in by.values()}

    # RUN1
    replace('BYD','Seal','BYD Israel Seal','https://bydauto.co.il/model/byd-seal/',[
      dict(version_or_trim='Design',body_type='Sedan',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=313,transmission='single_speed',drivetrain='RWD',year_start=2024,year_end=None),
      dict(version_or_trim='Excellence',body_type='Sedan',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=531,transmission='single_speed',drivetrain='AWD',year_start=2024,year_end=None)])
    m=replace('BYD','Seal U','BYD Israel Seal U','https://bydauto.co.il/model/byd-seal-u/',[
      dict(version_or_trim='Comfort',body_type='SUV',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=218,transmission='single_speed',drivetrain='FWD',year_start=2024,year_end=2026),
      dict(version_or_trim='Design',body_type='SUV',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=218,transmission='single_speed',drivetrain='FWD',year_start=2024,year_end=2026),
      dict(version_or_trim='Boost',body_type='SUV',fuel_type='plug_in_hybrid',engine='1.5L plug-in hybrid',engine_displacement_l=1.5,horsepower_hp=218,transmission='automatic',drivetrain='FWD',year_start=2024,year_end=2026),
      dict(version_or_trim='Comfort',body_type='SUV',fuel_type='plug_in_hybrid',engine='1.5L plug-in hybrid',engine_displacement_l=1.5,horsepower_hp=218,transmission='automatic',drivetrain='FWD',year_start=2024,year_end=2026),
      dict(version_or_trim='Design',body_type='SUV',fuel_type='plug_in_hybrid',engine='1.5L plug-in hybrid',engine_displacement_l=1.5,horsepower_hp=324,transmission='automatic',drivetrain='AWD',year_start=2024,year_end=2026)])
    m['source_alias_keys']=sorted(set(m.get('source_alias_keys',[])+['IL|BYD|Song Plus']))
    by.pop('IL|BYD|Song Plus',None)
    replace('BYD','Sealion 7','BYD Israel Sealion 7','https://bydauto.co.il/model/byd-sealion-7/',[
      dict(version_or_trim='Boost',body_type='SUV',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=231,transmission='single_speed',drivetrain='RWD',year_start=2025,year_end=None),
      dict(version_or_trim='Comfort',body_type='SUV',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=313,transmission='single_speed',drivetrain='RWD',year_start=2025,year_end=None),
      dict(version_or_trim='Design',body_type='SUV',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=313,transmission='single_speed',drivetrain='RWD',year_start=2025,year_end=None),
      dict(version_or_trim='Excellence',body_type='SUV',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=531,transmission='single_speed',drivetrain='AWD',year_start=2025,year_end=None)])
    m=get('Cadillac','Escalade IQ'); r=refs(m,'Cadillac Israel Escalade IQ','https://www.cadillac.co.il/ESCALADE-IQ/'); m['technical_variants_il']=[make_row(m,r,version_or_trim=t,body_type='SUV',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=750,transmission='single_speed',drivetrain='AWD',year_start=2026,year_end=None) for t in ['Luxury Sport','Premium Luxury']]; m['split_from_source_group_key']='IL|Cadillac|Escalade'; m['source_alias_keys']=['IL|Cadillac|Escalade']
    replace('Cadillac','XT6','Cadillac Israel XT6','https://www.cadillac.co.il/דגמים/xt6/',[
      dict(version_or_trim='Premium Luxury',body_type='SUV',fuel_type='petrol',engine='3.6L V6',engine_displacement_l=3.6,horsepower_hp=310,transmission='9-speed automatic',drivetrain='AWD',year_start=2020,year_end=2026),
      dict(version_or_trim='Sport',body_type='SUV',fuel_type='petrol',engine='3.6L V6',engine_displacement_l=3.6,horsepower_hp=310,transmission='9-speed automatic',drivetrain='AWD',year_start=2020,year_end=2026)])
    replace('Chery','Arrizo 8','Chery Israel Arrizo 8','https://cheryisrael.co.il/pricing/',[
      dict(version_or_trim='Comfort',body_type='Sedan',fuel_type='plug_in_hybrid',engine='1.5L turbo plug-in hybrid',engine_displacement_l=1.5,horsepower_hp=347,transmission='automatic',drivetrain='FWD',year_start=2024,year_end=2026),
      dict(version_or_trim='Noble',body_type='Sedan',fuel_type='plug_in_hybrid',engine='1.5L turbo plug-in hybrid',engine_displacement_l=1.5,horsepower_hp=347,transmission='automatic',drivetrain='FWD',year_start=2024,year_end=2026)])
    replace('Chery','Tiggo 8 Pro','Chery Israel Tiggo 8 Pro','https://cheryisrael.co.il/pricing/',[
      dict(version_or_trim='Luxury / Noble',body_type='SUV',fuel_type='petrol',engine='1.6L turbo',engine_displacement_l=1.6,horsepower_hp=186,transmission='7-speed dual_clutch',drivetrain='FWD',year_start=2022,year_end=2024),
      dict(version_or_trim='Ultimate',body_type='SUV',fuel_type='plug_in_hybrid',engine='1.5L turbo',engine_displacement_l=1.5,horsepower_hp=318,transmission='3-speed automatic',drivetrain='FWD',year_start=2023,year_end=2024)])

    # RUN2 selected replacements/additions
    replace('Chevrolet','Blazer EV','Chevrolet Israel Blazer EV','https://www.chevrolet.co.il/דגמים/blazer-ev/',[dict(version_or_trim='RS',body_type='SUV',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=300,transmission='single_speed',drivetrain='AWD',year_start=2026,year_end=None)])
    replace('Chevrolet','Corvette','Chevrolet Israel Corvette','https://www.chevrolet.co.il/corvette/',[
      dict(version_or_trim='Stingray 2LT',body_type='Coupe',fuel_type='petrol',engine='6.2L V8',engine_displacement_l=6.2,horsepower_hp=490,transmission='8-speed dual_clutch',drivetrain='RWD',year_start=2023,year_end=None),
      dict(version_or_trim='Stingray 2LT',body_type='Convertible',fuel_type='petrol',engine='6.2L V8',engine_displacement_l=6.2,horsepower_hp=490,transmission='8-speed dual_clutch',drivetrain='RWD',year_start=2023,year_end=None)])
    m=get('Chevrolet','Cruze')
    for v in m.get('technical_variants_il',[]):
        if v.get('engine')=='1.4L turbo' and v.get('horsepower_hp')==153: v['year_end']=2020
    m=get('Chevrolet','Equinox'); r=refs(m,'iCar Equinox','https://www.icar.co.il/שברולט/שברולט_אקווינוקס/')
    m.setdefault('technical_variants_il',[]).append(make_row(m,r,version_or_trim=None,body_type='SUV',fuel_type='petrol',engine='1.5L turbo',engine_displacement_l=1.5,horsepower_hp=170,transmission='6-speed automatic',drivetrain='AWD',year_start=2018,year_end=2024))
    replace('Chevrolet','Orlando','iCar Orlando','https://www.icar.co.il/שברולט/שברולט_אורלנדו/שברולט_אורלנדו_יד_שניה_ד10/version11882/',[
      dict(version_or_trim='LT',body_type='MPV',fuel_type='diesel',engine='2.0L turbo diesel',engine_displacement_l=2.0,horsepower_hp=163,transmission='6-speed automatic',drivetrain='FWD',year_start=2012,year_end=2018),
      dict(version_or_trim='LS',body_type='MPV',fuel_type='petrol',engine='1.4L turbo',engine_displacement_l=1.4,horsepower_hp=140,transmission='6-speed automatic',drivetrain='FWD',year_start=2014,year_end=2018),
      dict(version_or_trim='LT',body_type='MPV',fuel_type='petrol',engine='1.4L turbo',engine_displacement_l=1.4,horsepower_hp=140,transmission='6-speed automatic',drivetrain='FWD',year_start=2014,year_end=2018)])
    replace('Chevrolet','Spark','iCar Chevrolet Spark','https://www.icar.co.il/שברולט/שברולט_ספארק/',[
      dict(version_or_trim='LS',body_type='Hatchback',fuel_type='petrol',engine='1.0L',engine_displacement_l=1.0,horsepower_hp=68,transmission='manual',drivetrain='FWD',year_start=2011,year_end=2015),
      dict(version_or_trim='LT',body_type='Hatchback',fuel_type='petrol',engine='1.2L',engine_displacement_l=1.2,horsepower_hp=82,transmission='manual',drivetrain='FWD',year_start=2011,year_end=2015),
      dict(version_or_trim='LTZ',body_type='Hatchback',fuel_type='petrol',engine='1.2L',engine_displacement_l=1.2,horsepower_hp=82,transmission='manual',drivetrain='FWD',year_start=2011,year_end=2015),
      dict(version_or_trim='LT',body_type='Hatchback',fuel_type='petrol',engine='1.0L',engine_displacement_l=1.0,horsepower_hp=74,transmission='manual',drivetrain='FWD',year_start=2016,year_end=2018),
      dict(version_or_trim='LT+',body_type='Hatchback',fuel_type='petrol',engine='1.4L',engine_displacement_l=1.4,horsepower_hp=98,transmission='cvt',drivetrain='FWD',year_start=2016,year_end=2023),
      dict(version_or_trim='LTZ',body_type='Hatchback',fuel_type='petrol',engine='1.4L',engine_displacement_l=1.4,horsepower_hp=98,transmission='cvt',drivetrain='FWD',year_start=2016,year_end=2023),
      dict(version_or_trim='Premier',body_type='Hatchback',fuel_type='petrol',engine='1.4L',engine_displacement_l=1.4,horsepower_hp=98,transmission='cvt',drivetrain='FWD',year_start=2016,year_end=2023)])
    m=get('Chevrolet','Trax'); r=refs(m,'Chevrolet Israel Trax','https://www.chevrolet.co.il/trax/'); old=[v for v in m.get('technical_variants_il',[]) if not (v.get('engine')=='1.2L turbo i3' or (v.get('year_start')==2023 and v.get('horsepower_hp')==139))]; m['technical_variants_il']=old+[make_row(m,r,version_or_trim=t,body_type='SUV',fuel_type='petrol',engine='1.2L turbo i3',engine_displacement_l=1.2,horsepower_hp=139,transmission='6-speed automatic',drivetrain='FWD',year_start=2023,year_end=None) for t in ['1RS','2RS']]
    m=get('Chrysler','300C')
    for v in m.get('technical_variants_il',[]):
        if v.get('engine')=='3.6L V6' and v.get('year_start')==2012: v['version_or_trim']='Limited'; v.setdefault('field_sources',{})['version_or_trim']=v.get('source_indexes',[0])
    replace('Chrysler','Pacifica','iCar Chrysler Pacifica','https://www.icar.co.il/קרייזלר/קרייזלר_פסיפיקה/קרייזלר_פסיפיקה_יד_שניה_ד10/',[
      dict(version_or_trim='Limited',body_type='MPV',fuel_type='petrol',engine='3.6L V6',engine_displacement_l=3.6,horsepower_hp=280,transmission='9-speed automatic',drivetrain='FWD',year_start=2018,year_end=2022),
      dict(version_or_trim='Touring L',body_type='MPV',fuel_type='petrol',engine='3.6L V6',engine_displacement_l=3.6,horsepower_hp=280,transmission='9-speed automatic',drivetrain='FWD',year_start=2018,year_end=2022)])
    m=get('Chrysler','Voyager'); m['canonical_model']='Grand Voyager'; m['source_alias_keys']=sorted(set(m.get('source_alias_keys',[])+['IL|Chrysler|Grand Voyager']))
    m=get('Citroen','Berlingo'); r=refs(m,'iCar Citroen Berlingo','https://www.icar.co.il/סיטרואן/סיטרואן_ברלינגו/סיטרואן_ברלינגו_חדש/')
    for v in m.get('technical_variants_il',[]):
        if v.get('fuel_type')=='diesel' and v.get('engine') in {'1.5L turbo', '1.5L turbo diesel'}:
            if v.get('year_start')==2018: v['year_start']=2019
            if v.get('horsepower_hp')==130: v['transmission']='8-speed automatic'
    m['technical_variants_il'].append(make_row(m,r,version_or_trim=None,body_type='Van',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=136,transmission='single_speed',drivetrain='FWD',year_start=2024,year_end=None))

    # RUN3 blockers promoted with grounded rows
    replace('Chery','Tiggo 4 Pro','Chery Israel Tiggo 4 Pro','https://cheryisrael.co.il/models/tiggo4pro/',[
      dict(version_or_trim='Noble',body_type='SUV',fuel_type='petrol',engine='1.5L petrol',engine_displacement_l=1.5,horsepower_hp=95,transmission='cvt',drivetrain='FWD',year_start=2024,year_end=2025),
      dict(version_or_trim='Comfort',body_type='SUV',fuel_type='petrol',engine='1.5L petrol',engine_displacement_l=1.5,horsepower_hp=95,transmission='cvt',drivetrain='FWD',year_start=2025,year_end=None)])
    m=replace('Chery','Tiggo 9 Pro PHEV','Chery Israel Tiggo 9 PHEV','https://cheryisrael.co.il/models/tiggo-9-phev/',[
      dict(version_or_trim='Luxury',body_type='SUV',fuel_type='plug_in_hybrid',engine='1.5L turbo plug-in hybrid',engine_displacement_l=1.5,horsepower_hp=428,transmission='automatic',drivetrain='AWD',year_start=2026,year_end=None),
      dict(version_or_trim='Noble',body_type='SUV',fuel_type='plug_in_hybrid',engine='1.5L turbo plug-in hybrid',engine_displacement_l=1.5,horsepower_hp=428,transmission='automatic',drivetrain='AWD',year_start=2025,year_end=None)])
    m['split_from_source_group_key']='IL|Chery|Tiggo 9'; m['source_alias_keys']=['IL|Chery|Tiggo 9']; by.pop('IL|Chery|Tiggo 9',None)
    replace('Chevrolet','Camaro','iCar Camaro Israel','https://www.icar.co.il/חדשות_רכב/שברולט_קמארו_SS_ו-ZL1_בישראל/',[
      dict(version_or_trim='LT',body_type='Coupe',fuel_type='petrol',engine='3.6L V6',engine_displacement_l=3.6,horsepower_hp=335,transmission='10-speed automatic',drivetrain='RWD',year_start=2016,year_end=2024),
      dict(version_or_trim='SS',body_type='Coupe',fuel_type='petrol',engine='6.2L V8',engine_displacement_l=6.2,horsepower_hp=455,transmission='10-speed automatic',drivetrain='RWD',year_start=2021,year_end=2024),
      dict(version_or_trim='ZL1',body_type='Coupe',fuel_type='petrol',engine='6.2L V8 supercharged',engine_displacement_l=6.2,horsepower_hp=650,transmission='10-speed automatic',drivetrain='RWD',year_start=2021,year_end=2024)])
    replace('Chevrolet','Captiva','iCar Captiva Israel','https://www.icar.co.il/שברולט/שברולט_קפטיבה/שברולט_קפטיבה_יד_שניה_ד10/version17103/',[
      dict(version_or_trim='LT',body_type='SUV',fuel_type='diesel',engine='2.0L turbo diesel',engine_displacement_l=2.0,horsepower_hp=167,transmission='automatic',drivetrain='AWD',year_start=2007,year_end=2017),
      dict(version_or_trim='LT',body_type='SUV',fuel_type='petrol',engine='2.4L petrol',engine_displacement_l=2.4,horsepower_hp=167,transmission='automatic',drivetrain='FWD',year_start=2011,year_end=2018),
      dict(version_or_trim='LTZ',body_type='SUV',fuel_type='petrol',engine='3.0L V6',engine_displacement_l=3.0,horsepower_hp=258,transmission='automatic',drivetrain='AWD',year_start=2011,year_end=2018)])
    replace('Chevrolet','Tahoe','Chevrolet Israel Tahoe','https://www.chevrolet.co.il/tahoe/',[dict(version_or_trim='High Country',body_type='SUV',fuel_type='petrol',engine='6.2L V8',engine_displacement_l=6.2,horsepower_hp=420,transmission='10-speed automatic',drivetrain='4WD',year_start=2025,year_end=None)])
    replace('Chevrolet','Traverse','Chevrolet Israel Traverse','https://www.chevrolet.co.il/traverse/',[
      dict(version_or_trim='LT Luxury',body_type='SUV',fuel_type='petrol',engine='2.5L turbo I4',engine_displacement_l=2.5,horsepower_hp=328,transmission='8-speed automatic',drivetrain='FWD',year_start=2024,year_end=None),
      dict(version_or_trim='LT Midnight',body_type='SUV',fuel_type='petrol',engine='2.5L turbo I4',engine_displacement_l=2.5,horsepower_hp=328,transmission='8-speed automatic',drivetrain='AWD',year_start=2024,year_end=None),
      dict(version_or_trim='Z71',body_type='SUV',fuel_type='petrol',engine='2.5L turbo I4',engine_displacement_l=2.5,horsepower_hp=328,transmission='8-speed automatic',drivetrain='AWD',year_start=2024,year_end=None)])
    replace('Citroen','C3 Picasso','iCar C3 Picasso','https://www.icar.co.il/סיטרואן/סיטרואן_C3_פיקאסו/סיטרואן_C3_פיקאסו_יד_שניה_ד10/version9162/',[dict(version_or_trim='Comfort',body_type='Compact Van',fuel_type='diesel',engine='1.6L HDi diesel',engine_displacement_l=1.6,horsepower_hp=92,transmission='robotic automatic',drivetrain='FWD',year_start=2010,year_end=2017)])
    replace('Citroen','C4 X','iCar Citroen C4 X','https://www.icar.co.il/סיטרואן/סיטרואן_C4_X/סיטרואן_C4_X_יד_שניה_ד10/',[
      dict(version_or_trim='Shine',body_type='Sedan',fuel_type='petrol',engine='1.2L turbo',engine_displacement_l=1.2,horsepower_hp=130,transmission='8-speed automatic',drivetrain='FWD',year_start=2023,year_end=None),
      dict(version_or_trim='Shine',body_type='Sedan',fuel_type='diesel',engine='1.5L turbo diesel',engine_displacement_l=1.5,horsepower_hp=130,transmission='8-speed automatic',drivetrain='FWD',year_start=2023,year_end=None),
      dict(version_or_trim='Shine',body_type='Sedan',fuel_type='electric',engine='electric',engine_displacement_l=None,horsepower_hp=136,transmission='single_speed',drivetrain='FWD',year_start=2023,year_end=None)])
    replace('Citroen','C5 Aircross','Citroen Israel C5 Aircross','https://online.citroen.co.il/pricelist/c5-aircross/',[
      dict(version_or_trim='Feel',body_type='SUV',fuel_type='diesel',engine='1.5L BlueHDi turbo diesel',engine_displacement_l=1.5,horsepower_hp=130,transmission='8-speed automatic',drivetrain='FWD',year_start=2019,year_end=2022),
      dict(version_or_trim='Shine Pack',body_type='SUV',fuel_type='diesel',engine='1.5L BlueHDi turbo diesel',engine_displacement_l=1.5,horsepower_hp=130,transmission='8-speed automatic',drivetrain='FWD',year_start=2019,year_end=2025),
      dict(version_or_trim='Shine Pack',body_type='SUV',fuel_type='petrol',engine='1.6L turbo petrol',engine_displacement_l=1.6,horsepower_hp=180,transmission='8-speed automatic',drivetrain='FWD',year_start=2019,year_end=2022),
      dict(version_or_trim='Shine Pack',body_type='SUV',fuel_type='plug_in_hybrid',engine='1.6L turbo plug-in hybrid',engine_displacement_l=1.6,horsepower_hp=225,transmission='8-speed automatic',drivetrain='FWD',year_start=2021,year_end=2022),
      dict(version_or_trim='Max',body_type='SUV',fuel_type='mild_hybrid',engine='1.2L turbo mild-hybrid',engine_displacement_l=1.2,horsepower_hp=145,transmission='6-speed dual-clutch',drivetrain='FWD',year_start=2026,year_end=None)])

    # BMW duplicate cleanup
    by.pop('IL|Bmw|850i',None)
    m=by.get('IL|BMW|M850i')
    if m:
        m['split_from_source_group_key']='IL|BMW|850i'; m['source_alias_keys']=['IL|BMW|850i']

    # Clean every profile through validator (optional nulls, years, values, dedupe)
    cleaned=[]; validations=[]
    for m in by.values():
        res=validate_profile(m); validations.append(res)
        if not res.ready:
            print('NOT READY', key(m), res.issues[:5])
        cleaned.append(res.profile)
    cleaned=sorted(cleaned,key=lambda m:(str(m.get('make')).lower(),str(m.get('model')).lower()))
    readiness=build_readiness_report([validate_profile(m) for m in cleaned], web_search_enabled=True, checkpoint_state={})
    readiness.update({'clean_models':len(cleaned),'review_entries':0,'review_overlap_entries':0,'review_only_blocked_entries':0})
    cat['models']=cleaned; cat['ready_for_website_upload']=readiness['ready_for_website_upload']
    rev={'generated_at':cat.get('generated_at'),'market':'IL','models':[]}
    _atomic_write_json(str(CAT),cat); _atomic_write_json(str(READY),readiness); _atomic_write_json(str(REV),rev)
    scan_quality(cat,rev)

if __name__=='__main__': apply()
