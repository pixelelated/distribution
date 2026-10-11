from pathlib import Path
import subprocess,os,json,hashlib
p=Path(__file__).resolve().parent;r=Path.cwd();es=Path('/home/max/Development/emulationstation-next.worktrees/m7-qa19-gaps')
env={**os.environ,'TMPDIR':str(p),'ES_SRC':str(es)}
expected=json.loads((p/'source.json').read_text())['GuiMenu.cpp.sha256'];assert hashlib.sha256((es/'es-app/src/guis/GuiMenu.cpp').read_bytes()).hexdigest()==expected
steps=[('lifetime',['python3',str(es/'tests/cloud-oauth-lifetime.py')]),('governor',['python3',str(es/'tests/gpu-governor-save.py')]),('menumap',[str(r/'tools/es-menu-map-check')])]
rows=[]
for name,cmd in steps:
 with (p/(name+'.log')).open('w') as f:rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 rows.append({'name':name,'returncode':rc});(p/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print(name,rc,flush=True)
raise SystemExit(0 if all(x['returncode']==0 for x in rows) else 1)
