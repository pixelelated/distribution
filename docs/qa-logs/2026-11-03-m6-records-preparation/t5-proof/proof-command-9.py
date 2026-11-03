import json,hashlib,ast,os,re,subprocess,datetime,traceback
from pathlib import Path
p=Path('/tmp/m6-t46-records-proof-t5-20261103'); repo=Path('/workspace/tmp/m6-t46-proof-t5-20261103/repo'); ref='e9d512a230cf8dbd2cd985ae7984a6ef7eb9f9fc'
assert set(os.sched_getaffinity(0))==set(range(8,24))
def sha(b):return hashlib.sha256(b).hexdigest()
receipts=[]; result={}
def git(*args):
 q=subprocess.run(['git',*args],cwd=repo,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));receipts.append({'argv':q.args,'rc':q.returncode,'stdout_bytes':len(q.stdout),'stdout_sha256':sha(q.stdout),'stderr_sha256':sha(q.stderr)});assert q.returncode==0,q.stderr;return q.stdout
src=(p/'lint-audit-artifacts.py').read_text();tree=ast.parse(src);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='check_review_plan')
print('ACTUAL LOCAL INTERFACE FUNCTION\n',ast.get_source_segment(src,function))
ns={'json':json,'hashlib':hashlib,'re':re,'os':os,'Path':Path,'subprocess':subprocess,'datetime':datetime};exec(compile(ast.Module(body=[function],type_ignores=[]),'<immutable check_review_plan>','exec'),ns)
fixture=p/'2026_11_03-issue-t46-interface-proof';(fixture/'second-opinions').mkdir(parents=True)
base={'schema_version':1,'depth':'local','primary':{'harness':'Codex','model':'openai/gpt-6-astra','lab':'openai','identity_source':'Actual harness model label GPT-6-Astra; normalized namespace for lint only; no provider call or attestation','effort':'xhigh'},'reviewers':[]}
cases=[('namespaced-local',base),('display-label-local',{**base,'primary':{**base['primary'],'model':'GPT-6-Astra'}}),('reviewer-count',{**base,'reviewers':[{'member':'gpt'}]})]
checks={}
for name,plan in cases:
 (fixture/'second-opinions/review-plan.json').write_text(json.dumps(plan,indent=2)+'\n');bad=[];ok=[]
 try:ns['check_review_plan'](fixture,False,bad.append,ok.append);checks[name]={'bad':bad,'ok':ok}
 except Exception:checks[name]={'exception':traceback.format_exc()}
