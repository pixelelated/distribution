"""Fresh E-H gates, with current input snapshots and exact enumerated scan."""
import argparse,base64,datetime,hashlib,json,pathlib,subprocess,sys
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];p=argparse.ArgumentParser();p.add_argument('--phase',choices=['pre','resolution'],required=True);p.add_argument('--dest',required=True);args=p.parse_args();dest=A/args.dest;dest.mkdir(parents=True,exist_ok=False);rows=[]
def sha(b):return hashlib.sha256(b).hexdigest()
common=[A/'04-analysis.md',A/'05-punch-list.md',A/'second-opinions/review-plan.json',R/'docs/audits/README.md',A/'stage-e/scope-policy.json',A/'tools/eh-scope.py']
checks=[('index-write',['tools/work-log-index','--write']),('rules',['tools/rules-check']),('register',['tools/register-check']),('index',['tools/work-log-index','--check']),('ceremony',['tools/ceremony-check','--gate'])]
flags=['--phase','pre-issue'] if args.phase=='pre' else []
checks += [('audit-lint',['tools/lint-audit-artifacts',*flags,str(A.relative_to(R))]),('audit-issue-lint',['tools/lint-audit-artifacts',*flags,str(A.relative_to(R)),'--issue','1417']),('audit-checkboxes',['tools/box-check','--issue','1417']),('bug-checkboxes',['tools/box-check','--issue','1416']),('scope',['python3','-B',str(A/'tools/eh-scope.py'),'--repo',str(R),'--policy',str(A/'stage-e/scope-policy.json')]),('staged-whitespace',['git','diff','--cached','--check']),('working-whitespace',['git','diff','--check'])]
for name,cmd in checks:
 inputs=common+([R/cmd[0]] if cmd[0].startswith('tools/') else [])
 argv=['python3','-B',str(A/'tools/eh-record.py'),'--out',args.dest+'/'+name]
 for f in inputs:argv+=['--input',str(f)]
 argv+=['--',*cmd];r=subprocess.run(argv,cwd=R);rows.append({'name':name,'rc':r.returncode,'receipt':args.dest+'/'+name+'/receipt.json'});(dest/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
 if r.returncode:raise SystemExit('Current gate failed: '+name)
# Current source identity is a fresh comparison, not replay of old-source/control fixtures.
readme=(R/'docs/audits/README.md').read_bytes();assert len(readme)==813 and sha(readme)=='410e4432c01a38cda578a68fdaa730129c15a8e3e60c7305001bb40bd5a71b6c'
paths=set()
for cmd in [('git','diff','--name-only','-z','a0d4c4fda7a0c16c04d57edf921ffeb741eff19b'),('git','diff','--cached','--name-only','-z','a0d4c4fda7a0c16c04d57edf921ffeb741eff19b'),('git','ls-files','--others','--exclude-standard','-z')]:paths.update(x.decode() for x in subprocess.check_output(cmd,cwd=R).split(b'\0') if x)
manifest=[];chunks=[]
for path in sorted(paths):
 f=R/path;assert f.is_file() and not f.is_symlink();b=f.read_bytes();manifest.append({'path':path,'bytes':len(b),'sha256':sha(b)});chunks.append((path+'\n').encode()+b+b'\n')
data=b''.join(chunks);argv=['tools/forbidden-terms-check','--stdin'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,cwd=R,input=data,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat()
for name,b in [('stdout',r.stdout),('stderr',r.stderr)]:(dest/('scan-'+name+'.json')).write_text(json.dumps({'bytes':len(b),'sha256':sha(b),'base64':base64.b64encode(b).decode()},indent=2)+'\n')
scan={'argv':argv,'cwd':str(R),'start':start,'end':end,'rc':r.returncode,'program_sha256':sha((R/argv[0]).read_bytes()),'stdin_sha256':sha(data),'files':manifest,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'self_exclusions':'This scan manifest/output files and the active outer receipt are produced afterward. Exact final committed set is verified externally after final commit.'};(dest/'scan-manifest.json').write_text(json.dumps(scan,indent=2)+'\n');assert r.returncode==0
print('PASS current '+args.phase+' gates: '+str(len(rows))+' commands; exact source813 bytes; scan'+str(len(manifest))+' paths; explicit current04/05/plan/README/checker inputs')
