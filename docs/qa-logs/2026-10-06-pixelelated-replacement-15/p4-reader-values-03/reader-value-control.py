from pathlib import Path
import hashlib,importlib.machinery,importlib.util,json,subprocess
owner=Path(__file__).resolve().parent
loader=importlib.machinery.SourceFileLoader('reader_boundaries',str(owner/'boundaries.py'))
spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
original=m.Proof.audit_reader
def reader(self,kind):
 original(self,kind)
 if kind!='escaped':return
 expected=json.loads((self.logs/(self.case+'-value-selection.json')).read_text())
 old=subprocess.check_output(['git','-C',str(self.tree),'show','7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2:'+m.SOURCES+'/cloud_scan'])
 path=m.QA+'/pre-fix-cloud-scan';self.on('a','cat > '+path+'; chmod 755 '+path,data=old.decode())
 before=self.audit_snapshot()
 result=self.on('a',path,allowed=None)
 facts=dict(line.split('=',1) for line in self.on('a','cat /storage/.cache/cloud_sync/scan/settings',allowed=None).stdout.splitlines() if '=' in line)
 canonical=lambda f: f.get('MINE')==expected['expected_archive'] and f.get('SOURCE','').rstrip('/')==self.remote+expected['expected_directory']+'/'+self.on('a','/usr/bin/cloud_device_id').stdout.strip()
 m.require(not canonical(facts),'pre-fix reader unexpectedly met the corrected parsed-value predicate')
 m.require(self.audit_snapshot()==before,'old reader control mutated cloud/settings')
 self.on('a','/usr/bin/cloud_scan')
 corrected=dict(line.split('=',1) for line in self.on('a','cat /storage/.cache/cloud_sync/scan/settings').stdout.splitlines() if '=' in line)
 m.require(canonical(corrected),'corrected reader did not recover exact value selection after old-source control')
 m.require(self.audit_snapshot()==before,'corrected retry mutated cloud/settings')
 m.save(self.logs/'old-reader-negative-control.json',{'ref':'7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','source_sha256':hashlib.sha256(old).hexdigest(),'old_rc':result.returncode,'old_scan':facts,'corrected_scan':corrected,'expected':expected,'scope':'Actual predecessor scanner in a private guest QA path; installed binaries remain unchanged. This is not an old installed image.'})
 print('PASS actual predecessor reader rejected by exact-value predicate',flush=True)
m.Proof.audit_reader=reader
raise SystemExit(m.main())
