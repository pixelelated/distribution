from pathlib import Path
import hashlib,importlib.machinery,importlib.util,json,subprocess
owner=Path(__file__).resolve().parent
loader=importlib.machinery.SourceFileLoader('collision_boundaries',str(owner/'boundaries.py'))
spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
original=m.Proof.collision
def collision(self):
 original(self)
 self.reset()
 self.put('ROCKNIX/Saves/gb/A.srm',b'local progress\n')
 self.put('ROCKNIX/Content/ROMs/gb/A.gb',b'old content\n')
 self.put('pixelelated/Content/ROMs/gb/A.gb',b'foreign content\n')
 before=self.audit_snapshot()
 ref='ed5a6a51f5974deec8748fbf0dbd2f4984b690f5'
 old=subprocess.check_output(['git','-C',str(self.tree),'show',ref+':'+m.SOURCES+'/cloud_migrate_layout'])
 path=m.QA+'/pre-fix-cloud-migrate-layout'
 self.on('a','cat > '+path+'; chmod 755 '+path,data=old.decode())
 result=self.on('a',path+' --apply',allowed=None)
 after=self.audit_snapshot()
 record=self.on('a','test -s /storage/.config/cloud-layout-migration.json',allowed=None).returncode==0
 m.require(result.returncode!=0 and '>>> why THE NEW FOLDER ALREADY HAS FILES IN IT' in result.stdout,'old control did not reach the intended collision refusal')
 preserved=after==before and not record
 m.require(not preserved,'actual old script unexpectedly meets the stronger refusal invariant')
 m.require(record and after['cloud']!=before['cloud'],'old refusal must reproduce partial tier advancement and a created record')
 m.require(set(before['cloud'].values()).issubset(set(after['cloud'].values())),'old control lost original bytes')
 m.require((self.data/'pixelelated/Content/ROMs/gb/A.gb').read_bytes()==b'foreign content\n','old control overwrote foreign content')
 m.save(self.logs/'old-collision-negative-control.json',{'ref':ref,'source_sha256':hashlib.sha256(old).hexdigest(),'returncode':result.returncode,'before':before,'after':after,'record_created':record,'stronger_invariant':preserved,'scope':'Actual predecessor script in private guest QA path; installed binaries unchanged.'})
 print('PASS actual predecessor collision refusal rejected by unchanged-state predicate',flush=True)
 self.reset()
m.Proof.collision=collision
raise SystemExit(m.main())
