"""Read-only final-record reconciliation against accepted D; never runs producers."""
import pathlib,subprocess,json,hashlib,collections,os,sys,datetime
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');REL='docs/audits/2026_11_02-epic-m6-patches-shipped';A=R/REL;D='d37670de318eb428604e4442f95defe10eade173';SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
def sha(x):return hashlib.sha256(x).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def identity(p):
 st=p.lstat();mode='120000' if p.is_symlink() else '100755' if st.st_mode&0o111 else '100644';b=os.readlink(p).encode() if p.is_symlink() else p.read_bytes();return mode,hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha(b)
def same(e,a):
 assert e==a,'accepted artifact identity mismatch'
def main():
 # New checker has its own synthetic bad-identity control; no producer or prior control is replayed.
 try:same(('100644','a'*40),('100644','b'*40))
 except AssertionError as e:
  assert str(e)=='accepted artifact identity mismatch';print('EXPECTED FAIL new-checker changed accepted identity:',e)
 else:raise AssertionError('new checker failed to reject bad identity')
 entries=[]
 for line in git('ls-tree','-r','-z',D,'--',REL).split(b'\0'):
  if not line:continue
  fields,path=line.split(b'\t',1);mode,kind,oid=fields.decode().split();p=path.decode();local=p[len(REL)+1:]
  if local.startswith(('stage-a/','stage-b/','stage-c/','stage-d/','tools/','second-opinions/')) or local in ['01-research-notes.md','03-retrospective.md']:
   am,ao,s=identity(R/p);same((mode,oid),(am,ao));entries.append({'path':p,'mode':mode,'git_blob':oid,'sha256':s})
 print('PASS accepted D receipts, data, original producer tools and untouched research:',len(entries))
 for name in ['02-forward-audit.md','04-analysis.md']:
  before=git('show',D+':'+REL+'/'+name);assert (A/name).read_bytes().startswith(before),'historical analysis prefix changed'
 t=json.loads((A/'stage-b/tables.json').read_text());assert len(t['native'])==len(t['coverage'])==384;assert len({n['path'] for n in t['native']})==384
 assert len(t['inherited'])==50 and len({(n['patch'],n['override']) for n in t['inherited']})==50 and len({n['override'] for n in t['inherited']})==26
 assert collections.Counter(n['application_status'] for n in t['native'])=={'applies':151,'offset':38,'fuzz':22,'open-item':173}
 assert collections.Counter(n['conclusion'] for n in t['inherited'])=={'already-carried':21,'not-applicable-with-reason':7,'unresolved-with-specific-evidence-needed':22}
 raw=json.loads((A/'stage-b/native-inputs.json').read_text());native_identity=[]
 for n in raw:
  mode,oid,s=identity(R/n['path']);same((n['mode'],n['oid'],n['sha256']),(mode,oid,s));assert sha((R/n['referent']).read_bytes())==n['patch_sha256'];native_identity.append(n['path'])
 summary=json.loads((A/'stage-a/seed/summary.json').read_text());extra=[]
 for p,h in summary['selector_sha256'].items():assert sha((R/p).read_bytes())==h;extra.append(p)
 for n in summary['symlinks']:assert os.readlink(R/n['path'])==n['target'] and sha((R/n['resolved']).read_bytes())==n['sha256'];extra.append(n['resolved'])
 unique=set(native_identity+extra);assert len(unique)==391
 print('PASS current source/selector/referent identities:',len(unique),'; native384 and inherited50 remain separate; 173/22 limits unchanged')
 groups=json.loads((A/'stage-b/selection.json').read_text());g=next(g for g in groups if g['id']=='G383');r=json.loads((A/'stage-b/application/G383.json').read_text());missing=[i['path'] for i in g['stack'] if i['path'] not in {x['path'] for x in r['rows']}]
 expected='projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/patches/SM8550/000-swap-guid-and-misc.patch';assert missing==[expected] and all(x['status']=='open-item' and not x['invoked'] for x in r['rows']);assert len(r['rows'])==6
 for name in ['G202','G203']:assert len(json.loads((A/f'stage-b/application/{name}.json').read_text())['rows'])==1
 punch=(A/'05-punch-list.md').read_text();assert '| PL-01 | Deferred |' in punch and '  outcome: deferred' in punch and '#1410' in punch and '#677' in punch
 matrix=json.loads((A/'stage-e/owner-actions.json').read_text());assert len(matrix['native_limits'])==173 and len(matrix['inherited'])==50 and len(matrix['contribution_drafts'])==12
 assert not (A/'audit-completion.json').exists(),'completion marker is coordinator-owned'
 print('PASS Deferred route and G202/G203/G383 missing evidence preserved; no completion marker')
 if '--manifest' in sys.argv:
  out=pathlib.Path(sys.argv[sys.argv.index('--manifest')+1]);out.write_text(json.dumps({'accepted_D':D,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entries':entries,'source_identity_count':391,'negative_control':{'rejected':True,'exception':'AssertionError','message':'accepted artifact identity mismatch'},'scope':'New immutable-file reader; no application, extraction, old mutation, nested fixture or source producer invoked'},indent=2)+'\n')
 print('PASS final-record reconciliation')
if __name__=='__main__':main()
