#!/usr/bin/env python3
"""New pins-read records only: Git object reads and literal numbered quotations."""
from pathlib import Path
import datetime,hashlib,json,re,subprocess,time
R=Path.cwd();A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped-kernel';D=A/'stage-h/pins-read-correction'
SOURCE='02aab33bd9842610b0d466c9c186454dc14373ee'
START='61a1a674c10d520f9d93748c5a73deaadb08b158'
RECIPE='projects/ROCKNIX/packages/linux/package.mk'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==START
assert not D.exists(),'fresh packet required'
D.mkdir(parents=True);(D/'produce.py').write_bytes(Path(__file__).read_bytes())
checks=[];raw={}
for label,ref in [('source',SOURCE),('handback',START)]:
 argv=['git','show',ref+':'+RECIPE];start=stamp();tic=time.monotonic();p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (D/(label+'.git-show.out')).write_bytes(p.stdout);(D/(label+'.git-show.err')).write_bytes(p.stderr)
 checks.append(dict(label=label,argv=argv,cwd=str(R),start=start,end=stamp(),elapsed_seconds=round(time.monotonic()-tic,6),rc=p.returncode,stdout=label+'.git-show.out',stderr=label+'.git-show.err',stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr)))
 assert p.returncode==0 and not p.stderr;raw[label]=p.stdout
