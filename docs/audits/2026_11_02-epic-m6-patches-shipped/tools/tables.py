"""Generate and assert the T42 native/inherited tables from retained receipts."""
import pathlib,json,subprocess,hashlib,collections,datetime,copy,re,sys
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';B=A/'stage-b';C=A/'stage-c';SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def nonempty(x):return isinstance(x,str) and bool(x.strip())
def cell(x):return str(x).replace('|','&#124;').replace('\n','<br>').replace('\r','')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(cell(x) for x in row)+' |\n' for row in rows)
def header(n):
 claim=' / '.join(x['text'] for x in n['header'] if x['text'].startswith(('From:','Author:','Date:','Subject:')))
 return ('header claim: '+claim if claim else 'No mail attribution; original author unknown')+'; full literal header in native-inputs.json; source custody is the immutable Git blob, not verified external integration'
native_inputs=load(B/'native-inputs.json');inherited_inputs=load(B/'inherited-inputs.json');groups=load(B/'selection.json');groupmap={g['id']:g for g in groups};app={g['id']:load(B/'application'/f"{g['id']}.json") for g in groups};inherited=load(B/'inherited-decisions.json');hunks=load(B/'inherited-hunks.json');fork=load(B/'fork-written-observations.json')
currency={x['recipe']:x for x in load(B/'recipe-currency.json')}
rank={'applies':0,'offset':1,'fuzz':2,'open-item':3,'blocked':4,'fails':5};native=[];coverage=[];application_review=[]
for n in native_inputs:
 related=[g for g in groups if n['path'] in g['native']];pins=[];orders=[];results=[];receipts=['stage-b/native-inputs.json','stage-b/selection.json','stage-b/recipe-currency.json'];rawstatus=[]
 for g in related:
  m=g['metadata'];pin=m['values'].get('PKG_VERSION','unknown: static pin not established');pins.append(f"{g['plan']}: {g['recipe']} @ {pin}")
  positions=[str(i+1) for i,s in enumerate(g['stack']) if s['path']==n['path']];orders.append(f"{g['id']} {g['plan']}: {','.join(positions) or 'unresolved selection'}/{len(g['stack'])}; "+('conditional: '+'; '.join(m['stack_unknown']) if m['stack_unknown'] else 'C-order explicit unpack stack'))
  rr=[r for r in app[g['id']]['rows'] if r['path']==n['path']];r=rr[0] if rr else None;receipt=f"stage-b/application/{g['id']}.json";receipts.append(receipt)
  if r:
   status=r['status'];why=r.get('reason','normal rc 0; target-projection source only; no correctness/runtime claim')
  else:
   status='open-item';why='candidate created a safe relative UCM symlink; regular-file snapshot guard stopped before serializing normal rc. First patch remains recorded; this and later stack rows unclaimed.'
   assert g['id'] in ['G202','G203'],'unexplained missing application row'
  if status=='open-item' and r and not why.strip():why='regular-file output guard stopped at a generated UCM symlink; no normal rc receipt'
  rawstatus.append(status);results.append(f"{g['id']}: {status}; {why}; [{receipt}]({receipt})")
 recipe_currency='; '.join(p+': '+json.dumps(currency[p]['versions'],sort_keys=True) for p in sorted({g['recipe'] for g in related}))
 status=max(rawstatus,key=rank.get);disp='open-item' if status in ['open-item','blocked'] else 'bug' if status=='fails' else 'keep'
 if n['upstream_status']=='changed' and disp=='keep':disp='upstream-changed'
 if n['upstream_status']=='same-blob-elsewhere':disp='upstream-moved'
 if n['fork_written'] and disp=='keep' and '/themes/' not in n['path']:disp='#585'
 if n['index']==271:disp='bug'
 subj=' / '.join(x['text'][9:] for x in n['header'] if x['text'].startswith('Subject: '))
 reason=subj or pathlib.PurePosixPath(n['path']).name.removesuffix('.patch').replace('-',' ').replace('_',' ')
 reason='Recorded intent: '+reason+'. Preserve current behavior until its owner qualifies a replacement; title/header alone does not prove correctness.'
 targets=list(dict.fromkeys(x['text'] for x in n['targets']))
 if not targets:
  data=git('show',SEED+':'+n['referent']).decode();targets=[l for l in data.splitlines() if l.startswith(('*** a/','--- b/','diff --git '))]
 origin=git('log','-1','--format=%H %aI %an %s',SEED,'--',n['path']).decode().strip()
 row=dict(path=n['path'],mode=n['mode'],oid=n['oid'],sha256=n['sha256'],referent=n['referent'],referent_sha256=n['patch_sha256'],link_target=n['link_target'] or 'not a symlink',inventory_lines=n['inventory_lines'],plans=n['plans'],origin_header=header(n),last_path_commit=origin,targets='; '.join(targets) or 'open item: target syntax requires manual parser',target_version='; '.join(pins),recipe_pin_per_plan='; '.join(pins),order_context='; '.join(orders),application='; '.join(results),application_status=status,upstream_status=n['upstream_status'],upstream_evidence=f"fixed 651150fc88: {n['upstream_status']}; fixed base c445081a59518f37d9776e5412dd7b14910696f7: {n['base_status']}; identical blob counterparts: "+(', '.join(n['upstream_counterparts']) or 'none')+'; literal recipe pin comparison '+recipe_currency,backport_status='No component-upstream adoption claim. Header dates/URLs are unverified external claims; fixed ROCKNIX Git equality is separately recorded.',carrying_reason=reason,disposition=disp,owner='#689 T42 comparison owner; recipe-owner follow-up before any change'+('; #677 standalone-emulator owner, new reactive bug required' if n['index']==271 else '; #585 contribution draft only' if n['fork_written'] else '; #559/#563 integration owner' if n['upstream_status']!='identical' else ''),receipts=list(dict.fromkeys(receipts)))
 native.append(row);coverage.append(dict(path=n['path'],mode=n['mode'],oid=n['oid'],read='Path/header/target/currency digest and static recipe metadata; full 1-'+str(n['inventory_lines'])+' patch lines read' if n['fork_written'] else 'Path/header/target/currency digest and static recipe metadata; not a full patch-code review',evidence='stage-b/native-read-assessment.json; stage-b/native-inputs.json'+('; stage-b/fork-written-observations.json' if n['fork_written'] else ''),limits='Target-projection application is a separate result; neither full component correctness nor runtime efficiency certified.'))
