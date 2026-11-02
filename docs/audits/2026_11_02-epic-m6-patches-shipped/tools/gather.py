import collections,csv,datetime,hashlib,io,json,pathlib,posixpath,re,subprocess
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689'); A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped'; B=A/'stage-b';B.mkdir(exist_ok=True)
SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1';UP='651150fc88';BASE='c445081a59518f37d9776e5412dd7b14910696f7'
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
def show(path,ref=SEED):return git('show',ref+':'+path)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(path,o):path.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def tree(ref):
 d={}
 for ent in git('ls-tree','-r','-z',ref).split(b'\0'):
  if ent:
   m,p=ent.split(b'\t',1);mode,kind,oid=m.decode().split();d[p.decode()]=dict(mode=mode,kind=kind,oid=oid)
 return d
trees={ref:tree(ref) for ref in [SEED,UP,BASE]};T=trees[SEED];U=trees[UP];O=trees[BASE]
reverse=collections.defaultdict(list)
for p,d in U.items():
 if p.endswith('.patch'):reverse[d['oid']].append(p)
recipes={}; bodies={}
def recipe(p):
 if p in recipes:return recipes[p]
 data=show(p);txt=data.decode(errors='replace');bodies[p]=txt
 fields=[];includes=[];hooks=[]
 for i,line in enumerate(txt.splitlines(),1):
  if re.match(r'\s*(?:PKG_(?:NAME|VERSION|SHA256|URL|SOURCE_NAME|GIT_CLONE_BRANCH|ARCH|TOOLCHAIN|PATCH_DIRS|SKIP_PATCHES)|TARGET_(?:CPU|PATCH_ARCH))\s*=',line):fields.append(dict(line=i,text=line.strip()))
  if re.match(r'\s*\. ',line):includes.append(dict(line=i,text=line.strip()))
  if re.match(r'\s*(?:post_unpack|pre_patch)\s*\(',line):hooks.append(dict(line=i,text=line.strip()))
 rv=dict(path=p,sha256=sha(data),oid=T[p]['oid'],fields=fields,includes=includes,pre_patch_hooks=hooks,upstream='identical' if U.get(p)==T[p] else 'changed' if p in U else 'absent',base='identical' if O.get(p)==T[p] else 'changed' if p in O else 'absent')
 recipes[p]=rv
 for inc in includes:
  m=re.search(r'\$\{ROOT\}/([^"\s]+)',inc['text'])
  if m:
   target=m[1];name=re.search(r'^PKG_NAME=["\']?([^"\'\n]+)',txt,re.M)
   if name:target=target.replace('${PKG_NAME}',name[1])
   if target in T and target.endswith('package.mk'):recipe(target)
 return rv
def recipe_paths(path):
 if path.startswith('projects/ROCKNIX/patches/'):
  name=path.split('/')[3];return sorted(p for p in T if p.endswith('/'+name+'/package.mk'))
 pre=path.split('/patches/')[0];p=pre+'/package.mk'
 if p in T:return [p]
 while pre and pre!='.':
  pre=posixpath.dirname(pre);p=pre+'/package.mk'
  if p in T:return [p]
 return []
rows=json.loads((A/'stage-a/seed/rows.json').read_text()); native=[]
for i,row in enumerate(rows,1):
 p=row['path'];literal=show(p);resolved=p;target=None
 if T[p]['mode']=='120000':target=literal.decode();resolved=posixpath.normpath(posixpath.join(posixpath.dirname(p),target))
 data=show(resolved);txt=data.decode(errors='replace');lines=txt.splitlines();h=[]
 for ln,line in enumerate(lines,1):
  if line.startswith(('diff ','--- a/','--- /dev/null','Index:','+++ ')):break
  h.append(dict(line=ln,text=line))
 targets=[dict(line=n,text=s) for n,s in enumerate(lines,1) if s.startswith(('--- ','+++ ','diff --git ','Index:','rename from','rename to'))]
 ids=recipe_paths(p)
 for f in ids:recipe(f)
 status='identical' if U.get(p)==T[p] else 'changed' if p in U else 'same-blob-elsewhere' if reverse.get(T[p]['oid']) else 'absent'
 native.append(dict(index=i,path=p,mode=T[p]['mode'],oid=T[p]['oid'],sha256=sha(literal),link_target=target,referent=resolved,patch_sha256=sha(data),inventory_lines=row['lines'],plans=row['reachable_by'],fork_written=row['tier_note']=='fork-written',header=h,targets=targets,hunks=sum(s.startswith('@@') for s in lines),recipes=ids,upstream_status=status,upstream_counterparts=reverse.get(T[p]['oid'],[]),base_status='identical' if O.get(p)==T[p] else 'changed' if p in O else 'absent',render_required=sorted(set(re.findall(r'@(DEVICE|TARGET_CPU)@',txt))),backend='git apply' if re.search(r'^GIT binary patch$|^rename from|^rename to',txt,re.M) else 'patch'))
