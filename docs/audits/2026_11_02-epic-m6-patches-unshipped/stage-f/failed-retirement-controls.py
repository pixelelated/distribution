#!/usr/bin/env python3
"""New F controls for the H metadata/retirement guard; no production root mutation."""
import copy,datetime,hashlib,importlib.util,json,os,pathlib,sys,tempfile
R=pathlib.Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('retire',R/'tools/retirement.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
root=pathlib.Path(tempfile.mkdtemp(prefix='f-retirement-controls-',dir=m.BASE));allowed={str(root)}
created={'at':m.now(),'root':str(root),'pid':os.getpid(),'uid':os.getuid(),'cwd':os.getcwd(),'argv':sys.argv,'root_identity':m.meta(root.lstat()),'purpose':'new F retirement guard metadata fixture only'}
(R/'stage-f/retirement-control-creation.json').write_text(json.dumps(created,indent=2)+'\n')
f=root/'a.txt';f.write_bytes(b'owned F control\n')
def expected():return {'a.txt':{'type':'file','mode':oct(f.stat().st_mode&0o777),'sha256':m.sha(f.read_bytes()),'bytes':f.stat().st_size}}
want=expected();records=[]
def test(name,fn,reason):
 start=m.now()
 try:fn()
 except (AssertionError,OSError) as e:
  assert reason in str(e),(name,type(e).__name__,str(e))
  records.append({'name':name,'started':start,'finished':m.now(),'function':'retirement.inspect/permitted','actual_exception':type(e).__name__,'actual_message':str(e),'expected_refusal':reason,'passed':True})
 else:raise AssertionError('guard did not refuse '+name)
f.write_bytes(b'changed\n');test('changed-content',lambda:m.inspect(str(root),want,allowed),'content snapshot mismatch');f.write_bytes(b'owned F control\n')
f.unlink();f.symlink_to('target.txt');(root/'target.txt').write_bytes(b'owned target\n');test('symlink-substitution',lambda:m.inspect(str(root),want,allowed),'symlink or special-file substitution');f.unlink();(root/'target.txt').unlink();f.write_bytes(b'owned F control\n')
test('mount-crossing-metadata-control',lambda:m.inspect(str(root),want,allowed,device=root.stat().st_dev+1),'mount crossing')
test('owner-mismatch-metadata-control',lambda:m.inspect(str(root),want,allowed,owner_uid=os.getuid()+1),'owner mismatch')
prior=m.inspect(str(root),want,allowed)['nodes'];wrong=copy.deepcopy(prior);wrong['.']['ino']+=1
test('changed-identity',lambda:m.inspect(str(root),want,allowed,prior=wrong),'fresh identity/metadata changed')
test('unknown-root',lambda:m.inspect(str(m.BASE/'not-owned'),{},allowed),'unknown or unconfined path')
test('durable-receipt-root',lambda:m.inspect(str(m.BASE/'stage-d-publication'),{},{str(m.BASE/'stage-d-publication')}),'cache/receipt path protected')
fd=os.open(f,os.O_RDONLY)
try:
 live=m.live_references(allowed);assert any(x['pid']==os.getpid() for x in live)
 test('live-owner-reference',lambda:m.inspect(str(root),want,allowed,live=live),'live owner reference')
finally:os.close(fd)
positive=m.inspect(str(root),want,allowed);records.append({'name':'positive','function':'retirement.inspect','finished':m.now(),'passed':True,'root':str(root),'nodes':positive['nodes'],'content_snapshot_sha256':positive['content_snapshot_sha256']})
(R/'stage-f/retirement-controls.json').write_text(json.dumps({'program_sha256':m.sha((R/'tools/retirement.py').read_bytes()),'controller_sha256':m.sha(pathlib.Path(__file__).read_bytes()),'records':records,'limits':'mount/owner negatives inject mismatching expected metadata; no mount/chown action. Actual content/symlink/identity/unknown/durable-path/live-fd predicates exercised. No production path mutation.'},indent=2)+'\n')
(R/'stage-f/retirement-control-custody.json').write_text(json.dumps({'root':str(root),'creation_receipt':'stage-f/retirement-control-creation.json','final_snapshot':want,'observed':positive,'retirement':'Only after these receipts are committed, using the same bounded H path.'},indent=2)+'\n')
print('PASS new H guard:8 specific refusals and actual positive; tiny F scratch retained with creation/final custody; no production deletion')
