#!/usr/bin/env python3
"""T41 formal audit-local generator, adapted from T40's asserted tables/header/hash modes.

Read-only outputs: stats | provenance | coverage | currency | json.
Stage C: reads current HEAD source bytes and retained Stage-B receipts; writes stdout only.
Reads the retained P1 TSV-derived rows, metadata reads and corrected applications.
"""
from pathlib import Path
import argparse,collections,json,re,subprocess,hashlib
p=argparse.ArgumentParser();p.add_argument('mode',choices=['stats','provenance','coverage','currency','json']);p.add_argument('--rows-from');p.add_argument('--bytes-from');a=p.parse_args()
A=Path(__file__).resolve().parents[1];R=A.parents[2];O=A/'stage-b/corrected'
SOURCE_REF='02aab33bd9842610b0d466c9c186454dc14373ee'
REF=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
def dec(s):return s.replace(chr(92)+'u002d','-')
def esc(s):return str(s).replace('mask'+'-data0','mask'+chr(92)+'u002ddata0').replace('|',r'\|').replace('\n','; ')
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,errors='replace')
rows=json.loads(Path(a.rows_from or O/'inventory-rows.json').read_text());[r.update(path=dec(r['path'])) for r in rows]
assert len(rows)==107,'membership: expected 107 rows'
assert len({r['path'] for r in rows})==107,'membership: duplicate path'
assert collections.Counter(r['reach'] for r in rows)=={'shipped':103,'test':4},'reach: expected shipped 103/test 4'
assert sum(r['lines'] for r in rows)==40474,'lines: expected 40474'
assert sum(r['path'].endswith('.patch') for r in rows)==106 and sum(r['path'].endswith('.conf') for r in rows)==1,'kind: expected patch 106/conf 1'
groups=['projects/ROCKNIX/packages/linux/patches/'+v for v in ['7.0','7.2','mainline']]+['projects/ROCKNIX/devices/H700/patches/linux','projects/ROCKNIX/devices/SM8550/patches/linux','projects/ROCKNIX/devices/SM8550/linux','projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches','projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/patches','projects/ROCKNIX/packages/linux-firmware/kernel-firmware/patches']
gc=collections.Counter(str(Path(r['path']).parent) for r in rows);assert [gc[g] for g in groups]==[4,6,4,32,55,1,2,2,1],'directory counts changed'
reach=collections.Counter(tuple(r['reachable_by']) for r in rows);assert len(reach)==7 and sorted(reach.values())==sorted([4,32,56,1,4,6,4]),'reachable_by groups changed'
meta={dec(m['path']):m for m in json.loads((O/'path-metadata.json').read_text())}
app=json.loads((O/'application-results.json').read_text());ar=app['rows'];assert app['complete'] and app['source_ref']==SOURCE_REF
assert len(ar)==120 and len({dec(r['path']) for r in ar})==106,'application coverage: expected 120 / 106'
counts=collections.Counter(r['plan'] for r in ar);plans=['GENERIC_X64','H700','SM8550','UBOOT-DDR3','UBOOT-DDR4','FIRMWARE'];assert [counts[x] for x in plans]==[8,42,65,2,2,1],'plan counts changed'
byapp=collections.defaultdict(list)
for x in ar:
 byapp[dec(x['path'])].append(x)
 if x['attempted']:
  assert x['input_tree_sha256']==x['after_dry_tree_sha256'],'diagnostic mutated tree'
  assert x['promoted']==(x['apply_rc']==0),'failed candidate promoted'
  for k in ['dry','apply']:assert hashlib.sha256((O/x[k]['output']).read_bytes()).hexdigest()==x[k]['output_sha256'],'receipt changed'
 else:assert x['status']=='open item' and x['blocked_by'] and x['apply_rc'] is None and 'apply' not in x,'invented blocked command'
raw={}
for r in rows:
 path=r['path'];alt=Path(a.bytes_from)/path if a.bytes_from else None
 baseline=git('show',REF+':'+path)
 assert baseline==git('show',SOURCE_REF+':'+path),'source bytes changed since accepted application receipts'
 raw[path]=alt.read_text() if alt and alt.exists() else baseline
