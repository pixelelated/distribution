#!/usr/bin/env python3
import copy,datetime,gzip,hashlib,json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1];D=R/'stage-c';F=D/'fixtures';F.mkdir(parents=True,exist_ok=True);base=json.loads((R/'stage-b/table-input.json').read_text());cases=[]
x=copy.deepcopy(base);x.pop();cases.append(('drop-member','membership:',x))
x=copy.deepcopy(base);next(r for r in x if r['kind']=='config')['kind']='patch';cases.append(('wrong-config-kind','kind:',x))
x=copy.deepcopy(base);next(r for r in x if r['kind']=='symlink')['link']['sha256']='0'*64;cases.append(('changed-referent','link/referent identity:',x))
x=copy.deepcopy(base);r=next(r for r in x if any(t.startswith('From:') for n,t in r['header']));r['header']=[[n,'From: fabricated known attribution' if t.startswith('From:') else t] for n,t in r['header']];cases.append(('fabricated-header','header attribution:',x))
cases.append(('positive',None,base));results=[]
for name,want,data in cases:
 raw=(json.dumps(data,indent=2)+'\n').encode();f=F/(name+'.json.gz');f.write_bytes(gzip.compress(raw,mtime=0));argv=['python3',str(R/'tools/table.py'),str(f)]
 if want is None:argv+=['--output',str(R/'02-forward-audit.md')]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);(D/(name+'.stdout')).write_bytes(p.stdout);(D/(name+'.stderr')).write_bytes(p.stderr)
 row={'name':name,'argv':argv,'started':start,'exit':p.returncode,'fixture_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'decoded_input_sha256':hashlib.sha256(raw).hexdigest(),'producer_sha256':hashlib.sha256((R/'tools/table.py').read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'expected_refusal':want};results.append(row);(D/'table-controls.json').write_text(json.dumps(results,indent=2)+'\n')
 assert (p.returncode!=0 and want.encode() in p.stderr) if want else p.returncode==0,(name,p.stdout,p.stderr)
 print(name, 'EXPECTED REFUSAL' if want else 'PASS',p.returncode)
text=(R/'02-forward-audit.md').read_text()
for heading in ['Provenance','Coverage']:
 section=text.split('## '+heading+'\n',1)[1].split('\n## ',1)[0];keys=[l.split('|')[1].strip() for l in section.splitlines() if l.startswith('| projects/')];assert len(keys)==432 and len(set(keys))==432
print('PASS both rendered tables: exact 432 unique native keys')
