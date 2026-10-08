from pathlib import Path
import subprocess,json,hashlib,time
O=Path(__file__).parent;B=O.parent;R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17');G=B/'guest03';data=B/'backend/data'
ssh=['ssh','-i',str(G/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
def guest(code,label):
 q=subprocess.run(ssh+['bash -s'],input=code,capture_output=True,text=True,timeout=45);(O/(label+'.stdout')).write_text(q.stdout);(O/(label+'.stderr')).write_text(q.stderr);q.check_returncode();return q.stdout
def save(n,v):(O/(n+'.json')).write_text(json.dumps(v,indent=2)+'\n')
def snapshot():return {str(p.relative_to(data)):({'kind':'file','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} if p.is_file() else {'kind':'directory'}) for p in sorted(data.rglob('*'))}
def walk(n,s):
 p=O/(n+'.steps');p.write_text(s)
 q=subprocess.run(['python3',str(R/'tools/vm-visual-qa'),'--monitor','/tmp/pix508-cf10-17-mon.sock','run',str(p),'--outdir',str(O/n)],capture_output=True,text=True,timeout=90);(O/(n+'.log')).write_text(q.stdout+q.stderr);q.check_returncode()
witness='set -e\ncat /proc/sys/kernel/random/boot_id\nsha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf /usr/bin/emulationstation /usr/bin/cloud_setup /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo\n'
previous=B/'ui-create01'
before=(previous/'before.stdout').read_text()
initial=json.loads((previous/'cloud-before.json').read_text())
assert guest(witness,'before-resume')==before
assert (previous/'after-decline.stdout').read_text()==before
walk('result','settle\nshot saves-only-result\n')
after=snapshot();save('cloud-after-create',after)
assert all(after[k]==v for k,v in initial.items()),'unrelated data changed'
assert (data/'pixelelated/Saves/savefiles').is_dir()
assert (data/'pixelelated/Saves/savestates').is_dir()
assert (data/'pixelelated/Saves/screenshots').is_dir()
assert not (data/'pixelelated/Backups').exists() and not (data/'pixelelated/Content').exists()
assert all(k in initial or k in {'pixelelated','pixelelated/.layout'} or k.startswith('pixelelated/Saves') for k in after),after
assert (data/'pixelelated/.layout').read_text()=='layout=2\n'
assert any(p.is_file() and 'README' in p.name for p in (data/'pixelelated/Saves').rglob('*'))
assert guest(witness,'after-create')==before,'creation changed configuration'
# Repeat through the same real UI; result Back returns to CREATE FOLDERS.
walk('repeat','key z\nsettle\nshot prior-selection\nkey x\nsettle\nshot repeated-confirmation\nkey x\nwait 4\nsettle\nshot repeated-result\n')
assert snapshot()==after,'repeated creation changed existing bytes or structure'
assert guest(witness,'after-repeat')==before
result=json.loads(guest('/usr/bin/cloud_setup --validate-folders saves cf10-created','validation'))
assert result['complete'] and len(result['categories'])==1 and result['categories'][0]['state']=='empty',result
save('result',{'passed':True,'decline_unchanged_prior_partial_proof':'ui-create01; aggregate1 from unsupported sleep step after confirmation','selected_only':'saves','idempotent':True,'configuration_unchanged':True,'validation':result,'source_overlays':False,'frame_review':'pending','frames':{str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest() for p in O.rglob('*.png')}})
print('PASS native saves-only confirmation/create; decline and unrelated payload preserved; repeat idempotent; frames await review',flush=True)
