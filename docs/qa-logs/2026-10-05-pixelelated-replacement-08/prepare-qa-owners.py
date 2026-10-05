from pathlib import Path
import ast,hashlib,json,re,subprocess,datetime
base=Path('/workspace/tmp');build=base/'pixelelated-m7-replacement-08';j=json.loads((build/'inputs.json').read_text());commit=j['distribution_commit'];digest=hashlib.sha256((build/'inputs.json').read_bytes()).hexdigest()
pairs=[('qa-09','qa-10'),('boot-qualification-01','boot-qualification-02'),('image-08','image-09'),('sweep-05','sweep-06'),('settings-07','settings-08'),('link-07','link-08'),('guest-07','guest-08'),('runtime-08','runtime-09'),('proxy-06','proxy-07'),('optins-06','optins-07'),('memory-06','memory-07'),('ui-08','ui-09'),('predecessor-04','predecessor-05'),('subset-03','subset-04'),('inventory-05','inventory-06'),('cloud-ui-02','cloud-ui-03'),('signin-ui-02','signin-ui-03'),('signin-1g-02','signin-1g-03')]
replace={'pixelelated-m7-replacement-07/build-attempt-02':'pixelelated-m7-replacement-08','m7-pixelelated-replacement07':'m7-pixelelated-replacement08','pixelelated-m7-replacement-07':'pixelelated-m7-replacement-08','replacement07':'replacement08','a2586374b7b565965fe0c644656e22ff3c0ec317':commit,'a2586374b7':commit[:10],'dcc242bbb3039559515b20ca395135af809fdb099d31b3710cf907c97c4d4e84':digest,'c75aa3fac967ba532fd9ba1c21fa10ca024e8bc1':j['emulationstation_commit']}
replace.update({'pixelelated-m7-'+a:'pixelelated-m7-'+b for a,b in pairs});pattern=re.compile('|'.join(re.escape(k) for k in sorted(replace,key=len,reverse=True)))
def rewrite(s):return pattern.sub(lambda m:replace[m.group()],s)
receipts=[]
for old,new in pairs:
 src=base/('pixelelated-m7-'+old);dst=base/('pixelelated-m7-'+new);assert not dst.exists(),dst;dst.mkdir();(dst/'artifacts').mkdir()
 if (src/'pair').is_dir():(dst/'pair').mkdir()
 paths=[]
 for line in (src/'harness.sha256').read_text().splitlines():
  wanted,name=line.split(None,1);p=Path(name.strip());p=p if p.is_absolute() else src/p;assert p.parent==src and hashlib.sha256(p.read_bytes()).hexdigest()==wanted,p
  if p.name in ['provenance.json','runtime07-dependency.json']:continue
  q=dst/p.name;data=p.read_bytes();q.write_bytes(data if b'\0' in data else rewrite(data.decode()).encode());q.chmod((p.stat().st_mode&0o777)|0o200);paths.append(q)
 if new in ['qa-10','ui-09']:
  p=dst/'es_lifecycle.py';p.write_text(Path('/tmp/pixelelated-es-lifecycle-guard.py').read_text());paths.append(p)
  if new=='qa-10':
   p=dst/'identity-frames.py';s=p.read_text();target="subprocess.run(v+['run',str(owner/'identity.steps'),'--outdir',str(owner/'artifacts'/('identity-'+phase))],check=True)";assert target in s
   s=s.replace(target,"from es_lifecycle import Lifecycle\nwith Lifecycle(['./tools/vm-pair','ssh','a'], owner/'artifacts'/('lifecycle-'+phase)):\n "+target);p.write_text(s)
  else:
   p=dst/'ui.py';s=p.read_text();target=" subprocess.run(v+['run',str(owner/'identity.steps') if walk=='identity' else str(owner/('m7-'+walk+'.steps')),'--outdir',str(out/walk)],check=True)";assert target in s
   s='from es_lifecycle import Lifecycle\n'+s.replace(target," with Lifecycle(ssh, out/(walk+'-lifecycle')):\n "+target);p.write_text(s)
 p=dst/'provenance.json';p.write_text(json.dumps({'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_owner':str(src),'source_harness_sha256':hashlib.sha256((src/'harness.sha256').read_bytes()).hexdigest(),'frozen_commit':commit,'input_manifest_sha256':digest,'state':'UNSTARTED','scope':'New independent owner. Preserve Back/Back Settings save; actual ES PID/start-tick continuity and failure journals added to identity and bilingual walks (#436). Other assertions unchanged. Historical results are not inherited.'},indent=2)+'\n');paths.append(p)
 for p in paths:
  if b'\0' not in p.read_bytes():
   s=p.read_text()
   if p.suffix=='.py' or p.name=='settings-modes-test':ast.parse(s)
   elif p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
 h=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in sorted(paths));(dst/'harness.sha256').write_text(h)
 for p in paths:p.chmod(0o500 if p.stat().st_mode&0o111 else 0o400)
 receipts.append({'owner':str(dst),'harness_sha256':hashlib.sha256(h.encode()).hexdigest(),'members':len(paths),'state':'UNSTARTED','copied_from':str(src)})
(build/'qa-owners.json').write_text(json.dumps(receipts,indent=2)+'\n');print('Prepared18 independent08 owners, source checks pass; none executed')
