from pathlib import Path
import subprocess,json,time,hashlib,shlex,os
P=Path('/workspace/tmp/pixelelated-m7-identity-ui02')
R=Path('/workspace/repos/rocknix.worktrees/m7-p5-build-identity')
VM=Path('/workspace/tmp/pixelelated-m7-identity-01')
opts=['-i',str(VM/'qa-key'),'-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=3']
def ssh(s,timeout=40,check=True):return subprocess.run(['ssh',*opts,'-p','10292','root@127.0.0.1',s],check=check,capture_output=True,text=True,timeout=timeout)
def copy(src,dest):subprocess.run(['scp','-q',*opts,'-P','10292',str(src),'root@127.0.0.1:'+dest],check=True,timeout=20)
def visual(*args):subprocess.run([str(R/'tools/vm-visual-qa'),'--monitor','/tmp/pix530-01-mon.sock',*args],check=True,timeout=200)
def walk(name):visual('run',str(P/'information.steps'),'--outdir',str(P/name))
for _ in range(120):
 try:
  if json.loads(ssh('curl -fsS http://127.0.0.1:1234/isIdle').stdout)==[True]:break
 except (subprocess.CalledProcessError,ValueError):pass
 time.sleep(1)
else:raise RuntimeError('frontend idle timeout')
ssh('umount /etc/os-release; umount /usr/bin/rocknix-info')
baseline=ssh('rocknix-info --full',check=False);assert baseline.returncode==127
(P/'baseline-script.json').write_text(json.dumps({'returncode':baseline.returncode,'stdout':baseline.stdout,'stderr':baseline.stderr},indent=2)+'\n')
original=ssh('cat /etc/os-release').stdout;(P/'original-os-release.txt').write_text(original)
protected=ssh('sha256sum /storage/.config/system/configs/system.cfg /storage/.config/emulationstation/es_settings.cfg').stdout;(P/'protected-before.txt').write_text(protected)
walk('before')
source=R/'projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info'
copy(source,'/tmp/pix530-rocknix-info');ssh('chmod 755 /tmp/pix530-rocknix-info; mount --bind /tmp/pix530-rocknix-info /usr/bin/rocknix-info')
env=os.environ.copy();env.update(OS_VERSION='0.0.1',BUILD_TIMESTAMP='20261009T231500Z')
cmd='. config/build-identity; pixelelated_build_identity || exit $?; python3 -c \'import json,os;print(json.dumps({k:os.environ[k] for k in ("RELEASE_VERSION","BUILD_VERSION","BUILD_DATE","BUILD_TIMESTAMP","BUILD_DIRTY","GIT_HASH","OS_BUILD")}))\''
a=json.loads(subprocess.check_output(['bash','-c',cmd],cwd=R,env=env,text=True));(P/'derived-identity.json').write_text(json.dumps(a,indent=2)+'\n')
updates={'OS_VERSION':a['RELEASE_VERSION'],'VERSION_ID':a['RELEASE_VERSION'],'BUILD_VERSION':a['BUILD_VERSION'],'BUILD_DATE':a['BUILD_DATE'],'BUILD_TIMESTAMP':a['BUILD_TIMESTAMP'],'BUILD_DIRTY':a['BUILD_DIRTY'],'BUILD_ID':a['GIT_HASH'],'OS_BUILD':a['OS_BUILD']}
metadata='\n'.join(line for line in original.splitlines() if line.split('=',1)[0] not in updates)+'\n'+''.join(k+'="'+v+'"\n' for k,v in updates.items())
(P/'new-os-release.txt').write_text(metadata);copy(P/'new-os-release.txt','/tmp/pix530-os-release');ssh('mount --bind /tmp/pix530-os-release /etc/os-release')
new_result=ssh('rocknix-info --full',check=False);assert new_result.returncode==baseline.returncode
actual=new_result.stdout;(P/'new-information.txt').write_text(actual)
assert 'VERSION: 0.0.1-dev\n' in actual and 'BUILD ID: 2026-10-09 23:15:00Z / '+a['GIT_HASH'][:12] in actual and 'community' not in actual
walk('new-identity')
ssh('umount /etc/os-release')
legacy_result=ssh('rocknix-info --full',check=False);assert legacy_result.returncode==baseline.returncode
legacy=legacy_result.stdout;(P/'legacy-information.txt').write_text(legacy)
assert 'VERSION: 0.0.1\n' in legacy and 'community' not in legacy and 'BUILD ID: '+original.split('BUILD_ID="')[1][:12] in legacy
walk('legacy-metadata')
after=ssh('sha256sum /storage/.config/system/configs/system.cfg /storage/.config/emulationstation/es_settings.cfg').stdout;(P/'protected-after.txt').write_text(after)
assert protected==after
actualhash=ssh('sha256sum /usr/bin/rocknix-info').stdout.split()[0];assert actualhash==hashlib.sha256(source.read_bytes()).hexdigest()
(P/'result.json').write_text(json.dumps({'pass':True,'script_sha256':actualhash,'source_overlay_not_new_firmware':True,'original_settings_hashes_equal':True,'flows':['before','new-identity','legacy-metadata'],'panel':'640x480','visual_review':'pending','existing_script_exit':127,'script_exit_explanation':'optional absent VM info quirk glob; original and revised scripts have the same exit while producing the full display rows'},indent=2)+'\n')
print('PASS actual information script and retained settings; frame review pending')
