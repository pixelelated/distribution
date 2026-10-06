from pathlib import Path
import collections,datetime,hashlib,json,re,subprocess
repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
baseline='51f78ac5b4';current='ed5a6a51f5974deec8748fbf0dbd2f4984b690f5'
report=repo/'docs/rasteratops/p0-sweep-hits.txt'
dest=repo/'docs/qa-logs/2026-10-06-pixelelated-replacement-15/cloud-path-disposition'
dest.mkdir(exist_ok=True)
assert not any(dest.iterdir()), 'completed disposition must not be replayed'
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args],text=True)
rows=[];sources={}
for line in report.read_text().splitlines():
 if '[cloud-path]' not in line:continue
 match=re.fullmatch(r'class3 KEEP \[cloud-path\] (.*?):(\d+): (.*?)  -- .*',line);assert match,line
 path,old_line,snippet=match.groups();old=git('show',baseline+':'+path);new=git('show',current+':'+path)
 assert old.splitlines()[int(old_line)-1].strip()==snippet.strip(),(path,old_line)
 sources[path]={'baseline_sha256':hashlib.sha256(old.encode()).hexdigest(),'candidate_sha256':hashlib.sha256(new.encode()).hexdigest()}
 matches=[{'line':i,'text':s.strip()} for i,s in enumerate(new.splitlines(),1) if s.strip()==snippet.strip()]
 if matches:
  if '/network/rclone/' in path:
   assert snippet.lstrip().startswith('#')
   disposition='KEEP_LEGACY_COMMENT';reason='Historical layout or migration/normalization example; not a current default.'
  elif 'https://github.com/ROCKNIX/' in snippet:
   disposition='KEEP_UPSTREAM_URL';reason='Upstream package/source attribution or download location; not a player cloud path.'
  else:
   disposition='KEEP_BUILD_PATH';reason='Build-system project/directory reference retained by D-WORKFLOW-123; not a cloud destination.'
 else:
  key=re.match(r'\s*([A-Z_0-9]+)=',snippet);assert key,(path,snippet)
  key=key.group(1)
  matches=[{'line':i,'text':s.strip()} for i,s in enumerate(new.splitlines(),1) if re.match(r'\s*'+key+'=',s)]
  if '/network/rclone/' in path:
   # CONTENT also has a branch preserving an explicit stored choice. Match
   # the historical literal default to the current literal default only.
   matches=[m for m in matches if '/pixelelated/' in m['text']]
   assert len(matches)==1,(path,key,matches)
   assert '/pixelelated/' in matches[0]['text'],matches
   disposition='CHANGED_CURRENT_DEFAULT';reason='Current default/destination uses /pixelelated under D-CLOUD-174.'
  else:
   assert len(matches)==1,(path,key,matches)
   assert path.endswith('/rocknix-splash/package.mk') and matches[0]['text']=='PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"',(path,matches)
   site=[{'line':i,'text':s.strip()} for i,s in enumerate(new.splitlines(),1) if s.strip()=='PKG_SITE="https://github.com/pixelelated/splash"']
   assert len(site)==1;matches+=site
   disposition='CHANGED_FORK_SOURCE';reason='Fork-owned splash source moved to canonical pixelelated organization; not a player cloud folder.'
 row={'id':len(rows)+1,'path':path,'baseline_line':int(old_line),'baseline_text':snippet,'disposition':disposition,'reason':reason,'candidate_matches':matches}
 if disposition.startswith('CHANGED'):
  row['history']=git('log','--format=%H %s','-n','3','-S',snippet,current,'--',path).splitlines()
 rows.append(row)
assert len(rows)==56
counts=collections.Counter(r['disposition'] for r in rows)
value={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_ref':git('rev-parse',baseline).strip(),'candidate_ref':current,'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'count':len(rows),'counts':dict(counts),'source_sha256':sources,'rows':rows,'scope':'Retrospective exact 56-entry reconciliation to candidate15 source. Not a claim that a new same-commit reconciliation existed at the old baseline; not a whole-image sweep.'}
(dest/'disposition.json').write_text(json.dumps(value,indent=2)+'\n')
text='''# Historical cloud-path sweep reconciliation

The immutable first-sweep report has 56 hits under its broad `cloud-path`
rule. This receipt matches every original line to its actual baseline source
and classifies the corresponding frozen candidate15 source. Many hits are
upstream URLs or build paths. Historical and compatibility examples remain;
all changed cloud defaults use `/pixelelated`.

This is a retrospective mapping written now. It does not claim the mapping
was written in the historical implementation commits. The original sweep
remains unchanged. Whole-image brand/credential classification and VM
migration checks are separate evidence in this candidate's QA directory.

| Hit | Original location | Disposition | Candidate line |
| --- | --- | --- | --- |
'''
for r in rows:text+=f"| {r['id']} | `{r['path']}:{r['baseline_line']}` | {r['disposition']} | "+', '.join(str(m['line']) for m in r['candidate_matches'])+' |\n'
(dest/'README.md').write_text(text)
(dest/'reconcile.py').write_bytes(Path(__file__).read_bytes())
(dest/'sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file()},indent=2)+'\n')
print(json.dumps({'count':len(rows),'counts':dict(counts),'unclassified':0}))