inherited=[]
for i,lead in enumerate(csv.DictReader(io.StringIO((R/'docs/qa-logs/2026-11-02-m6-resume/t42-inherited/leads.tsv').read_text()),delimiter='\t'),1):
 p=lead['patch'];rp=lead['override']+'/package.mk';recipe(rp);data=show(p)
 inherited.append(dict(index=i,patch=p,override=lead['override'],sha256=sha(data),oid=T[p]['oid'],recipe=rp,owner=lead['recipe_owner'],prior_evidence=lead['prior_evidence'],patch_text=data.decode(errors='replace'),upstream_status='identical' if U.get(p)==T[p] else 'changed' if p in U else 'absent'))
dump(B/'native-inputs.json',native);dump(B/'inherited-inputs.json',inherited);dump(B/'recipes.json',recipes)
digest=[]
for n in native:
 subject=' / '.join(x['text'] for x in n['header'] if x['text'].startswith(('Subject:','From:','Date:')))
 if not subject:subject='NO MAIL HEADER; '+ ' / '.join(x['text'] for x in n['header'][:3])
 pins='; '.join(f+': '+ ', '.join(v['text'] for v in recipes[f]['fields'] if v['text'].startswith('PKG_VERSION')) for f in n['recipes'])
 digest.append(f"{n['index']:03d} {n['path']}\n  {subject}\n  target: {'; '.join(x['text'] for x in n['targets'])[:1600]}\n  recipe: {pins}; upstream {n['upstream_status']}; base {n['base_status']}; hunks {n['hunks']}; rendering {n['render_required']}\n")
(B/'native-reading.txt').write_text('\n'.join(digest))
(B/'fork-written-reading.txt').write_text('\n'.join(f"\n{n['index']:03d} {n['path']}\n"+'\n'.join(f'{i}: {line}' for i,line in enumerate(show(n['path']).decode().splitlines(),1)) for n in native if n['fork_written']))
(B/'inherited-reading.txt').write_text('\n'.join(f"\nI{n['index']:02d} {n['patch']} -> {n['override']} ({n['owner']})\n{n['patch_text']}\nRECIPE (selected metadata and source; secret-shaped lines omitted):\n"+'\n'.join(f'{i}: {line}' for i,line in enumerate(bodies[n['recipe']].splitlines(),1) if not re.search('key|pass|token|user|psk',line,re.I)) for n in inherited))
(B/'recipes-reading.txt').write_text('\n'.join(p+'\n'+'\n'.join(str(v['line'])+': '+v['text'] for v in d['fields']+d['includes']+d['pre_patch_hooks']) for p,d in sorted(recipes.items())))
summary=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),native=len(native),inherited=len(inherited),recipes=len(recipes),native_upstream=dict(collections.Counter(n['upstream_status'] for n in native)),native_base=dict(collections.Counter(n['base_status'] for n in native)),missing_recipe=[n['path'] for n in native if not n['recipes']],no_mail_header=sum(not any(x['text'].startswith('From:') for x in n['header']) for n in native),fork_written=sum(n['fork_written'] for n in native))
dump(B/'gather-summary.json',summary)
with (A/'00-running-log.md').open('a') as f:f.write(f"\n### {summary['utc']} — B immutable source extraction\n\nPROOF: B-01 (source-read) — stage-b/native-inputs.json and inherited-inputs.json bind each raw patch to its immutable Git identity, header/target digest, recipe candidates and fixed-upstream/base comparison. This extracts source metadata, not source archives, and does not evaluate shell recipes. Human assessment follows; no application or correctness PASS is inferred.\n")
with (A/'02-forward-audit.md').open('w') as f:f.write(f'''# T42 forward audit (#689)

Auditor: Codex / openai/gpt-6-astra / xhigh. reviewed-at: {SEED}.

## First observations before prior-verdict comparison

{summary['utc']}. scripts/unpack:126–196 selects recipe-dependent stacks and renders DEVICE/TARGET_CPU for the ordinary backend; config/functions:1057–1088 prefers local overrides and rejects ambiguity. Therefore a historical survey reach row and an unapplied generic patch are questions, not proof of current application or a missing fix. Stage-b immutable metadata records header claims separately from fixed-upstream equality. The current table has {summary['no_mail_header']} native identities without a From header (links resolved); that is a provenance limitation, not by itself a defect. Prior per-criterion audit files have not been opened yet. Runtime costs and both time-to-play measurements are unmeasured in this source-only pass.

## Coverage boundary

All 384 Git patch identities are metadata-extracted; 50 inherited patches are separately bound. Planned human reading is header/target/recipe/currency assessment for native rows, full lines for the 12 fork-written patches, and individual intent/feature/pin comparison for inherited rows. No claim to line-by-line reading of all 71,387 native lines. Completion of those readings is recorded separately from this extraction.
''')
print(json.dumps(summary,indent=2))
