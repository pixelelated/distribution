"""Seal and scan only the new exact T46 record paths, never a corpus body sweep."""
import datetime,hashlib,json,pathlib,subprocess,sys
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];seed='8710a6210a40de0110244d03a886161ee06faf29';out=A/'stage-d/new-record-scan';out.mkdir(exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
paths=set()
for args in [('diff','--name-only','-z',seed),('ls-files','--others','--exclude-standard','-z')]:paths.update(x.decode() for x in git(*args).split(b'\0') if x)
exact={'.github/sessions/saved-session-state-feature-m6-records-693.md','docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md','docs/work-logs/INDEX.md'};rows=[];chunks=[]
for path in sorted(paths):
 assert path.startswith(str(A.relative_to(R))+'/') or path in exact,path
 p=R/path;assert p.is_file() and not p.is_symlink(),path;b=p.read_bytes();rows.append({'path':path,'bytes':len(b),'sha256':sha(b)});chunks.append((path+'\n').encode()+b+b'\n')
data=b''.join(chunks);(out/'manifest.json').write_text(json.dumps({'seed':seed,'files':rows,'stdin_sha256':sha(data),'limit':'Snapshot before this scan output/receipt creation. Final published-tree scan is external to observed commit.'},indent=2)+'\n')
argv=['tools/forbidden-terms-check','--stdin'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,cwd=R,input=data,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat();(out/'stdout').write_bytes(p.stdout);(out/'stderr').write_bytes(p.stderr);(out/'scan-command.json').write_text(json.dumps({'argv':argv,'cwd':str(R),'start':start,'end':end,'rc':p.returncode,'stdin_sha256':sha(data),'program_sha256':sha((R/argv[0]).read_bytes()),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)},indent=2)+'\n')
print('NEW_RECORDS',len(rows),'BYTES',sum(x['bytes'] for x in rows),'STDIN_SHA256',sha(data));sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr);sys.exit(p.returncode)
