"""Bounded T42 E-H reconciliation. Immutable Git metadata/new receipts only.
No producer imports/execution, old stage replay, or source/cache/archive reads.
External file reads are confined to the explicitly authorized publication directory.
"""
import collections,functools,hashlib,json,os,pathlib,re,stat,subprocess
R='/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
F='4cf8c8820791624dbddad3eb3664101a03953a82';D='d37670de318eb428604e4442f95defe10eade173';S='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
C='afdec2bf8b88135befcb7ec56efb3a7ea327bd73';A='docs/audits/2026_11_02-epic-m6-patches-shipped/'
PUB='/workspace/tmp/m6-t42-final-publication-20261102T203040Z';MH='62ef887c2fd2cc67c7b88ebd9c1bdb80091423596c60a1cf0e6e1cdc01dc8781'
OUT=pathlib.Path(__file__).parent;errors=[];bindings=[];artifacts={}
def sha(b):return hashlib.sha256(b).hexdigest()
def check(ok,why):
 if not ok:errors.append(why)
def git(*a):return subprocess.check_output(['git','-C',R,*a])
@functools.lru_cache(None)
def blob(p,ref=F):return git('show',ref+':'+p)
def raw(p):
 b=blob(A+p);artifacts[p]=sha(b);return b
def j(p):return json.loads(raw(p))
def tree(ref,paths):
 out={}
 for i in range(0,len(paths),150):
  for row in git('ls-tree','-rz',ref,'--',*paths[i:i+150]).split(b'\0'):
   if row:
    meta,p=row.decode().split('\t',1);mode,kind,oid=meta.split();out[p]=(mode,oid)
 return out
dt=tree(D,[A]);ft=tree(F,[A]);manifest=j('stage-f/accepted-manifest.json')
accepted={p:v for p,v in dt.items() if p[len(A):].startswith(('stage-a/','stage-b/','stage-c/','stage-d/','tools/','second-opinions/')) or p[len(A):] in ['01-research-notes.md','03-retrospective.md']}
entries=manifest['entries'];check(len(entries)==len({n['path'] for n in entries})==len(accepted)==3931,'3931 exact accepted entries')
check({n['path'] for n in entries}==set(accepted),'accepted key set')
for n in entries:check(accepted.get(n['path'])==ft.get(n['path'])==(n['mode'],n['git_blob']),'accepted mode/blob '+n['path'])
check(manifest['accepted_D']==D and manifest['source_identity_count']==391,'manifest refs/count')
for p in ['02-forward-audit.md','04-analysis.md']:check(blob(A+p).startswith(blob(A+p,D)),'historical prefix '+p)
seed_summary=j('stage-a/seed/summary.json');source_paths=set(j('stage-a/seed/tree.json'))|set(seed_summary['selector_sha256'])|{n['resolved'] for n in seed_summary['symlinks']}
check(len(source_paths)==391,'391 source paths');sources={ref:tree(ref,sorted(source_paths)) for ref in [S,D,F]}
check(sources[S]==sources[D]==sources[F],'source modes/blobs seed/D/final')
allow=[A,'.github/sessions/saved-session-state-feature-m6-patches-shipped-689.md','docs/retros/2026-11-02-m6-patches-shipped.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md']
def allowed(p):return any(p.startswith(a) if a.endswith('/') else p==a for a in allow)
commits=[]
for row in git('rev-list','--reverse','--parents',D+'..'+F).decode().splitlines():
 ps=row.split();check(len(ps)==2,'no coordinator merge '+ps[0]);paths=git('diff','--name-only','-z',ps[1],ps[0]).decode().strip('\0').split('\0');check(all(allowed(p) for p in paths),'unauthorized delta '+ps[0]);commits.append({'commit':ps[0],'parent':ps[1],'changed_paths':len(paths)})
