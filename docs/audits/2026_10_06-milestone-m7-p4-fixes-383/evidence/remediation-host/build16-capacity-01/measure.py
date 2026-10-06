from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
p=Path(__file__).resolve().parent
root=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15/build.pixelelated-GENERIC_X64.x86_64')
(p/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
    r=subprocess.run(['du','-sx','-B1',str(root)],text=True,capture_output=True)
    (p/'du.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
    cache=int(r.stdout.split()[0]);free=os.statvfs('/workspace').f_bavail*os.statvfs('/workspace').f_frsize
    reserves={'build_growth':40*1024**3,'qa':80*1024**3,'host_margin':100*1024**3}
    needed=cache+sum(reserves.values());result=dict(verified_utc=datetime.now(timezone.utc).isoformat(),cache_parent=str(root),cache_allocated_bytes=cache,free_bytes=free,reserves_bytes=reserves,required_bytes=needed,margin_after_requirement=free-needed,capacity_sufficient=free>=needed,scope='Read-only estimate for independent replacement16 copy. Recheck available bytes immediately before allocation; no cleanup or reserve changes authorized.')
    (p/'capacity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
    assert free>=needed,'capacity estimate insufficient'
    rc=0
finally:
    (p/'inner.rc').write_text(str(rc)+'\n');(p/'outer.rc').write_text(str(rc)+'\n')
raise SystemExit(rc)
