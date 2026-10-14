from pathlib import Path
import ast,hashlib,json,shutil,subprocess,argparse
p=argparse.ArgumentParser();p.add_argument('--variant',choices=['baseline','candidate'],required=True);p.add_argument('--owner',type=Path,required=True);p.add_argument('--vnc',type=int,required=True);a=p.parse_args()
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');q=Path('/workspace/tmp/pix583-current-native-20261014-02/qualification-inputs');src=Path('/workspace/tmp/pix588-'+a.variant+'-service-20261014-01');packet=Path('/workspace/tmp/pix588-'+a.variant+'-native-service-20261014-02');assert not packet.exists();shutil.copytree(src,packet)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
b=json.loads((packet/'bindings.json').read_text());proof=json.loads((q/'native-provenance.json').read_text());assert proof['source_pins_verified'] is True
b['libraries']['rchash']['sha256']=proof['elf']['sha256'];b['source_pins_verified']=True
b['native_provenance']={'file':'native-provenance.json','sha256':sha(q/'native-provenance.json'),'receipt':'native-build-receipt.json','receipt_sha256':sha(q/'native-build-receipt.json'),'scope':'Fresh current native source linkage; exact VM overlay; runtime is separately measured'}
for name in ('native-provenance.json','native-build-receipt.json'):shutil.copyfile(q/name,packet/name)
dump(packet/'bindings.json',b)
helper='''from pathlib import Path
import hashlib,json
def verify(packet,binding):
 def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
 row=binding['native_provenance'];assert row['file']=='native-provenance.json' and row['receipt']=='native-build-receipt.json'
 p=packet/row['file'];r=packet/row['receipt'];assert sha(p)==row['sha256'] and sha(r)==row['receipt_sha256']
 proof=json.loads(p.read_text());receipt=json.loads(r.read_text());assert proof['source_pins_verified'] is True
 assert receipt['status']=='CURRENT_SOURCE_BUILD_BOUND_VM_UNRUN' and receipt['source']['all_original_sources_unchanged'] is True
 assert receipt['pins']=={'raofflineproxy':'c7ebd1b6e777f3751ff0ecdf8aba54045844e00d','raofflineproxy-rcheevos':'1433173220a7eaede6a9ed7a18e94117be1821e0','raofflineproxy-libchdr':'607694ca0812edfc9cc2030c64634fc2393668de'}
 assert proof['build_receipt']=={'path':row['receipt'],'bytes':r.stat().st_size,'sha256':sha(r)}
 elf=Path(binding['libraries']['rchash']['path']);assert sha(elf)==proof['elf']['sha256']==receipt['elf']['sha256']==binding['libraries']['rchash']['sha256']
 assert elf.stat().st_size==proof['elf']['bytes']==receipt['elf']['bytes']
 return {'source_pins_verified':True,'receipt_sha256':sha(r),'elf_sha256':sha(elf),'pins':receipt['pins'],'scope':'Current native source linkage; source-staged disposable overlay, not final installed image'}
'''
(packet/'bootstrap/native_provenance_check.py').write_text(helper)
namespace={};exec(compile(helper,'native_provenance_check.py','exec'),namespace);test_binding=json.loads(json.dumps(b));test_binding['libraries']['rchash']['path']=str(q/'libraproxy_rchash.so');assert namespace['verify'](packet,test_binding)['source_pins_verified'] is True
f=packet/'bootstrap/sitecustomize.py';t=f.read_text();needle="    assert os.environ['RAOFFLINEPROXY_CONFIG_DIR'] == str(state)\n";assert t.count(needle)==1;t=t.replace(needle,"    from native_provenance_check import verify\n    native_provenance = verify(packet, binding)\n"+needle);assert t.count('source_pins_verified=False')==1;t=t.replace('source_pins_verified=False',"source_pins_verified=native_provenance['source_pins_verified']");f.write_text(t)
f=packet/'run.py';t=f.read_text();needle="        binding = json.loads((PACKET / 'bindings.json').read_text())\n";assert t.count(needle)==1;t=t.replace(needle,needle+"        REPORT['native_provenance'] = module('pix588_native_provenance', PACKET / 'bootstrap/native_provenance_check.py').verify(PACKET, binding)\n        REPORT['source_pins_verified'] = REPORT['native_provenance']['source_pins_verified']\n");needle="'source_pins_verified': False, 'libraries': binding['libraries']";assert t.count(needle)==1;t=t.replace(needle,"'source_pins_verified': REPORT['source_pins_verified'], 'libraries': binding['libraries']");f.write_text(t)
seal=json.loads((packet/'runner-seal.json').read_text());seal['bootstrap/startup_gate.py']=sha(packet/'bootstrap/startup_gate.py');seal['bootstrap/native_provenance_check.py']=sha(packet/'bootstrap/native_provenance_check.py');seal['native-provenance.json']=sha(packet/'native-provenance.json');seal['native-build-receipt.json']=sha(packet/'native-build-receipt.json')
for name in seal:seal[name]=sha(packet/name)
dump(packet/'runner-seal.json',seal)
for f in packet.rglob('*.py'):ast.parse(f.read_bytes())
files=[f for f in sorted(packet.rglob('*')) if f.is_file() and f.name!='SHA256SUMS'];(packet/'SHA256SUMS').write_text(''.join(sha(f)+'  '+str(f.relative_to(packet))+'\n' for f in files))
prepared=Path('/workspace/tmp/pix583-native-prepared-20261014-02' if a.variant=='baseline' else '/workspace/tmp/pix588-candidate-prepared-20261014-01')
rows=[{'path':str(f),'destination':'service-prepared/'+str(f.relative_to(prepared)),'sha256':sha(f)} for f in sorted(prepared.rglob('*')) if f.is_file() and (f.suffix=='.py' or f==prepared/'source.json')]
rows +=[{'path':str(f),'destination':'service-packet/'+str(f.relative_to(packet)),'sha256':sha(f)} for f in sorted(packet.rglob('*')) if f.is_file()]
rows +=[{'path':str(q/'libraproxy_rchash.so'),'destination':'native/libraproxy_rchash.so','sha256':sha(q/'libraproxy_rchash.so')}]
work=Path('/workspace/tmp/pix588-'+a.variant+'-host-prep-20261014-02');work.mkdir();dump(work/'inputs.json',{'files':rows,'variant':a.variant,'source_packet_manifest':sha(packet/'SHA256SUMS')})
guest=Path('/workspace/tmp/pix583-service-vm-20261014-05/run-guest.sh').read_text().replace('run05','run588')
overlay='''python3 -I -S -B -c 'from pathlib import Path; import hashlib,json; p=Path("/usr/lib/libraproxy_rchash.so"); assert not any(x.split()[4]==str(p) for x in Path("/proc/self/mountinfo").read_text().splitlines()); Path("/tmp/pix-output/service/native-before.json").write_text(json.dumps({"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size})+"\\n")'
mount --bind /tmp/pix-input/native/libraproxy_rchash.so /usr/lib/libraproxy_rchash.so
mount --make-private /usr/lib/libraproxy_rchash.so
python3 -I -S -B -c 'from pathlib import Path; import hashlib,json; p=Path("/usr/lib/libraproxy_rchash.so"); proof=json.loads(Path("/tmp/pix-input/service-packet/native-provenance.json").read_text()); assert hashlib.sha256(p.read_bytes()).hexdigest()==proof["elf"]["sha256"]; assert p.stat().st_size==proof["elf"]["bytes"]; Path("/tmp/pix-output/service/native-overlay-mountinfo.txt").write_text(Path("/proc/self/mountinfo").read_text())'
/lib64/ld-linux-x86-64.so.2 --list /usr/lib/libraproxy_rchash.so > /tmp/pix-output/service/native-loader-list.txt 2>&1
'''
guest=guest.replace('mkdir /run/pix583-service-packet',overlay+'mkdir /run/pix583-service-packet',1)
needle='umount /run/pix583-service-packet\n';assert guest.count(needle)==1
guest=guest.replace(needle,needle+'''umount /usr/lib/libraproxy_rchash.so
python3 -I -S -B -c 'from pathlib import Path; import hashlib,json; b=json.loads(Path("/tmp/pix-output/service/native-before.json").read_text()); p=Path("/usr/lib/libraproxy_rchash.so"); assert hashlib.sha256(p.read_bytes()).hexdigest()==b["sha256"]; Path("/tmp/pix-output/service/native-restored.json").write_text(json.dumps(b)+"\\n")'
''')
(work/'run-guest.sh').write_text(guest)
subprocess.run(['sh','-n',str(work/'run-guest.sh')],check=True)
subprocess.run(['python3','-I',str(repo/'docs/qa-logs/2026-10-14-independent-format-runtime/coordinator/pix-m7-new-vm.py'),'--owner',str(a.owner),'--inputs',str(work/'inputs.json'),'--guest-script',str(work/'run-guest.sh'),'--issue','588','--stage','proxy-startup-'+a.variant,'--guest-seconds','350','--vnc',str(a.vnc)],check=True)
f=a.owner/'vm-lifecycle.py';t=f.read_text();needle='  ready={';assert t.count(needle)==1;t=t.replace(needle,(repo/'docs/qa-logs/2026-10-14-proxy-service-runtime/coordinator/unified-boot-insertion.py.txt').read_text()+needle);ast.parse(t);f.write_text(t)
plan=json.loads((a.owner/'retention-plan.json').read_text());plan['builds'][0]['basis']+=' Actual main/systemd startup causal '+a.variant+'; private unified-cgroup reboot within same900s clock; real15s monitor, unchanged240/272/280s guards; source-bound current native overlay restored. Expected original result '+('1 for causal failure' if a.variant=='baseline' else '0')+'.'
for x in plan['builds'][0]['evidence']:x['sha256']=sha(Path(x['path']))
dump(a.owner/'retention-plan.json',plan)
print(json.dumps({'variant':a.variant,'packet':str(packet),'packet_sha256':sha(packet/'SHA256SUMS'),'native_elf':proof['elf'],'owner':str(a.owner)}))
