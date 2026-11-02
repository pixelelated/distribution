#!/usr/bin/env python3
"""Synthetic D228 sealed-packet controls. No producer/generator is invoked.
The in-memory Git/record double uses real Git blob-id construction; only the
expected formal-program hash is rebound to this fixture's inert bytes. The
candidate's published constant and generated shell stay pinned to the real hash.
"""
import copy, hashlib, json, pathlib as P, runpy, sys, types
OWN=P.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12')
lib=runpy.run_path(str(OWN/'test_reconcile.py'),run_name='fixture_library');ns=lib['ns'];template=lib['setup']();RESULTS=[]
ROOT='audit/'+ns['PROOF_ROOT'];M=ROOT+'/manifest.json';HEAD='e'*40
sha=lambda b:hashlib.sha256(b).hexdigest()
blobid=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
ns['PROOF_PROGRAM_SHA']=sha(template.blob('audit/tools/t41-tables.py'))

def tree(self,ref,path):
 return {p:self.modes.get((ref,p),'100644')+' blob '+blobid(b) for p,b in self.refs.get(ref,{}).items() if not path or p==path or p.startswith(path.rstrip('/')+'/')}
def git(self,*args,missing=False):
 if args[:2]==('cat-file','-t'):return b'commit\n' if args[2] in self.refs else b'blob\n'
 if args[:2]==('merge-base','--is-ancestor'):return None if self.unrelated else b''
 raise AssertionError('unexpected immutable Git interface '+repr(args))
def js(r,p,v):r.put(p,json.dumps(v,indent=2)+'\n')
def getm(r):return json.loads(r.data[M])
def mut(r,fn):v=getm(r);fn(v);js(r,M,v)
def drop(r,path):r.data.pop(path,None);r.refs[r.tip].pop(path,None)

def setup():
 r=copy.deepcopy(template);r.modes={};r.unrelated=False;r.tree=types.MethodType(tree,r);r.git=types.MethodType(git,r)
 baseline=json.dumps(r.inv,indent=2)+'\n';r.put('audit/stage-b/corrected/inventory-rows.json',baseline,[ns['STAGE_C']])
 # Valid historical timestamps and one Stage-D record identify unchanged support.
 hist=json.loads(r.data['audit/stage-c/validation.json'])
 for x in hist['checks']:x['start']='2026-11-02T18:00:00+00:00'
 r.put('audit/stage-c/validation.json',json.dumps(hist),[ns['STAGE_C']])
 r.put('audit/stage-d/record.json','{"synthetic":"retained D record"}\n')
 r.refs[ns['STAGE_D']]=copy.deepcopy(r.refs[r.tip]);r.refs[HEAD]=copy.deepcopy(r.refs[r.tip])
 inputs=[]
 rows=copy.deepcopy(r.inv);reach=copy.deepcopy(rows);next(x for x in reach if x['reach']=='shipped')['reach']='test'
 for kind,value in [('drop',rows[:-1]),('reach',reach)]:
  path='fixtures/'+kind+'.json';raw=(json.dumps(value,indent=2)+'\n').encode();r.put(ROOT+'/'+path,raw);inputs.append(dict(kind=kind,path=path,mode='100644',size_bytes=len(raw),sha256=sha(raw)))
 selected=sorted(x['path'].replace('\\u002d','-') for x in rows)
 for hp in selected:
  raw=r.blob(hp,ns['SOURCE']);parts=raw.splitlines(keepends=True);ix=next((i for i,line in enumerate(parts[:60]) if line.startswith(b'From: ')),None)
  if hp.endswith('.patch') and ix is not None:break
 changed=list(parts);changed[ix]=b'X-Proof-From: '+parts[ix][len(b'From: '):];overlay=b''.join(changed);path='fixtures/bytes/'+hp;r.put(ROOT+'/'+path,overlay)
 inputs.append(dict(kind='header',path=path,mode='100644',size_bytes=len(overlay),sha256=sha(overlay),source_path=hp,baseline_blob_id=blobid(raw),baseline_sha256=sha(raw)))
 checks=[];assertions=['membership: expected 107 rows','reach: expected shipped 103/test 4','From header census: expected 87']
 for i,kind in enumerate(['drop','reach','header','stats']):
  args=['python3','-I','audit/tools/t41-tables.py','stats']
  if kind!='stats':args += ['--bytes-from' if kind=='header' else '--rows-from',ROOT+'/fixtures/bytes' if kind=='header' else ROOT+'/fixtures/'+kind+'.json']
  out=r.audit('stage-c/tables/stats.txt') if kind=='stats' else b'';err=b'' if kind=='stats' else ('synthetic traceback\nAssertionError: '+assertions[i]+'\n').encode()
  stdout='logs/'+kind+'.stdout';stderr='logs/'+kind+'.stderr';r.put(ROOT+'/'+stdout,out);r.put(ROOT+'/'+stderr,err)
  checks.append(dict(kind=kind,argv=args,cwd='/synthetic/t41',start=f'2026-11-02T23:00:0{i}+00:00',end=f'2026-11-02T23:00:0{i}.010000+00:00',elapsed_seconds=.01,rc=0 if kind=='stats' else 1,stdout=stdout,stderr=stderr,stdout_sha256=sha(out),stderr_sha256=sha(err)))
 m=dict(schema=ns['PROOF_SCHEMA'],authority='D-WORKFLOW-228',historical_input_identity='unavailable; new controls only',source_ref=ns['SOURCE'],stage_c_ref=ns['STAGE_C'],run_head=HEAD,program=dict(path='tools/t41-tables.py',sha256=ns['PROOF_PROGRAM_SHA']),baseline_rows=dict(path='stage-b/corrected/inventory-rows.json',sha256=sha(baseline.encode())),inputs=inputs,checks=checks,result='PASS')
 js(r,M,m);builder=b"raise RuntimeError('inert synthetic builder; never executed')\n";r.put(ROOT+'/run.py',builder)
 readme='Synthetic new controls; original inputs unavailable.\nBuilder SHA256 '+sha(builder)+'\nValidation: git show REF:PATH; sha256sum FILE\n'
 readme+='\n'.join([x['path'] for x in inputs]+[x[k] for x in checks for k in ['stdout','stderr']]+['run.py','manifest.json'])+'\n';r.put(ROOT+'/README.md',readme)
 return r

