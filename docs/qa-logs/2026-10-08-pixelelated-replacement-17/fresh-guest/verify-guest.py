from pathlib import Path
import json,hashlib,datetime,subprocess,shlex
O=Path('/workspace/tmp/pixelelated-m7-cf10-17/guest03');R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17');W=Path((O/'run.path').read_text().strip())
channels={n:(O/n).read_text().strip() for n in ['inner.rc','outer.rc','tool-wrapper.rc']};channels['build.rc']=(W/'build.rc').read_text().strip();assert set(channels.values())=={'0'}
assert json.loads((O/'launcher-result.json').read_text())['runner_returncode']==0
pids=[json.loads((O/'launcher-pid.json').read_text())['pid']]+[int((W/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']];assert all(not Path('/proc',str(p)).exists() for p in pids)
guest=json.loads((O/'guest.json').read_text());pid=guest['qemu_pid'];args=Path('/proc',str(pid),'cmdline').read_bytes().split(b'\0');assert any((b'file='+str(O/'vm.qcow2').encode()) in arg.split(b',') for arg in args)
assert int((O/'vm.pid').read_text())==pid
ssh=['ssh','-i',str(O/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
messages=json.loads((R/'docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/host01/new-messages.json').read_text())
code='''import gettext,json,pathlib,hashlib,os
p=pathlib.Path('/usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo')
with p.open('rb') as f:t=gettext.GNUTranslations(f)
messages=json.loads('''+repr(json.dumps(messages))+''')
for en,want in messages.items():assert t.gettext(en)==want,en
staged=pathlib.Path('/usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo')
assert p.read_bytes()==staged.read_bytes()
print(json.dumps({'passed':True,'message_count':len(messages),'staged_runtime_equal':True,'runtime_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'runtime_resolved_path':str(p.resolve()),'boot_id':pathlib.Path('/proc/sys/kernel/random/boot_id').read_text().strip()}))
'''
(O/'verify-runtime-catalog.py').write_text(code)
q=subprocess.run(ssh+['python3 -'],input=code,text=True,capture_output=True,timeout=20);(O/'runtime-catalog.stdout').write_text(q.stdout);(O/'runtime-catalog.stderr').write_text(q.stderr);q.check_returncode();proof=json.loads(q.stdout);assert proof['passed']
(O/'runtime-catalog.json').write_text(json.dumps(proof,indent=2)+'\n')
with (O/'owner-verification.json').open('x') as f:json.dump({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','channels':channels,'launcher_pids_absent':pids,'qemu_pid_live':pid,'exact_owned_disk':str(O/'vm.qcow2'),'runtime_catalog':proof,'private_qa_key_custody':'guest03/qa-key; original guest.json qa_key label retained as stale descriptive field, actual SSH argv and current receipt bind correct file','scope':'fresh image boot and installed-byte/catalog inclusion only; CF10 actions and other VM suites pending'},f,indent=2);f.write('\n')
print('PASS fresh image boot, exact owned live guest, launcher exits, runtime catalog alias and all11 French translations')