(p/'local-interface-results.json').write_text(json.dumps(checks,indent=2)+'\n');result['local_interface']=checks
result['epic_local_exception_expression']=[ast.unparse(n.value) for n in ast.walk(function) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='tier_exception' for t in n.targets)]
# Newly authored tiny range fixtures only: never open a historical day-log target.
range_fixture='# Work log 2026-11-03\n\n## 16:00 UTC — later clock time\nfirst body\n## 09:00 UTC — final entry in file\nlast body\n### Details\nnested body\n## Untimed appendix\nappendix body\n'
lines=range_fixture.splitlines();headings=[(i+1,len(m[1]),m[2]) for i,line in enumerate(lines) if (m:=re.fullmatch(r'(#{1,6}) +(.*)',line))]
ts=[h for h in headings if re.search(r'\b\d\d:\d\d UTC\b',h[2])]
last=ts[-1];stop=next((ln for ln,level,title in headings if ln>last[0] and level<=last[1]),len(lines)+1)
result['range_fixture']={'only_synthetic':True,'last_in_file_start':last[0],'exclusive_next_heading':stop,'inclusive_selected_range':[last[0],stop-1],'chronological_latest_start':max(ts,key=lambda h:re.search(r'\b\d\d:\d\d',h[2])[0])[0],'ambiguities':['last means file order or timestamp maximum','through next heading includes boundary heading or stops before it','no timestamp / fenced pseudo-heading / same timestamp fallback must be explicit']}
(p/'synthetic-range.md').write_text(range_fixture)
# Metadata route selector probes are new; no execution of retained extractor/classifier.
prefixes=['docs/qa-logs','docs/qa-frames','docs/audits','docs/work-logs','docs/retros','docs/retrospective','docs/futros','research','.github/sessions']
selected=lambda x:x=='docs/reviews/inventory.json' or any(x==r or x.startswith(r+'/') for r in prefixes)
selector_cases={'docs/retros':True,'docs/retros/a.md':True,'docs/retrospective/a.md':True,'docs/retrospective-other/a.md':False,'docs/reviews/inventory.json':True,'docs/reviews/inventory.json/extra':False,'t43-final/':False}
assert all(selected(k)==v for k,v in selector_cases.items());result['selector_tiny_cases']=selector_cases
# Exact live-body criteria reconciliation, no issue or repo writes.
issue=json.loads((p/'issue-693.stdout').read_bytes());brief=(p/'brief.stdout').read_text();sec=brief.split('## 7. Acceptance criteria',1)[1].split('\n## ',1)[0]
bc=[re.sub(r'^\d+\.\s*','',s).strip() for s in sec.splitlines() if re.match(r'^\d+\.\s',s)]
ic=[re.sub(r'^-\s*\[[ xX]\]\s*','',s).strip() for s in issue['body'].splitlines() if re.match(r'^-\s*\[[ xX]\]',s)]
result['criteria']={'brief_count':len(bc),'issue_count':len(ic),'literal_equal':bc==ic,'differences':[{'number':i+1,'brief':b,'issue':c} for i,(b,c) in enumerate(zip(bc,ic)) if b!=c]}
# Retained census group totals / historical values reused, not generator replay.
groups=json.loads((p/'inputs/root-input-groups.json').read_bytes());t3=json.loads((p/'inputs/t3-report.json').read_bytes())
assert len(groups)==10 and sum(v['paths'] for v in groups.values())==127469 and sum(v['logical_bytes'] for v in groups.values())==2190843187
result['ten_roots']={k:{'paths':v['paths'],'logical_bytes':v['logical_bytes']} for k,v in groups.items()}
result['historical_denominators']={'survey_rows':t3['reused_survey']['selected_rows'],'stored_lines':t3['reused_survey']['inventory_lines'],'generated_read_lines_not_budget':t3['reused_survey']['generated_read_lines'],'inventory_self_stored_lines':t3['inventory_self']['stored_row_reused']['lines'],'delta':{k:t3['delta'][k] for k in ['added','deleted','changed','unchanged']}}
# Preserve opaque old deletions: never fetch their paths or blobs.
for ep in json.loads((p/'inputs/p1-routes/entrypoints.json').read_bytes()):
 raw=git('ls-tree','-l','-z',t3['pins']['current_candidate'],'--',ep['path']); head,path=raw.rstrip(b'\0').split(b'\t',1);mode,kind,oid,size=head.split()
 expected=ep['git'];assert mode.decode()==expected['mode'] and kind.decode()==expected['type'] and oid.decode()==expected.get('oid',expected.get('blob')) and int(size)==expected.get('bytes',expected.get('size'))
