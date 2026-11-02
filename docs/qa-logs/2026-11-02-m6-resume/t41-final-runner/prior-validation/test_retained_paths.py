#!/usr/bin/env python3
"""Synthetic retained D228 + path controls; no producer/application runs.
Author Codex (GPT-6), /root, wN:p5, session01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import base64,copy,json,pathlib as P,runpy,types
OWN=P.Path(__file__).parent
lib=runpy.run_path(str(OWN/'test_supplement.py'),run_name='fixture_library');ns=lib['ns'];ROOT=lib['ROOT'];M=lib['M'];sha=lib['sha'];ATT=ROOT+'-attempt-1';RESULTS=[]

def putm(r,m):r.put(M,json.dumps(m,indent=2)+'\n')
def setup():
 r=lib['setup']();m=lib['getm'](r)
 old_line=br"        rec=emit('fixtures/'+kind+'.json',(json.dumps(obj,indent=2)+'\n').encode())"
 new_line=b"        rec=emit('fixtures/'+kind+'.json',dump(obj).encode())"
 old_builder=b'# inert synthetic identity only\n'+old_line+b'\n';builder=old_builder.replace(old_line,new_line)
 prior=r.data[ROOT+'/run.py'];r.put(ROOT+'/run.py',builder);r.put(ROOT+'/README.md',r.data[ROOT+'/README.md'].replace(sha(prior).encode(),sha(builder).encode()))
 for kind in ['drop','reach']:
  entry=next(x for x in m['inputs'] if x['kind']==kind);rows=json.loads(r.data[ROOT+'/'+entry['path']])
  for x in rows:x['path']=ns['dec'](x['path'])
  raw=(json.dumps(rows,indent=2)+'\n').encode().replace(b'mask-data0',b'mask\\u002ddata0');r.put(ROOT+'/'+entry['path'],raw);entry.update(size_bytes=len(raw),sha256=sha(raw))
 putm(r,m)
 st=r.tree(ns['SOURCE'],'');identities=[dict(path=p,mode=st[p].split()[0],blob_id=st[p].split()[2]) for p in sorted(ns['dec'](x['path']) for x in r.inv)]
 r.put(ROOT+'/source-identities.json',json.dumps(identities,indent=2)+'\n')
 for path,b in list(r.data.items()):
  if path.startswith(ROOT+'/'):r.put(ATT+path[len(ROOT):],b)
 old=copy.deepcopy(m);encoded=[]
 for kind in ['drop','reach']:
  entry=next(x for x in old['inputs'] if x['kind']==kind);path=entry['path'];decoded=r.data[ROOT+'/'+path].replace(b'\\u002d',b'-');r.put(ATT+'/'+path+'.base64',base64.encodebytes(decoded));lib['drop'](r,ATT+'/'+path);entry.update(size_bytes=len(decoded),sha256=sha(decoded))
  encoded.append(dict(original_path=path,stored_path=path+'.base64',size_bytes=len(decoded),sha256=sha(decoded),encoding='base64; exact original bytes, not a rewritten input'))
 for x in old['checks']:
  for key in ['start','end']:x[key]=x[key].replace('T23:','T22:')
 r.put(ATT+'/manifest.json',json.dumps(old,indent=2)+'\n');r.put(ATT+'/run.py',old_builder);r.put(ATT+'/README.md',r.data[ATT+'/README.md'].replace(sha(builder).encode(),sha(old_builder).encode()))
 r.put(ATT+'/serialization-error.json',json.dumps(dict(timestamp='2026-11-02T22:30:00Z',result='generator controls passed; publication hygiene failed',encoded_original_files=encoded,original_packet_preserved_at='/NEVER/READ/THIS')))
 return r

def json_change(r,path,fn):v=json.loads(r.data[path]);fn(v);r.put(path,json.dumps(v,indent=2)+'\n')
def check(label,fn,expected='FAIL'):
 try:fn();state='PASS';reason=''
 except Exception as e:state='FAIL';reason=type(e).__name__+': '+str(e)
 ok=state==expected;RESULTS.append(dict(label=label,ok=ok,state=state,reason=reason));print(('PASS' if ok else 'FAIL')+' TEST '+label+': '+state)

def proof_case(change=None):
 r=setup()
 if change:change(r)
 return ns['reconcile_generator'](r)

check('exact first attempt lossless reconstruction',proof_case,'PASS')
mutations=[
 ('retained encoded byte damage',lambda r:r.put(ATT+'/fixtures/drop.json.base64',b'!!!!')),
 ('retained encoding identity mismatch',lambda r:json_change(r,ATT+'/serialization-error.json',lambda x:x['encoded_original_files'][0].update(sha256='0'*64))),
 ('retained wrong encoding path',lambda r:json_change(r,ATT+'/serialization-error.json',lambda x:x['encoded_original_files'][0].update(stored_path='../outside'))),
 ('retained header altered',lambda r:r.put(ATT+'/'+lib['getm'](r)['inputs'][2]['path'],b'changed\n')),
 ('retained source identity altered',lambda r:r.put(ATT+'/source-identities.json',b'[]\n')),
 ('retained failed attempt identity changed',lambda r:json_change(r,ATT+'/manifest.json',lambda x:x.update(run_head='0'*40))),
 ('retained negative falsely passed',lambda r:json_change(r,ATT+'/manifest.json',lambda x:x['checks'][0].update(rc=0))),
 ('retained extra fixture',lambda r:r.put(ATT+'/fixtures/bytes/extra.patch',b'x\n')),
 ('retained nonserialization builder change',lambda r:r.put(ATT+'/run.py',r.data[ATT+'/run.py']+b'# extra\n')),
 ('retained false failure timing',lambda r:json_change(r,ATT+'/serialization-error.json',lambda x:x.update(timestamp='2026-11-02T23:30:00Z'))),
 ('retained wrong failure disposition',lambda r:json_change(r,ATT+'/serialization-error.json',lambda x:x.update(result='PASS'))),
 ('retained missing failure record',lambda r:lib['drop'](r,ATT+'/serialization-error.json')),
]
for label,change in mutations:check(label,lambda c=change:proof_case(c))

# The actual section guard runs over a tiny immutable-record Git double. It cannot
# invoke any command outside the enumerated read interfaces.
def guard_case(section,change=None):
 r=setup();r.dispatch='a'*40;r.coord='b'*40;commit='c'*40;header=lib['getm'](r)['inputs'][2]['path']
 changed=[ROOT+'/'+header,ATT+'/'+header];original_git=r.git
 def git(self,*args,missing=False):
  if args[0]=='log':return (commit+'\n').encode()
  if args[0]=='diff-tree' and '--numstat' in args:return ('1\t'+str(getattr(self,'removed',0))+'\t'+args[-1]+'\0').encode()
  if args[0]=='diff-tree':return b'\0'.join(x.encode() for x in changed)+b'\0'
  return original_git(*args,missing=missing)
 r.git=types.MethodType(git,r);r.refs[commit]=copy.deepcopy(r.refs[r.tip])
 if change:change(r,changed,commit)
 return ns['check'](r,section)
for section in ['product-paths','patch-untouched','fixes-record']:
 check(section+' exact two validated overlays',lambda s=section:guard_case(s),'PASS')
 cases=[
 ('wrong path',lambda r,ps,c:ps.append('audit/wrong/fixture.patch')),
 ('extra fixture',lambda r,ps,c:(r.put(ROOT+'/fixtures/bytes/extra.patch',b'x\n'),ps.append(ROOT+'/fixtures/bytes/extra.patch'))),
 ('product edit restored at final tip',lambda r,ps,c:ps.append('projects/ROCKNIX/product.txt')),
 ('selected source edit restored at final tip',lambda r,ps,c:ps.append(ns['dec'](r.inv[0]['path']))),
 ('overlay edit restored at final tip',lambda r,ps,c:r.refs[c].update({ps[0]:b'edited then restored\n'})),
 ('overlay executable mode',lambda r,ps,c:r.modes.update({(c,ps[0]):'100755'})),
 ('retained header altered',lambda r,ps,c:r.put(ps[1],b'edited\n')),
 ('register line removed',lambda r,ps,c:(ps.append('docs/decision-register.md'),setattr(r,'removed',1))),
 ('unrelated conf file',lambda r,ps,c:ps.append('audit/any.conf')),
 ]
 for name,change in cases:check(section+' '+name,lambda s=section,c=change:guard_case(s,c))
check('append-only register record stays permitted',lambda:guard_case('product-paths',lambda r,ps,c:ps.append('docs/decision-register.md')),'PASS')
check('product scope refuses another audit folder',lambda:guard_case('product-paths',lambda r,ps,c:ps.append('docs/audits/other-epic-m6-patches-shipped-kernel/x.md')))
(OWN/'checks-retained-paths.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
bad=sum(not x['ok'] for x in RESULTS);print('RETAINED/PATH SUMMARY',len(RESULTS)-bad,'passed,',bad,'failed');raise SystemExit(bool(bad))