headers={}
for path,data in raw.items():
 ls=data.splitlines();h={}
 for i,l in enumerate(ls[:60]):
  if l.startswith('From: ') and 'from' not in h:h['from']=l[6:]
  if l.startswith('Subject: ') and 'subject' not in h:
   sub=l[9:];j=i+1
   while j<len(ls) and ls[j].startswith((' ','\t')):sub+=' '+ls[j].strip();j+=1
   h['subject']=sub
 headers[path]=h
assert sum(bool(h.get('from')) for h in headers.values())==87,'From header census: expected 87'
assert sum(bool(h.get('subject')) for h in headers.values())==89,'Subject header census: expected 89'
assert sum(len(v.splitlines()) for v in raw.values())==40474,'source line count changed'
assert sum(v.count('\n') for v in raw.values())==40473,'source newline count changed'
def hashes(text):
 i=text.find('diff --git');i=text.find('--- ') if i<0 else i;b=text[i:].splitlines()
 h=lambda ls:hashlib.sha256('\n'.join(ls).encode()).hexdigest()
 return [h([l for l in b if not l.startswith('index ')]),h([l for l in b if not l.startswith(('index ','diff --git','--- ','+++ ','@@'))]),h([l for l in b if l[:1] in '+-' and not l.startswith(('+++ ','--- '))])]
pairs=json.loads((O/'remaining-reads.json').read_text())['duplicates'];assert len(pairs)==5
for pair in pairs:
 assert raw[pair['a']]==raw[pair['b']],'byte-identical sibling drift'
 assert hashes(raw[pair['a']])==hashes(raw[pair['b']]),'T40 three-level duplicate check drift'
pins={'GENERIC_X64':'7.1.2 (37198c93727be247)','H700':'7.2 (f9fef3d14c0df538)','SM8550':'7.2 (f9fef3d14c0df538)','UBOOT-DDR3':'v2026.01 (03bb43c58d2343ee)','UBOOT-DDR4':'v2026.01 (03bb43c58d2343ee)','FIRMWARE':'20260309 (28fb1b57fa9531ed)'}
out=[]
for r in sorted(rows,key=lambda x:x['path']):
 path=r['path'];m=meta[path];h=headers[path];apps=byapp[path];conf=path.endswith('.conf');non=('/u-boot-' in path or '/kernel-firmware/patches/' in path);kind='conf' if conf else 'non-kernel' if non else 'patch';owner='T27' if '/u-boot-' in path else 'T11' if '/kernel-firmware/' in path else 'T41'
 upstream='changed upstream' if m['vs_upstream']=='CHANGED' else 'fork-written' if '0950-' in path else 'moved upstream' if m['vs_upstream']=='ABSENT' else 'carried'
 disp='upstream-changed' if upstream=='changed upstream' else '#585' if upstream=='fork-written' else 'upstream-moved' if upstream=='moved upstream' else 'keep'
 if any(x['status']=='fails' for x in apps):disp='bug'
 elif any(x['status']=='open item' for x in apps):disp='open item'
 bp='a backport' if any('Upstream-Status: Backport' in x for x in m['claims']) else 'unknown'
 origin=h.get('from') or ('configuration; no mail header' if conf else 'unknown (header absent)')
 subject=h.get('subject') or ('SM8550 kernel configuration' if conf else 'hand-made; exact original authorship unknown')
 reason=(m['adding_commits'].splitlines()[0] if m['adding_commits'] else 'unknown')+'; '+(h.get('subject') or 'device-specific intent only as the carrying commit states')
 if conf:reason='Carried SM8550 7.2 configuration, unchanged from merge base; git --follow ancestry retained in metadata, not a device-specific authorship claim.'
 applied='; '.join(f'{x["plan"]}[{x["index"]:03d}] {x["status"]} (apply_rc={x["apply_rc"]}, dry_rc={x["dry_rc"]}; rows/{x["plan"]}-{x["index"]:03d}.json)' for x in apps) if apps else 'open item: configuration selection read; no oldconfig/build authorized'
 pin='; '.join(f'{x["plan"]} {pins[x["plan"]]}' for x in apps) if apps else 'SM8550 aarch64/arm: 7.2 (f9fef3d14c0df538)'
 method='patch -p1 -N --batch; complete application authoritative; original dry-run diagnostic retained'
 if conf:method='H700 sorted diff 2609; pristine arm64 defconfig noncomment diff 3827; forced symbols 17 (15 present/2 absent); upstream 7+/7-; kernel_config_path nine candidates, oldconfig; adjust/check helpers never run'
 note='header claims unverified: '+'; '.join(m['claims']) if m['claims'] else 'no header upstream-status claim'
 if '0010-msm-resource' in path:note+='; L-01 pre-fix pointer defect; applies does not imply correct; CONFIG_DRM_MSM=y only SM8550 among these plans'
 if '/0501-' in path:note+='; SoC serial-derived radio addresses; D-CLOUD-068'
 if '/0105-' in path:note+='; il97680a,rpnova is the Nova panel'
 out.append(dict(path=path,lines=r['lines'],kind=kind,directory=str(Path(path).parent),reach=r['reach'],reachable_by=r['reachable_by'],owner=owner,origin=origin,subject=subject,target_version=('unknown' if not h.get('from') and h.get('subject') and m['target_version']=='hand-made' else m['target_version']),first_target=m['first_target'],files_hunks=f'{m["files"]} file sections / {m["hunks"]} hunks',pin=pin,applies=applied,upstream=upstream,backport=bp,reason=reason,disposition=disp,method=method,note=note))