for row in inherited:
 h=next(x for x in hunks if x['index']==row['index']);row['target_pins']='; '.join(s['pin']+(' ('+pathlib.Path(s['receipt']).stem+')') for s in h['source']);row['counterpart_source_evidence']='stage-b/inherited-hunks.json I%02d: '%row['index']+'; '.join('counterpart '+c['path']+'; '+c['kind'] for c in h['counterparts']) if h['counterparts'] else 'Individual source-hunk and target records: stage-b/inherited-hunks.json I%02d; manual version/feature judgment above; full pair deltas in stage-b/pair-diffs.json'%row['index'];row['evidence']+=['stage-b/pair-diffs.json']
for f in fork:
 n=next(x for x in native if x['path']==f['path']);f['application']=n['application_status']+'; per-plan receipts in native provenance';f['source_trace']=n['targets']+'; exact pin(s) '+n['recipe_pin_per_plan'];f['prior_evidence']='Patch header and recorded Git history: '+n['last_path_commit']+'; historical evidence retains its original scope, never a new test';f['contribution']='DRAFT #585 only: '+f['reading']+' Verify component upstream, attribution and focused reproduction before any submission.' if '/themes/' not in f['path'] else 'Fork branding/presentation; no generic upstream submission proposed. Preserve setting identifiers and separate theme owner evidence.'