delta=git('diff','--name-only','-z',D,F).decode().strip('\0').split('\0')
scan=j('stage-h/current-scan-inputs.json')
scan_scope={'listed_paths':len(scan['paths']),'final_changed_paths':len(delta),'omitted_from_final_delta':sorted(set(delta)-set(scan['paths'])),'recorded_input_sha256':scan['input_sha256'],'scope_text':scan['scope']}
check(A+'audit-completion.json' not in ft,'completion marker remains absent')
tables=j('stage-b/tables.json');matrix=j('stage-e/owner-actions.json')
expected_native=[{'path':n['path'],'owner':n['owner'],'required_action':n['application'],'receipts':n['receipts']} for n in tables['native'] if n['application_status']=='open-item']
expected_inherited=[{'patch':n['patch'],'override':n['override'],'conclusion':n['conclusion'],'prior_owner':n['prior_recipe_owner'],'next_owner_action':n['remaining_owner_action'],'evidence':n['evidence']} for n in tables['inherited']]
expected_contrib=[{'path':n['path'],'owner':n['owner'],'action':n['contribution']} for n in tables['fork_written']]
check(matrix['native_limits']==expected_native and len(expected_native)==173,'173 owner/action rows exact')
check(matrix['inherited']==expected_inherited and len(expected_inherited)==50,'50 inherited owner/action rows exact')
check(matrix['contribution_drafts']==expected_contrib and len(expected_contrib)==12,'12 contribution rows exact')
check(sum(n['conclusion']=='unresolved-with-specific-evidence-needed' for n in expected_inherited)==22,'22 unresolved limits')
check(matrix['PL-01']=={'outcome':'deferred','bug':1410,'context':677,'route':'Coordinator-owned separate source-changing fix brief; no GUIDE mapping chosen','bug_state':'open'},'PL route')
for p in ['stage-b/selection.json','stage-b/application/G202.json','stage-b/application/G203.json','stage-b/application/G383.json']:check(dt[A+p]==ft[A+p],'preserved gap '+p)
check(raw('stage-e/disposition.stdout')==blob('docs/qa-logs/2026-11-02-m6-resume/t42-stage-d-disposition.md',C),'exact disposition readback')
check(raw('stage-e/coordinator-register.stdout')==blob('docs/decision-register.md',C),'exact register readback')
live={n:json.loads((OUT/f'live-{n}.json').read_text()) for n in [689,1411,1410]}
def comments(n,id):return next(c['body'] for c in live[n]['comments'] if c['id']==id)
check(j('stage-e/dispatch.stdout')['body']==comments(689,6587447155),'dispatch live match')
def receipt(x,stage):
 stem=stage+'/'+x['name'];hs={}
 for stream in ['stdout','stderr']:
  h=sha(raw(stem+'.'+stream));check(h==x[stream+'_sha256'],'new output hash '+stem+'.'+stream);hs[stream+'_sha256']=h
 bindings.append({'stem':stem,'rc':x['rc'],'argv':x['argv'],'utc':x.get('utc'),**hs})
for p in ['stage-e/commands.json','stage-f/commands.json','stage-h/cleanup-commands.json','stage-h/final-checks.json']:
 for x in j(p):receipt(x,p.split('/')[0])
check(next(x for x in j('stage-h/final-checks.json') if x['name']=='forbidden-current')['stdin_sha256']==scan['input_sha256'],'scoped scan recorded input binding')
for p in ['stage-f/resolution.stdout','stage-f/resolution-with-issue.stdout','stage-h/resolution-final.stdout','stage-h/resolution-issue-final.stdout']:check(raw(p).decode().rstrip().endswith('PASS'),'resolution literal PASS '+p)
for p in ['stage-f/final-record-check.stdout','stage-h/new-record-reconciliation.stdout']:check(b'EXPECTED FAIL new-checker changed accepted identity:' in raw(p) and b'3931' in raw(p) and b'391' in raw(p),'new checker control/pass '+p)
def boxes(s):return re.findall(r'^- \[([ xX])\].*$',s,re.M)
for p,want in [('stage-e/audit-disposition-readback.stdout',[' ',' ',' ']),('stage-e/audit-criterion1-readback.stdout',['x',' ',' ']),('stage-f/audit-criterion2-readback.stdout',['x','x',' '])]:check(boxes(j(p)['body'])==want,'criterion sequence '+p)
for n,label in [(1411,'audit'),(1410,'bug')]:
 r=j('stage-h/'+label+'-final.stdout');check(r['body']==live[n]['issue']['body'],'current live body '+str(n));check(r['state'].lower()==live[n]['issue']['state']=='open','current state '+str(n))
