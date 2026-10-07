from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json

old = Path('/workspace/tmp/pixelelated-m7-p4-build16-supplemental-02')
owner = Path('/workspace/tmp/pixelelated-m7-p4-build16-selected-content-01')
assert not owner.exists()
owner.mkdir(mode=0o700)
(owner / 'proof').mkdir(mode=0o700)
for name in ['run.py', 'verify-inputs.py']:
    (owner / name).write_bytes((old / name).read_bytes())
prior = (old / 'extra-boundaries.py').read_text()
header = prior[:prior.index('class Extra(m.Proof):')]
tail = prior[prior.index('  for name,action in cases:'):]
body = r'''class Extra(m.Proof):
 def selected_content(self,kind):
  self.audit_current('')
  system='unsupported_qa' if kind=='unsupported' else 'bios' if kind=='bios' else 'gb'
  filename='AuditSelected-'+kind+('.bin' if kind=='bios' else '.gb')
  cloud_path=('ROMs/' if kind=='tiered' else '')+system+'/'+filename
  payload=(('candidate16 selected '+kind+' witness\n')*257).encode()
  target='/storage/roms/'+system+'/'+filename
  self.on('a','test ! -e '+shlex.quote(target))
  if kind=='unsupported': self.on('a','mkdir -p /storage/roms/unsupported_qa')
  self.put(cloud_path,payload);self.put('Photos/unrelated.txt',b'not game content\n')
  before=self.audit_snapshot()
  scan=self.on('a','/usr/bin/cloud_content_restore --scan')
  rows=[line.split('|') for line in scan.stdout.splitlines() if line.startswith(system+'|')]
  matches=[row for row in rows if row[1]==str(len(payload))]
  require(len(matches)==1 and matches[0][2]==('0' if kind=='unsupported' else '1'),'installed capability row incorrect')
  require(not re.search(r'^Photos\|',scan.stdout,re.M),'unrelated folder offered as content')
  require(self.audit_snapshot()==before,'scan changed original state')
  result={'kind':kind,'cloud_path':cloud_path,'row':matches[0],'before':before,'target':target,'sha256':hashlib.sha256(payload).hexdigest()}
  if kind!='unsupported':
   self.on('a','/usr/bin/cloud_content_restore --set-systems '+system)
   self.on('a','/usr/bin/cloud_content_restore --selected')
   actual=self.on('a','sha256sum '+shlex.quote(target)).stdout.split()[0]
   require(actual==result['sha256'],'actual selected restore bytes differ')
   result['restored_sha256']=actual
  else:
   self.on('a','test ! -e '+shlex.quote(target));result['not_restored']=True
  require(self.audit_snapshot()==before,'selection/restore changed source cloud or pointers')
  result['after']=self.audit_snapshot();save(self.logs/(self.case+'-selected.json'),result)
 def run_cases(self):
  cases=[('PL001-installed-selected-'+kind,lambda k=kind:self.selected_content(k)) for kind in ['legacy','tiered','bios','unsupported']]
'''
source = header.replace('import argparse,', 'import re,argparse,') + body + tail
ast.parse(source)
(owner / 'extra-boundaries.py').write_text(source)
(owner / 'provenance.json').write_text(json.dumps(dict(
    prepared_utc=datetime.now(timezone.utc).isoformat(), issue=467,
    scope='Actual installed selected-content restore from legacy and tiered root, BIOS and unsupported-system control. Complements the accepted EN/FR root chooser/capability frames.',
    parent=str(old), installed_scripts_replaced=False,
    candidate='ee014909137e03706e0b3020b8396be589aaa705',
    source_tree='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16',
    order='Only after cloud02 terminal and actual guest/backend cleanup.'), indent=2)+'\n')
seals = {p: h for p,h in json.loads((old/'seal.json').read_text()).items() if not p.startswith(str(old)+'/')}
for p in owner.iterdir():
    if p.is_file():seals[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
assert len(seals)==212
for name,digest in seals.items():
    assert hashlib.sha256((Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')/name).read_bytes()).hexdigest()==digest,name
(owner/'seal.json').write_text(json.dumps(seals,indent=2)+'\n')
print(owner, 'prepared; 4 installed cases, 212 verified input seals')
