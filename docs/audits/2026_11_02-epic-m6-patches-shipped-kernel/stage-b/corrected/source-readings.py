#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,re,hashlib,time,datetime,collections,ast
R=Path.cwd(); A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped-kernel';O=A/'stage-b/corrected';REF='02aab33bd9842610b0d466c9c186454dc14373ee';U='651150fc88'; MB='c445081a59'
records=[]
def esc(s):return s.replace('mask'+'-data0','mask'+chr(92)+'u002ddata0')
def save(name,s): (O/name).write_text(esc(s))
def git(*args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();tic=time.monotonic();r=subprocess.run(['git',*args],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 records.append({'argv':['git',*args],'start':start,'elapsed_seconds':round(time.monotonic()-tic,3),'rc':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest()})
 return r.stdout.decode(errors='replace')
def blob(path,ref=REF):return git('show',ref+':'+path)
def numbered(s):return '\n'.join(f'{i}: {l}' for i,l in enumerate(s.splitlines(),1))
paths=(A/'stage-a/p1-qa-scratch/paths.txt').read_text().replace(chr(92)+'u002d','-').splitlines();meta=[]
for p in paths:
 data=blob(p);ls=data.splitlines();h=ls[:60];origin=next((l[6:].strip() for l in h if l.startswith('From: ')),None);subject=next((l[9:].strip() for l in h if l.startswith('Subject: ')),None);date=next((l[6:].strip() for l in h if l.startswith('Date: ')),None)
 headers=[l for l in ls if l.startswith(('Link:','Upstream-Status:'))];targets=[]
 for l in ls:
  if l.startswith('+++ ') and len(l[4:].split()) and l[4:].split()[0]!='/dev/null':
   q=l[4:].split()[0];targets.append(q.split('/',1)[1] if '/' in q else q)
 sha=re.search(r'^From ([a-f0-9]{40}) ',data,re.M)
 version=(sha.group(1) if sha and sha.group(1)!='0'*40 else date or ('hand-made' if not origin else 'unknown')) if p.endswith('.patch') else 'Linux/arm64 7.2.0 header'
 upstream=git('rev-parse','--verify',U+':'+p).strip();own=git('rev-parse',REF+':'+p).strip();base=git('rev-parse','--verify',MB+':'+p).strip()
 adding=git('log','--follow','--diff-filter=A','--format=%H %cs %an %s',REF,'--',p).strip()
 m=dict(path=p,lines=len(ls),newlines=data.count('\n'),from_header=origin,subject=subject,date=date,claims=headers,target_version=version,first_target=targets[0] if targets else 'kernel configuration',files=len(targets),unique_targets=sorted(set(targets)),hunks=sum(l.startswith('@@') for l in ls),adding_commits=adding,upstream_blob=upstream,source_blob=own,base_blob=base,vs_upstream='ABSENT' if not upstream else 'SAME' if upstream==own else 'CHANGED',vs_base='ABSENT' if not base else 'SAME' if base==own else 'CHANGED',header_excerpt='\n'.join(h))
 meta.append(m)
save('path-metadata.json',json.dumps(meta,indent=2)+'\n')
# The narrow source reads required by the floor, without sourcing recipes.
notes=[]
def section(title,body):notes.append('## '+title+'\n\n'+body+'\n')
RAMP='projects/ROCKNIX/devices/H700/patches/linux/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch';section('Ramoops, all 38 lines',numbered(blob(RAMP)))
for d in ['H700','SM8550','GENERIC_X64']:
 ext='x86_64' if d=='GENERIC_X64' else 'aarch64';data=blob(f'projects/ROCKNIX/devices/{d}/linux/linux.{ext}.conf')
 chosen=[f'{i}: {l}' for i,l in enumerate(data.splitlines(),1) if re.match(r'^CONFIG_(PSTORE_RAM|PSTORE_CONSOLE|WATCHDOG_SYSFS|SOFTLOCKUP_DETECTOR|DETECT_HUNG_TASK|DEFAULT_HUNG_TASK_TIMEOUT|DRM_MSM)=',l) or i==3]
 section(d+' config evidence','\n'.join(chosen));opt=blob(f'projects/ROCKNIX/devices/{d}/options');section(d+' options','\n'.join(f'{i}: {l}' for i,l in enumerate(opt.splitlines(),1) if 'LINUX=' in l or 'KERNEL_TARGET' in l or 'TARGET_KERNEL_PATCH_ARCH' in l))
recipe=blob('projects/ROCKNIX/packages/linux/package.mk');section('Kernel override recipe, whole text',numbered(recipe))
section('Unpack, read only', '\n'.join(numbered(blob('scripts/unpack')).splitlines()[117:196]));section('Config resolution, read only','\n'.join(numbered(blob('config/functions')).splitlines()[1448:1472]));section('arm patch arch',numbered(blob('config/arch.arm')).splitlines()[79])
section('0010 upstream fix message',git('show','-s','--format=fuller','9416eec2c2'))
pair=['projects/ROCKNIX/packages/linux/patches/'+v+'/0010-msm-resource-cleanup.patch' for v in ['7.0','7.2']]
section('0010 diff and stat',git('diff','--stat',REF,U,'--',*pair)+git('diff',REF,U,'--',pair[1]))
section('0010 source patch opening','\n'.join(numbered(blob(pair[1])).splitlines()[:65]))
result=json.loads((O/'application-results.json').read_text());last=next(r for r in result['rows'] if r['plan']=='SM8550' and r['index']==65)
src=Path(last['candidate'])/'drivers/gpu/drm/msm/disp/dpu1/dpu_crtc.c';ls=src.read_text().splitlines();hits=[i for i,l in enumerate(ls) if 'cstate->num_mixers = 0' in l]
for hit in hits:section('Final SM8550 patched dpu_crtc.c around num_mixers reset','\n'.join(f'{i+1}: {ls[i]}' for i in range(max(0,hit-22),min(len(ls),hit+28))))
section('0010 intent history',git('log','--format=%h %cs %s','-S','cstate->num_mixers = 0',U,'--',pair[1]))
section('Polldev rename history',git('show','--stat','--format=fuller','fe5216ff69'))
section('Polldev consumers',git('grep','-n','-i','polldev',REF,'--','projects/ROCKNIX/devices/H700/patches/linux','projects/ROCKNIX/packages/linux-drivers/rocknix-joypad'))
section('BLS upstream history',git('show','-s','--format=fuller','cafbb1657d'))
section('Upstream recipe line 18','\n'.join(numbered(blob('projects/ROCKNIX/packages/linux/package.mk',U)).splitlines()[15:20]))
for p in ['projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch','projects/ROCKNIX/devices/SM8550/patches/linux/0105-drm-panel-Add-Retroid-Pocket-Nova-panel.patch','projects/ROCKNIX/devices/SM8550/patches/linux/0501-ROCKNIX-fix-wifi-and-bt-mac.patch']:
 data=blob(p);selected=[f'{i}: {l}' for i,l in enumerate(data.splitlines(),1) if re.search('rocknix-dt-id|rpnova|serial',l,re.I)];section(p,'\n'.join(selected))
section('dt-id consumer',git('grep','-n','rocknix-dt-id',REF,'--','projects/ROCKNIX/devices/H700/bootloader'))
section('New dispcc patch header','\n'.join(numbered(blob('projects/ROCKNIX/packages/linux/patches/7.2/0017-clk-qcom-blank-dsi-panels-before-dispcc-park.patch',U)).splitlines()[:20]))
# pristine source is the newly extracted initial tree, not a patched candidate.
ht=next(t for t in result['tar'] if t['plan']=='H700');pristine=Path(ht['initial_tree']);ls=(pristine/'arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi').read_text().splitlines();hit=next(i for i,l in enumerate(ls) if '0x40000000 0x0 0x40000' in l)
section('Pristine 7.2 ramoops context', '\n'.join(f'{i+1}: {ls[i]}' for i in range(hit-3,hit+6))+'\nramoops count: '+str(sum('ramoops' in l for l in ls)))
section('Ramoops fork/upstream history',git('log','--format=%h %cs %an %s',REF,'--',RAMP)+'ancestor rc '+str(subprocess.run(['git','merge-base','--is-ancestor','cbf75c0b06',U],cwd=R).returncode)+'\nupstream ramoops names: '+str(sum('ramoops' in p.lower() for p in git('ls-tree','-r','--name-only',U,'--','projects/ROCKNIX/devices/H700/patches/linux').splitlines())))
kd=['projects/ROCKNIX/packages/linux/patches','projects/ROCKNIX/devices/H700/patches/linux','projects/ROCKNIX/devices/SM8550/patches/linux','projects/ROCKNIX/devices/SM8550/linux'];delta=git('diff','--name-status',MB,U,'--',*kd);save('upstream-delta.txt',delta);section('Upstream delta',delta)
syms=[]
for l in git('ls-tree','-r',REF).splitlines():
 if l.startswith('120000'):
  p=l.split('\t')[1]
  if re.match(r'^(projects/ROCKNIX/(devices|packages/linux)|packages/linux)',p):syms.append(p+' -> '+blob(p).strip())
section('Symlinks under member roofs','\n'.join(syms))
section('Disabled siblings',git('ls-tree','-r','--name-only',REF,'--','projects/ROCKNIX/devices/H700/patches/linux','projects/ROCKNIX/devices/SM8550/patches/linux'))
# L-06: distinguish a matching added line from a full upstream merge.
probes=[]
for m in meta:
 p=m['path'];n=Path(p).name
 selected=(('/H700/' in p and n.startswith(('0002-','0008-','0110-','0126-','0160-'))) or ('/SM8550/' in p and n.startswith(('0006-','0120-','20260424_','v6_20260210_'))) or ('/7.2/' in p and n.startswith(('0011-','0016-'))))
 if not selected:continue
 first=m['first_target'];src=pristine/first
 if '/SM8550/' in p:src=Path(next(t for t in result['tar'] if t['plan']=='SM8550')['initial_tree'])/first
 text=blob(p);first_start=text.find('+++ ');part=text[first_start:].splitlines();end=next((i for i,l in enumerate(part[1:],1) if l.startswith('diff --git ')),len(part));added=[l[1:] for l in part[:end] if l.startswith('+') and not l.startswith('+++') and len(l[1:].strip())>=16]
 candidate=next((l for l in added if not l.lstrip().startswith(('#include','/*','*','//'))),added[0] if added else None)
 rawsrc=src.read_text(errors='replace') if src.exists() else '';count=sum(candidate in l for l in rawsrc.splitlines()) if candidate else None
 probes.append(dict(path=p,source=str(src),source_exists=src.exists(),first_target=first,probe=candidate,count=count,interpretation='Single added-line overlap probe only; does not establish complete patch supersession. Complete corrected application succeeds.'))
save('mailing-list-probes.json',json.dumps(probes,indent=2)+'\n')
save('source-readings.md','\n'.join(notes));save('source-readings-commands.json',json.dumps(records,indent=2)+'\n')
print('Metadata',len(meta),'source read sections',len(notes),'mailing-list probes',len(probes),'commands',len(records));print('upstream',dict(collections.Counter(m['vs_upstream'] for m in meta)));print('headers',sum(bool(m['from_header']) for m in meta),sum(bool(m['subject']) for m in meta))