check(boxes(live[1411]['issue']['body'])==['x','x',' '],'audit final criteria');check(boxes(live[1410]['issue']['body'])==[' ',' ',' '],'bug final criteria')
check(live[1410]['issue']['body']==json.loads(blob(A+'stage-d/issue-1410-final.json',D))['body'],'bug body unchanged from accepted D')
retro='docs/retros/2026-11-02-m6-patches-shipped.md';g=j('stage-g/receipt.json');gr=raw('stage-g/readback.json')
check(sha(blob(retro))==g['retro_sha256']=='22b1b2eb6b6be46e7a5f105e6956a20c317b7a5fb9095ad47d2088553dbc24b3','retro file hash')
check(sha(gr)==g['readback_sha256'],'retro readback hash');check(json.loads(gr)['body']==comments(689,6587734065)==raw('stage-g/comment-body.md').decode(),'retro exact body/live')
check(blob(retro).decode().strip() in json.loads(gr)['body'],'retro content in posted body')
bindings.extend([{'stem':'stage-g/post','rc':g['post_rc'],'argv':g['post_argv'],'stdout_sha256':sha(raw('stage-g/post.stdout')),'stderr_sha256':sha(raw('stage-g/post.stderr'))},{'stem':'stage-g/readback','rc':g['readback_rc'],'argv':g['readback_argv'],'stdout_sha256':sha(gr)}])
cm=j('stage-h/cleanup-manifest.json');cr=j('stage-h/cleanup-result.json');cc=j('stage-h/cleanup-controls.json');roots=cm['roots']
check(len(roots)==len({r['path'] for r in roots})==cr['root_count']==522,'522 exact root keys')
check([r['path'] for r in roots]==cr['removed_roots'],'retirement removed list')
check(sum(r['logical_file_bytes'] for r in roots)==cr['logical_file_bytes_retired']==502085226,'retirement byte sum')
check(len(cm['cache_preserved_metadata'])==cr['cache_archive_count_untouched']==129,'cache metadata count')
check(cm['accepted_manifest_sha256']==sha(raw('stage-f/accepted-manifest.json')),'cleanup binds F manifest')
check(blob(A+'stage-f/accepted-manifest.json',cm['needed_receipts_committed_at'])==raw('stage-f/accepted-manifest.json')==raw('stage-h/committed-manifest.stdout'),'committed manifest custody')
origin_counts=collections.Counter()
for r in roots:
 p=pathlib.PurePosixPath(r['path']);check(str(p)=='/tmp/m6-t42-inputs.8whm3634' or str(p.parent)=='/workspace/tmp/m6-t42','root confinement '+str(p));o=r['origin'];origin_counts[o['kind']]+=1
 for path in ([o['receipt']] if 'receipt' in o else [])+[x['receipt'] for x in o.get('children',[])]+[x['receipt'] for x in o.get('files',[])]:check(A+path in accepted,'retirement origin accepted '+path)
check(cc['outside_path']['rejected'] and cc['live_owner']['rejected'],'cleanup refusal controls')
check(all(p.startswith(('/var/lib/docker/','/run/docker/','/run/snapd/ns')) for p in cc['excluded_filesystems']),'excluded mount boundaries')
for name in ['owner-control-closed','pre-delete-owned-source','pre-delete-owned-text-export']:
 x=next(x for x in j('stage-h/cleanup-commands.json') if x['name']==name);check(x['rc']==1 and raw('stage-h/'+name+'.stdout')==raw('stage-h/'+name+'.stderr')==b'','closed-owner raw '+name)
