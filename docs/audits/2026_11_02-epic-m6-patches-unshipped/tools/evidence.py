#!/usr/bin/env python3
import datetime,hashlib,json,pathlib,re,subprocess
R=pathlib.Path(__file__).resolve().parents[1];C=R/'stage-b';B=json.loads((R/'stage-a/bindings.json').read_text());S=B['source'];U=B['upstream']
def git(*a):return subprocess.check_output(['git',*a])
def show(ref,p):return git('show',ref+':'+p)
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(C/n).write_text(json.dumps(x,indent=2)+'\n')
contexts=[('T25','9b9be6a9481e4e9ee5b9d97f6c7bb72eda3ca3b4','2026_10_25-epic-m6-devices-unshipped',[(109,129),(148,174),(291,307),(328,356)]),('T11','47672fe4a04fc3b69dee9f0381fbc9f076b891e5','2026_10_25-epic-m6-device-generic-x64-and-kernel',[(94,108),(136,146),(318,328)]),('T27','0ac98afe434c0429bace5f239482e5de0e0bc394','2026_10_25-epic-m6-device-h700',[(65,93)]),('T41','e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0','2026_11_02-epic-m6-patches-shipped-kernel',[(318,342),(548,565)]),('T42','4cf8c8820791624dbddad3eb3664101a03953a82','2026_11_02-epic-m6-patches-shipped',[(873,906)])]
prior=[]
for label,ref,folder,ranges in contexts:
 p='docs/audits/'+folder+'/02-forward-audit.md';raw=show(ref,p);lines=raw.decode().splitlines();prior.append({'label':label,'ref':ref,'path':p,'sha256':sha(raw),'excerpt':[[i+1,lines[i]] for a,z in ranges for i in range(a-1,min(z,len(lines)))],'method':'immutable read only; accepted producer not rerun; no application result transfers to T43'})
write('prior-context.json',prior)
rows=json.loads((C/'observations.json').read_text());conf=[];recipe='projects/ROCKNIX/packages/linux/package.mk';t=show(S,recipe).decode().splitlines();writers=[[i,l] for i,l in enumerate(t,1) if 'scripts/config ' in l or 'oldconfig' in l or 'PKG_KERNEL_CFG_FILE' in l or '@DISTRONAME@' in l or '@DEVICENAME@' in l]
for row in rows:
 if row['kind']!='config':continue
 p=row['path'];text=show(S,p).decode().splitlines();u=show(U,p);delta=git('diff','--numstat',S,U,'--',p).decode().strip() or '0\t0\t'+p
 conf.append({'path':p,'source_sha256':row['sha256'],'header':row['header'],'consumers':row['buildable_by'],'selected_path':p,'selection':'config/functions:1449-1471 version, LINUX, device precedence; native device path exists; no earlier version or LINUX override established','base_identical':row['base_identical'],'upstream_sha256':sha(u),'source_to_upstream_numstat':delta,'source_hostname':[[i,l] for i,l in enumerate(text,1) if l.startswith('CONFIG_DEFAULT_HOSTNAME=')],'source_RAID6':[[i,l] for i,l in enumerate(text,1) if 'RAID6_PQ_BENCHMARK' in l],'static_writers':writers,'missing':'No generated .config, oldconfig, compiler, boot or installed/runtime result; T11 historical built-config proof not transferred','owner':'T11 #658 kernel recipe; T25 #672 target context; T43 #690 config table'})
write('configurations.json',conf)
links=json.loads((R/'stage-a/source/symlinks.json').read_text());shared='projects/ROCKNIX/packages/apps/mangohud/patches/SM8550/0002-SM8750-Battery.patch'
for row in links:
 row['link_tree']=git('ls-tree',S,'--',row['path']).decode().strip();row['referent_tree']=git('ls-tree',S,'--',row['resolved']).decode().strip();row['owner']='T43 #690'
write('links.json',{'native':links,'shipped_context':{'path':shared,'tree':git('ls-tree',S,'--',shared).decode().strip(),'literal':show(S,shared).decode(),'owner':'T42 #689; context only'}})
write('upstream-kernel-context.json',{'ref':U,'path':recipe,'sha256':sha(show(U,recipe)),'lines':[[i,l] for i,l in enumerate(show(U,recipe).decode().splitlines(),1) if 16<=i<=65],'integration_owners':['#563','#559'],'limits':'7.2.6 is a directory selector, not 7.2.11 source version; no source adopted'})
write('upstream-scope-diff.json',{'argv':['git','diff','--name-status','-M',B['fork_base'],U,'--','projects/ROCKNIX/devices','projects/ROCKNIX/packages/linux/patches'],'output':git('diff','--name-status','-M',B['fork_base'],U,'--','projects/ROCKNIX/devices','projects/ROCKNIX/packages/linux/patches').decode()})
with (R/'01-research-notes.md').open('a') as f:f.write('\n## '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — Prior context comparison and config boundary\n\nAfter own first observations, read named immutable T25/T11/T27/T41/T42 contexts, bound in stage-b/prior-context.json. Existing #1101 unpack reach, T25 SM8750 hostname lead, T11 built-config results and T27 ATF paired URL/checksum remain inherited evidence. T42 #1410 owns the nested PPSSPP patch defect; no duplicate issue is inferred. T42 normal applications are not T43 proof. The 12 config records distinguish source headers, hostname and RAID6 options from static recipe writers and missing installed outputs. Fixed-upstream 7.2.6 is a patch selector; actual RK3566/RK3576/S922X source is 7.2.11. #563/#559 own uptake and polldev moves.\n')
print('Bound five immutable prior contexts, 12 config records, two native links and one T42 shared consumer.')