payload={'native':native,'coverage':coverage,'inherited':inherited,'fork_written':fork}
REQUIRED_NATIVE=['origin_header','last_path_commit','targets','target_version','recipe_pin_per_plan','order_context','application','application_status','upstream_status','upstream_evidence','backport_status','carrying_reason','disposition','owner']
def validate(data):
 ns=data['native']; expected={n['path']:n for n in native_inputs};keys=[x['path'] for x in ns]
 assert len(keys)==384 and len(set(keys))==384 and set(keys)==set(expected),'native membership assertion'
 cov=data['coverage'];assert len(cov)==384 and {x['path'] for x in cov}==set(expected),'coverage membership assertion'
 ik=[(x['patch'],x['override']) for x in data['inherited']];wanted={(x['patch'],x['override']) for x in inherited_inputs}
 assert len(ik)==50 and len(set(ik))==50 and set(ik)==wanted,'inherited unique-key assertion'
 assert len({x['override'] for x in data['inherited']})==26,'inherited override assertion'
 for n in ns:
  e=expected[n['path']];assert (n['mode'],n['oid'],n['sha256'])==(e['mode'],e['oid'],e['sha256']),'native byte/mode assertion'
  assert n['referent']==e['referent'] and n['referent_sha256']==e['patch_sha256'],'symlink referent identity assertion'
  assert n['origin_header']==header(e),'header attribution assertion'
  assert all(nonempty(n[k]) for k in REQUIRED_NATIVE),'nonempty native fields assertion'
  assert n['disposition'] in ['keep','upstream-changed','upstream-moved','superseded-at-pin','bug','#585','inherited','open-item'],'native disposition assertion'
  assert re.search(r'#\d+',n['owner']),'native owner assertion'
  assert n['application_status'] in rank,'application classification assertion'
  assert n['receipts'] and all((A/p).is_file() for p in n['receipts']),'native receipt links assertion'
 for n in data['inherited']:
  assert n['conclusion'] in ['already-carried','absorbed-at-pin','not-applicable-with-reason','change-needed-with-trace','unresolved-with-specific-evidence-needed'],'inherited conclusion assertion'
  assert all(nonempty(n[k]) for k in ['prior_recipe_owner','target_pins','feature_architecture_and_intent','counterpart_source_evidence','prior_base_disposition','remaining_owner_action']),'nonempty inherited fields assertion'
  assert re.search(r'#\d+',n['remaining_owner_action']),'inherited owner assertion'
  assert all((A/p).is_file() for p in n['evidence']),'inherited receipt links assertion'
 assert len(data['fork_written'])==12 and sum(f['logical_lines'] for f in data['fork_written'])==498,'fork-written population assertion'
 assert all(f['read_lines']=='1-'+str(f['logical_lines']) for f in data['fork_written']),'full-line range assertion'
 assert len(list((A/'second-opinions').iterdir()))==1,'Local one-file second-opinions assertion'
 return True
C.mkdir(exist_ok=True);controls=[]
for name,assertion,mutate in [
 ('removed-native','native membership assertion',lambda d:d['native'].pop()),
 ('duplicate-inherited','inherited unique-key assertion',lambda d:d['inherited'].append(copy.deepcopy(d['inherited'][0]))),
 ('altered-referent','symlink referent identity assertion',lambda d:next(n for n in d['native'] if n['mode']=='120000').update(referent_sha256='0'*64)),
 ('fabricated-attribution','header attribution assertion',lambda d:d['native'][0].update(origin_header='From: Fabricated Author <fabricated@example.invalid>'))]:
 d=copy.deepcopy(payload);mutate(d)
 try:validate(d)
 except AssertionError as e:
  assert str(e)==assertion,(name,str(e));controls.append(dict(control=name,expected=assertion,observed=str(e),rejected=True,exception_type="AssertionError"));print('EXPECTED FAIL',name,str(e))
 else:raise AssertionError('negative control unexpectedly passed '+name)
