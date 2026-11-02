import pathlib,subprocess,json,hashlib,datetime,re,shutil
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped';O=A/'stage-b/nested-patch';S=pathlib.Path('/workspace/tmp/m6-t42/nested-patch');REF='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1';O.mkdir(exist_ok=True);S.mkdir(exist_ok=False)
path='projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/patches/007-disable-home-pause.patch'
data=subprocess.check_output(['git','show',REF+':'+path],cwd=R);sha=lambda b:hashlib.sha256(b).hexdigest();out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'constructed source fixture, NOT applies-at-pin','path':path,'patch_sha256':sha(data),'tool':subprocess.check_output(['patch','--version']).decode().splitlines()[0],'runs':[]}
for mode in ['diagnostic','normal']:
 d=S/mode;d.mkdir();(d/'SDL').mkdir();(d/'SDL/SDLJoystick.cpp').write_text('SENTINEL unchanged original joystick source\n');cmd=['patch','-p1','-N','--batch']+(['--dry-run'] if mode=='diagnostic' else []);r=subprocess.run(cmd,input=data,cwd=d,capture_output=True,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'});(O/(mode+'.stdout')).write_bytes(r.stdout);(O/(mode+'.stderr')).write_bytes(r.stderr);out['runs'].append(dict(argv=cmd,cwd=str(d),rc=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr)));assert r.returncode==0;assert (d/'SDL/SDLJoystick.cpp').read_text()=='SENTINEL unchanged original joystick source\n'
created=S/'normal/package/batocera/emulators/ppsspp/007-disable-home-pause.patch';assert created.is_file();out['created_path']=str(created.relative_to(S/'normal'));out['created_sha256']=sha(created.read_bytes());out['source_unchanged']=True
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',REF],cwd=R).decode().splitlines();hits=[]
for p in paths:
 if p.endswith('.patch'):
  b=subprocess.check_output(['git','show',REF+':'+p],cwd=R)
  for l in b.decode(errors='replace').splitlines():
   if l.startswith('+++ ') and re.search(r'\.patch(?:\s|$)',l):hits.append(dict(path=p,header=l))
out['sibling_search']={'argv':['git','ls-tree','-r','--name-only',REF],'predicate':'every tracked *.patch; added-file +++ header ends .patch; inspect outer creation and inner +diff separately','hits':hits}
(O/'receipt.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS constructed nested-patch proof; source sentinel unchanged. Sibling headers',len(hits));print(json.dumps(hits,indent=2))