check(raw('stage-h/owner-control-live.stdout')!=b'' and raw('stage-h/owner-control-live.stderr')==b'','live owner raw refusal')
census=j('stage-h/final-census.json');check(sha(raw('stage-h/final-process-census.stdout'))==census['stdout_sha256'],'census raw hash');bindings.append({'stem':'stage-h/final-census','rc':census['rc'],'argv':census['argv'],'stdout_sha256':census['stdout_sha256']})
ret=j('stage-h/retirement-exit-observation.json');check(ret['exec_tool_exit_code']==0 and '522 exact owned roots; 502085226 logical bytes; 129 cache archives preserved' in ret['stdout'],'retirement observation');bindings.append({'stem':'stage-h/retirement-exit-observation','rc':ret['exec_tool_exit_code'],'argv':ret['argv'],'stdout_sha256':sha(ret['stdout'].encode()),'custody':'producer recorded completed exec-tool observation; not standalone raw shell stdout'})
# Open each ancestor with NOFOLLOW; only manifest-listed regular receipt files and
# four explicitly named later delivery records are read. No arbitrary traversal.
fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
for part in pathlib.PurePosixPath(PUB).parts[1:]:
 newfd=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=newfd
external_bytes={};external_meta={}
def external(name):
 check(name not in ['.','..'] and '/' not in name and '\\' not in name,'confined external basename '+name)
 if '/' in name or name in ['.','..']:raise ValueError(name)
 if name in external_bytes:return external_bytes[name]
 f=os.open(name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd);st=os.fstat(f)
 if not stat.S_ISREG(st.st_mode):os.close(f);raise ValueError('not regular '+name)
 with os.fdopen(f,'rb') as h:b=h.read()
 external_bytes[name]=b;external_meta[name]={'bytes':len(b),'sha256':sha(b),'regular':True,'nlink':st.st_nlink};return b
mb=external('manifest.json');check(sha(mb)==MH,'authorized publication manifest SHA');pm=json.loads(mb)
check(pm['final_commit']==F and pm['reviewed_at']==S and pm['directory']==PUB,'publication manifest binding')
check(len(pm['files'])==len({n['path'] for n in pm['files']})==36,'36 publication files')
for n in pm['files']:
 b=external(n['path']);check(len(b)==n['bytes'] and sha(b)==n['sha256'],'external manifest file '+n['path'])
pub=json.loads(external('publication.json'));events=json.loads(external('commands.json'));check(pub['events']==events,'publication/event agreement')
for x in events:
 hs={}
 for stream in ['stdout','stderr']:
  h=sha(external(x[stream+'_file']));check(h==x[stream+'_sha256'],'publication command stream '+x['name']);hs[stream+'_sha256']=h
 check(x['rc']==0 and x['start']<=x['end'],'publication recorded result/time '+x['name']);bindings.append({'stem':'external/'+x['name'],'rc':x['rc'],'argv':x['argv'],'start':x['start'],'end':x['end'],**hs})
