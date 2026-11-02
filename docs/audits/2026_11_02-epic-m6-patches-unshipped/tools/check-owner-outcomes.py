#!/usr/bin/env python3
"""Validate the new exact93-key custody matrix against immutable D evidence."""
import importlib.util,json,pathlib,sys
P=pathlib.Path(__file__).with_name('s1-input-contract.py');spec=importlib.util.spec_from_file_location('s1_inputs',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def pairs(rows):
 out={}
 for k,v in rows:
  assert k not in out,'duplicate key: '+k
  out[k]=v
 return out
def check(path):
 actual=json.loads(pathlib.Path(path).read_text(),object_pairs_hook=pairs);expected,inputs=m.contract()
 assert actual['schema_version']==1 and actual['authority']==expected['authority'] and actual['accepted_at']==expected['accepted_at'],'authority identity'
 a=actual['outcomes'];e=expected['outcomes'];assert len(a)==93 and set(a)==set(e),'native key membership'
 for key,want in e.items():
  row=a[key];assert row['owner']==want['owner'],'original owner changed'
  assert row['application']==want['application'] and row['receipts']==want['receipts'],'original application/receipt text changed'
  assert row['source_input_status']=='open' and row['custody_outcome']==want['custody_outcome'],'missing input must remain open'
  assert row['mixed']==want['mixed'],'mixed qualification changed'
  assert row['original_binding']==want['original_binding'],'bound receipt identity'
  got=row['consumers'];wc=want['consumers']
  assert len({x['group'] for x in got})==len(got),'duplicate consumer'
  original_open={x['group'] for x in wc if x['status']=='open-item'}
  original_positive={x['group'] for x in wc if x['status']!='open-item'}
  present={x['group'] for x in got}
  assert original_open<=present,'open consumer membership lost'
  assert original_positive<=present,'positive consumer membership lost'
  assert present==original_open|original_positive,'unexpected consumer'
  by={x['group']:x for x in got}
  for want_c in wc:
   c=by[want_c['group']]
   if want_c['status']=='open-item':assert c['status']=='open-item' and c['source_input_status']=='open' and c['retained_normal_result'] is None,'missing input must remain open'
   assert c['evidence']==want_c['evidence'] and c['plan_binding']==want_c['plan_binding'],'bound receipt identity'
   assert c==want_c,'per-plan qualification/owner/input/mechanism changed'
 print('PASS S1 exact93-key custody; owners9/72/3/7/2;87 wholly open/6 mixed; all positive/open consumers and receipt identities preserved; no source-input gap resolved')
if __name__=='__main__':check(sys.argv[1])
