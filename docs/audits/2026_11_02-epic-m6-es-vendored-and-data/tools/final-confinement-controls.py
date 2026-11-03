#!/usr/bin/env python3
"""New tiny-Git E-H guard controls; no accepted producer/source copied."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys, tempfile
def sha(b):return hashlib.sha256(b).hexdigest()
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 p=argparse.ArgumentParser();p.add_argument('--guard',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=False)
 root=pathlib.Path(tempfile.mkdtemp(prefix='m6-t44-eh-fixture-'));r=root/'repo';es=root/'es';r.mkdir();es.mkdir()
 events=[]
 def run(repo,args):
  cmd=['git','-c','user.name=T44 synthetic','-c','user.email=t44-fixture@example.invalid','-c','core.hooksPath=/dev/null',*args];start=stamp();x=subprocess.run(cmd,cwd=repo,capture_output=True)
  events.append({'argv':cmd,'cwd':str(repo),'start':start,'end':stamp(),'rc':x.returncode,'stdout':x.stdout.decode(),'stderr':x.stderr.decode(),'stdout_sha256':sha(x.stdout),'stderr_sha256':sha(x.stderr)})
  assert x.returncode==0,events[-1];return x.stdout.decode().strip()
 def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
 def commit(msg):run(r,['add','.']);run(r,['commit','-m',msg]);return run(r,['rev-parse','HEAD'])
 for repo in (r,es):run(repo,['init','--template='])
 write(es/'identity','synthetic ES only\n');run(es,['add','.']);run(es,['commit','-m','fixture ES'])
 audit='docs/audits/t44'; product='projects/toy/package.mk';write(r/product,'synthetic source placeholder\n');seed=commit('seed')
 write(r/(audit+'/stage-a/frozen.json'),'accepted synthetic record\n');write(r/(audit+'/00-running-log.md'),'D narrative\n');d=commit('D')
 cfg={'seed':seed,'accepted_d':d,'audit':audit,'editable':[audit+'/00-running-log.md'],'new_tools':[audit+'/tools/final-confinement.py'],'exact_paths':['docs/retros/2026-11-03-m6-es-vendored-and-data.md','docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md','docs/work-logs/INDEX.md'],'es_head':run(es,['rev-parse','HEAD']),'es_tree':run(es,['rev-parse','HEAD^{tree}'])}
 allow=root/'allowlist.json';write(allow,json.dumps(cfg,indent=2)+'\n');results=[]
 def check(name,expected,reason):
  cmd=[sys.executable,'-I','-B',a.guard,'--repo',str(r),'--allowlist',str(allow),'--es',str(es)];start=stamp();x=subprocess.run(cmd,capture_output=True)
  (out/(name+'.stdout')).write_bytes(x.stdout);(out/(name+'.stderr')).write_bytes(x.stderr)
  row={'name':name,'argv':cmd,'start':start,'end':stamp(),'rc':x.returncode,'expected_rc':expected,'expected_reason':reason,'tip':run(r,['rev-parse','HEAD']),'stdout_sha256':sha(x.stdout),'stderr_sha256':sha(x.stderr),'allowlist_sha256':sha(allow.read_bytes()),'program_sha256':sha(pathlib.Path(a.guard).read_bytes())};results.append(row)
  assert x.returncode==expected and reason in x.stdout.decode(),row
 def reset():run(r,['reset','--hard',d]);run(r,['clean','-fd'])
 write(r/product,'changed synthetic product\n');commit('forbidden edit');write(r/product,'synthetic source placeholder\n');commit('revert product');check('product-edit-revert',1,'PATH');reset()
 write(r/(audit+'/stage-a/frozen.json'),'changed accepted record\n');commit('frozen change');check('frozen-artifact',1,'FROZEN');reset()
 write(r/'docs/retros/2026-11-03-unrelated.md','unrelated\n');commit('unrelated retro');check('unrelated-retro',1,'PATH');reset()
 write(r/'docs/work-logs/2026_11-work_logs/2026_11_04-work_log.md','wrong date\n');commit('wrong day');check('unrelated-worklog',1,'PATH');reset()
 q=r/(audit+'/stage-e/link');q.parent.mkdir(parents=True,exist_ok=True);q.symlink_to('../../source');commit('symlink');check('symlink',1,'MODE');reset()
 q=r/(audit+'/stage-e/executable');write(q,'synthetic\n');q.chmod(0o755);commit('executable mode');check('executable-mode',1,'MODE');reset()
 run(r,['rm',audit+'/stage-a/frozen.json']);commit('delete frozen');check('deletion',1,'FROZEN');reset()
 run(r,['mv',audit+'/stage-a/frozen.json',audit+'/stage-a/renamed.json']);commit('rename frozen');check('rename',1,'FROZEN');reset()
 write(r/(audit+'/stage-e/decision.md'),'new documentary decision\n')
 for path in cfg['exact_paths']:write(r/path,'authorized exact date record\n')
 commit('positive records with exact dated retro and worklog');check('positive',0,'PASS')
 # Dirty and different ES identity are distinct refusing predicates.
 write(es/'identity','dirty\n');check('es-dirty',1,'ES DIRTY');run(es,['checkout','--','identity'])
 run(es,['commit','--allow-empty','-m','other ES identity']);check('es-identity',1,'ES IDENTITY');run(es,['reset','--hard',cfg['es_head']])
 files=[]
 for f in sorted(root.rglob('*')):
  if f.is_file() and not f.is_symlink():s=f.stat();files.append({'path':str(f),'bytes':s.st_size,'sha256':sha(f.read_bytes()),'device':s.st_dev,'inode':s.st_ino})
 (out/'results.json').write_text(json.dumps({'result':'PASS','controls':results,'commands':events,'fixture_created_by':{'argv':sys.argv,'start_bound_by_parent_receipt':True,'pid':os.getpid(),'cpus':sorted(os.sched_getaffinity(0))},'fixture_root':str(root),'final_files':files,'custody':'Retain as synthetic refusal evidence for root review; no deletion authorized by this program'},indent=2)+'\n')
 print(json.dumps({'result':'PASS','controls':len(results),'refusals':sum(x['expected_rc']==1 for x in results),'fixture':str(root)}))
if __name__=='__main__':main()
