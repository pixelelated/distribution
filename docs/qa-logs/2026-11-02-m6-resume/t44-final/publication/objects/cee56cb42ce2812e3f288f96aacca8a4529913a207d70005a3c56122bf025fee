#!/usr/bin/env python3
"""T44 E-H read-only record guard; separate from frozen A-D tools."""
import argparse, hashlib, json, os, pathlib, stat, subprocess, sys

class Refusal(Exception): pass
def require(value, message):
    if not value: raise Refusal(message)
def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args],env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','LC_ALL':'C'})
def tree(repo,ref):
    out={}
    for row in git(repo,'ls-tree','-r','-z',ref).split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1); mode,kind,oid=meta.decode().split()
        out[path.decode()] = (mode,kind,oid)
    return out
def delta(a,b): return sorted(p for p in a.keys()|b.keys() if a.get(p)!=b.get(p))
def allowed(path,cfg,late):
    if path in cfg['exact_paths']: return True
    if not late: return path.startswith(cfg['audit']+'/')
    return path in cfg['editable']+cfg['new_tools'] or any(path.startswith(cfg['audit']+'/'+s+'/') for s in ('stage-e','stage-f','stage-g','stage-h')) or path==cfg['audit']+'/README.md'
def check_delta(a,b,cfg,late,label):
    for p in delta(a,b):
        require(p in b, 'DELETION '+label+' '+p)
        require(allowed(p,cfg,late),'PATH '+label+' '+p)
        require(b[p][:2]==('100644','blob'),'MODE '+label+' '+p)
def preserve(d,t,cfg,label):
    for p,v in d.items():
        if p.startswith(cfg['audit']+'/') and p not in cfg['editable']:
            require(t.get(p)==v, 'FROZEN '+label+' '+p)
def validate(repo,cfg,tip,working,es):
    seed,accepted=cfg['seed'],cfg['accepted_d']
    require(not git(repo,'merge-base','--is-ancestor',seed,accepted),'ANCESTRY seed/D')
    require(not git(repo,'merge-base','--is-ancestor',accepted,tip),'ANCESTRY D/tip')
    seedtree,dtree,ttree=tree(repo,seed),tree(repo,accepted),tree(repo,tip)
    commits=git(repo,'rev-list','--reverse',seed+'..'+tip).decode().splitlines()
    late=False; rows=[]
    for rev in commits:
        parents=git(repo,'rev-list','--parents','-n','1',rev).decode().split()
        require(len(parents)==2,'MERGE '+rev)
        parent=parents[1]
        if parent==accepted: late=True
        t=tree(repo,rev); p=tree(repo,parent)
        if late: preserve(dtree,t,cfg,rev)
        check_delta(p,t,cfg,late,rev)
        rows.append({'commit':rev,'parent':parent,'changed':delta(p,t),'post_d':late})
    check_delta(seedtree,ttree,cfg,False,'seed-to-tip')
    preserve(dtree,ttree,cfg,'tip')
    work=[]
    if working:
        require(git(repo,'rev-parse','HEAD').decode().strip()==tip,'WORKING HEAD mismatch')
        candidates=set(git(repo,'diff','--name-only','-z',tip).decode().strip('\0').split('\0'))|set(git(repo,'ls-files','--others','--exclude-standard','-z').decode().strip('\0').split('\0'))
        wt=ttree.copy()
        for p in sorted(candidates-{''}):
            q=pathlib.Path(repo)/p
            require(q.exists() or q.is_symlink(),'DELETION working '+p)
            for parent in [q,*list(q.parents)[:len(pathlib.PurePosixPath(p).parts)-1]]:
                require(not parent.is_symlink(),'MODE symlink '+p)
            s=q.lstat(); require(stat.S_ISREG(s.st_mode) and not s.st_mode&0o111,'MODE working '+p)
            oid=git(repo,'hash-object','--',p).decode().strip()
            wt[p]=('100644','blob',oid); work.append(p)
        preserve(dtree,wt,cfg,'working')
        check_delta(ttree,wt,cfg,True,'working')
    eshead=git(es,'rev-parse','HEAD').decode().strip(); estree=git(es,'rev-parse','HEAD^{tree}').decode().strip()
    require(eshead==cfg['es_head'] and estree==cfg['es_tree'],'ES IDENTITY')
    require(not git(es,'status','--porcelain=v1','--untracked-files=all'),'ES DIRTY')
    frozen=[p for p in dtree if p.startswith(cfg['audit']+'/') and p not in cfg['editable']]
    return {'result':'PASS','seed':seed,'accepted_d':accepted,'tip':tip,'tip_tree':git(repo,'rev-parse',tip+'^{tree}').decode().strip(),'commits':rows,'seed_to_tip_changed':delta(seedtree,ttree),'working_changes':work,'preserved_D_artifacts':len(frozen),'D_mode_blob_manifest_sha256':hashlib.sha256(json.dumps({p:dtree[p] for p in sorted(frozen)},sort_keys=True).encode()).hexdigest(),'source_selector_rule_identity':'all non-allowlisted modes/blobs unchanged, including every commit','es_head':eshead,'es_tree':estree,'es_clean':True}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--repo',required=True);p.add_argument('--allowlist',required=True);p.add_argument('--tip',default='HEAD');p.add_argument('--working',action='store_true');p.add_argument('--es',required=True);a=p.parse_args()
    data=pathlib.Path(a.allowlist).read_bytes();cfg=json.loads(data)
    try:
        tip=git(a.repo,'rev-parse',a.tip+'^{commit}').decode().strip()
        out=validate(a.repo,cfg,tip,a.working,a.es);out['allowlist_sha256']=hashlib.sha256(data).hexdigest();print(json.dumps(out,indent=2));return 0
    except (Refusal,subprocess.CalledProcessError,OSError,ValueError) as e:
        print(json.dumps({'result':'REFUSE','reason':str(e),'allowlist_sha256':hashlib.sha256(data).hexdigest()}));return 1
if __name__=='__main__':sys.exit(main())
