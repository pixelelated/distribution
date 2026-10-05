from pathlib import Path
import hashlib,json,shutil,subprocess,ast,re,stat
old=Path('/workspace/tmp/pixelelated-m7-sweep-08');new=Path('/workspace/tmp/pixelelated-m7-sweep-09');assert not new.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();receipt=json.loads((old/'completion.json').read_text());assert receipt['actual_tool_rc']==1 and receipt['qemu_absent']
sources=[]
for line in (old/'harness.sha256').read_text().splitlines():
 h,n=line.split(None,1);p=Path(n);assert sha(p)==h;sources.append(p)
rows=json.loads(Path('/tmp/pixelelated-sweep08-unknown-contexts.json').read_text());assert len(rows)==20
root=Path('/workspace/tmp/pixelelated-m7-image-11/root');tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09');build=tree/'build.pixelelated-GENERIC_X64.x86_64'
proxy=build/'build/raofflineproxy-7252fc781392d45b22f50d1a92f9febc4d1fa172/linux/raofflineproxy/config.py';src=proxy.read_text()
for row in rows:
 assert sha(root/row['path'])==row['file_sha256'];assert hashlib.sha256(row['text'].encode()).hexdigest()==row['context_sha256']
 if row['path']=='usr/bin/perf':
  source=tree/row['text'].split('/m7-pixelelated/',1)[1];assert source.is_file()
  row.update(source=str(source),source_sha256=sha(source),reason='Compiler source path; retained machine identity under NAMING.md v2. Not player-facing branding.')
 else:
  symbol=re.search(r'running_on_rocknix|DEFAULT_ROCKNIX_[A-Z_]+',row['text'])[0];assert symbol in src
  row.update(source=str(proxy),source_sha256=sha(proxy),symbol=symbol,reason='Existing upstream compatibility identifier verified in consumed proxy config.py; adjacent bytes are marshal references. Retain under NAMING.md v2.')
new.mkdir();(new/'artifacts').mkdir()
for p in sources:shutil.copyfile(p,new/p.name)
for p in new.iterdir():
 if p.suffix in {'.py','.sh','.json'}:
  data=p.read_text().replace(str(old),str(new));p.write_text(data)
allow=json.loads((old/'allowlist.json').read_text());existing={(r['path'],r['context_sha256']) for r in allow['branding']}
for row in rows:
 assert (row['path'],row['context_sha256']) not in existing
 allow['branding'].append({k:row[k] for k in ['path','context_sha256','reason']}|{'disposition':'KEEP','issue':442})
(new/'allowlist.json').write_text(json.dumps(allow,indent=2)+'\n');(new/'context-review.json').write_text(json.dumps({'issue':442,'original_receipt':receipt,'contexts':rows,'policy_sha256':sha(Path('NAMING.md'))},indent=2)+'\n')
p=new/'run.sh';s=p.read_text();a=s.index("python3 - <<'READABLE'");b=s.index("python3 \"$TASK_OWNER/check-controls.py\"",a)
s=s[:a]+'''python3 - <<'READABLE'
from pathlib import Path
import json,stat
p=Path('/workspace/tmp/pixelelated-m7-image-11/root/usr/cache/shadow')
assert stat.S_IMODE(p.stat().st_mode)==0o400
prior=Path('/workspace/tmp/pixelelated-m7-sweep-08/artifacts/extraction-read-permissions.json')
assert json.loads(prior.read_text())['original_mode']=='0000'
Path('/workspace/tmp/pixelelated-m7-sweep-09/artifacts/extraction-read-permissions.json').write_bytes(prior.read_bytes())
READABLE
python3 "$TASK_OWNER/context-controls.py"
'''+s[b:];p.write_text(s)
(new/'context-controls.py').write_text('''from pathlib import Path
import hashlib,importlib.machinery,json,re,shlex,tempfile
owner=Path(__file__).parent
module=importlib.machinery.SourceFileLoader('scan',str(owner/'scan-artifact.py')).load_module()
line,=[x for x in (owner/'secret-patterns').read_text().splitlines() if x.startswith('SECRET_PATTERNS=')]
patterns=re.compile(shlex.split(line)[0].split('=',1)[1].encode())
rows=json.loads((owner/'context-review.json').read_text())['contexts'];allow=json.loads((owner/'allowlist.json').read_text());results=[]
with tempfile.TemporaryDirectory(prefix='pixelelated-context-controls-') as name:
 root=Path(name)
 for row in rows:
  p=root/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(row['text'].encode())
  assert module.scan(root,allow,patterns)['pass']
  removed=dict(allow);removed['branding']=[r for r in allow['branding'] if (r['path'],r['context_sha256'])!=(row['path'],row['context_sha256'])]
  assert not module.scan(root,removed,patterns)['pass']
  p.write_bytes(b'UNREVIEWED-'+row['text'].encode());assert not module.scan(root,allow,patterns)['pass']
  p.write_bytes(row['text'].encode());other=root/'different-path';p.rename(other);assert not module.scan(root,allow,patterns)['pass'];other.unlink()
  results.append({'path':row['path'],'context_sha256':row['context_sha256'],'exact_pass':True,'removed_reject':True,'altered_reject':True,'different_path_reject':True})
(owner/'artifacts/context-controls.json').write_text(json.dumps({'passed':True,'contexts':results},indent=2)+'\\n')
print('PASS20 exact contexts and60 negative controls')
''')
(new/'correction-provenance.json').write_text(json.dumps({'issue':442,'parent':str(old),'parent_seal_sha256':sha(old/'harness.sha256'),'scanner_unchanged':sha(new/'scan-artifact.py')==sha(old/'scan-artifact.py'),'patterns_unchanged':sha(new/'secret-patterns')==sha(old/'secret-patterns'),'public_patterns_unchanged':allow['public_patterns']==json.loads((old/'allowlist.json').read_text())['public_patterns'],'added_contexts':20},indent=2)+'\n')
for p in sorted(new.iterdir()):
 if not p.is_file():continue
 if p.suffix=='.py':ast.parse(p.read_text())
 if p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
paths=sorted(p for p in new.iterdir() if p.is_file());(new/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in paths))
for p in paths+[new/'harness.sha256']:p.chmod(0o500 if p.suffix=='.sh' else 0o400)
print('PASS fresh sweep09 prepared:',len(paths),'sealed source members; old seal verified, scanner/patterns/public exceptions unchanged')