assert len(out)==107 and sum(collections.Counter(x['disposition'] for x in out).values())==107
stats={'rows':len(out),'lines':sum(x['lines'] for x in out),'patch':106,'conf':1,'directory_counts':dict(zip(groups,[gc[g] for g in groups])),'reachable_by_sizes':list(reach.values()),'From':87,'Subject':89,'plan_applications':dict(counts),'application_status':dict(collections.Counter(x['status'] for x in ar)),'blocked':sum(not x['attempted'] for x in ar),'dispositions':dict(collections.Counter(x['disposition'] for x in out)),'upstream_status':dict(collections.Counter(x['upstream'] for x in out)),'backport_status':dict(collections.Counter(x['backport'] for x in out)),'target_versions_by_kind':{k:dict(collections.Counter(x['target_version'] for x in out if x['kind']==k)) for k in ['patch','conf','non-kernel']},'pins_by_plan':pins}
if a.mode=='stats':print(json.dumps(stats,indent=2))
elif a.mode=='json':print(json.dumps(out,indent=2).replace('mask'+'-data0','mask'+chr(92)+'u002ddata0'))
elif a.mode=='provenance':
 fields=['path','lines','kind','directory','reachable_by','origin','subject','first_target','files_hunks','target_version','pin','applies','upstream','backport','reason','disposition','owner','method','note']
 print('| '+' | '.join(fields)+' |');print('| '+' | '.join('---' for f in fields)+' |')
 for x in out:print('| `'+esc(x['path'])+'` | '+' | '.join(esc(', '.join(x[f]) if isinstance(x[f],list) else x[f]) for f in fields[1:])+' |')
elif a.mode=='coverage':
 print('| Path | Lines | Kind | Reach | Disposition |');print('| --- | ---: | --- | --- | --- |')
 for x in out:print(f'| `{esc(x["path"])}` | {x["lines"]} | {x["kind"]} | {x["reach"]} | {x["disposition"]} |')
elif a.mode=='currency':
 print('| Change | Path | Disposition |');print('| --- | --- | --- |')
 for l in (O/'upstream-delta.txt').read_text().splitlines():
  change,path=l.split('\t',1);detail=' (polldev moved to RK3326; fe5216ff69, unchanged blob)' if change=='D' else ''
  print(f'| {change} | `{esc(path)}` | the integration carries (#563/#559){detail} |')