def run(label,expected='FAIL',change=None):
 r=setup()
 if change:change(r)
 try:
  reason=ns['reconcile_generator'](r);status='PASS'
 except ns['Absent'] as e:status='ABSENT';reason=str(e)
 except ns['Cannot'] as e:status='CANNOT';reason=str(e)
 except (ns['Invalid'],KeyError,ValueError,TypeError,IndexError) as e:status='FAIL';reason=str(e)
 ok=status==expected
 if status=='PASS':ok &= 'original negative inputs remain unavailable' in reason and 'D228 new sealed' in reason
 RESULTS.append(dict(label=label,ok=ok,status=status,reason=reason));print(('PASS' if ok else 'FAIL')+' TEST '+label+': '+status)
 if not ok:print(reason)

def input_change(r,kind,fn):
 m=getm(r);entry=next(x for x in m['inputs'] if x['kind']==kind);path=ROOT+'/'+entry['path'];raw=fn(r.data[path]);r.put(path,raw);entry.update(size_bytes=len(raw),sha256=sha(raw));js(r,M,m)
def output_change(r,kind,stream,raw):
 m=getm(r);entry=next(x for x in m['checks'] if x['kind']==kind);r.put(ROOT+'/'+entry[stream],raw);entry[stream+'_sha256']=sha(raw);js(r,M,m)
def row_change(raw,fn):v=json.loads(raw);fn(v);return (json.dumps(v,indent=2)+'\n').encode()
def mode_change(r,kind,mode):
 entry=next(x for x in getm(r)['inputs'] if x['kind']==kind);r.modes[(r.tip,ROOT+'/'+entry['path'])]=mode

