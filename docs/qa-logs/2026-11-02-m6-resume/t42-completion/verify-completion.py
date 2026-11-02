import subprocess,json,hashlib,os,stat,datetime
from pathlib import Path
TIP='0eeaa4c9a6d384f57e0017c0be75673eb872f2db';ACCEPTED='4cf8c8820791624dbddad3eb3664101a03953a82';A='docs/audits/2026_11_02-epic-m6-patches-shipped/'
OUT=Path('docs/qa-logs/2026-11-02-m6-resume/t42-completion');sha=lambda b:hashlib.sha256(b).hexdigest();cmds=[]
def git(*a):
 p=subprocess.run(['git',*a],capture_output=True);cmds.append({'argv':['git',*a],'rc':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)});assert p.returncode==0;return p.stdout
def show(p):return git('show',TIP+':'+p)
def tree(ref):
 d={}
 for row in git('ls-tree','-r','-z',ref).split(b'\0'):
  if row:meta,p=row.split(b'\t',1);d[p.decode()]=meta.decode()
 return d
old,new=tree(ACCEPTED),tree(TIP);allowed={'.github/sessions/saved-session-state-feature-m6-patches-shipped-689.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md'}
changes={p for p in old.keys()|new.keys() if old.get(p)!=new.get(p)}
assert all(p in allowed or p==A+'audit-completion.json' or p.startswith(A+'completion/') for p in changes)
assert not any(p.startswith(A) and old[p]!=new.get(p) for p in old)
assert show('docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md').startswith(git('show',ACCEPTED+':docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'))
mraw=show(A+'audit-completion.json');assert sha(mraw)=='02c67e76fd0b667bcd34e39044976ad3b876e69bc41e83bc3a4d9b8b1ac2fee6';m=json.loads(mraw);assert m['schema']==1 and m['issue']==1411
for path,h in m['evidence'].items():assert sha(show(path))==h
live=json.loads((OUT/'live-closed-audit.json').read_text());rb=json.loads(show(m['tracker_readback']));tc=json.loads(show(m['tracker_completion']))
assert live['state']==rb['state']=='closed' and live['state_reason']==rb['state_reason']=='completed' and live['body']==rb['body']==show(A+'completion/1411-body.md').decode()
assert rb['body'].count('- [x]')==3 and '- [ ]' not in rb['body'];assert tc['verified_utc']==m['completed_at']
dt=lambda s:datetime.datetime.fromisoformat(s.replace('Z','+00:00'));assert dt(m['completed_at'])>=dt(rb['closed_at'])
checks=[]
for name in ['tracker-commands.json','checks.json']:
 for r in json.loads(show(A+'completion/'+name)):
  for stream in ('stdout','stderr'):
   assert sha(show(A+'completion/'+r['name']+'.'+stream))==r[stream+'_sha256'],r['name']
  checks.append({'name':r['name'],'rc':r['rc']})
for n in ['resolution','resolution-with-issue']:assert show(A+'completion/'+n+'.stdout').decode().rstrip().endswith('PASS')
external=Path('/tmp/m6-t42-completion-publication-_106q1ju');manifest=external/'manifest.json'
assert sha(manifest.read_bytes())=='936bf9104eb8729f697eb486fa07e51b79e81bd05d975cbb5ad29d2d8c3224d1'
em=json.loads(manifest.read_bytes());assert em['completion_record_tip']==TIP
records=[]
for r in em['files']:
 rel=Path(r['path']);assert not rel.is_absolute() and '..' not in rel.parts and len(rel.parts)==1
 fd=os.open(external/rel,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as f:assert stat.S_ISREG(os.fstat(f.fileno()).st_mode);b=f.read()
 assert len(b)==r['bytes'] and sha(b)==r['sha256'];records.append({'path':str(rel),'sha256':r['sha256'],'utf8':b.decode()})
for r in json.loads((external/'commands.json').read_bytes()):
 assert r['rc']==0,r['name']
 for stream in ('stdout','stderr'):
  assert sha((external/(r['name']+'.'+stream)).read_bytes())==r[stream+'_sha256']
assert (external/'tip.stdout').read_text().strip()==TIP and (external/'remote.stdout').read_text().split()[0]==TIP
assert (external/'final-clean.stdout').read_bytes()==b''
blob=''.join(json.dumps(r,ensure_ascii=True)+'\n' for r in records).encode();(OUT/'publication-receipts.jsonl').write_bytes(blob);(OUT/'publication-manifest.json').write_bytes(manifest.read_bytes())
result={'result':'PASS new completion record; no accepted producer replay','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'accepted_source':ACCEPTED,'completion':TIP,'marker_sha256':sha(mraw),'marker_evidence_hashes':len(m['evidence']),'prior_audit_files_unchanged':sum(p.startswith(A) for p in old),'all_other_prior_files_unchanged_except_pointer_log_index':True,'changed_paths':sorted(changes),'new_command_bindings':checks,'external_publication_files':len(records),'external_all_commands_rc0':True,'external_packet_sha256':sha(blob),'live_closed_body_exact':True,'completed_at':m['completed_at'],'closed_at':rb['closed_at']}
(OUT/'coordinator-verification.json').write_text(json.dumps(result,indent=2)+'\n');(OUT/'coordinator-commands.json').write_text(json.dumps(cmds,indent=2)+'\n');(OUT/'audit-completion.json').write_bytes(mraw)
print('PASS',len(m['evidence']),'evidence hashes;',len(checks),'new command bindings;',len(records),'publication files;',sum(p.startswith(A) for p in old),'accepted audit files unchanged')
