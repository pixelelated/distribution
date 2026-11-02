#!/usr/bin/env python3
"""New own-lane controls after explicit #690 process-scope clarification."""
import copy,hashlib,importlib.util,json,os,pathlib,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('retire',R/'tools/retirement.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
root=pathlib.Path(tempfile.mkdtemp(prefix='f-retirement-controls-',dir=m.BASE));allowed={str(root)};records=[];children=[]
created={'at':m.now(),'root':str(root),'pid':os.getpid(),'process_identity':m.OWN.identity(os.getpid()),'uid':os.getuid(),'cwd':os.getcwd(),'argv':sys.argv,'root_identity':m.meta(root.lstat()),'purpose':'new F own-lane retirement metadata controls; original failed attempt preserved'}
(R/'stage-f/retirement-control-creation-v2.json').write_text(json.dumps(created,indent=2)+'\n')
f=root/'a.txt';f.write_bytes(b'owned F control\n')
want={'a.txt':{'type':'file','mode':oct(f.stat().st_mode&0o777),'sha256':m.sha(f.read_bytes()),'bytes':f.stat().st_size}}
def save():
 (R/'stage-f/retirement-controls-v2.json').write_text(json.dumps({'program_sha256':m.sha((R/'tools/retirement.py').read_bytes()),'scope_program_sha256':m.sha((R/'tools/retirement-owner-scope.py').read_bytes()),'controller_sha256':m.sha(pathlib.Path(__file__).read_bytes()),'records':records,'known_children':children,'scope':'new record controls only; no production path mutation; no unrelated-process inspection'},indent=2)+'\n')
def test(name,fn,reason,inputs=None):
 start=m.now()
 try:fn()
 except (AssertionError,OSError) as e:
  assert reason in str(e),(name,type(e).__name__,str(e))
  records.append({'name':name,'started':start,'finished':m.now(),'actual_exception':type(e).__name__,'actual_message':str(e),'expected_refusal':reason,'inputs':inputs,'passed':True});save()
 else:raise AssertionError('guard did not refuse '+name)
f.write_bytes(b'changed\n');test('changed-content',lambda:m.inspect(str(root),want,allowed),'content snapshot mismatch');f.write_bytes(b'owned F control\n')
f.unlink();f.symlink_to('target.txt');(root/'target.txt').write_bytes(b'owned target\n');test('symlink-substitution',lambda:m.inspect(str(root),want,allowed),'symlink or special-file substitution');f.unlink();(root/'target.txt').unlink();f.write_bytes(b'owned F control\n')
test('mount-crossing-metadata',lambda:m.inspect(str(root),want,allowed,device=root.stat().st_dev+1),'mount crossing')
test('owner-mismatch-metadata',lambda:m.inspect(str(root),want,allowed,owner_uid=os.getuid()+1),'owner mismatch')
prior=m.inspect(str(root),want,allowed)['nodes'];wrong=copy.deepcopy(prior);wrong['.']['ino']+=1
test('changed-identity',lambda:m.inspect(str(root),want,allowed,prior=wrong),'fresh identity/metadata changed')
test('unknown-root',lambda:m.inspect(str(m.BASE/'not-owned'),{},allowed),'unknown or unconfined path')
test('durable-root',lambda:m.inspect(str(m.BASE/'stage-d-publication'),{},{str(m.BASE/'stage-d-publication')}),'cache/receipt path protected')
completion=m.completed('stage-b/application-run.json');observer=m.OWN.observer()
fd=os.open(f,os.O_RDONLY)
try:test('actual-own-fd',lambda:m.OWN.assess(str(root),completion,[observer]),'known own cwd/fd reference',{'root':str(root),'completion':completion,'known_jobs':[observer],'actual_fd':fd})
finally:os.close(fd)
missing=copy.deepcopy(completion);missing['finished']=None
test('missing-own-completion',lambda:m.OWN.assess(str(root),missing,[observer]),'missing or ambiguous own completion',missing)
ambiguous=copy.deepcopy(observer);ambiguous['start_ticks']=str(int(ambiguous['start_ticks'])+1)
test('ambiguous-known-identity',lambda:m.OWN.assess(str(root),completion,[ambiguous]),'ambiguous known owner identity',ambiguous)
# A new explicitly known child restricts its own /proc visibility; no elevation.
child_code="import ctypes,os,sys,json\nassert ctypes.CDLL(None).prctl(4,0,0,0,0)==0\nprint(json.dumps({'pid':os.getpid(),'uid':os.getuid(),'restricted_own_visibility':True}),flush=True)\nsys.stdin.buffer.readline()\n"
argv=[sys.executable,'-c',child_code];child=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);started=m.now()
try:
 line=child.stdout.readline();announcement=json.loads(line);identity=m.OWN.identity(child.pid);job={**identity,'role':'known F control child','state':'live'}
 test('actual-inaccessible-known-owner',lambda:m.OWN.assess(str(root),completion,[job]),'inaccessible or ambiguous known owner',{'argv':argv,'announcement':announcement,'known_jobs':[job]})
finally:
 out,err=child.communicate(b'finish\n',timeout=10)
 children.append({'argv':argv,'pid':child.pid,'started':started,'finished':m.now(),'exit':child.returncode,'stdout':line.decode()+out.decode(),'stderr':err.decode(),'joined':True});save()
assert child.returncode==0
scoped=m.OWN.assess(str(root),completion,[observer]);assert scoped['global_no_reference_assertion'] is False and '/proc/2389/cwd' in scoped['unknown_process_visibility_limit']
positive=m.inspect(str(root),want,allowed)
records.append({'name':'scoped-positive-after-fd-close','finished':m.now(),'passed':True,'scope':scoped,'observation':positive,'out_of_scope_failure_cannot_imply_global_clean':True});save()
(R/'stage-f/retirement-control-custody-v2.json').write_text(json.dumps({'root':str(root),'creation_receipt':'stage-f/retirement-control-creation-v2.json','final_snapshot':want,'observed':positive,'child_termination_evidence':'stage-f/retirement-controls-v2.json','all_known_children_joined':True,'retirement':'Only after creation/content/actual termination receipts are committed'},indent=2)+'\n')
print('PASS new own-lane H controls:11 specific refusals including actual own FD, missing/ambiguous completion and actual inaccessible known child; scoped positive after FD close; child joined exit0; no global-clean claim')