result['entrypoint_metadata_readbacks']=10
print('RESULT',json.dumps(result,indent=2))
(p/'proof-09.json').write_text(json.dumps(result,indent=2)+'\n');(p/'command-09.json').write_text(json.dumps(receipts,indent=2)+'\n')
# Store an exact rerunnable own-proof script; never invoke accepted producers from it.
own=Path(__file__).read_bytes() if '__file__' in globals() and Path(__file__).is_file() else b''
report="""T5 → wN:p2: bounded T46 v1 unfamiliar-executor proof

Actual harness: Codex / GPT-6-Astra / xhigh / OpenAI, /root; existing T5 m6-t5-build-engine wN:p7, session 01a19d12-3d7a-7642-9108-ae06a719cdd7. No provider attestation.
Authority: #693 comment6602867918, read full #693 and #1415 including kickoff.
Candidate e9d512a230cf8dbd2cd985ae7984a6ef7eb9f9fc.
Brief SHA256 caa0c9f2afe657770093b4fb502512dcc331eb47dd17c66063229c9f99ef931f.
Input helper SHA256 c4fd76fb059d6b2a59efe51db1f4527f5e21f986b9fadd0be014ccf0028f000b.

Concrete corrections before dispatch:
1. inputs.py resolves commit but check() binds tree and metadata only. Tiny private commit4518a3a09bbc234693879c465e4308e47fb92d99 has the same source tree and was accepted (rc0). Enforce resolved commit == SOURCE if exact source-commit identity is the contract; otherwise explicitly describe tree-equivalent acceptance. The literal prescribed d707c82 command itself passes.
2. Supply exact Local review-plan JSON model spelling and tier exception fields. Actual check_review_plan requires primary.model.split('/',1)[0] == primary.lab: display label GPT-6-Astra with lab openai is rejected, whereas openai/gpt-6-astra is a normalization of the actual harness label, not provider attestation. See local-interface-results.json and proof-09.json for actual fixture outcomes and the exact Epic exception expression. Preserve actual primary, effort and identity source; never label this an independent reviewer.
3. Make the 86-day-log selection deterministic before execution: define supported timestamp-heading syntax, file-order versus clock-order meaning of 'last', inclusive/exclusive end, and no-match/fenced-heading fallback. Synthetic range fixture demonstrates file-order start5 vs chronological start3 and next-heading boundary9. Recommend last supported timestamp heading in file order, through line before the next same-or-higher heading or EOF, otherwise explicit unknown/escalation. This is a brief ambiguity, not a historical-record finding.

Verified:
- Literal membership block rc0, exact expected PASS127469/2190843187/10roots. Modes98024/29445; 38355 unique blobs /1084128032 unique logical bytes. Source d707c82/root b3ce6c6; execution seed remains prospective; new candidate/output files are not retrospectively added to source.
- Own in-memory missing/extra/mode/blob/size/canonical-input/root-drift refusals pass. Tiny empty-subtree commitd70f40ce819972e558d73dab0547911a1f5d1287 has identical selected leaves and is rejected rc1 by root identity. Root seven retained binding negatives remain distinct from these new probes and from future audit-table/link/confinement obligations.
- All14 original P1 files verified against retention.json; documentary TSV reconstructed from UTF-8 JSON only in memory and original SHA/bytes match. Root retained five-output equality receipts are all true; accepted extractor not rerun.
- Independent join of retained routes and supplied selector matches root rows exactly:95occurrences/89targets,88blobs/1directory.86 unique anchorless INDEX day links; other targets are historical next handoff, inventory singleton and retros directory. Ten entrypoint metadata identities read back. 13 unresolved shorthands,67dynamic/glob examples,6schematic layouts and8suppressed occurrences stay qualified. No guessed base, recursion, external fetching or hidden-name recovery.
- T39 cutoff metadata readback48/48 matches retained pre-correction identities. Accepted-source/completion equality and root192-comparison receipt reused; no historical body or accepted producer replay. T39 remains accepted integration-pending under #686/#807/#346; D223/D224/#1407 retains33/2770,32edit-scope plus unchanged table-only plan.
- Tool interfaces inspected at candidate, no final gates run. Retained --help results distinguish unsupported flags and accidental actual checks; initial whitespace rc2 remains separate from full tracked scan rc0 and later correction. work-log-index --write/--check; ceremony-check --gate; forbidden-terms-check REPO/--stdin; lint --phase pre-issue FOLDER then resolution / --issue N; box-check --issue N.
- Root owns final brief/criteria/seed/dispatch/acceptance/integration. T3 has not been started. Prospective A-D stop remains published D; later E-H needs dispatch. This proof neither satisfies the future audit reading floor nor its table/link/confinement validation.

Limits and command accounting:
Ten top-level commands total including two failed own read/display attempts (#05 scalar-shape recursion, #07 locally missing retained extract.py; both before substantive controls and recovered). #04 is the literal block in one pinned shell invocation. #09 uses only the actual isolated Local review-plan function on new tiny JSON, not full audit lint/gates. #10 is this final Herdr delivery. Per-command receipts and own proof scripts accompany this return.
Private metadata clone: /workspace/tmp/m6-t46-proof-t5-20261103/repo, --shared --no-checkout --no-tags --no-hardlinks. Only named small helper/text/JSON copies and tiny synthetic Git objects, no source checkout/export/fetch. Small text/JSON proof directory: /tmp/m6-t46-records-proof-t5-20261103. All subprocesses CPUs8-23. Read-only actual root m6-renovation-plan-346; historical launch/T38/T42 untouched.
No audit, target historical day/audit/QA body reads, accepted generator/parser/test replay, tracker/repository/shared-ref/kit changes, cleanup/integration/final scans/gates, host/cache/process/private/retained-root inspection, runtime/build/guest/provider/device/cloud action, or permission answers. Stop after handback.
"""
report+='\nActual Local fixture results:\n'+json.dumps(checks,indent=2)+'\nEpic exception expression:\n'+json.dumps(result['epic_local_exception_expression'])+'\nCriteria reconciliation:\n'+json.dumps(result['criteria'],indent=2)+'\n'
(p/'RETURN.md').write_text(report)
manifest=[]
for file in sorted(p.rglob('*')):
 if file.is_file() and file.name not in ['MANIFEST.sha256','delivery.json','hashes.json']:manifest.append(sha(file.read_bytes())+'  '+str(file.relative_to(p)))
(p/'MANIFEST.sha256').write_text('\n'.join(manifest)+'\n')
hashes={n:sha((p/n).read_bytes()) for n in ['RETURN.md','proof-08.json','proof-09.json','MANIFEST.sha256']};(p/'hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');print('HANDBACK HASHES',json.dumps(hashes))
