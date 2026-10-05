from pathlib import Path
import ast,hashlib,json,re,subprocess,datetime
base=Path('/workspace/tmp');build=base/'pixelelated-m7-replacement-09';j=json.loads((build/'inputs.json').read_text());commit=j['distribution_commit'];digest=hashlib.sha256((build/'inputs.json').read_bytes()).hexdigest();oldj=json.loads((base/'pixelelated-m7-replacement-08/inputs.json').read_text())
pairs=[('qa-10','qa-11'),('boot-qualification-02','boot-qualification-03'),('image-09','image-10'),('sweep-06','sweep-07'),('settings-08','settings-09'),('link-08','link-09'),('guest-08','guest-09'),('runtime-09','runtime-10'),('proxy-07','proxy-08'),('optins-07','optins-08'),('memory-07','memory-08'),('ui-09','ui-10'),('predecessor-05','predecessor-06'),('subset-04','subset-05'),('inventory-06','inventory-07'),('cloud-ui-03','cloud-ui-04'),('signin-ui-03','signin-ui-04'),('signin-1g-03','signin-1g-04')]
replace={'m7-pixelelated-replacement08':'m7-pixelelated-replacement09','pixelelated-m7-replacement-08':'pixelelated-m7-replacement-09','replacement08':'replacement09',oldj['distribution_commit']:commit,oldj['distribution_commit'][:10]:commit[:10],hashlib.sha256((base/'pixelelated-m7-replacement-08/inputs.json').read_bytes()).hexdigest():digest,'frozen57cbc':'frozen'+commit[:10]};replace.update({'pixelelated-m7-'+a:'pixelelated-m7-'+b for a,b in pairs});pattern=re.compile('|'.join(re.escape(k) for k in sorted(replace,key=len,reverse=True)))
def rewrite(s):return pattern.sub(lambda m:replace[m.group()],s)
receipts=[]
for old,new in pairs:
 src=base/('pixelelated-m7-'+old);dst=base/('pixelelated-m7-'+new);assert not dst.exists(),dst;dst.mkdir();(dst/'artifacts').mkdir()
 if (src/'pair').is_dir():(dst/'pair').mkdir()
 paths=[]
 for line in (src/'harness.sha256').read_text().splitlines():
  wanted,name=line.split(None,1);p=Path(name.strip());p=p if p.is_absolute() else src/p;assert p.parent==src and hashlib.sha256(p.read_bytes()).hexdigest()==wanted,p
  if p.name=='provenance.json':continue
  q=dst/p.name;data=p.read_bytes();q.write_bytes(data if b'\0' in data else rewrite(data.decode()).encode());q.chmod((p.stat().st_mode&0o777)|0o200);paths.append(q)
 if new=='qa-11':
  p=dst/'proxy-identity.py';p.write_text('''"""Execute only the installed module against temporary synthetic OS fixtures."""
from pathlib import Path
import json,tempfile
from raofflineproxy import config
assert str(Path(config.__file__).resolve()).startswith('/usr/lib/')
assert config.running_on_rocknix(), 'actual pixelelated OS must be recognized'
rows=[]
original_release=config.OS_RELEASE_PATH;original_settings=config.DEFAULT_ROCKNIX_SYSTEM_CFG
try:
 with tempfile.TemporaryDirectory(prefix='qa-proxy-identity-') as temporary:
  root=Path(temporary);release=root/'os-release';settings=root/'system.cfg';settings.touch()
  config.OS_RELEASE_PATH=release;config.DEFAULT_ROCKNIX_SYSTEM_CFG=settings
  for record,expected in [('OS_NAME="ROCKNIX"',True),('OS_NAME="pixelelated"',True),('OS_NAME="RASTERATOPS"',False),('# OS_NAME="ROCKNIX"',False),('PREVIOUS_OS_NAME="ROCKNIX"',False)]:
   release.write_text(record+'\\n');actual=config.running_on_rocknix();assert actual==expected,(record,actual)
   if expected:assert config.detect_rocknix_system_cfg()==str(settings)
   rows.append({'record':record,'recognized':actual})
finally:
 config.OS_RELEASE_PATH=original_release;config.DEFAULT_ROCKNIX_SYSTEM_CFG=original_settings
print(json.dumps({'passed':True,'installed_module':config.__file__,'actual_os_recognized':True,'cases':rows}))
''');paths.append(p)
  p=dst/'check-payload.py';s=p.read_text();s+='''\nproxy_code = (owner / 'proxy-identity.py').read_text()
proxy_result = json.loads(guest("python3 - <<'PROXY_IDENTITY'\\n" + proxy_code + "\\nPROXY_IDENTITY"))
assert proxy_result['passed']
(owner / 'artifacts' / ('proxy-identity-' + sys.argv[1] + '.json')).write_text(json.dumps(proxy_result, indent=2) + '\\n')
print('PASS ' + sys.argv[1] + ' installed proxy identities and account discovery')
''';p.write_text(s)
 p=dst/'provenance.json';p.write_text(json.dumps({'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_owner':str(src),'source_harness_sha256':hashlib.sha256((src/'harness.sha256').read_bytes()).hexdigest(),'frozen_commit':commit,'input_manifest_sha256':digest,'state':'UNSTARTED','scope':'New independent09 owner; original assertions and lifecycle guards retained, bindings updated. QA11 additionally verifies the installed proxy recognizes only supported OS identities and discovers the shared account-settings layout. Historical results are not inherited.'},indent=2)+'\n');paths.append(p)
 for p in paths:
  if b'\0' not in p.read_bytes():
   s=p.read_text()
   if p.suffix=='.py' or p.name=='settings-modes-test':ast.parse(s)
   elif p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
 h=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in sorted(paths));(dst/'harness.sha256').write_text(h)
 for p in paths:p.chmod(0o500 if p.stat().st_mode&0o111 else 0o400)
 receipts.append({'owner':str(dst),'harness_sha256':hashlib.sha256(h.encode()).hexdigest(),'members':len(paths),'state':'UNSTARTED','copied_from':str(src)})
(build/'qa-owners.json').write_text(json.dumps(receipts,indent=2)+'\n');print('Prepared18 independent09 owners; all inputs parse; none executed')
