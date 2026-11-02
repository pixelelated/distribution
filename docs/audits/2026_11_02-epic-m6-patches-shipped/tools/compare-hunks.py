"""Whole unified-hunk comparisons. Identity and unknowns are explicit."""
import pathlib,re,json,subprocess,hashlib,datetime,collections
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';B=A/'stage-b';SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
def blob(p,ref=SEED):return subprocess.check_output(['git','-C',str(R),'show',ref+':'+p]).decode()
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def hunks(txt):
 ls=txt.splitlines();out=[];target=None;i=0
 while i<len(ls):
  l=ls[i]
  if l.startswith('diff --git '):
   target=l.split()[3].split('/',1)[1]
  if l.startswith('+++ '):
   raw=l[4:].split()[0];target=raw.split('/',1)[1] if '/' in raw and raw!='/dev/null' else None
  m=re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',l)
  if m:
   oldn=int(m[2] if m[2] is not None else 1);newn=int(m[4] if m[4] is not None else 1);before=[];after=[];changes=[];line=i+1;i+=1
   while i<len(ls) and (oldn or newn):
    z=ls[i];i+=1
    if z=='' and oldn>0 and newn>0:z=' ' # GNU patch accepts an empty context line
    if z.startswith('\\'):continue
    if z.startswith(' '):before.append(z[1:]);after.append(z[1:]);oldn-=1;newn-=1
    elif z.startswith('-'):before.append(z[1:]);changes.append(z);oldn-=1
    elif z.startswith('+'):after.append(z[1:]);changes.append(z);newn-=1
    else:raise ValueError('unsupported hunk line '+str(i))
   if oldn or newn:raise ValueError('incomplete hunk')
   out.append(dict(target=target,line=line,before=before,after=after,changes=changes))
   continue
  i+=1
 return out
def locate(lines,seq):
 if not seq:return []
 return [i+1 for i in range(len(lines)-len(seq)+1) if lines[i:i+len(seq)]==seq]
leads=json.loads((B/'inherited-inputs.json').read_text());native=json.loads((B/'native-inputs.json').read_text());out=[]
for lead in leads:
 h=hunks(lead['patch_text']);record=dict(index=lead['index'],patch=lead['patch'],override=lead['override'],patch_sha256=lead['sha256'],hunks=len(h),counterparts=[],source=[])
 for n in native:
  if not n['path'].startswith(lead['override']+'/patches/'):continue
  try:nh=hunks(blob(n['referent']))
  except ValueError:continue
  canon=lambda rows:[(x['target'],x['changes']) for x in rows]
  if h and canon(h)==canon(nh):record['counterparts'].append(dict(path=n['path'],kind='all ordered changed lines and targets identical; hunk context not asserted equal',sha256=n['patch_sha256']))
 names=[lead['override'].split('/')[-1]] if lead['index']!=1 else ['u-boot-DDR3','u-boot-DDR4']
 for name in names:
  rp=B/'inherited-source'/f'{name}.json';receipt=json.loads(rp.read_text());s={'receipt':str(rp.relative_to(A)),'pin':receipt['pin'],'status':receipt['status'],'hunks':[]}
  if receipt['status']=='qualified raw source':
   root=pathlib.Path(receipt['scratch'])
   for unit in h:
    target=root/unit['target'] if unit['target'] else None;lines=target.read_text(errors='replace').splitlines() if target and target.is_file() else []
    s['hunks'].append(dict(target=unit['target'],patch_line=unit['line'],before_sha256=sha('\n'.join(unit['before'])),after_sha256=sha('\n'.join(unit['after'])),before_at=locate(lines,unit['before']),after_at=locate(lines,unit['after']),changed_lines=unit['changes'],source_sha256=sha(target.read_text(errors='replace')) if target and target.is_file() else None))
  record['source'].append(s)
 out.append(record)
(B/'inherited-hunks.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
for x in out:
 print('I%02d'%x['index'],'counterpart:',','.join(z['path'].split('/patches/')[-1] for z in x['counterparts']) or 'none', 'raw source:',[(s['pin'],s['status'],sum(bool(h['after_at']) for h in s['hunks']),sum(bool(h['before_at']) for h in s['hunks']),x['hunks']) for s in x['source']])
