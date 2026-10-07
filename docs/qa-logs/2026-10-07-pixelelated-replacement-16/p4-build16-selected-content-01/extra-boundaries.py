"""Additional installed acceptance for #471; same isolated pair ownership as the frozen runner."""
from pathlib import Path
import re,argparse,hashlib,importlib.machinery,importlib.util,json,shlex,socket,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--tree',type=Path,required=True);ap.add_argument('--image',type=Path,required=True);ap.add_argument('--build-id',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
source=a.tree/'tools/pixelelated-vm-cloud-boundaries'
loader=importlib.machinery.SourceFileLoader('frozen_boundaries',str(source));spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
Q=m.QA;C=m.CONF;require=m.require;save=m.save
class Extra(m.Proof):
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
  for name,action in cases:
   self.case=name;print('START '+name,flush=True)
   try:
    self.reset();action();self.results.append({'case':name,'status':'PASS'});print('PASS '+name,flush=True)
   except (AssertionError,subprocess.SubprocessError,OSError,StopIteration) as e:
    self.results.append({'case':name,'status':'FAIL','reason':str(e)});print('FAIL '+name+': '+str(e),flush=True)
   save(self.logs/'results.json',self.results)
  self.case='final-custody'
  for key,value in self.original_scripts.items():
   guest,script=key.split('/');require(self.on(guest,'sha256sum /usr/bin/'+script).stdout.split()[0]==value,'installed script changed')
  return 0 if all(row['status']=='PASS' for row in self.results) else 1
proof=Extra(a)
try:proof.start();result=proof.run_cases()
finally:proof.cleanup()
sys.exit(result)