if __name__=='__main__':
 run('absent supplement is ABSENT','ABSENT',lambda r:drop(r,M))
 run('missing fixture file',change=lambda r:drop(r,ROOT+'/fixtures/drop.json'))
 run('wrong schema',change=lambda r:mut(r,lambda m:m.update(schema='unknown')))
 run('wrong authority',change=lambda r:mut(r,lambda m:m.update(authority='D-WORKFLOW-226')))
 run('historical identity falsely claimed',change=lambda r:mut(r,lambda m:m.update(historical_input_identity='recovered')))
 run('wrong source ref',change=lambda r:mut(r,lambda m:m.update(source_ref='0'*40)))
 run('wrong Stage-C ref',change=lambda r:mut(r,lambda m:m.update(stage_c_ref='0'*40)))
 run('unrelated run head',change=lambda r:setattr(r,'unrelated',True))
 run('run head is not a commit',change=lambda r:mut(r,lambda m:m.update(run_head='0'*40)))
 run('failed producer result',change=lambda r:mut(r,lambda m:m.update(result='FAIL')))
 run('wrong program hash',change=lambda r:mut(r,lambda m:m['program'].update(sha256='0'*64)))
 run('wrong baseline hash',change=lambda r:mut(r,lambda m:m['baseline_rows'].update(sha256='0'*64)))
 run('accepted Stage-D receipt changed',change=lambda r:r.put('audit/stage-d/record.json','changed\n'))
 run('selected source changed at run head',change=lambda r:r.refs[HEAD].update({r.inv[0]['path']:b'changed'}))
 run('remove first row instead of last',change=lambda r:input_change(r,'drop',lambda raw:(json.dumps(r.inv[1:])+'\n').encode()))
 run('reordered dropped rows',change=lambda r:input_change(r,'drop',lambda raw:row_change(raw,lambda rows:rows.reverse())))
 run('extra changed row field',change=lambda r:input_change(r,'reach',lambda raw:row_change(raw,lambda rows:rows[0].update(lines=1))))
 def wrong_reach(r):
  rows=copy.deepcopy(r.inv);ix=[i for i,x in enumerate(rows) if x['reach']=='shipped'];rows[ix[1]]['reach']='test';input_change(r,'reach',lambda raw:json.dumps(rows).encode())
 run('changed second shipped row',change=wrong_reach)
 run('header changed extra byte',change=lambda r:input_change(r,'header',lambda raw:raw+b'x'))
 run('header stripped instead of renamed prefix',change=lambda r:input_change(r,'header',lambda raw:b'\n'.join(x for x in raw.split(b'\n') if not x.startswith(b'X-Proof-From: '))))
 run('wrong header source path',change=lambda r:mut(r,lambda m:m['inputs'][2].update(source_path=r.inv[-1]['path'])))
 run('wrong baseline blob id',change=lambda r:mut(r,lambda m:m['inputs'][2].update(baseline_blob_id='0'*40)))
 run('wrong baseline source hash',change=lambda r:mut(r,lambda m:m['inputs'][2].update(baseline_sha256='0'*64)))
 run('wrong input hash',change=lambda r:mut(r,lambda m:m['inputs'][0].update(sha256='0'*64)))
 run('wrong input length',change=lambda r:mut(r,lambda m:m['inputs'][0].update(size_bytes=1)))
 run('bool is not integer size',change=lambda r:mut(r,lambda m:m['inputs'][0].update(size_bytes=True)))
 run('extra overlay file',change=lambda r:r.put(ROOT+'/fixtures/bytes/extra.patch','extra\n'))
 run('extra JSON fixture',change=lambda r:r.put(ROOT+'/fixtures/extra.json','[]\n'))
 run('symlink overlay refused',change=lambda r:mode_change(r,'header','120000'))
 run('executable overlay refused',change=lambda r:mode_change(r,'header','100755'))
 run('parent traversal path',change=lambda r:mut(r,lambda m:m['inputs'][0].update(path='../drop.json')))
 run('absolute artifact path',change=lambda r:mut(r,lambda m:m['checks'][0].update(stdout='/tmp/drop.out')))
 run('duplicate input kind',change=lambda r:mut(r,lambda m:m['inputs'][1].update(kind='drop')))
 run('non-object input refused',change=lambda r:mut(r,lambda m:m['inputs'].__setitem__(0,'invalid')))
 run('non-object check refused',change=lambda r:mut(r,lambda m:m['checks'].__setitem__(0,'invalid')))
 run('wrong command order',change=lambda r:mut(r,lambda m:m['checks'].reverse()))
 run('extra fifth command',change=lambda r:mut(r,lambda m:m['checks'].append(copy.deepcopy(m['checks'][3]))))
 run('wrong generator argv',change=lambda r:mut(r,lambda m:m['checks'][0]['argv'].__setitem__(2,'other.py')))
 run('wrong input argv',change=lambda r:mut(r,lambda m:m['checks'][0]['argv'].__setitem__(5,ROOT+'/fixtures/reach.json')))
 run('wrong header flag',change=lambda r:mut(r,lambda m:m['checks'][2]['argv'].__setitem__(4,'--rows-from')))
 run('negative rc is not exactly one',change=lambda r:mut(r,lambda m:m['checks'][0].update(rc=2)))
 run('bool is not integer rc',change=lambda r:mut(r,lambda m:m['checks'][0].update(rc=True)))
 run('non-UTC timestamp',change=lambda r:mut(r,lambda m:m['checks'][0].update(start='2026-11-02T23:00:00')))
 run('new proof backdated as old',change=lambda r:mut(r,lambda m:m['checks'][0].update(start='2026-11-02T17:00:00Z')))
 run('negative elapsed time',change=lambda r:mut(r,lambda m:m['checks'][0].update(elapsed_seconds=-1)))
 run('wrong raw output hash',change=lambda r:mut(r,lambda m:m['checks'][0].update(stderr_sha256='0'*64)))
 run('missing raw output',change=lambda r:drop(r,ROOT+'/logs/drop.stderr'))
 run('wrong final assertion even with valid hash',change=lambda r:output_change(r,'drop','stderr',b'AssertionError: wrong\n'))
 run('positive differs even with valid hash',change=lambda r:output_change(r,'stats','stdout',b'changed stats\n'))
 run('positive stderr nonempty',change=lambda r:output_change(r,'stats','stderr',b'warning\n'))
 run('output path alias',change=lambda r:mut(r,lambda m:m['checks'][1].update(stdout=m['checks'][0]['stdout'])))
 run('builder missing',change=lambda r:drop(r,ROOT+'/run.py'))
 run('builder changed without README binding',change=lambda r:r.put(ROOT+'/run.py','changed builder\n'))
 run('README file list missing',change=lambda r:r.put(ROOT+'/README.md','no evidence list\n'))
 def duplicate_json(r):r.put(M,b'{"schema":"duplicate",'+r.data[M][1:])
 run('duplicate JSON manifest key',change=duplicate_json)
 run('exact sealed supplement plus historical receipt control','PASS')
 def absolute_commands(r):
  def change(m):
   for x in m['checks']:
    x['argv'][2]=x['cwd']+'/'+x['argv'][2]
    if len(x['argv'])==6:x['argv'][5]=x['cwd']+'/'+x['argv'][5]
  mut(r,change)
 run('absolute bound command paths control','PASS',absolute_commands)
 def unescaped(r):
  for kind in ['drop','reach']:input_change(r,kind,lambda raw:raw.replace(b'\\\\u002d',b'-'))
 run('known filename escape normalization control','PASS',unescaped)
 # Exercise the actual Reader-to-Git empty-prefix seam on the tiny fixture repo.
 actual=ns['Reader'].__new__(ns['Reader']);actual.fixture='';actual.repo=str(lib['F']/'repo');actual.cache={}
 try:
  entries=actual.tree(lib['state']['base'],'');ok=len(entries)==437 and all(x['path'].replace('\\u002d','-') in entries for x in lib['inv'])
 except Exception:ok=False
 RESULTS.append(dict(label='actual Git full-tree read has no empty pathspec',ok=ok,status='PASS' if ok else 'FAIL'))
 print(('PASS' if ok else 'FAIL')+' TEST actual Git full-tree seam')
 (OWN/'checks-supplement.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
 bad=sum(not x['ok'] for x in RESULTS);print('D228 SUPPLEMENT TEST SUMMARY:',len(RESULTS)-bad,'passed,',bad,'failed');sys.exit(bool(bad))
