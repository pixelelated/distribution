#!/usr/bin/env python3
"""Test first: seven new metadata refusals, then production exact93 matrix."""
import copy,datetime,hashlib,importlib.util,json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1];D=R/'stage-e';F=D/'fixtures';F.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('s1_inputs',R/'tools/s1-input-contract.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
candidate,inputs=m.contract();(D/'input-manifest.json').write_text(json.dumps({'accepted_at':m.D,'files':inputs},indent=2)+'\n')
first=next(iter(candidate['outcomes']));mixed=next(k for k,v in candidate['outcomes'].items() if v['mixed'])
cases=[]
def add(name,edit,reason):
 x=copy.deepcopy(candidate);edit(x);f=F/(name+'.json');f.write_text(json.dumps(x,indent=2)+'\n');cases.append((name,f,reason))
add('missing-key',lambda x:x['outcomes'].pop(first),'native key membership')
dup=json.dumps(candidate,indent=2).replace('"outcomes": {','"outcomes": {'+json.dumps(first)+':'+json.dumps(candidate['outcomes'][first])+',',1)
f=F/'duplicate-key.json';f.write_text(dup+'\n');cases.append(('duplicate-key',f,'duplicate key:'))
add('changed-owner',lambda x:x['outcomes'][first].__setitem__('owner','invented owner'),'original owner changed')
add('lost-open-consumer',lambda x:x['outcomes'][mixed].__setitem__('consumers',[v for v in x['outcomes'][mixed]['consumers'] if v['group']!=next(v['group'] for v in x['outcomes'][mixed]['consumers'] if v['status']=='open-item')]),'open consumer membership lost')
add('lost-positive-consumer',lambda x:x['outcomes'][mixed].__setitem__('consumers',[v for v in x['outcomes'][mixed]['consumers'] if v['group']!=next(v['group'] for v in x['outcomes'][mixed]['consumers'] if v['status']!='open-item')]),'positive consumer membership lost')
def invent(x):
 c=next(c for c in x['outcomes'][first]['consumers'] if c['status']=='open-item');c['status']='applies';c['source_input_status']='resolved';c['retained_normal_result']={'exit':0}
add('invented-success',invent,'missing input must remain open')
add('changed-receipt',lambda x:x['outcomes'][first]['consumers'][0]['evidence'].__setitem__('blob','0'*40),'bound receipt identity')
def sha(b):return hashlib.sha256(b).hexdigest()
records=[]
def run(name,f,expected,reason):
 argv=['python3',str(R/'tools/check-owner-outcomes.py'),str(f)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (F/(name+'.stdout')).write_bytes(p.stdout);(F/(name+'.stderr')).write_bytes(p.stderr)
 record={'name':name,'argv':argv,'started':start,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':p.returncode,'fixture_sha256':sha(f.read_bytes()),'reader_sha256':sha((R/'tools/check-owner-outcomes.py').read_bytes()),'input_reader_sha256':sha((R/'tools/s1-input-contract.py').read_bytes()),'immutable_input_manifest_sha256':sha((D/'input-manifest.json').read_bytes()),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'expected_refusal':reason}
 records.append(record);(D/'owner-outcome-controls.json').write_text(json.dumps(records,indent=2)+'\n')
 assert p.returncode==expected,(name,p.stderr.decode())
 if reason:assert reason.encode() in p.stderr,(name,'wrong refusal',p.stderr.decode())
for name,f,reason in cases:run(name,f,1,reason)
production=D/'owner-outcomes.json';assert not production.exists();production.write_text(json.dumps(candidate,indent=2)+'\n')
run('positive',production,0,None)
counts={'native_keys':len(candidate['outcomes']),'mixed':sum(v['mixed'] for v in candidate['outcomes'].values()),'open_consumers':sum(c['status']=='open-item' for v in candidate['outcomes'].values() for c in v['consumers']),'positive_consumers':sum(c['status']!='open-item' for v in candidate['outcomes'].values() for c in v['consumers']),'programs':{str(p.relative_to(R)):sha(p.read_bytes()) for p in [pathlib.Path(__file__),R/'tools/check-owner-outcomes.py',R/'tools/s1-input-contract.py']},'matrix_sha256':sha(production.read_bytes()),'retained_inputs':len(inputs),'meaning':'custody only; all93 source-input gaps remain open'}
(D/'s1-result.json').write_text(json.dumps(counts,indent=2)+'\n')
print('PASS seven specific S1 refusals then production positive:',json.dumps(counts))
