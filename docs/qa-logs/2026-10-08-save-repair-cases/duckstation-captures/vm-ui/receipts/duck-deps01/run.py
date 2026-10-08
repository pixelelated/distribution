import pathlib,subprocess,json,hashlib,shutil
b=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');o=b/'duck-deps01';lib=pathlib.Path('/workspace/repos/rocknix.worktrees/m7-duckstation-deps01/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/lib/libcom_err.so.2.1');sha='043101a87e5eaa57b786b88dfbd227be2d7768445d53b69346b547fef2e938a3';assert hashlib.sha256(lib.read_bytes()).hexdigest()==sha
ssh=['ssh','-i',str(b/'guest01/qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1'];scp=['scp','-q','-i',str(b/'guest01/qa-key'),'-P','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
subprocess.run(scp+[str(lib),'root@127.0.0.1:/storage/qa521/libcom_err.so.2.1'],check=True)
cmd='''set -eu
mkdir -p /storage/qa521/libupper /storage/qa521/libwork
mount -t overlay overlay -o lowerdir=/usr/lib,upperdir=/storage/qa521/libupper,workdir=/storage/qa521/libwork /usr/lib
for n in libcom_err.so libcom_err.so.2 libcom_err.so.2.1; do install -m 0755 /storage/qa521/libcom_err.so.2.1 /usr/lib/$n; done
sha256sum /usr/lib/libcom_err.so*
. /etc/profile
timeout 20 /usr/bin/duckstation-sa -help
''';(o/'stage.sh').write_text(cmd);q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'entrypoint.log').write_bytes(q.stdout);print(q.stdout.decode());q.check_returncode()
q=subprocess.run(ssh+['python3 -'],input=(pathlib.Path('/tmp/pix521-closure.py')).read_bytes(),stdout=subprocess.PIPE,stderr=subprocess.PIPE);(o/'all-elf-closure.json').write_bytes(q.stdout);(o/'closure-stderr.txt').write_bytes(q.stderr);q.check_returncode();d=json.loads(q.stdout);issues=[x for x in d['entries'] if x['issues'] or x['exit']];assert not issues,issues;assert len(d['entries'])==121;print('PASS121 bundled ELF/plugin closures resolved and actual AppImage application -help exits0')
(o/'identity.json').write_text(json.dumps({'distribution_commit':'052771f05d841fb91fa818198f8f4e0ad83affb8','launcher_helper_commit':'dda2a04aaf411b8bc13aedf5ce44ff33ce4b3d3a','target_lib_sha256':sha,'target_lib_source':str(lib),'appimage_sha256':'b204886bb498ede1a290215fc2efb521c0c2f26b964788df697b4fc2cb3f7f7b','kind':'explicit project-target-library source overlay, not rebuilt firmware'},indent=2)+'\n')