check(pub['final_commit']==pub['fixed_at']==F and pub['accepted_D']==D and pub['reviewed_at']==S,'publication final refs')
for p in ['final-tip.stdout','final-head.stdout']:check(external(p).decode()==F+'\n','final HEAD '+p)
check(external('remote-readback.stdout').decode()==F+'\trefs/heads/feature/m6-patches-shipped-689\n','remote final tip')
for p in ['status-before-push.stdout','status-after-push.stdout','final-clean.stdout']:check(external(p)==b'','clean output '+p)
before=json.loads(external('issue-before.stdout'));after=json.loads(external('issue-after.stdout'));check(after['body']==live[689]['issue']['body']==external('issue-689-final-body.md').decode(),'live689 exact final body')
check(boxes(before['body'])==boxes(after['body'])==[' ']*20,'689 criteria unchanged')
changed_body=re.sub(r'^reviewed-at:[ \t]*$', 'reviewed-at: '+S, before['body'],flags=re.M)
changed_body=re.sub(r'^fixed-at:[ \t]*$', 'fixed-at: '+F, changed_body,flags=re.M)
check(changed_body==after['body'],'only 689 ref fields changed')
delivery=json.loads(external('h-delivery.json'));hb=external('h-handback-readback.json');body=external('h-handback-body.md').decode()
check(delivery['publication_manifest_sha256']==MH and delivery['final_commit']==F,'delivery manifest/final refs')
check(sha(hb)==delivery['readback_sha256'],'H readback hash');check(json.loads(hb)['body']==body==comments(689,6587952866),'H exact body/live')
herdr=json.loads(external('herdr-h-handback.json'))
bindings.extend([{'stem':'external/h-post','rc':delivery['post_rc'],'argv':delivery['post_argv'],'custody':'recorded exit; live/readback establishes posted body; no separate post stdout file'},{'stem':'external/h-readback','rc':delivery['readback_rc'],'argv':delivery['readback_argv'],'stdout_sha256':sha(hb)},{'stem':'external/h-herdr','rc':delivery['herdr_rc'],'argv':delivery['herdr_argv'],'stdout_sha256':sha(external('herdr-h-handback.json'))},{'stem':'external/h-final-status','rc':delivery['final_status_rc'],'argv':delivery['final_status_argv'],'custody':'recorded empty-status boolean; no separate raw stdout file at this later time'}])
os.close(fd)
result={'identity':'Codex / OpenAI; session01a19d11-dda5-72e3-86f9-416f36341c24; m6-p1-survey wN:p3','final':F,'accepted_D':D,'seed':S,'errors':errors,'accepted_artifacts':len(accepted),'source_identities':len(source_paths),'changed_paths_since_D':len(delta),'commits_since_D':commits,'owner_matrix':{'native_limits':len(expected_native),'inherited':len(expected_inherited),'unresolved_inherited':22,'contribution_drafts':len(expected_contrib),'PL-01':matrix['PL-01']},'new_command_bindings':bindings,'new_command_exit_counts':dict(collections.Counter(str(x['rc']) for x in bindings)),'retirement':{'roots':len(roots),'logical_file_bytes':sum(r['logical_file_bytes'] for r in roots),'origin_counts':dict(origin_counts),'cache_metadata_count':len(cm['cache_preserved_metadata']),'needed_receipts_committed_at':cm['needed_receipts_committed_at'],'mount_exclusions':len(cc['excluded_filesystems']),'no_fresh_host_or_cache_verification':True},'scan_scope':scan_scope,'external_manifest_sha256':MH,'external_files':external_meta,'artifact_sha256':artifacts,'limits':['Accepted A-D correctness reused, not re-audited; preservation proved by immutable Git mode/blob IDs.','3931 manifest SHA values are producer records; no reread of accepted exported source content.','Retirement and census remain retained-time observations; no live host, cache, archive or deleted-root read. Cache preservation receipt checks inode/size/mtime, not content hashes.','Later H delivery final-status has rc/empty boolean, without separate raw stdout; earlier final-clean raw output is independently hash-bound.','H scoped scan names 126 of 129 final changed paths, excluding its own input manifest/stdout/stderr; recorded input digest is not an independently reconstructed final-byte scan.','Root integration/acceptance, audit criterion3/closure/completion marker, all689 criterion ticks and future1410 fix remain pending.']}
(OUT/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ['errors','accepted_artifacts','source_identities','changed_paths_since_D','commits_since_D','owner_matrix','new_command_exit_counts','retirement']},indent=2));print('bindings',len(bindings),'external_files',len(external_meta));print('results_sha256',sha((OUT/'results.json').read_bytes()))
