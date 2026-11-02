"""Read-only T44 record confinement: every distribution commit and current changes; whole ES unchanged."""
import os,pathlib,subprocess,json,sys
AUDIT='docs/audits/2026_11_02-epic-m6-es-vendored-and-data/'
SEED='48a335700d05a733703e1b58536877b91b921259'
ES='55158d2a64c69fe295fb4e67fd174424a71b1b4d'
TREE='64b90eb8cb07bdfcd690c74ff6bc980ae490657c'
D=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-es-vendored-and-data-691')
E=pathlib.Path('/home/max/Development/emulationstation-next.worktrees/m6-es-vendored-and-data-691')
EXACT={'.github/sessions/saved-session-state-feature-m6-es-vendored-and-data-691.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md'}
def validate_paths(rows):
    for p,mode in rows:
        if not p or p.startswith('/') or '\\' in p or any(x in ('','.','..') for x in p.split('/')):raise ValueError('NONCANONICAL_PATH:'+p)
        if not (p.startswith(AUDIT) or p in EXACT):raise ValueError('FORBIDDEN_PATH:'+p)
        if mode not in ('100644','100755'):raise ValueError('NONRECORD_MODE:'+p)
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def diff(a,b=None):
    rows=[]
    fields=git(D,'diff','--raw','-z','--no-renames',a,*([b] if b else []),'--').split(b'\0');i=0
    while i<len(fields) and fields[i]:
        meta=fields[i].decode().split();p=fields[i+1].decode();i+=2
        if meta[-1]=='D':raise ValueError('DELETION:'+p)
        rows.append((p,meta[1]))
    validate_paths(rows);return rows
def main():
    head=git(D,'rev-parse','HEAD').decode().strip();commits=git(D,'rev-list','--reverse',SEED+'..'+head).decode().splitlines()
    subprocess.run(['git','-C',str(D),'merge-base','--is-ancestor',SEED,head],check=True)
    reviewed=[]
    for c in commits:
        parents=git(D,'show','-s','--format=%P',c).decode().split()
        if len(parents)!=1:raise ValueError('MERGE_NOT_ALLOWED')
        reviewed.append(dict(commit=c,paths=diff(parents[0],c)))
    # Diff with omitted second revision includes index and worktree against seed.
    live=diff(SEED)
    untracked=git(D,'ls-files','--others','--exclude-standard','-z').split(b'\0');rows=[]
    for b in untracked:
        if not b:continue
        p=b.decode();f=D/p
        if f.is_symlink() or not f.is_file():raise ValueError('UNTRACKED_NOT_REGULAR:'+p)
        rows.append((p,'100755' if f.stat().st_mode&0o111 else '100644'))
    validate_paths(rows)
    eh=git(E,'rev-parse','HEAD').decode().strip();et=git(E,'rev-parse','HEAD^{tree}').decode().strip();status=git(E,'status','--porcelain=v1','--untracked-files=all')
    if eh!=ES or et!=TREE or status:raise ValueError('ES_CHANGED')
    print(json.dumps(dict(distribution_head=head,seed=SEED,commits=reviewed,live_changed=live,untracked_count=len(rows),es_head=eh,es_tree=et,es_status_empty=True),indent=2))
    print('PASS T44 confinement: every new commit and current path allowed; whole ES seed/tree clean')
if __name__=='__main__':main()
