from pathlib import Path
import ast,hashlib,json,shutil,subprocess,datetime
prefix='/workspace/tmp/pixelelated-m7-'
names=[('cloud-ui-07','cloud-ui-08'),('signin-ui-07','signin-ui-08'),('signin-1g-07','signin-1g-08')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads(Path(prefix+'cloud-ui-07/completion.json').read_text());assert c['job_rc']==1 and c['qemu_absent']
for a,b in names:
 assert not Path(prefix+b).exists()
 if a!='cloud-ui-07':assert not Path(prefix+a+'/qa.start').exists()
rows=[]
for a,b in names:
 src=Path(prefix+a);dst=Path(prefix+b);dst.mkdir(mode=0o700)
 for line in (src/'harness.sha256').read_text().splitlines():
  h,n=line.split(None,1);p=Path(n);assert sha(p)==h
  q=dst/p.name;s=p.read_text()
  for old,new in names:s=s.replace(prefix+old,prefix+new)
  q.write_text(s)
 if b=='cloud-ui-08':
  p=dst/'cloud-ui.sh';s=p.read_text()
  old="  protocol_init || exit 2\n  # Limit the fault"
  new="  # Reboot before installing volatile fault files; Refs #446.\n  debug_reboot\n  require_no_game || exit 2\n  protocol_init || exit 2\n  # Limit the fault"
  assert s.count(old)==1;s=s.replace(old,new)
  old="  debug_reboot\n  require_no_game || exit 2\n  G_ 'rm -f /tmp/cloud-epic-protocol/fired' || exit 2"
  assert s.count(old)==1;s=s.replace(old,"  require_no_game || exit 2\n  G_ 'rm -f /tmp/cloud-epic-protocol/fired' || exit 2")
  old="  protocol_snapshot > \"$P/logs/UI17-before-cloud.json\""
  new="""  G_ '. /etc/profile >/dev/null 2>&1; test -x /tmp/cloud-epic-protocol/rclone && test -s /tmp/cloud-epic-protocol/fault && test \"$(command -v rclone)\" = /tmp/cloud-epic-protocol/rclone'
  rc=$?; check "$rc" 'UI17 post-reboot fault files and actual executable selection verified'; [ "$rc" -eq 0 ] || exit 2
"""+old
  assert s.count(old)==1;s=s.replace(old,new)
  s=s.replace("G_ '/usr/bin/cloud_setup --check >/dev/null 2>&1'; check $?", "G_ '/usr/bin/cloud_setup --check >/dev/null 2>&1'; rc=$?; check \"$rc\"")
  s=s.replace("'UI17 real connectivity gate passes despite layout-only fault'", "'UI17 real connectivity gate passes despite layout-only fault'; [ \"$rc\" -eq 0 ] || exit 2")
  s=s.replace("[ \"$rc\" -ne 0 ]; check $? 'UI17 selected layout operation really fails before driving wizard'", "[ \"$rc\" -ne 0 ]; check $? 'UI17 selected layout operation really fails before driving wizard'; [ \"$rc\" -ne 0 ] || exit 2")
  s=s.replace("G_ 'test -s /tmp/cloud-epic-protocol/fired && rm /tmp/cloud-epic-protocol/fired'; check $? 'UI17 control reached fault; clear only its test count'", "G_ 'test -s /tmp/cloud-epic-protocol/fired && rm /tmp/cloud-epic-protocol/fired'; rc=$?; check \"$rc\" 'UI17 control reached fault; clear only its test count'; [ \"$rc\" -eq 0 ] || exit 2")
  assert s.index('debug_reboot',s.index('if want UI17;')) < s.index('protocol_init || exit 2',s.index('if want UI17;'))
  p.write_text(s)
 (dst/'reboot-fault-provenance.json').write_text(json.dumps({'issue':446,'prior_owner':str(src),'old_seal':sha(src/'harness.sha256'),'scope':'Reboot before volatile fault installation; require actual post-reboot fault controls. Fresh downstream bindings. Product and preservation assertions unchanged.'},indent=2)+'\n')
 subprocess.run(['python3','-I',str(dst/'prepare-dirs.py')],check=True)
 for p in dst.iterdir():
  if p.suffix=='.py':ast.parse(p.read_text())
  if p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
 files=sorted(p for p in dst.iterdir() if p.is_file());(dst/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in files))
 for p in files+[dst/'harness.sha256']:p.chmod(0o500 if p.suffix=='.sh' else 0o400)
 rows.append({'prior':str(src),'owner':str(dst),'sealed_members':len(files),'seal_sha256':sha(dst/'harness.sha256')})
Path('/tmp/pixelelated-cloud-ui08-chain.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'issue':446,'owners':rows,'product_unchanged':True},indent=2)+'\n')
print('PASS fresh three-owner chain: post-reboot fault controls, private directories, sealed inputs')