assert raw['source']==raw['handback']==(R/RECIPE).read_bytes()
ls=raw['source'].decode().splitlines(keepends=True)
versions=[i for i,l in enumerate(ls,1) if re.match(r'^\s*PKG_VERSION=',l)]
dirs=[i for i,l in enumerate(ls,1) if re.match(r'^\s*PKG_PATCH_DIRS\+?=',l)]
conditional=[i for i,l in enumerate(ls,1) if 'PKG_PATCH_DIRS' in l and i not in dirs]
cases=[i for i,l in enumerate(ls,1) if 21<i<53 and re.match(r'^  [A-Z0-9_|]+\)',l)]
assert versions==[23,30,37,43,49] and dirs==[16,27,40,46] and conditional==[18] and cases==[22,29,36,42,48]
numbers=sorted(versions+dirs+conditional+cases);quote=''.join(f'{i:6d}\t{ls[i-1]}' for i in numbers)
(D/'numbered-assignments-and-cases.out').write_text(quote)
counts=f'PKG_VERSION assignments {len(versions)}; anchored PKG_PATCH_DIRS assignments {len(dirs)}; separate conditional PKG_PATCH_DIRS append {len(conditional)}; assignments total {len(versions)+len(dirs)+len(conditional)}; case labels {len(cases)}\n'
(D/'counts.out').write_text(counts)
now=stamp()
paragraph=f"""
## Pins-read presentation correction — {now}

New records under D-WORKFLOW-226's failed-predicate rule, explicitly dispatched by the coordinator before final acceptance. This corrects the base brief §10 count/presentation gap only. The old “5 PKG_VERSION / 2 PKG_PATCH_DIRS” count is not the whole recipe: the command-derived census is:

{counts}
Source: {SOURCE}:{RECIPE}. The same complete recipe bytes were read at prior hand-back {START}; both raw git-show outputs, exact argv/cwd/UTC/exit and SHA256 are retained in stage-h/pins-read-correction/. Whole-recipe SHA256: {sha(raw['source'])}. Read-only commands were git show with those exact immutable ref:path arguments; no shell evaluation, recipe sourcing or configuration helper ran.

The following fifteen numbered lines are copied literally, in source order, from that immutable recipe. They include all ten assignments (five versions, four anchored patch-directory assignments and the separate conditional append) plus all five case labels:

"""
paragraph+=chr(96)*3+'text\n'+quote+chr(96)*3+'\n'
paragraph+="""
**Whole-recipe context versus selected T41 pins.** RK3588's full commit pin at line23, RK3576/RK3566's 7.0.2 at line43, and S922X/RK3399's 6.18.49 at line49 are recipe context only; they add no selected T41 row or application. H700 and SM8550 select the 7.2 branch at line30; GENERIC_X64 selects 7.1.2 at line37. The four selected current pins across T41 remain 7.2, 7.1.2, v2026.01 (the four H700 U-Boot rows), and 20260309 (the firmware row). U-Boot and firmware pins belong to their own recipes, not this Linux case. The 7.0 values at lines40/46 are patch-directory additions, not a new selected current kernel version.

Line16 is the default directory assignment; line18 conditionally appends mainline-rockchip for RK devices; line27 replaces directories in RK3588's case; lines40/46 append 7.0 in their respective cases. These literal lines describe the whole recipe without evaluating its variables or widening T41's selected-source scope.

Membership stays 107 paths (106 patches/one configuration), selected pins and 120 accepted application records unchanged. All accepted A–D artifacts, the formal generator, and both final/first-attempt D228 packets remain byte-identical to the prior published tip. No application, generator, accepted control, extraction, source/config evaluation, merge, runtime/host/provider/device/cloud action or permission answer is authorized or performed by this correction.
"""
(A/'02-forward-audit.md').open('a').write(paragraph)
entry=f'\n## Pins-read bounded records correction — {now}\n\nExplicit coordinator dispatch under D226 before final acceptance. New immutable git-show reads of {SOURCE}:{RECIPE} and {START}:{RECIPE} match byte-for-byte. stage-h/pins-read-correction/read-record.json and both complete raw outputs retain actual commands, times, exits and hashes; numbered-assignments-and-cases.out is quoted literally in 02. '+counts.strip()+' Selected T41 pins remain 7.2/7.1.2/v2026.01/20260309; other Linux case versions are whole-recipe context only. No accepted producer/control replay, source/config evaluation or product edit. Existing source/runtime/permission boundaries remain. Actual Codex / GPT-6-Astra / xhigh, T3 wN:p6, session 01a19d12-29e3-7fe0-9f41-038dac0a5deb; observed footer, not provider-attested. Current new-record checks and both resolution lints follow, then normal clean publication and stop for coordinator.\n'
(A/'00-running-log.md').open('a').write(entry)
p=R/'.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md';s=p.read_text()
s=re.sub(r'(?m)^> \*\*Last updated:\*\*.*$', '> **Last updated:** '+now+' by Codex / GPT-6-Astra / xhigh, T3 wN:p6, session 01a19d12-29e3-7fe0-9f41-038dac0a5deb; observed footer, not provider-attested.',s)
s=s.replace('## Current focus — records-only E–H complete; final publication and coordinator acceptance','## Current focus — bounded pins-read quotation correction; coordinator acceptance pending')
s=s.replace('## Immediate next action — final clean publication, then idle for coordinator','## Immediate next action — publish bounded pins-read records correction, then idle')
s=s.replace('Publish the final H packet, update only #688 commit headers, post one clean hand-back and deliver it to m6-coordinator wN:p2; then idle for coordinator simulated integration/final acceptance.','Prior H hand-back 6586647714 published clean tip 61a1a674c10d520f9d93748c5a73deaadb08b158. The explicitly dispatched pins-read presentation correction appends all ten literal assignments and five case labels to 02, with new immutable git-show receipts in stage-h/pins-read-correction. Whole-recipe context is distinguished from selected T41 pins; counts/source unchanged. Run current new-record checks and both resolution lints, commit/push this bounded correction, update #688 final header/checkpoint to one clean tip and return to wN:p2; then idle for coordinator acceptance.')
p.write_text(s)
log=R/'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'
log.open('a').write('\n## '+now+' — #688 T41 pins-read quotation correction\n\nNew read-only evidence corrects the brief count/presentation gap: five PKG_VERSION assignments, four anchored PKG_PATCH_DIRS assignments plus one separate conditional append, and five case labels, all literal numbered source lines appended to 02. Source and prior hand-back recipe bytes match exactly; full output/argv/time/hash receipts retained under stage-h/pins-read-correction. Whole-recipe versions do not widen selected pins or membership. Accepted A–D and both D228 packets remain untouched. No producer/control replay, source/config evaluation, product, runtime or permission action. Coordinator retains count erratum, final acceptance and integration.\n')
record=dict(result='PASS',source_ref=SOURCE,prior_tip=START,source_path=RECIPE,source_sha256=sha(raw['source']),numbered_sha256=sha(quote.encode()),version_lines=versions,anchored_dirs_lines=dirs,conditional_dirs_lines=conditional,case_label_lines=cases,checks=checks,builder_sha256=sha(Path(__file__).read_bytes()),scope='New records; read Git bytes only; no accepted execution replay')
(D/'read-record.json').write_text(json.dumps(record,indent=2)+'\n')
print(counts,end='');print('recipe SHA256',record['source_sha256']);print('New literal quotation PASS')