validate(payload);print('PASS native 384 / inherited 50 / overrides 26 / fork-written 12:498; four fail-first controls')
dump(C/'negative-controls.json',controls);dump(B/'tables.json',payload);dump(B/'fork-written-observations.json',fork)
stats={'native_disposition':dict(collections.Counter(n['disposition'] for n in native)),'native_application':dict(collections.Counter(n['application_status'] for n in native)),'inherited_conclusion':dict(collections.Counter(n['conclusion'] for n in inherited)),'application_groups':len(groups),'raw_native_application_limit':'one status per native path takes the worst of its per-plan rows; source target projections only','native_paths':384,'inherited_keys':50}
assert sum(stats['native_disposition'].values())==sum(stats['native_application'].values())==384;assert sum(stats['inherited_conclusion'].values())==50;dump(B/'table-counts.json',stats)
intro=(A/'02-forward-audit.md').read_text().split('## Provenance')[0]
out=intro+'\n## Provenance\n\n384 native keys. Headers are literal claims. Source pins are static reads, not executed configurations. The full input/receipt data is [tables.json](stage-b/tables.json); [selection.json](stage-b/selection.json) preserves all context siblings and the exact order. Application trees are projections of needed source members, not complete source trees. Unknown pre-patch hooks, feature branches and checksums remain explicit. No external URL was followed.\n\n'
out+=table(['Path','Mode / link','Lines / plans','Origin / header','Target / recipe pin per plan','Order / context','Application / receipt','Currency / backport','Carrying reason','Disposition / owner'],[(n['path'],n['mode']+'; '+n['link_target']+'; referent '+n['referent']+' sha256 '+n['referent_sha256'],str(n['inventory_lines'])+'; '+', '.join(n['plans']),n['origin_header']+'; '+n['last_path_commit'],n['targets']+'; '+n['recipe_pin_per_plan'],n['order_context'],n['application'],n['upstream_evidence']+'; '+n['backport_status'],n['carrying_reason'],n['disposition']+'; '+n['owner']) for n in native])
out+='\n## Coverage\n\nA separate exact 384-key table; only the twelve fork-written members claim every patch line was read.\n\n'+table(['Path','Mode / blob','Read','Evidence / limits'],[(n['path'],n['mode']+' '+n['oid'],n['read'],n['evidence']+'; '+n['limits']) for n in coverage])
out+='\n## Inherited comparisons\n\nExactly 50 frozen keys / 26 overrides, separate from native coverage. The other 24 T40 rows remain excluded: two strict duplicates, four symlink-applied, eighteen carried another way. Recipe acceptance does not answer adoption. `already-carried` describes the specific current-pin intent stated in the row, not a claim that every newer generic hunk is byte-identical.\n\n'+table(['Key / override','Prior owner / base disposition','Actual pin','Feature, architecture and generic intent','Counterpart / source evidence','Conclusion / remaining owner'],[(f"I{n['index']:02d} {n['patch']} → {n['override']}",n['prior_recipe_owner']+'; '+n['prior_base_disposition'],n['target_pins'],n['feature_architecture_and_intent'],n['counterpart_source_evidence'],n['conclusion']+'; '+n['remaining_owner_action']) for n in inherited])
out+='\n## Fork-written reading\n\nAll twelve members / 498 logical lines, including Dolphin. Contribution text is draft only and was not posted to #585.\n\n'+table(['Path / full range','Intent / reader','Source trace / application','Prior evidence','Owner / contribution'],[(n['path']+' '+n['read_lines']+' ('+str(n['logical_lines'])+')',n['reading']+'; '+n['reader'],n['source_trace']+'; '+n['application'],n['prior_evidence'],n['owner']+'; '+n['contribution']) for n in fork])
out+='\n## Symlink boundary\n\n'+table(['Native path','Literal target','Resolved source','Ownership'],[(n['path'],n['link_target'],n['referent']+' sha256 '+n['referent_sha256'],'T43 referent is context only; native link remains T42' if '/mangohud/' in n['path'] else 'T42 link; shared vitaquake2 referent counted once by its own native key') for n in native if n['mode']=='120000'])
out+='\n## Application guard observations\n\nThe partial-failure fixture changed a candidate, kept the successful prefix unchanged and blocked its successor. [Receipt](stage-b/application/partial-failure-control.json). G202/G203 stopped on the regular-file snapshot assertion after a patch created a relative UCM symlink; later rows are open, and the unrecorded normal exit is not reconstructed. WebKit/Samba archives were withheld for duplicate members. Those are runner coverage limits, not product defects. Hook references in the v1 selection manifest are character offsets; actual line references are in recipes.json. No shell recipe or config was evaluated.\n'
(A/'02-forward-audit.md').write_text(out)
print(json.dumps(stats,indent=2))

with (A/"02-forward-audit.md").open("a") as findings_out:
 findings_out.write("\n## Findings index\n\n| bucket | reader | finding | severity | result |\n| --- | --- | --- | --- | --- |\n| native 271 | gpt | F-T42-01 | Medium | PPSSPP nested patch is inert as SDL transformation; PL-01 / #1410 |\n\n## Verification\n\n### F-T42-01 (gpt, primary Local reader)\n\n**Verdict:** **confirmed, Medium**. Seed PPSSPP 007 lines 11–16 create a nested file; lines 17–29 add the intended SDL diff as text. scripts/unpack:191–196 applies the outer file once; recipe post_unpack does not apply the nested file. The constructed fixture in stage-b/nested-patch/receipt.json returns normal rc 0, creates the nested target and leaves sentinel SDLJoystick.cpp unchanged. This is a source-format mechanism proof, not an at-pin or runtime result. Fixed upstream's direct diff uses NKCODE_GUIDE, whereas the nested seed payload uses NKCODE_UNKNOWN. Owner must resolve intended behavior in the separate fix #1410; audit #1411 / PL-01 remains open pending coordinator disposition. Source and negative duplicate searches are retained in stage-b/source-context/.\n")
