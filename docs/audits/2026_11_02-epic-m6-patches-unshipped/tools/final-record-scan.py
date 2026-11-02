#!/usr/bin/env python3
"""Enumerated new-record scan; exact scope, bytes and command result retained."""
import hashlib,json,pathlib,subprocess,sys
D='676115271e9bbaa9e8db81f6de73a7b49094c5b4'
def git(*a):return subprocess.check_output(['git',*a])
def paths(mode,ref):
 p=set(git('diff','--name-only',D,ref).decode().splitlines()) if mode=='commit' else set(git('diff','--name-only',D).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
 return sorted(p)
def data(mode,ref,p):return git('show',ref+':'+p) if mode=='commit' else pathlib.Path(p).read_bytes()
def collect(mode,ref):
 ref=git('rev-parse',ref).decode().strip()
 files={}
 for p in paths(mode,ref):
  b=data(mode,ref,p);files[p]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 return {'mode':mode,'ref':ref,'base':D,'scope':'Every changed record path since accepted D; current mode also includes all untracked paths. Unchanged accepted records are covered by final-confinement mode/blob reconciliation.','excluded_repository_paths':[],'count':len(files),'total_bytes':sum(x['bytes'] for x in files.values()),'files':files}
def validate(m):
 assert m['base']==D and m['mode'] in ('commit','current'),'manifest authority'
 expected=paths(m['mode'],m['ref']);assert set(expected)==set(m['files']) and m['count']==len(expected),'scan membership mismatch'
 for p,v in m['files'].items():
  b=data(m['mode'],m['ref'],p);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],'scan byte identity mismatch'
 assert m['total_bytes']==sum(x['bytes'] for x in m['files'].values()),'scan byte count mismatch'
 assert m['excluded_repository_paths']==[],'unexpected scan exclusion'
if __name__=='__main__':
 if sys.argv[1]=='validate':
  validate(json.loads(pathlib.Path(sys.argv[2]).read_text()));print('PASS exact enumerated scan manifest');sys.exit(0)
 mode=sys.argv[1];out=pathlib.Path(sys.argv[2]);assert out.is_relative_to('/workspace/tmp/m6-t43/eh-publication'),'external ordinary-file scan packet required'
 m=collect(mode,'HEAD');validate(m);out.parent.mkdir(parents=True,exist_ok=True)
 payload=b'\n'.join(data(mode,m['ref'],p) for p in m['files'])
 p=subprocess.run(['tools/forbidden-terms-check','--stdin'],input=payload,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out.with_suffix('.manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 out.with_suffix('.check.stdout').write_bytes(p.stdout);out.with_suffix('.check.stderr').write_bytes(p.stderr)
 out.with_suffix('.result.json').write_text(json.dumps({'argv':['tools/forbidden-terms-check','--stdin'],'exit':p.returncode,'stdin_sha256':hashlib.sha256(payload).hexdigest(),'stdin_bytes':len(payload),'manifest_sha256':hashlib.sha256(out.with_suffix('.manifest.json').read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'excluded_repository_paths':[]},indent=2)+'\n')
 assert p.returncode==0,'forbidden scan failed'
 print('PASS enumerated '+mode+' record scan: '+str(m['count'])+' paths, '+str(m['total_bytes'])+' bytes; zero repository exclusions; exact manifest; forbidden exit0')
