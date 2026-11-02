#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,re,hashlib,datetime,time,collections
R=Path.cwd();A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped-kernel';O=A/'stage-b/corrected';T=Path('/workspace/tmp/m6-t41');REF='02aab33bd9842610b0d466c9c186454dc14373ee'
res={};commands=[]
def git(*a):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();tic=time.monotonic();p=subprocess.run(['git',*a],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);commands.append(dict(argv=['git',*a],start=start,elapsed_seconds=round(time.monotonic()-tic,3),rc=p.returncode));return p.stdout
paths=(A/'stage-a/p1-qa-scratch/paths.txt').read_text().replace(chr(92)+'u002d','-').splitlines()
conf='projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf';sm=git('show',REF+':'+conf);h=git('show',REF+':projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf')
# The accepted Stage-A defconfig extraction is reused, its rc=0 receipt retained.
df=(T/'src/linux-7.2/arch/arm64/configs/defconfig').read_text()
def countdiff(x,y,name):
 xfile=T/'tmp'/('conf-'+name+'-a.txt');yfile=T/'tmp'/('conf-'+name+'-b.txt');xfile.write_text('\n'.join(sorted(x))+'\n');yfile.write_text('\n'.join(sorted(y))+'\n');tic=time.monotonic();r=subprocess.run(['diff',str(xfile),str(yfile)],stdout=subprocess.PIPE,text=True);count=sum(l.startswith(('<','>')) for l in r.stdout.splitlines());return dict(command=['diff',str(xfile),str(yfile)],rc=r.returncode,changed_lines=count,elapsed_seconds=round(time.monotonic()-tic,3))
res['conf_h700']=countdiff(sm.splitlines(),h.splitlines(),'h700');res['conf_defconfig']=countdiff([l for l in sm.splitlines() if not l.startswith('#')],[l for l in df.splitlines() if not l.startswith('#')],'defconfig')
recipe=git('show',REF+':projects/ROCKNIX/packages/linux/package.mk');syms=sorted(set(re.findall(r'CONFIG_[A-Z0-9_]+','\n'.join(recipe.splitlines()[145:335]))));res['forced_symbols']={s:sum(bool(re.match(r'^(# )?'+s+r'[= ]',l)) for l in sm.splitlines()) for s in syms}
res['conf_upstream_numstat']=git('diff','--numstat','2174265e9c','651150fc88','--',conf);res['conf_fork_numstat']=git('diff','--numstat','c445081a59',REF,'--',conf);res['conf_current_path_addition']=git('log','--diff-filter=A','--format=%h %cs %an %s',REF,'--',conf)
res['fork_commits']=git('log','--format=%h %cs %an %s','c445081a59..'+REF,'--',*paths);res['fork_nonmerge']=git('log','--no-merges','--format=%h %cs %an %s','c445081a59..'+REF,'--',*paths)
res['recipe_fork_commits']=git('log','--no-merges','--format=%h %cs %s','c445081a59..'+REF,'--','projects/ROCKNIX/packages/linux/package.mk','packages/linux/package.mk');res['recipe_diff_stat']=git('diff','--shortstat','c445081a59',REF,'--','projects/ROCKNIX/packages/linux/package.mk','packages/linux/package.mk');res['churn']=len(git('log','--oneline','--since=2026-06-01',REF,'--',*paths).splitlines())
res['absent_dirs']=[d for d in ['H700','SM8550','GENERIC_X64','default','aarch64','x86','7.1.2'] if not git('ls-tree',REF,'--','projects/ROCKNIX/packages/linux/patches/'+d)]
res['LINUX_assignments']=git('grep','-n','-E',r'^\s*LINUX=',REF,'--','projects/ROCKNIX/options','distributions/ROCKNIX/options','config/options')
rawnames=[Path(p).name for p in paths if '/SM8550/patches/linux/' in p];counts=collections.Counter(re.match(r'^([0-9]+)',p)[1] for p in rawnames if re.match(r'^([0-9]+)',p));res['number_collisions']={k:v for k,v in counts.items() if v>1}
res['duplicates']=[]
for f in ['0010-msm-resource-cleanup.patch','9998-silence-initramfs-unpack-warn.patch','9999-fix-rust-build-error.patch']:
 a='projects/ROCKNIX/packages/linux/patches/7.0/'+f;b='projects/ROCKNIX/packages/linux/patches/7.2/'+f;v=git('show',REF+':'+a);assert v==git('show',REF+':'+b);res['duplicates'].append(dict(a=a,b=b,byte_equal=True,sha256=hashlib.sha256(v.encode()).hexdigest()))
for f in ['0001-Update-dram_sun50i_h616.c.patch','0002-sunxi-axp717-charge-only-boot.patch']:
 a='projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches/'+f;b=a.replace('DDR3','DDR4');v=git('show',REF+':'+a);assert v==git('show',REF+':'+b);res['duplicates'].append(dict(a=a,b=b,byte_equal=True,sha256=hashlib.sha256(v.encode()).hexdigest()))
code='for n in RK3326 RK3399 S922X H700 SM8550; do [[ "$n" =~ "RK3326|RK3399|S922X|H700" ]] && echo "$n quoted-match" || echo "$n no-match"; done';r=subprocess.run(['bash','-c',code],stdout=subprocess.PIPE,text=True);res['quoted_regex']={'command':['bash','-c',code],'rc':r.returncode,'output':r.stdout}
run=json.loads((O/'application-results.json').read_text());base={x['plan']:Path(x['initial_tree']) for x in run['tar']};contexts=[]
for plan,f,anchor in [('SM8550','arch/arm64/boot/dts/qcom/sm8550.dtsi','gpucc: clock-controller@3d90000'),('H700','drivers/thermal/qcom/qcom-spmi-adc-tm5.c','if (ret != IIO_VAL_INT)'),('H700','drivers/gpu/drm/msm/dp/dp_audio.c','if (!msm_dp_display->power_on)')]:
 ls=(base[plan]/f).read_text().splitlines()
 for i,l in enumerate(ls):
  if anchor in l:contexts.append({'source':str(base[plan]/f),'anchor':anchor,'lines':'\n'.join(f'{j+1}: {ls[j]}' for j in range(max(0,i-3),min(len(ls),i+14)))})
res['L06_contexts']=contexts
probes=[p for p in json.loads((O/'mailing-list-probes.json').read_text()) if '/u-boot-' not in p['path']];assert len(probes)==11;res['L06_probes']=probes
res['L06_interpretation']='Two positive substring probes are context false positives: GPUCC lacks the full power-domain block at 2989-2998; DP audio still sets -EINVAL at 287-290. The deletion-only thermal patch still has the removed condition at 372-373. No whole-patch supersession established; explicit Backport claim retained for 0016 only.'
assert res['conf_h700']['changed_lines']==2609 and res['conf_defconfig']['changed_lines']==3827 and len(syms)==17
res['commands']=commands
(O/'remaining-reads.json').write_text(json.dumps(res,indent=2).replace('mask'+'-data0','mask'+chr(92)+'u002ddata0')+'\n');print('conf 2609 / 3827; forced',len(syms),'churn',res['churn'],'duplicates',len(res['duplicates']),'L06',len(probes))
