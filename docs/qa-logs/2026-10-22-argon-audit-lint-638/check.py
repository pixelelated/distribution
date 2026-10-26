import importlib.machinery,importlib.util,json,hashlib,tempfile,copy
from pathlib import Path
loader=importlib.machinery.SourceFileLoader('audit_lint',str(Path.cwd()/'tools/lint-audit-artifacts'));spec=importlib.util.spec_from_loader(loader.name,loader);mod=importlib.util.module_from_spec(spec);loader.exec_module(mod)
plan={'schema_version':1,'depth':'independent','primary':{'harness':'Codex','model':'unknown','lab':'openai','identity_source':'known primary lab, exact slug unavailable'},'reviewers':[{'member':'gemini-argon','model':'google/gemini-4-argon','lab':'google','effort':'high','calls':[{'phase':'blind','output':'blind.md'},{'phase':'refutation','output':'refute.md'}]}]}
text=b'Synthetic audit fixture only\n';digest=hashlib.sha256(text).hexdigest()
receipt={'member':'gemini-argon','facilitator_version':'council-facilitator@1.14.1-pixelelated.2','declared_model':'google/gemini-4-argon (OpenRouter, effort=high)','final':{'outcome':'success','verification':{'result':'PASS','model_identity_source':'provider_response','observed':'google/gemini-4-argon'},'effort_verification':{'result':'PASS','declared':'high'},'provider_verification':{'result':'PASS','observed_providers':['Google']},'file_artifact_sha256':digest}}
for case in ['valid','wrong-model','wrong-provider','unverified-provider','wrong-effort','missing-hash','wrong-legacy-hash','same-lab','missing-pass']:
 with tempfile.TemporaryDirectory(prefix='pix638-lint-') as temp:
  root=Path(temp);r=root/'second-opinions';r.mkdir();p=copy.deepcopy(plan);j=copy.deepcopy(receipt)
  if case=='wrong-model':j['final']['verification']['observed']='google/gemini-3.8-flash'
  if case=='wrong-provider':j['final']['provider_verification']['observed_providers']=['Other']
  if case=='unverified-provider':j['final']['provider_verification']['result']='UNVERIFIABLE'
  if case=='wrong-effort':p['reviewers'][0]['effort']='medium';j['final']['effort_verification']['declared']='medium'
  if case=='missing-hash':del j['final']['file_artifact_sha256']
  if case=='wrong-legacy-hash':j['output_file_sha256']='0'*64
  if case=='same-lab':p['primary']['lab']='google'
  if case=='missing-pass':p['reviewers'][0]['calls']=p['reviewers'][0]['calls'][:1]
  (r/'review-plan.json').write_text(json.dumps(p))
  for name in ['blind.md','refute.md']:(r/name).write_bytes(text);(r/(name+'.provenance.json')).write_text(json.dumps(j))
  bad=[];ok=[];mod.check_review_plan(root,True,bad.append,ok.append)
  assert (not bad and len(ok)==1) if case=='valid' else (len(bad)==1 and not ok),(case,bad,ok)
  print(case,'PASS')
